---
title: System design — Strict Full Plugin Architecture
type: reference
status: active
keywords: [plugin, architecture, core, isolation, event-bus, dependency-injection, manifest, lifecycle, versioning, fault-isolation, saga, contract-testing, security, observability]
related: [./README.md, ../../kit/new-project-scaffold.md]
summary: >
  Reference design for a strict Core + Plugins application. The Core provides infrastructure only; every
  business feature is an independent, self-contained plugin that can be removed without breaking the Core.
  Plugins never import each other — they communicate only through Core interfaces, the Event Bus, or shared
  services resolved via DI. This is the enforceable contract: responsibilities, the plugin manifest, load
  order, versioning, fault isolation, namespacing, shared-data ownership, security boundaries, contract
  testing, observability, and the CI gates that make every rule real instead of aspirational.
updated: 2026-06-29
---

# System Design — Strict Full Plugin Architecture

> **The one litmus test.** *Any plugin can be removed and the Core still boots, and every other plugin still
> works.* Every rule below exists to keep that true. If it is ever false, the architecture is broken — fix
> the coupling, don't work around it.

## 1. High-level structure

```
App  (composition root)          # the ONLY place that assembles + runs the whole system — §1.1
│    wires ▼ Core + the chosen ▼ Plugins, then boots them
│
├── Core                         # infrastructure only — knows NO business feature
│   ├── Plugin Loader            # discovery → dependency resolution → ordered lifecycle
│   ├── Router · Event Bus · Service Container (DI)
│   ├── Auth (authn) · Authorization (authz) framework
│   ├── Config · Database Abstraction · Cache · Logging · Telemetry
│   ├── Shared Interfaces · Shared UI · Layout · Theme · i18n · Notification
│   └── Shared Domain Services   # cross-cutting entities used by many plugins (e.g. User) — §7
│
└── Plugins/                     # one self-contained slice per plugin — `kind` decides its shape (§3.1)
    ├── CRM/ · Chat/ · Inventory/ · Report/ · Dashboard/ · AI/ ...   # kind: capability — in-process features
    └── Tools-Postgres/ · Tools-Redis/ · Tools-MinIO/ ...            # kind: tool — sidecar backing services (own container + compose fragment)
```

A plugin owns its **full vertical slice**: backend (api · controllers · services · models · migrations ·
seeds · repositories · validation · jobs · events) + frontend (pages · components · routes · assets · i18n ·
state) + system (manifest · config · permissions · commands · listeners · tests).

### 1.1 Composition root — the App (where the full system runs)

Core is a framework and each plugin is a module; **neither runs on its own.** The **App** is the thin
composition root that assembles them — it depends on Core, declares which plugins to load
(`plugins.config`), and boots the whole thing. It is the only place that knows the concrete plugin *set*.

- **Run the full system here.** The entrypoint loads Core, then `register()` / `boot()`s the enabled plugins
  in dependency order (§4); the dev server / `docker compose up` lives here.
- **Test the full system here.** Integration tests (Core + several plugins on a real DB + bus) and E2E saga
  tests (§13) run against the assembled App. The removability matrix (§15) flips plugins on/off via this
  config, proving the §2.2 invariant.
- **It holds no business logic** (that's plugins) and **no infrastructure** (that's Core) — only wiring,
  config, env/secrets, and the run + test harness. Keep it thin.

## 2. The litmus rules (MUST)

1. **Core contains zero business logic.** No feature pages, APIs, services, tables, routes, permissions, or
   config in Core. Core is generic and reusable across products.
2. **A plugin is removable.** Deleting a plugin folder (and running its migrations down) leaves Core and
   every *other* plugin working. If removing A breaks B, they are illegally coupled.
3. **No plugin-to-plugin imports.** A plugin MUST NOT import another plugin's classes, types, or modules.
   Cross-feature interaction uses exactly one of the three sanctioned channels (§5).
4. **Extend, never modify.** Add features as plugins; never edit the Core to add a feature (Open/Closed).

## 3. The plugin contract — manifest

Every plugin ships a declarative `manifest` the Loader reads **before any plugin code runs**. This is what
makes discovery, ordering, versioning, namespacing, and security enforceable instead of hopeful.

```jsonc
// plugins/CRM/manifest.json
{
  "id": "crm",                       // globally unique — also the MANDATORY namespace prefix (§6)
  "name": "CRM",
  "version": "1.4.0",                // plugin's own semver
  "coreVersion": "^2.0.0",           // Core API range it is compatible with (§4)
  "kind": "capability",              // capability (in-process, default) · tool (ships a compose fragment) · app (§3.1)
  "dependencies": ["contacts"],      // plugin ids that MUST boot first (§4)
  "optionalDependencies": ["ai"],    // used if present, degraded-but-functional if absent
  "provides": ["crm.LeadService"],   // shared contracts this plugin registers into the container
  "consumes": ["core.User", "contacts.ContactService"], // contracts it resolves via DI (§5, §9-security)
  "permissions": ["crm.view", "crm.edit"],   // all prefixed with id (§6)
  "routes": ["/crm/*"],
  "events": { "emits": ["crm.lead.created"], "listens": ["billing.invoice.paid"] },
  "config": { "schema": "./config.schema.json" }, // validated config + feature flags (§11)
  "migrations": "./database/migrations"
}
```

The Loader **refuses boot** when: `coreVersion` is incompatible · a hard `dependencies` entry is missing ·
a declared `permission`/`route`/`event` collides with another plugin · a key is not prefixed with `id` · a
`consumes` entry was never `provide`d by anyone.

### 3.1 Plugin kinds — capability vs tool vs app (the in-process / out-of-process seam)

Not every plugin is the same shape. The manifest's **`kind`** declares which, and it decides *where the
plugin runs* and *what language it may be written in*. The dividing line is the **network seam**: a plugin
that talks to Core in-process must share Core's language; a plugin behind the network may be anything.

| `kind` | Runs | Talks to Core via | Ships | Language |
|---|---|---|---|---|
| **`capability`** *(default)* | in-process (inside Core / the worker) | DI contracts + Event Bus (§5) | code only — owns its tables in the shared DB | **same as Core** (in-process DI needs one runtime) |
| **`tool`** | its **own container** (a sidecar) | a namespaced **connection contract** over the network | a **`compose` fragment** + a thin contract (e.g. `postgres.Connection`, `minio.Storage`) | any — it's behind the seam |
| **`app`** | its **own container + own database** | HTTP contracts + events across the network (§5) | a `compose` fragment + its full vertical slice | any — it's behind the seam |

- **Tools are backing services, separated from features.** A **`tool`** plugin wraps infrastructure — a
  datastore (Postgres, Redis), an object store (MinIO), a messaging/bot gateway (Telegram) — as an
  installable unit. This is the **zero-datastore Core** model: **Core ships no datastore of its own**; a
  tool plugin brings the sidecar container (its `compose` fragment) *and* the thin connection contract the
  rest of the system `consumes` via DI. Enable the tool ⇒ its service joins the generated compose and its
  contract appears in the container; disable it ⇒ both disappear. Capability plugins depend on a tool by
  its **contract token** (`consumes: ["postgres.Connection"]`), never on the container directly — so
  swapping Postgres for another provider is a tool swap, not a feature rewrite.
- **The one polyglot rule.** Cross-language is allowed **iff** the plugin sits behind the network seam
  (`kind: tool`/`app`). A `capability` shares Core's process, so it MUST be Core's language; a `tool`/`app`
  owns its container and reaches Core only over HTTP + events, so it MAY be Node, Go, Rust, anything. This
  *qualifies*, not contradicts, "one language inside the process" — the process boundary is the sanctioned
  place to go polyglot, so a team can build a non-core service in its own stack without a Core rewrite.
- **An out-of-process plugin never touches another plugin's or Core's DB directly** — it owns its own data
  and asks over the published contract (§7), exactly like an in-process plugin. Isolation is identical; only
  the transport (network vs in-process call) differs.

> **Naming convention.** Give tool plugins a clear, greppable name — `[Name]-Plugin-Tools-<Infra>`
> (e.g. `-Tools-Postgres`, `-Tools-Redis`, `-Tools-MinIO`) — and derive the manifest `id` by stripping the
> `Tools-` segment (`postgres`, `redis`, `minio`) so the id stays a valid namespace prefix (§6).

## 4. Load order, dependency resolution & versioning

- **Discovery is automatic; order is computed.** The Loader reads every manifest, builds a dependency graph
  from `dependencies`, **topologically sorts** it, then: runs **`register()` for all** plugins first (so all
  `provides` exist in the container), then **`boot()` in dependency order**.
- **Cycle = hard failure.** A dependency cycle (A→B→A) fails boot with a clear, named error. Cycles are an
  architecture violation, not a runtime problem to paper over.
- **Version compatibility.** Each plugin declares `coreVersion`; the Loader won't load a plugin whose range
  excludes the running Core. Plugin↔plugin compatibility flows through `dependencies` + the consumed
  contract's semver. Record every plugin + Core version in `architecture/versions.md` (registry rule).
- **Migration ordering.** Each plugin owns its migrations, but they **run in plugin dependency order** so a
  foreign key into an upstream table never precedes that table. Down-migrations run in reverse.

## 5. Communication — the only three channels

```
Plugin ──▶ Core Interface ──▶ Plugin         synchronous contract, resolved via DI (needs an answer now)
Plugin ──▶ Event Bus       ──▶ Plugin         async, fire-and-forget, publisher ignorant of subscribers
Plugin ──▶ DI Container    ──▶ Shared Service a Core-owned or plugin-provided contract
```

- **Prefer events** for anything that doesn't need a synchronous answer — keeps coupling loose, cohesion
  high.
- **Contracts are owned & versioned.** A consumed interface (`contacts.ContactService`) is a *published
  contract*; breaking it is a **major** bump of the owning plugin, coordinated through `dependencies`.
- **Eventual consistency is explicit.** A flow that spans plugins (Order → Inventory → Payment) is
  event-driven and therefore eventually consistent. A multi-step write that must not partially apply uses a
  **saga with compensating actions**; never wrap cross-plugin writes in one DB transaction.

```
Saga example — place order (each step is one plugin, linked only by events):
  orders.place ──▶ orders.created
                     └▶ inventory.reserve ──▶ inventory.reserved
                                                └▶ billing.charge ──▶ billing.charged ──▶ orders.confirm
   on billing.failed ──▶ inventory.release  (compensating action)  ──▶ orders.cancel
```

### 5.1 Collaboration patterns — when plugin A needs plugin B

Two plugins living in the same system **never import each other** (§2.3). Pick the channel by what the
interaction actually needs. Worked example: **Order** (plugin A) must reserve stock from **Inventory**
(plugin B).

**Pattern A — needs an answer *now* (synchronous) → service contract via DI.**
B publishes a contract; A declares it as both a dependency (for load order, §4) and a consumed token.

```jsonc
// plugins/inventory/manifest.json
{ "id": "inventory", "provides": ["inventory.StockService"] }

// plugins/order/manifest.json
{ "id": "order",
  "dependencies": ["inventory"],          // Loader boots inventory first (§4)
  "consumes": ["inventory.StockService"]  // resolved via DI — the ONLY handle Order gets
}
```
```ts
class OrderService {
  constructor(private stock: StockService) {}          // injected interface, never an import
  place(o) { return this.stock.reserve(o.items); }     // calls the contract, not a concrete class
}
// ❌ import { ReserveService } from "../../inventory/..."   ← plugin→plugin import, forbidden
```

**Pattern B — fire-and-react, eventual is fine → Event Bus (preferred, loosest).**
A emits; B reacts; neither knows the other exists. Use a saga + compensation for multi-step writes (§5).

```
order.placed ──▶ inventory (listens) → reserve ──▶ inventory.reserved / inventory.failed
                                                       └▶ order (listens) → confirm / cancel
```

**Pattern C — the data is shared by neither → it belongs to Core (§7).**
A widely-used entity (User, Tenant, Money) is owned by a Core Shared Domain Service; both plugins consume
`core.User`, so there is no A↔B coupling at all.

| What the interaction needs | Channel |
|---|---|
| An immediate return value (validate stock before confirming) | **Service contract + DI** (Pattern A) |
| React after the fact / can be eventual | **Event Bus** (Pattern B) — *default* |
| A cross-cutting entity owned by neither plugin | **Core shared service** (Pattern C) |
| A multi-step write that must not partially apply | **Saga + compensating action** (§5) |

> **Litmus check before you wire them (§2.2):** *"Remove plugin B — does plugin A still work, even
> degraded?"* **Yes →** the split is right; collaborate via contract/event above. **No →** they are one
> bounded context; **merge them into a single plugin** (with internal sub-modules) rather than coupling two.

Running both together is the **App**'s job (§1.1): enable `order` + `inventory` in `plugins.config`, and the
Loader topologically boots `inventory` before `order`. A **consumer-driven contract test** (§13) pins
`inventory.StockService` so Inventory can't break Order silently across the no-import boundary.

## 6. Namespacing — no silent collisions

Every globally-visible key a plugin registers — **route · permission · event name · menu id · config key ·
DI token · DB schema/table prefix** — MUST be prefixed with the plugin `id`:

| Kind | Good | Bad |
|---|---|---|
| Permission | `crm.lead.edit` | `edit` |
| Event | `crm.lead.created` | `leadCreated` |
| Route | `/crm/leads` | `/leads` |
| DB table | `crm_leads` (or schema `crm`) | `leads` |
| DI token | `crm.LeadService` | `LeadService` |

The Loader validates prefixes at boot; a collision is a boot failure, not a runtime surprise.

## 7. Shared data & cross-cutting entities

The rule "never touch another plugin's tables" leaves one gap: entities **many** plugins need (User, Tenant,
Money, AuditLog). Resolve it explicitly:

- A widely-shared entity is **owned by Core** (or a dedicated Shared Domain Service), never by a feature
  plugin. Plugins consume it via a Core interface (`core.User`) — never by reading its table.
- A plugin needing *another plugin's* data reads it through that plugin's **published service contract**
  (`contacts.ContactService.find(id)`), never via SQL into `contacts_*`.
- Cross-feature reporting that genuinely needs joins uses a **read model / projection** fed by events, not
  direct cross-schema queries.

## 8. Fault isolation

The Core must survive a misbehaving plugin.

- Each lifecycle call (`register`/`boot`/`shutdown`) runs inside a **boundary**: an exception is caught,
  logged with the plugin id, and the plugin is marked **degraded** — it does not crash the Core or other
  plugins (unless a hard dependant declared it required, in which case the dependant degrades too).
- Event Bus delivery is **isolated**: a failing subscriber never fails the publisher. Synchronous contract
  calls are guarded with **timeouts + circuit breakers** for anything that can block.
- Every plugin gets **scoped logging + metrics** tagged by plugin id, so failures are attributable.

## 9. Security boundaries (NEW — least privilege between plugins)

Isolation is also a security property, not only a maintainability one.

- **Capability, not ambient authority.** A plugin can resolve only the contracts it declared in `consumes`;
  the container refuses an undeclared token. No plugin gets a god-object handle to the whole system.
- **Authz at the contract edge.** Every cross-plugin call and every route carries the caller's permission
  context; the Authorization framework checks the namespaced permission (`crm.lead.edit`) — a plugin can't
  silently act with another plugin's rights.
- **Data-scope enforcement.** Shared services apply tenant / row-level scoping centrally (§7), so a plugin
  can't read another tenant's data by crafting an id.
- **Secrets per the kit rule.** Plugin secrets live only in gitignored env behind the prod boot-guard;
  never in the manifest, never in a browser-shipped frontend bundle.

## 10. Lifecycle

```
register()   register services/contracts into the DI container — NO cross-plugin calls yet
boot()       wire up routes · menus · permissions · listeners · scheduled tasks — in dependency order
shutdown()   release resources · flush · deregister — in reverse dependency order
enable()/disable()   toggle a plugin at runtime without redeploy (§11) — idempotent
```

## 11. Configuration, feature flags & runtime enable/disable (NEW)

- **Config is schema-validated** (`config.schema.json`) and **config-driven, not hardcoded** (kit no-hardcode
  rule) — read only from a single settings object, editable from an admin surface + DB.
- **Feature flags** gate risky paths inside a plugin so they ship dark and roll out gradually.
- **Runtime toggle.** A plugin can be **disabled without a redeploy**: the Loader runs `disable()`,
  unregisters its routes/menus/listeners, and — because nothing imports it directly — the rest keeps
  running. Re-`enable()` is the inverse. This is the litmus rule (§2.2) made operational.

## 12. Layering inside every plugin

```
HTTP / route layer  →  service / business-logic layer  →  repository / data-access layer
```

All data access lives in the repository layer (no queries in controllers); I/O is async where the platform
supports it; config comes from one settings object. Keep this even in small plugins so they stay testable.

## 13. Testing strategy (NEW — how isolation is proven, not assumed)

| Level | Scope | Guarantees |
|---|---|---|
| **Unit** | service / repository in one plugin, deps mocked | business logic correctness |
| **Integration** | one plugin against a real DB + in-memory bus | migrations + repository + events wire up |
| **Contract (consumer-driven)** | the *consuming* plugin pins the shape of a `consumes` contract; the *providing* plugin's CI verifies it | a provider can't break a consumer silently across the no-import boundary |
| **Isolation** | boot the **App** with the plugin **removed** (toggle its `plugins.config` entry) | proves §2.2 — Core + others still boot (CI matrix) |
| **E2E (saga)** | the **App** assembled with all involved plugins; run the cross-plugin flow incl. the failure path | compensating actions actually compensate |

Contract tests are the linchpin: because plugins never import each other, the *only* coupling is the
published contract — so that is exactly what CI must pin. **Integration / isolation / E2E levels run in the
App** (§1.1) — the only place Core and multiple plugins are assembled together.

## 14. Observability (NEW)

- **Structured logs** tagged `{plugin.id, request.id, tenant.id}` — per-plugin filterable.
- **Metrics per plugin** — request rate / errors / latency, plus lifecycle (boot time, degraded count).
- **Distributed tracing across the bus** — a trace id propagates through events so a saga is one trace, not
  N disconnected spans. This is how you debug an eventually-consistent flow.
- **Health** — `/health` reports Core + each plugin's state (`active` / `degraded` / `disabled`) and version
  (from the manifest, never hardcoded → ties to `versions.md`).

## 15. Enforcement — every rule is a CI gate

Rules that only live in prose rot. Each becomes an automated gate:

| Rule | Gate |
|---|---|
| No plugin-to-plugin imports (§2.3) | dependency-cruiser: fail on any import crossing `plugins/<a>/ → plugins/<b>/` |
| Core has no business logic (§2.1) | lint: `core/` MUST NOT import from `plugins/` |
| Manifest valid (§3) | JSON-schema-validate every `manifest.json` |
| Namespacing (§6) | Loader self-check at boot + CI scan of registered keys for the `id` prefix |
| Dependency graph acyclic (§4) | CI builds the graph, fails on a cycle |
| Removability (§2.2) | CI matrix boots the app with each plugin removed |
| Contracts honored (§13) | consumer-driven contract tests run in the provider's pipeline |
| Version config-driven, not hardcoded | kit no-hardcode guard; version flows manifest → `/health` |

## 16. Concrete folder shapes

**A plugin** (lives under `[Name]-Plugin/`):

```
[Name]-Plugin/crm/
├── manifest.json          # the contract (§3)
├── config.schema.json     # validated config + feature flags (§11)
├── index.ts               # exports register() · boot() · shutdown() · enable() · disable()
├── backend/
│   ├── api/ · controllers/ · services/ · repositories/ · models/ · validation/ · jobs/ · events/
│   └── database/ { migrations/ · seeds/ }
├── frontend/
│   ├── pages/ · components/ · routes/ · state/ · assets/ · i18n/
└── tests/
    ├── unit/ · integration/ · contract/   # contract/ pins each consumed contract (§13)
```

**The App — composition root** (§1.1; the one place the full system is assembled + run + integration-tested):

```
[Name]-App/
├── plugins.config.{ts,json}   # which plugins are enabled — the assembly manifest (toggle for §15 matrix)
├── src/main.ts                # entrypoint: load Core → register()/boot() enabled plugins in dep order (§4)
├── env/.env.example           # secrets gitignored; real values never committed (kit rule)
├── docker-compose.yml         # run the FULL stack (Core + enabled plugins + datastores) here
└── tests/
    ├── integration/           # Core + several plugins on a real DB + bus
    └── e2e/                   # full cross-plugin saga flows incl. failure/compensation paths
```

> The App holds **no** business logic and **no** infrastructure — only wiring, config, and the run/test
> harness. It depends on `[Name]-Core` + the chosen `[Name]-Plugin/*`; it is never depended *on*.

## 17. Design principles (the why)

SOLID · Dependency Inversion (depend on interfaces, not implementations) · Interface Segregation ·
Event-Driven Design · Loose Coupling / High Cohesion · Separation of Concerns · Open/Closed ·
Feature-Based Architecture · Composition over inheritance · Least Privilege · DRY · KISS.

## 18. Definition of Done — a new plugin (NEW)

A plugin is "done" only when **all** are true:

- [ ] `manifest.json` complete & schema-valid (`id`, `coreVersion`, `dependencies`, `provides`/`consumes`).
- [ ] Every registered key (route / permission / event / table / DI token) is `id`-prefixed.
- [ ] No import crosses into another plugin; cross-feature access is via interface or event only.
- [ ] Owns its migrations + seeds; touches no other plugin's tables.
- [ ] Registered in the **App**'s `plugins.config`; the assembled App boots and its integration + E2E pass.
- [ ] Unit + integration + **contract** tests pass; the removal-isolation matrix still boots.
- [ ] Any cross-plugin write flow has a saga + compensating action.
- [ ] Config is schema-validated & config-driven; secrets in gitignored env; nothing hardcoded.
- [ ] Logs/metrics tagged by plugin id; version surfaced at `/health`; entry added to `versions.md`.
- [ ] The plugin can be **disabled at runtime** and the rest of the app keeps working.

## 19. Review checklist (apply on every change)

For each finding state **why it's a problem · severity · suggested fix · the better architecture**:

- [ ] Business logic leaking into Core?
- [ ] A plugin importing another plugin directly (vs interface/event)?
- [ ] Circular dependency between plugins?
- [ ] A plugin reading/writing another plugin's tables directly?
- [ ] Un-namespaced route / permission / event / config key?
- [ ] Manifest missing `coreVersion` / `dependencies` for a real dependency?
- [ ] A cross-plugin write flow with no saga / compensation?
- [ ] A consumed contract with no contract test pinning it?
- [ ] Could this plugin be removed (or disabled) without breaking the system? (if no → fix)
- [ ] Shared code duplicated across plugins that should move to Core?

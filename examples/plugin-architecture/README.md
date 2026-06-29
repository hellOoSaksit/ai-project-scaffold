# Example — Strict Full Plugin Architecture on the scaffold

This worked example shows how to build a **strict Core + Plugins application** *inside* the structure the
[new-project scaffolder](../../kit/new-project-scaffold.md) produces. The two are **orthogonal and
complementary**:

- **The scaffold** decides *where knowledge and repos live* (one `CLAUDE.md` router, `AGENTS.md` + `llms.txt`
  entry points, job-first `docs/`, registries, CI).
- **The plugin architecture** decides *how the application code is structured* (a generic **Core** that
  provides infrastructure only, plus self-contained feature **plugins** that can each be removed without
  breaking the rest).

They don't compete — the plugin design is **content that lives in `docs/architecture/`**, while the *app code*
follows it across two repos: `[Name]-Core/` (the host) and `[Name]-Plugin/` (the features).

> 📄 The enforceable design contract is **[system-design.md](system-design.md)** — manifest, load order,
> versioning, fault isolation, namespacing, shared-data ownership, security boundaries, contract testing,
> observability, and the CI gates that make every rule real. It is written in the kit's `docs/` frontmatter
> format so you can drop it straight into a scaffolded project.

> **Naming note.** This example uses **`Core` / `Plugin`** instead of the kit's generic `Main` / `Standalone`
> labels, because the whole architecture is plugin-based and those words are the industry standard (host
> `Core` + `Plugin`s, as in VSCode / WordPress / Strapi). The layout is identical to the scaffold's — only
> the two repo names are specialized to the domain.

---

## How the plugin concept maps onto the scaffold

| Plugin concept | Where it lives in a scaffolded project |
|---|---|
| **Core** (Loader, Router, DI, Auth, Cache, Logging — infra only) | host repo `[Name]-Core/` |
| **Each feature plugin** (self-contained, no plugin→plugin import) | `[Name]-Plugin/<id>/` — one folder per plugin |
| **The architecture rules & contracts** | `[Name]-Docs/docs/architecture/system-design.md` (this doc) |
| **Operating rules (MUST / MUST NOT)** | `[Name]-Docs/docs/[name]-dev-rules.md` |
| **One doc per plugin** | `[Name]-Docs/docs/features/<id>.md` |
| **Plugin + Core versions** | `[Name]-Docs/docs/architecture/versions.md` (registry) |
| **Host ports per app** | `[Name]-Docs/docs/architecture/ports.md` (registry) |

**Why it fits cleanly:** the scaffold's core principle — *a feature is a removable, self-contained slice that
talks to the rest only through contracts* — is the **same idea** as a plugin that can't import another plugin
and must survive its neighbours being removed. The plugin manifest's `version` / `coreVersion` map onto the
`versions.md` registry; "no business logic in Core" maps onto the kit's layering rule.

---

## What you get after running the scaffolder

Running the scaffolder for a project named **`Acme`** that builds a plugin-based app with three starter
plugins (`crm`, `chat`, `inventory`) produces this. Folders the **scaffold** always creates are marked
`scaffold`; folders **you** add as you build the app are marked `app`.

```
Acme-Project/                        # workspace root = its own thin git repo (tracks only the shared root files)
│
├── CLAUDE.md                        # scaffold · the ONE thin router: always-on rules + project map + task router
├── AGENTS.md                        # scaffold · signal-dense entry for 30+ agents (build/test/run + boundaries)
├── llms.txt                         # scaffold · LLM navigation map (llmstxt.org)
│
├── Acme-Core/                       # scaffold · the HOST repo — infrastructure ONLY, knows no feature
│   ├── README.md                    # scaffold · GitHub overview (no project knowledge)
│   ├── plugin-loader/               # app · discovery → topological sort → ordered lifecycle
│   ├── router/  event-bus/  container/      # app · routing · Event Bus · DI container
│   ├── auth/  authorization/                # app · authn framework · authz framework
│   ├── config/  database/  cache/  logging/  telemetry/
│   ├── shared-ui/  layout/  theme/  i18n/  notification/
│   └── shared-domain/               # app · cross-cutting entities (User, Tenant) — owned by Core
│
├── Acme-Plugin/                     # scaffold · EVERY feature is a plugin — one self-contained folder each
│   ├── crm/
│   │   ├── manifest.json            # app · the contract: id · version · coreVersion · dependencies · provides/consumes
│   │   ├── config.schema.json       # app · validated config + feature flags
│   │   ├── index.ts                 # app · exports register() · boot() · shutdown() · enable() · disable()
│   │   ├── backend/
│   │   │   ├── api/ controllers/ services/ repositories/ models/ validation/ jobs/ events/
│   │   │   └── database/ { migrations/  seeds/ }     # crm OWNS its tables (crm_*)
│   │   ├── frontend/
│   │   │   └── pages/ components/ routes/ state/ assets/ i18n/
│   │   └── tests/ { unit/  integration/  contract/ }  # contract/ pins each consumed contract
│   ├── chat/                        # app · same shape — self-contained
│   └── inventory/                   # app · same shape — self-contained
│
└── Acme-Docs/                       # scaffold · all knowledge, centralized, English, frontmatter on every file
    ├── README.md                    # scaffold · GitHub overview
    ├── scripts/docs-lint.py         # scaffold · frontmatter + link/anchor validator → CI
    └── docs/
        ├── README.md                # scaffold · docs index / map (read first)
        ├── GLOSSARY.md              # scaffold · domain terms
        ├── acme-dev-rules.md        # scaffold · operating contract (the plugin MUST/MUST NOT rules land here)
        ├── architecture/
        │   ├── system-design.md     # ★ THIS DOC — the plugin architecture contract
        │   ├── data-model.md  database-design.md  tech-stack.md  deploy.md  risks.md
        │   ├── ports.md             # scaffold · registry — host ports (Core + each plugin's dev port)
        │   └── versions.md          # scaffold · registry — Core version + each plugin version (manifest → here)
        ├── features/                # app · 1 file = 1 plugin
        │   ├── crm.md  chat.md  inventory.md
        ├── process/                 # scaffold · playbook · session-handoff · lessons · ai-runbooks
        ├── new-project/             # scaffold · the setup prompts + principles.html
        └── templates/               # scaffold · copy-to-create scaffolds (frontmatter, feature, plugin…)
```

### Reading the three repos

- **`Acme-Core/` = the host (infra only).** The Plugin Loader, Router, Event Bus, DI container, auth, cache,
  logging — and the shared cross-cutting entities (User, Tenant). It knows **no** feature. This is where the
  Loader discovers plugins, resolves their `dependencies`, and boots them in order.
- **`Acme-Plugin/` = the features.** One self-contained folder per plugin, each a full vertical slice
  (manifest + backend + frontend + tests). Each is **removable** and talks to the rest only through Core
  interfaces or the Event Bus — never by importing another plugin.
- **`Acme-Docs/` = the project's brain.** The router + entry points sit at the workspace root; all knowledge
  (architecture, per-plugin docs, registries, process) lives here with frontmatter for retrieval.

### The invariant that ties it together

> Delete any `Acme-Plugin/<id>/` folder, run its migrations down, and **`Acme-Core` still boots and every
> other plugin still works**. That single property is enforced by a CI matrix (see system-design.md §15) and
> is the reason this architecture stays maintainable from 3 plugins to 300.

---

## Use it

1. Run the [new-project scaffolder](../../kit/new-project-scaffold.md) — answer the intake, pick your stack;
   tell it to use the `Core` / `Plugin` repo names instead of `Main` / `Standalone`.
2. Drop [system-design.md](system-design.md) into `[Name]-Docs/docs/architecture/` and move the MUST/MUST NOT
   rules into `[name]-dev-rules.md`.
3. Build `[Name]-Core/` (infra only) and your first `[Name]-Plugin/<id>/` to the contract; wire the §15 CI gates.
4. Keep `versions.md` / `ports.md` in sync with each plugin's manifest (registry rule).

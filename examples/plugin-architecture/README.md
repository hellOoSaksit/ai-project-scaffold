# Example — Strict Full Plugin Architecture on the scaffold

This worked example shows how to build a **strict Core + Plugins application** *inside* the structure the
[new-project scaffolder](../../kit/new-project-scaffold.md) produces. The two are **orthogonal and
complementary**:

- **The scaffold** decides *where knowledge and repos live* (one `CLAUDE.md` router, `AGENTS.md` + `llms.txt`
  entry points, job-first `docs/`, registries, CI).
- **The plugin architecture** decides *how the application code is structured* (a generic Core that provides
  infrastructure only, plus self-contained feature plugins that can each be removed without breaking the rest).

They don't compete — the plugin design is **content that lives in `docs/architecture/`**, while the *app code*
follows it inside `[Name]-Main/`.

> 📄 The enforceable design contract is **[system-design.md](system-design.md)** — manifest, load order,
> versioning, fault isolation, namespacing, shared-data ownership, security boundaries, contract testing,
> observability, and the CI gates that make every rule real. It is written in the kit's `docs/` frontmatter
> format so you can drop it straight into a scaffolded project.

---

## How the plugin concept maps onto the scaffold

| Plugin concept | Where it lives in a scaffolded project |
|---|---|
| **Core** (Loader, Router, DI, Auth, Cache, Logging — infra only) | app code in `[Name]-Main/core/` |
| **Each feature plugin** (self-contained, no plugin→plugin import) | app code in `[Name]-Main/plugins/<id>/` |
| **A big feature that can ship on its own** | promote to the **standalone line** → `[Name]-Standalone/<app>/` |
| **The architecture rules & contracts** | `[Name]-Docs/docs/architecture/system-design.md` (this doc) |
| **Operating rules (MUST / MUST NOT)** | `[Name]-Docs/docs/[name]-dev-rules.md` |
| **One doc per feature** | `[Name]-Docs/docs/features/<id>.md` |
| **Plugin + Core versions** | `[Name]-Docs/docs/architecture/versions.md` (registry) |
| **Host ports per app** | `[Name]-Docs/docs/architecture/ports.md` (registry) |

**Why it fits cleanly:** the scaffold's core principle — *a feature is a removable, self-contained slice that
talks to the rest only through contracts* — is the **same idea** as a plugin that can't import another plugin
and must survive its neighbours being removed. The plugin manifest's `version` / `coreVersion` map onto the
`versions.md` registry; "no business logic in Core" maps onto the kit's layering rule.

---

## What you get after running the scaffolder

Running the scaffolder for a project named **`Acme`** that builds a plugin-based app with three starter
features (`crm`, `chat`, `inventory`) produces this. Folders the **scaffold** always creates are marked
`scaffold`; folders **you** add as you build the plugin app are marked `app`.

```
Acme-Project/                        # umbrella = its own thin git repo (tracks only the shared root files)
│
├── CLAUDE.md                        # scaffold · the ONE thin router: always-on rules + project map + task router
├── AGENTS.md                        # scaffold · signal-dense entry for 30+ agents (build/test/run + boundaries)
├── llms.txt                         # scaffold · LLM navigation map (llmstxt.org)
│
├── Acme-Main/                       # scaffold · the application repo — Core + Plugins live HERE
│   ├── README.md                    # scaffold · GitHub overview (no project knowledge)
│   ├── core/                        # app · infrastructure ONLY — knows no feature
│   │   ├── plugin-loader/           #        discovery → topological sort → ordered lifecycle
│   │   ├── router/  event-bus/  container/      # routing · Event Bus · DI container
│   │   ├── auth/  authorization/                # authn framework · authz framework
│   │   ├── config/  database/  cache/  logging/  telemetry/
│   │   ├── shared-ui/  layout/  theme/  i18n/  notification/
│   │   └── shared-domain/           #        cross-cutting entities (User, Tenant) — owned by Core
│   └── plugins/                     # app · one self-contained vertical slice per feature
│       ├── crm/
│       │   ├── manifest.json        #        the contract: id · version · coreVersion · dependencies · provides/consumes
│       │   ├── config.schema.json   #        validated config + feature flags
│       │   ├── index.ts             #        exports register() · boot() · shutdown() · enable() · disable()
│       │   ├── backend/
│       │   │   ├── api/ controllers/ services/ repositories/ models/ validation/ jobs/ events/
│       │   │   └── database/ { migrations/  seeds/ }   # crm OWNS its tables (crm_*)
│       │   ├── frontend/
│       │   │   └── pages/ components/ routes/ state/ assets/ i18n/
│       │   └── tests/ { unit/  integration/  contract/ }   # contract/ pins each consumed contract
│       ├── chat/                    #        same shape — self-contained
│       └── inventory/               #        same shape — self-contained
│
├── Acme-Standalone/                 # scaffold · big features promoted to their own apps (empty at first)
│   └── <app>/                       # app · one folder per standalone app, when one exists
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
        ├── features/                # app · 1 file = 1 feature
        │   ├── crm.md  chat.md  inventory.md
        ├── standalone/              # app · 1 subfolder = 1 standalone app
        ├── process/                 # scaffold · playbook · session-handoff · lessons · ai-runbooks
        ├── new-project/             # scaffold · the setup prompts + principles.html
        └── templates/               # scaffold · copy-to-create scaffolds (frontmatter, feature, standalone…)
```

### Reading the two halves

- **Left/top = the scaffold's job:** the umbrella, the router + entry points, and `Acme-Docs/docs/` — created
  the moment you scaffold, before a line of app code. This is *where the project's brain lives*.
- **`Acme-Main/core/` + `Acme-Main/plugins/` = your job:** the actual Core + Plugins app, built to the
  contract in [system-design.md](system-design.md). Each `plugins/<id>/` is a removable vertical slice; the
  Loader discovers them, resolves `dependencies`, and boots them in order.

### The invariant that ties it together

> Delete any `plugins/<id>/` folder, run its migrations down, and **`Acme-Main` still boots and every other
> plugin still works**. That single property is enforced by a CI matrix (see system-design.md §15) and is the
> reason this architecture stays maintainable from 3 plugins to 300.

---

## Use it

1. Run the [new-project scaffolder](../../kit/new-project-scaffold.md) — answer the intake, pick your stack.
2. Drop [system-design.md](system-design.md) into `[Name]-Docs/docs/architecture/` and move the MUST/MUST NOT
   rules into `[name]-dev-rules.md`.
3. Build `core/` (infra only) and your first `plugins/<id>/` to the contract; wire the §15 CI gates.
4. Keep `versions.md` / `ports.md` in sync with each plugin's manifest (registry rule).

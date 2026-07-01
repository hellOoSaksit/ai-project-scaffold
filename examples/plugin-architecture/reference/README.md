# Reference implementation — the plugin contract made concrete

These files are the **runnable skeleton** behind [system-design.md](../system-design.md). They are
illustrative reference (TypeScript-ish pseudocode + real JSON/JS configs), not a buildable app — their job
is to show *exactly* what each rule looks like in code, and to give you the two CI gates ready to copy.

```
reference/
├── manifest.schema.json        # §3  — JSON Schema for a plugin manifest (a CI gate; the App validates each manifest against it)
├── .dependency-cruiser.cjs     # §15 — CI gate: no plugin→plugin imports · core can't import plugins · no cycles
├── core/
│   └── contracts/
│       ├── stock-service.ts        # §5/§6 — a published cross-plugin contract (interface in Core, impl in the owner plugin)
│       └── postgres-connection.ts  # §3.1/§6 — same pattern, for a `kind: tool` plugin's connection contract
├── plugins/
│   ├── postgres/                # id = the tool's id — NOT a `Tools-` prefixed folder (§3.1 naming note)
│   │   ├── manifest.json           # kind: tool · PROVIDES postgres.Connection · secrets:[database_url] · compose fragment
│   │   ├── compose.fragment.yml     # the sidecar container this tool ships — merged into the App's stack when enabled
│   │   └── index.ts                 # register() only — no boot() wiring, a tool has nothing to react to
│   ├── inventory/
│   │   ├── manifest.json       # PROVIDES inventory.StockService · listens order.placed
│   │   └── index.ts            # §10 lifecycle · §5.1 Pattern A (provide) + Pattern B (event) · §8 fault boundary
│   └── order/
│       ├── manifest.json       # dependencies:[inventory] · CONSUMES inventory.StockService
│       └── index.ts            # §5.1 — consumes the contract via DI (never imports inventory) + saga tail
└── app/                        # §1.1 — the composition root
    ├── plugins.config.ts       # the enabled-plugin set (toggle for the §15 removal matrix)
    └── src/main.ts             # entrypoint: build Core → validate → topological boot → serve
```

## The one thing to notice

`order/index.ts` needs Inventory's `reserve()`, but **never imports the Inventory plugin**. It imports the
`StockService` *interface* from `core/contracts/` and gets the *implementation* injected via the DI token
`inventory.StockService`. That single indirection is the whole architecture:

- swap or remove Inventory → Order still compiles (it only knows the Core interface);
- `dependency-cruiser` fails CI the moment anyone writes `import … from "plugins/inventory/…"`;
- a consumer-driven contract test pins `StockService` so Inventory can't break Order silently (§13).

## The `postgres` plugin — a `tool`, not a feature

`plugins/postgres/` is the same manifest + lifecycle shape as `inventory`/`order`, but its `kind` is
**`tool`**, not `capability` (§3.1): it ships a `compose.fragment.yml` (its own sidecar container) and
`register()`s the `postgres.Connection` contract instead of a business service. Any capability plugin that
needs a database would declare `dependencies: ["postgres"]` + `consumes: ["postgres.Connection"]` — same
DI indirection as `StockService` above, so swapping Postgres for another provider means swapping this one
plugin, not touching every feature that reads/writes data. Note its folder is **`postgres/`, not
`Tools-Postgres/`** — the manifest `id` is always lowercase (schema-enforced); `Tools-` is a *repo-name*
convention, used only once a plugin is promoted to its own repo (`[Name]-Plugin-Tools-Postgres`) in the
"repo-per-plugin" phase.

## Use the two gates in your pipeline

```bash
# 1. validate every plugin manifest against the schema (§3)
npx ajv validate -s reference/manifest.schema.json -d "plugins/*/manifest.json"

# 2. enforce the import boundaries (§2.1, §2.3, §4)
npx depcruise --config reference/.dependency-cruiser.cjs core plugins app
```

Wire both into CI alongside the removal-isolation matrix (boot `app` once per plugin with that plugin
disabled in `plugins.config`) and the architecture stops being aspirational — it's enforced on every push.

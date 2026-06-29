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
│       └── stock-service.ts    # §5/§6 — a published cross-plugin contract (interface in Core, impl in the owner plugin)
├── plugins/
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

## Use the two gates in your pipeline

```bash
# 1. validate every plugin manifest against the schema (§3)
npx ajv validate -s reference/manifest.schema.json -d "plugins/*/manifest.json"

# 2. enforce the import boundaries (§2.1, §2.3, §4)
npx depcruise --config reference/.dependency-cruiser.cjs core plugins app
```

Wire both into CI alongside the removal-isolation matrix (boot `app` once per plugin with that plugin
disabled in `plugins.config`) and the architecture stops being aspirational — it's enforced on every push.

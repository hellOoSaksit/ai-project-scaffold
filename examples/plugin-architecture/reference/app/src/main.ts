/**
 * App entrypoint (§1.1) — assemble Core + the enabled plugins and RUN the full system.
 *
 * This file is the whole reason the App repo exists. It contains NO business logic and NO infrastructure —
 * only wiring: build Core, discover the enabled plugins, let the Loader resolve order, boot, serve.
 *
 *   docker compose up   →   node dist/main.js   (the full stack runs from here)
 */
import { createCore } from '../../core';
import { enabledPlugins } from '../plugins.config';

async function main() {
  // 1. Core first — infrastructure only (router, event bus, DI container, db, auth, telemetry)
  const core = await createCore({ configSource: process.env }); // config-driven; secrets from gitignored env

  // 2. Load each enabled plugin's manifest + module
  const loaded = await Promise.all(
    enabledPlugins().map(async (e) => ({
      manifest: await core.loader.readManifest(e.from), // validated against manifest.schema.json (§3)
      module: (await import(e.from)).default,
    })),
  );

  // 3. Loader enforces the contract BEFORE running anything (§3, §4, §6):
  //    - coreVersion compatible?  - all hard `dependencies` present?  - no namespace collisions?
  //    - every `consumes` is `provide`d somewhere?  - dependency graph acyclic?
  core.loader.validate(loaded.map((l) => l.manifest));

  // 4. Topological order from `dependencies` → register() ALL, then boot() in order (§4, §10)
  const order = core.loader.topologicalOrder(loaded.map((l) => l.manifest)); // e.g. [inventory, order]
  for (const id of order) core.loader.register(byId(loaded, id), core.context);
  for (const id of order) await core.loader.boot(byId(loaded, id), core.context);

  // 5. Serve the assembled system; /health reports Core + each plugin's state + version (§14)
  await core.serve();
  core.log.info(`up — plugins booted: ${order.join(' → ')}`);
}

const byId = (loaded: Array<{ manifest: { id: string }; module: unknown }>, id: string) =>
  loaded.find((l) => l.manifest.id === id)!.module;

main().catch((err) => {
  // a plugin that throws in boot() is isolated and marked degraded (§8); a Core failure is fatal
  console.error('fatal during assembly:', err);
  process.exit(1);
});

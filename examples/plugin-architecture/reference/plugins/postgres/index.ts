/**
 * Postgres tool plugin — PROVIDES `postgres.Connection` (§3.1).
 * `kind: tool`: the actual database runs in its OWN container (`compose.fragment.yml`), reached over
 * the network; this file only owns the connection seam Core-side. Compare to `plugins/inventory/index.ts`
 * (a `kind: capability` plugin) — same lifecycle shape, but this one never touches business tables.
 *
 * No `boot()` cross-plugin wiring here: a tool has nothing to react to, it only publishes a contract.
 */
import type { PluginContext, Plugin } from '../../core/plugin-loader/types';
import { Connection, Transaction, POSTGRES_CONNECTION } from '../../core/contracts/postgres-connection';

class PostgresConnection implements Connection {
  constructor(private readonly databaseUrl: string) {}

  async tx<T>(fn: (t: Transaction) => Promise<T>): Promise<T> {
    // pseudocode: open a pooled client at this.databaseUrl, BEGIN, run fn, COMMIT/ROLLBACK on throw
    return withPooledConnection(this.databaseUrl, fn);
  }
}

const plugin: Plugin = {
  // register(): resolve the `database_url` secret (manifest `secrets`, §9-security — never hardcoded)
  // and bind the contract. Nothing else may read this secret directly.
  register(ctx: PluginContext) {
    ctx.container.bind(POSTGRES_CONNECTION, () => new PostgresConnection(ctx.secrets.get('database_url')));
  },

  async shutdown(ctx: PluginContext) {
    // pseudocode: drain the pool opened in register()
  },
};

export default plugin;

declare function withPooledConnection<T>(url: string, fn: (t: Transaction) => Promise<T>): Promise<T>;

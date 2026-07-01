/**
 * A published cross-plugin CONTRACT for a `kind: tool` plugin (§3.1) — same pattern as
 * `stock-service.ts`, just for a backing service instead of a feature: the *interface* sits in Core's
 * Shared Interfaces, the *implementation* + the actual Postgres container live in the `postgres` tool
 * plugin, bound at runtime under the namespaced DI token `postgres.Connection` (§3 `provides`, §6).
 *
 * Any plugin that needs a database declares `dependencies: ["postgres"]` (load order, §4) and
 * `consumes: ["postgres.Connection"]` (§5, §9-security) — it resolves this interface, never the
 * concrete client, and never reaches into the sidecar container directly.
 */
export interface Connection {
  /** Run `fn` inside a transaction; commits on return, rolls back on throw. */
  tx<T>(fn: (t: Transaction) => Promise<T>): Promise<T>;
}

export interface Transaction {
  query<T>(sql: string, params?: unknown[]): Promise<T[]>;
}

/** The DI token both sides agree on — namespaced to the OWNER (the `postgres` tool plugin). */
export const POSTGRES_CONNECTION = 'postgres.Connection' as const;

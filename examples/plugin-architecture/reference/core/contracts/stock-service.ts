/**
 * A published cross-plugin CONTRACT (interface only — no implementation).
 *
 * Why it lives in Core, not in the Inventory plugin: if Order imported this type from
 * `plugins/inventory/...`, that would be a plugin→plugin import (forbidden, §2.3). So the *interface*
 * sits in Core's Shared Interfaces, while the *implementation* lives in the Inventory plugin and is bound
 * at runtime under the namespaced DI token `inventory.StockService` (§3 `provides`, §6 namespacing).
 *
 * Breaking this interface is a MAJOR version bump of the owning plugin (§5), and a consumer-driven
 * contract test (§13) pins its shape so the provider can't break a consumer silently.
 */
export interface StockService {
  /** Reserve stock for the given lines; throws StockError if any line is short. */
  reserve(lines: ReadonlyArray<{ sku: string; qty: number }>): Promise<ReservationId>;
  /** Compensating action for the saga (§5) — releases a prior reservation. */
  release(reservation: ReservationId): Promise<void>;
}

export type ReservationId = string;

export class StockError extends Error {}

/** The DI token both sides agree on — namespaced to the OWNER (Inventory). */
export const STOCK_SERVICE = 'inventory.StockService' as const;

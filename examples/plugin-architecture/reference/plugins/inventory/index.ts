/**
 * Inventory plugin — PROVIDES `inventory.StockService` and reacts to `order.placed`.
 * Demonstrates Pattern A (publish a contract) + Pattern B (event listener) from §5.1.
 *
 * Note the imports: only Core. No `plugins/order/...` import anywhere — the two plugins are wired solely
 * through the contract + the Event Bus.
 */
import type { PluginContext, Plugin } from '../../core/plugin-loader/types';
import { StockService, STOCK_SERVICE, ReservationId, StockError } from '../../core/contracts/stock-service';

class InventoryStockService implements StockService {
  constructor(private readonly db: PluginContext['db']) {}

  async reserve(lines: ReadonlyArray<{ sku: string; qty: number }>): Promise<ReservationId> {
    // all data access stays in the repository/data layer (§12); writes only to inventory_* tables (§7)
    return this.db.tx(async (t) => {
      for (const { sku, qty } of lines) {
        const ok = await t.decrementIfAvailable('inventory_stock', sku, qty);
        if (!ok) throw new StockError(`short on ${sku}`);
      }
      return t.insertReservation('inventory_reservations', lines);
    });
  }

  async release(reservation: ReservationId): Promise<void> {
    await this.db.tx((t) => t.releaseReservation('inventory_reservations', reservation));
  }
}

const plugin: Plugin = {
  // register(): only put things into the DI container — no cross-plugin calls yet (§10)
  register(ctx: PluginContext) {
    ctx.container.bind(STOCK_SERVICE, () => new InventoryStockService(ctx.db));
  },

  // boot(): wire routes/permissions/listeners — runs in dependency order (§4, §10)
  boot(ctx: PluginContext) {
    const stock = ctx.container.resolve<StockService>(STOCK_SERVICE);

    // Pattern B (§5.1): react to another plugin's event without knowing who emitted it
    ctx.events.on('order.placed', async (e: { reservationLines: any[]; orderId: string }) => {
      try {
        const reservation = await stock.reserve(e.reservationLines);
        ctx.events.emit('inventory.reserved', { orderId: e.orderId, reservation });
      } catch (err) {
        // fault stays inside this plugin's boundary (§8); the saga compensates on the event
        ctx.events.emit('inventory.failed', { orderId: e.orderId, reason: String(err) });
      }
    });
  },

  async shutdown(ctx: PluginContext) {
    ctx.events.off('order.placed');
  },
};

export default plugin;

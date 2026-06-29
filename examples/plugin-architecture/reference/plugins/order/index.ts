/**
 * Order plugin — CONSUMES `inventory.StockService` (Pattern A) and drives a saga over the bus (Pattern B).
 * See §5.1. It declares `dependencies: ["inventory"]` so the Loader boots inventory first (§4).
 *
 * Critical: Order imports the StockService *interface* from Core, never the Inventory implementation.
 * dependency-cruiser's `no-plugin-to-plugin` rule would fail CI on a `plugins/inventory/...` import.
 */
import type { PluginContext, Plugin } from '../../core/plugin-loader/types';
import { StockService, STOCK_SERVICE } from '../../core/contracts/stock-service';

class OrderService {
  // the contract is injected — Order has no idea which plugin implements it
  constructor(private readonly stock: StockService, private readonly events: PluginContext['events']) {}

  /**
   * Pattern A — synchronous validation when we need an answer NOW (reserve before we accept the order).
   * Pattern B — then emit `order.placed` to let the rest of the saga proceed eventually.
   */
  async place(order: { id: string; lines: Array<{ sku: string; qty: number }> }) {
    await this.stock.reserve(order.lines); // sync contract call across the boundary (§5.1 Pattern A)
    this.events.emit('order.placed', { orderId: order.id, reservationLines: order.lines });
  }
}

const plugin: Plugin = {
  register(ctx: PluginContext) {
    ctx.container.bind('order.OrderService', () => {
      const stock = ctx.container.resolve<StockService>(STOCK_SERVICE); // resolved, not imported
      return new OrderService(stock, ctx.events);
    });
  },

  boot(ctx: PluginContext) {
    // saga tail (§5): react to inventory's outcome — confirm or compensate
    ctx.events.on('inventory.reserved', (e: { orderId: string }) =>
      ctx.events.emit('order.confirmed', { orderId: e.orderId }),
    );
    ctx.events.on('inventory.failed', (e: { orderId: string; reason: string }) =>
      ctx.events.emit('order.cancelled', { orderId: e.orderId, reason: e.reason }),
    );
  },

  async shutdown(ctx: PluginContext) {
    ctx.events.off('inventory.reserved');
    ctx.events.off('inventory.failed');
  },
};

export default plugin;

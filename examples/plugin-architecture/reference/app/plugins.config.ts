/**
 * The assembly manifest for the App composition root (§1.1).
 * This is the ONE place that knows the concrete set of plugins the running system includes.
 *
 * Toggle entries here to drive the §15 removal-isolation matrix: CI boots the App once per plugin with
 * that plugin disabled and asserts Core + the rest still boot — proving the §2.2 invariant.
 */
export interface PluginEntry {
  id: string;
  /** path/package the App loads the plugin from (workspace path here; a versioned package in polyrepo) */
  from: string;
  enabled: boolean;
}

export const plugins: PluginEntry[] = [
  { id: 'inventory', from: '../plugins/inventory', enabled: true },
  { id: 'order', from: '../plugins/order', enabled: true },
  // add more plugins here; load ORDER is computed from each manifest's `dependencies`, not this list
];

export const enabledPlugins = () => plugins.filter((p) => p.enabled);

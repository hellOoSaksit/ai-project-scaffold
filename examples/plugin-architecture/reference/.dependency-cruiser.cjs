/**
 * dependency-cruiser config — turns the architecture's hard rules into a CI gate
 * (system-design.md §15). Run in the app/plugin repos' pipeline:
 *
 *   npx depcruise --config .dependency-cruiser.cjs core plugins app
 *
 * Paths are relative to the repo root and assume the reference layout:
 *   core/  plugins/<id>/  app/
 */
module.exports = {
  forbidden: [
    {
      name: 'no-plugin-to-plugin',
      comment:
        'A plugin MUST NOT import another plugin (§2.3). Cross-feature interaction goes through a Core ' +
        'interface, the Event Bus, or a DI-resolved contract — never a direct import.',
      severity: 'error',
      from: { path: '^plugins/([^/]+)/' },
      // flag any import whose target is a DIFFERENT plugin (capture-group backreference $1)
      to: { path: '^plugins/([^/]+)/', pathNot: '^plugins/$1/' },
    },
    {
      name: 'no-core-to-plugin',
      comment:
        'Core is infrastructure only and MUST NOT know any feature (§2.1). It can never import a plugin.',
      severity: 'error',
      from: { path: '^core/' },
      to: { path: '^plugins/' },
    },
    {
      name: 'no-app-business-logic',
      comment:
        'The App is a thin composition root (§1.1): it may import Core + plugins to wire them, but must ' +
        'not be imported BY them, and holds no business logic itself.',
      severity: 'error',
      from: { path: '^(core|plugins)/' },
      to: { path: '^app/' },
    },
    {
      name: 'no-circular',
      comment: 'A dependency cycle (incl. plugin dep cycles) is an architecture violation (§4).',
      severity: 'error',
      from: {},
      to: { circular: true },
    },
    {
      name: 'no-orphans',
      comment: 'Dead modules rot — every file should be reachable.',
      severity: 'warn',
      from: { orphan: true, pathNot: '\\.(d\\.ts|config\\.(js|cjs|ts))$' },
      to: {},
    },
  ],
  options: {
    doNotFollow: { path: 'node_modules' },
    tsConfig: { fileName: 'tsconfig.json' },
  },
};

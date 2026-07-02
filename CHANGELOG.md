# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Anti-bloat docs-hygiene guards** — the reference `kit/docs-lint.py` now guards the docs an agent
  re-reads *every session* from silent, append-only bloat: it **fails** when `process/session-handoff.md`
  passes a line ceiling (~350) or stacks more than a couple of `SESSION-END STATE` blocks, **warns** when
  any curated doc passes ~600 lines (usually two concepts → split), and (path-gated behind
  `$PROJECT_MEMORY_DIR`, local-only) caps agent-memory files + their index. The failure message states the
  rule — *trim / split / move to git history, never raise the limit*. Folded the concept inline into the
  scaffolder's **rule 8** and **removed the standalone `kit/docs-hygiene-guards.md`** (the prompt stays
  self-contained). Mirrored into the README kit table + enforcement bullet.

### Changed
- **README restructured for readability.** Added a hero *"at a glance"* panel with the headline stat,
  moved a 30-second **Quick start** near the top, made the long `🇹🇭 สรุปภาษาไทย` summary collapsible
  (`<details>`) so it no longer buries the English intro, and reordered the sections into a clearer
  narrative. Also refreshed the **Quality review** section to reflect `v0.4.1` (shipped enforcement +
  OWASP-aligned security baseline + the repo dogfooding its own structure) and to be honest that the pass
  *found and fixed* real drift rather than asserting none. Every cross-file anchor (the ones
  `docs/evidence/measurements.md` and the badges depend on) was preserved; both linters stay green.

## [0.4.1] - 2026-07-02

### Security
- **Secure-coding baseline** — a new always-on **rule 8** (*Secure by default*: no string-built SQL/shell —
  parameterized queries/ORM only · validate every input at the edge · framework auto-escaping against XSS ·
  server-side deny-by-default authz incl. object-level · generic client errors) plus a scaffolded
  **`architecture/security.md`** seeded from an OWASP-aligned MUST table (injection, XSS, broken
  authz/IDOR, auth & sessions, mass assignment, file uploads, SSRF/path traversal, errors & logging,
  abuse controls, dependency audits) with the per-stack decision (ORM · validator · hashing lib) recorded
  per row at intake — scaffolder convention 6 + output contract + tree. Mirrored into the refactorer
  (a "no security baseline → seed it, never invent per-stack choices" detect rule + Target Shape tree),
  `kit/principles.html` (always-on rules 1–8), the example README tree, and the README **Security**
  section + Thai summary. Cross-links the plugin example's §9 for between-plugin least privilege.

## [0.4.0] - 2026-07-02

### Added
- **README Thai summary** — a concise `🇹🇭 สรุปภาษาไทย` section near the top (linked from **Contents**)
  covering the same principles as the English body (router/AGENTS.md/llms.txt, job-first docs, registries,
  plugin lifecycle + the capability/tool split, docs-lint, the measured token-economics headline) for a
  Thai-reading visitor to grasp the kit fast on GitHub. Detailed prose (tables, citations, install steps)
  stays English-only per the kit's own doc-language rule — this is a presentation hook, not a duplicated
  knowledge source.
- **Plugin kinds — separate features from tools** (folded back from a real project using the kit). The
  plugin manifest gains a **`kind`** field — `capability` (in-process feature, default) · `tool` (a backing
  service that ships its own container via a `compose` fragment + a connection contract) · `app` (an
  out-of-process app that owns its container + DB) — plus `compose` and `secrets` manifest fields. Documents
  the **zero-datastore Core** model (Core ships no datastore; a `tool` plugin brings it), the **polyglot
  process-boundary rule** (cross-language allowed iff behind the network seam), and the
  `[Name]-Plugin-Tools-<Infra>` naming convention. Added to `examples/plugin-architecture/system-design.md`
  (new **§3.1**), `reference/manifest.schema.json` (`kind`/`compose`/`secrets`), the example README, the
  scaffolder's **rule 5**, `kit/principles.html`, and the README Examples section.
- **Recommended agent toolchain** — a new **rule 10** in `kit/new-project-scaffold.md` naming the
  high-leverage plugin/MCP set that runs the structure (`superpowers`, `code-review`, `github`, `context7`,
  `claude-md-management`, `skill-creator`, `security-guidance`, a language **LSP** (`pyright-lsp` /
  `typescript-lsp`), `serena`, `hookify`) with a "right-size it / personal tools are per-developer" note.
  Mirrored into `kit/knowledge-refactorer.md` (flag-if-missing scope note), `kit/principles.html` (new
  section 10), and the README **Installation** section.
- **A real `postgres` tool-plugin example** in `examples/plugin-architecture/reference/` — the runnable
  skeleton previously only demonstrated `capability` plugins (`inventory`, `order`). New:
  `plugins/postgres/{manifest.json,compose.fragment.yml,index.ts}` (kind: tool, `secrets`, `compose`),
  `core/contracts/postgres-connection.ts` (the published `postgres.Connection` contract, same pattern as
  `stock-service.ts`), wired into `app/plugins.config.ts`, and documented in `reference/README.md`.
- **`kit/docs-lint.py` — a ready-to-copy reference validator** for the `scripts/docs-lint.py` the scaffolder
  prescribes (rule 8), which previously had **no** shipped implementation (every project reinvented it).
  Stdlib-only, UTF-8-safe; enforces required frontmatter + valid `type`/`status`, balanced frontmatter,
  resolvable relative links, GitHub-style anchors (correct across scripts — e.g. Thai), and the `related:`
  graph. Referenced from the scaffolder rule 8, the refactorer scope note, and the README kit table.
- **This repo now dogfoods its own structure** — added a root `CLAUDE.md` router, `AGENTS.md`, and `llms.txt`
  entry map; a `docs/README.md` index; and frontmatter on `docs/evidence/measurements.md` (it lives under
  `docs/` and so was previously in breach of the kit's own frontmatter rule).

### Changed
- **Every umbrella tree now shows the capability/tool split.** The project-root tree diagrams still drew a
  single `[Name]-Plugin/<id>/` (or `<app>/`) line, so the feature-vs-tool separation was invisible at the
  structure level. Updated the trees in the README Examples section, `kit/new-project-scaffold.md`,
  `kit/knowledge-refactorer.md` (Target Shape), and `kit/principles.html` (§1 mermaid) to show a
  `kind: capability` feature folder **and** a `kind: tool` backing-service folder (postgres/redis/minio,
  own container + compose fragment), and to note the repo-per-plugin evolution
  (`[Name]-Plugin-<Feature>/` · `[Name]-Plugin-Tools-<Infra>/`) matching a real deployed project — while
  keeping the single-repo default that the example's CI gates assume.
- **Renamed the generic host repo `[Name]-Main` → `[Name]-Core`** across the kit for one vocabulary
  (`[Name]-{Core,Docs,Plugin}`), and reframed it as *the primary/host app everything plugs into + the
  promotion target*. Lifecycle prose followed (`fold into core`, `dependency direction core→plugin`,
  `promote into core`, `Core = base pair`) in `kit/new-project-scaffold.md`, `kit/knowledge-refactorer.md`,
  `kit/principles.html`, and the README. The `examples/plugin-architecture/` naming note now *keeps* `Core`
  (matching the kit) and tightens it to an infra-only host rather than renaming `Main`→`Core`. The git
  branch `main` and `src/main.ts` entrypoints are unchanged; earlier released changelog entries keep their
  original wording.
- **`scripts/docs-lint.sh` now checks internal links** — it validates that every relative Markdown link
  resolves and **fails the build** on a broken one (previously only the advisory lychee CI step touched
  links, with `fail: false`), so this repo's own tooling now backs the "broken link → build red" claim.
- **Clarified that `[Name]-App` is added by the example, not scaffolded.** The scaffolder creates three
  repos (`Core`/`Docs`/`Plugin`); the plugin-architecture example adds a fourth (`App`). Re-marked the
  `Acme-App/` tree rows in the example README as `app` (was `scaffold`) and reworded the README Examples
  heading to "the four repos this example uses".

### Fixed
- **Stale `updated:` frontmatter dates.** `kit/new-project-scaffold.md`, `kit/knowledge-refactorer.md`
  (both `2026-06-20`) and `examples/plugin-architecture/system-design.md` (`2026-06-29`) had not been
  bumped to their real edit date despite substantive later edits — a breach of the kit's own docs-discipline
  and frontmatter schema. Set to the edit date.
- **`kit/principles.html` still misused the repo-name convention as the plugin id.** The §3 note read
  "a `tool` plugin (`[Name]-Plugin-Tools-<Infra>`) brings it" — the exact `id` vs repo-name confusion an
  earlier commit fixed everywhere *except* this HTML mirror. Corrected it to "folder = the lowercase `id`,
  e.g. `postgres/`" and split the §1 mermaid to show separate `capability` and `tool` folders, matching the
  change the changelog already claimed.
- **README Thai summary was missing the agent-toolchain recommendation** — the English body has a full
  "Recommended agent toolchain" table (scaffolder rule 10) but the `🇹🇭 สรุปภาษาไทย` section never
  mentioned it, so a Thai-reading visitor could miss the whole install-these-plugins step. Added a
  "ต้องติดตั้ง plugin/MCP อะไรให้ agent บ้าง" section listing all 10 (superpowers, code-review, github,
  context7, claude-md-management, skill-creator, security-guidance, a language LSP, serena, hookify), and
  added a matching "**A recommended agent toolchain**" bullet to the English **What you get** list so the
  feature is visible there too, not only buried in Installation.
- **Tool-plugin naming was inconsistent with its own schema.** The plugin-kinds tree examples used a
  `Tools-Postgres/`-style folder name, but the manifest `id` pattern is lowercase-only (`^[a-z][a-z0-9-]*$`)
  and namespaces everything (§6) — so the folder must be `postgres/`, matching the `id`. Fixed the tree
  diagrams in `kit/new-project-scaffold.md` (which previously had **no** tool-plugin example at all),
  `examples/plugin-architecture/system-design.md` §1/§3.1, and the example README, and clarified that
  `[Name]-Plugin-Tools-<Infra>` is a *repo-name* convention (used only once a tool is promoted to its own
  repo) — never the manifest `id` or its folder.
- Updated the top-level README's Examples section to point at the real `postgres` reference example and
  the same id-vs-repo-name clarification, instead of the stale `[Name]-Plugin-Tools-Postgres` naming.

## [0.3.0] - 2026-06-29

### Added
- **`examples/plugin-architecture/`** — a worked Strict Full Plugin Architecture example: an enforceable
  `system-design.md`, a runnable `reference/` skeleton (Core contract + `inventory`/`order` plugins + the App
  composition root), and two copy-paste CI gates (`manifest.schema.json` + a `dependency-cruiser` config that
  blocks plugin→plugin imports). Linked from a new README **Examples** section.

### Changed
- **Renamed the "Standalone" line → "Plugin"** across the kit for one consistent vocabulary: `[Name]-Standalone`
  → `[Name]-Plugin`, the `standalone/` docs folder → `plugin/`, and "standalone lifecycle / standalone-first"
  → "plugin lifecycle / plugin-first" in `kit/new-project-scaffold.md`, `kit/knowledge-refactorer.md`,
  `kit/principles.html`, and the README. The lifecycle semantics are unchanged (build-independently-first →
  gated promotion → dependency direction main→plugin). Earlier released entries keep their original wording.
- README intro + "What you get" now list the worked example; **Contents** nav added for one-page browsing.
- **Line endings normalized to LF repo-wide** via `.gitattributes` (`* text=auto eol=lf`), ending the CRLF
  churn and restoring the `docs-lint` run.

## [0.2.1] - 2026-06-20

### Changed
- **`kit/principles.html`** refreshed to match the v0.2 prompts: new "Start here" section (new-vs-refactor
  routing · back up before refactoring · key/secret handling), rule 2 updated with any-source secret
  handling, plus new sections for token economics (measured) and anti-drift ("won't drift / remembers
  mistakes").

## [0.2.0] - 2026-06-20

### Added
- **OpenSSF Best Practices passing badge** (project 13318) + a Security policy badge in the README.
- **`scripts/docs-lint.sh`** automated docs test suite, wired into a **`docs-lint`** GitHub Actions workflow
  (runs on every push/PR, plus a Markdown link check) — verified green in CI.
- Scaffolder **guided intake**: asks *new vs refactor* first, then takes name + logic, then a **tiered stack
  interview** (each question carries a recommendation + reason; the stack is never fixed in the prompt).
- Explicit **AI key/secret-handling rule** (applies to any source, not only `.env`) in both prompts, and a
  **Security & secret handling** section in the README.
- **Backup / clean-git-tree guardrail** before refactoring (and before scaffolding into a non-empty folder),
  plus a prominent backup warning in the README.
- **Token economics** and **anti-drift** README sections, backed by **`docs/evidence/measurements.md`**
  (real `tiktoken` measurements + a docs-lint pass/fail demonstration) and research citations.
- README **Installation** section and a **`new-project/`** entry in the kit.

### Changed
- Repo layout tidied for clarity: the three kit files moved into **`kit/`**; community-health files
  (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`) moved into **`.github/`** (still auto-detected by GitHub).
  Internal links and badge URLs updated accordingly.

### Security
- Documented end-to-end secret handling; confirmed no real secrets are tracked or present in git history,
  and that `*.example` templates carry placeholders only.

## [0.1.0] - 2026-06-20

### Added
- **`new-project-scaffold.md`** — system prompt to bootstrap a new project from zero (umbrella
  `[Name]-Project/` + `[Name]-{Main,Docs,Standalone}` + the full convention set: router, frontmatter,
  registries, standalone lifecycle, runbooks, docs-lint).
- **`knowledge-refactorer.md`** — system prompt to refactor an existing project's Markdown into the same
  architecture, non-destructively (zero information loss).
- **`principles.html`** — visual overview of the structure and workflows (mermaid graphs, English, with an
  offline fallback).
- **`README.md`** — GitHub overview: who it's for, what you get, quality-review scorecard, references.
- Community & security health files: **`LICENSE`** (MIT), **`SECURITY.md`**, **`CONTRIBUTING.md`**,
  **`CODE_OF_CONDUCT.md`**.
- Supply-chain hardening: **OpenSSF Scorecard** workflow, **Dependabot** (GitHub Actions), all CI actions
  pinned by commit SHA.

[Unreleased]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.4.1...HEAD
[0.4.1]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/hellOoSaksit/ai-project-scaffold/releases/tag/v0.1.0

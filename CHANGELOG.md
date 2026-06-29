# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/hellOoSaksit/ai-project-scaffold/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/hellOoSaksit/ai-project-scaffold/releases/tag/v0.1.0

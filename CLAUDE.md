# CLAUDE.md — router for `ai-project-scaffold`

This repo *is* the kit: system-prompt templates + a worked example that install an AI-friendly project
structure. It practices what it prescribes, so this file is the thin router the kit itself mandates —
always-on rules + a map to the doc that owns each topic. Detail lives in the owning file, not here.

## Always-on rules (this repo)

1. **Two prompts, one source of truth.** [`kit/new-project-scaffold.md`](kit/new-project-scaffold.md) is
   **canonical** for the structure + convention set. Any structural change is mirrored, *in the same
   commit*, into every downstream copy: [`kit/knowledge-refactorer.md`](kit/knowledge-refactorer.md) (Target
   Shape), [`kit/principles.html`](kit/principles.html), and the README (English body **and** the
   `🇹🇭 สรุปภาษาไทย` summary). `principles.html` is HTML (grep-resistant) — check it explicitly.
2. **English, generalized, self-contained.** Prompt/doc prose is English (a presentation artifact may use a
   local language). Use `[Name]` / `<app>` placeholders — never hardcode a specific project. Each prompt
   carries its full structure inline; add no external dependency.
3. **No invented facts.** Don't add fictional example content; leave dirs/index rows ready instead.
4. **Docs discipline.** Change a file under `docs/` → update its index row ([`docs/README.md`](docs/README.md))
   in the same commit. Keep every knowledge file's `updated:` frontmatter equal to its edit date.
5. **Secrets.** This repo ships no runtime and no real secrets; keep it that way (only `*.example`
   placeholders, redact any credential to `****`).

## Map / task router

| When you're… | Open |
|---|---|
| Editing the new-project structure or conventions (canonical) | [`kit/new-project-scaffold.md`](kit/new-project-scaffold.md) |
| Editing the existing-project refactor flow | [`kit/knowledge-refactorer.md`](kit/knowledge-refactorer.md) |
| Updating the visual overview | [`kit/principles.html`](kit/principles.html) |
| Working on the plugin-architecture example | [`examples/plugin-architecture/`](examples/plugin-architecture/) — contract in [`system-design.md`](examples/plugin-architecture/system-design.md), runnable skeleton + CI gates in [`reference/`](examples/plugin-architecture/reference/) |
| Touching the docs-lint reference validator | [`kit/docs-lint.py`](kit/docs-lint.py) |
| Looking for the measured evidence | [`docs/README.md`](docs/README.md) → [`docs/evidence/measurements.md`](docs/evidence/measurements.md) |
| Checking build/test/run commands + boundaries | [`AGENTS.md`](AGENTS.md) |

## Validate before you commit

```bash
bash scripts/docs-lint.sh      # required files · balanced frontmatter · internal links (this repo)
python3 kit/docs-lint.py .     # frontmatter + link/anchor/related — the reference the kit installs
```

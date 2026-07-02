# AGENTS.md

Signal-dense entry for coding agents (Codex, Copilot, Cursor, Gemini CLI, Aider…). This repo is the
`ai-project-scaffold` kit: system-prompt templates (`kit/`) + a worked plugin-architecture example
(`examples/`). No application runtime — the deliverable is Markdown, one HTML overview, and one Python
validator.

## Build / test / run

There is nothing to compile or install. Validate the docs before every commit:

```bash
bash scripts/docs-lint.sh      # required files · balanced frontmatter · internal-link resolution
python3 kit/docs-lint.py .     # frontmatter + valid type/status · links · GitHub anchors · related graph
```

`docs-lint.sh` needs only `bash`; `docs-lint.py` needs only Python 3.8+ stdlib (no pip). Both run in CI on
push/PR (`.github/workflows/docs-lint.yml`), which also runs an advisory external-link check (lychee).

## Boundaries (ask before doing)

- **Keep the two prompts in sync.** `kit/new-project-scaffold.md` is canonical; mirror any structural change
  into `kit/knowledge-refactorer.md`, `kit/principles.html`, and the README (incl. the Thai summary) in the
  same commit. See [`CLAUDE.md`](CLAUDE.md) rule 1.
- **English + generalized + self-contained.** `[Name]`/`<app>` placeholders, no external dependency, no
  invented example content.
- **Secrets:** never add a real credential; redact to `****`. This repo tracks none.
- **Don't run git commit/push** unless the user asks.

Depth and the full task router live in [`CLAUDE.md`](CLAUDE.md); contribution rules in
[`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md).

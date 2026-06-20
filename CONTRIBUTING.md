# Contributing

Thanks for helping improve **AI Project Scaffold**. Contributions that add a convention, runbook, or
frontmatter field **proven in a real project** are especially welcome.

## How to propose a change

1. **Open an issue** first for anything non-trivial — describe the problem and the proposed change.
2. **Fork** the repo and create a branch (`feat/…`, `fix/…`, `docs/…`).
3. Make the change (see requirements below).
4. **Open a pull request** against `main`. The CI checks (OpenSSF Scorecard) must pass.

For small fixes (typos, broken links) you can skip the issue and go straight to a PR.

## Requirements for contributions

- **Generalized** — use the `[Name]` / `<app>` placeholders; don't hardcode a specific project.
- **English** — all prompt/doc prose is in English (a presentation artifact may use a local language).
- **Self-contained** — the two prompts must each carry the full structure inline; don't add an external
  dependency.
- **Keep the two prompts in sync** — `new-project-scaffold.md` is the canonical source for the shape and
  convention set; mirror any structural change into `knowledge-refactorer.md`'s Target Shape in the same PR.
- **No invented facts** — don't add fictional example content; leave dirs/index rows ready instead.
- **Match the existing style** — heading levels, table format, tone.

## Reporting bugs & security issues

- **Bugs / ideas:** open a [GitHub issue](https://github.com/hellOoSaksit/ai-project-scaffold/issues).
- **Security / supply-chain issues:** follow [`SECURITY.md`](SECURITY.md) (private advisory preferred).

## Code of conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Contributions are accepted under the project's [MIT License](LICENSE).

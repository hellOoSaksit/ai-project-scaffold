# Security Policy

## Scope

This repository ships **documentation and system-prompt templates** (Markdown + a static HTML overview).
It contains no application runtime, no server, and no dependencies that execute on a user's machine. The
main security surface is the **CI workflow** under `.github/workflows/` and the integrity of the templates.

## Supported versions

The `main` branch is the only supported version. Fixes land on `main`; there are no long-lived release
branches.

## Reporting a vulnerability

If you find a security issue (e.g. a malicious edit to a template, a CI/supply-chain weakness, or a
misleading instruction that could cause an AI agent to take an unsafe action):

1. **Preferred:** open a [private security advisory](https://github.com/hellOoSaksit/ai-project-scaffold/security/advisories/new)
   via GitHub.
2. Or open a regular [issue](https://github.com/hellOoSaksit/ai-project-scaffold/issues) for non-sensitive
   reports.

Please include what you found, where (file + line), and the impact. We aim to acknowledge reports within
**7 days** and to address confirmed issues on `main` as soon as practical.

## Supply-chain hygiene

- GitHub Actions are **pinned by full commit SHA**.
- **Dependabot** watches the Actions ecosystem for updates.
- **OpenSSF Scorecard** runs in CI and publishes its results (see the badge in the README).

---
title: Docs index — ai-project-scaffold
type: index
status: active
keywords: [index, docs map, evidence, measurements, navigation]
related: [../README.md, ./evidence/measurements.md]
summary: >
  Map of this repo's own docs/ tree (read first). This repository ships the kit itself, so docs/ is small —
  it holds the recorded evidence behind the README's claims. The kit's structure/conventions live in the
  prompts under kit/, not here.
updated: 2026-07-02
---

# Docs

This is the **docs index** for the `ai-project-scaffold` repository itself — the same "read this first" map
that the kit prescribes for every scaffolded project (`docs/README.md`, `type: index`).

Because this repo *is* the kit (system-prompt templates + a worked example, not an application), its `docs/`
tree is deliberately small: it holds the reproducible evidence behind the README's headline claims. The
kit's structure, conventions, and lifecycle live in the prompts under [`../kit/`](../kit/), and the worked
plugin architecture lives under [`../examples/`](../examples/).

## Map

| Area | File | What it holds |
|---|---|---|
| Evidence | [`evidence/measurements.md`](evidence/measurements.md) | Verbatim `tiktoken` token-economics counts + a `docs-lint` pass/fail demonstration — the raw runs behind the README's "measured, not guessed" claims. |

> This index follows the kit's own rule: change what lives under `docs/` → update this map in the same
> commit. It is validated by `scripts/docs-lint.sh` (this repo) and by the reference
> [`kit/docs-lint.py`](../kit/docs-lint.py).

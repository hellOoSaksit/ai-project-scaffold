# AI Project Scaffold — an AI-friendly project structure & knowledge architecture

> A portable, self-contained kit for starting **or** restructuring any software project with a clean,
> **AI-friendly** layout that coding agents (**Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI,
> Aider**) navigate well — one `CLAUDE.md` router, `AGENTS.md` + `llms.txt` entry points, job-first docs
> with frontmatter, single-source-of-truth registries, and a `docs-lint` CI check.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made for AI coding agents](https://img.shields.io/badge/made%20for-AI%20coding%20agents-6366f1.svg)](#who-is-this-for)
[![CLAUDE.md](https://img.shields.io/badge/CLAUDE.md-ready-8b5cf6.svg)](new-project-scaffold.md)
[![AGENTS.md](https://img.shields.io/badge/AGENTS.md-ready-10b981.svg)](new-project-scaffold.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

**Keywords:** AI project structure · Claude Code template · `CLAUDE.md` / `AGENTS.md` / `llms.txt` starter ·
AI documentation architecture · RAG knowledge base · monorepo scaffold · AI-first docs · context engineering.

---

## What is this?

Setting up a project so that **AI coding agents stay accurate** is mostly an architecture problem: where
do the rules live, how does an agent find the one doc it needs, how do you stop facts from drifting across
files. This kit answers that with a **proven, opinionated structure** you can drop onto any project — from
a solo app to 100+ services — without reinventing the layout each time.

It ships as **two system prompts** (one to scaffold a new project, one to refactor an existing one) plus a
**visual overview**. Everything is embedded inline — no external reference repo required.

## Who is this for?

| You are… | Use this to… |
|---|---|
| **Developer / engineer** starting a new project or repo | Bootstrap a clean, AI-friendly structure from commit one — no bikeshedding the layout. |
| **Working with AI coding agents** (Claude Code, Cursor, Copilot, Codex, Gemini CLI…) | Get docs an agent navigates well: one router, `AGENTS.md`/`llms.txt` entry points, progressive disclosure, frontmatter for retrieval. |
| **Tech lead / architect** standardizing several projects or teams | Install one proven, repeatable shape (umbrella + Main/Docs/Standalone) everyone inherits. |
| **Team with messy / monolithic existing docs** | Refactor existing Markdown into the same architecture — non-destructively, with zero information loss. |
| **Solo builder / indie hacker** | Skip reinventing structure; start with a battle-tested scaffold and grow from 1 to 100+ services. |

**Not for:** throwaway scripts or a single-file experiment — the structure pays off once a project has real
docs, multiple apps, or AI agents working in it.

## What you get

- **One shared `CLAUDE.md` router** — thin: always-on rules + a task router (progressive disclosure, not a wall of context).
- **`AGENTS.md` entry point** — the de-facto standard read by 30+ agents; signal-dense build/test/run commands + boundaries.
- **`llms.txt` navigation map** — [llmstxt.org](https://llmstxt.org/) format for LLM discovery.
- **Job-first `docs/`** — grouped by job (architecture · features · process · standalone), every file with `title/type/status/keywords/related/summary` frontmatter for RAG.
- **Single-source-of-truth registries** — `ports.md` + `versions.md`, so values never drift.
- **Standalone lifecycle** — build big features as separate apps, then fold back into main on gated promotion.
- **Enforcement** — `docs-lint` (frontmatter + link/anchor validator) wired into CI.

## The kit

| File | Use for |
|---|---|
| [`new-project-scaffold.md`](new-project-scaffold.md) | **Scaffolder** — bootstrap a brand-new project from zero: umbrella `[Name]-Project/` + `[Name]-{Main,Docs,Standalone}` + every convention (router · frontmatter · registries · standalone lifecycle · runbooks · skills · enforcement). |
| [`knowledge-refactorer.md`](knowledge-refactorer.md) | **Refactorer** — refactor an *existing* project's Markdown into this architecture (one shared router · README = GitHub · `docs/` in English). |
| [`principles.html`](principles.html) | **Visual overview** of the whole structure & workflows as graphs (mermaid) — open in a browser; for attaching/presenting. The `.md` prompts are the source of truth. |

## Quick start

1. Pick the right prompt: **new project → [`new-project-scaffold.md`](new-project-scaffold.md)**; **existing project → [`knowledge-refactorer.md`](knowledge-refactorer.md)**.
2. Paste its full contents into your AI coding agent (Claude Code, Cursor, Copilot, etc.) as the system / instruction prompt.
3. Give it your project name and one line on what it builds.
4. Let the agent create the structure, then commit. Open [`principles.html`](principles.html) to see the shape visually.

> **Self-contained:** these prompts carry the full structure inline, so a new project inherits it without
> depending on any reference codebase. Improve a convention here and every future project picks it up.

## Contributing

Issues and PRs welcome — especially new conventions, runbooks, or frontmatter fields proven in a real
project. Keep changes generalized (`[Name]`/`<app>` placeholders), English, and self-contained.

## License

[MIT](LICENSE) © 2026 Saksit Chuenmaiwaiy

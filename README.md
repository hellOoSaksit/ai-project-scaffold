# AI Project Scaffold — an AI-friendly project structure & knowledge architecture

> A portable, self-contained kit for starting **or** restructuring any software project with a clean,
> **AI-friendly** layout that coding agents (**Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI,
> Aider**) navigate well — one `CLAUDE.md` router, `AGENTS.md` + `llms.txt` entry points, job-first docs
> with frontmatter, single-source-of-truth registries, and a `docs-lint` CI check.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Design review: 100/100](https://img.shields.io/badge/design%20review-100%2F100-brightgreen.svg)](#-quality-review--benchmarks)
[![Made for AI coding agents](https://img.shields.io/badge/made%20for-AI%20coding%20agents-6366f1.svg)](#who-is-this-for)
[![CLAUDE.md](https://img.shields.io/badge/CLAUDE.md-ready-8b5cf6.svg)](kit/new-project-scaffold.md)
[![AGENTS.md](https://img.shields.io/badge/AGENTS.md-ready-10b981.svg)](kit/new-project-scaffold.md)
[![llms.txt](https://img.shields.io/badge/llms.txt-ready-f59e0b.svg)](https://llmstxt.org/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

<!-- live project stats (auto-updating) + external automated health score -->
[![Stars](https://img.shields.io/github/stars/hellOoSaksit/ai-project-scaffold)](https://github.com/hellOoSaksit/ai-project-scaffold/stargazers)
[![Forks](https://img.shields.io/github/forks/hellOoSaksit/ai-project-scaffold)](https://github.com/hellOoSaksit/ai-project-scaffold/network/members)
[![Contributors](https://img.shields.io/github/contributors/hellOoSaksit/ai-project-scaffold)](https://github.com/hellOoSaksit/ai-project-scaffold/graphs/contributors)
[![Issues](https://img.shields.io/github/issues/hellOoSaksit/ai-project-scaffold)](https://github.com/hellOoSaksit/ai-project-scaffold/issues)
[![Last commit](https://img.shields.io/github/last-commit/hellOoSaksit/ai-project-scaffold)](https://github.com/hellOoSaksit/ai-project-scaffold/commits/main)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/hellOoSaksit/ai-project-scaffold/badge)](https://scorecard.dev/viewer/?uri=github.com/hellOoSaksit/ai-project-scaffold)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/13318/badge)](https://www.bestpractices.dev/projects/13318)

**Keywords:** AI project structure · Claude Code template · `CLAUDE.md` / `AGENTS.md` / `llms.txt` starter ·
AI documentation architecture · RAG knowledge base · monorepo scaffold · AI-first docs · context engineering.

> ⭐ **If this saves you setup time, star the repo** — it helps others find it.

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

## 🏅 Quality review & benchmarks

This kit is **continuously reviewed against published best-practice standards** — not shipped and forgotten.
The latest structured design review used the 5-dimension rubric below, **benchmarked against the
[references](#-references--research)**, and scored it **100/100**: drift between the two prompts eliminated,
the visual overview validated, and every internal link checked.

| Dimension | Score | What was checked |
|---|:--:|---|
| **Structure / Clarity** | 5/5 | umbrella + job-first docs + progressive disclosure; single-root vs nested-monorepo justified |
| **Completeness** | 5/5 | router · entry files · frontmatter · registries · standalone lifecycle · runbooks · enforcement · CI |
| **Best-practice alignment** | 5/5 | matches the **AGENTS.md** & **llms.txt** specs; acknowledges **Diátaxis** & the nested-monorepo pattern |
| **Maintainability** | 5/5 | one canonical source + a bidirectional sync rule → **zero drift** between the two prompts |
| **AI-readability** | 5/5 | frontmatter for retrieval · English · signal-dense entry files · intent encoded in `type:` |
| **Total** | **100/100** | structured design review, benchmarked to the sources below |

> **Transparency:** the score is a *structured self-review* against external standards, not a third-party
> audit. The rubric and every reference are public — so you can re-run the judgement yourself.

**Two different scores, kept separate (don't conflate them):**

| Score | Source | Measures |
|---|---|---|
| **100/100** (above) | structured self-review vs published standards | *design quality* of the structure |
| **OpenSSF Scorecard** badge (top) | [OpenSSF](https://securityscorecards.dev/) automated analysis, runs in CI | *supply-chain / repo-health & security posture* — **not** content quality |

The Scorecard badge populates after the [Scorecard workflow](.github/workflows/scorecard.yml) runs once on
CI. The live **stars / forks / contributors** badges are objective GitHub stats that grow over time.

## The kit

| File | Use for |
|---|---|
| [`kit/new-project-scaffold.md`](kit/new-project-scaffold.md) | **Scaffolder** — bootstrap a brand-new project from zero: umbrella `[Name]-Project/` + `[Name]-{Main,Docs,Standalone}` + every convention (router · frontmatter · registries · standalone lifecycle · runbooks · skills · enforcement). |
| [`kit/knowledge-refactorer.md`](kit/knowledge-refactorer.md) | **Refactorer** — refactor an *existing* project's Markdown into this architecture (one shared router · README = GitHub · `docs/` in English). |
| [`kit/principles.html`](kit/principles.html) | **Visual overview** of the whole structure & workflows as graphs (mermaid) — open in a browser; for attaching/presenting. The `.md` prompts are the source of truth. |

## Installation

This kit is **prompts, not a dependency** — there's nothing to compile or `npm install`. You "install" it by
dropping the prompt into your AI agent. Pick whichever fits:

**A — Clone the repo** (gets everything: both prompts, `kit/principles.html`, and the `docs-lint` suite):

```bash
git clone https://github.com/hellOoSaksit/ai-project-scaffold.git
cd ai-project-scaffold
```

**B — Grab one file, no install** — open [`kit/new-project-scaffold.md`](kit/new-project-scaffold.md) or
[`kit/knowledge-refactorer.md`](kit/knowledge-refactorer.md) on GitHub and copy the raw contents. Each file is
fully self-contained, so a single copy is enough.

**Set it up in your agent:**

| Agent | Where to put the prompt |
|---|---|
| **Claude Code** | Paste into your project's `CLAUDE.md`, or pass the file as the system / instruction prompt. |
| **Cursor** | New chat → paste as the instruction, or add it to `.cursorrules`. |
| **GitHub Copilot** | Paste into `.github/copilot-instructions.md`. |
| **Codex · Gemini CLI · Aider** | Paste as the system / instruction prompt at the start of the session. |

**Run the docs-lint suite** (optional — validates the docs after the agent scaffolds them):

```bash
bash scripts/docs-lint.sh
```

Needs only `bash` (built in on macOS/Linux; on Windows use Git Bash or WSL). It also runs automatically in CI
on every push and pull request.

## Usage

1. Pick the right prompt: **new project → [`kit/new-project-scaffold.md`](kit/new-project-scaffold.md)**; **existing project → [`kit/knowledge-refactorer.md`](kit/knowledge-refactorer.md)**.
2. Paste its full contents into your AI coding agent (Claude Code, Cursor, Copilot, etc.) as the system / instruction prompt.
3. Give it your project name and one line on what it builds.
4. Let the agent create the structure, then commit. Open [`kit/principles.html`](kit/principles.html) to see the shape visually.

> **Self-contained:** these prompts carry the full structure inline, so a new project inherits it without
> depending on any reference codebase. Improve a convention here and every future project picks it up.

## 📚 References & research

The structure and the review rubric are grounded in published standards and research — read them and judge for yourself:

**Standards & specs**
- [AGENTS.md spec & recommended sections (2026)](https://www.morphllm.com/agents-md-guide)
- [AGENTS.md — a research-backed guide (ASDLC)](https://asdlc.io/practices/agents-md-spec/)
- [llms.txt specification (llmstxt.org)](https://llmstxt.org/)
- [Anthropic — Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- [CLAUDE.md, AGENTS.md & Copilot instructions — configuration guide (DeployHQ)](https://www.deployhq.com/blog/ai-coding-config-files-guide)

**Research that shaped the scoring**
- [“Your AGENTS.md is probably too long” — *less is more* (Upsun)](https://developer.upsun.com/posts/ai/agents-md-less-is-more) — bloated / auto-generated context files **lower** agent task-success and raise cost ~20%; minimal, hand-written ones help (~+4%). That finding is *why* the entry files here are deliberately **signal-dense**, not exhaustive.
- [CLAUDE.md best practices — 10 sections to include (UX Planet)](https://uxplanet.org/claude-md-best-practices-1ef4f861ce7c) — tiered, living, link-out-not-inline.

**Frameworks & patterns**
- [Diátaxis documentation framework](https://diataxis.fr/) — why this kit groups docs **job-first** and encodes Diátaxis intent in frontmatter `type:` instead of the folder tree.
- [The “Virtual Monorepo” pattern (Owen Zanzal)](https://medium.com/devops-ai/the-virtual-monorepo-pattern-how-i-gave-claude-code-full-system-context-across-35-repos-43b310c97db8) — one shared router across many repos.

**Real-world examples**
- [claude-code-best-practices — 11 CLAUDE.md templates](https://github.com/MuhammadUsmanGM/claude-code-best-practices)
- [duyet/monorepo — AGENTS.md as the canonical CLAUDE.md entrypoint](https://github.com/duyet/monorepo/blob/master/CLAUDE.md)

## Contributing

Issues and PRs welcome — especially new conventions, runbooks, or frontmatter fields proven in a real
project. Keep changes generalized (`[Name]`/`<app>` placeholders), English, and self-contained.

If you adopt this in a project, a ⭐ or a link back helps others discover it.

## License

[MIT](LICENSE) © 2026 Saksit Chuenmaiwaiy

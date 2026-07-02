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
[![Security policy](https://img.shields.io/badge/security-policy-blue.svg)](.github/SECURITY.md)
[![Live overview](https://img.shields.io/badge/live-visual%20overview-8b5cf6.svg)](https://helloosaksit.github.io/ai-project-scaffold/kit/principles.html)

**Keywords:** AI project structure · Claude Code template · `CLAUDE.md` / `AGENTS.md` / `llms.txt` starter ·
AI documentation architecture · RAG knowledge base · monorepo scaffold · AI-first docs · context engineering.

> ⭐ **If this saves you setup time, star the repo** — it helps others find it.

---

## 🇹🇭 สรุปภาษาไทย

> รายละเอียดเต็ม (โค้ด ตาราง งานวิจัยอ้างอิง) อยู่เป็นภาษาอังกฤษด้านล่างทั้งหมด ส่วนนี้อธิบายหลักการแบบง่ายๆ ก่อน

**ปัญหาคืออะไร**

เวลาใช้ AI (Claude Code, Cursor, Copilot ฯลฯ) ช่วยทำงานในโปรเจกต์ใหญ่ๆ ปัญหาที่เจอบ่อยคือ AI หาเอกสารไม่เจอ เปิดผิดไฟล์ หรือเอกสารสองที่เขียนไม่ตรงกัน (เช่นไฟล์นึงบอก port 8000 อีกไฟล์บอก 8080) ปัญหาแบบนี้แก้ด้วยการเขียนพรอมต์เก่งๆ อย่างเดียวไม่ได้ ต้องเริ่มจาก**จัดโครงสร้างโปรเจกต์ให้ถูก** — kit นี้คือโครงสร้างสำเร็จรูปสำหรับเรื่องนั้น

**ในโครงสร้างนี้มีอะไรบ้าง**

- **CLAUDE.md** — ไฟล์เดียวที่ AI เปิดอ่านก่อนเสมอ เขียนสั้นๆ แค่กฎหลักกับบอกว่า "เรื่องนี้ให้ไปอ่านไฟล์ไหนต่อ" ไม่ใส่รายละเอียดทุกอย่างลงไฟล์นี้ เพราะจะยาวจนกิน token เยอะโดยไม่จำเป็น
- **AGENTS.md** — คล้ายกัน แต่เป็นไฟล์มาตรฐานที่ AI tool ตัวอื่น (Cursor, Copilot, Codex) อ่านได้ด้วย
- **docs/ ที่แบ่งเป็นไฟล์ย่อยตามเรื่อง** — เช่น แยกไฟล์ architecture, features, process แต่ละไฟล์มี metadata บอกว่าไฟล์นี้เกี่ยวกับอะไร ทำให้ AI เปิดอ่านแค่ไฟล์ที่เกี่ยวจริงๆ ไม่ต้องโหลดเอกสารทั้งโปรเจกต์
- **Registry** — ค่าที่ต้องมีที่เดียว เช่น port, version เก็บไว้ในไฟล์เดียว (`ports.md`, `versions.md`) ไม่กระจายไปเขียนซ้ำหลายที่ กันปัญหาไฟล์นึงบอกอย่าง อีกไฟล์บอกอีกอย่าง
- **Plugin** — ฟีเจอร์ใหม่แต่ละตัวแยกเป็น plugin ของตัวเอง ถอดออกได้โดยไม่กระทบส่วนอื่น พอฟีเจอร์นิ่งแล้วค่อยรวมเข้า Core ทีหลัง และแยกชัดระหว่าง plugin ที่เป็นฟีเจอร์ (รันในโปรเซสเดียวกับ Core) กับ plugin ที่เป็น **tool** (เช่น Postgres, Redis, MinIO — มีคอนเทนเนอร์ของตัวเอง แยกออกไปต่างหาก) ดูตัวอย่างเต็มที่ [Examples](#-examples)
- **docs-lint** — สคริปต์ที่รันใน CI คอยเช็คว่าลิงก์ไม่พัง เอกสารไม่ขาดตก ถ้าพังคือ build แดงทันที ไม่ปล่อยให้เอกสารค่อยๆ เพี้ยนไปเรื่อยๆ

**ต้องติดตั้ง plugin/MCP อะไรให้ agent บ้าง**

มีแค่โครงสร้างไฟล์เฉยๆ ไม่พอ ต้องมี agent ที่ "ใช้" โครงสร้างนี้เป็นด้วย ชุดที่แนะนำ (ชื่อเป็น plugin/MCP ของ Claude Code — agent ตัวอื่นก็หาของเทียบเคียงได้):

- **superpowers** — กระบวนการทำงานหลักของ agent (brainstorm / TDD / debug) แทนที่จะแก้โค้ดมั่วๆ
- **code-review** — รีวิว diff/PR ก่อน merge
- **github** — จัดการ PR/issue จาก agent ได้เลย
- **context7** — ดึงเอกสาร library เวอร์ชันล่าสุดมาใช้ กัน AI เขียนโค้ดตาม API เก่าที่จำมาผิด
- **claude-md-management** — ดูแล `CLAUDE.md` ให้บางและตรงกับโปรเจกต์เสมอ ไม่ปล่อยให้บวมจนกิน token
- **skill-creator** — แปลง workflow ที่ agent ทำซ้ำบ่อยๆ ให้เป็น skill ของตัวเอง
- **security-guidance** — เตือนเรื่อง security ระหว่างแก้โค้ด
- **LSP ของภาษาที่ใช้** (เช่น `pyright-lsp` สำหรับ Python, `typescript-lsp` สำหรับ JS/TS) — ให้ go-to-definition/type-check แม่นกว่า grep เยอะ **โปรเจกต์ที่มีโค้ดจริงควรมี**
- **serena** — semantic code search ใช้ได้กับทุกภาษา โปรเจกต์ยิ่งใหญ่ยิ่งจำเป็น
- **hookify** — เอากฎเฉพาะของโปรเจกต์ (เช่น "รันใน sandbox เท่านั้น") มาทำเป็น guardrail hook บังคับอัตโนมัติ ไม่ต้องหวังให้ agent จำเอง

ชุดนี้คือชุดเต็มสำหรับโปรเจกต์จริงจัง สคริปต์เล็กๆ ไม่ต้องติดครบทุกตัว รายละเอียด + เหตุผลของแต่ละตัวอยู่ที่ [Installation](#installation)

**ทำไมถึงคุ้ม**

มีคนวัดจริงด้วย `tiktoken` (ไม่ใช่เดาเอา) ว่าพอใช้โครงสร้างนี้ AI โหลด context น้อยลง **83–96%** ต่องาน เพราะเปิดแค่ไฟล์ที่เกี่ยวจริงๆ ไม่ต้องโหลดทั้งคลังความรู้ ดูตัวเลขจริงที่ [Token economics](#-token-economics--measured-not-guessed)

**เหมาะกับใคร**

คนที่เริ่มโปรเจกต์ใหม่แล้วไม่อยากมานั่งคิดเองว่าจะจัดโครงสร้างยังไง, tech lead ที่อยากได้มาตรฐานเดียวใช้กับหลายทีม, หรือทีมที่เอกสารกระจัดกระจายอยากจัดใหม่โดยไม่ให้ข้อมูลหาย — **ไม่เหมาะ** กับสคริปต์เล็กๆ หรือโปรเจกต์ไฟล์เดียว เพราะไม่คุ้มที่จะจัดโครงสร้างขนาดนี้

**เริ่มใช้ยังไง**

เปิดไฟล์ [`kit/new-project-scaffold.md`](kit/new-project-scaffold.md) (ถ้าเริ่มโปรเจกต์ใหม่) หรือ [`kit/knowledge-refactorer.md`](kit/knowledge-refactorer.md) (ถ้ามีโปรเจกต์เดิมอยู่แล้วอยากจัดเอกสารใหม่) copy เนื้อหาทั้งไฟล์ไปวางเป็น system prompt ให้ AI agent บอกชื่อโปรเจกต์กับสิ่งที่มันทำสั้นๆ แล้วปล่อยให้ AI จัดโครงสร้างให้เลย ขั้นตอนละเอียดอยู่ที่ [Installation](#installation)

---

## Contents

- [🇹🇭 สรุปภาษาไทย](#-สรุปภาษาไทย)
- [What is this?](#what-is-this) · [Who is this for?](#who-is-this-for) · [What you get](#what-you-get)
- [🔒 Security & secret handling](#-security--secret-handling) · [🏅 Quality review & benchmarks](#-quality-review--benchmarks) · [💸 Token economics](#-token-economics--measured-not-guessed) · [🧭 Won't drift as it grows](#-wont-drift-as-it-grows--and-it-remembers-its-mistakes)
- [The kit](#the-kit) · [🧩 Examples](#-examples) · [Installation](#installation) · [Usage](#usage)
- [📚 References & research](#-references--research) · [Contributing](#contributing) · [License](#license)

---

## What is this?

Setting up a project so that **AI coding agents stay accurate** is mostly an architecture problem: where
do the rules live, how does an agent find the one doc it needs, how do you stop facts from drifting across
files. This kit answers that with a **proven, opinionated structure** you can drop onto any project — from
a solo app to 100+ services — without reinventing the layout each time.

It ships as **two system prompts** (one to scaffold a new project, one to refactor an existing one), a
**visual overview**, and a **worked example** — a full plugin architecture with a runnable reference and
copy-paste CI gates. The prompts are self-contained and embedded inline — no external reference repo required.

## Who is this for?

| You are… | Use this to… |
|---|---|
| **Developer / engineer** starting a new project or repo | Bootstrap a clean, AI-friendly structure from commit one — no bikeshedding the layout. |
| **Working with AI coding agents** (Claude Code, Cursor, Copilot, Codex, Gemini CLI…) | Get docs an agent navigates well: one router, `AGENTS.md`/`llms.txt` entry points, progressive disclosure, frontmatter for retrieval. |
| **Tech lead / architect** standardizing several projects or teams | Install one proven, repeatable shape (umbrella + Core/Docs/Plugin) everyone inherits. |
| **Team with messy / monolithic existing docs** | Refactor existing Markdown into the same architecture — non-destructively, with zero information loss. |
| **Solo builder / indie hacker** | Skip reinventing structure; start with a battle-tested scaffold and grow from 1 to 100+ services. |

**Not for:** throwaway scripts or a single-file experiment — the structure pays off once a project has real
docs, multiple apps, or AI agents working in it.

## What you get

- **One shared `CLAUDE.md` router** — thin: always-on rules + a task router (progressive disclosure, not a wall of context).
- **`AGENTS.md` entry point** — the de-facto standard read by 30+ agents; signal-dense build/test/run commands + boundaries.
- **`llms.txt` navigation map** — [llmstxt.org](https://llmstxt.org/) format for LLM discovery.
- **Job-first `docs/`** — grouped by job (architecture · features · process · plugin), every file with `title/type/status/keywords/related/summary` frontmatter for RAG.
- **Single-source-of-truth registries** — `ports.md` + `versions.md`, so values never drift.
- **Plugin lifecycle** — build big features as separate apps, then fold back into core on gated promotion.
- **Enforcement** — `docs-lint` (frontmatter + link/anchor validator) wired into CI; LF normalized repo-wide via `.gitattributes`.
- **A worked example** — a full [plugin-architecture](examples/plugin-architecture/) build (Core + Plugin + App + Docs) with an enforceable `system-design.md`, a runnable reference skeleton, and two copy-paste CI gates (manifest schema + a no-plugin→plugin-imports check).
- **A recommended agent toolchain** — a curated plugin/MCP set (process skills, code review, VCS, fresh library docs, router upkeep, a language LSP, semantic search, guardrail hooks) so the agent works *with* the structure above instead of around it — see [Installation](#installation).

## 🔒 Security & secret handling

> [!IMPORTANT]
> **Keys never live in the repo — and your AI agent is told so, explicitly.** The scaffolded
> `CLAUDE.md` / `AGENTS.md` carry a **hard rule** for handling credentials **from any source** (not just
> `.env` — also config files, MCP config, pasted snippets, logs, command output): never print / log /
> paste a real key value (redact to `****`), never hardcode or commit one (only `*.example` placeholders),
> never put a real secret in a browser-shipped frontend env (`VITE_*` / `NEXT_PUBLIC_*`), and **flag +
> rotate** any leaked key.

What the kit bakes in:

- **Secrets only in gitignored env files** — commit `*.example` placeholders only; never in code, docs, or the frontend bundle.
- **Prod boot-guard** — the app refuses to start in `production` while any credential is still a dev default.
- **AI-aware by default** — the agent rules above mean assistants redact keys, don't echo them back, and won't commit one by accident.
- **Supply-chain hygiene** — GitHub Actions SHA-pinned · Dependabot on · **OpenSSF Scorecard** in CI · holds the **OpenSSF Best Practices** passing badge (see badges up top).

Found a vulnerability? See **[`SECURITY.md`](.github/SECURITY.md)** — a private advisory is preferred.

## 🏅 Quality review & benchmarks

This kit is **continuously reviewed against published best-practice standards** — not shipped and forgotten.
The latest structured design review used the 5-dimension rubric below, **benchmarked against the
[references](#-references--research)**, and scored it **100/100**: drift between the two prompts eliminated,
the visual overview validated, and every internal link checked.

| Dimension | Score | What was checked |
|---|:--:|---|
| **Structure / Clarity** | 5/5 | umbrella + job-first docs + progressive disclosure; single-root vs nested-monorepo justified |
| **Completeness** | 5/5 | router · entry files · frontmatter · registries · plugin lifecycle · runbooks · enforcement · CI |
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

## 💸 Token economics — measured, not guessed

Built on how LLMs actually spend tokens, then **measured on a real project that uses this kit** (42 docs,
~122k tokens of knowledge). With progressive disclosure the agent loads the thin router + `llms.txt` + only
the doc that *owns* the task — not the whole knowledge base:

| Task | Loaded *with* the structure | Load the full KB | Saved |
|---|--:|--:|--:|
| Allocate a host port | 4,499 | 125,334 | **96%** |
| Work on a feature (Compare) | 9,017 | 125,334 | **93%** |
| Add a backend endpoint | 11,617 | 125,334 | **91%** |
| Change the DB schema | 19,177 | 125,334 | **85%** |
| Start a new session | 21,103 | 125,334 | **83%** |

*Measured with `tiktoken` (cl100k_base); "full KB" = router + every doc (the no-map worst case). Real
per-task savings land **83–96%**. Picking which doc to open costs only ~5.5k tokens (all 42 frontmatter
blocks combined). Treat "full KB" as an upper bound — the structural point is: open **1 owning doc, not 42**.*

**Raw run, method & how to reproduce:** [`docs/evidence/measurements.md`](docs/evidence/measurements.md) — verbatim `tiktoken` output, not estimates.

Why it holds, from published work:

- **Load less, on purpose.** Anthropic's guidance is to find *"the smallest possible set of high-signal tokens"* and to treat context as *"a finite resource with diminishing marginal returns"* (context rot). The thin router + `llms.txt` identifiers + just-in-time **progressive disclosure** are exactly that. — [Anthropic, *Effective context engineering*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Big context also hurts accuracy.** *Lost in the Middle* finds a U-shaped curve — accuracy drops **>30%** when the needed fact sits mid-context. Smaller context is cheaper **and** more correct. — [Liu et al., TACL 2023](https://arxiv.org/abs/2307.03172)
- **Bloated context files cost more and work worse** (~**+20%** cost, lower task success) vs minimal hand-written ones — why `AGENTS.md` here is signal-dense, not exhaustive. — [Upsun](https://developer.upsun.com/posts/ai/agents-md-less-is-more)
- **English docs are cheaper per token** — up to **15×** token disparity across languages; Thai measured here at **×2.8–6** the English count for the same meaning (`hello` = 1 token vs `สวัสดี` = 6). The kit mandates English doc prose (local language only for *content*). — [Petrov et al., NeurIPS 2023](https://aleksandarpetrov.github.io/tokenization-fairness/)

**When it does *not* pay:** a throwaway script, or docs left to bloat (the exact failure the research warns about).

## 🧭 Won't drift as it grows — and it remembers its mistakes

Structure alone isn't enough; the kit wires in the feedback loops that keep a long-running project on track
instead of slowly rotting:

- **One map, every time** — every task re-enters through the single `CLAUDE.md` router + `llms.txt`, so the agent navigates from the same map and doesn't wander or re-invent paths.
- **It resumes, not restarts** — `process/session-handoff.md` carries the live status + a "resume here" prompt, updated each session, so the next session (or a different agent) picks up exactly where the last one stopped.
- **It remembers its mistakes** — `process/lessons.md` is a running log of decisions made, traps hit *for real*, and known-but-unfixed risks, so the same wrong turn isn't taken twice.
- **Recurring work is a runbook, not a guess** — `process/ai-runbooks.md` (R1–R8: pause/resume · move machine · remove a lib · audit deps · incident/rollback · release · expose a plugin · create a skill).
- **Drift can't pass silently** — `docs-lint` runs in CI and **fails** on a broken link/anchor or missing/invalid frontmatter, so the docs and their `related:` graph can't quietly fall out of sync with the code.
- **Values can't drift** — single-source-of-truth registries (`ports.md`, `versions.md`), read + updated in the same commit; no duplicated numbers diverging across files.
- **Change keeps the map true** — the rule "update the owning doc **and** its index in the same commit" (plus "one file = one concept" and "reuse before you build") bounds sprawl as the project scales.

**Proof the guard bites** (real `docs-lint` run — clean → broken link → exit 1 → green again): [`docs/evidence/measurements.md`](docs/evidence/measurements.md).

## The kit

| File | Use for |
|---|---|
| [`kit/new-project-scaffold.md`](kit/new-project-scaffold.md) | **Scaffolder** — bootstrap a brand-new project from zero: umbrella `[Name]-Project/` + `[Name]-{Core,Docs,Plugin}` + every convention (router · frontmatter · registries · plugin lifecycle · runbooks · skills · enforcement). |
| [`kit/knowledge-refactorer.md`](kit/knowledge-refactorer.md) | **Refactorer** — refactor an *existing* project's Markdown into this architecture (one shared router · README = GitHub · `docs/` in English). |
| [`kit/principles.html`](kit/principles.html) | **Visual overview** of the whole structure & workflows as graphs (mermaid) — **[open the live version ↗](https://helloosaksit.github.io/ai-project-scaffold/kit/principles.html)** (GitHub Pages) or open the file locally; for attaching/presenting. The `.md` prompts are the source of truth. |
| [`kit/docs-lint.py`](kit/docs-lint.py) | **Reference validator** the scaffolder installs as `scripts/docs-lint.py` (rule 8) — stdlib-only, UTF-8-safe; enforces required frontmatter + valid `type`/`status`, resolvable relative links, GitHub-style anchors, and the `related:` graph. Copy it into your docs repo and wire CI at it. |

## 🧩 Examples

Worked, opinionated applications of the kit — copy the shape, not just the idea.

| Example | What it shows |
|---|---|
| [**Strict Full Plugin Architecture**](examples/plugin-architecture/) | A Core + Plugins app built **inside** the scaffold: a generic `Core` (infra only) + self-contained, removable feature `plugins` + an `App` that assembles and runs the whole system. Ships an enforceable [`system-design.md`](examples/plugin-architecture/system-design.md) and a [runnable reference](examples/plugin-architecture/reference/) with two copy-paste CI gates. |

**The four repos this example uses** — the scaffolder creates the three `[Name]-{Core,Docs,Plugin}` repos;
this example keeps those names (tightening `Core` to an infra-only host) and **adds a fourth, `[Name]-App`**,
the composition root that assembles and runs the system:

```
[Name]-Project/              # workspace root — CLAUDE.md · AGENTS.md · llms.txt        (scaffolder)
├── [Name]-Core/             # the HOST — infra only (Plugin Loader · Router · Event Bus · DI · Auth); ships no datastore  (scaffolder)
├── [Name]-Plugin/           # every plugin is a self-contained folder here — removable, never imports another  (scaffolder)
│   ├── <feature>/           #   kind: capability — an in-process feature (crm, chat, …), same language as Core
│   └── postgres/            #   kind: tool — a backing service in its own container (compose fragment + a connection contract)
├── [Name]-App/              # composition root — wires Core + chosen plugins, RUNS + integration-tests the system  (this example adds)
└── [Name]-Docs/docs/        # all knowledge (architecture/system-design.md lives here) + registries  (scaffolder)
```

> **Grows to repo-per-plugin.** The tree above is the single-repo default (plugins are folders under
> `[Name]-Plugin/`, which is what the example's CI gates assume). When a plugin needs its own release cadence
> it graduates to its **own repo** — `[Name]-Plugin-<Feature>/` for features and `[Name]-Plugin-Tools-<Infra>/`
> for tools (e.g. `[Name]-Plugin-Tools-Postgres`) — while the manifest `id` inside stays the lowercase,
> unprefixed namespace (`postgres`). Same contract either way; only the packaging changes.

**Why it matters** — the design is fully enforceable, not aspirational:

- **One litmus rule** — delete any plugin and `Core` still boots and every other plugin still works (CI matrix).
- **No plugin→plugin imports** — features talk only through a Core interface, the Event Bus, or a DI-resolved contract; a [`dependency-cruiser`](examples/plugin-architecture/reference/.dependency-cruiser.cjs) gate fails CI on a violation.
- **Manifest contract** — a [JSON Schema](examples/plugin-architecture/reference/manifest.schema.json) drives load order, version compatibility, and namespacing; the App boots plugins in topological order.
- **Features vs tools, one manifest field** — `kind: capability` runs in-process (same language as Core); `kind: tool`/`app` is a backing service or app in its own container (ships a `compose` fragment, exposes a connection contract, may be polyglot). Core ships no datastore — a **tool** plugin (folder = the lowercase manifest `id`, e.g. `postgres/`, `redis/`, `minio/`; a runnable [`postgres` example](examples/plugin-architecture/reference/plugins/postgres/) is included) brings it. `[Name]-Plugin-Tools-<Infra>` is a *repo-name* convention for later, once a tool is promoted to its own repo — not the id.

> Want another example (event-sourcing, multi-tenant SaaS, a CLI tool)? Open an issue — examples are the
> fastest way to show the structure paying off on a real shape.

## Installation

This kit is **prompts, not a dependency** — there's nothing to compile or `npm install`. You "install" it by
dropping the prompt into your AI agent. Pick whichever fits:

**A — Clone the repo** (gets everything: both prompts, `kit/principles.html`, the `examples/`, and the `docs-lint` suite):

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

**Recommended agent toolchain** (the structure is inert without an agent that can navigate it — install a
small, high-leverage plugin/MCP set so it works *with* the conventions). Names are the Claude Code
plugin/MCP ecosystem; swap the equivalent on another agent. Full rationale: the scaffolder's **rule 10**.

| Plugin / MCP | Why |
|---|---|
| `superpowers` | Process skills — brainstorm / TDD / debug as the default operating loop. |
| `code-review` | Review the diff/PR for bugs + simplifications before merge (pairs with the CI gates). |
| `github` | Drive PRs/issues from the agent — branch → review → merge in one place. |
| `context7` | Pull a library's *current* docs on demand so code tracks the installed version — kills API drift. |
| `claude-md-management` | Keep the `CLAUDE.md` router thin and current as the project grows. |
| `skill-creator` | Turn a recurring workflow into a `.claude/skills/<name>/SKILL.md`. |
| `security-guidance` | Flag risky patterns while editing — reinforces the key/secret rules at authoring time. |
| **Language LSP** (`pyright-lsp` · `typescript-lsp` · your server) | Trustworthy go-to-definition + type-check, far sharper than grep. **Every real-code repo should have one** — swap the server per language. |
| `serena` | Language-agnostic semantic code search; scales past what grep + one context window can hold. |
| `hookify` | Compile a project's own rules into auto-enforced guardrail hooks. |

> **Right-size it.** The full set is for a real, growing codebase — a throwaway script needs almost none of
> it. Personal-workflow optimizations (a token-saver tied to a specific language or writing style) are
> installed **per developer**, not mandated by the project.

**Run the docs-lint suite.** Two validators, don't conflate them:

```bash
bash scripts/docs-lint.sh      # validates THIS repo (required files · balanced frontmatter · internal links)
python3 kit/docs-lint.py .     # the reference your scaffolded project installs as scripts/docs-lint.py
```

`docs-lint.sh` needs only `bash` (built in on macOS/Linux; on Windows use Git Bash or WSL) and runs in CI
on every push and pull request. `kit/docs-lint.py` is the richer, stdlib-only validator (no pip install)
that the scaffolder drops into a new project's docs repo — it adds required-frontmatter, GitHub-anchor, and
`related:`-graph checks; copy it in and point your project's CI at it.

## Usage

> [!WARNING]
> **Back up first — especially before refactoring.** The refactorer **moves, renames, and rewrites real
> files**. Run it only on a **clean, committed git tree** and on a **new branch** (e.g. `refactor/docs`) —
> or copy the folder first if it isn't a git repo. Review the **before→after map and apply only after you
> approve**. Never run it over uncommitted work: every change should be one `git restore` / `git checkout .`
> away from undo.

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
- [Anthropic — *Effective context engineering for AI agents*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — smallest set of high-signal tokens · context as a finite resource (context rot) · just-in-time progressive disclosure. The basis for the thin router + `llms.txt` + load-the-owning-doc design.
- [Liu et al. — *Lost in the Middle: How Language Models Use Long Contexts* (TACL 2023)](https://arxiv.org/abs/2307.03172) — accuracy degrades (>30%) when relevant info is buried mid-context → smaller, targeted context is cheaper **and** more reliable.
- [Petrov et al. — *Language Model Tokenizers Introduce Unfairness Between Languages* (NeurIPS 2023)](https://aleksandarpetrov.github.io/tokenization-fairness/) — up to 15× token disparity across languages → the reason doc prose is mandated in English (token-cheap), local language only for *content*.

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

# Evidence — measured, reproducible (not floaty)

Raw, recorded results behind the [Token economics](../../README.md#-token-economics--measured-not-guessed)
and [Won't drift](../../README.md#-wont-drift-as-it-grows--and-it-remembers-its-mistakes) claims in the
README. Measured **2026-06-20** on a real production project built with this kit (**PiKaOs** — 42 docs).
Local absolute paths are shortened to repo-relative; numbers and tool output are otherwise verbatim.

---

## 1. Token economics

**Method.** Count tokens with `tiktoken` (`cl100k_base`) for the router (`CLAUDE.md` + `llms.txt`) and
every `docs/**/*.md`. `full-KB` = router + every doc (the no-map worst case). `structured` per task =
router + `llms.txt` + only the doc(s) the task router points to (progressive disclosure).

**Reproduce** (no test program needed — a few lines in a REPL):

```python
import tiktoken, glob
enc = tiktoken.get_encoding("cl100k_base")
tok = lambda p: len(enc.encode(open(p, encoding="utf-8").read()))
docs = glob.glob("PiKaOs-docs/docs/**/*.md", recursive=True)
full_kb = tok("CLAUDE.md") + tok("llms.txt") + sum(tok(p) for p in docs)
task    = tok("CLAUDE.md") + tok("llms.txt") + tok("PiKaOs-docs/docs/architecture/ports.md")
print(full_kb, task, f"{100*(1-task/full_kb):.0f}% saved")
```

**Recorded run output (verbatim):**

```text
tokenizer = tiktoken cl100k_base
knowledge base = 42 docs, 121,974 tokens
router: CLAUDE.md=2,692  llms.txt=668  AGENTS.md=392
all frontmatter blocks (rank-to-pick cost) = 5,555 tokens (5% of KB)
full-KB load (CLAUDE.md + llms.txt + every doc) = 125,334 tokens

per-task: load router + llms.txt + only the owning doc(s):
Allocate a host port       owning=architecture/ports.md                          structured=  4,499  full-KB= 125,334  saved=96%
Work on Compare feature    owning=features/compare.md                            structured=  9,017  full-KB= 125,334  saved=93%
Add a backend endpoint     owning=pikaos-dev-rules.md                            structured= 11,617  full-KB= 125,334  saved=91%
Change the DB schema       owning=pikaos-dev-rules.md,architecture/data-model.md structured= 19,177  full-KB= 125,334  saved=85%
Start a new session        owning=session-handoff.md,playbook.md,lessons.md      structured= 21,103  full-KB= 125,334  saved=83%

Thai vs English, same meaning (real token counts):
  EN   1 | TH   6 | x6.0   hello
  EN   4 | TH  11 | x2.8   Never commit a secret
  EN  10 | TH  44 | x4.4   Read the doc that owns the task, then act
```

**Reading it.** Opening one owning doc instead of the whole knowledge base = **83–96% fewer context
tokens** per task. Picking *which* doc costs only ~5.5k tokens (every frontmatter block combined, 5% of
the KB). Thai is ×2.8–6 the English token count for the same meaning — the reason doc prose is English.

**Caveats (honest).** `cl100k_base` is OpenAI's tokenizer; Claude's differs slightly but the ratios
hold. `full-KB` is an upper bound (a real agent might read fewer than all 42 files) — the structural
point stands: open **1 owning doc, not 42**.

---

## 2. Won't drift — guards demonstrated

The anti-drift claim is backed by mechanisms that are **real files in every scaffolded project**, plus a
linter that **fails the build** on drift. Canonical locations (under `[Name]-Docs/docs/`):

- `process/session-handoff.md` — resume point per session
- `process/lessons.md` — decisions + traps hit for real (remembers mistakes)
- `process/ai-runbooks.md` — R1–R8 recurring-task procedures
- `architecture/ports.md` · `architecture/versions.md` — SSOT registries (values can't diverge)

**Proof the guard bites** — `docs-lint.py` run, a broken link injected, then removed (verbatim, paths
shortened):

```text
########## 1) clean run ##########
docs-lint OK — 42 docs, frontmatter + links + anchors + related all valid.

########## 2) inject a broken link, re-run ##########
docs-lint FAILED:

  - PiKaOs-docs/docs/_evidence_tmp.md: broken link → ./this-file-does-not-exist.md

1 problem(s) in 43 docs.
EXIT=1

########## 3) remove temp, confirm green again ##########
docs-lint OK — 42 docs, frontmatter + links + anchors + related all valid.
EXIT=0
```

A broken internal link → **exit 1** (CI red). Drift cannot be merged silently; the docs and their
`related:` graph stay true to the code as the project grows. The same check runs in CI, so this holds on
every push, not just locally.

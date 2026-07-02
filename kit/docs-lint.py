#!/usr/bin/env python3
# docs-lint.py — the reference validator the scaffolder installs as `scripts/docs-lint.py`
# (new-project-scaffold.md rule 8). Copy it into a scaffolded project's docs repo and wire it
# into CI. It has NO third-party dependencies (Python 3.8+ stdlib only) and its output is UTF-8
# safe, so it runs the same on Linux/macOS/Windows CI.
#
# What it enforces on a `[Name]-Docs/` repo (run it with that repo, or its `docs/`, as the root):
#   1. Frontmatter — every KNOWLEDGE file under `docs/` opens with a YAML block carrying the
#      canonical fields (title · type · status · keywords · related · summary · updated), and
#      `type` / `status` use the allowed vocabulary. The root entry files (CLAUDE.md, AGENTS.md),
#      the GitHub README.md overviews and llms.txt are EXEMPT by their own conventions.
#   2. Balanced frontmatter — a file that opens with `---` also closes it.
#   3. Internal links — every relative Markdown link `](path)` resolves to a file that exists
#      (external http(s)/mailto links are not this tool's job; check them with a link checker).
#   4. Anchors — a `...#anchor` link points at a heading that actually exists in the target file.
#   5. `related:` graph — every path in a file's `related:` list resolves to an existing file.
#   6. Hygiene guards (anti-bloat) — the docs an agent re-reads every session must not silently grow
#      by append-only accretion: `process/session-handoff.md` stays under a line ceiling and stacks no
#      more than a couple of end-state blocks (fail); an oversized curated doc warns (split it). Agent
#      memory files are guarded too when $PROJECT_MEMORY_DIR is set (local-only; CI skips it). See the
#      constants block below to tune the limits per project.
#
# Exit code is 0 when clean, 1 when any problem is found — so a broken link, missing/invalid
# frontmatter, or a bloated read-every-session doc turns the build red instead of letting the docs
# quietly drift from the code. Non-blocking hygiene nudges print as warnings without failing.
#
# Usage:  python3 scripts/docs-lint.py [ROOT]      # ROOT defaults to the current directory

import os
import re
import sys
import io
import unicodedata

# --- canonical frontmatter vocabulary (keep in sync with templates/frontmatter.md) ----------
REQUIRED_KEYS = ["title", "type", "status", "keywords", "related", "summary", "updated"]
VALID_TYPES = {
    "rule", "reference", "architecture", "feature", "process",
    "index", "prompt", "template", "glossary",
}
VALID_STATUS = {"active", "design", "built", "draft", "deprecated"}

# Files that are markdown but carry NO frontmatter by their own spec/convention.
EXEMPT_BASENAMES = {"CLAUDE.md", "AGENTS.md", "README.md"}

# --- docs hygiene guards (anti-bloat) — tune per project ------------------------------------
# The docs an agent re-reads EVERY session (the status handoff, hot docs, memories) decay by
# append-only accretion: each session stacks another block and nothing trims, until the file that
# should orient a new session in 30s is thousands of lines that cost more and orient less. Link/
# frontmatter checks don't catch it (the file is valid, just bloated), so guard size + history.
# When a guard trips, the fix is to TRIM / SPLIT / move to git history — never raise the limit.
SESSION_HANDOFF_SUFFIX = os.path.join("process", "session-handoff.md")
MAX_SESSION_HANDOFF_LINES = 350          # one latest state block + prose; older logs → git history
END_STATE_MARKER = "SESSION-END STATE"   # your session-end block marker
MAX_END_STATE_BLOCKS = 2                  # latest + at most one prior; no stacked history
CURATED_DOC_WARN_LINES = 600             # a doc this big is usually two concepts → warn, don't fail
# Agent-memory guards are agent-specific and usually live OUTSIDE the repo, so they run only when
# $PROJECT_MEMORY_DIR points at an existing dir (local pre-commit / a docs-check skill, not CI).
MEMORY_DIR_ENV = "PROJECT_MEMORY_DIR"
MEMORY_INDEX_NAME = "MEMORY.md"
MAX_MEMORY_FILE_LINES = 200              # a memory is "one fact"; a 500-line memory is stale accretion
MAX_MEMORY_INDEX_LINES = 120            # it's an index (one line per memory), never memory bodies

LINK_RE = re.compile(r"\]\(([^)]+)\)")          # the target inside ](...)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def slugify(heading: str) -> str:
    """GitHub-flavoured heading → anchor slug. Lowercase; drop punctuation & symbols (incl.
    emoji) but keep `-`/`_` and letters/marks/digits of EVERY script (so Thai vowel marks and
    other non-Latin text survive, matching GitHub); then each whitespace char → one hyphen (a
    removed `&`/em-dash leaves two spaces → `--`, exactly as GitHub renders it)."""
    out = []
    for ch in heading.strip().lower():
        if ch in "-_":
            out.append(ch)
        elif unicodedata.category(ch)[0] in ("P", "S"):
            continue                            # punctuation / symbol / emoji → dropped
        else:
            out.append(ch)
    return re.sub(r"\s", "-", "".join(out))


def split_frontmatter(text: str):
    """Return (frontmatter_dict_or_None, had_open_marker, closed_ok, body_offset_lines)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, False, True, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return parse_frontmatter(lines[1:i]), True, True, i + 1
    return None, True, False, 0                 # opened but never closed


def parse_frontmatter(fm_lines):
    """A deliberately small YAML-ish parser for the flat frontmatter schema this kit uses:
    `key: value`, `key: [a, b]` inline lists, and `key: >`/`|` folded/literal block scalars."""
    data = {}
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-"):       # block scalar: consume the indented lines
            block = []
            i += 1
            while i < len(fm_lines) and (fm_lines[i].startswith((" ", "\t")) or not fm_lines[i].strip()):
                block.append(fm_lines[i].strip())
                i += 1
            data[key] = " ".join(b for b in block if b).strip()
            continue
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [x.strip() for x in inner.split(",") if x.strip()] if inner else []
        else:
            data[key] = val
        i += 1
    return data


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code so link extraction ignores literal examples."""
    out, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(out)


def collect_anchors(path: str) -> set:
    anchors = set()
    try:
        with io.open(path, encoding="utf-8") as fh:
            in_fence = False
            for line in fh:
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                m = HEADING_RE.match(line)
                if m:
                    anchors.add(slugify(m.group(2)))
    except OSError:
        pass
    return anchors


def is_under_docs(path: str) -> bool:
    parts = os.path.normpath(path).split(os.sep)
    return "docs" in parts


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    problems = []
    warnings = []
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for name in filenames:
            if name.endswith(".md"):
                md_files.append(os.path.join(dirpath, name))

    for path in sorted(md_files):
        try:
            with io.open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            problems.append(f"{path}: cannot read ({exc})")
            continue

        fm, had_open, closed_ok, _ = split_frontmatter(text)
        base = os.path.basename(path)

        # (1)(2) frontmatter — required for knowledge files under docs/. The GitHub overview
        # README.md and the root CLAUDE.md/AGENTS.md are exempt, but `docs/README.md` is the
        # docs INDEX (type: index) and DOES need frontmatter, so don't exempt that one.
        parent = os.path.basename(os.path.dirname(path))
        is_docs_index = base == "README.md" and parent == "docs"
        exempt = base in EXEMPT_BASENAMES and not is_docs_index
        needs_fm = is_under_docs(path) and not exempt
        if had_open and not closed_ok:
            problems.append(f"{path}: frontmatter opened with '---' but never closed")
        elif needs_fm:
            if fm is None:
                problems.append(f"{path}: missing frontmatter (needs {', '.join(REQUIRED_KEYS)})")
            else:
                for key in REQUIRED_KEYS:
                    if key not in fm:
                        problems.append(f"{path}: frontmatter missing key '{key}'")
                if fm.get("type") and fm["type"] not in VALID_TYPES:
                    problems.append(f"{path}: invalid type '{fm['type']}' (allowed: {sorted(VALID_TYPES)})")
                if fm.get("status") and fm["status"] not in VALID_STATUS:
                    problems.append(f"{path}: invalid status '{fm['status']}' (allowed: {sorted(VALID_STATUS)})")

        base_dir = os.path.dirname(path)

        # (5) related: graph resolves
        if fm and isinstance(fm.get("related"), list):
            for rel in fm["related"]:
                target = rel.split("#", 1)[0]
                if not target or target.startswith(("http://", "https://")):
                    continue
                if not os.path.exists(os.path.join(base_dir, target)):
                    problems.append(f"{path}: related: entry does not resolve → {rel}")

        # (3)(4) internal links + anchors
        for target in LINK_RE.findall(strip_code(text)):
            target = target.strip().split(" ", 1)[0]
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            file_part, _, anchor = target.partition("#")
            if not file_part:                    # same-file anchor
                if anchor and anchor not in collect_anchors(path):
                    problems.append(f"{path}: anchor not found → #{anchor}")
                continue
            dest = os.path.join(base_dir, file_part)
            if not os.path.exists(dest):
                problems.append(f"{path}: broken link → {target}")
            elif anchor and dest.endswith(".md") and anchor not in collect_anchors(dest):
                problems.append(f"{path}: anchor not found in {file_part} → #{anchor}")

        # (6) docs hygiene guards (anti-bloat) — see the constants block up top
        line_count = text.count("\n") + 1
        norm = os.path.normpath(path)
        if norm.endswith(SESSION_HANDOFF_SUFFIX):
            if line_count > MAX_SESSION_HANDOFF_LINES:
                problems.append(
                    f"{path}: session-handoff is {line_count} lines (> {MAX_SESSION_HANDOFF_LINES}) "
                    f"— trim to the latest state; older logs live in git history, don't stack them here")
            end_blocks = text.count(END_STATE_MARKER)
            if end_blocks > MAX_END_STATE_BLOCKS:
                problems.append(
                    f"{path}: {end_blocks} '{END_STATE_MARKER}' blocks (> {MAX_END_STATE_BLOCKS}) "
                    f"— keep the latest + at most one prior; delete older ones (they're in git history)")
        elif needs_fm and line_count > CURATED_DOC_WARN_LINES:
            warnings.append(
                f"{path}: {line_count} lines (> {CURATED_DOC_WARN_LINES}) — likely two concepts; "
                f"consider splitting (1 file = 1 concept). Trim/split — don't raise the limit.")

    # (6b) agent-memory guards — path-gated (memory usually lives outside the repo, so CI skips it)
    mem_dir = os.environ.get(MEMORY_DIR_ENV)
    if mem_dir and os.path.isdir(mem_dir):
        for dirpath, dirnames, filenames in os.walk(mem_dir):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
            for name in sorted(filenames):
                if not name.endswith(".md"):
                    continue
                mpath = os.path.join(dirpath, name)
                try:
                    with io.open(mpath, encoding="utf-8") as fh:
                        n = fh.read().count("\n") + 1
                except OSError:
                    continue
                if name == MEMORY_INDEX_NAME and n > MAX_MEMORY_INDEX_LINES:
                    problems.append(
                        f"{mpath}: memory index is {n} lines (> {MAX_MEMORY_INDEX_LINES}) "
                        f"— it's an index (one line per memory), never memory bodies")
                elif name != MEMORY_INDEX_NAME and n > MAX_MEMORY_FILE_LINES:
                    problems.append(
                        f"{mpath}: memory is {n} lines (> {MAX_MEMORY_FILE_LINES}) "
                        f"— a memory is one fact; split or trim, don't grow it")

    # UTF-8-safe output regardless of the CI locale
    out = sys.stdout
    try:
        out.reconfigure(encoding="utf-8")        # Python 3.7+
    except (AttributeError, ValueError):
        pass

    total = len(md_files)
    if warnings:
        print("docs-lint warnings (non-blocking):\n", file=out)
        for w in warnings:
            print(f"  ! {w}", file=out)
        print("", file=out)
    if problems:
        print("docs-lint FAILED:\n", file=out)
        for p in problems:
            print(f"  - {p}", file=out)
        print(f"\n{len(problems)} problem(s) in {total} docs.", file=out)
        return 1
    print(f"docs-lint OK — {total} docs, frontmatter + links + anchors + related + hygiene all valid.", file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

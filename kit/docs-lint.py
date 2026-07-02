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
#
# Exit code is 0 when clean, 1 when any problem is found — so a broken link or missing/invalid
# frontmatter turns the build red instead of letting the docs quietly drift from the code.
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

    # UTF-8-safe output regardless of the CI locale
    out = sys.stdout
    try:
        out.reconfigure(encoding="utf-8")        # Python 3.7+
    except (AttributeError, ValueError):
        pass

    total = len(md_files)
    if problems:
        print("docs-lint FAILED:\n", file=out)
        for p in problems:
            print(f"  - {p}", file=out)
        print(f"\n{len(problems)} problem(s) in {total} docs.", file=out)
        return 1
    print(f"docs-lint OK — {total} docs, frontmatter + links + anchors + related all valid.", file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

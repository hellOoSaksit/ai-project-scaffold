#!/usr/bin/env bash
# docs-lint: automated test suite for this documentation-only project.
#
# Validates that:
#   1. all required community/health docs are present,
#   2. any Markdown file that opens with YAML frontmatter also closes it, and
#   3. every relative (in-repo) Markdown link resolves to a file that exists —
#      a broken internal link fails the build (external http(s) links are checked
#      separately, and advisorily, by the lychee step in the CI workflow).
#
# Run locally with:  bash scripts/docs-lint.sh
set -euo pipefail

fail=0

required_docs=(
  README.md
  LICENSE
  CHANGELOG.md
  .github/CONTRIBUTING.md
  .github/SECURITY.md
  .github/CODE_OF_CONDUCT.md
)

echo "== Checking required documentation files =="
for f in "${required_docs[@]}"; do
  if [[ -f "$f" ]]; then
    echo "OK:      $f"
  else
    echo "MISSING: $f"
    fail=1
  fi
done

echo
echo "== Checking Markdown frontmatter is balanced =="
while IFS= read -r -d '' f; do
  first_line="$(head -n 1 "$f" || true)"
  if [[ "$first_line" == "---" ]]; then
    markers="$(grep -c '^---$' "$f" || true)"
    if [[ "${markers:-0}" -lt 2 ]]; then
      echo "BAD FRONTMATTER (unclosed): $f"
      fail=1
    else
      echo "OK:      $f (frontmatter)"
    fi
  fi
done < <(find . -type f -name '*.md' -not -path './.git/*' -print0)

echo
echo "== Checking internal Markdown links resolve =="
links_ok=1
while IFS= read -r -d '' f; do
  dir="$(dirname "$f")"
  # Extract every inline-link target: the `...` inside `](...)`. Strip fenced code
  # blocks and inline `code` spans first — a `[name](path)` inside backticks is a
  # literal example (e.g. the llms.txt format), not a real link to resolve.
  targets="$(awk '/^```/{fence=!fence;next} !fence{gsub(/`[^`]*`/,"");print}' "$f" \
             | grep -oE '\]\([^)]+\)' | sed -E 's/^\]\(//; s/\)$//' || true)"
  [[ -z "$targets" ]] && continue
  while IFS= read -r target; do
    [[ -z "$target" ]] && continue
    target="${target%% *}"                 # drop an optional "title" after the path
    case "$target" in
      http://*|https://*|mailto:*|tel:*|'#'*) continue ;;   # external / anchor-only → not our job
    esac
    path="${target%%#*}"                    # strip #anchor, keep the file path
    [[ -z "$path" ]] && continue
    if [[ ! -e "$dir/$path" ]]; then
      echo "BROKEN LINK: $f → $target"
      fail=1
      links_ok=0
    fi
  done <<< "$targets"
done < <(find . -type f -name '*.md' -not -path './.git/*' -print0)
[[ "$links_ok" -eq 1 ]] && echo "OK:      all internal Markdown links resolve"

echo
if [[ "$fail" -ne 0 ]]; then
  echo "docs-lint: FAILED"
  exit 1
fi
echo "docs-lint: PASSED"

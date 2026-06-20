#!/usr/bin/env bash
# docs-lint: automated test suite for this documentation-only project.
#
# Validates that:
#   1. all required community/health docs are present, and
#   2. any Markdown file that opens with YAML frontmatter also closes it.
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
if [[ "$fail" -ne 0 ]]; then
  echo "docs-lint: FAILED"
  exit 1
fi
echo "docs-lint: PASSED"

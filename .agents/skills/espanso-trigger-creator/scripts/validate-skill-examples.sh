#!/usr/bin/env sh
set -eu

SKILL_DIR="$(
  unset CDPATH
  cd -- "$(dirname -- "$0")/.." && pwd
)"

# Check if expected files exist
while IFS= read -r f; do
  [ -n "$f" ] || continue
  if [ ! -f "$f" ]; then
    echo "FAIL missing file: $f"
    exit 1
  fi
done <<EOF
$SKILL_DIR/SKILL.md
$SKILL_DIR/references/basics.md
$SKILL_DIR/references/forms.md
$SKILL_DIR/references/patterns-and-pitfalls.md
$SKILL_DIR/references/regex-and-vars.md
$SKILL_DIR/references/shell-and-automation.md
$SKILL_DIR/references/example-trigger.yml
$SKILL_DIR/scripts/scaffold_espanso_trigger.py
$SKILL_DIR/scripts/lint_espanso_yaml.py
EOF

# Run scaffold checks
python3 "$SKILL_DIR/scripts/scaffold_espanso_trigger.py" \
  --type form \
  --trigger :test_form \
  --fields name,desc >/dev/null

# Run lint checks
python3 "$SKILL_DIR/scripts/lint_espanso_yaml.py" \
  "$SKILL_DIR/references/example-trigger.yml" >/dev/null

echo "OK skill examples validated"

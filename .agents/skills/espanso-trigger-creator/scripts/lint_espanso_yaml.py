#!/usr/bin/env python3
"""Lint Espanso YAML for standard trigger constraints and anti-patterns."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import yaml
import jsonschema

# Regex to match placeholders like {{variable}} in the replacement template
PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z0-9_\.]+)\}\}")

# Regex to match form fields like [[field]] in a form layout
FORM_FIELD_RE = re.compile(r"\[\[([a-zA-Z0-9_-]+)\]\]")

# Warning patterns for clipboard status leakage
WARN_CLIPBOARD_STATUS = (
    "Copied to clipboard",
    "copied result to clipboard",
    "copied to clipboard",
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "..", "resources", "match.schema.json")


def validate_against_schema(data: dict) -> list[str]:
    """Validate data against the official Espanso match schema.

    Returns a list of error strings.
    """
    errors: list[str] = []
    if not os.path.exists(SCHEMA_PATH):
        errors.append(f"Espanso match schema file not found at {SCHEMA_PATH}")
        return errors

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as exc:
        errors.append(f"Failed to parse Espanso match schema JSON: {exc}")
        return errors

    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.path)
        path_str = f" at {path}" if path else ""
        errors.append(f"Schema violation{path_str}: {error.message}")

    return errors


def check_match_entry(match_idx: int, entry: dict) -> tuple[list[str], list[str]]:
    """Validate a single match entry in an Espanso file.

    Returns:
        (errors, warnings) lists.
    """
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Trigger / Triggers vs Regex Exclusivity
    has_trigger = "trigger" in entry or "triggers" in entry
    has_regex = "regex" in entry

    if not has_trigger and not has_regex:
        errors.append(
            f"Match #{match_idx} is missing trigger/triggers or regex key."
        )
        return errors, warnings

    if has_trigger and has_regex:
        errors.append(
            f"Match #{match_idx} has both trigger and regex keys. They are mutually exclusive."
        )

    # 2. Check variables and placeholders
    replace_val = entry.get("replace", "")
    placeholders = set()
    if isinstance(replace_val, str):
        placeholders = set(PLACEHOLDER_RE.findall(replace_val))

    # Add variables defined in vars
    defined_vars = set()
    vars_list = entry.get("vars", [])
    if isinstance(vars_list, list):
        for var_idx, var_item in enumerate(vars_list):
            if not isinstance(var_item, dict):
                errors.append(
                    f"Match #{match_idx} vars index {var_idx} is not a dictionary."
                )
                continue
            name = var_item.get("name")
            if not name:
                errors.append(
                    f"Match #{match_idx} vars index {var_idx} is missing 'name' attribute."
                )
                continue
            if name in defined_vars:
                errors.append(
                    f"Match #{match_idx} defines duplicate variable name '{name}'."
                )
            defined_vars.add(name)

            # Check shell command absolute paths
            var_type = var_item.get("type")
            if var_type == "shell":
                cmd = var_item.get("params", {}).get("cmd", "")
                if cmd:
                    # Detect absolute paths (Unix/Windows format)
                    if re.match(r"^(/|[a-zA-Z]:\\)", cmd):
                        warnings.append(
                            f"Match #{match_idx} shell variable '{name}' uses hardcoded absolute path in cmd. Hint: Use %CONFIG% instead."
                        )

    # Add named capture groups from regex
    regex_val = entry.get("regex", "")
    if regex_val and isinstance(regex_val, str):
        # Look for named groups (?P<name>...)
        regex_captures = set(re.findall(r"\(\?P<([a-zA-Z0-9_]+)>", regex_val))
        defined_vars.update(regex_captures)

    # Check that placeholders are defined (except standard built-ins if they don't need vars)
    # Standard Espanso built-in vars include 'clipboard' if it's evaluated natively (but usually requires clipboard var definition).
    # We warn/error on undefined placeholders. Let's make it an error if it's a completely unresolved placeholder.
    # Note: simple forms with [[field]] are handled below.
    unresolved = placeholders - defined_vars
    # Ignore standard system variables if the user hasn't overridden them
    # Espanso standard vars sometimes are implicitly defined (e.g. date if not defined, though usually declared).
    # To be safe, let's treat any unresolved placeholder as an error unless it's a known global built-in.
    for placeholder in unresolved:
        errors.append(
            f"Match #{match_idx} references placeholder '{{{{{placeholder}}}}}' in replace, but it is not defined in vars or regex captures."
        )

    # 3. Form layouts and field mapping
    form_layout = entry.get("form", "")
    form_fields = entry.get("form_fields", {})

    if form_layout and isinstance(form_layout, str):
        # Extract [[field]] placeholders
        layout_fields = set(FORM_FIELD_RE.findall(form_layout))
        
        # Verify all form_fields defined are present in the form layout
        if isinstance(form_fields, dict):
            for field_name, field_cfg in form_fields.items():
                if field_name not in layout_fields:
                    warnings.append(
                        f"Match #{match_idx} defines form field '{field_name}' in form_fields, but it is not in the form layout."
                    )
                if isinstance(field_cfg, dict):
                    field_type = field_cfg.get("type")
                    if field_type is not None:
                        if field_type not in ("choice", "list"):
                            errors.append(
                                f"Match #{match_idx} form field '{field_name}' has invalid type '{field_type}'. "
                                "Espanso only supports 'choice' or 'list' as types. "
                                "For text/multiline fields, omit the 'type' attribute and set 'multiline: true'."
                            )
                        elif "values" not in field_cfg:
                            errors.append(
                                f"Match #{match_idx} form field '{field_name}' is of type '{field_type}' but is missing required 'values' list."
                            )
                    
                    if "multiline" in field_cfg and not isinstance(field_cfg["multiline"], bool):
                        errors.append(
                            f"Match #{match_idx} form field '{field_name}' has non-boolean 'multiline' value."
                        )
                else:
                    errors.append(
                        f"Match #{match_idx} form field '{field_name}' configuration must be a dictionary."
                    )
        else:
            errors.append(
                f"Match #{match_idx} 'form_fields' must be a dictionary."
            )

    # 4. Anti-pattern checks
    if isinstance(replace_val, str):
        for pattern in WARN_CLIPBOARD_STATUS:
            if pattern in replace_val:
                warnings.append(
                    f"Match #{match_idx} replace text contains clipboard status feedback '{pattern}'. Hint: Return the payload directly."
                )

    return errors, warnings


def lint_yaml_content(text: str) -> tuple[list[str], list[str]]:
    """Parse and lint the YAML content.

    Returns:
        (errors, warnings) lists.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        errors.append(f"YAML parsing error: {exc}")
        return errors, warnings

    if not isinstance(data, dict):
        errors.append("Root of Espanso file must be a dictionary/mapping.")
        return errors, warnings

    # Run JSON Schema Validation first
    schema_errors = validate_against_schema(data)
    errors.extend(schema_errors)

    matches = data.get("matches")
    if matches is None:
        errors.append("Missing top-level 'matches' key.")
        return errors, warnings

    if not isinstance(matches, list):
        errors.append("Top-level 'matches' key must be a list.")
        return errors, warnings

    for idx, entry in enumerate(matches, start=1):
        if not isinstance(entry, dict):
            errors.append(f"Match #{idx} is not a dictionary.")
            continue
        e, w = check_match_entry(idx, entry)
        errors.extend(e)
        warnings.extend(w)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint standard Espanso match files."
    )
    parser.add_argument("paths", nargs="+", help="YAML files or directories")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures (returns non-zero exit code on warnings)",
    )
    args = parser.parse_args()

    # Discover files
    files: list[pathlib.Path] = []
    for raw in args.paths:
        p = pathlib.Path(raw)
        if p.is_file() and p.suffix in (".yml", ".yaml"):
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.yml")))
            files.extend(sorted(p.rglob("*.yaml")))

    if not files:
        print("error: No Espanso YAML files found to lint.")
        return 1

    failed = False
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"error: Failed to read {path}: {exc}")
            failed = True
            continue

        errors, warnings = lint_yaml_content(text)

        if not errors and not warnings:
            print(f"OK   {path}")
            continue

        if errors:
            failed = True
            print(f"FAIL {path}")
            for item in errors:
                print(f"  - error: {item}")

        if warnings:
            print(f"WARN {path}")
            for item in warnings:
                print(f"  - warning: {item}")
            if args.strict:
                failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

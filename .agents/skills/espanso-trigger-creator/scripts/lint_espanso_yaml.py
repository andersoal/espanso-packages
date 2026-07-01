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

# Regex to match named capture groups like (?P<name>...) in a trigger regex
REGEX_NAMED_GROUP_RE = re.compile(r"\(\?P<([a-zA-Z0-9_]+)>")

# Regex to detect absolute paths (Unix "/..." or Windows "C:\...") in shell cmds
ABSOLUTE_PATH_RE = re.compile(r"^(/|[a-zA-Z]:\\)")

# Warning patterns for clipboard status leakage
WARN_CLIPBOARD_STATUS = (
    "Copied to clipboard",
    "copied result to clipboard",
    "copied to clipboard",
)

# The only field types Espanso accepts in form_fields; text/multiline fields
# must omit 'type' entirely.
VALID_FORM_FIELD_TYPES = ("choice", "list")

# File extensions recognized as Espanso YAML files
YAML_SUFFIXES = (".yml", ".yaml")

# Match entries are reported 1-indexed to mirror how users count them in YAML
FIRST_MATCH_INDEX = 1

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "..", "resources", "match.schema.json")


def _load_match_schema() -> tuple[dict | None, str | None]:
    """Load the official Espanso match schema.

    Returns:
        (schema, error_message); exactly one of the two is None.
    """
    if not os.path.exists(SCHEMA_PATH):
        return None, f"Espanso match schema file not found at {SCHEMA_PATH}"

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as exc:
        return None, f"Failed to parse Espanso match schema JSON: {exc}"


def validate_against_schema(data: dict) -> list[str]:
    """Validate data against the official Espanso match schema.

    Returns a list of error strings.
    """
    schema, load_error = _load_match_schema()
    if load_error:
        return [load_error]

    errors: list[str] = []
    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.path)
        path_str = f" at {path}" if path else ""
        errors.append(f"Schema violation{path_str}: {error.message}")

    return errors


class MatchEntryChecker:
    """Runs all lint checks for a single match entry.

    Collects errors and warnings, prefixing every message with the
    1-indexed match number so users can locate the entry in the file.
    """

    def __init__(self, match_idx: int, entry: dict) -> None:
        self.entry = entry
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self._message_prefix = f"Match #{match_idx}"

    def run(self) -> tuple[list[str], list[str]]:
        """Execute every check and return (errors, warnings)."""
        if self._check_trigger_keys():
            defined_vars = self._collect_defined_vars()
            self._check_placeholders(defined_vars)
            self._check_form_layout()
            self._check_clipboard_status_leak()
        return self.errors, self.warnings

    def _error(self, message: str) -> None:
        self.errors.append(f"{self._message_prefix} {message}")

    def _warn(self, message: str) -> None:
        self.warnings.append(f"{self._message_prefix} {message}")

    def _replace_text(self) -> str:
        """Return the replace template, or "" when absent/non-string."""
        replace_val = self.entry.get("replace", "")
        return replace_val if isinstance(replace_val, str) else ""

    def _check_trigger_keys(self) -> bool:
        """Enforce trigger/triggers vs regex exclusivity.

        Returns False when the entry has neither key, in which case the
        remaining checks are meaningless and should be skipped.
        """
        has_trigger = "trigger" in self.entry or "triggers" in self.entry
        has_regex = "regex" in self.entry

        if not has_trigger and not has_regex:
            self._error("is missing trigger/triggers or regex key.")
            return False

        if has_trigger and has_regex:
            self._error(
                "has both trigger and regex keys. They are mutually exclusive."
            )
        return True

    def _collect_defined_vars(self) -> set[str]:
        """Gather variable names available to {{placeholders}} in replace.

        Variables come from the 'vars' list and from named capture groups
        in the 'regex' trigger. Malformed var entries are reported as they
        are encountered.
        """
        defined_vars: set[str] = set()
        vars_list = self.entry.get("vars", [])
        if isinstance(vars_list, list):
            for var_idx, var_item in enumerate(vars_list):
                name = self._validate_var_item(var_idx, var_item, defined_vars)
                if name:
                    defined_vars.add(name)
        defined_vars.update(self._regex_capture_groups())
        return defined_vars

    def _validate_var_item(
        self, var_idx: int, var_item: object, already_defined: set[str]
    ) -> str | None:
        """Validate one 'vars' entry and return its name, or None if unusable."""
        if not isinstance(var_item, dict):
            self._error(f"vars index {var_idx} is not a dictionary.")
            return None

        name = var_item.get("name")
        if not name:
            self._error(f"vars index {var_idx} is missing 'name' attribute.")
            return None

        if name in already_defined:
            self._error(f"defines duplicate variable name '{name}'.")

        if var_item.get("type") == "shell":
            self._check_shell_command(name, var_item)
        return name

    def _check_shell_command(self, name: str, var_item: dict) -> None:
        """Warn when a shell variable hardcodes an absolute path in cmd."""
        cmd = var_item.get("params", {}).get("cmd", "")
        if cmd and ABSOLUTE_PATH_RE.match(cmd):
            self._warn(
                f"shell variable '{name}' uses hardcoded absolute path in cmd. Hint: Use %CONFIG% instead."
            )

    def _regex_capture_groups(self) -> set[str]:
        """Return the named capture groups defined by the 'regex' trigger."""
        regex_val = self.entry.get("regex", "")
        if regex_val and isinstance(regex_val, str):
            return set(REGEX_NAMED_GROUP_RE.findall(regex_val))
        return set()

    def _check_placeholders(self, defined_vars: set[str]) -> None:
        """Report {{placeholders}} in replace that no variable resolves."""
        placeholders = set(PLACEHOLDER_RE.findall(self._replace_text()))
        for placeholder in placeholders - defined_vars:
            self._error(
                f"references placeholder '{{{{{placeholder}}}}}' in replace, but it is not defined in vars or regex captures."
            )

    def _check_form_layout(self) -> None:
        """Cross-check form_fields definitions against the form layout."""
        form_layout = self.entry.get("form", "")
        if not form_layout or not isinstance(form_layout, str):
            return

        form_fields = self.entry.get("form_fields", {})
        if not isinstance(form_fields, dict):
            self._error("'form_fields' must be a dictionary.")
            return

        layout_fields = set(FORM_FIELD_RE.findall(form_layout))
        for field_name, field_cfg in form_fields.items():
            self._check_form_field(field_name, field_cfg, layout_fields)

    def _check_form_field(
        self, field_name: str, field_cfg: object, layout_fields: set[str]
    ) -> None:
        """Validate one form_fields entry against the layout and type rules."""
        if field_name not in layout_fields:
            self._warn(
                f"defines form field '{field_name}' in form_fields, but it is not in the form layout."
            )

        if not isinstance(field_cfg, dict):
            self._error(
                f"form field '{field_name}' configuration must be a dictionary."
            )
            return

        self._check_form_field_type(field_name, field_cfg)
        if "multiline" in field_cfg and not isinstance(field_cfg["multiline"], bool):
            self._error(
                f"form field '{field_name}' has non-boolean 'multiline' value."
            )

    def _check_form_field_type(self, field_name: str, field_cfg: dict) -> None:
        """Ensure an explicit field type is one Espanso supports."""
        field_type = field_cfg.get("type")
        if field_type is None:
            return

        if field_type not in VALID_FORM_FIELD_TYPES:
            self._error(
                f"form field '{field_name}' has invalid type '{field_type}'. "
                "Espanso only supports 'choice' or 'list' as types. "
                "For text/multiline fields, omit the 'type' attribute and set 'multiline: true'."
            )
        elif "values" not in field_cfg:
            self._error(
                f"form field '{field_name}' is of type '{field_type}' but is missing required 'values' list."
            )

    def _check_clipboard_status_leak(self) -> None:
        """Warn when replace text echoes clipboard status instead of payload."""
        replace_text = self._replace_text()
        for status_phrase in WARN_CLIPBOARD_STATUS:
            if status_phrase in replace_text:
                self._warn(
                    f"replace text contains clipboard status feedback '{status_phrase}'. Hint: Return the payload directly."
                )


def check_match_entry(match_idx: int, entry: dict) -> tuple[list[str], list[str]]:
    """Validate a single match entry in an Espanso file.

    Returns:
        (errors, warnings) lists.
    """
    return MatchEntryChecker(match_idx, entry).run()


def _parse_yaml_root(text: str) -> tuple[dict | None, list[str]]:
    """Parse YAML text and require a mapping at the root.

    Returns:
        (data, errors); data is None when parsing or shape validation fails.
    """
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return None, [f"YAML parsing error: {exc}"]

    if not isinstance(data, dict):
        return None, ["Root of Espanso file must be a dictionary/mapping."]

    return data, []


def _check_matches(matches_value: object) -> tuple[list[str], list[str]]:
    """Validate the top-level 'matches' value and each of its entries."""
    errors: list[str] = []
    warnings: list[str] = []

    if matches_value is None:
        return ["Missing top-level 'matches' key."], warnings
    if not isinstance(matches_value, list):
        return ["Top-level 'matches' key must be a list."], warnings

    for idx, entry in enumerate(matches_value, start=FIRST_MATCH_INDEX):
        if not isinstance(entry, dict):
            errors.append(f"Match #{idx} is not a dictionary.")
            continue
        entry_errors, entry_warnings = check_match_entry(idx, entry)
        errors.extend(entry_errors)
        warnings.extend(entry_warnings)

    return errors, warnings


def lint_yaml_content(text: str) -> tuple[list[str], list[str]]:
    """Parse and lint the YAML content.

    Returns:
        (errors, warnings) lists.
    """
    data, parse_errors = _parse_yaml_root(text)
    if data is None:
        return parse_errors, []

    # Run JSON Schema Validation first
    errors = validate_against_schema(data)

    match_errors, warnings = _check_matches(data.get("matches"))
    errors.extend(match_errors)
    return errors, warnings


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lint standard Espanso match files."
    )
    parser.add_argument("paths", nargs="+", help="YAML files or directories")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures (returns non-zero exit code on warnings)",
    )
    return parser.parse_args()


def _discover_yaml_files(raw_paths: list[str]) -> list[pathlib.Path]:
    """Expand file/directory arguments into the list of YAML files to lint."""
    files: list[pathlib.Path] = []
    for raw in raw_paths:
        path = pathlib.Path(raw)
        if path.is_file() and path.suffix in YAML_SUFFIXES:
            files.append(path)
        elif path.is_dir():
            for suffix in YAML_SUFFIXES:
                files.extend(sorted(path.rglob(f"*{suffix}")))
    return files


def _report_file_results(
    path: pathlib.Path, errors: list[str], warnings: list[str], strict: bool
) -> bool:
    """Print the lint results for one file. Returns True when it failed."""
    if not errors and not warnings:
        print(f"OK   {path}")
        return False

    if errors:
        print(f"FAIL {path}")
        for item in errors:
            print(f"  - error: {item}")

    if warnings:
        print(f"WARN {path}")
        for item in warnings:
            print(f"  - warning: {item}")

    return bool(errors) or (strict and bool(warnings))


def _lint_file(path: pathlib.Path, strict: bool) -> bool:
    """Lint a single file and report results. Returns True when it failed."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"error: Failed to read {path}: {exc}")
        return True

    errors, warnings = lint_yaml_content(text)
    return _report_file_results(path, errors, warnings, strict)


def main() -> int:
    args = _parse_args()

    files = _discover_yaml_files(args.paths)
    if not files:
        print("error: No Espanso YAML files found to lint.")
        return EXIT_FAILURE

    failed = False
    for path in files:
        file_failed = _lint_file(path, strict=args.strict)
        failed = failed or file_failed

    return EXIT_FAILURE if failed else EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Generate standard scaffolds for standard Espanso triggers."""

from __future__ import annotations

import argparse
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate standard Espanso trigger YAML scaffolds."
    )
    parser.add_argument(
        "--type",
        choices=("simple", "regex", "date", "form", "shell"),
        required=True,
        help="Type of trigger scaffold to generate",
    )
    parser.add_argument(
        "--trigger",
        default="",
        help="Trigger string (e.g. ':sig'). Used for single trigger.",
    )
    parser.add_argument(
        "--triggers",
        default="",
        help="Comma-separated trigger strings (e.g. ':sig,:signature') to generate a YAML array.",
    )
    parser.add_argument(
        "--regex",
        default="",
        help="Regex pattern (e.g. ':greet\\((?P<person>.*)\\)'). Required for 'regex' type.",
    )
    parser.add_argument(
        "--replace",
        default="Hello World",
        help="Replacement text or pattern",
    )
    parser.add_argument(
        "--var-name",
        default="output",
        help="Variable name for date or shell types",
    )
    parser.add_argument(
        "--cmd",
        default="echo 'hello'",
        help="Command to run for shell type",
    )
    parser.add_argument(
        "--fields",
        default="name,topic",
        help="Comma-separated field names for form layout",
    )
    return parser.parse_args()


def _format_trigger_header(args: argparse.Namespace, default_trigger: str) -> str:
    """Format the trigger / triggers line(s) for scaffold output."""
    triggers_val = getattr(args, "triggers", "")
    if triggers_val:
        trigger_list = [t.strip() for t in triggers_val.split(",") if t.strip()]
        formatted = ", ".join(f'"{t}"' for t in trigger_list)
        return f"  - triggers: [{formatted}]"
    trig = getattr(args, "trigger", "") or default_trigger
    return f'  - trigger: "{trig}"'


def generate_scaffold(args: argparse.Namespace) -> str:
    trigger_type = args.type

    if trigger_type == "simple":
        header = _format_trigger_header(args, ":hello")
        return f"""{header}
    replace: "{args.replace}"
"""

    elif trigger_type == "regex":
        reg = args.regex or r":greet\((?P<person>.*)\)"
        rep = args.replace if args.replace != "Hello World" else "Hey {{person}}, welcome!"
        return f"""  - regex: "{reg}"
    replace: "{rep}"
"""

    elif trigger_type == "date":
        header = _format_trigger_header(args, ":today")
        var_name = args.var_name or "date"
        return f"""{header}
    replace: "{{{{{var_name}}}}}"
    vars:
      - name: {var_name}
        type: date
        params:
          format: "%Y-%m-%d"
"""

    elif trigger_type == "form":
        header = _format_trigger_header(args, ":form")
        fields = [f.strip() for f in args.fields.split(",") if f.strip()]
        
        # Build form layout
        layout_lines = []
        for field in fields:
            layout_lines.append(f"    {field.capitalize()}: [[{field}]]")
        layout_str = "\n".join(layout_lines)
        
        # Build form_fields
        fields_lines = []
        for field in fields:
            fields_lines.append(f"      {field}:")
            fields_lines.append(f"        default: \"\"")
        fields_str = "\n".join(fields_lines)

        return f"""{header}
    form: |
{layout_str}
    form_fields:
{fields_str}
"""

    elif trigger_type == "shell":
        header = _format_trigger_header(args, ":shell")
        var_name = args.var_name or "output"
        cmd = args.cmd
        return f"""{header}
    replace: "{{{{{var_name}}}}}"
    vars:
      - name: {var_name}
        type: shell
        params:
          cmd: "{cmd}"
"""

    return ""


def main() -> int:
    args = parse_args()
    
    try:
        scaffold = generate_scaffold(args)
        print("=== Espanso Trigger Scaffold ===")
        print(scaffold)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

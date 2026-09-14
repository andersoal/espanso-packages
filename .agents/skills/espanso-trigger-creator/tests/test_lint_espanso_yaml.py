#!/usr/bin/env python3
"""Unit tests for standard Espanso trigger linter."""

from __future__ import annotations

import unittest
import sys
import os

# Add parent directory to sys.path so we can import scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.lint_espanso_yaml import lint_yaml_content


class TestLintEspansoYaml(unittest.TestCase):
    """Test suite for standard Espanso YAML linter checks."""

    def test_valid_simple_trigger(self):
        content = """
matches:
  - trigger: ":sig"
    replace: "Jane Doe | jane@example.com"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_valid_triggers_flow_array(self):
        content = """
matches:
  - triggers: [":sig", ":signature"]
    replace: "Jane Doe | jane@example.com"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_valid_triggers_block_array(self):
        content = """
matches:
  - triggers:
      - ":email"
      - ":mail"
    replace: "jane@example.com"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_valid_regex_trigger(self):
        content = """
matches:
  - regex: ":greet\\\\((?P<person>.*)\\\\)"
    replace: "Hey {{person}}, welcome!"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_trigger_and_regex(self):
        content = """
matches:
  - replace: "No trigger here!"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertTrue(any("missing trigger/triggers or regex key" in err for err in errors))

    def test_trigger_regex_collision(self):
        content = """
matches:
  - trigger: ":sig"
    regex: ":sig-regex"
    replace: "Collision!"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertTrue(any("both trigger and regex keys" in err for err in errors))

    def test_unresolved_placeholder(self):
        content = """
matches:
  - trigger: ":greet"
    replace: "Hey {{person}}, welcome!"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertTrue(any("references placeholder '{{person}}'" in err for err in errors))

    def test_resolved_placeholder_via_vars(self):
        content = """
matches:
  - trigger: ":now"
    replace: "It's {{time}}"
    vars:
      - name: time
        type: date
        params:
          format: "%H:%M"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_duplicate_variable_name(self):
        content = """
matches:
  - trigger: ":now"
    replace: "It's {{time}}"
    vars:
      - name: time
        type: date
      - name: time
        type: shell
"""
        errors, warnings = lint_yaml_content(content)
        self.assertTrue(any("duplicate variable name 'time'" in err for err in errors))

    def test_form_fields_warnings(self):
        content = """
matches:
  - trigger: ":form"
    form: |
      Name: [[name]]
    form_fields:
      name:
        default: ""
      extra:
        default: ""
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertTrue(any("defines form field 'extra' in form_fields, but it is not in the form layout" in warn for warn in warnings))

    def test_absolute_path_warning(self):
        content = """
matches:
  - trigger: ":run"
    replace: "{{output}}"
    vars:
      - name: output
        type: shell
        params:
          cmd: "/usr/bin/my_script.sh"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertTrue(any("uses hardcoded absolute path in cmd" in warn for warn in warnings))

    def test_clipboard_status_warning(self):
        content = """
matches:
  - trigger: ":copy"
    replace: "Copied to clipboard!"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertTrue(any("clipboard status feedback" in warn for warn in warnings))

    def test_schema_validation_error(self):
        # Test schema error at root
        content = """
invalid_root_key: true
matches:
  - trigger: ":sig"
    replace: "Jane Doe"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertTrue(any("Schema violation" in err for err in errors))

        # Test schema error inside a match (invalid property)
        content = """
matches:
  - trigger: ":sig"
    replace: "Jane Doe"
    invalid_match_key: 123
"""
        errors, warnings = lint_yaml_content(content)
        self.assertTrue(any("Schema violation at matches -> 0: Additional properties are not allowed ('invalid_match_key' was unexpected)" in err for err in errors))

    def test_valid_ergonomic_label(self):
        content = """
matches:
  - trigger: ":sig"
    label: "[Personal] Email Signature (Standard Full Contact Details)"
    replace: "Jane Doe | jane@example.com"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_label_raw_placeholder_warning(self):
        content = """
matches:
  - trigger: ":act"
    label: "[Prompts] [[Persona]]"
    replace: "Act as a persona"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertTrue(any("contains raw variable placeholders" in warn for warn in warnings))

    def test_label_dangling_connector_warning(self):
        content = """
matches:
  - trigger: ":draft"
    label: "[Prompts] Write A First Draft Of"
    replace: "Draft text"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertTrue(any("ends with dangling connector/preposition" in warn for warn in warnings))

    def test_label_lazy_trigger_repeat_warning(self):
        content = """
matches:
  - trigger: ":prmresearch"
    label: "[Prompts] Prmresearch"
    replace: "Research text"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertTrue(any("lazily repeats trigger name" in warn for warn in warnings))

    def test_label_empty_warning(self):
        content = """
matches:
  - trigger: ":sig"
    label: ""
    replace: "Jane Doe"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertTrue(any("label is empty" in warn for warn in warnings))

    def test_resolved_placeholder_via_global_vars(self):
        content = """
global_vars:
  - name: company
    type: echo
    params:
      echo: "Acme Corp"
matches:
  - trigger: ":co"
    replace: "Welcome to {{company}}!"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_escaped_curly_braces_ignored(self):
        content = """
matches:
  - trigger: ":tmpl"
    replace: "Hello \\\\{\\\\{not_a_var\\\\}\\\\}"
"""
        errors, warnings = lint_yaml_content(content)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()

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
        type: text
      extra:
        type: text
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


if __name__ == "__main__":
    unittest.main()

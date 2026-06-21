#!/usr/bin/env python3
"""Unit tests for standard Espanso trigger scaffolder."""

from __future__ import annotations

import unittest
import sys
import os
import argparse

# Add parent directory to sys.path so we can import scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.scaffold_espanso_trigger import generate_scaffold


class TestScaffoldEspansoTrigger(unittest.TestCase):
    """Test suite for standard Espanso scaffolder checks."""

    def test_scaffold_simple(self):
        args = argparse.Namespace(
            type="simple",
            trigger=":hi",
            replace="Hello there",
            regex="",
            var_name="output",
            cmd="echo 'hello'",
            fields="name,topic",
        )
        scaffold = generate_scaffold(args)
        self.assertIn('trigger: ":hi"', scaffold)
        self.assertIn('replace: "Hello there"', scaffold)

    def test_scaffold_regex(self):
        args = argparse.Namespace(
            type="regex",
            trigger="",
            replace="Hey {{person}}, welcome!",
            regex=r":greet\((?P<person>.*)\)",
            var_name="output",
            cmd="echo 'hello'",
            fields="name,topic",
        )
        scaffold = generate_scaffold(args)
        self.assertIn('regex: ":greet\\((?P<person>.*)\\)"', scaffold)
        self.assertIn('replace: "Hey {{person}}, welcome!"', scaffold)

    def test_scaffold_date(self):
        args = argparse.Namespace(
            type="date",
            trigger=":today",
            replace="Hello World",
            regex="",
            var_name="my_date",
            cmd="echo 'hello'",
            fields="name,topic",
        )
        scaffold = generate_scaffold(args)
        self.assertIn('trigger: ":today"', scaffold)
        self.assertIn('replace: "{{my_date}}"', scaffold)
        self.assertIn("type: date", scaffold)
        self.assertIn("format: \"%Y-%m-%d\"", scaffold)

    def test_scaffold_form(self):
        args = argparse.Namespace(
            type="form",
            trigger=":my_form",
            replace="Hello World",
            regex="",
            var_name="output",
            cmd="echo 'hello'",
            fields="first,last",
        )
        scaffold = generate_scaffold(args)
        self.assertIn('trigger: ":my_form"', scaffold)
        self.assertIn("form: |", scaffold)
        self.assertIn("First: [[first]]", scaffold)
        self.assertIn("Last: [[last]]", scaffold)
        self.assertIn("form_fields:", scaffold)
        self.assertIn("first:", scaffold)
        self.assertIn("last:", scaffold)

    def test_scaffold_shell(self):
        args = argparse.Namespace(
            type="shell",
            trigger=":run",
            replace="Hello World",
            regex="",
            var_name="my_cmd",
            cmd="curl ifconfig.me",
            fields="name,topic",
        )
        scaffold = generate_scaffold(args)
        self.assertIn('trigger: ":run"', scaffold)
        self.assertIn('replace: "{{my_cmd}}"', scaffold)
        self.assertIn("type: shell", scaffold)
        self.assertIn('cmd: "curl ifconfig.me"', scaffold)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Audit espanso packages for duplicate, overlapping, and shadowed triggers.

Checks all packages in the repo for:

1. Exact duplicate triggers:
   Duplicates are allowed only when every match sharing the trigger has
   a distinct `label` (espanso then displays an interactive disambiguation
   popup instead of picking one arbitrarily).

2. Prefix shadowing & overlapping without `word: true` (CRITICAL):
   A trigger without `word: true` expands the exact instant its characters
   are typed. Any longer plain trigger or regex trigger starting with this
   sequence is unreachable because the shorter trigger fires first.

3. Overlapping prefixes with `word: true` (WARNING / NOTICE):
   When a trigger has `word: true`, longer triggers sharing the prefix remain
   reachable unless followed by a word separator. These are tracked and can
   be inspected with `--warn-all`.

4. Regex trigger conflicts:
   Detects when plain triggers shadow regex trigger invocation prefixes
   (e.g. `:hooks` shadowing `:hooks(...)`).

Exits non-zero if any duplicate collisions or unhandled shadowing is found.
"""

import argparse
import collections
import glob
import os
import re
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORED_PACKAGES = {"_example-package", "_docs", "_scripts", "_workflows", "_resources"}


class SafeLineLoader(yaml.SafeLoader):
    """YAML loader that records 1-indexed start line numbers for mappings."""

    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        mapping["__line__"] = node.start_mark.line + 1
        return mapping


class MatchEntry:
    def __init__(self, trigger, match_type, pkg, file_rel, line, word, label):
        self.trigger = trigger
        self.match_type = match_type  # 'plain' or 'regex'
        self.pkg = pkg
        self.file_rel = file_rel
        self.line = line
        self.word = word
        self.label = label or ""

        # Extract base literal prefix for regex triggers (e.g. ':hooks\(' -> ':hooks')
        if match_type == "regex":
            prefix_match = re.match(r"^([a-zA-Z0-9_\-:\.]+)", trigger)
            self.literal_prefix = prefix_match.group(1) if prefix_match else trigger
        else:
            self.literal_prefix = trigger

    def __repr__(self):
        return f"<MatchEntry {self.trigger!r} ({self.match_type}, word={self.word}) {self.file_rel}:{self.line}>"


def load_matches(include_base=False):
    """Yield MatchEntry for all plain and regex triggers across packages."""
    files_to_check = []

    # Walk all package directories
    for root, dirs, files in os.walk(REPO_ROOT):
        rel_root = os.path.relpath(root, REPO_ROOT)
        parts = rel_root.split(os.sep) if rel_root != "." else []
        if parts:
            top_dir = parts[0]
            if top_dir in IGNORED_PACKAGES or top_dir.startswith((".", "_")):
                continue

        for f in sorted(files):
            if f.endswith((".yml", ".yaml")) and not f.startswith("."):
                pkg = parts[0] if parts else "root"
                files_to_check.append((os.path.join(root, f), pkg))

    # Optional base.yml check in parent directory
    if include_base:
        base_path = os.path.abspath(os.path.join(REPO_ROOT, "..", "base.yml"))
        if os.path.exists(base_path):
            files_to_check.append((base_path, "base"))

    for path, pkg in files_to_check:
        file_rel = os.path.relpath(path, REPO_ROOT)
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.load(f, Loader=SafeLineLoader)
        except Exception as e:
            print(f"ERROR reading {file_rel}: {e}", file=sys.stderr)
            continue

        if not isinstance(data, dict):
            continue

        for match in data.get("matches", []):
            if not isinstance(match, dict):
                continue
            line = match.get("__line__", 1)
            word = bool(match.get("word", False))
            label = match.get("label", "")

            # 1. Plain triggers (trigger / triggers)
            triggers = match.get("triggers") or (
                [match["trigger"]] if "trigger" in match else []
            )
            for t in triggers:
                yield MatchEntry(
                    trigger=str(t),
                    match_type="plain",
                    pkg=pkg,
                    file_rel=file_rel,
                    line=line,
                    word=word,
                    label=label,
                )

            # 2. Regex triggers
            if "regex" in match:
                yield MatchEntry(
                    trigger=str(match["regex"]),
                    match_type="regex",
                    pkg=pkg,
                    file_rel=file_rel,
                    line=line,
                    word=word,
                    label=label,
                )


def audit_triggers(matches, warn_all=False, verbose=False):
    """Audit triggers for duplicates, critical shadowing, and overlapping prefixes."""
    errors = 0
    warnings = 0

    # ---------------------------------------------------------
    # Check 1: Exact Duplicates
    # ---------------------------------------------------------
    by_trigger = collections.defaultdict(list)
    for m in matches:
        by_trigger[m.trigger].append(m)

    duplicate_groups = {k: v for k, v in by_trigger.items() if len(v) > 1}

    print(f"Auditing {len(matches)} trigger definitions across packages...")

    if duplicate_groups:
        print("\n=== DUPLICATE TRIGGER AUDIT ===")
        for trigger, entries in sorted(duplicate_groups.items()):
            labels = [e.label for e in entries]
            distinct_labels = all(labels) and len(set(labels)) == len(labels)

            pkgs_str = ", ".join(f"{e.pkg} ({e.file_rel}:{e.line})" for e in entries)
            if distinct_labels:
                if verbose:
                    print(
                        f"ALLOWED DUPLICATE  {trigger!r} ({len(entries)}x) - "
                        f"disambiguated by labels in: {pkgs_str}"
                    )
            else:
                errors += 1
                print(
                    f"ERROR: DUPLICATE COLLISION  {trigger!r} defined {len(entries)}x without unique labels!\n"
                    f"  Locations: {pkgs_str}\n"
                    f"  Espanso cannot disambiguate this trigger. Ensure all occurrences have distinct labels."
                )

    # ---------------------------------------------------------
    # Check 2: Prefix Shadowing & Overlaps without `word: true`
    # ---------------------------------------------------------
    critical_shadowing = []
    word_protected_overlaps = collections.defaultdict(list)

    for m_short in matches:
        t_short = m_short.trigger
        short_prefix = m_short.literal_prefix

        for m_long in matches:
            if m_short is m_long:
                continue

            t_long = m_long.trigger
            long_prefix = m_long.literal_prefix

            # Skip identical triggers (handled in duplicate check)
            if t_short == t_long:
                continue

            is_overlap = False
            overlap_kind = ""

            # Case A: Plain short trigger prefixes longer plain trigger
            if m_short.match_type == "plain" and m_long.match_type == "plain":
                if t_long.startswith(t_short):
                    is_overlap = True
                    overlap_kind = "plain_prefixes_plain"

            # Case B: Plain short trigger prefixes regex trigger (e.g. :hooks vs :hooks\()
            elif m_short.match_type == "plain" and m_long.match_type == "regex":
                if long_prefix.startswith(t_short):
                    is_overlap = True
                    overlap_kind = "plain_prefixes_regex"

            if not is_overlap:
                continue

            if not m_short.word:
                # CRITICAL: Trigger without word: true fires instantly, shadowing the longer trigger
                critical_shadowing.append((m_short, m_long, overlap_kind))
            else:
                # Trigger has word: true; safe from instant firing, but shares prefix
                word_protected_overlaps[m_short].append(m_long)

    print("\n=== OVERLAPPING TRIGGERS (WITHOUT word: true) ===")
    if critical_shadowing:
        # Deduplicate reporting pairs
        seen_pairs = set()
        for m_short, m_long, kind in critical_shadowing:
            pair_key = (m_short.trigger, m_short.file_rel, m_long.trigger, m_long.file_rel)
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)
            errors += 1

            if kind == "plain_prefixes_regex":
                print(
                    f"CRITICAL OVERLAP [UNREACHABLE REGEX]:\n"
                    f"  Trigger:       {m_short.trigger!r} (word: false)\n"
                    f"  Defined in:    {m_short.pkg} [{m_short.file_rel}:{m_short.line}]\n"
                    f"  Shadows Regex: {m_long.trigger!r}\n"
                    f"  Defined in:    {m_long.pkg} [{m_long.file_rel}:{m_long.line}]\n"
                    f"  -> Explanation: When typing {m_long.literal_prefix!r}, {m_short.trigger!r} expands immediately.\n"
                    f"  -> Fix: Add 'word: true' to {m_short.trigger!r} or rename.\n"
                )
            else:
                print(
                    f"CRITICAL OVERLAP [UNREACHABLE TRIGGER]:\n"
                    f"  Short Trigger: {m_short.trigger!r} (word: false)\n"
                    f"  Defined in:    {m_short.pkg} [{m_short.file_rel}:{m_short.line}]\n"
                    f"  Shadows:       {m_long.trigger!r}\n"
                    f"  Defined in:    {m_long.pkg} [{m_long.file_rel}:{m_long.line}]\n"
                    f"  -> Explanation: When typing {m_long.trigger!r}, {m_short.trigger!r} expands before completion.\n"
                    f"  -> Fix: Add 'word: true' to {m_short.trigger!r} or rename.\n"
                )
    else:
        print("OK: No critical prefix shadowing found without 'word: true'.")

    # ---------------------------------------------------------
    # Check 3: Overlapping Prefixes with `word: true` (Warnings)
    # ---------------------------------------------------------
    if word_protected_overlaps:
        warnings = len(word_protected_overlaps)
        if warn_all or verbose:
            print("\n=== OVERLAPPING PREFIXES (PROTECTED BY word: true) ===")
            print(
                "Note: These triggers share prefixes, but the shorter trigger has 'word: true',\n"
                "so the longer trigger remains typeable unless preceded/followed by a word separator.\n"
            )
            for m_short, longs in sorted(word_protected_overlaps.items(), key=lambda x: x[0].trigger):
                unique_longs = sorted(list({l.trigger for l in longs}))
                pkgs = sorted(list({l.pkg for l in longs}))
                print(
                    f"WARNING: PREFIX SHARE  {m_short.trigger!r} (word: true in {m_short.pkg}) "
                    f"is prefix of {len(unique_longs)} triggers across [{', '.join(pkgs)}]:\n"
                    f"  Example targets: {', '.join(unique_longs[:4])}{'...' if len(unique_longs) > 4 else ''}"
                )
        else:
            print(
                f"\nINFO: {warnings} triggers with 'word: true' share prefixes with longer triggers (safe).\n"
                f"      Run with '--warn-all' to view the full list of prefix-sharing triggers."
            )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------
    print("\n=== AUDIT SUMMARY ===")
    print(f"Total triggers scanned: {len(matches)}")
    print(f"Disallowed duplicate collisions: {len(duplicate_groups) - sum(1 for e in duplicate_groups.values() if all(x.label for x in e) and len(set(x.label for x in e)) == len(e))}")
    print(f"Critical shadowing overlaps (missing word: true): {len(critical_shadowing)}")
    print(f"Prefix-sharing triggers protected by word: true: {len(word_protected_overlaps)}")

    if errors:
        print(f"\nFAILED: {errors} critical problem(s) found. Please resolve the issues above.")
        return 1

    print("\nSUCCESS: All triggers verified! No unhandled duplicates or critical shadowing.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Audit espanso triggers for duplicates, prefix shadowing, and overlaps."
    )
    parser.add_argument(
        "--warn-all",
        action="store_true",
        help="Print all overlapping triggers, including those protected by 'word: true'.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (shows allowed duplicates and full target details).",
    )
    parser.add_argument(
        "--include-base",
        action="store_true",
        help="Also check base.yml in the parent directory if present.",
    )
    args = parser.parse_args()

    matches = list(load_matches(include_base=args.include_base))
    return audit_triggers(matches, warn_all=args.warn_all, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())

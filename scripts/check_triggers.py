#!/usr/bin/env python3
"""Audit espanso packages for duplicate and shadowed triggers.

Checks every */package.yml in the repo for:

1. Exact duplicate triggers. Duplicates are allowed only when every match
   sharing the trigger has a distinct `label` (espanso then shows a
   disambiguation popup instead of picking one arbitrarily).
2. Prefix shadowing: a trigger without `word: true` fires the moment it is
   typed, so any longer trigger it prefixes can never be typed.

Exits non-zero if either check finds a problem.
"""

import collections
import glob
import os
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORED_PACKAGES = {"_example-package"}


def load_matches():
    """Yield (trigger, package, word_flag, label) for every plain trigger."""
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, "*", "package.yml"))):
        pkg = os.path.basename(os.path.dirname(path))
        if pkg in IGNORED_PACKAGES:
            continue
        with open(path) as f:
            data = yaml.safe_load(f)
        for match in data.get("matches", []):
            triggers = match.get("triggers") or (
                [match["trigger"]] if "trigger" in match else []
            )
            for trigger in triggers:
                yield trigger, pkg, bool(match.get("word")), match.get("label")


def main():
    matches = list(load_matches())
    by_trigger = collections.defaultdict(list)
    for trigger, pkg, word, label in matches:
        by_trigger[trigger].append((pkg, word, label))

    problems = 0

    for trigger, entries in sorted(by_trigger.items()):
        if len(entries) < 2:
            continue
        labels = [label for _, _, label in entries]
        if all(labels) and len(set(labels)) == len(labels):
            continue  # intentional label-disambiguated set (e.g. :lorem)
        problems += 1
        pkgs = ", ".join(pkg for pkg, _, _ in entries)
        print(f"DUPLICATE  {trigger!r} defined {len(entries)}x in: {pkgs}")

    triggers = sorted(by_trigger)
    for short in triggers:
        if any(word for _, word, _ in by_trigger[short]):
            continue  # word: true only fires at a word boundary; no shadowing
        for long in triggers:
            if long != short and long.startswith(short):
                short_pkgs = ",".join({p for p, _, _ in by_trigger[short]})
                long_pkgs = ",".join({p for p, _, _ in by_trigger[long]})
                problems += 1
                print(
                    f"SHADOWED   {long!r} ({long_pkgs}) is unreachable: "
                    f"{short!r} ({short_pkgs}) fires first (add `word: true` "
                    f"to {short!r} or rename)"
                )

    total = len(matches)
    if problems:
        print(f"\n{problems} problem(s) found across {total} triggers.")
        return 1
    print(f"OK: {total} triggers, no duplicates or shadowing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

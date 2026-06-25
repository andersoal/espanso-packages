---
name: espanso-trigger-creator
description: >-
  Create, debug, review, and teach Espanso text-expansion triggers — from
  simple text replacements to regex captures, interactive forms, and
  shell-command variables. Use whenever the user mentions Espanso, text
  expanders, match files, "trigger", ":me"-style shortcuts, snippet expansion,
  or wants to automate typing (signatures, emails, commands, templates).
  Trigger for "make an Espanso trigger for X", "Espanso shell command",
  "Espanso form", "Espanso regex match", building/fixing a `.yml` match file,
  or describing the desired typing behavior without naming Espanso. Also use
  to review, audit, clean up, or rewrite an existing match file, not just to
  author new triggers. For runtime-generated dynamic form layouts driven by
  an external script/binary contract, prefer `espanso-dynamic-forms` instead.
license: MIT
metadata:
  author: DevGuyRash
  version: "1.0.0"
  category: development
---

# Espanso Trigger Creator

Build and teach Espanso match-file triggers — simple text replacement up through regex, interactive forms, and shell-powered automation. This skill is the general-purpose Espanso reference. For dynamic, script-generated form *layouts* (a provider contract pattern), defer to `espanso-dynamic-forms`.

## How to teach as you build (adaptive style)

- **Simple, familiar ask** ("make a trigger for my email signature") → give the YAML directly, one or two lines on why it's structured that way, done.
- **New concept for the user, or a complex/multi-feature trigger** (regex + shell, multi-field forms, chained vars) → briefly walk through each piece (trigger/regex syntax → vars → replace) *before* assembling the final YAML, so the user understands what each part does, not just copy-paste output.
- Always produce valid, ready-to-paste YAML. Never give pseudo-YAML.
- Default file target: the user's `match/base.yml` (or a new file under `match/` if they're organizing by topic) inside the Espanso config directory — mention this path concept but don't assume their OS-specific path unless they tell you or you ask.

## Quick OS note

Espanso config root differs by OS:
- Linux: `~/.config/espanso/`
- macOS: `~/Library/Application Support/espanso/`
- Windows: `%APPDATA%\espanso\`

Match files live in `match/` inside that root (`base.yml` by default). If the user hasn't said their OS and it matters (e.g. giving a full path or OS-specific shell command), ask — don't assume.

## Core decision: which trigger type?

| User wants... | Use | Reference |
|---|---|---|
| Fixed text → fixed output | Plain `trigger`/`replace` | [references/basics.md](references/basics.md) |
| Output depends on typed input | `regex` match with capture groups | [references/regex-and-vars.md](references/regex-and-vars.md) |
| Prompt a dialog for input | `form` | [references/forms.md](references/forms.md) |
| Run a command / compute something | `shell` var | [references/shell-and-automation.md](references/shell-and-automation.md) |
| Date/time, clipboard, random, or other built-ins | built-in var types | [references/regex-and-vars.md](references/regex-and-vars.md) |
| Script generates the *entire form layout* at runtime | defer to `espanso-dynamic-forms` skill | — |

Read the relevant reference file(s) before writing nontrivial triggers — they hold the syntax details, gotchas, and security notes so this file stays short. For straightforward asks you may already know enough from this file's examples below; for anything regex/shell/form-related, skim the reference first.

## Minimal examples (for the simple, no-reference-needed cases)

Plain text:
```yaml
- trigger: ":sig"
  replace: "Jane Doe | jane@example.com | (555) 867-5309"
```

Built-in date var:
```yaml
- trigger: ":today"
  replace: "{{date}}"
  vars:
    - name: date
      type: date
      params:
        format: "%Y-%m-%d"
```

Word-boundary fix (typo autocorrect):
```yaml
- trigger: "teh"
  replace: "the"
  word: true
```

For anything beyond these patterns — regex captures, multi-step forms, shell commands, clipboard manipulation, chained vars — read the matching reference file first, then build.

## Validation before handing off

After writing a trigger:
1. Confirm YAML indentation is consistent (2 spaces, no tabs) — Espanso match files are whitespace-sensitive.
2. If `regex` is used, mention that `trigger` and `regex` are mutually exclusive on the same match — never include both.
3. If `shell` is used, read [references/shell-and-automation.md](references/shell-and-automation.md) for the security/latency notes before finalizing — never suggest a shell command that exfiltrates input unsafely or blocks on slow network calls without flagging the tradeoff.
4. Ensure the match structure complies with the official Espanso JSON schema. For example, never use invalid form field attributes like `type: text` or `type: checkbox`. (Text fields should omit `type` entirely, and multiline fields should use `multiline: true`).
5. Tell the user which file to paste it into and to run `espanso restart` (or it'll reload automatically depending on their install) to pick up changes.

## Debugging existing triggers

If the user pastes a broken match file or describes unexpected behavior:
- Check trigger/regex mutual exclusivity, indentation, and missing `vars:` blocks for `{{name}}` placeholders referenced in `replace`.
- Check for `word: true` issues (trigger firing mid-word or not firing as a suffix).
- For form issues, check that every `[[field]]` in the `layout` has a matching entry under `fields:`.
- See [references/patterns-and-pitfalls.md](references/patterns-and-pitfalls.md) for a fuller checklist and common failure modes.

This is reactive, single-trigger troubleshooting. For a full audit or cleanup pass across a whole file (or several), use the systematic process below instead.

## Reviewing & refactoring existing triggers (full file audit)

Use this when the user asks to "review," "audit," "clean up," "rewrite," or "improve" an existing match file (or pastes a large/established config without a specific single bug) — not just when one trigger misbehaves.

1. **Inventory first.** Read the whole file (or all pasted files) before commenting on anything. Note every `trigger`/`triggers`/`regex` value as you go — you need the full list to catch cross-match problems in step 3.
2. **Per-match checklist.** For each match entry, run it against [references/patterns-and-pitfalls.md](references/patterns-and-pitfalls.md)'s debugging checklist (items 1–5: indentation, trigger/regex collision, unresolved placeholders, `word: true` correctness, shell var hygiene).
3. **Cross-file/cross-match checks** (these need the full inventory, not just one match at a time):
   - Duplicate or shadowing triggers across matches/files (checklist item 7).
   - Inconsistent conventions — mixed `:`-prefix usage, inconsistent quoting style, some triggers using `triggers:` (plural) where others use `trigger:` for the same kind of shortcut.
   - Files that have grown past ~15-20 matches with no topic split (see "prefer composability" pattern in patterns-and-pitfalls.md).
4. **Anti-pattern sweep.** Check every match against the anti-patterns in patterns-and-pitfalls.md specifically:
   - Hardcoded absolute paths in `cmd:` → should use `%CONFIG%`.
   - Status-text leakage (replace text describes a side effect instead of delivering the payload).
   - Shell vars interpolating regex/form captures directly into `cmd` without quoting or env-var isolation — flag every instance, not just the first (see shell-and-automation.md security note).
   - Unbounded/uncontrolled dynamic output with no fallback.
5. **Report before rewriting.** Summarize findings grouped by severity (breaks the trigger / works but risky / style-only) before presenting a rewritten file — don't silently rewrite without explaining what changed and why. The user should be able to see the diff in reasoning, not just the diff in YAML.
6. **Propose the rewrite.** Provide corrected YAML for flagged matches (or the full file if changes are pervasive), preserving the user's existing trigger strings and intent unless a trigger collision forces a rename — call out any rename explicitly since it changes muscle memory.

Keep the report concise: a short bulleted list per file/section is more useful than prose paragraphs per match.

---
name: espanso-trigger-creator
description: >-
  Create, design, debug, and teach Espanso text-expansion triggers — from
  simple text replacements to regex captures, interactive forms, shell-command
  variables, and date/clipboard expansions. Use this skill whenever the user
  mentions Espanso, text expanders, match files, "trigger", ":me"-style
  shortcuts, snippet expansion, or wants to automate typing (signatures,
  emails, commands, IPs, templates). Always trigger this for requests like
  "make an Espanso trigger for X", "how do I expand text when I type Y",
  "Espanso shell command", "Espanso form", "Espanso regex match", or any
  request to build, fix, or explain a `.yml` Espanso match file — even if the
  user doesn't say the word "skill" or "Espanso" explicitly but describes the
  behavior (e.g. "I want typing :sig to paste my signature"). For
  runtime-generated dynamic form layouts driven by an external script/binary
  contract, prefer the more specialized `espanso-dynamic-forms` skill instead.
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
4. Tell the user which file to paste it into and to run `espanso restart` (or it'll reload automatically depending on their install) to pick up changes.

## Debugging existing triggers

If the user pastes a broken match file or describes unexpected behavior:
- Check trigger/regex mutual exclusivity, indentation, and missing `vars:` blocks for `{{name}}` placeholders referenced in `replace`.
- Check for `word: true` issues (trigger firing mid-word or not firing as a suffix).
- For form issues, check that every `[[field]]` in the `layout` has a matching entry under `fields:`.
- See [references/patterns-and-pitfalls.md](references/patterns-and-pitfalls.md) for a fuller checklist and common failure modes.

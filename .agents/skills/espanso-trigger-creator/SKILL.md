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
| Fixed text → fixed output | Plain `trigger` or `triggers` (array) / `replace` | [references/basics.md](references/basics.md) |
| Multiple shortcuts / aliases for same output | `triggers:` (flow `[...]` or block list) | [references/basics.md](references/basics.md) |
| Case-adaptive text (hello/Hello/HELLO) | `propagate_case: true` (optional `uppercase_style`) | [references/basics.md](references/basics.md) |
| Initial cursor placed at a specific spot | Cursor hint `$|$` in `replace` | [references/basics.md](references/basics.md) |
| Word boundary check (whole word vs prefix only) | `word: true` (whole word) or `left_word: true` (word start) | [references/basics.md](references/basics.md) |
| Output depends on typed input | `regex` match with capture groups `(?P<name>...)` | [references/regex-and-vars.md](references/regex-and-vars.md) |
| Rich formatted text (Markdown or HTML) | `markdown:` (with optional `paragraph: true`) or `html:` | [references/basics.md](references/basics.md) |
| Paste an image file | `image_path: "$CONFIG/images/..."` | [references/basics.md](references/basics.md) |
| Force clipboard paste / override injection | `force_clipboard: true` or `force_mode: clipboard` | [references/basics.md](references/basics.md) |
| Interactive search/dropdown selection | `choice` extension (`type: choice`) | [references/regex-and-vars.md](references/regex-and-vars.md) |
| Prompt a dialog with multiple inputs | `form` (`layout` + `form_fields`) | [references/forms.md](references/forms.md) |
| Run a command in shell | `shell` var (`cmd`, `trim`, `shell`, `debug`) | [references/shell-and-automation.md](references/shell-and-automation.md) |
| Run an external binary directly (safe args) | `script` var (`args`, `trim`) | [references/shell-and-automation.md](references/shell-and-automation.md) |
| Date/time (offsets, timezone, locale), clipboard, random | built-in var types (`date`, `clipboard`, `random`, `echo`) | [references/regex-and-vars.md](references/regex-and-vars.md) |
| Reusable template snippets / anchors | YAML `anchors:` and `anchor: &name` | [references/basics.md](references/basics.md) |
| Modular match files / private sets | Root `imports:` and file-level `global_vars:` | [references/basics.md](references/basics.md) |
| Script generates the *entire form layout* at runtime | defer to `espanso-dynamic-forms` skill | — |

Read the relevant reference file(s) before writing nontrivial triggers — they hold the syntax details, gotchas, and security notes so this file stays short. For straightforward asks you may already know enough from this file's examples below; for anything regex/shell/form-related, skim the reference first.

## Minimal examples (for the simple, no-reference-needed cases)

Plain text with cursor placement:
```yaml
- trigger: ":fn"
  label: "[Code] JavaScript Function (Template with Initial Cursor Inside)"
  replace: "function $|$() {\n\n}"
```

Case-adaptive replacement:
```yaml
- trigger: "greet"
  label: "[Text] Greeting (Case Adaptive Hello Expansion)"
  replace: "hello"
  propagate_case: true
```

Multiple triggers (aliases / YAML array):
```yaml
# Flow sequence (inline array)
- triggers: [":sig", ":signature"]
  label: "[General] Email Signature (Short Multi-Trigger Alias)"
  replace: "Jane Doe | jane@example.com"

# Block sequence (indented list)
- triggers:
    - ":email"
    - ":mail"
  label: "[General] Email Address (Direct Address Paste)"
  replace: "jane@example.com"
```

Built-in date var with offset (e.g. tomorrow):
```yaml
- trigger: ":tomorrow"
  label: "[General] Tomorrow's Date (ISO Format with 86400s Offset)"
  replace: "{{date}}"
  vars:
    - name: date
      type: date
      params:
        format: "%Y-%m-%d"
        offset: 86400
```

Word-boundary fix (typo autocorrect):
```yaml
- trigger: "teh"
  label: "[Autocorrect] The (Fix Typo Teh to The)"
  replace: "the"
  word: true
```

Interactive choice dialog:
```yaml
- trigger: ":status"
  label: "[General] Status Selector (Choose from Active List)"
  replace: "Status: {{val}}"
  vars:
    - name: val
      type: choice
      params:
        values:
          - "In Progress"
          - "Under Review"
          - "Completed"
```

For anything beyond these patterns — regex captures, multi-step forms, shell commands, clipboard manipulation, chained vars — read the matching reference file first, then build.

## Validation before handing off

After writing a trigger:
1. Ensure line 1 of the match file retains `# yaml-language-server: $schema=https://raw.githubusercontent.com/espanso/espanso/dev/schemas/match.schema.json` for IDE validation.
2. Confirm YAML indentation is consistent (2 spaces, no tabs) and multi-line strings in `form:` or `replace:` use literal block scalar `|` (avoid single-quoted multi-line strings with `''` escaping).
3. Ensure the match is well-documented with high-ergonomics metadata:
   - **Label Standard**: `label: "[<Package Tag>] <Intuitive Recall Concept> (<Complementary Context/Snippet/Action>)"`
     - **Intuitive Recall Concept**: Clear, memorable concept title explaining what the trigger accomplishes (never a raw/lazy repeat of the trigger name, e.g. `:pceo` -> `CEO & Founder Profile`, never `Pceo`; `:pmatch` -> `Job Match Analysis`, never `Pmatch`).
     - **Complementary Context**: Meaningful parenthetical detail indicating what the snippet produces, key input variables, or framework applied (e.g. `(Interactive Persona Formulation)`, `(STAR Method)`, `(Plain Language & Everyday Analogies)`).
     - **No Truncated Prepositions**: Never leave sentence fragments ending in prepositions or connecting words ("For", "To", "With", "About", "On", "Of", "In", "At", "Into", "As", "A", "An", "The").
     - **No Raw Placeholders**: Never include unparsed template tokens like `[[...]]` or `{{...}}` in labels.
   - `search_terms:` containing the package name and key aliases for fuzzy search discovery.
   - `# <Context/Notes>`: Document prompt intent or instructions using native YAML `# <description>` comments (with `#` hashtag) inside the match definition. Never use a `comment:` YAML property on matches.
4. If `regex` is used, mention that `trigger` and `regex` are mutually exclusive on the same match — never include both.
5. **Match Disambiguation & Triggers**:
   - Multiple matches CAN share the exact same trigger per official Espanso docs (`https://espanso.org/docs/matches/basics/#match-disambiguation`); Espanso will display an interactive selection popup. When identical triggers exist, ensure each has a distinct `label:` to facilitate selection.
   - Avoid unintentional prefix collisions where a non-word trigger (e.g. `:act`) shadows a longer trigger (e.g. `:action`). Use `word: true` or distinct triggers when immediate firing is not intended.
6. If `shell` is used, read [references/shell-and-automation.md](references/shell-and-automation.md) for the security/latency notes before finalizing — never suggest a shell command that exfiltrates input unsafely or blocks on slow network calls without flagging the tradeoff.
7. **Schema & Form Hygiene**:
   - Ensure the match structure complies with the official Espanso JSON schema.
   - Text fields in forms should omit `type` entirely, and multiline fields should use `multiline: true` (never specify `type: text`, `type: checkbox`, or `multiline: false`).
   - Choice/list form fields require `type: choice` or `type: list` and `values: [...]`.
   - Variable names (in `vars:` and `[[form_fields]]`) MUST only contain alphanumeric characters and underscores (`[a-zA-Z0-9_]+`). **Never use hyphens** in form placeholders (e.g. use `[[task_before]]`, never `[[task-before]]`).
   - For `vars: type: choice`, prefer `{ id: "...", label: "..." }` value objects for complete schema validation compliance.
8. **Cursor Placement**: If an initial cursor landing position is desired after expansion, verify `$|$` is placed inside `replace:` (e.g. `function $|$()`).
9. **Case Propagation**: When matching words/greetings typed in lowercase, Titlecase, or UPPERCASE, verify `propagate_case: true` is configured where appropriate (and optional `uppercase_style: uppercase | capitalize | capitalize_words`).
10. **Escaping Curly Braces**: If literal `{{` and `}}` are needed in `replace` (e.g., in code templates or Jinja/Handlebars), verify they are escaped as `\\{\\{...}}` in quoted strings or `\{\{...}}` in block scalars.
11. **Package Specification**: If creating or updating a package, ensure the package directory and manifest `name` match `^[a-z0-9-]+$` (lowercase letters, numbers, hyphens only), and that `_manifest.yml`, `package.yml`, and `README.md` are all present.
12. Tell the user which file to paste it into and to run `espanso restart` (or it'll reload automatically depending on their install) to pick up changes.
13. **Update Manifest Version**: On any change to a package's triggers or files, update `<package>/_manifest.yml` with a **MAJOR** (breaking change / trigger renaming), **MINOR** (new triggers / features), or **PATCH** (bug fixes / typos / doc updates) version bump.

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
2. **Per-match checklist.** For each match entry, run it against [references/patterns-and-pitfalls.md](references/patterns-and-pitfalls.md)'s debugging checklist (items 1-5: indentation, trigger/regex collision, unresolved placeholders, `word: true` correctness, shell var hygiene) and verify metadata:
   - Check `label:` follows `[<Package Tag>] <Intuitive Concept> (<Complementary Context/Action>)`.
   - Ensure labels do not use raw trigger names, do not end in prepositions ("For", "To", "With", etc.), and contain no unparsed `[[field]]` placeholders.
3. **Cross-file/cross-match checks** (these need the full inventory, not just one match at a time):
   - Duplicate or shadowing triggers across matches/files (checklist item 7).
   - Inconsistent conventions — mixed `:`-prefix usage, inconsistent quoting style, some triggers using `triggers:` (plural) where others use `trigger:` for the same kind of shortcut.
   - Files that have grown past ~15-20 matches with no topic split (see "prefer composability" pattern in patterns-and-pitfalls.md).
4. **Anti-pattern sweep.** Check every match against the anti-patterns in patterns-and-pitfalls.md specifically:
   - Lazy, truncated, or raw trigger labels (violating the ergonomic label pattern).
   - Hardcoded absolute paths in `cmd:` → should use `%CONFIG%`.
   - Status-text leakage (replace text describes a side effect instead of delivering the payload).
   - Shell vars interpolating regex/form captures directly into `cmd` without quoting or env-var isolation — flag every instance, not just the first (see shell-and-automation.md security note).
   - Unbounded/uncontrolled dynamic output with no fallback.
5. **Report before rewriting.** Summarize findings grouped by severity (breaks the trigger / works but risky / style-only) before presenting a rewritten file — don't silently rewrite without explaining what changed and why. The user should be able to see the diff in reasoning, not just the diff in YAML.
6. **Propose the rewrite.** Provide corrected YAML for flagged matches (or the full file if changes are pervasive), preserving the user's existing trigger strings and intent unless a trigger collision forces a rename — call out any rename explicitly since it changes muscle memory.

Keep the report concise: a short bulleted list per file/section is more useful than prose paragraphs per match.

# Espanso Basics: Trigger / Replace

## Anatomy of a match

```yaml
matches:
  - trigger: ":me"
    replace: "Jane Doe"
```

- `trigger`: the exact string typed that fires the expansion. Convention: prefix with `:` since it's rare in normal English typing — but it's not required.
- `replace`: what gets typed in its place.

## Multiple triggers, one replacement (YAML array / list)

When you want multiple shortcuts or aliases to expand to the same replacement, use `triggers:` (plural) with a YAML array/sequence.

**Flow sequence (inline array):**
```yaml
- triggers: [":sig", ":signature"]
  replace: "Jane Doe | jane@example.com"
```

**Block sequence (multi-line list):**
```yaml
- triggers:
    - ":sig"
    - ":signature"
    - ":sign"
  replace: "Jane Doe | jane@example.com"
```

Both styles are valid YAML and fully supported by Espanso. Use inline arrays for short 2-3 item lists and indented block lists when there are many aliases.


## Word-boundary matching (typo autocorrect)

```yaml
- trigger: "teh"
  replace: "the"
  word: true
```

`word: true` requires the trigger be surrounded by word boundaries (so it fires on "teh " or "teh." but not inside "Teheran"). Without it, Espanso matches substrings anywhere, which is usually what you want for `:`-prefixed triggers but *not* for bare-word autocorrects.

## Multi-line replacements

```yaml
- trigger: ":addr"
  replace: |
    123 Main St
    Springfield, ST 00000
```

Use the YAML block scalar `|` to preserve line breaks exactly. Avoid single-quoted multiline strings that lead to noisy `''` escaping.

## Match Metadata: Label, Comment & Search Terms

Espanso matches support built-in metadata properties:

```yaml
- trigger: :c-review
  label: "[Engineering] Code Review & Quality Audit"
  comment: "Conducts a 2-pass code review (quality standards + edge cases/risks)"
  search_terms:
    - engineering
    - code review
    - pr
  form: |
    Review this code for quality and correctness:
    [[code]]
```

- `label`: Human-readable title displayed in the Espanso search bar (`Alt + Space`) and disambiguation popups. Convention: use `[Package Tag] Descriptive Title` so triggers are easily identifiable.
- `comment`: Contextual description explaining the prompt's intent directly in YAML without modifying output.
- `search_terms`: Search keywords/aliases used by Espanso's fuzzy search palette to find triggers by concept.

## Schema Header Directive

Always include the language server schema directive at the top of every match file:
```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/espanso/espanso/dev/schemas/match.schema.json
```

## Organizing match files

Don't cram everything into `base.yml` once it grows. Espanso loads all `.yml`/`.yaml` files under `match/`. Common organization:

```
match/
├── base.yml       # core/everyday
├── email.yml      # email templates
├── dev.yml        # shell/dev shortcuts
└── forms.yml       # interactive forms
```

Each file needs its own `matches:` top-level key — they're independent documents, not merged sections of one file.

## File-level config (rare, but know it exists)

A match file can carry top-level settings like `word: true` applied skill-wide via `matches` defaults, but per-match overrides are more common and more predictable. Prefer being explicit per-match unless you have a strong reason for a file-wide default.

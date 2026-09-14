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

## Cursor placement (`$|$`)

Espanso supports positioning the cursor at a specific point inside the replacement after expansion by inserting the cursor hint `$|$`:

```yaml
- trigger: ":fn"
  replace: "function $|$() {\n\n}"
```

When you type `:fn`, Espanso types `function () {\n\n}` and places your cursor right between the space and parentheses.

## Case propagation (`propagate_case: true`)

`propagate_case: true` enables case-adaptive expansions. Espanso recognizes uppercase and capitalized trigger variants and adapts the output accordingly:

```yaml
- trigger: "greet"
  replace: "hello"
  propagate_case: true
```

- Typing `greet` yields `hello`
- Typing `Greet` yields `Hello`
- Typing `GREET` yields `HELLO`

Note: When using `propagate_case: true`, the `trigger` must be defined in all lowercase.

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
  label: "[Engineering] Code Review & Quality Audit (2-Pass Standards & Risks)"
  comment: "Conducts a 2-pass code review (quality standards + edge cases/risks)"
  search_terms:
    - engineering
    - code review
    - pr
  form: |
    Review this code for quality and correctness:
    [[code]]
```

- `label`: Human-readable title displayed in the Espanso search bar (`Alt + Space`) and disambiguation popups.
  - **Standard Format**: `[<Package Tag>] <Intuitive Recall Concept> (<Complementary Context/Snippet/Action>)`
  - **Intuitive Recall Concept**: Use an easy-to-remember title describing the primary action or topic. Avoid raw trigger repeats (`[Marketing] Pceo` is bad; `[Marketing] CEO & Founder Profile` is good).
  - **Complementary Context**: Add parenthesized detail describing what the prompt actually does, the output format, or form fields involved (`(Interactive Persona Formulation)`).
  - **No Truncated Prepositions**: Avoid ending labels with prepositions/connectors (`[Prompts] Write A First Draft Of` is bad; `[Prompts] First Draft Generator (Initial Version from Angle)` is good).
  - **No Raw Placeholders**: Never leave raw variables like `[[topic]]` or `{{date}}` inside labels.
- `comment`: Contextual description explaining the prompt's intent directly in YAML without modifying output.
- `search_terms`: Search keywords/aliases used by Espanso's fuzzy search palette to find triggers by concept.

## Match Disambiguation

When multiple matches share the exact same trigger, Espanso displays a native disambiguation dialog keyed by `label:`, allowing you to choose the desired expansion:

```yaml
- trigger: ":quote"
  label: "[Quotes] Steve Jobs (Stay Hungry Stay Foolish)"
  replace: "Stay hungry, stay foolish."

- trigger: ":quote"
  label: "[Quotes] Alan Kay (Invent the Future)"
  replace: "The best way to predict the future is to invent it."
```

Each duplicate trigger must have a unique, descriptive `label:` so the disambiguation popup is clear.

## Injection Modes (`force_mode: clipboard` vs `keys`)

By default, Espanso injects text using emulated keystrokes or automatically switches to clipboard injection for large snippets. You can explicitly enforce clipboard or keystroke injection on a specific match:

```yaml
- trigger: ":huge-template"
  replace: |
    ... large multiline content ...
  force_mode: clipboard
```

- `force_mode: clipboard`: Fast and reliable for large text blocks, emojis, or non-ASCII characters.
- `force_mode: keys`: Emulates keyboard typing directly; useful when an application restricts clipboard access or pasting.

## Global Variables (`global_vars:`)

To share variables across multiple matches within the same YAML file, declare `global_vars:` at the root level before `matches:`:

```yaml
global_vars:
  - name: company
    type: echo
    params:
      echo: "Acme Corporation"
  - name: my_date
    type: date
    params:
      format: "%Y-%m-%d"

matches:
  - trigger: ":co"
    replace: "Welcome to {{company}}!"

  - trigger: ":notice"
    replace: "Published by {{company}} on {{my_date}}."
```

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

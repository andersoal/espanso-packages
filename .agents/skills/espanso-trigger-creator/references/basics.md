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


## Word-boundary matching (`word: true` and `left_word: true`)

```yaml
- trigger: "ther"
  replace: "there"
  word: true
```

- `word: true`: requires the trigger be surrounded by word boundaries on both sides (spaces, commas, punctuation, newlines). Prevents "ther" from firing inside "other" or "bother".
- `left_word: true`: ensures a match only occurs at the beginning of a word (preceded by a word separator), but not in the middle. Unlike `word: true`, it permits immediate trailing characters. Useful for expanding at the start of words or prefixes.

## Cursor placement (`$|$`)

Espanso supports positioning the cursor at a specific point inside the replacement after expansion by inserting the cursor hint `$|$`:

```yaml
- trigger: ":fn"
  replace: "function $|$() {\n\n}"
```

When you type `:fn`, Espanso types `function () {\n\n}` and places your cursor right between the space and parentheses.
- Note: Only one cursor hint `$|$` is permitted per match. Multiple hints are ignored.

## Case propagation & uppercase style

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

### Multi-word capitalization (`uppercase_style`)

By default, `propagate_case: true` capitalizes only the first word in multi-word replacements (`Ordinary least squares`). To customize this, specify `uppercase_style`:
```yaml
- trigger: ";ols"
  replace: "ordinary least squares"
  propagate_case: true
  uppercase_style: capitalize_words
```

Possible values for `uppercase_style`:
- `capitalize`: Capitalizes only the first word (default).
- `capitalize_words`: Capitalizes every word in the replacement (`Ordinary Least Squares`).
- `uppercase`: Converts every letter to uppercase (`ORDINARY LEAST SQUARES`).

## Rich Text (Markdown & HTML)

Espanso supports rich formatted text expansions using Markdown or HTML:

```yaml
- trigger: ":rich"
  markdown: "This *text* is **very rich**!"
  paragraph: true

- trigger: ":badge"
  html: |
    <p>Status: <span style="color: #ffffff; background: #28a745; padding: 2px 6px; border-radius: 3px;">Active</span></p>
```

- `markdown`: Parses and injects text formatted with Markdown syntax.
- `paragraph: true`: Optional setting for `markdown:` matches. Prevents Espanso from automatically appending a trailing newline and starting a new paragraph.
- `html`: Injects raw formatted HTML content.

## Image Matches (`image_path`)

Espanso can expand matches into images rather than text:

```yaml
- trigger: ":logo"
  image_path: "$CONFIG/images/logo.png"
```

- Specify `image_path` instead of `replace`.
- Use the `$CONFIG` convention (`$CONFIG/images/...`) for portability across systems.
- Format support: PNG, JPEG, and GIF on Windows and macOS. On Linux, PNG is strongly recommended for desktop clipboard compatibility.

## Keyboard Triggers

Espanso can respond to CTRL-key triggers by specifying ASCII hex-codes:
```yaml
- trigger: "\x05" # <Ctrl+E>
  replace: "Expanded via Ctrl+E"
  force_mode: keys
```
- Note: CTRL combinations can conflict with editor menu shortcuts; `force_mode: keys` may be needed to prevent over-backspacing.


## Match Metadata: Label & Search Terms

Espanso matches support built-in metadata properties:

```yaml
- trigger: :c-review
  label: "[Engineering] Code Review & Quality Audit (2-Pass Standards & Risks)"
  # Conducts a 2-pass code review (quality standards + edge cases/risks)
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
- `# <Context/Notes>`: Native YAML comments starting with `#` (hashtag) placed inside the match block to document intent and instructions. Never use a `comment:` YAML property.
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

## Injection Modes (`force_clipboard: true` & `force_mode: clipboard` vs `keys`)

By default, Espanso injects text using emulated keystrokes or automatically switches to clipboard injection for large snippets. You can explicitly enforce clipboard or keystroke injection on a specific match:

```yaml
- trigger: ":huge-template"
  replace: |
    ... large multiline content ...
  force_clipboard: true
```

- `force_clipboard: true`: Directly forces Espanso to inject the text via system clipboard paste. Fast and reliable for large text blocks, emojis, or non-ASCII characters.
- `force_mode: clipboard`: Overrides the injection backend mechanism to use clipboard paste.
- `force_mode: keys`: Overrides backend mechanism to emulate keyboard typing directly; useful when an application restricts clipboard access or pasting.

## YAML Anchors and Aliases (`anchors:` and `anchor:`)

To reuse common text, snippets, or script code across multiple matches without duplicating YAML, use the YAML Anchor/Alias syntax:

```yaml
anchors:
  shared_text: &shared_greeting |
    Hello! Thank you for contacting our support team.
    How can we assist you today?

matches:
  - trigger: ":sup1"
    replace: *shared_greeting

  - trigger: ":sup2"
    replace: |
      *shared_greeting
      (Priority Queue)
```

You can also embed an anchor directly on a match:
```yaml
- trigger: ":base-fn"
  anchor: &base_snippet "console.log('standard');"
  replace: *base_snippet
```

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

## Organizing match files & Imports (`imports:`)

Don't cram everything into `base.yml` once it grows. Espanso loads all `.yml`/`.yaml` files under `match/`. Common organization:

```
match/
├── base.yml       # core/everyday
├── email.yml      # email templates
├── dev.yml        # shell/dev shortcuts
└── forms.yml       # interactive forms
```

Each file needs its own `matches:` top-level key — they're independent documents, not merged sections of one file.

### Loading External Files with `imports:`

Espanso supports the `imports:` root property to load match sets located outside the default directory or group private files:

```yaml
# Import match sets from external locations
imports:
  - "/path/to/shared/company_matches.yml"
  - "./_private_tokens.yml"

matches:
  - trigger: ":ping"
    replace: "pong"
```

### Private Match Sets (Underscore Prefix `_`)
Files whose names begin with an underscore (e.g. `_js_snippets.yml`) are ignored by Espanso's automatic directory scanner. They will only be loaded if explicitly included via `imports:` in another match file, or via `extra_includes:` in an app-specific configuration (`config/<app>.yml`).


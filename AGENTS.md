# Espanso Packages Repository Guidelines

## Package Manifest Versioning Rule

Whenever any modification, addition, or deletion is made to files within a package (such as `package.yml`, `_manifest.yml`, `README.md`, or any files within a package directory):

**You MUST update the package's `_manifest.yml` `version` field according to Semantic Versioning (`MAJOR.MINOR.PATCH`):**

1. **MAJOR version bump (`X.0.0`)**:
   - Apply when introducing breaking changes, removing triggers, renaming existing triggers, changing trigger behavior in a way that breaks existing user workflows/shortcuts, or major package structural overhauls.
   - Example: `1.4.2` -> `2.0.0`

2. **MINOR version bump (`X.Y.0`)**:
   - Apply when adding new triggers, adding new features, expanding templates with new functionality, or making backward-compatible enhancements.
   - Example: `1.4.2` -> `1.5.0` (reset patch to 0)

3. **PATCH version bump (`X.Y.Z`)**:
   - Apply for backward-compatible bug fixes, minor typo corrections, formatting tweaks, documentation fixes, or small prompt refinements.
   - Example: `1.4.2` -> `1.4.3`

### Instructions for Agent:
- Always locate `<package-name>/_manifest.yml`.
- Inspect the current `version`.
- Increment the appropriate **MAJOR**, **MINOR**, or **PATCH** version component.
- Ensure the `_manifest.yml` is updated as part of the same change / commit.

---

## Package Structure & Specification (Official Docs Standard)

All packages in this repository must conform to the official Espanso package specification (`https://espanso.org/docs/packages/package-specification/`):

1. **Package Directory & Name Rules**:
   - Every package must live in its own directory: `<package-name>/`.
   - **Name constraint**: Package names must only contain lowercase letters, numbers, and the hyphen symbol `-` (`^[a-z0-9-]+$`). No uppercase, underscores, or spaces.
2. **Mandatory Package Files**:
   - `_manifest.yml`: Metadata descriptor containing:
     - `name`: Must exactly match the package directory name.
     - `title`: Human-readable display title.
     - `description`: Concise summary of the package's domain/purpose.
     - `version`: Semantic version (`MAJOR.MINOR.PATCH`).
     - `author`: Maintainer / creator name.
     - `tags`: (Optional) List of topical tags.
   - `package.yml`: Primary match file containing the triggers, forms, and replacements.
   - `README.md`: Markdown documentation describing available triggers, use-cases, and variable options.
3. **Optional Package Files**:
   - Additional `.yml` match files: Espanso automatically loads all `.yml` files in a package directory, allowing large packages to be cleanly split into sub-modules.
   - Scripts directory: Helper binaries or shell scripts called by `shell` extensions.

---

## Match Quality & Ergonomics Standards

Every match definition across all packages must adhere to these consistency and ergonomic rules:

1. **IDE Schema Header**:
   Line 1 of every match file must specify the official JSON schema directive:
   ```yaml
   # yaml-language-server: $schema=https://raw.githubusercontent.com/espanso/espanso/dev/schemas/match.schema.json
   ```

2. **High-Ergonomics Label Standard**:
   Every trigger must define a clean, human-readable label:
   ```yaml
   label: "[<Package Tag>] <Intuitive Recall Concept> (<Complementary Context/Snippet/Action>)"
   ```
   - **Intuitive Recall Concept**: Clear, memorable concept title describing the primary task (never a raw repeat of the trigger name, e.g. `:pceo` -> `CEO & Founder Profile`, never `Pceo`).
   - **Complementary Context**: Parenthetical detail indicating output type, key form fields, or method (e.g. `(Interactive Persona Formulation)`, `(STAR Framework)`).
   - **No Dangling Prepositions**: Never end labels with prepositions or connectors ("For", "To", "With", "About", "On", "Of", "In", "At", "Into", "As", "A", "An", "The").
   - **No Raw Placeholders**: Never include unparsed template variables like `[[...]]` or `{{...}}` in labels.

3. **Metadata Hygiene**:
   - `label`: Mandatory clear display title used for search and popup disambiguation.
   - `# <Context/Notes>`: Document prompt intent, instructions, or contextual tips using native YAML `# <description>` comments (with `#` hashtag) directly inside the match block.
   - **No `comment:` property on matches**: Espanso does not use `comment:` for search or expansion. Never define `comment:` as a YAML key on matches; always use native `#` hashtag comments instead.
   - `search_terms`: Include package tag and relevant search keywords for fuzzy search discovery (`Alt + Space`).
   - `replace`/`form`: Use YAML literal block scalar `|` for multi-line text to preserve line breaks and avoid ugly `''` quote escaping.

---

## Core Espanso Feature Guidelines (Official Docs Reference)

When authoring or updating triggers, leverage native Espanso capabilities:

- **Match Disambiguation (Identical Triggers)**:
  According to official Espanso docs (`https://espanso.org/docs/matches/basics/#match-disambiguation`), **multiple matches CAN share the exact same trigger**. When typed, Espanso displays a selection popup allowing the user to choose the right expansion.
  - To support disambiguation, each match sharing the same trigger **must** define a distinct, human-readable `label:`.
  - Avoid creating awkward, synthetic trigger variations when sharing an intuitive trigger with popup disambiguation is clearer.

- **Cursor Placement (`$|$)**: Place the cursor at an exact spot in the expansion:
  ```yaml
  - trigger: ":fn"
    replace: "function $|$() {\n\n}"
  ```
- **Case Propagation (`propagate_case: true`)**: Adapt capitalization automatically based on how the trigger was typed:
  ```yaml
  - trigger: "greet"
    replace: "hello"
    propagate_case: true
  # "greet" -> "hello", "Greet" -> "Hello", "GREET" -> "HELLO"
  ```
- **Word Boundary Controls (`word`, `left_word`, `right_word`)**:
  - `word: true`: Expands only when surrounded by word separators (spaces, commas, punctuation, newlines). Critical for autocorrect triggers.
  - `left_word: true`: Matches only at the start of a word.
  - `right_word: true`: Matches only at the end of a word.
  - Prefix shadowing warning: Shorter triggers without `word: true` fire immediately and shadow longer triggers. Use `word: true` or distinct prefixes.

- **Uppercase Style (`uppercase_style`)**:
  When `propagate_case: true` is enabled, customize the casing format with `uppercase_style: uppercase | capitalize | capitalize_words`. Note that `uppercase_style` requires `propagate_case: true`.

- **Rich Text & Image Matches**:
  - `markdown: "..."`: Formats text using Markdown. Use `paragraph: true` to prevent automatic newline/paragraph insertion.
  - `html: "..."`: Injects rich HTML content.
  - `image_path: "$CONFIG/images/example.png"`: Expands trigger into an image. Always use `$CONFIG` for portable cross-platform paths.

- **Form Controls (`form:` & `form_fields:`)**:
  - Text input (default): Omit `type` entirely. Use `multiline: true` for multi-line text areas. Never specify `type: text` or `multiline: false`.
  - Choice box (`type: choice`): Single select dropdown with `values: [...]`.
  - List box (`type: list`): List selection control with `values: [...]` and optional `separator: ","`.
  - **Form Variable Naming**: Form fields in `[[field_name]]` and `form_fields` MUST use alphanumeric characters and underscores (`[a-zA-Z0-9_]+`). **Never use hyphens** (e.g. `[[task_before]]`, never `[[task-before]]`), as hyphens are evaluated as subtraction operators in templating expressions.

- **Variable Extensions (`vars:`)**:
  - Variable names MUST only contain alphanumeric characters and underscores (`[a-zA-Z0-9_]+`).
  - `date`: Supports `format` (strftime format string), `offset` (seconds in future/past), `locale` (BCP47, e.g. `en-US`), `tz` (IANA timezone).
  - `choice`: Selection dialog in replacement; supports `values: [{ id: "...", label: "..." }]` for full schema compliance, or string lists.
  - `random`: Random selection with `choices: [...]`.
  - `clipboard`: Fetches current system clipboard content.
  - `shell`: Runs shell commands with `cmd: "..."`, optional `shell: bash|cmd|powershell|pwsh|sh|zsh|wsl`, `trim: true`, and `debug: true`.
  - `script`: Calls external script binaries with `args: [...]` and `trim: true`.
  - `match`: Nested matches referencing existing triggers with `trigger: ":other"`.
  - `echo`: Echoes literal text via `echo: "..."`.

- **Environment Variables & Variable Chaining (`depends_on`)**:
  - Shell commands and scripts automatically receive variables as uppercase environment variables: `$ESPANSO_<VAR_NAME>` (e.g. `{{name}}` -> `$ESPANSO_NAME`).
  - When variables depend on other variables (e.g., shell command using form input), explicitly declare `depends_on: [var1, var2]` to enforce evaluation order.
  - Use `inject_vars: false` when variable syntax (`{{...}}`) inside commands or scripts should not be parsed by Espanso.

- **Regex Triggers (`regex`)**:
  - Use `regex` instead of `trigger` (they are strictly mutually exclusive).
  - Espanso uses the Rust `regex` engine. Named capture groups MUST follow Rust syntax: `(?P<group_name>...)`.
  - Captured named groups automatically become Espanso variables accessible via `{{group_name}}` in `replace` or `$ESPANSO_GROUP_NAME` in shell scripts.
  - Escape backslashes in quoted strings (e.g. `":greet\\d"`), or use unquoted scalars (`regex: :greet\d`).

- **Quotes & Escaping**:
  - Double quotes are required for strings containing `\n`, `\t`, or starting with YAML special characters (`' " [ ] { } > | * & ! % # \` @`).
  - Literal curly braces in replacement text must be escaped as `\\{\\{...}}` in quoted strings or `\{\{...}}` in YAML block scalars.
  - Prefer clean YAML literal block scalars (`|`) for multi-line replacements.

- **Global Variables (`global_vars:`)**: Reusable variables declared at the root level above `matches:` for cross-match sharing within a file.



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
   - `comment`: Describe the prompt's intent and contextual tips without altering expansion output.
   - `search_terms`: Include package tag and relevant search keywords for fuzzy search discovery (`Alt + Space`).
   - `replace`/`form`: Use YAML literal block scalar `|` for multi-line text to preserve line breaks and avoid ugly `''` quote escaping.

---

## Core Espanso Feature Guidelines (Official Docs Reference)

When authoring or updating triggers, leverage native Espanso capabilities:

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
- **Word Boundary (`word: true`)**: Ensure expansions fire only when surrounded by word separators (spaces, commas, punctuation), critical for autocorrect triggers:
  ```yaml
  - trigger: "teh"
    replace: "the"
    word: true
  ```
- **Match Disambiguation**: When multiple matches share the same trigger, Espanso displays a selection popup. Ensure distinct, descriptive `label:` attributes to make disambiguation intuitive.
- **Form Controls (`form:` & `form_fields:`)**:
  - Text input (default): Omit `type` entirely. Use `multiline: true` for multi-line text areas.
  - Choice box (`type: choice`): Single select dropdown with `values: [...]`.
  - List box (`type: list`): List selection control with `values: [...]`.
- **Variable Extensions (`vars:`)**:
  - `date`: Supports `format` (strftime), `offset` (seconds in future/past), `locale` (BCP47, e.g. `en-US`), `tz` (IANA timezone).
  - `choice`: Selection dialog in replacement; supports `values: [...]` or `{ label: "...", id: "..." }`.
  - `random`: Random selection with `choices: [...]`.
  - `clipboard`: Fetches current system clipboard content.
  - `shell`: Runs shell commands with `cmd: "..."`, optional `shell: powershell|bash|sh|cmd`, and `trim: true`.
- **Variable Injection & Escaping**:
  - Variable injection occurs inside `params` and `replace` using `{{var_name}}`.
  - Literal curly braces in replacement text must be escaped as `\\{\\{...}}` (in quoted strings) or `\{\{...}}` (in block scalars).
- **Global Variables (`global_vars:`)**: Reusable variables declared at the root level above `matches:` for cross-match sharing within a file.


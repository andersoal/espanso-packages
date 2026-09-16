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
## Comprehensive Espanso Match Schema Property Reference (Official Docs Standard)

Every match file in this repository must conform to `https://raw.githubusercontent.com/espanso/espanso/dev/schemas/match.schema.json`. Below is the complete specification and contextual guidance for every schema property, derived from the official Espanso documentation:

### 1. Root-Level File Properties

- **`$schema`** (`string`):
  Official JSON schema directive for IDE auto-completion and validation.
  - Recommended header on Line 1:
    ```yaml
    # yaml-language-server: $schema=https://raw.githubusercontent.com/espanso/espanso/dev/schemas/match.schema.json
    ```
  - May alternatively be specified as a YAML property: `$schema: "https://raw.githubusercontent.com/espanso/espanso/dev/schemas/match.schema.json"`.

- **`imports`** (`array` of `string`):
  Imports other match sets from external locations outside the configuration directory, or groups modular files:
  ```yaml
  imports:
    - "/path/to/shared/matches.yml"
    - "./_submodule.yml"
  ```
  - **Private Match Sets (`_`)**: Files prefixed with an underscore (e.g. `_code.yml`) are ignored by Espanso's automatic directory scanner. Use `imports:` or `extra_includes:` in app-specific configs (`config/<app>.yml`) to selectively bundle and activate them.

- **`anchors`** (`array` of `object`):
  Defines reusable YAML anchor blocks (`&anchor_name`) placed *before* the `matches:` section in the same file:
  ```yaml
  anchors:
    script_snippet: &shared_script |
      import sys
      print("Shared logic")
  ```

- **`matches`** (`array` of `match` objects):
  The primary array containing all text expansion definitions in the file.

- **`global_vars`** (`array` of `var` objects):
  Defines variables shared across all matches in the current file and its descendants. Evaluated before match-local variables unless explicit dependencies are declared:
  ```yaml
  global_vars:
    - name: user_company
      type: echo
      params:
        echo: "Acme Corp"
  ```

---

### 2. Match Object Properties (`matches:`)

- **`trigger`** (`string`):
  Single string sequence typed by the user that fires the expansion (e.g. `":greet"`).
  - Mutually exclusive with `triggers` and `regex`.
  - Prefix convention: Use `:` or similar non-letter characters to prevent accidental typing in regular prose.

- **`triggers`** (`array` of `string`):
  Multiple alternative trigger strings (aliases) mapping to the same expansion:
  ```yaml
  - triggers: [":sig", ":signature"]
    replace: "Jane Doe | jane@example.com"
  ```
  - Mutually exclusive with `trigger` and `regex`.

- **`regex`** (`string`):
  Regular expression trigger matching dynamic input patterns using the Rust `regex` engine:
  ```yaml
  - regex: ":greet\\((?P<person>.*)\\)"
    replace: "Hello {{person}}!"
  ```
  - **Named capture groups**: Syntax MUST be `(?P<name>exp)`. Captured groups become variables accessible via `{{name}}` in `replace` and `$ESPANSO_NAME` in scripts.
  - Mutually exclusive with `trigger` and `triggers`.

- **`replace`** (`string` or `null`):
  Plain text expansion or template containing variable placeholders (`{{var_name}}`). Can be omitted or set to `null` when using `form:`, `image_path:`, `markdown:`, or `html:`.
  - Place cursor hint `$|$` where the cursor should land after expansion.
  - Multi-line expansions must use YAML literal block scalar `|`.

- **`form`** (`string`):
  Interactive popup form layout template containing `[[field_name]]` placeholders:
  ```yaml
  - trigger: ":meeting"
    form: |
      Meeting with [[client]] on [[date]]
      Notes: [[notes]]
    form_fields:
      notes:
        multiline: true
  ```
  - Shorthand for an inline form extension. Prompt submitted via `Ctrl+Enter` (or `Cmd+Enter` on macOS) or canceled with `Esc`.

- **`form_fields`** (`object`):
  Configures the interactive controls for `[[field_name]]` variables in `form:`:
  - Text input (default): Omit `type` entirely. Use `multiline: true` for multiline text areas; `default: "..."` for pre-filled text.
  - Dropdown box: `type: choice`, `values: [...]`, `default: "..."`.
  - Selection list: `type: list`, `values: [...]`, `default: "..."`, `separator: ","`.
  - String trimming: `trim_string_values: true` when `values:` is a multiline string to trim whitespace and drop empty lines.

- **`markdown`** (`string`):
  Formats expansion as rich Markdown text:
  ```yaml
  - trigger: ":bold"
    markdown: "This **important notice** is formatted via Markdown."
    paragraph: true
  ```

- **`paragraph`** (`boolean`):
  Used exclusively with `markdown:`. When set to `true`, prevents Espanso from automatically appending a trailing newline and starting a new paragraph.

- **`html`** (`string`):
  Injects rich formatted HTML directly:
  ```yaml
  - trigger: ":badge"
    html: "<span style='color: #ffffff; background: #007acc; padding: 2px 6px; border-radius: 3px;'>STATUS</span>"
  ```

- **`image_path`** (`string`):
  Expands the trigger into an image pasted from the filesystem:
  ```yaml
  - trigger: ":logo"
    image_path: "$CONFIG/images/logo.png"
  ```
  - Use `$CONFIG` for portable cross-platform paths. Supports PNG, JPEG, GIF (PNG recommended on Linux).

- **`label`** (`string`):
  Mandatory human-readable title shown in the Search Bar (`Alt+Space`) and the Match Disambiguation dialog:
  - Format: `[<Package Tag>] <Intuitive Recall Concept> (<Complementary Context/Snippet/Action>)`.
  - Must never simply repeat the trigger name, end in a dangling preposition, or include unparsed `[[field]]` placeholders.

- **`search_terms`** (`array` of `string`):
  Keywords and synonyms indexed by Espanso's fuzzy search engine to make matches discoverable in the Search Bar.

- **`word`** (`boolean`):
  When `true`, triggers only when surrounded by word separators (spaces, commas, punctuation, newlines). Critical for autocorrect triggers to avoid mid-word expansions.

- **`left_word`** (`boolean`):
  When `true`, triggers only when preceded by a word separator (at the start of a word), preventing accidental triggers inside other words while allowing immediate trailing text.

- **`propagate_case`** (`boolean`):
  Adapts the casing of the replacement based on how the trigger was typed (lowercase -> lowercase, Capitalized -> Capitalized, UPPERCASE -> UPPERCASE).
  - Requirement: The `trigger` MUST be defined in all lowercase.

- **`uppercase_style`** (`string` enum: `uppercase`, `capitalize`, `capitalize_words`):
  Controls multi-word capitalization behavior when `propagate_case: true` is active:
  - `capitalize`: Capitalizes only the first word (default behavior).
  - `capitalize_words`: Capitalizes every word in the replacement (e.g. `ordinary least squares` -> `Ordinary Least Squares`).
  - `uppercase`: Converts all letters to uppercase.

- **`force_clipboard`** (`boolean`):
  Forces Espanso to inject the replacement via system clipboard paste rather than simulating keystrokes. Highly recommended for large multi-line texts, emojis, non-ASCII characters, or laggy applications.

- **`force_mode`** (`string` enum: `clipboard`, `keys`):
  Overrides Espanso's injection backend for this specific match:
  - `clipboard`: Forces clipboard paste.
  - `keys`: Forces simulated keystrokes (useful when target app blocks clipboard paste).
  - Note: Used primarily for testing or workarounds; persistent app-level preferences should be configured via `backend:` in `config/<app>.yml`.

- **`anchor`** (`string`):
  YAML anchor identifier (`anchor: &anchor_name`) allowing subsequent matches to alias or inherit properties.

- **`comment`** (`string`):
  Property defined in the JSON schema. **Repository Rule**: Do NOT use `comment:` as a YAML key on matches. Always use native YAML `# <description>` (hashtag) comments inside the match block.

- **`vars`** (`array` of `var` objects):
  Dynamic variable definitions evaluated before the replacement is expanded.

---

### 3. Variable Extensions (`vars:` and `global_vars:`)

All variable definitions require `name:` (`[a-zA-Z0-9_]+`) and `type:`. Common optional properties:
- **`inject_vars`** (`boolean`, default `true`): When set to `false`, prevents Espanso from parsing `{{var}}` placeholders inside `params`, passing them as literal strings.
- **`depends_on`** (`array` of `string`): Explicitly specifies execution order dependencies (e.g. `depends_on: ["var_a", "var_b"]`). Essential when chaining variables via environment variables (`$ESPANSO_<NAME>`), where Espanso cannot automatically infer the dependency.

#### Variable Types:

1. **`shell`**:
   Executes shell commands and captures stdout:
   ```yaml
   - name: git_branch
     type: shell
     params:
       cmd: "git rev-parse --abbrev-ref HEAD"
       shell: bash # enum: bash, cmd, fish, nu, powershell, pwsh, sh, wsl, wsl2, zsh
       trim: true  # strips trailing whitespaces and newlines (default true)
       debug: true # logs command execution to 'espanso log'
   ```
   - **Environment Variables**: Variables in scope are injected as uppercase env vars:
     - Bash/WSL: `$ESPANSO_VAR_NAME`
     - PowerShell: `$env:ESPANSO_VAR_NAME`
     - CMD: `%ESPANSO_VAR_NAME%`
     - Special: `CONFIG` points to the Espanso configuration directory.

2. **`script`**:
   Invokes an external binary/script directly without shell wrapping:
   ```yaml
   - name: python_calc
     type: script
     params:
       args: [python, "%CONFIG%/scripts/calc.py", "arg1"]
       trim: true
   ```
   - **Security**: Prefer `script` over `shell` when passing arguments, as `args:` avoids shell parsing and command injection risks. Supports inline scripts via `args: [python, -c, "| ..."]`.

3. **`date`**:
   Generates localized and timezone-aware timestamps:
   ```yaml
   - name: future_date
     type: date
     params:
       format: "%A, %B %d, %Y" # strftime format string
       offset: 86400           # Seconds offset from now (+ for future, - for past). Number or "{{var}}" string
       locale: "en-US"         # BCP47 locale string enum (e.g. en-US, pt-BR, es-ES, de-DE, ja-JP)
       tz: "America/New_York"  # IANA timezone database enum (e.g. UTC, Europe/London, Asia/Tokyo)
   ```

4. **`echo`**:
   Outputs a static string or combines multiple variables:
   ```yaml
   - name: full_name
     type: echo
     params:
       echo: "{{first_name}} {{last_name}}"
   ```

5. **`clipboard`**:
   Retrieves current system clipboard contents:
   ```yaml
   - name: clipboard_content
     type: clipboard
   ```

6. **`choice`**:
   Displays an interactive search/dropdown popup to choose a value:
   ```yaml
   - name: env
     type: choice
     params:
       values:
         - label: "Production Cluster"
           id: "https://prod.example.com"
         - label: "Staging Sandbox"
           id: "https://stage.example.com"
   ```

7. **`form`** (Verbose Form Syntax):
   Defines a form within `vars:` for complex multi-stage pipelines:
   ```yaml
   - name: user_form
     type: form
     params:
       layout: "Name: [[name]]\nRole: [[role]]"
       fields:
         role:
           type: choice
           values: ["Admin", "User", "Guest"]
   ```

8. **`random`**:
   Picks a random item from a list of choices on each expansion:
   ```yaml
   - name: greeting
     type: random
     params:
       choices:
         - "Hello"
         - "Hi"
         - "Greetings"
   ```

9. **`match`** (Nested Match):
   Invokes another existing trigger and embeds its expansion:
   ```yaml
   - name: header
     type: match
     params:
       trigger: ":common-header"
   ```

---

### 4. Quotes, Escaping & Delimiters

- **YAML Block Scalars (`|`)**: Mandatory for all multi-line text replacements and form layouts. Preserves newlines cleanly without escaping quotes.
- **Double Curly Braces Escaping**:
  - Literal `{{...}}` in replacement text (e.g. in Jinja, Vue, Handlebars templates) MUST be escaped:
    - In YAML literal block scalar (`|`): `\{\{variable\}\}`
    - In YAML double-quoted scalar (`"..."`): `\\{\\{variable\\}\\}`
- **Form Placeholders**: Double square brackets `[[variable_name]]` used exclusively in form layouts. Variable names must be snake_case (`[a-zA-Z0-9_]+`); never use hyphens.




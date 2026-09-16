# Regex Matches and Built-in Variables

## Regex matches (capture typed input)

```yaml
- regex: ":greet\\((?P<person>.*)\\)"
  replace: "Hey {{person}}, hope you're doing well!"
```

- Use `regex` instead of `trigger` when the replacement depends on what the user types.
- `regex` and `trigger`/`triggers` are **mutually exclusive** on the same match entry — never combine them.
- Named capture groups (`(?P<name>...)`) become `{{name}}` placeholders directly in `replace` — no `vars:` block needed for simple captures.
- Escape regex metacharacters in YAML double-quoted strings carefully (`\\(` for a literal paren, etc.), or use single quotes / block scalars to avoid double-escaping.

Multiple captures:
```yaml
- regex: ":inv\\((?P<num>\\d+),(?P<client>.*)\\)"
  replace: "Invoice #{{num}} for {{client}}"
```

## Built-in variable types

Declared under a `vars:` list, referenced as `{{name}}` in `replace` (or in a `form` layout).

### date
```yaml
- trigger: ":tomorrow"
  replace: "Tomorrow is {{date}}"
  vars:
    - name: date
      type: date
      params:
        format: "%A, %B %d, %Y"
        offset: 86400           # Seconds added to current time (86400 = +1 day)
        locale: "en-US"         # BCP47 locale for localized month/day names
        tz: "America/New_York"  # IANA timezone
```
- `format`: `strftime` syntax (`%Y-%m-%d`, `%H:%M:%S`, `%A`, `%B`, etc.).
- `offset`: Integer offset in seconds. Positive numbers for future dates, negative for past dates.
- `locale`: BCP47 locale string (e.g. `en-US`, `pt-BR`, `de-DE`, `fr-FR`).
- `tz`: IANA timezone identifier (e.g. `UTC`, `America/New_York`, `Europe/London`).

### choice
Prompts the user with an interactive dropdown selection dialog during expansion:

**Simple string list:**
```yaml
- trigger: ":env"
  replace: "Selected environment: {{target}}"
  vars:
    - name: target
      type: choice
      params:
        values:
          - "development"
          - "staging"
          - "production"
```

**Custom labels with distinct IDs/payloads:**
```yaml
- trigger: ":api"
  replace: "Endpoint: {{endpoint}}"
  vars:
    - name: endpoint
      type: choice
      params:
        values:
          - label: "Production API"
            id: "https://api.prod.example.com"
          - label: "Staging Sandbox"
            id: "https://api.stage.example.com"
```

### clipboard
```yaml
- trigger: ":paste-wrapped"
  replace: "<<{{clip}}>>"
  vars:
    - name: clip
      type: clipboard
```
Inserts current clipboard contents. Useful for wrapping/transforming whatever was last copied.

### random
```yaml
- trigger: ":coinflip"
  replace: "{{result}}"
  vars:
    - name: result
      type: random
      params:
        choices:
          - "Heads"
          - "Tails"
```

### echo (static passthrough, composing, and global defaults)
```yaml
vars:
  - name: greeting
    type: echo
    params:
      echo: "Hello"
```

### match (nested match)
Includes the output of an existing trigger inside another match:
```yaml
- trigger: ":one"
  replace: "nested"

- trigger: ":nested"
  replace: "This is a {{output}} match"
  vars:
    - name: output
      type: match
      params:
        trigger: ":one"
```

### form (verbose form syntax inside vars)
Defines an interactive form layout within a variable, allowing the result to be passed directly to subsequent script or shell variables:
```yaml
- trigger: ":user"
  replace: "User {{form1.name}} with role {{form1.role}}"
  vars:
    - name: form1
      type: form
      params:
        layout: |
          Name: [[name]]
          Role: [[role]]
        fields:
          role:
            type: choice
            values: ["Admin", "Member", "Guest"]
```

## Variable Injection in `params`

Espanso supports injecting earlier variables or regex captures into subsequent variable `params` using `{{var_name}}`:

```yaml
- regex: ":lookup\\((?P<user>.*)\\)"
  replace: "User info: {{info}}"
  vars:
    - name: info
      type: shell
      params:
        cmd: "gh user view '{{user}}' --json name,bio"
```

Espanso evaluates `vars` in sequential order from top to bottom. A variable can only reference variables or regex captures that precede it.

### Date Offset Variable Injection
The `offset` parameter in `date` vars can be a number (e.g. `86400`) or a string supporting variable injection:
```yaml
- regex: ":offset_date\\((?P<days>\\d+)\\)"
  replace: "Future date: {{future}}"
  vars:
    - name: sec
      type: shell
      params:
        cmd: "expr {{days}} \\* 86400"
    - name: future
      type: date
      params:
        format: "%Y-%m-%d"
        offset: "{{sec}}"
```

## Disabling Variable Injection (`inject_vars: false`)

If a variable's `params` contain curly brackets that should NOT be expanded by Espanso (for example, code strings or template literals), specify `inject_vars: false`:

```yaml
- trigger: ":tpl"
  replace: "Output: {{output}}"
  vars:
    - name: output
      type: echo
      inject_vars: false
      params:
        echo: "{{literal_var}}"
```

## Controlling Execution Order (`depends_on`)

When using environment variables (`$ESPANSO_<VAR>`) in shell commands or when coordinating global variables (`global_vars:`), Espanso cannot automatically detect variable dependencies. Use `depends_on:` to enforce the evaluation order:

```yaml
global_vars:
  - name: one
    type: shell
    params:
      cmd: "echo first"
  - name: two
    type: shell
    depends_on: ["one"]
    params:
      cmd: "echo $ESPANSO_ONE then second"
```

## Escaping Curly Brackets (`\{\{...}}`)

If you want literal double curly braces in your replacement (e.g. for Handlebars, Jinja2, Vue, Django, or GitHub Actions templates), you must escape them so Espanso does not interpret them as variable placeholders:

- **In YAML literal block scalars (`|`)**:
  ```yaml
  - trigger: ":vue-tmpl"
    replace: |
      <template>
        <div>\{\{ message \}\}</div>
      </template>
  ```
- **In YAML double-quoted strings**:
  ```yaml
  - trigger: ":jinj"
    replace: "The user is \\{\\{ user.name \\}\\}"
  ```

If curly braces are not escaped, Espanso will attempt to look up a variable named `message` or `user.name` and fail with an undefined variable error.

## Choosing trigger vs regex vs form

- **trigger**: fixed input → fixed (or var-templated) output. No user-typed parameters.
- **regex**: user encodes a parameter *inline* in the trigger itself (e.g., `:greet(Nikto)`). Fast, no dialog popup, but less discoverable and harder to read for multi-field inputs.
- **choice**: user types a trigger and selects an option from an interactive dropdown before insertion.
- **form**: user is prompted in a dialog for one or more values *after* typing the trigger. Best for multi-field forms. See references/forms.md.


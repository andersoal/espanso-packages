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

### echo (static passthrough, rarely needed directly but useful for composing)
```yaml
vars:
  - name: greeting
    type: echo
    params:
      echo: "Hello"
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

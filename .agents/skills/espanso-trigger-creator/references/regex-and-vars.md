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
- trigger: ":now"
  replace: "It's {{time}}"
  vars:
    - name: time
      type: date
      params:
        format: "%H:%M"
```
Format string follows `strftime` conventions (`%Y-%m-%d`, `%B %d, %Y`, etc.).

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

## Chaining/nesting vars

Vars can reference other vars' output as `params` inputs in some setups (e.g., feeding a `shell` var's output into another var) — this is most common with `shell` (see references/shell-and-automation.md). Keep the dependency order: Espanso evaluates top-to-bottom within the `vars:` list, so a var that depends on another must be declared after it.

## Choosing trigger vs regex vs form

- **trigger**: fixed input → fixed (or var-templated) output. No user-typed parameters.
- **regex**: user encodes a parameter *inline* in the trigger itself (e.g., `:greet(Nikto)`). Fast, no dialog popup, but less discoverable and harder to read for multi-field inputs.
- **form**: user is prompted in a dialog for one or more values *after* typing the trigger. Best for multi-field or when you don't want users to remember exact regex syntax. See references/forms.md.

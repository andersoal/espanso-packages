# Interactive Forms

## Minimal form (single text field)

```yaml
- trigger: ":greet"
  form: |
    Hey [[name]],
    Happy Birthday!
```

Typing `:greet` opens a dialog box with a text field for `name`; Espanso fills `[[name]]` into the layout text and types out the result.

## Multiple fields in one form

```yaml
- trigger: ":followup"
  form: |
    Hi [[name]],

    Following up on [[topic]] — let me know if you have questions.

    Best,
    [[sender]]
  form_fields:
    sender:
      default: "Jane"
```

- Every `[[field]]` placeholder in `layout`/`form` needs either a default text-field behavior (automatic) or an explicit entry under `form_fields` if you want non-default behavior (dropdown, default value, multiline, etc.).
- Fields without an entry in `form_fields` default to a single-line text input.

## Form Submission & Shortcuts

- **Submit**: Press `Ctrl + Enter` on Windows/Linux or `Cmd + Enter` on macOS.
- **Cancel**: Press `Escape`.
- **Navigate fields**: Use `Tab` and `Shift + Tab` to move focus between input fields.

## Field Controls and Types

According to the official Espanso specification, `type` is only used for choice and list controls. Never specify `type: text`!

### 1. Single-line Text Field (Default)
Omit `type` entirely.
```yaml
form_fields:
  client_name:
    default: "Acme Corp"
```

### 2. Multi-line Text Area
Omit `type`, set `multiline: true`.
```yaml
form_fields:
  notes:
    multiline: true
    default: "Initial thoughts..."
```

### 3. Choice Box (Dropdown)
Set `type: choice` with a list of options in `values:`.
```yaml
form_fields:
  tier:
    type: choice
    values:
      - "Free"
      - "Pro"
      - "Enterprise"
    default: "Free"
```

You can also specify `values:` as a multiline string scalar (or populate it dynamically from a shell variable like `values: "{{files}}"`). When using a multiline string, enable `trim_string_values: true` to trim line whitespaces and drop empty lines:
```yaml
form_fields:
  tier:
    type: choice
    values: |
      Free
      Pro
      Enterprise
    trim_string_values: true
```

### 4. List Box (Selectable List)
Set `type: list` with options in `values:`.
```yaml
form_fields:
  environment:
    type: list
    values:
      - "Development"
      - "Staging"
      - "Production"
    default: "Development"
    separator: ", "
```

- **Multiple Selection**: From Espanso v2.4.0, holding `Ctrl` or `Shift` allows selecting multiple items.
- `separator`: The delimiter string used to join multiple selected items (default: `", "`).

### Form Field Properties Reference

| Control Type | Property | Type | Default | Description |
|---|---|---|---|---|
| Text / Multiline | `multiline` | `boolean` | `false` | When `true`, renders a multiline text area. |
| Text / Multiline | `default` | `string` | `""` | Initial pre-filled text in the field. |
| Choice / List | `type` | `string` | — | Must be `"choice"` or `"list"`. |
| Choice / List | `values` | `array` or `string` | — | List of options as array or multiline string. |
| Choice / List | `default` | `string` | `""` | Initial selected option. |
| Choice / List | `trim_string_values` | `boolean` | `false` | Trims whitespace and removes blank lines when `values` is multiline string. |
| List | `separator` | `string` | `", "` | Joining separator when multiple items are selected. |


## Two-stage forms (form result feeds a second form/layout)

Useful when the first form's answers determine what the second form should even show (e.g., pick a "provider" or "template" in form 1, then show provider-specific fields in form 2). This is the foundation of dynamic forms — see `espanso-dynamic-forms` skill for the full runtime-generator pattern. The simple, non-scripted version:

```yaml
- name: form1
  type: form
  params:
    layout: |
      Type:
      [[kind]]
    fields:
      kind:
        type: choice
        values: ["personal", "work"]

- name: form2
  type: form
  params:
    layout: |
      {{#if form1.kind == "work"}}
      Project:
      [[project]]
      {{/if}}
```

Note: conditional layout logic inside Espanso YAML is limited — for anything beyond simple cases, generating the layout text via an external script (the dynamic-forms pattern) is more reliable than trying to encode branching directly in YAML.

## When to reach for forms vs regex

Forms are better when:
- There are 2+ logically distinct fields a user fills out.
- You want a dropdown/checkbox rather than free text.
- Discoverability matters (a regex syntax like `:inv(123,Acme)` is easy to forget; a form dialog is self-explanatory).

Regex is better when:
- It's a single parameter and speed matters (no dialog popup, no extra keystrokes to confirm).
- The user is comfortable with the syntax and types it often (power-user shortcut).

## Common pitfalls

- Mismatched bracket syntax: `[[field]]` in `layout`, but referencing it elsewhere as `{{field}}` — these are *not* interchangeable. `[[ ]]` is form-layout placeholder syntax; `{{ }}` is general var-output substitution syntax used in `replace` and (for some setups) cross-referencing earlier `vars`/named matches.
- Forgetting `form_fields` entries for non-text inputs (dropdowns silently fall back to plain text fields if misconfigured).
- Long forms with no defaults — set sensible `default:` values to reduce friction for repeat use.

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

## Field types

```yaml
form_fields:
  priority:
    type: choice
    values:
      - "Low"
      - "Medium"
      - "High"
  notes:
    multiline: true
  confirmed:
    type: choice
    values:
      - "Yes"
      - "No"
```

Common field configurations: text input (default), multiline text input (`multiline: true`), and choice/list selections (`type: choice` or `type: list` with `values`).

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

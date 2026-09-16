# Patterns and Pitfalls

## Debugging checklist

When a user reports "my trigger isn't working" or pastes broken YAML, check in this order:

1. **YAML indentation.** Espanso match files are whitespace-sensitive (2 spaces, no tabs). A single misaligned line under `vars:` or `form_fields:` can silently break the whole match or file.
2. **trigger vs regex collision.** A match entry must have exactly one of `trigger`/`triggers` or `regex` — never both.
3. **Unresolved placeholders.** Every `{{name}}` in `replace` needs a matching `name:` entry in `vars:` (or a regex named capture). Every `[[field]]` in a form `layout` needs either default text-field behavior or an entry in `form_fields`.
4. **word: true side effects.** If a trigger fires inside other words unexpectedly, the user probably wants `word: true`. If a trigger refuses to fire at all, check they're not accidentally relying on `word: true` while typing the trigger mid-word (e.g., immediately after another character with no boundary).
5. **Shell var returning nothing / erroring silently.** Stderr output from a backing script won't show up in the replacement — ask the user to run the `cmd` directly in their terminal to see real errors. Trailing newline issues (see shell-and-automation.md) are also a frequent culprit for "extra blank line" complaints.
6. **File not loaded.** Confirm the match file lives under `match/` in the Espanso config dir and has a top-level `matches:` key. New files need Espanso restarted (`espanso restart`) or may auto-reload depending on install/version — when in doubt, suggest a restart.
7. **Multiple matches with the same trigger.** Espanso uses the most specific/most recently loaded match when triggers collide across files. Exact duplicate triggers are allowed only when each match has a unique `label:` (which activates Espanso's disambiguation menu).
8. **Prefix shadowing.** A trigger without `word: true` fires immediately when typed. Shorter triggers (e.g. `:act`, `:mck`, `:brain-upgrade`) shadow longer triggers (e.g. `:action-plan`, `:mckinsey-deck`, `:brain-upgrade-30d`). Always make prefix triggers distinct or use `word: true`.
9. **Unescaped double curly braces.** Literal `{{foo}}` in template code (Handlebars, Jinja, Vue) causes Espanso to seek a nonexistent variable `foo`. Escape as `\\{\\{foo\\}\\}` (quoted) or `\{\{foo\}\}` (block scalar `|`).
10. **Package naming violations.** Package directories and manifest `name` fields must strictly match `^[a-z0-9-]+$` (lowercase alphanumeric + hyphens only). Underscores (`_`) and uppercase letters are invalid in Espanso package names.
11. **Invalid form field `type: text`.** Single-line and multi-line text fields in `form_fields` must omit `type` completely (use `multiline: true` for text areas). Specifying `type: text` violates the schema.
12. **Cursor hint typos.** The cursor placement hint must be written exactly as `$|$`. Variations like `$|` or `$$` are typed out as literal text.
13. **Using `comment:` property on matches.** Espanso does not index or display `comment:` match properties. Always use native YAML `# <description>` comments (with hashtag) inside the match block.
14. **Hyphenated form variable names.** Variables in forms (e.g. `[[field-name]]`) can be parsed as subtraction expressions in templating engines. Always use snake_case (`[[field_name]]`).
15. **Choice var schema compliance.** In `vars: type: choice`, the official JSON schema requires `params.values` to contain `{ id: "...", label: "..." }` objects. Plain string arrays are only valid under `form_fields:`.
16. **Missing `depends_on` with environment variables.** When accessing `$ESPANSO_<NAME>` in `shell:` or `script:`, Espanso cannot detect variable dependencies automatically. Declare `depends_on: ["var_name"]`.
17. **`uppercase_style` without `propagate_case: true`.** `uppercase_style` is only valid when `propagate_case: true` is enabled on the match.
18. **Unintentional newlines with `markdown:`.** If expanding markdown inserts an unwanted trailing newline or paragraph, add `paragraph: true` to the match.


## Pattern: prefer composability over one giant match file

Once a user has more than ~15-20 triggers, split by topic (`email.yml`, `dev.yml`, `dates.yml`) rather than one `base.yml`. Easier to debug, easier to disable a whole category, easier to share/version-control a subset.

## Anti-pattern: single-quoted multiline strings & escaped apostrophes

```yaml
# BAD — produced by unconfigured YAML dumpers; hard to read and noisy
- trigger: :app
  replace: 'Design a startup MVP.
    Ensure it''s scalable.
    '

# GOOD — clean YAML literal block scalar
- trigger: :app
  replace: |
    Design a startup MVP.
    Ensure it's scalable.
```

## Anti-pattern: status text replacing payload

```yaml
# BAD — user wanted clipboard content, got a status message instead
- trigger: ":copyit"
  replace: "Copied to clipboard!"
  vars:
    - name: x
      type: shell
      params:
        cmd: "echo 'something' | xclip -selection clipboard"
```

If the goal is to *output* a payload via expansion, the `replace` should contain the payload (or `{{output}}` referencing it), not a side-effect confirmation string. Side effects (like writing to the clipboard) should happen in addition to, not instead of, the typed replacement — and shouldn't block the visible expansion if avoidable.

## Anti-pattern: hardcoded absolute paths

```yaml
# BAD — breaks on any other machine
cmd: "/home/janedoe/scripts/build_report.sh"

# GOOD — portable
cmd: "%CONFIG%/scripts/build_report.sh"
```

## Anti-pattern: unbounded/uncontrolled dynamic content

If a trigger's output depends on a script or external source (shell call, file read), make sure there's a sane fallback or bound — a runaway/huge output from a misbehaving command will type out character-by-character into whatever app has focus, which is hard to interrupt mid-expansion.

## Anti-pattern: lazy, truncated, or raw trigger labels

Labels appear in the search palette and disambiguation menus. If a label simply repeats the trigger name, ends in a dangling preposition, or contains raw placeholder tokens, the user loses context and searchability.

```yaml
# BAD — lazy raw trigger repeat
- trigger: ":prmresearch"
  label: "[Prompts] Prmresearch"

# BAD — truncated sentence ending in preposition
- trigger: ":chain-draft"
  label: "[Prompts] Write A First Draft Of"

# BAD — unparsed template variable
- trigger: ":act"
  label: "[Prompts] [[Persona]]"

# GOOD — intuitive recall title with complementary context/action
- trigger: ":prmresearch"
  label: "[Prompts] Academic Research Audit (Methodology Findings & Limitations Critique)"

- trigger: ":chain-draft"
  label: "[Prompts] First Draft Generator (Initial Version from Angle)"

- trigger: ":act"
  label: "[Prompts] Role Persona Prompt (Interactive Persona & Task Formulation)"
```

## Anti-pattern: invalid package directory or manifest naming

Espanso packages are strict: package names must only contain lowercase alphanumeric characters and hyphens.

```yaml
# BAD — underscores and uppercase break official package specifications
name: "My_Cool_Package"

# GOOD — lowercase alphanumeric and hyphens only (^[a-z0-9-]+$)
name: "my-cool-package"
```

## Anti-pattern: unescaped template variables in code snippets

When expanding template code (e.g. Jinja, Liquid, Handlebars, Helm), literal double curly braces will be treated by Espanso as missing variables unless properly escaped.

```yaml
# BAD — Espanso errors on missing variable 'item.name'
- trigger: ":item-tpl"
  replace: "<span>{{ item.name }}</span>"

# GOOD — escaped curly braces
- trigger: ":item-tpl"
  replace: "<span>\\{\\{ item.name \\}\\}</span>"
```

## Anti-pattern: specifying `type: text` on form fields

Espanso forms only accept `type: choice` or `type: list`. Setting `type: text` violates the JSON schema.

```yaml
# BAD — invalid field type
form_fields:
  author:
    type: text
    default: "Jane"

# GOOD — omit type entirely for text inputs
form_fields:
  author:
    default: "Jane"
```

## Anti-pattern: using `comment:` property on matches

Espanso does not index or search the `comment:` match property. Defining `comment:` as a YAML property wastes schema space and violates repo metadata hygiene.

```yaml
# BAD — YAML key comment
- trigger: :prompt
  label: "[Marketing] Copy Audit"
  comment: "Evaluates copywriting effectiveness"
  replace: "..."

# GOOD — native YAML # hashtag comment
- trigger: :prompt
  label: "[Marketing] Copy Audit"
  # Evaluates copywriting effectiveness
  replace: "..."
```


## When the user actually needs `espanso-dynamic-forms`

If the user describes wanting a *runtime-generated* form layout — i.e., the set of fields or even the structure of the form itself isn't fixed in YAML but produced by a script/binary at expansion time based on a provider/operation contract — that's the `espanso-dynamic-forms` skill's territory, not this one. Signs of this need:
- "the form should look different depending on which [provider/template/mode] I pick"
- "I want a script to generate the whole form layout, not just fill in values"
- Multi-stage forms where stage 2's *structure* (not just values) depends on stage 1's answer, beyond simple show/hide of a couple fields

For straightforward multi-field or two-stage forms with a fixed, known set of fields, this skill's forms.md pattern is sufficient and simpler.

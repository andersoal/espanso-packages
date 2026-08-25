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

## When the user actually needs `espanso-dynamic-forms`

If the user describes wanting a *runtime-generated* form layout — i.e., the set of fields or even the structure of the form itself isn't fixed in YAML but produced by a script/binary at expansion time based on a provider/operation contract — that's the `espanso-dynamic-forms` skill's territory, not this one. Signs of this need:
- "the form should look different depending on which [provider/template/mode] I pick"
- "I want a script to generate the whole form layout, not just fill in values"
- Multi-stage forms where stage 2's *structure* (not just values) depends on stage 1's answer, beyond simple show/hide of a couple fields

For straightforward multi-field or two-stage forms with a fixed, known set of fields, this skill's forms.md pattern is sufficient and simpler.

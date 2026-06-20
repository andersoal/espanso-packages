# Espanso Basics: Trigger / Replace

## Anatomy of a match

```yaml
matches:
  - trigger: ":me"
    replace: "Jane Doe"
```

- `trigger`: the exact string typed that fires the expansion. Convention: prefix with `:` since it's rare in normal English typing — but it's not required.
- `replace`: what gets typed in its place.

## Multiple triggers, one replacement

```yaml
- triggers: [":sig", ":signature"]
  replace: "Jane Doe | jane@example.com"
```

## Word-boundary matching (typo autocorrect)

```yaml
- trigger: "teh"
  replace: "the"
  word: true
```

`word: true` requires the trigger be surrounded by word boundaries (so it fires on "teh " or "teh." but not inside "Teheran"). Without it, Espanso matches substrings anywhere, which is usually what you want for `:`-prefixed triggers but *not* for bare-word autocorrects.

## Multi-line replacements

```yaml
- trigger: ":addr"
  replace: |
    123 Main St
    Springfield, ST 00000
```

Use the YAML block scalar `|` to preserve line breaks exactly.

## Organizing match files

Don't cram everything into `base.yml` once it grows. Espanso loads all `.yml`/`.yaml` files under `match/`. Common organization:

```
match/
├── base.yml       # core/everyday
├── email.yml      # email templates
├── dev.yml        # shell/dev shortcuts
└── forms.yml       # interactive forms
```

Each file needs its own `matches:` top-level key — they're independent documents, not merged sections of one file.

## File-level config (rare, but know it exists)

A match file can carry top-level settings like `word: true` applied skill-wide via `matches` defaults, but per-match overrides are more common and more predictable. Prefer being explicit per-match unless you have a strong reason for a file-wide default.

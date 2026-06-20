# Shell Commands and Automation

## Basic shell var

```yaml
- trigger: ":myip"
  replace: "{{output}}"
  vars:
    - name: output
      type: shell
      params:
        cmd: "curl ifconfig.me"
```

The `cmd` runs in the system shell; stdout becomes the var's value.

## Common automation patterns

Date-stamped status line:
```yaml
- trigger: ":ps"
  replace: "Status Report: {{output}}"
  vars:
    - name: output
      type: shell
      params:
        cmd: "date '+%B %d, %Y'"
```

Base64 encode arbitrary captured text (regex + shell combo):
```yaml
- regex: ":b64\\((?P<val>.*?)\\)"
  replace: "{{output}}"
  vars:
    - name: output
      type: shell
      params:
        cmd: "echo '{{val}}' | base64 | tr -d '\n'"
```

Note the `{{val}}` capture from the regex is interpolated directly into the shell command string — see security note below before using this pattern with untrusted input.

## ⚠️ Security notes

- Shell vars execute arbitrary commands with the user's own privileges. Treat any Espanso match file as equivalent in trust level to a shell script.
- **Never interpolate captured/typed text directly into a shell command without considering injection.** `{{val}}` substitution happens as raw text before the shell parses it — a malicious or just-unlucky input containing `'; rm -rf ~ #` style content run through an interpolated `cmd` is a real risk if the trigger is ever used with untrusted/copy-pasted input. For anything beyond personal, trusted, hand-typed use, prefer passing values as environment variables to a script (like the dynamic-forms contract does) rather than raw string interpolation into `cmd`.
- Flag this explicitly to the user any time you write a shell var that interpolates a regex capture or form field into `cmd`.

## Latency considerations

- Espanso blocks the expansion on the shell command's completion. A slow command (network call, heavy computation) means a visible delay before text appears.
- For network calls (like the `:myip` example), this is usually acceptable for occasional use but mention the tradeoff if the user is building something they'll trigger frequently.
- For anything that needs to feel instant, prefer doing the heavy lifting once (e.g., caching `:myip` output, or precomputing) rather than a `shell` call on every expansion.

## Calling external scripts/binaries

```yaml
- trigger: ":report"
  replace: "{{output}}"
  vars:
    - name: output
      type: shell
      params:
        cmd: "%CONFIG%/scripts/build_report.sh"
```

`%CONFIG%` resolves to the Espanso config directory — use it for portable paths instead of hardcoding an absolute user path, so the match file is portable across machines/OSes (the script itself still needs to exist on each machine, but the YAML reference stays valid).

For multi-argument scripts driven by form/regex inputs, pass values as positional args or env vars rather than building one big interpolated string:

```yaml
- name: output
  type: shell
  params:
    cmd: "%CONFIG%/scripts/build_report.sh '{{form1.client}}' '{{form1.date}}'"
```

Quote each interpolated value to reduce (not eliminate) word-splitting issues; for anything sensitive or complex, an env-var contract (see `espanso-dynamic-forms` skill) is safer than string-built `cmd` lines.

## Output hygiene

- A `shell` var's stdout becomes the literal replacement text — trailing newlines from commands like `date` are often fine, but commands like `echo` may need `tr -d '\n'` or `printf` instead of `echo` to avoid stray blank lines in the expansion.
- Send error/diagnostic output to stderr in any backing script, not stdout — stdout is what gets typed into whatever app the user is in.

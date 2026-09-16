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

## Shell Extension Parameters

- `cmd` (`string`, required): The shell command or executable to execute.
- `shell` (`string` enum, optional): Shell binary to use. Supported options in schema:
  - `bash`, `sh`, `zsh`, `fish`, `nu`, `pwsh`: Cross-platform shells (available on any OS with the binary installed on PATH).
  - `cmd`, `powershell`, `wsl`, `wsl2`: Windows-specific shells (invoke Windows/WSL binaries). Note: Windows `cmd` does not support multiline inline code.
  - Platform defaults: PowerShell on Windows, bash on Linux, user's login shell on macOS.
- `trim` (`boolean`, optional, default: `true`): Automatically strips leading and trailing whitespaces and newlines from command stdout. Disable (`trim: false`) only if preserving exact whitespace is essential.
- `debug` (`boolean`, optional): When `true`, logs the executed command, exit code, and stdout/stderr in Espanso's logs (`espanso log`).
- `inject_vars` (`boolean`, optional, default `true`): If set to `false`, prevents parsing `{{var}}` placeholders inside `cmd`.
- `depends_on` (`array` of `string`, optional): Declares prerequisite variables that must be evaluated first.

Example specifying shell, trim, and debug:
```yaml
- trigger: ":branch"
  replace: "Current git branch: {{branch}}"
  vars:
    - name: branch
      type: shell
      params:
        cmd: "git rev-parse --abbrev-ref HEAD"
        shell: bash
        trim: true
        debug: true
```

## Script Extension (`type: script`)

While `shell` executes commands via a shell interpreter, the **Script Extension** calls an external binary or executable directly, passing arguments as a list:

```yaml
- trigger: ":calc"
  replace: "Result: {{output}}"
  vars:
    - name: output
      type: script
      params:
        args:
          - python
          - "%CONFIG%/scripts/calculate.py"
          - "arg1"
        trim: true
```

### Why use `script` instead of `shell`?
- **Security**: The arguments in `args:` are passed directly to the binary's process invocation without shell expansion, making it inherently safe against shell command injection.
- **No Escaping Hassles**: Special characters, spaces, and quotes in arguments do not require complex shell quote escaping.

### Inline Scripts
Scripts can also be executed inline using `args:`:
```yaml
- trigger: ":fruits"
  replace: "{{output}}"
  vars:
    - name: output
      type: script
      params:
        args:
          - python
          - -c
          - |
            fruits = ["apple", "banana", "cherry"]
            print(", ".join(fruits))
        trim: true
```
*Note for Windows users: Windows enforces an 8,191-character limit on command-line arguments, so large scripts should be stored in separate `.py`/`.ps1` files under `%CONFIG%/scripts/`.*

## Environment Variables & Variable Chaining

When Espanso evaluates a `shell` or `script` variable, it automatically exposes all previously evaluated variables as uppercase environment variables prefixed with `ESPANSO_`:
- `myname` becomes `ESPANSO_MYNAME`
- `form1.city` becomes `ESPANSO_FORM1_CITY`
- `CONFIG` points to the Espanso configuration directory

### Reading Environment Variables by Shell:
- **Bash / WSL / Linux / macOS**: `$ESPANSO_MYNAME`
- **Windows PowerShell**: `$env:ESPANSO_MYNAME`
- **Windows Command Prompt (cmd)**: `%ESPANSO_MYNAME%`
- **Python Scripts**: `os.environ["ESPANSO_MYNAME"]`

### Declaring `depends_on` for Environment Variables
When using environment variables instead of template interpolation (`{{var}}`), Espanso cannot automatically detect dependencies between variables. You MUST explicitly declare `depends_on`:
```yaml
global_vars:
  - name: user_id
    type: shell
    params:
      cmd: "whoami"
  - name: report
    type: shell
    depends_on: ["user_id"]
    params:
      cmd: "echo 'Active user: '$ESPANSO_USER_ID"
```

## UTF-8 Output Encoding Tips
If commands or scripts output non-ASCII or foreign-language characters, ensure stdout is configured for UTF-8:
- **Python**: `import sys; sys.stdout.reconfigure(encoding='utf-8')`
- **PowerShell**: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
- **Bash**: `export LANG='en_US.UTF-8'`


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

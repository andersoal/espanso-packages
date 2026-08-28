# Espanso Packages Collection

A modular collection of custom **[Espanso](https://espanso.org/)** text-expansion packages designed for AI prompt engineering, software development, productivity, cognitive workflows, content strategy, and daily utilities.

---

## 📂 Repository Structure & Packages

- 📁 [`_example-package/`](./_example-package) — Reference template for creating new Espanso packages.
- 📁 [`behavior/`](./behavior) — Triggers and workflows for ADHD cognitive load management, task breakdown, and focus.
- 📁 [`career/`](./career) — Professional framing, resume highlights, interview preparation, and career development prompts.
- 📁 [`content-creation/`](./content-creation) — Storytelling frameworks, copywriting structures, and content creation templates.
- 📁 [`docs/`](./docs) — Documentation, ADRs, and trigger conflict audit reports ([`trigger-audit.md`](./docs/trigger-audit.md)).
- 📁 [`engineering/`](./engineering) — Programming shortcuts, Git/Shell helpers, code block scaffolding, and developer utilities.
- 📁 [`finance/`](./finance) — Financial planning prompts, budgeting macros, and expense tracking shortcuts.
- 📁 [`learn/`](./learn) — Learning frameworks, active recall study prompts, and comprehension shortcuts.
- 📁 [`learn-language/`](./learn-language) — Vocabulary drills, grammar breakdown templates, and translation assistant workflows.
- 📁 [`marketing-sales/`](./marketing-sales) — Pitch templates, sales frameworks, and marketing copy generators.
- 📁 [`mattpocock-skills/`](./mattpocock-skills) — AI prompt templates & agent workflows inspired by Matt Pocock (TDD, Code Review, Bug Diagnosis, Wayfinder, Deep Module Design, Grilling).
- 📁 [`md-formatting/`](./md-formatting) — Markdown callouts, tables, banners, badges, and document formatting shortcuts.
- 📁 [`private/`](./private) — Personal custom triggers and private macros.
- 📁 [`productivity/`](./productivity) — Daily review frameworks, habit tracking, focus blocks, and time management tools.
- 📁 [`prompts/`](./prompts) — General-purpose AI prompts, system instructions, and persona modifiers.
- 📁 [`relationship/`](./relationship) — Interpersonal communication, empathetic feedback frameworks, and conflict resolution templates.
- 📁 [`scripts/`](./scripts) — Repository maintenance tools and validation scripts ([`check_triggers.py`](./scripts/check_triggers.py)).
- 📁 [`social-strategy/`](./social-strategy) — Niche research, content calendars, viral hook design, and social media analytics frameworks.
- 📁 [`thinking-prompts/`](./thinking-prompts) — 10 AI-powered metacognition and self-reflection prompts inspired by SAINT NULL's Thinking Toolkit.
- 📁 [`utils/`](./utils) — Date/time generators, text transforms, system shortcuts, and Espanso macros.

---

## 🚀 Installation & Usage

### 1. Install via Espanso CLI (Recommended)

Since this is a public repository, you can install any package directly using Espanso's CLI with the `--git` and `--external` flags:

```bash
# General syntax
espanso install <package-name> --git https://github.com/andersoal/espanso-packages --external

# Example: Install the prompts package
espanso install prompts --git https://github.com/andersoal/espanso-packages --external

# Example: Install the productivity package
espanso install productivity --git https://github.com/andersoal/espanso-packages --external
```

### 2. Manual Installation (Symlink / Local Copy)

If you prefer to clone and link packages locally:

```bash
# Linux / macOS (Symlink)
ln -s /path/to/packages/prompts ~/.config/espanso/match/packages/prompts

# Windows (Command Prompt as Administrator)
mklink /D "%APPDATA%\espanso\match\packages\prompts" "C:\path\to\packages\prompts"
```

### 3. Restart Espanso

After installing or updating packages, restart Espanso to apply changes:

```bash
espanso restart
```

---

## 🛠️ Repository Maintenance & Auditing

This repository includes custom tooling to ensure trigger hygiene, prevent shortcut collisions, and validate package structure:

### Run Trigger Audit Script

```bash
python scripts/check_triggers.py
```

The script scans all package YAML files to identify:
- Duplicate triggers across packages
- Potential prefix collisions (e.g., `:act` shadowing `:action`)
- Missing or malformed manifest fields
- Syntax & structural warnings

Detailed audit reports are generated in [`docs/trigger-audit.md`](./docs/trigger-audit.md).

---

## 📝 Creating a New Package

Quickly scaffold a new package by copying the [`_example-package`](./_example-package) directory:

```bash
# Copy template to a new package directory
cp -r _example-package my-new-package
```

1. Edit `my-new-package/_manifest.yml` to set package `name`, `title`, `description`, and `author`.
2. Add your Espanso triggers inside `my-new-package/package.yml` (or subfiles under `my-new-package/match/`).
3. Run `python scripts/check_triggers.py` to verify trigger uniqueness and syntax correctness.

---

## 📄 License

This collection is distributed under the [MIT License](./LICENSE). Individual packages may include specific licensing requirements in their respective manifests.


# Espanso Packages Collection

A modular collection of custom **[Espanso](https://espanso.org/)** text-expansion packages designed for AI prompt engineering, software development, productivity, cognitive workflows, content strategy, and daily utilities.

---

## 📂 Repository Structure & Packages

- 📁 [`_example-package/`](./_example-package) — Reference template for creating new Espanso packages.
- 📁 [`behavior/`](./behavior) — Triggers and workflows for ADHD cognitive load management, task breakdown, and focus.
- 📁 [`career/`](./career) — Professional framing, resume highlights, interview preparation, and career development prompts.
- 📁 [`content-creation/`](./content-creation) — Storytelling frameworks, copywriting structures, and content creation templates.
- 📁 [`engineering/`](./engineering) — Programming shortcuts, architecture review, developer utilities, and AI Agent Skills (TDD, Code Review, Bug Diagnosis, Wayfinder, Grilling).
- 📁 [`finance/`](./finance) — Financial planning prompts, budgeting macros, and expense tracking shortcuts.
- 📁 [`genealogy/`](./genealogy) — AI prompts for family tree building, surname origins, public record leads, and ancestry analysis.
- 📁 [`learn/`](./learn) — Learning frameworks, active recall study prompts, and comprehension shortcuts.
- 📁 [`learn-language/`](./learn-language) — Vocabulary drills, grammar breakdown templates, and translation assistant workflows.
- 📁 [`marketing-sales/`](./marketing-sales) — Pitch templates, sales frameworks, and marketing copy generators.
- 📁 [`md-formatting/`](./md-formatting) — Markdown callouts, tables, banners, badges, and document formatting shortcuts.
- 📁 [`private/`](./private) — Personal custom triggers and private macros.
- 📁 [`productivity/`](./productivity) — Daily review frameworks, habit tracking, focus blocks, and time management tools.
- 📁 [`prompts/`](./prompts) — General-purpose AI prompts, system instructions, and persona modifiers.
- 📁 [`relationship/`](./relationship) — Interpersonal communication, empathetic feedback frameworks, and conflict resolution templates.
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

espanso install behavior --git https://github.com/andersoal/espanso-packages --external
espanso install career --git https://github.com/andersoal/espanso-packages --external
espanso install content-creation --git https://github.com/andersoal/espanso-packages --external
espanso install finance --git https://github.com/andersoal/espanso-packages --external
espanso install genealogy --git https://github.com/andersoal/espanso-packages --external
espanso install learn --git https://github.com/andersoal/espanso-packages --external
espanso install learn-language --git https://github.com/andersoal/espanso-packages --external
espanso install marketing-sales --git https://github.com/andersoal/espanso-packages --external
espanso install md-formatting --git https://github.com/andersoal/espanso-packages --external
espanso install prompts --git https://github.com/andersoal/espanso-packages --external
espanso install productivity --git https://github.com/andersoal/espanso-packages --external
espanso install engineering --git https://github.com/andersoal/espanso-packages --external
espanso install social-strategy --git https://github.com/andersoal/espanso-packages --external
espanso install relationship --git https://github.com/andersoal/espanso-packages --external
espanso install thinking-prompts --git https://github.com/andersoal/espanso-packages --external
espanso install utils --git https://github.com/andersoal/espanso-packages --external

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
python _scripts/check_triggers.py
```

The script scans all package YAML files to identify:
- Duplicate triggers across packages
- Potential prefix collisions (e.g., `:act` shadowing `:action`)
- Missing or malformed manifest fields
- Syntax & structural warnings

Detailed audit reports are generated in [`trigger-audit.md`](./_docs/trigger-audit.md).

---

## 📝 Creating a New Package

Quickly scaffold a new package by copying the [`_example-package`](./_example-package) directory:

```bash
# Copy template to a new package directory
cp -r _example-package my-new-package
```

1. Edit `my-new-package/_manifest.yml` to set package `name`, `title`, `description`, and `author`.
2. Add your Espanso triggers inside `my-new-package/package.yml` (or subfiles under `my-new-package/match/`).
3. Run `python _scripts/check_triggers.py` to verify trigger uniqueness and syntax correctness.

---

## 📄 License

This collection is distributed under the [MIT License](./LICENSE). Individual packages may include specific licensing requirements in their respective manifests.



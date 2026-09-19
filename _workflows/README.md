# Workflows & Loop Engine (`_workflows/`)

This directory houses the formal **workflow specifications** designed under the `/loop-me` discipline and operationalized through native **Espanso** text-expansion shortcuts.

Prefixing this directory with an underscore (`_workflows/`) guarantees that Espanso's package scanner treats these files as documentation rather than invalid match bundles.

---

## 1. The Loop Lens & Shared Vocabulary

A **loop** is a recurring pattern in your life or engineering practice: daily nutrition logging, prompt quality assurance, quarterly decision retrospectives, or life management resets. Picturing activities as loops reveals predictable patterns prime for **delegation**.

- **Loop**: The running, recurring instantiation of an activity.
- **Workflow**: The explicit, deterministic specification of a loop, residing in `_workflows/*.md`. It serves as the single source of truth for an implementer agent.
- **Trigger**: The stimulus that starts a run — either an **event** (a prompt drafted, a meal logged) or a **schedule** (daily at 20:00, quarterly).
- **Checkpoint**: A human-in-the-loop review gate where you are asked to verify or decide.
- **Push Right**: The design discipline of deferring the checkpoint as far to the right as possible. Complete maximal autonomous work before asking the human, keeping cognitive overhead minimal.
- **Brief**: The decision-ready document presented at a checkpoint. Contains the what, the why, and a tradeoff delta — never raw unstructured output.
- **Department**: A self-contained operational domain in personal life management (e.g. Operations, Health, Finances, Craft, Relationships) maintaining dedicated logs.

---

## 2. System Environment & Tooling

- **Text Expansion Runtime**: Espanso v2+ on Windows (`%APPDATA%\espanso`), managed through this repository (`c:\Users\ag\Documents\Obsidian\espanso\match\packages`).
- **Primary Knowledge Base**: Obsidian markdown vault with wikilinks, tags, and YAML frontmatter.
- **Data & Spreadsheet Tracking**: Google Sheets (used for daily calorie/macro logging and longitudinal data tracking).
- **Agentic Execution Engines**: Google Antigravity (Gemini 3 Pro), Claude Code, Cursor, or Codex CLI operating on PowerShell backend.

---

## 3. Workflow Catalog

| Workflow Spec | Associated Trigger | Package | Cadence & Trigger Type | Checkpoint Strategy |
|---|---|---|---|---|
| [`prompt-deconstruction-loop.md`](prompt-deconstruction-loop.md) | `:prompt-deconstruct` | `prompts` | Event-driven (Prompt authored or flagged) | **Push Right**: Only fires upon convergence ($\le 5\%$ improvement) or academic blocker. |
| [`life-management-system.md`](life-management-system.md) | `:prod-life-system` | `productivity` | Periodic (Quarterly audit, annual reset) | **Milestone**: Approves department structure & log schema after 5-question interview blocks. |

---

## 4. Where and How to Use the Workflows

You can execute and interact with these workflows across four primary environments:

### A. Directly in Any AI Chat Interface via Espanso Triggers
Every workflow is bound to an ergonomic Espanso trigger. You can fire them in any text field across Windows (ChatGPT, Claude.ai, Gemini, Cursor, Obsidian, email, terminal):

1. **Prompt Stress-Testing & Deconstruction (`:prompt-deconstruct`)**:
   - Type `:prompt-deconstruct` anywhere.
   - An Espanso popup dialog appears. Paste or type your candidate prompt into `target_prompt`.
   - The expanded template instructs the AI to run the 3 Adversarial Tests (Precision, Intelligence, Challenge) with continuity proofs and rollback protection.
2. **Life Management Onboarding (`:prod-life-system`)**:
   - Type `:prod-life-system` into an active AI chat.
   - The AI begins a structured interview in 5-question blocks calibrated for low cognitive load, checking in on fatigue at each boundary before synthesizing your department logs.
3. **Calorie & Macro Logging (`:prod-macro-sheet`)**:
   - Type `:prod-macro-sheet` to open an interactive configuration form.
   - Pre-fill your daily calories, protein, carbs, fat, and fiber targets to scaffold or instruct a food-logging session with real-time budget warnings.
4. **Metacognition & Year Review (`:think-existential`, `:think-year-review`)**:
   - Type directly into chats where the AI already has extensive conversational history with you to generate deep psychological portraits or annual reflection syntheses.

### B. Inside Your Obsidian Vault
Because this repository is nested directly within your Obsidian vault:

- **Wikilinking**: Link workflow specs directly within your daily notes, project canvases, or MOCs (e.g. `[[_workflows/prompt-deconstruction-loop]]` or `[[_workflows/life-management-system]]`).
- **Department Log Housing**: When executing `life-management-system.md`, designate an Obsidian folder (e.g., `logs/` or `departments/`) to store the generated Markdown logs (such as `health-log.md`, `finance-log.md`).

### C. Delegating to Autonomous AI Agents (Antigravity, Claude Code, Cursor)
The workflow markdown files are written as deterministic runbooks for autonomous agents. Instead of running prompts manually, delegate the entire loop:

- **In Antigravity or Agent Chat**:
  > *"Read `_workflows/prompt-deconstruction-loop.md` and execute it autonomously on our system instructions in `prompts/package.yml`. Stop only when you reach the Stage 4 Termination Checkpoint and present the brief."*
- **In Claude Code / Terminal**:
  > *"Execute the workflow in `_workflows/prompt-deconstruction-loop.md` targeting `draft_prompt.txt`. Enforce continuity proofs and output only the final decision brief."*

The agent will execute all intermediate stages, perform rollback checks on hallucinations, and only interrupt you at the **push-right checkpoint**.

### D. Spreadsheets & External Data Integrations
For workflows tracking tabular or numerical state (such as `:prod-macro-sheet`):
- Connect Google Drive / Sheets to your AI chat (e.g. ChatGPT Google Drive tool).
- Expand `:prod-macro-sheet` to establish automated date-stamped sheet generation (`YYYY-MM-DD`) and track running macronutrient deficits.

---

## 5. Authoring New Workflows: Definition of Done

When authoring future workflow specifications in this folder:

1. **No Unresolved Questions**: A workflow spec is done when an implementer agent can run it without asking a single clarification question.
2. **Explicit Trigger & Checkpoint**: Always define whether the loop is event-driven or scheduled, and explicitly state what the checkpoint brief displays.
3. **Push Right Discipline**: Never include checkpoints on routine sub-steps; push human involvement to the decision threshold.
4. **Link to Espanso**: If the workflow has an interactive user entry point, create a companion trigger in the appropriate package (`prompts`, `thinking-prompts`, `productivity`, etc.) and bump the package manifest version.

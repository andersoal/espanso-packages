# Matt Pocock Skills Pack (`mattpocock-skills`)

Espanso expansion package for workflows and skills inspired by [mattpocock/skills](https://github.com/mattpocock/skills).

Provides **Dual-Mode** execution for every engineering prompt — completely OS- and environment-agnostic:
1. **⚡ Direct Text Replacement (`:...`)**: Instant in-chat prompt expansion without modal dialogs.
2. **📋 Interactive Form Dialog (`:-form` or `:f-...`)**: Pops up a structured dialog with text areas and dropdowns when you want to supply structured inputs.

---

## 🛠️ Triggers Reference (Direct & Form Modes)

| Direct Trigger | Form Dialog Trigger | Name | What it Does / Form Inputs |
|---|---|---|---|
| `:grill` (or `:grill-me`, `:grilling`, `:grill-docs`) | `:grill-form` (or `:grill-me-form`, `:grilling-form`, `:f-grill`) | **Relentless Plan & Design Grilling** | Attacks assumptions, failure modes, scalability traps, docs & specs (Inputs: Context, Proposal, Mode & Focus dropdown) |
| `:implement` (or `:build`) | `:implement-form` (or `:f-implement`) | **Step-by-Step Implementation** | Step-by-step implementation against specification with tests (Inputs: Goal, Context, Constraints) |
| `:tdd` (or `:tdd-loop`) | `:tdd-form` (or `:f-tdd`) | **TDD Workflow** | Red-Green-Refactor loop protocol (Inputs: Goal, Test Framework dropdown, Files) |
| `:refactor` (or `:refactor-plan`) | `:refactor-form` (or `:f-refactor`) | **Refactoring Plan** | Safe incremental refactor plan with tiny verifiable commits (Inputs: Current Code, Target Architecture) |
| `:review` (or `:codereview`, `:code-review`) | `:review-form` (or `:f-review`) | **Dual-Axis Code Review** | Dual-axis review: Spec Alignment & Code Standards / Modularity (Inputs: Scope Target, Spec, Diff) |
| `:diag` (or `:diagnose`, `:debug`) | `:diag-form` (or `:f-diag`) | **Bug Diagnosis** | Systematic hypothesis testing and minimal verification probes before fixing (Inputs: Symptom, Expected, Repro, Context) |
| `:design` (or `:design-api`, `:design-ui`) | `:design-form` (or `:f-design`) | **API / Interface Design** | Explores 2-3 radically different designs ("Design it twice") with trade-offs (Inputs: Responsibility, Callers, Constraints) |
| `:improve-arch` (or `:architecture`) | `:improve-arch-form` (or `:f-arch`) | **Improve Architecture** | Identifies coupling, leaky abstractions, and creates deep module boundaries (Inputs: Current Code, Goals) |
| `:proto` (or `:prototype`) | `:proto-form` (or `:f-proto`) | **Throwaway Prototype** | Minimal prototype to validate hypotheses or API feel (Inputs: Hypothesis, Interaction Flow) |
| `:conflicts` (or `:resolve-conflicts`) | `:conflicts-form` (or `:f-conflicts`) | **Conflict Resolution** | Synthesizes intent of both branches without semantic regressions (Inputs: Files, Incoming Changes, Base Changes) |
| `:wait-what` (or `:challenge`) | `:wait-what-form` (or `:f-wait-what`) | **Assumption Challenger** | Challenges confusing decisions and finds simpler alternative approaches (Input: Proposal) |
| `:teach` (or `:learn`, `:lesson`) | `:teach-form` (or `:f-teach`) | **Structured Teaching Framework** | Progressive learning in Zone of Proximal Development (Inputs: Topic, Mission, Level dropdown, Focus dropdown) |
| `:glossary` (or `:vocab`) | `:glossary-form` (or `:f-glossary`) | **Canonical Glossary Entry** | Tight 1-2 sentence definition + "_Avoid_" list for ubiquitous language (Inputs: Term, Domain, Draft) |
| `:record` (or `:learning-record`) | `:record-form` (or `:f-record`) | **Learning Record** | Breakthrough insight, non-obvious learnings, future implications (Inputs: Insight, Non-Obvious, Implications) |
| `:domain-modeling` (or `:domain`) | `:domain-modeling-form` (or `:f-domain`) | **Domain Modeling** | Domain entities, boundary invariants, and canonical vocabulary (Inputs: Domain, Concepts, Rules) |
| `:wayfinder` (or `:wf`) | `:wayfinder-form` (or `:f-wayfinder`) | **Wayfinder Breakdown** | Decomposes large initiatives into an investigation ticket graph (Inputs: Goal, Constraints) |
| `:spec` (or `:to-spec`, `:prd`) | `:spec-form` (or `:f-spec`) | **Technical Specification / PRD** | Transforms discussions into a structured technical PRD (Inputs: Overview, Requirements, Constraints) |
| `:tickets` (or `:to-tickets`, `:tasks`) | `:tickets-form` (or `:f-tickets`) | **Actionable Task Breakdown** | Decomposes specs into small, testable, verifiable tickets (Inputs: Spec, Order) |
| `:questionnaire` (or `:to-questionnaire`) | `:questionnaire-form` (or `:f-questionnaire`) | **Requirements Questionnaire** | Structured questions to eliminate ambiguity and extract requirements (Inputs: Idea, Audience) |
| `:triage` | `:triage-form` (or `:f-triage`) | **Issue & Bug Triage** | Categorizes and prioritizes reported bugs and issues (Input: Issues list) |
| `:wizard` (or `:guide`) | `:wizard-form` (or `:f-wizard`) | **Step-by-Step Task Wizard** | Step-by-step guidance protocol through complex workflows (Inputs: Task, Starting Point) |
| `:handoff` (or `:session-handoff`) | `:handoff-form` (or `:f-handoff`) | **Session Handoff** | Compact summary of completed work, state, blockers, and next steps (Inputs: Objective, Completed, State, Next Steps, Touchpoints) |
| `:askmatt` (or `:ask-matt`) | `:askmatt-form` (or `:f-askmatt`) | **Ask Matt Style Q&A** | High-clarity mental models, concrete comparisons, and trade-offs (Inputs: Topic, Context, Focus dropdown) |
| `:audit` (or `:skill-audit`) | `:audit-form` (or `:f-audit`) | **Skill & Prompt Auditor** | Audits prompt/skill against trigger reliability, context efficiency & leverage (Inputs: Skill Name, Content) |
| `:write-agents` (or `:writing-for-agents`) | `:write-agents-form` (or `:f-write-agents`) | **Writing Prompts for Agents** | Formats prompts with clean Markdown sections and deterministic constraints (Inputs: Objective, Draft) |
| `:research` (or `:investigate`) | `:research-form` (or `:f-research`) | **Primary Source Research** | Grounded primary source investigation protocol (Inputs: Topic, Context) |
| `:setup-skills` | `:setup-skills-form` (or `:f-setup-skills`) | **Setup Agent Skills** | Structure modular, portable skill repositories and prompt libraries (Inputs: Stack, Workflows) |
| `:regex` (or `:pattern`) | `:regex-form` (or `:f-regex`) | **Regex Crafter & Extractor** | Complete regex design, component breakdown, and flags (Inputs: Goal, Engine dropdown, Samples, Captures) |
| `:shell` (or `:bash`, `:script`) | `:shell-form` (or `:f-shell`) | **Shell & Script Generator** | Safe, portable script generation with error handling (Inputs: Task, Shell Type dropdown, Inputs) |
| — | `:trigger` (or `:make-trigger`, `:new-trigger`, `:trigger-form`) | **Espanso Trigger Creator** | Interactive dialog for creating new Espanso triggers (Inputs: Trigger Text, Replace Text, Type dropdown, Word Boundary dropdown) |

---

## 🚀 Installation & Reload

To apply changes immediately:
```powershell
espanso restart
```

# Engineering & Agent Skills Pack (`engineering`)

A comprehensive Espanso expansion package for software engineers, systems architects, and AI agent workflows.

This package combines standard engineering shortcuts, code generators, and architectural audit templates with advanced **Agent Skills** (inspired by Matt Pocock's workflows) supporting both **Direct Text Replacement** and **Interactive Form Dialogs**.

---

## ⚡ Agent Skills & Advanced Engineering Workflows

Every agent skill provides **Dual-Mode** execution:
1. **⚡ Direct Text Replacement (`:...`)**: Instant in-chat prompt expansion without modal dialogs.
2. **📋 Interactive Form Dialog (`:-form` or `:f-...`)**: Structured form dialog with text areas and dropdowns.

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

## 🛠️ Core Engineering & Coding Prompts

### Architecture, Planning & Audits
- `:p-audit` — Project architecture, technical debt & security audit form.
- `:p-vault` — Project memory & context vault generator.
- `:p-parallel` — Parallel multi-agent delegation prompt.
- `:p-navigate` — Reasoning depth & strategy navigator.
- `:c-archreview` — System architecture scalability review form.
- `:system-design-impl` — Scalable system architecture and MVP design prompt.
- `:architecture-reconstruction` — Staff-level architecture reconstruction and modularization.
- `:repo-understanding-refactor` / `:codebase-refactoring` — Unfamiliar codebase onboarding & architectural refactor.

### Code Quality, Review & Debugging
- `:c-review` — Senior engineer code review & quality audit.
- `:c-debug` — Root cause step-by-step debugging breakdown.
- `:c-refactor` — Clean code refactoring without changing functionality.
- `:c-unittests` / `:c-integtests` — Comprehensive unit and integration test suite generators.
- `:c-optimize` / `:c-reactopt` / `:performance-optimization` / `:perf-opt` — Performance bottleneck pinpointing and optimization.
- `:c-secaudit` / `:c-secscanpipeline` — Security vulnerability scanning and automated pipeline design.
- `:c-errorhandle` — Resilient error handling and defensive programming.
- `:debugging-engineer` — Production bug diagnostic engineer persona prompt.

### Full-Stack, Backend & Frontend Development
- `:feature-developer` — Senior software engineer full feature specification and plan.
- `:app-from-scratch` — Full-stack MVP application generator.
- `:ui-component-developer` — Accessible, reusable UI component architect.
- `:api-development` / `:c-endpoint` — Clean REST API architecture and endpoint generator.
- `:c-sqlopt` / `:c-schema` / `:c-migration` — SQL optimizer, schema design, and safe migration scripts.
- `:c-auth` — JWT authentication, signup/login, and protected middleware design.
- `:c-cicd` / `:c-releasemanage` — CI/CD pipeline and automated release management.
- `:c-ratelimit` / `:c-retry` — Rate limiting and exponential backoff retry patterns.
- `:c-statemachine` / `:c-cli` / `:c-healthcheck` — State machine, CLI tool, and health check probes.
- `:c-tots` — JavaScript to TypeScript migration.

### AI Systems & LLM Engineering
- `:c-aiagent` / `:c-multiagent` / `:multi-agent-workflow` — Multi-agent system architecture and 4-agent dev workflows.
- `:c-rag` — Retrieval Augmented Generation system pipeline design.
- `:c-promptchain` / `:c-sysprompt` / `:c-evalprompt` / `:c-templatelib` — Prompt engineering, system prompts, and evaluations.
- `:c-extract` / `:c-enrich` / `:c-docpipeline` — Structured JSON extraction and intelligent document pipelines.
- `:c-aimonitor` / `:c-aieval` / `:c-feedbackloop` / `:c-hitl` — LLM observability, evaluation matrices, and human-in-the-loop workflows.
- `:c-voiceai` / `:c-sentiment` / `:c-recsys` / `:c-anomaly` / `:c-trenddetect` — Specialized ML/AI applications.
- `:pdf-summary` — One-page executive brief summarizer for complex technical PDFs.
- `:interactive-tools` — Interactive web calculator/tool architect with HTML/JS/CSS.

---

## 🚀 Installation & Reload

To apply changes immediately in Espanso:
```powershell
espanso restart
```

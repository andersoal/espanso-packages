# Workflow: Life Management System (LMS) Design & Maintenance Loop

## 1. Overview & Loop Definition
An architectural interview and operational scaffolding loop designed to establish or audit personal life management systems. It breaks personal complexity into specialized departments, enforces low cognitive load through structured inquiry batches, and delivers lightweight log file schemas tailored to current technical competency.

- **Loop Cadence**: Periodic (Quarterly audit, annual life reset, or major role transition).
- **Implementer Target**: AI Life Strategist or Personal Operations Agent.

---

## 2. Trigger
- **Type**: Event
- **Firing Condition**: User invokes the system initialization trigger `:prod-life-system` or requests an operational review of personal domains.

---

## 3. Workflow Pipeline & Stages

### Stage 1: Low Cognitive Load Inquiry Batches
- **Protocol**:
  - The agent conducts an interview in blocks of exactly 5 questions.
  - Questions are presented one by one, each formatted to minimize cognitive strain (concrete multiple choices, yes/no with elaboration, or single-phrase answers).
- **Fatigue Gate**:
  - After every 5th question, pause and check: *"Are you experiencing decision fatigue, or ready for another 5 questions?"*
  - If user pauses or stops, transition directly to Stage 2 with gathered context.

### Stage 2: Department Synthesis & Domain Modeling
Group revealed activities, obligations, and goals into distinct organizational departments:
- **Common Department Archetypes**:
  - Operations & Logistics (Home, admin, scheduling)
  - Health & Vitality (Nutrition, fitness, sleep, medical)
  - Financial Architecture (Cash flow, investments, taxes)
  - Career & Craft (Core skill development, high-leverage projects)
  - Relationships & Community (Family, key partnerships, social circle)
  - Personal Growth & Exploration (Hobbies, philosophy, metacognition)

### Stage 3: Log File Specification
For each confirmed department:
- Define a single Markdown-based log file (e.g. `logs/<department>-log.md`).
- Specify a minimal schema:
  - Header: Department mission statement & primary metric.
  - Quick-capture table: Date, event/interaction, outcome, next action.
  - Review cadence: Weekly or monthly check-in prompt.

### Stage 4: Technical Competency Calibration
- Inspect and constrain the tooling requirements:
  - If technical skill is non-programming: Keep entirely within plain Markdown files, Obsidian notes, or Google Sheets.
  - If technical skill is advanced: Enable CLI automation, API hooks, or local scripts.

---

## 4. Checkpoint (Push Right)
- **Placement**: Staged once after Stage 3 & 4 are drafted.
- **Checkpoint Brief**:
  - **Proposed Department Map**: 4-6 departments with 1-line mission statements.
  - **Log Schemas**: Minimal templates ready to instantiate.
  - **Recommended Tooling**: Tool selection matching user competency.
  - **Decision Needed**: Approve architecture, merge/split departments, or adjust review cadence.

---

## 5. Associated Espanso Shortcut
- **Trigger**: `:prod-life-system` (located in `productivity/package.yml`)

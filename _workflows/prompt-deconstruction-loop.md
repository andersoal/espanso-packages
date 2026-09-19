# Workflow: Prompt Deconstruction & Adversarial Improvement Loop

## 1. Overview & Loop Definition
A recurring quality-assurance loop for mission-critical prompts and agent system instructions. It subjects target prompts to three adversarial stress tests, verifies self-consistency, enforces hallucination guards via continuity proofs, and isolates incremental value deltas before finalizing.

- **Loop Cadence**: On-demand / Event-driven.
- **Implementer Target**: Frontier reasoning LLM or automated prompt engineering agent.

---

## 2. Trigger
- **Type**: Event
- **Firing Condition**: A prompt is authored, flagged as brittle/underspecified, or yields inconsistent outputs in production.

---

## 3. Workflow Pipeline & Stages

### Stage 1: Ingestion & Boundary Analysis
- **Inputs**:
  - `target_prompt`: The candidate prompt text under review.
  - `domain_constraints`: Any non-negotiable operational boundaries, schemas, or latency targets.
- **Checks**:
  - Verify syntax, bracket balance, and placeholder naming (`snake_case`).

### Stage 2: The Three Adversarial Tests
Execute an iterative refinement pass on the candidate prompt:
1. **Precision Test**:
   - Identify ambiguities exploitable under $\ge 2$ distinct adversarial interpretations.
   - For every ambiguity found, draft at least one concrete counter-example and propose clarified wording.
2. **Intelligence Test**:
   - Formulate a self-referential consistency proof demonstrating that internal rules do not conflict or produce deadlocks.
3. **Challenge Test**:
   - Invert $\ge 1$ core assumption from previous iterations.
   - Constraint: Inversions must alter assumptions within constraints without weakening or deleting hard requirements.

### Stage 3: Safeguards & Continuity Proof
Before committing any iteration:
- **Inheritance Check**: Ensure all rules from prior iterations are preserved unless explicitly superseded.
- **Hallucination Fail-Safe**:
  - Validate all refinements against prior source context; replace ungrounded inferences with `[Unverified: requires clarification]`.
  - Compile the **Continuity Proof**:
    - *Characters / Entities*: Identity and role consistency.
    - *Timeline*: Chronological and causal validity.
    - *Rules / Constraints*: Strict compliance with all accumulated boundaries.
    - *Setting / World*: Environmental and system consistency.
- **Rollback Condition**: If a hallucination or rule regression is detected, immediately revert to the last valid iteration state.

### Stage 4: Convergence & Termination Criteria
Continue iterations until one of the following termination conditions is met:
1. **Convergence**: Three consecutive iterations show $\le 5\%$ net improvement across precision, intelligence, and challenge metrics (with quantitative justifications).
2. **External Boundary**: Resolving remaining flaws requires external domain/academic expertise outside context.

---

## 4. Checkpoint (Push Right)
- **Placement**: Pushed fully to the right — the human is **not** interrupted during intermediate test cycles or rollback adjustments.
- **Trigger**: Fired only upon meeting a Termination Criterion.
- **Checkpoint Brief**:
  - **Status**: Completed / Converged or Terminated with external blocker.
  - **Iterations Completed**: Total cycles run.
  - **Summary of Tradeoffs**: A compact matrix comparing the original prompt vs. refined candidate.
  - **Continuity Proof Status**: Passed / Verified.
  - **Action Required**: Accept proposed prompt or reject with guidance.

---

## 5. Associated Espanso Shortcut
- **Trigger**: `:prompt-deconstruct` (located in `prompts/package.yml`)

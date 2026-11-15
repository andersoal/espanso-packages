# Thinking Prompts

A curated collection of 10 AI-powered metacognition and self-reflection prompts designed to sharpen your thinking, expose blind spots, and accelerate self-awareness.

Inspired by [SAINT NULL's Thinking Toolkit](https://www.tiktok.com/@saint.null).

## The 10 Prompts

| Trigger | Name | Purpose |
|---------|------|---------|
| `:think-snap` | Snap Awakening | Fresh perspective on recurring problems |
| `:think-mirror` | Mirror My Mind | Analyze your thinking patterns and biases |
| `:think-destroy` | Destroy My Idea | Build the strongest case against your beliefs |
| `:think-borrow` | Borrow 5 Brains | 5 expert perspectives on your problem |
| `:think-learn` | Learning Cheat Code | Focused, high-impact skill acquisition plan |
| `:think-blocks` | Find My Blocks | Identify and remove self-sabotage patterns |
| `:think-insight` | Insight Finder | Break any topic into 5 non-obvious insights |
| `:think-decode` | Decode Actions | Reveal hidden drivers behind your behavior |
| `:think-vision` | Visionary Thinking | How bold thinkers would approach your challenge |
| `:think-blind` | Blind Spot Exposer | Challenge your logic, expose biases, reframe |
| `:think-existential` | Existential Analysis | Transversal psychological analysis & rupture scenario |
| `:think-year-review` | Annual AI Reflection | Yearly conversation growth, patterns, and blind spots |

## How to Use

Each trigger expands into a structured prompt you can paste into any AI chat or assistant interface.

- **Interactive forms** (`:think-snap`, `:think-destroy`, `:think-borrow`, `:think-learn`, `:think-blocks`, `:think-insight`, `:think-decode`, `:think-vision`, `:think-blind`) will open a dialog asking for your specific context.
- **Static prompts** (`:think-mirror`, `:think-existential`, `:think-year-review`) work immediately based on conversation history.

## When to Use

| Situation | Trigger |
|-----------|---------|
| Stuck on a recurring problem | `:think-snap` or `:think-borrow` |
| Want to understand how you think | `:think-mirror` |
| Need a raw, transversal psychological profile | `:think-existential` |
| Year-end or annual review of your AI conversations | `:think-year-review` |
| Need to stress-test a belief | `:think-destroy` or `:think-blind` |
| Feeling blocked or stuck | `:think-blocks` or `:think-decode` |
| Want to learn something fast | `:think-learn` |
| Need deeper understanding | `:think-insight` |
| Need bold, unconventional moves | `:think-vision` |

## Installation

```bash
espanso install thinking-prompts
```

Or clone/copy this package into your `espanso/match/` directory.

## Regex Variants (Inline Quick-Fire)

Instant expansion without opening a form dialog:

| Trigger | Example |
|---------|---------|
| `:think-snap(problem)` | `:think-snap(I keep procrastinating)` |
| `:think-destroy(topic)` | `:think-destroy(remote work is better)` |
| `:think-borrow(idea)` | `:think-borrow(my startup idea)` |
| `:think-learn(skill)` | `:think-learn(DataWeave 2.0)` |
| `:think-blocks(area)` | `:think-blocks(my career)` |
| `:think-insight(topic)` | `:think-insight(AI in healthcare)` |
| `:think-decode(problem)` | `:think-decode(conflict with manager)` |
| `:think-vision(person,challenge)` | `:think-vision(Steve Jobs,new market)` |
| `:think-blind(topic)` | `:think-blind(quitting my job)` |

## Chain Triggers (Multi-Step Workflows)

- **The Decision Forge** (`:think-chain-decide` → `-2` → `-3`): Clarify → Stress-Test → Commit
- **The Insight Pipeline** (`:think-chain-master` → `-2` → `-3`): Deconstruct → Stress-Test → Integrate
- **The Problem Breaker** (`:think-chain-solve` → `-2` → `-3` → `-4`): Reframe → Decode → Multiply → Execute

## Cross-Package Synergy & Help

| Trigger | Purpose | Integration |
|---------|---------|-------------|
| `:think-decide` / `:think-decide-quick` | Reflective decision protocol | `:djlog` (`decision-journal`) |
| `:think-strategize` / `:think-innovate` | Multi-lens strategy & ideation | `social-strategy` |
| `:think-accelerate` / `:think-teachback` | Rapid learning & Feynman check | `learn-*` triggers |
| `:think-productivity` | Procrastination unlock | `prod-*` triggers |
| `:think-weekly` | Weekly reflection ritual | `:djlog` + `:djreview` |
| `:think-help` | Quick reference card | Self-contained |

## Package Info

- **Name**: `thinking-prompts`
- **Version**: 1.2.0
- **Author**: Anderson Guarnier da Silva

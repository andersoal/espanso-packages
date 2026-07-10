# Thinking Prompts

A curated collection of AI-powered metacognition and self-reflection prompts for deeper thinking, blind spot detection, and cognitive improvement.

**Source:** SAINT NULL's Thinking Toolkit
**Version:** 1.1.0

---

## What's Inside

### Core 10 Prompts

The foundational set of thinking prompts, each available as an interactive form:

| # | Prompt | Trigger | Purpose |
|---|--------|---------|---------|
| 1 | **Snap Awakening** | `:think-snap` | Break out of recurring problem loops |
| 2 | **Mirror My Mind** | `:think-mirror` | Analyze your thinking patterns and biases |
| 3 | **Destroy My Idea** | `:think-destroy` | Stress-test your beliefs |
| 4 | **Borrow 5 Brains** | `:think-borrow` | Get expert perspectives on any problem |
| 5 | **Learning Cheat Code** | `:think-learn` | Create focused learning plans |
| 6 | **Find My Blocks** | `:think-blocks` | Identify self-sabotage patterns |
| 7 | **Insight Finder** | `:think-insight` | Extract non-obvious insights from any topic |
| 8 | **Decode Actions** | `:think-decode` | Reveal hidden drivers behind behavior |
| 9 | **Visionary Thinking** | `:think-vision` | Channel bold thinkers for unconventional approaches |
| 10 | **Blind Spot Exposer** | `:think-blind` | Audit your logic and assumptions |

### Inline Variants (Regex)

For speed demons -- no forms, just instant expansion with your argument inline:

```
:think-snap(I keep procrastinating)
:think-destroy(remote work is better)
:think-borrow(my startup idea)
:think-learn(DataWeave 2.0)
:think-blocks(my career)
:think-insight(AI adoption in healthcare)
:think-decode(my conflict with my manager)
:think-vision(Steve Jobs, entering a new market)
:think-blind(I should quit my job)
```

### Multi-Step Thinking Chains

Structured workflows for deep thinking sessions:

| Chain | Triggers | Steps | Purpose |
|-------|----------|-------|---------|
| **Decision Forge** | `:think-chain-decide` + `-2` + `-3` | 3 | Rigorous decision-making protocol |
| **Insight Pipeline** | `:think-chain-master` + `-2` + `-3` | 3 | Deep topic mastery workflow |
| **Problem Breaker** | `:think-chain-solve` + `-2` + `-3` + `-4` | 4 | Complete problem resolution |

### Cross-Package Synergy

Triggers that bridge with other packages for integrated workflows:

| Trigger | Partners With | Workflow |
|---------|---------------|----------|
| `:think-decide` | `:djlog`, `:djreview` | Think -> Decide -> Log -> Review |
| `:think-decide-quick` | `:djlog` | Compressed decision audit |
| `:think-strategize` | social-strategy, marketing-sales | Multi-lens strategic analysis |
| `:think-innovate` | social-strategy | Breakthrough idea generation |
| `:think-accelerate` | `:learn-*` | Accelerated learning protocol |
| `:think-teachback` | `:learn-*` | Feynman comprehension check |
| `:think-productivity` | `:prod-*` | Procrastination unlock sequence |
| `:think-weekly` | `:djlog`, `:djreview` | Complete weekly reflection ritual |

### Quick Reference

Type `:think-help` anytime to see all available triggers.

---

## Installation

```bash
espanso install thinking-prompts
```

Or manually copy the `thinking-prompts` folder to your espanso configuration directory.

---

## Requirements

- [Espanso](https://espanso.org/) >= 2.0

---

## License

MIT

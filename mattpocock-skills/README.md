# Matt Pocock Skills Pack (`mattpocock-skills`)

Espanso expansion package for workflows and skills inspired by [mattpocock/skills](https://github.com/mattpocock/skills).

Provides clean interactive form templates and double-slash command shortcuts for agent sessions.

---

## 📋 Interactive Prompt Forms

Type any of the clean `:` triggers to open a popup dialog with structured inputs:

| Trigger | Name | Description |
|---|---|---|
| `:teach` (or `:learn`, `:lesson`) | **Structured Teaching Framework** | Topic, real-world mission, level dropdown, focus dropdown (ZPD, Storage Strength) |
| `:glossary` (or `:vocab`) | **Canonical Glossary Entry** | Term, domain, definition rules (tight 1-2 sentence definition + "_Avoid_" list) |
| `:learning-record` (or `:record`) | **Learning Record** | Breakthrough insight, non-obvious learnings, future implications |
| `:tdd` (or `:tdd-loop`) | **TDD Workflow** | Goal, test framework dropdown (Vitest, Jest, Playwright, Pytest, etc.), file paths |
| `:grill` (or `:grill-me`) | **Grill Me** | Context, proposal, focus area dropdown (Modularity, Scalability, Edge Cases, etc.) |
| `:review` (or `:codereview`) | **Dual-Axis Review** | PR target, original spec, and code diff to review |
| `:diag` (or `:diagnose`) | **Bug Diagnosis** | Observed error, expected behavior, reproduction steps, suspected files |
| `:wayfinder` (or `:wf`) | **Wayfinder Breakdown** | High-level goal, known constraints, ticket graph decomposition |
| `:refactor` (or `:refactor-plan`) | **Refactoring Plan** | Current code, target architecture, safe commit breakdown |
| `:design` (or `:design-api`) | **API / Interface Design** | Responsibility, caller context, 3 radical interface designs ("Design it twice") |
| `:handoff` (or `:session-handoff`) | **Session Handoff** | Objective, completed tasks, state/blockers, immediate next steps |
| `:askmatt` (or `:ask-matt`) | **Ask Matt Style Q&A** | Topic / question, code context, clear mental model explanation |
| `:audit` (or `:skill-audit`) | **Skill Auditor** | Skill name, content, trigger/context/leverage checklist |

---

## ⚡ Quick Agent Command Shortcuts (`//...`)

Type these double-slash shortcuts when you just want the fast slash command in agent chats:

| Trigger | Expansion | Purpose |
|---|---|---|
| `//teach` | `/teach ` | Multi-session workspace teaching loop |
| `//tdd` | `/tdd ` | Test-driven development loop |
| `//review` | `/review ` | Dual-axis review (Standards & Spec) |
| `//code-review` | `/code-review ` | Comprehensive code review |
| `//grill` | `/grill-me ` | Stress-test plans & architecture |
| `//diag` | `/diagnosing-bugs ` | Systematic bug diagnosis protocol |
| `//wayfinder` | `/wayfinder ` | Large-scale task graph decomposition |
| `//refactor` | `/request-refactor-plan ` | Safe incremental refactor RFC |
| `//design` | `/design-an-interface ` | Explore multiple radical API designs |
| `//domain` | `/domain-modeling ` | Domain modeling & ubiquitous language |
| `//proto` | `/prototype ` | Throwaway design prototype |
| `//qa` | `/qa ` | Interactive QA & bug filing |
| `//handoff` | `/claude-handoff ` | Session state handoff summary |
| `//research` | `/research ` | High-trust primary source investigation |
| `//audit` | `/skill-auditor ` | Audit and health-check agent skills |
| `//prd` | `/to-prd ` | Turn notes / discussions into PRD |
| `//issues` | `/to-issues ` | Convert PRD / specs into issues |
| `//ask-matt` | `/ask-matt ` | High-clarity TypeScript / architecture Q&A |

---

## 🚀 Installation & Reload

To apply changes immediately:
```powershell
espanso restart
```

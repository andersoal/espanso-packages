# Genealogy & Family Tree AI Prompts

A comprehensive Espanso package of AI prompts and workflows for genealogists and family history researchers. Turn half-remembered names into structured family trees, trace surname etymology, locate free public records, break through brick-wall ancestors, and generate visual and data-ready tree structures.

---

## 🌳 Included Prompts & Workflows

### 1. The 4-Step AI Roots Method
| Trigger | Name | Purpose |
|---|---|---|
| `:gen-dump` / `:gen-braindump` | Brain Dump Interview | Step 1: Let AI interview you branch-by-branch to capture names, places, and years |
| `:gen-origin` / `:gen-surname` | Surname Origins | Step 2: Trace surname meaning, linguistic roots, and historic migrations |
| `:gen-leads` / `:gen-search` | Find Records & Leads | Step 3: Search free public records (FamilySearch, Find a Grave, obits, census) |
| `:gen-visual` / `:gen-tree` | Visual Tree & GEDCOM | Step 4: Generate visual generation hierarchy + GEDCOM export format |

### 2. Deep Investigation & Discovery
| Trigger | Name | Purpose |
|---|---|---|
| `:gen-timeline` | Family Timeline | Build a chronological generation timeline and pinpoint gaps |
| `:gen-branches` | Hidden Branches | Identify forgotten relatives, name variations, and remarriages |
| `:gen-migration` | Ancestor Migration Map | Reconstruct generational movement with historical/economic context |
| `:gen-connections` | Hidden Connections | Connect relatives across shared surnames, locations, and jobs |
| `:gen-mystery` | Mystery Investigation | Investigate missing years, name changes, and conflicting records |
| `:gen-story` | Historical Narrative | Turn family facts into a compelling narrative with separated context |
| `:gen-roadmap` | Research Roadmap | Prioritized research plan with target archives and record sets |

### 3. Genealogist Power Tools & Frameworks
| Trigger | Name | Purpose |
|---|---|---|
| `:gen-rtfl` / `:gen-framework` | Prompt Framework | Role–Task–Format–Limits prompt generator with context & challenges |
| `:gen-blindspots` / `:gen-missing` | Blindspot Detector | Ask "What am I missing?" to find overlooked archives & events |
| `:gen-forks` / `:gen-decisions` | Decision Points | Identify key crossroads and strategic decisions in research |
| `:gen-brickwall` / `:gen-wall` | Brick-Wall Breaker | Deep investigation plan for difficult or lost ancestors |
| `:gen-audit` / `:gen-verify` | Fact-Check Audit | Audit AI output: strictly separate CONFIRMED from UNVERIFIED leads |
| `:gen-contact` / `:gen-outreach` | Relative Outreach | Draft a short, warm, low-pressure message to discovered relatives |
| `:gen-improve` / `:gen-prompt` | Prompt Optimizer | Enhance a genealogy prompt with historical context and obstacles |

### 4. Specialized Tree Modeling & Formats
| Trigger | Name | Purpose |
|---|---|---|
| `:gen-dynasty` / `:gen-history-tree` | Dynastic Lineage Tree | Multi-generation historical tree with achievements and context |
| `:gen-ancient-tree` / `:gen-biblical` | Ancient / Biblical Tree | Chronological tree for ancient, mythological, or biblical lines |
| `:gen-cladogram` | Family Cladogram | ASCII evolutionary branching tree (├──, └──) from common ancestor |
| `:gen-json-analyst` | JSON Tree Analyst | System prompt for parsing and traversing nested genealogy JSON |
| `:gen-web-analyst` | Family Webpage Developer | Prompt for building/analyzing interactive family HTML pages |
| `:gen-brandcestry` | Brand Ancestry Tree | Parent-subsidiary corporate hierarchy and brand ancestry spec |

---

## 🚀 Installation & Usage

### 1. Install via Espanso CLI
```bash
espanso install genealogy --git https://github.com/andersoal/espanso-packages --external
```

### 2. Manual Installation
Copy the `genealogy` folder into your Espanso `match/packages/` directory:
```bash
# Windows (mklink)
mklink /D "%APPDATA%\espanso\match\packages\genealogy" "C:\path\to\espanso-packages\genealogy"
```

### 3. Restart Espanso
```bash
espanso restart
```

---

## 📦 Package Info
- **Name**: `genealogy`
- **Version**: 1.0.0

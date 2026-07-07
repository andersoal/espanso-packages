# Trigger Audit — Duplicates & Overlapping Triggers

*Audit date: 2026-07-05. Scope: every `*/package.yml` (739 triggers across 14 packages, `_example-package` excluded).*

The audit found three classes of problems: **exact duplicate triggers** (21 triggers defined 2–3 times, several with conflicting content), **prefix shadowing** (113 pairs where a short trigger without `word: true` fires the moment it is typed, making every longer trigger it prefixes untypeable), and **2 regex patterns declared with the `trigger:` key** (regex matches require the `regex:` key in espanso).

All issues are fixed. The audit now reports: **711 triggers, no duplicates or shadowing.** Re-run it anytime with:

```sh
python3 scripts/check_triggers.py
```

The script exits non-zero on any exact duplicate (unless every copy has a distinct `label`, which espanso disambiguates with a popup) or any prefix-shadowed trigger.

## Where the duplicates came from (git archaeology)

The repo grew by **batch-importing prompt collections** (many converted from screenshots — see the `Source: <hash>.png` comments) into whichever package was being worked on at the time, with no duplicate check. The concrete origins:

| Duplicate class | Introduced by | What happened |
|---|---|---|
| utils ⇄ md-formatting md helpers + punctuation wrappers | `8b5f1c0` (initial packages commit) | Both packages were initialized carrying the same markdown/wrap helpers from day one |
| social-strategy `:p-*` business series | `6ccbf6d` created them in social-strategy; **`9754147`** (2026-06-27, "add new trigger to espanso") re-imported refined rewrites of the same prompts into **prompts** | `9754147` appended **123 triggers** to prompts in one batch — the single biggest source of cross-package conflicts (`:p-market`, `:p-viral`, `:p_negotiate`, `:p-missing`, `:tag`, …) |
| career headless `:pfix`/`:pmatch`/`:pcover` variants | `5184577` ("modularize espanso configuration") | The modularization reshuffle imported experimental "headless" variants alongside the form versions already added by `6ccbf6d` |
| Second `:genius`, `[cite: 1]` markers | `5184577` | Content pasted from an AI chat export carried Gemini-style `[cite: 1]` citation markers (37 occurrences in productivity + prompts) and re-used an existing trigger name |

The `scripts/check_triggers.py` guard now catches all of this at import time — run it after adding any batch of prompts.

## Reorganization: topical prompts moved out of `prompts`

Principle applied: **the generic `prompts` package keeps only general-purpose prompt-engineering templates; anything clearly topical lives in its topical package** — and where a duplicate existed, the better-written survivor is the version that moves.

| Trigger(s) | Moved to | Why |
|---|---|---|
| `:p-market` `:p-problem` `:p-offer` `:p-distro` `:p-viral` `:p-competitor` `:p-scale` | **social-strategy** | The 7-part business-building series originated there (`6ccbf6d`); the refined rewrites return home. Also fixed the misplaced section comments that had drifted inside the previous match's `form_fields` |
| `:pcareer` `:p-decision` `:p-success` `:profile-as-lp` `:ai-interview` | **career** | Career clarity, career decision tree, career/life success, LinkedIn profile rewriter, job-interview simulator — all explicitly career content |
| `:genius-zone` | **marketing-sales** | Niche/monetization framework; fits the `:pniche`/`:poffer` cluster (also stripped `[cite: 1]` markers and an unused `current_date` var) |
| `:p_difficult` | **relationship** | Interpersonal difficult-conversation coach |
| `:p-calendar` | **productivity** | Weekly calendar / time-management prompt |

Content fixes in the same pass: removed all 37 leaked `[cite: 1]` citation markers (productivity, prompts) and the leaked AI-refusal sentence inside social-strategy's `:yt-ideas` prompt.

## Renamed triggers (update your muscle memory)

| Old trigger | New trigger | Package | Why |
|---|---|---|---|
| `:genius` (Zone of Genius monetization) | `:genius-zone` | prompts | Collided with `:genius` (replicate a figure's thinking), which keeps the name |
| `:p-decision` (decision pressure test) | `:p-premortem-decision` | prompts | Collided with `:p-decision` (career decision tree), which keeps the name |
| `:p-missing` (gaps in previous response) | `:p-gaps` | prompts | Collided with `:p-missing` (the ONE insight I'm missing), which keeps the name |
| `:p-schedule` (weekly calendar planner) | `:p-calendar` | prompts | Collided with marketing-sales' `:p-schedule` (posting schedule), which keeps the name |
| `:p_negotiate` (difficult conversation) | `:p_difficult` | prompts | Collided with career's `:p_negotiate` (salary negotiation), which keeps the name |
| `:tag` (Task/Action/Goal framework) | `:p-tag` | prompts | Collided with utils' `:tag` (HTML tag wrapper), which keeps the name |
| `:pstudio(...)` inline variant | `:ps(...)` | content-creation | Converted from broken `trigger:` to `regex:`; renamed so plain `:pstudio` can't fire first |
| `:imgclean(...)` inline variant | `:ic(...)` | content-creation | Converted from broken `trigger:` to `regex:`; renamed so plain `:imgclean` can't fire first |

## Removed triggers

| Trigger(s) | Removed from | Reason |
|---|---|---|
| `:md-code` `:md-collapse` `:md-link` `:html-link` `:bb-link` | utils | Byte-identical copies exist in **md-formatting**, which is their topical home |
| `:((` `:[[` `:{{` `:<<` `` :`` `` `:''` `:""` `:__` `:**` | md-formatting | Produced byte-identical output to utils' single-char wrappers (`:(` `:[` …) and were unreachable whenever both packages were installed |
| `:p-market` `:p-problem` `:p-offer` `:p-viral` `:p-competitor` `:p-scale` | social-strategy | Conflicted with the **prompts** versions, which are refined rewrites of the same prompts (more structured output specs); prompts versions kept |
| `:p-dist` | social-strategy | Same concept as prompts' `:p-distro` (30-day distribution plan), which is the refined version |
| `:pfix` ×1, `:pmatch` ×2, `:pcover` ×2 ("headless" variants) | career | Unlabeled duplicates of the form-based versions, containing unfilled placeholders (`YOUR_NAME_HERE`, `/path/to/your/vault/Master_Resume.md`); the interactive form versions kept |

## `word: true` added (prefix shadowing fix)

Without `word: true`, espanso expands a trigger the instant its last character is typed, so a short trigger makes every longer trigger it prefixes unreachable — e.g. utils' `:b` fired before `:bi`, `:biu`, `:br`, `:btc`, `:bu`, or prompts' `:brainstorm` could ever be typed. With `word: true` the trigger only fires when followed by a word separator (space, punctuation), and since `-` is not a separator, `:prompt-creator` is typeable while `:prompt` + space still expands.

- **utils**: `:b` `:i` `:u` `:bi` `:bu` `:iu` `:biu` `:ci` `:cm` `:br` `:para` `:tag` `:date` and the bracket/quote wrappers `:(` `:[` `:{` `:<` `` :` `` `:'` `:"` `:_` `:*` `:-`
- **prompts**: `:pm` `:prompt` `:gs` `:star` `:mastery` `:chain4` `:genius` `|quality` `:learn-feynman-technique` `:deep-youtube-summary`
- **career**: `:pfit` (shadowed prompts' `:pfitness`)
- **relationship**: `:expert` (shadowed prompts' `:expert-crit`)
- **content-creation**: `:fixlight` (shadowed its own `:fixlighting`), `:imgclean`, `:pstudio`, `:prompt-scale` (shadowed its own `:prompt-scale-fast`)

**Behavior change to be aware of:** these triggers now require a word separator to fire. `:b` + space produces `**|**` (plus the space); `:b` mid-word does nothing. For the cursor-wrap triggers (`:b`, `:(`, …) this is the intended trade-off that makes the longer triggers reachable.

## Kept as-is (intentional)

- `:lorem` ×2 in utils — both copies carry distinct `label`s ("Paragraph" / "Sentence"), so espanso shows a disambiguation popup. This is a supported pattern; the audit script allows it.

## Other observations

- Packages install independently; cross-package conflicts only bite when both packages are installed. This audit treats the repo as one installable set, which is the safest assumption.

## Version bumps

career 0.2.0 · content-creation 0.2.0 · marketing-sales 0.2.0 · md-formatting 1.1.0 · productivity 1.1.0 · prompts 1.3.0 · relationship 0.2.0 · social-strategy 1.1.0 · utils 0.2.0

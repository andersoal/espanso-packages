# Trigger Audit — Duplicates & Overlapping Triggers

*Audit date: 2026-07-05. Scope: every `*/package.yml` (739 triggers across 14 packages, `_example-package` excluded).*

The audit found three classes of problems: **exact duplicate triggers** (21 triggers defined 2–3 times, several with conflicting content), **prefix shadowing** (113 pairs where a short trigger without `word: true` fires the moment it is typed, making every longer trigger it prefixes untypeable), and **2 regex patterns declared with the `trigger:` key** (regex matches require the `regex:` key in espanso).

All issues are fixed. The audit now reports: **711 triggers, no duplicates or shadowing.** Re-run it anytime with:

```sh
python3 scripts/check_triggers.py
```

The script exits non-zero on any exact duplicate (unless every copy has a distinct `label`, which espanso disambiguates with a popup) or any prefix-shadowed trigger.

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

## Other observations (not trigger-related, not fixed here)

- social-strategy's `:yt-ideas(...)` regex replacement contains leaked AI-refusal text mid-prompt: *"Normally I can help with things like this, but I don't seem to have access to that content. You can try again or ask me for something else."* — worth cleaning up.
- Packages install independently; cross-package conflicts only bite when both packages are installed. This audit treats the repo as one installable set, which is the safest assumption.

## Version bumps

career 0.2.0 · content-creation 0.2.0 · md-formatting 1.1.0 · prompts 1.3.0 · relationship 0.2.0 · social-strategy 1.1.0 · utils 0.2.0

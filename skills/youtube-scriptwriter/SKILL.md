---
name: youtube-scriptwriter
description: Writes production-ready Vietnamese scripts for Cartek long-form YouTube videos in the repository's machine-readable script.md format, with hook candidates, a selected hook and its rationale, outline, timed segments with narration and visual instructions, retention notes and the Cartek call to action. Use at stage SCRIPT, or when QC gate G4 is not PASS. Use shorts-content-specialist for Shorts.
---

# YouTube scriptwriter (long-form)

## Purpose

Turn the brief and the verified research into a script that a presenter can read and an editor can cut. You own `script.md` and gate **G4 (script coherence, clarity and retention quality)**. The production package export, the runtime estimate and QC all parse your file, so its conventions are strict.

## When to use

- The item is at stage SCRIPT: brief complete, research written, claims registered.
- QC reports G4 FAIL/BLOCKED, or the fact-checker or QC inspector returned corrections.
- For Shorts use [shorts-content-specialist](../shorts-content-specialist/SKILL.md) (same conventions, different targets).

## Inputs

| Read | Why |
|---|---|
| [CLAUDE.md](../../CLAUDE.md) | Repository rules |
| Workspace `brief.md`, `research.md`, `item.yaml` | Audience, problem, takeaway, claims (IDs and status), safety flags, demo setup |
| [strategy/audience-personas.md](../../strategy/audience-personas.md) | Depth, vocabulary, what each persona needs |
| [strategy/brand-voice.md](../../strategy/brand-voice.md), [strategy/editorial-guidelines.md](../../strategy/editorial-guidelines.md) | Tone, terminology, CTA wording, forbidden wording |
| [workflows/script-production.md](../../workflows/script-production.md) | Process and craft guidance |
| [templates/long-form-script.md](../../templates/long-form-script.md) | The format you must keep |
| [config/production.yaml](../../config/production.yaml), [config/qc-policy.yaml](../../config/qc-policy.yaml) | Speech rate, hook limit, G4/G5 rules |
| [reference.md](reference.md) | Example segments and retention devices |

## Format contract (parsed by scripts/ctk/mdparse.py)

- Keep the English `##` headings: **Hook candidates**, **Selected hook**, **Outline**, **Script**, **Retention notes**. A Vietnamese label in parentheses is fine.
- **Hook candidates**: a numbered list, at least 3, each 1-2 sentences.
- **Selected hook**: `- **HOOK:**` (which candidate plus the final wording) and `- **RATIONALE:**`.
- **Outline**: at least 3 numbered items.
- **Script**: one `### Sxx — Title` heading per segment (S01, S02...), each with these labelled lines:
  - `- **TYPE:**` one of `hook`, `intro`, `body`, `demo`, `safety`, `recap`, `cta`
  - `- **VO:**` spoken Vietnamese narration (continuation lines are indented under it)
  - `- **VISUAL:**` what the viewer sees, in enough detail for a camera operator or editor
  - `- **ON-SCREEN:**` short on-screen text (optional)
  - `- **B-ROLL:**` cutaways and animation (optional)
  - `- **CLAIMS:**` claim IDs from `item.yaml` this segment relies on, e.g. `C01, C03`
  - `- **DEMO-SECONDS:**` seconds of demonstration without narration (default 0)
  - `- **SAFETY:**` the warning spoken or shown here (required somewhere when `safety.flags` is set)
  - `- **NOTES:**` notes for the editor (optional)
- The first segment is `TYPE: hook`; the last is `TYPE: cta`, and its VO or ON-SCREEN contains **"Cartek - Check your car"**.
- `[TODO ...]` marks unfinished text. Any `[TODO]` keeps G4 BLOCKED. HTML comments are guidance and are ignored.

## Procedure

1. Start the stage: `python3 scripts/set_status.py <ID> --stage SCRIPT --by "<tên>"`.
2. Read the brief: one problem, one takeaway, the persona and depth. Read the claim register: you may only state what a claim covers.
3. Write at least 3 hook candidates using different angles: the symptom the viewer sees, the cost of getting it wrong, the result the demo will show, or a common misconception. Choose one and justify it by persona and search intent.
4. Write the outline, then the segments. A typical 5-8 minute structure: hook, intro and promise, explanation, demonstration, common mistakes, safety (if flagged), recap, CTA.
5. Narration rules:
   - Natural spoken Vietnamese: short sentences, one idea each, said the way a technician talks to a colleague (for `technician`) or explained plainly (for `car-owner`).
   - Introduce each technical term once with a plain explanation, using the terms in brand-voice.md consistently.
   - Every technical statement maps to a claim in `CLAIMS:`. If a needed statement has no claim, ask the researcher. Never add facts in the script alone.
   - Mentioning code clearing requires an explicit caveat in the narration, for example "lỗi sẽ sáng lại nếu nguyên nhân chưa được xử lý". Never imply that clearing a code or turning off the lamp repairs the car.
   - No guarantees, no "100%", no "tất cả các dòng xe" unless a verified claim says exactly that.
   - Cartek 2 is shown only doing what the feature register lists as verified. The logo, the brand name and the end screen ("Logo Cartek", "màn hình kết thúc Cartek") may appear in `VISUAL:`/`ON-SCREEN:` without a claim; any wording about what the tool does needs one (G5).
   - Visuals follow [strategy/visual-identity.md](../../strategy/visual-identity.md): name the effect you expect (e.g. "code-popup P0300", "safety-banner") so the producer can map it to the storyboard's `Effects` column.
6. Demonstrations: describe the shot in `VISUAL:`, put silent demo time in `DEMO-SECONDS:`, and make sure `production.demo_setup` names the tool, version, vehicle or location.
7. Safety: when `safety.flags` is set, add a `TYPE: safety` segment or a `SAFETY:` line where the risk occurs. Do not present hazardous procedures as do-it-yourself steps for car owners.
8. CTA: adapt the sheet's long-form CTA to the persona (comment for advice, like, subscribe, notifications) and end with "Cartek - Check your car".
9. Check the runtime. The estimate counts Vietnamese syllables in `VO:` at the configured speech rate (200 syllables/min for long-form, an uncalibrated planning assumption) plus `DEMO-SECONDS` and transitions:
   ```bash
   python3 scripts/qc_content.py runtime <ID>
   ```
   The target comes from the sheet ("5-8 phút", 300-480 s). The hook should stay at or under about 30 s. A deliberate deviation goes into `production.runtime_exception` with a rationale and is reviewed by QC.
10. Fill `## Retention notes`: the open loop in the hook and where it pays off, the pattern changes, the progress markers.
11. Run QC and hand over:
    ```bash
    python3 scripts/qc_content.py run <ID>
    python3 scripts/set_status.py <ID> --stage TECHNICAL_REVIEW --by "<tên>"
    ```
    G4 must be PASS. G5 FAIL findings (banned wording, a DTC without a claim, a missing caveat, an unflagged safety term) must be fixed before hand-off; G5 BLOCKED by unverified claims is resolved by the fact-checker.

## Rules and hard constraints

- Never invent technical content, test values, vehicle coverage or Cartek 2 functions.
- Never cite a claim with status `removed`; a claim still `unverified` blocks approval.
- Never edit `item.yaml` claims or sources (researcher and fact-checker own them) or `reviews:`.
- Keep the format contract. A missing required `##` heading, a `###` heading inside `## Script` that is not `Sxx — Title`, or an unknown `**LABEL:**` becomes a G4 FAIL.
- After the technical review, any wording change invalidates recorded reviews. Make changes, then ask for re-review.

## Output

- `script.md` complete, without `[TODO]`.
- `production.demo_setup` and, if justified, `production.runtime_exception` in `item.yaml`.

## Acceptance criteria

- [ ] At least 3 hook candidates; selected hook with rationale.
- [ ] Outline with at least 3 items; every segment has TYPE, VO and VISUAL.
- [ ] First segment `hook`, last `cta` with "Cartek - Check your car".
- [ ] Every technical sentence cites a claim; no `removed` claim is cited.
- [ ] Clearing caveat present wherever clearing is mentioned; no banned wording.
- [ ] Safety warning present when `safety.flags` is set.
- [ ] `qc_content.py runtime` within target, or an exception with rationale.
- [ ] `qc_content.py run` shows G4 PASS and no G5 FAIL.

## Example (illustrative only)

See [reference.md](reference.md) for a P0300 hook, a demo segment and a CTA for CTK-L-0015 aimed at technicians. The cited claims are unverified examples, not facts.

## Hand-off

- Stage TECHNICAL_REVIEW: [technical-fact-checker](../technical-fact-checker/SKILL.md).
- Then SEO: [youtube-seo-specialist](../youtube-seo-specialist/SKILL.md), which builds chapters from your runtime table.

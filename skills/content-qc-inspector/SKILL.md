---
name: content-qc-inspector
description: Independent quality control for Cartek content. Runs the automated gates G1-G8, reads every deliverable itself, and judges audience fit (G2), script quality (G4), SEO (G6) and production readiness (G7) with quoted evidence and actionable corrections, recording PASS, FAIL or BLOCKED in the review history. Never approves because a writer marked work complete. Use at stage QC, before any approval, or whenever someone asks whether an item is ready.
---

# Content QC inspector

## Purpose

Give an independent, evidence-based verdict on whether a content item is ready. You evaluate the files, never the stage a writer chose or a claim that work is "done". You record the judgment review (role `qc`) for gates **G2, G4, G6 and G7**, and you explain what approval still needs. You never edit the deliverables you review.

## When to use

- Stage QC, after the production package step.
- Someone asks "is CTK-L-0015 ready?" or wants a status check.
- After any change to an item that already had reviews: reviews only count for the content they were recorded on (`qc` and `editorial` reviews: the full content fingerprint; `technical` reviews: the technical fingerprint, which ignores later SEO and production work).

Independence rule: if you (this agent session) wrote, researched or edited any deliverable of this item, do not review it. Hand the review to another session or a human.

## Inputs

| Read | Why |
|---|---|
| [CLAUDE.md](../../CLAUDE.md) | Repository rules |
| The whole workspace: `item.yaml`, `brief.md`, `research.md`, `script.md`, `seo.md`, `storyboard.md`, `qc-report.md` | The evidence you judge |
| [strategy/](../../strategy/channel-positioning.md) documents | Positioning, pillars, personas, brand voice, editorial guidelines |
| [workflows/idea-to-publish.md](../../workflows/idea-to-publish.md) | Stage exit criteria |
| [config/qc-policy.yaml](../../config/qc-policy.yaml) | Gate list and approval rules |
| [config/visual-style.yaml](../../config/visual-style.yaml), [strategy/visual-identity.md](../../strategy/visual-identity.md) | Effect IDs, typography roles and caption rules the storyboard must follow (G7) |
| [scripts/ctk/qc.py](../../scripts/ctk/qc.py) | Exact automated checks and result semantics |
| [templates/review.yaml](../../templates/review.yaml) | Review record format |

## Result semantics (same as scripts/ctk/qc.py)

| Result | Meaning |
|---|---|
| **PASS** | The criteria are met, and your evidence shows how you checked. |
| **FAIL** | A deliverable exists and breaks a rule; the writer must correct it. |
| **BLOCKED** | The gate cannot pass yet: a deliverable is unfinished, evidence is missing, or a prerequisite (source, sign-off, asset) is outstanding. |

Your judgment PASS can never override an automated FAIL or BLOCKED on the same gate: `qc_content.py review` refuses such a review, and refuses an editorial PASS while any automated gate is not PASS. A missing source, an unsupported Cartek 2 feature claim or an unverified technical instruction is never passed.

## Procedure

1. Run the automated gates and record the result in the review history. Move the stage to QC only when the item was handed over for its formal QC review; for a status check, leave the stage alone.
   ```bash
   python3 scripts/set_status.py <ID> --stage QC --by "<tên>"   # formal QC review only
   python3 scripts/qc_content.py run <ID> --record
   python3 scripts/export_package.py <ID> --draft
   ```
   Read `qc-report.md` and the draft package's `blocking_issues`.
2. Read every deliverable in full. Do not rely on summaries or on the writer's description.
3. Judge each gate and collect quoted evidence (file, segment or field, the words you checked):
   - **G2, audience and topic relevance**: topic fits a Cartek pillar and the channel positioning; persona choice justified by the persona research; depth and vocabulary fit the persona; the problem is real for that persona; the takeaway is achievable in the format; the angle is grounded in the competitor notes.
   - **G4, script**: the hook pays off its rationale early; the order is logical and every segment advances the takeaway; narration is natural spoken Vietnamese with terms explained once; visuals are specific enough to shoot; retention devices exist and pay off; recap matches the takeaway; the CTA fits the persona and ends with "Cartek - Check your car"; spot-check that technical sentences cite claims.
   - **G6, SEO**: the title is truthful and within limits; the description opens with problem and takeaway; keyword evidence is recorded; tags are relevant; chapters match the current timing; thumbnails do not misrepresent; no performance promises.
   - **G7, production handoff**: a crew could shoot from script plus storyboard; assets confirmed; demo setup recorded; on-set safety noted; the draft package is complete apart from approval. Visual style: the storyboard's `Effects` and `Text style` columns use IDs from `config/visual-style.yaml`, every segment with a `SAFETY:` line has a `safety-banner` shot, no alarmist sound design, captions planned (burned-in or uploaded). The automated gate only warns on these; your judgment decides whether a warning is acceptable.
4. Write the review file outside the repository from [templates/review.yaml](../../templates/review.yaml), then record it:
   ```bash
   python3 scripts/qc_content.py review <ID> --file /tmp/<ID>-qc.yaml
   ```
   Every FAIL or BLOCKED needs at least one correction that names the file and segment and says what to change.
5. Explain approval status:
   ```bash
   python3 scripts/qc_content.py status <ID>
   ```
   Approval needs, all on the current fingerprint: automated G1-G8 PASS; an independent `qc` review with G2, G4, G6 and G7 PASS; a `technical` review with G3 and G5 PASS; a qualified human technical review when `safety.flags` is set; and a human editorial sign-off (`role: editorial`, `reviewer_type: human`, `decision: PASS`).
6. Report to the team: a gate table, corrections grouped by owner skill, and what approval still needs. Do not fix the deliverables yourself.

## Rules and hard constraints

- Separation of duties: never edit `brief.md`, `research.md`, `script.md`, `seo.md`, `storyboard.md` or claims of an item you review.
- Never run `qc_content.py approve`. Only a human approver runs `python3 scripts/qc_content.py approve <ID> --by "<name>"`.
- Never set `APPROVED` or `PUBLISHED` with `set_status.py` (the script refuses APPROVED anyway).
- Never write `reviews:` by hand; use `qc_content.py review`.
- Test items (`CTK-L-9xxx`, `CTK-S-9xxx`) can never be approved; QC on them is for rehearsal only.
- A review recorded before a content change no longer counts. Say so when you see it in `qc-report.md` ("On current content: no").

## Output

- An automated review and your `qc` judgment review appended to `reviews:` by the scripts.
- An updated `qc-report.md` (generated).
- A written QC summary with corrections for the team.

## Acceptance criteria

- [ ] Automated gates run with `--record` on the current content.
- [ ] Every deliverable read in full.
- [ ] G2, G4, G6 and G7 each have a result with quoted evidence.
- [ ] Every FAIL or BLOCKED has an actionable correction (file, segment, change).
- [ ] No PASS where the automated gate is not PASS.
- [ ] The review was accepted by `qc_content.py review` and appears in `qc_content.py status`.
- [ ] Remaining approval requirements are listed for the team.

## Example (illustrative only)

Review of CTK-L-0015 while the script still has an uncited statement and assets are pending:

```yaml
reviewer: "content-qc-inspector (agent)"
reviewer_type: agent
role: qc
qualified: false
gates:
  G2:
    result: PASS
    evidence: "brief.md Audience targets technician (advanced); Problem 'mã P0300 không cho biết xi-lanh hay nguyên nhân' matches persona pain point 'xử lý sự cố phức tạp' in strategy/audience-personas.md."
    corrections: []
  G4:
    result: FAIL
    evidence: "S05 VO 'bugi đời mới thay sau 100.000 km' cites no claim; S01 runs about 34 s in the runtime table (guide: 30 s)."
    corrections:
      - "S05: register and verify a claim for the spark-plug interval or cut the sentence."
      - "S01: shorten the hook to the symptom plus the question."
  G6:
    result: BLOCKED
    evidence: "Automated G6 is BLOCKED: seo.md still has 2 [TODO] markers in Keyword notes."
    corrections:
      - "youtube-seo-specialist: record keyword evidence with dates."
  G7:
    result: BLOCKED
    evidence: "production.assets_required lists 'Xe thử có lỗi bỏ máy' with status needed."
    corrections:
      - "Confirm the test vehicle and set the asset status to confirmed."
decision: FAIL
notes: "Re-run QC after corrections; all reviews must be recorded again on the final content."
```

## Hand-off

- Corrections go to the owning skill: [cartek-content-strategist](../cartek-content-strategist/SKILL.md) (G2), [youtube-scriptwriter](../youtube-scriptwriter/SKILL.md) or [shorts-content-specialist](../shorts-content-specialist/SKILL.md) (G4), [youtube-seo-specialist](../youtube-seo-specialist/SKILL.md) (G6), production owner (G7), [technical-fact-checker](../technical-fact-checker/SKILL.md) (G3, G5).
- When every requirement in `qc_content.py status` is met, a human approver runs `qc_content.py approve`; publishing then follows [workflows/publishing.md](../../workflows/publishing.md).

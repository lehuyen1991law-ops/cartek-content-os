# Technical review

An independent check of every technical claim and every safety risk before a script can be approved. The reviewer is not the researcher or the scriptwriter of the item.

**Skills used:** [technical-fact-checker](../skills/technical-fact-checker/SKILL.md). A qualified human technical reviewer is mandatory for safety-flagged items.

**Done when:** every claim is `verified` or `removed`, safety topics are flagged or dismissed with a rationale, gates G3 and G5 are PASS, and a `technical` review is recorded on the current content fingerprint. For safety-flagged items, that review is by a human with `qualified: true`.

## When a qualified human is mandatory

[config/qc-policy.yaml](../config/qc-policy.yaml) → `approval.human_technical_review`:

| Value | Human technical review required for |
|---|---|
| `safety_flagged` (current setting) | items whose `safety.flags` is not empty |
| `always` | every item (recommended once a technical reviewer is assigned) |

"Qualified" means trained and experienced on the system concerned, for example a technician trained for high-voltage work when the item touches hybrid or EV systems. Write the basis of the qualification in the review `notes`.

An agent can still record a `technical` review for items without safety flags. The approval also always needs a human editorial sign-off ([idea-to-publish.md](idea-to-publish.md#8-qc-kiểm-duyệt-chất-lượng)).

## Preconditions

1. `research.md` and `script.md` have no `[TODO]` markers. Gate G5 is BLOCKED until both are finished.
2. Run QC and read the G3 and G5 findings:

```bash
python3 scripts/qc_content.py run <ID>
```

## Procedure

1. **Claims, one by one** (`item.yaml` → `claims`). For each claim:
   1. Open every cited source. Check that it says exactly what the claim says: scope, conditions, units, vehicles, model years.
   2. Check that at least one source has an accepted type for the claim category ([research.md](research.md#accepted-source-types-per-claim-category)).
   3. Decide:
      - `verified`: set `verified_by` (your name or skill name) and `verified_on` (`YYYY-MM-DD`).
      - `disputed`: sources conflict. Explain in `notes`. The item stays BLOCKED.
      - `removed`: the claim cannot be supported. Delete the statement from `script.md` and remove its ID from every `CLAIMS:` line.
   4. Add a row to `research.md` → "Fact-check log": claim, decision, evidence, checked by, date.
2. **Codes.** Every DTC in narration, on-screen text or SEO text needs a claim whose text contains the code. Codes in manufacturer-controlled ranges (`^P1`, `^P3[0-3]`, `^[BCU][12]`) need `vehicle.scope: specific` with the brand named.
3. **Codes vs causes.** The script must not present a code as a confirmed root cause. Candidate causes need the test that confirms them.
4. **Clearing codes.** Clearing a code or resetting the warning lamp never repairs the fault. Any narration that mentions clearing needs a caveat that the cause remains and the fault can return.
5. **Cartek 2 features.** Each `cartek-feature` claim points (`feature_id`) to a `verified` entry in [data/reference/cartek-2-feature-register.yaml](../data/reference/cartek-2-feature-register.yaml). The register is empty on 2026-11-05, so such claims stay BLOCKED until the product team confirms features ([strategy/product-facts.md](../strategy/product-facts.md)).
6. **Safety.** Decide flags and dismissals (next section). For flagged items, make sure the script has a `TYPE: safety` segment or `SAFETY:` lines where the risk occurs.
7. **Wording.** Read the warnings G5 reports for absolute or all-vehicle wording ("100%", "chắc chắn", "tất cả các dòng xe", "không cần thợ") and confirm a verified claim supports each, or have it rewritten.
8. Re-run QC. Record a PASS only when G3 and G5 are PASS.
9. Record the review (below). A technical review is bound to the **technical scope** of the content: `brief.md`, `research.md`, `script.md` and the `item.yaml` fields other than `seo` and `production` (claims, sources, vehicle, safety...). Later SEO or production work does not void it; any change inside that scope does, and the review must be recorded again.

## Safety flags and dismissals

QC scans the working title, `brief.md`, `research.md` and `script.md` for hazardous topics ([config/qc-policy.yaml](../config/qc-policy.yaml) → `safety_terms`; template prompts in `[TODO ...]` and HTML comments are ignored). Each detected topic must be either flagged or dismissed. Otherwise G5 FAILs.

| Flag ([config/taxonomy.yaml](../config/taxonomy.yaml)) | Topic | Example trigger words (accents ignored) |
|---|---|---|
| `high-voltage` | Hybrid / EV high-voltage systems | cao áp, điện áp cao, xe điện, hybrid |
| `brakes` | Braking systems, ABS, EPB | phanh, ABS, EPB, má phanh |
| `steering` | Steering, EPS, steering-angle calibration | vô lăng, trợ lực lái, EPS, góc lái, thước lái |
| `airbag-srs` | Airbags / SRS, seat-belt pretensioners | túi khí, SRS, airbag, căng đai |
| `fuel-system` | Fuel lines, pressure release, fire risk | áp suất nhiên liệu, ống/đường xăng, bơm xăng, xả áp, tháo kim phun, rò rỉ xăng |
| `lifting` | Jacking, lifts, working under the vehicle | kích xe, con đội, cầu nâng, chui gầm |
| `battery-12v` | 12 V battery disconnection, jump starting | ắc quy, câu bình, tháo cực |
| `hot-or-moving-parts` | Hot coolant, fans, belts, running engine | nước làm mát nóng, nắp két nước, quạt két nước, dây curoa, động cơ đang chạy/nổ |
| `adas` | ADAS sensors and calibration | ADAS, radar, cân chỉnh camera |

- **Flag** (`safety.flags`) when the video shows, demonstrates or explains how to do work on that system. The item then needs a qualified human technical review and a safety warning in the script where the risk occurs.
- **Dismiss** (`safety.dismissed`) when the system is only named, for example a fuel pump mentioned as a possible cause or a test left to a professional, and no procedure is shown or explained. Each dismissal needs a rationale of at least 15 characters:

```yaml
safety:
  flags: []
  dismissed:
    - flag: fuel-system
      rationale: "Bơm xăng chỉ được nhắc như một nguyên nhân có thể; video không có thao tác trên hệ thống nhiên liệu."
```

The reviewer confirms each dismissal; a wrong dismissal is a G5 FAIL in the judgment review.

## Recording the review

1. Copy [templates/review.yaml](../templates/review.yaml) to a scratch location outside `content/`.
2. Fill it:

```yaml
reviewer: "technical-fact-checker (agent)"   # or the human reviewer's name
reviewer_type: agent                          # human for safety-flagged items
role: technical
qualified: false                              # true for a qualified human reviewer
gates:
  G3:
    result: PASS
    evidence: "C01-C04 checked against SRC01-SRC03; C05 removed and deleted from S04."
    corrections: []
  G5:
    result: PASS
    evidence: "P0300 defined by C01; clearing caveat in S05; fuel-system dismissed (pump named only as a cause)."
    corrections: []
decision: PASS
notes: "Qualification basis (humans): ..."
```

3. Record it:

```bash
python3 scripts/qc_content.py review <ID> --file <path/to/review.yaml>
python3 scripts/qc_content.py status <ID>
```

The script refuses a review with an unknown gate or result, evidence shorter than 15 characters, or a FAIL/BLOCKED without corrections. It stamps the date, a review ID and the current content fingerprint, then rewrites `qc-report.md`.

A review counts toward approval only while the content is unchanged. When a later QC result for the same role and gate is not PASS, the latest result wins.

## What QC checks

**G3 — research completeness and factual accuracy:** see [research.md](research.md#what-qc-checks-g3).

**G5 — automotive technical and safety review** ([scripts/ctk/qc.py](../scripts/ctk/qc.py) → `gate_g5`):

- BLOCKED while `script.md` or `research.md` is unfinished.
- Banned wording in narration, on-screen text, safety notes or SEO text, such as "xóa lỗi là xong": FAIL. The same words in a sentence that clearly debunks a myth ("nhiều người tưởng…", "không phải…", "là sai", "hiểu lầm") are reported as a warning for the reviewer instead. A bare "không" does not count as debunking.
- Absolute or all-vehicle wording: warnings the reviewer must resolve.
- Narration mentions clearing codes without a caveat: FAIL.
- A DTC in public text without a claim containing it: FAIL. A manufacturer-controlled code without a specific vehicle: FAIL.
- A detected safety topic neither flagged nor dismissed, or an unknown flag: FAIL.
- Safety flags without a safety segment or `SAFETY:` line: FAIL.
- `safety` or `diagnostic-procedure` claims still `unverified` or `disputed`: BLOCKED.

The automated gate checks structure and wording. It cannot judge whether a statement is true; the recorded technical review does.

---
name: automotive-researcher
description: Researches the technical substance of a Cartek video or Short. Writes research.md and the item.yaml source and claim register, separating OBD-II standard behaviour from manufacturer-specific behaviour, fault codes from confirmed root causes, model-year differences, and verified Cartek 2 features from unverified ones. Use at stage RESEARCH, or whenever QC gate G3 is BLOCKED or FAIL.
---

# Automotive researcher

## Purpose

Produce traceable evidence for every technical statement the video will make. You write `research.md` and the `sources:` and `claims:` blocks of `item.yaml`. Gate **G3 (research completeness and factual accuracy)** depends on your work; G5 depends on it too.

Accuracy beats completeness. A claim you cannot support stays `unverified`. QC then blocks technical approval, which is the intended outcome.

## When to use

- The item is at stage RESEARCH (after [cartek-content-strategist](../cartek-content-strategist/SKILL.md) drafted the brief).
- QC reports G3 BLOCKED or FAIL: missing sources, unverified claims, script citing unknown claims.
- A script needs a new technical statement: register it as a claim first.

## Inputs

| Read | Why |
|---|---|
| [CLAUDE.md](../../CLAUDE.md) | Repository rules |
| The workspace `brief.md` and `item.yaml` | Research question, persona, vehicle scope |
| [workflows/research.md](../../workflows/research.md) | Research standards and process |
| [strategy/editorial-guidelines.md](../../strategy/editorial-guidelines.md) | Accuracy, sourcing and safety rules |
| [strategy/product-facts.md](../../strategy/product-facts.md), [data/reference/cartek-2-feature-register.yaml](../../data/reference/cartek-2-feature-register.yaml) | The only allowed source of Cartek 2 capabilities |
| [config/taxonomy.yaml](../../config/taxonomy.yaml) | `source_types`, `claim_categories`, `safety_flags` |
| [config/qc-policy.yaml](../../config/qc-policy.yaml) | `claim_source_requirements`, `manufacturer_specific_dtc_patterns`, `safety_terms` |
| [reference.md](reference.md) | Source hierarchy, OBD-II services, DTC structure, claim examples |
| [templates/research-report.md](../../templates/research-report.md) | Required sections |

## Procedure

1. Restate the research question from the brief in `research.md` under **Research question**. Note the persona and depth so the evidence fits the audience.
2. Classify every point the video needs to make:
   - **OBD-II/EOBD standard behaviour** (category `obd-standard`): services $01-$0A, generic DTC definitions, readiness monitors.
   - **Generic DTC meaning** (`dtc-definition`): what the code means according to SAE J2012 / ISO 15031-6 or OEM service information.
   - **Manufacturer-specific** (`manufacturer-specific`) or **vehicle-specific** (`vehicle-specific`): manufacturer-controlled code ranges (by default `P1xxx`, `P30xx-P33xx`, `B1/B2`, `C1/C2`, `U1/U2` in `manufacturer_specific_dtc_patterns`; verify against the standard), procedures, specifications, model-year changes.
   - **Diagnostic procedure** (`diagnostic-procedure`): a test or repair step a viewer could perform.
   - **Cartek 2 capability** (`cartek-feature`): allowed only with a `feature_id` that is `verified` in the feature register.
   - **Safety** (`safety`), **general knowledge** (`general-knowledge`), **market news** (`market-news`).
3. Find sources, strongest first (see [reference.md](reference.md)). Open and read each source. Record only what you actually read:
   ```yaml
   sources:
     - id: SRC01
       title: "<exact document or page title>"
       publisher: "<organisation>"
       type: standard            # config/taxonomy.yaml -> source_types
       url: "https://..."        # or citation: "<book, edition, page>" for offline sources
       accessed: "YYYY-MM-DD"    # required when url is set
       notes: "<section/page you relied on>"
   ```
4. Register each statement as a claim, worded exactly as the script may say it:
   ```yaml
   claims:
     - id: C01
       text: "<one checkable statement>"
       category: dtc-definition
       sources: [SRC01]
       status: unverified        # the fact-checker sets verified/disputed/removed
       feature_id: null
       verified_by: ""
       verified_on: null
       notes: ""
   ```
   Leave `status: unverified` yourself. Verification is the independent [technical-fact-checker](../technical-fact-checker/SKILL.md)'s job. Never mark your own claims `verified`.
5. Write `research.md`, every section, no `[TODO]`:
   - **Findings** with claim IDs in brackets, e.g. `[C01]`.
   - **Standard vs manufacturer-specific**: a table per topic.
   - **Codes vs root causes**: a code says a condition was detected. List the candidate causes and the test that would confirm each one, each with a claim ID.
   - **Vehicle and model-year differences**, or "Không phụ thuộc dòng xe" with the reason.
   - **Cartek 2 features used**: feature IDs from the register, or "none". If the register lacks a needed feature, say so and leave the related claim unverified.
   - **Safety notes**: hazards for viewers and for the film crew.
   - **Open questions**: everything you could not verify, or "None".
6. Check:
   ```bash
   python3 scripts/qc_content.py run <ID>
   python3 scripts/validate_content.py
   ```
   G3 must show no FAIL: no dangling source IDs, valid types and categories, access dates. BLOCKED from unverified claims is expected until fact-checking.
7. Hand back: the strategist finalizes the brief (stage BRIEF).

## Rules and hard constraints

- Never invent diagnostic data, PIDs, specifications, vehicle compatibility, fault causes, test values, URLs, page numbers or document versions.
- A DTC is not a root cause. Write "P0300 cho biết ECU phát hiện bỏ máy", never "P0300 nghĩa là bugi hỏng".
- Clearing a code does not repair anything. Clearing also erases diagnostic evidence such as freeze frame data and readiness status; register that as a claim when the video mentions clearing.
- Do not assume US or EU OBD mandates describe vehicles sold in Vietnam. Model year, market and engine matter: verify per vehicle.
- Cartek 2 capabilities come only from the feature register. Marketing assumptions, "every scanner does this" and competitor tools are not evidence for Cartek 2.
- Forums, social posts and videos (`other`) are leads, never sufficient evidence alone.
- Flag hazardous topics (high voltage, brakes, steering, airbags/SRS, fuel system, lifting, hot or moving parts, ADAS) in Safety notes. The fact-checker decides `safety.flags` or `safety.dismissed`.
- Do not edit `script.md`, `seo.md` or `data/`.

## Output

- `research.md`: all template sections complete.
- `item.yaml`: `sources:` and `claims:` (all claims `unverified`), plus vehicle-scope corrections if research shows the topic is vehicle-specific.

## Acceptance criteria

- [ ] Every technical statement the brief needs is a claim with at least one source.
- [ ] Every source has a type from `config/taxonomy.yaml` and a URL with access date, or a citation.
- [ ] Each claim's sources include a type accepted for its category (`claim_source_requirements`), or the gap is stated in Open questions.
- [ ] Standard and manufacturer-specific points are separated; codes are separated from root causes.
- [ ] No Cartek 2 capability appears without a register feature ID.
- [ ] `research.md` has no `[TODO]`; G3 shows no FAIL.

## Example (illustrative only)

Item CTK-L-0015 "Lỗi P0300 - Ác Mộng của Mọi Động Cơ?", persona `technician`. The statements below show the format. They are not verified facts: each stays `unverified` until the cited source has been read and checked.

```yaml
claims:
  - id: C01
    text: "P0300 là mã chuẩn OBD-II cho tình trạng phát hiện bỏ máy ngẫu nhiên/nhiều xi-lanh (Random/Multiple Cylinder Misfire Detected)."
    category: dtc-definition
    sources: [SRC01]          # SAE J2012 / ISO 15031-6, or OEM service information
    status: unverified
  - id: C02
    text: "Xóa mã lỗi bằng máy chẩn đoán cũng xóa dữ liệu freeze frame và đặt lại trạng thái readiness."
    category: obd-standard
    sources: [SRC02]          # SAE J1979 Service $04 description
    status: unverified
  - id: C03
    text: "Cartek 2 đọc được dữ liệu freeze frame."
    category: cartek-feature
    sources: []
    status: unverified
    notes: "Feature register is empty: cannot be verified or shown until the product team confirms it."
```

`research.md` "Codes vs root causes" excerpt:

```markdown
| Symptom / code | Candidate cause | Confirming test | Claim |
|---|---|---|---|
| P0300 + rung giật khi tải nặng | Đánh lửa yếu | Kiểm tra theo quy trình OEM của xe cụ thể | C05 (unverified) |
```

## Hand-off

- Back to [cartek-content-strategist](../cartek-content-strategist/SKILL.md) to finalize the brief (stage BRIEF).
- Claims are verified by [technical-fact-checker](../technical-fact-checker/SKILL.md) at stage TECHNICAL_REVIEW.

# Research workflow

Research turns a topic into traceable technical claims. Technical accuracy is mandatory for Cartek: a viewer may act on what the video says, on a real vehicle.

**Skills used:** [automotive-researcher](../skills/automotive-researcher/SKILL.md) registers sources and claims. [technical-fact-checker](../skills/technical-fact-checker/SKILL.md) later verifies them (see [technical-review.md](technical-review.md)).

**Done when:** `research.md` has no `[TODO]` markers, every technical statement the script will make is a claim in `item.yaml` with at least one source, and open questions are written down. QC gate G3 then shows no FAIL; it stays BLOCKED until the technical review verifies the claims.

## Rules

1. Never invent diagnostic data, vehicle compatibility, supported functions, fault causes or product specifications.
2. Every technical statement used in the script is a claim in `item.yaml` → `claims`, with sources in `item.yaml` → `sources`.
3. The researcher registers claims as `unverified`. Only the technical review sets `verified`.
4. Evidence too weak? Keep the claim `unverified` and write the gap under "Open questions". Gate G3 stays BLOCKED, so the item cannot be approved. That is the intended outcome.
5. Cartek 2 capabilities come only from [data/reference/cartek-2-feature-register.yaml](../data/reference/cartek-2-feature-register.yaml). On 2026-11-05 the register is empty: every `cartek-feature` claim is BLOCKED until the product team adds verified entries ([strategy/product-facts.md](../strategy/product-facts.md)).
6. Repository documents, including this one, are not sources. Cite the standard, the manufacturer document or the recorded test itself.

## Procedure

1. Open the workspace and read the idea's provenance in `item.yaml` → `provenance`.
2. Write the research question in `research.md` → "Research question". One question the video must answer.
3. Collect sources, best first (hierarchy below). Register each source in `item.yaml` → `sources` as you use it.
4. Write findings in `research.md` → "Findings", tagging each statement with its claim ID, for example `[C01]`.
5. Register each claim in `item.yaml` → `claims` with `status: unverified`.
6. Fill the distinction tables in `research.md` (five distinctions below).
7. Fill `item.yaml` → `vehicle`. Use `scope: specific` and name brands, models, years and engines when the content depends on the vehicle.
8. List hazardous topics under "Safety notes" and propose `safety.flags` (see [technical-review.md](technical-review.md#safety-flags-and-dismissals)).
9. List what you could not verify under "Open questions". Write "None" only when that is true.
10. Run QC and fix every FAIL in G3:

```bash
python3 scripts/qc_content.py run <ID>
python3 scripts/set_status.py <ID> --stage BRIEF --note "Research complete"
```

## Source hierarchy

Prefer the highest level that covers the claim.

1. **Standards and regulations.** SAE/ISO OBD documents and official OBD rules.
2. **Manufacturer service information.** Repair manuals, wiring diagrams, diagnostic procedures and technical service bulletins for the exact vehicle.
3. **Recorded hands-on tests.** Dated test on a named vehicle with the tool and software version, kept as a log or footage.
4. **Tool and component maker documentation.** For Cartek 2, only official product documentation or written product-team confirmation.
5. **Textbooks, training curricula, trade publications.**
6. **Named, dated expert interviews.**
7. **Anything else.** Forum posts, videos and blogs are leads, never proof on their own.

Source types are defined in [config/taxonomy.yaml](../config/taxonomy.yaml) → `source_types`:

| Type | Meaning |
|---|---|
| `standard` | SAE / ISO standard (e.g. SAE J1979, SAE J2012, ISO 15031, ISO 15765-4) |
| `regulation` | Regulation text (e.g. US EPA / CARB OBD rules, EU type-approval) |
| `oem-service-information` | Manufacturer service/repair information for a specific vehicle |
| `oem-tsb` | Manufacturer technical service bulletin |
| `manufacturer-documentation` | Tool or component maker documentation (not Cartek) |
| `cartek-product-documentation` | Official Cartek documentation or written product-team confirmation |
| `hands-on-test` | Recorded test on a real vehicle (date, vehicle, tool version) |
| `textbook` | Automotive engineering textbook or training curriculum |
| `trade-publication` | Trade or technical publication |
| `expert-interview` | Named expert, recorded and dated |
| `news` | Dated news article |
| `other` | Anything else; weak evidence on its own |

## Accepted source types per claim category

A claim can only be verified when at least one of its sources has an accepted type for its category ([config/qc-policy.yaml](../config/qc-policy.yaml) → `claim_source_requirements`). Otherwise G3 FAILs.

| Claim category | Meaning | Accepted source types |
|---|---|---|
| `obd-standard` | Behaviour defined by OBD-II/EOBD standards | standard, regulation, textbook, oem-service-information, manufacturer-documentation |
| `dtc-definition` | Meaning of a diagnostic trouble code | standard, oem-service-information, textbook, manufacturer-documentation |
| `manufacturer-specific` | Behaviour or code meaning that depends on the manufacturer | oem-service-information, oem-tsb, manufacturer-documentation, hands-on-test |
| `vehicle-specific` | Applies to a specific make/model/year/engine | oem-service-information, oem-tsb, hands-on-test |
| `diagnostic-procedure` | A test or repair step the viewer may perform | oem-service-information, oem-tsb, standard, textbook, hands-on-test, manufacturer-documentation |
| `cartek-feature` | What the Cartek 2 device or app can do | cartek-product-documentation, hands-on-test (plus a verified register entry) |
| `safety` | Safety statement or warning | oem-service-information, regulation, standard, textbook, manufacturer-documentation |
| `general-knowledge` | General automotive knowledge | standard, regulation, oem-service-information, oem-tsb, textbook, trade-publication, manufacturer-documentation, expert-interview, hands-on-test |
| `market-news` | Industry or market news | news, trade-publication, regulation, manufacturer-documentation, cartek-product-documentation |

## Registering sources and claims in item.yaml

Sources (`item.yaml` → `sources`):

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `SRC01`, `SRC02`, … unique in the item |
| `title` | yes | Document title |
| `type` | yes | One of the source types above |
| `url` or `citation` | one of them | `citation` for offline documents (standard number, manual name, page) |
| `accessed` | with `url` | Date you read it, `YYYY-MM-DD` |
| `publisher` | no | Organisation |
| `notes` | no | Revision, section, limits of the source |

Claims (`item.yaml` → `claims`):

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `C01`, `C02`, … unique in the item; the script cites these IDs |
| `text` | yes | The exact statement, as narrow as the evidence. Include the DTC code when the claim defines one |
| `category` | yes | One of the claim categories above |
| `sources` | yes | Source IDs; every ID must exist in `sources` |
| `status` | yes | `unverified` when registered; the technical review sets `verified`, `disputed` or `removed` |
| `feature_id` | for `cartek-feature` | ID of a `verified` entry in the feature register |
| `verified_by`, `verified_on` | when `verified` | Who verified it and when (set by the technical review) |
| `notes` | no | Conditions, exceptions, what the source does not say |

Example (structure only: these claims are unverified and the citations must be checked against the real documents before use):

```yaml
sources:
  - id: SRC01
    title: "SAE J2012 — Diagnostic Trouble Code Definitions"
    publisher: "SAE International"
    type: standard
    citation: "SAE J2012, current revision — confirm revision and section before citing"
    notes: "Generic P0xxx definitions."
  - id: SRC02
    title: "Service information for <make/model/year>, misfire diagnosis"
    type: oem-service-information
    citation: "<manual name, section, page>"
claims:
  - id: C01
    text: "P0300 = Random/Multiple Cylinder Misfire Detected"
    category: dtc-definition
    sources: [SRC01]
    status: unverified
    feature_id: null
    verified_by: ""
    verified_on: null
    notes: ""
  - id: C02
    text: "Trên <xe cụ thể>, quy trình kiểm tra bỏ máy bắt đầu bằng ... (theo SRC02)"
    category: vehicle-specific
    sources: [SRC02]
    status: unverified
    feature_id: null
    verified_by: ""
    verified_on: null
    notes: "Chỉ áp dụng cho đời xe trong SRC02."
```

## The five distinctions

Every research report keeps these apart. `research.md` has a table or section for each.

### 1. OBD-II standard vs manufacturer-specific

Section "Standard vs manufacturer-specific". Orientation only; cite the standard, not this page:

- Standardised: the emissions-related diagnostic services defined in SAE J1979 / ISO 15031-5 (current data, freeze frame, stored, pending and permanent DTCs, clearing emission-related information, monitor test results, vehicle information) and generic DTC definitions in SAE J2012 / ISO 15031-6.
- Manufacturer-specific: enhanced diagnostics (ABS, SRS, body, transmission modules), bidirectional tests, coding and adaptations, service resets, and manufacturer-controlled DTC ranges. QC treats codes matching `^P1`, `^P3[0-3]` and `^[BCU][12]` as manufacturer-controlled ([config/qc-policy.yaml](../config/qc-policy.yaml)); such content must name the vehicle.

### 2. Confirmed facts vs assumptions

- A confirmed fact is a claim the technical review marks `verified`.
- Everything else is an assumption: keep it `unverified`, write it under "Open questions", and do not let the script state it as fact.
- Words like "thường", "hay gặp" or "phổ biến" are claims too. They need a source.

### 3. DTC vs root cause

Section "Codes vs root causes". A DTC says that the control module detected a condition. It does not confirm the root cause. For each code, list candidate causes and the test that confirms each one. The script must never present one cause as certain from the code alone, and never imply that clearing the code repairs anything.

### 4. Model-year and vehicle differences

Section "Vehicle and model-year differences". Record the makes, models, years and engines each claim covers. Claims that depend on the vehicle use category `vehicle-specific` or `manufacturer-specific` and need service information or a recorded test on that vehicle. Generic content must say when behaviour varies by vehicle.

### 5. Supported Cartek 2 features vs unverified claims

Section "Cartek 2 features used". Only features with `status: verified` in [the feature register](../data/reference/cartek-2-feature-register.yaml) may be shown or described. A claim of category `cartek-feature` needs `feature_id` pointing to such an entry; otherwise G3 is BLOCKED. Never infer a Cartek 2 capability from another scanner, a competitor video or general OBD-II knowledge.

## What QC checks (G3)

[scripts/ctk/qc.py](../scripts/ctk/qc.py) → `gate_g3`:

- `research.md` exists (else BLOCKED) and has the sections "Research question", "Findings", "Standard vs manufacturer-specific", "Open questions" (else FAIL).
- No `[TODO]` markers in `research.md` (else BLOCKED).
- At least one claim that is not `removed` (else BLOCKED).
- Unique source and claim IDs; known source types and claim categories; every URL source has `accessed` (else FAIL).
- Every claim cites existing sources (else FAIL).
- `unverified` or `disputed` claims → BLOCKED.
- `verified` claims cite an accepted source type and record `verified_by` and `verified_on` (else FAIL).
- `cartek-feature` claims point to a verified register entry (else BLOCKED).
- Every `CLAIMS:` reference in `script.md` exists and is not `removed` (else FAIL).

G5 also reads `research.md` for its safety-term scan, and stays BLOCKED while `research.md` has `[TODO]` markers.

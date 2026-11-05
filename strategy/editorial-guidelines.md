# Editorial guidelines

The accuracy, safety, sourcing and integrity rules every Cartek video follows. QC enforces most of them automatically through [config/qc-policy.yaml](../config/qc-policy.yaml); the rest are checked by the independent reviews.

Related: [research workflow](../workflows/research.md) · [technical review workflow](../workflows/technical-review.md) · [brand voice](brand-voice.md) · [product facts](product-facts.md)

## From the sheet (source)

The sheet sets the channel topic, "Chia sẻ kinh nghiệm sửa chữa ô tô qua hệ thống OBD2" ('Content Direction'!B1), and names the product "Cartek 2" ('Content Direction'!B5). It contains no editorial rules. Everything below is repository guidance.

## Repository guidance (added 2026-11-05; editorial assumption, change freely)

### Five distinctions every script must keep

| Keep apart | What it means in practice |
|---|---|
| **OBD-II standard vs manufacturer-specific** | Generic diagnostic services and generic codes come from the OBD-II/EOBD standards (SAE J1979, SAE J2012, ISO 15031). Manufacturer codes, module access beyond the engine, coding, adaptations and service resets depend on the make, the model and the tool. Say which one you are showing. |
| **Confirmed fact vs assumption** | A fact has a verified claim with an accepted source. An assumption is labelled as one ("có thể", "thường gặp") only when a source supports that hedge. Unverified statements stay out of the script. |
| **Trouble code vs root cause** | A code records what the control unit detected. The cause is confirmed only by a test. Present causes as candidates, each with the test that confirms or rules it out. |
| **Vehicle and model-year differences** | Procedures, specifications and code meanings can change by make, model, year, engine and market. Name the vehicle ("Toyota Vios 2018 1.5 AT") whenever a step or value is vehicle-specific. Vehicles sold in Vietnam may differ from other markets; confirm, do not assume. |
| **Verified Cartek 2 features vs claims** | Only features with `status: verified` in the [feature register](../data/reference/cartek-2-feature-register.yaml) may be described. The register is empty today. See [product facts](product-facts.md). |

### Never invent

Do not invent, estimate or "fill in":

- diagnostic data (codes, freeze frame values, live data, test results) that was not captured on a real vehicle;
- vehicle compatibility or protocol support;
- fault causes, failure rates or "most common" rankings without a source;
- specifications (torque values, pressures, resistances, intervals);
- Cartek 2 capabilities, versions or prices;
- YouTube metrics, search volumes or market statistics.

If evidence is missing, the claim stays `unverified`, QC blocks technical approval, and the open question goes into `research.md` → "Open questions".

### Clearing codes never repairs a fault

Clearing a code removes the stored record and turns the warning lamp off. It does not repair the cause; if the fault is still present, the code and the lamp come back. On OBD-II vehicles, clearing also erases related diagnostic data such as freeze frame data and readiness status; confirm the details for the topic in research and cite the standard when you state them on screen.

QC gate G5 fails any wording that presents clearing as a fix (for example "xóa lỗi là xong"). It also fails a script that mentions clearing codes without saying that clearing does not fix the cause. Sentences that debunk the myth are flagged for a reviewer instead of failed.

### Safety-flagged topics

These topics come from `safety_flags` in [config/taxonomy.yaml](../config/taxonomy.yaml):

| Flag | Covers |
|---|---|
| high-voltage | Hybrid / EV high-voltage systems |
| brakes | Braking systems, ABS, EPB |
| steering | Steering, EPS, steering-angle calibration |
| airbag-srs | Airbags / SRS, seat-belt pretensioners |
| fuel-system | Fuel lines, pressure release, fire risk |
| lifting | Jacking, lifts, working under the vehicle |
| battery-12v | 12 V battery disconnection, jump starting |
| hot-or-moving-parts | Hot engine/coolant, fans, belts, running engine |
| adas | ADAS sensors and calibration |

Rules:

1. QC scans the brief, research and script for safety terms. Every detected topic must be either **flagged** (`safety.flags`) or **dismissed** with a written rationale (`safety.dismissed`), for example when a part is only named as a possible cause and no work on it is shown.
2. A flagged item needs an on-screen safety warning: a `TYPE: safety` segment or a `**SAFETY:**` line where the risk occurs.
3. A flagged item cannot be approved without a **qualified human technical review** of gates G3 and G5 (`approval.human_technical_review: safety_flagged`). The policy can be raised to `always` once a technical reviewer is assigned.
4. Never show viewers how to defeat, bypass or disable a safety or emission system.

### Source hierarchy

Use the strongest source available. Source types are defined in [config/taxonomy.yaml](../config/taxonomy.yaml) → `source_types`.

1. **Standards and regulations** (`standard`, `regulation`): SAE J1979, SAE J2012, ISO 15031 series, ISO 15765-4, regulation texts. Authority for generic OBD-II behaviour and generic code definitions.
2. **OEM information** (`oem-service-information`, `oem-tsb`): authority for vehicle-specific procedures, specifications and manufacturer codes.
3. **Cartek evidence** (`cartek-product-documentation`, `hands-on-test`): the only evidence for Cartek 2 capabilities. A hands-on test records date, vehicle and tool version.
4. **Technical references** (`textbook`, `manufacturer-documentation` for non-Cartek tools and parts).
5. **Secondary sources** (`trade-publication`, `expert-interview`, `news`): dated and attributed.
6. **Other** (`other`): forums, videos, blogs. Leads only, never the sole evidence for a technical claim.

### The claims register

Every technical statement in a script is a claim in `item.yaml`. Fields are defined in [schemas/content.schema.json](../schemas/content.schema.json); a guide is in [templates/item.yaml](../templates/item.yaml).

- **Sources** (`sources:`): `id` (SRC01…), `title`, `type`, and a `url` with an `accessed` date or a `citation` for offline material.
- **Claims** (`claims:`): `id` (C01…), `text`, `category`, `sources`, `status` (`unverified`, `verified`, `disputed`, `removed`), plus `verified_by` and `verified_on` once verified, and `feature_id` for Cartek 2 claims.
- **Script links:** each segment lists the claims it relies on (`**CLAIMS:** C01, C02`). A segment may not cite a missing or removed claim.
- **Codes:** every trouble code that appears on screen or in the narration must be defined by a claim. Codes in manufacturer-controlled ranges require a vehicle-specific item (`vehicle.scope: specific` with the brand).
- **Accepted evidence per category** (mirror of `claim_source_requirements` in [config/qc-policy.yaml](../config/qc-policy.yaml) on 2026-11-05; if they differ, the config wins):

| Claim category | A verified claim needs at least one source of type |
|---|---|
| obd-standard | standard, regulation, textbook, oem-service-information, manufacturer-documentation |
| dtc-definition | standard, oem-service-information, textbook, manufacturer-documentation |
| manufacturer-specific | oem-service-information, oem-tsb, manufacturer-documentation, hands-on-test |
| vehicle-specific | oem-service-information, oem-tsb, hands-on-test |
| diagnostic-procedure | oem-service-information, oem-tsb, standard, textbook, hands-on-test, manufacturer-documentation |
| cartek-feature | cartek-product-documentation, hands-on-test (plus a verified register entry) |
| safety | oem-service-information, regulation, standard, textbook, manufacturer-documentation |
| general-knowledge | standard, regulation, oem-service-information, oem-tsb, textbook, trade-publication, manufacturer-documentation, expert-interview, hands-on-test |
| market-news | news, trade-publication, regulation, manufacturer-documentation, cartek-product-documentation |

### Wording QC reviews

[config/qc-policy.yaml](../config/qc-policy.yaml) lists phrases that a reviewer must confirm, such as "100%", "chắc chắn", "đảm bảo", "tuyệt đối", "vĩnh viễn", "tất cả các dòng xe", "mọi xe" and "không cần thợ". They are allowed only when a verified claim supports them. Avoid them by default.

### No invented performance

- Never promise CTR, rankings, "lên top", "triệu view" or virality in titles, descriptions, thumbnails or SEO notes. QC gate G6 fails these phrases.
- Performance data comes only from YouTube Studio or its export, entered in `performance.yaml` with the source and evidence ([post-publish analysis](../workflows/post-publish-analysis.md)).

### Privacy

- Do not show customers' faces, names, phone numbers, addresses, invoices, licence plates or full VINs without written consent. Blur them in the edit.
- Prefer test vehicles owned by Cartek or the team. Record the vehicle in `production.demo_setup` by make, model, year and engine only.
- Never commit raw footage or customer documents to Git. Store footage elsewhere and link it in `production.footage_links`.

### Trademarks and fairness

- Other companies' product and channel names (for example Autel, Launch, X431, Thinktool, Gscan) are their trademarks. Use them only to describe what a video genuinely covers, never to imply endorsement, partnership or compatibility.
- Do not disparage competitors. See [competitor analysis](competitor-analysis.md#rules-for-using-competitor-research).

### Corrections after publication

1. Assess the error with the technical reviewer. Safety-relevant errors are handled first.
2. Correct publicly: a pinned comment and a note at the top of the description that states the correction.
3. If the video could lead to unsafe work, the channel owner decides whether to make it private or unlisted until it is fixed.
4. Record what happened in `item.yaml` → `corrections` (date, description, action, who); the log does not change the approval fingerprint. Add an action in `performance.yaml` when the lesson affects future content.
5. Do not edit the approved `script.md` of a published video. A re-edited or re-recorded video is a new content item with its own ID.

### Enforcement map

| Rule | Enforced by |
|---|---|
| Claims, sources, accepted evidence, Cartek 2 register | QC gate G3 |
| Clearing wording, code coverage, safety flags, review phrases | QC gate G5 |
| Performance promises, title/description/tag limits | QC gate G6 |
| Independent and human sign-off | Approval rules in [config/qc-policy.yaml](../config/qc-policy.yaml) |
| Judgment (clarity, fit, accuracy beyond patterns) | [content-qc-inspector](../skills/content-qc-inspector/SKILL.md) and [technical-fact-checker](../skills/technical-fact-checker/SKILL.md) |

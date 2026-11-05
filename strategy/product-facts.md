# Cartek 2 product facts

Why the Cartek 2 feature register exists, what it holds today, how the product team adds a verified feature, and the questions the content team needs answered.

Related: [feature register](../data/reference/cartek-2-feature-register.yaml) · [editorial guidelines](editorial-guidelines.md) · [content pillars](content-pillars.md) · [technical review workflow](../workflows/technical-review.md)

## From the sheet (source)

- The sheet names the product in pillar 1: "Hướng dẫn sử dụng thiết bị OBD2 (Cartek 2)" ('Content Direction'!B5).
- Four long-form ideas depend on it: CTK-L-0001 "Cách kết nối Cartek 2 với các dòng xe phổ biến tại Việt Nam" ('Content Direction'!D6), CTK-L-0002 "Đọc và hiểu các mã lỗi OBD2 trên cartek 2" (E6), CTK-L-0003 "Xóa mã lỗi và reset hệ thống" (F6) and CTK-L-0004 "Sử dụng các tính năng nâng cao của Cartek 2" (G6).
- The sheet documents **no** Cartek 2 functions, supported protocols, vehicle coverage, software versions or prices.

## Repository guidance (added 2026-11-05; editorial assumption, change freely)

### Why a register

Content about a company's own product is where unverified claims slip in most easily. A viewer who buys or uses Cartek 2 because of a video must be able to do what the video showed. The register is the single place where a capability becomes usable in content, and only with evidence.

### Current state

On 2026-11-05 the register is **empty** (`features: []`). Consequences:

- Any claim with `category: cartek-feature` is **BLOCKED** by QC gate G3, so no item that describes a Cartek 2 capability can be approved.
- Videos can still show diagnostic concepts and data with neutral wording ("máy chẩn đoán", "dữ liệu trực tiếp") as long as they claim nothing about what Cartek 2 can or cannot do.

### How QC uses the register

1. The writer registers each Cartek 2 statement as a claim in `item.yaml` with `category: cartek-feature` and the `feature_id` of the register entry.
2. Gate G3 blocks the claim when `feature_id` is missing, is not in the register, or its entry is not `status: verified`.
3. The claim itself also needs a source of type `cartek-product-documentation` or `hands-on-test` (`claim_source_requirements` in [config/qc-policy.yaml](../config/qc-policy.yaml)).
4. The [technical-fact-checker](../skills/technical-fact-checker/SKILL.md) checks that the script describes the feature within its recorded limitations and versions.

### Adding a verified feature (product team)

Edit [data/reference/cartek-2-feature-register.yaml](../data/reference/cartek-2-feature-register.yaml) in a pull request. One entry per feature:

| Field | Content |
|---|---|
| `id` | Next free ID: F001, F002… Never reuse an ID. |
| `name` | Short name as it should appear on screen. |
| `description` | What the feature does, in one or two sentences. |
| `status` | `verified`, `unverified` or `unsupported`. Only `verified` can be used in content. Record `unsupported` too, so nobody claims it later. |
| `standard_or_oem` | `obd-standard` (generic OBD-II function) or `manufacturer-specific` (enhanced function that depends on make and model). |
| `evidence.type` | `cartek-product-documentation` (manual, specification, written product-team confirmation) or `hands-on-test` (recorded test on a real vehicle). |
| `evidence.reference` | Where the evidence is: document and page, or test log with date and vehicle. |
| `evidence.date` | Date of the evidence (YYYY-MM-DD). |
| `evidence.confirmed_by` | Name and role of the person confirming. |
| `firmware_or_app_version` | Version the evidence applies to. Features can change between versions. |
| `vehicles_tested` | Make, model, year and engine of each vehicle tested. |
| `limitations` | Known unsupported makes, models, functions or conditions. |

Rules:

- One pull request per change, reviewed by someone from the product team and someone from the content team.
- A hands-on test records the date, the vehicle, the tool and app versions, what was done, and the result. Keep the log outside Git if it holds customer data.
- When a firmware or app update changes a feature, update the entry. Then re-run QC on items that cite it (`python3 scripts/qc_content.py run --all`).

### Open questions for the product team

These are questions, not facts. Answer them in the register (with evidence) or in a dated note in this section.

1. Which vehicle communication protocols does Cartek 2 support (for example ISO 15765-4 CAN, ISO 14230-4 KWP2000, ISO 9141-2, SAE J1850 PWM/VPW)?
2. Which makes, models and years sold in Vietnam has Cartek 2 been tested on, and with which results?
3. Which generic OBD-II services does it support: reading stored codes, pending codes, permanent codes, clearing codes, freeze frame, live data, readiness status, vehicle information?
4. Does it read anything beyond the engine (transmission, ABS, airbags, body modules)? On which makes?
5. Does it offer manufacturer-specific (enhanced) functions such as service resets, adaptations, coding or actuator tests? Which ones, on which vehicles?
6. Which hardware revision, firmware and app versions are current, and how do users update them?
7. How does Cartek 2 connect to the phone or display (for example Bluetooth, Wi-Fi, cable), and on which phone operating systems does the app run?
8. Can it record or export diagnostic sessions for use in videos?
9. Which code definitions does the app show: generic only, or manufacturer definitions too? What is their source?
10. What limitations or warnings should every Cartek 2 video state?
11. Who on the product team confirms new features, and how quickly?

# Automotive research reference

Orientation material for [SKILL.md](SKILL.md). It tells you where to look, not what to say: every statement used in content still needs its own source in `item.yaml`. Standards are paywalled documents; cite the edition you or a reliable secondary source actually used, and never invent clause or page numbers.

## Source hierarchy (strongest first)

| Rank | Source type (`config/taxonomy.yaml`) | Use it for | Examples |
|---|---|---|---|
| 1 | `standard`, `regulation` | OBD-II/EOBD behaviour, generic DTC definitions, communication protocols | SAE J1979 / ISO 15031-5 (diagnostic services), SAE J2012 / ISO 15031-6 (DTC definitions), ISO 15765-4 (OBD on CAN), US EPA / CARB OBD-II regulations, EU type-approval rules for EOBD |
| 2 | `oem-service-information`, `oem-tsb` | Manufacturer-specific codes, procedures, specifications, model-year changes | The make's workshop manual and technical service bulletins for the exact model, year and engine |
| 3 | `manufacturer-documentation` | Component or tool behaviour (not Cartek) | Ignition-component or scan-tool maker documentation |
| 4 | `cartek-product-documentation`, `hands-on-test` | Cartek 2 capabilities (also need a verified feature-register entry) | Official Cartek documentation, written product-team confirmation, a dated test log naming vehicle and software version |
| 5 | `textbook`, `trade-publication` | General system explanations, training-level theory | Automotive engineering textbooks, vocational curricula |
| 6 | `expert-interview` | Field practice, context | A named technician, recorded and dated |
| 7 | `news` | Market and industry news (pillar P5) | Dated news articles |
| 8 | `other` | Leads only | Forums, social posts, videos. Never sufficient alone |

Accepted source types per claim category are set in `config/qc-policy.yaml` (`claim_source_requirements`). QC gate G3 fails a `verified` claim that lacks an accepted type.

## OBD-II diagnostic services (SAE J1979 / ISO 15031-5)

Use this table to classify statements as standard behaviour. Confirm the details for a claim against the standard or a reliable secondary source, and remember a vehicle may not support every service or PID.

| Service | Purpose |
|---|---|
| $01 | Current powertrain diagnostic data (PIDs, live data) |
| $02 | Freeze frame data stored with a DTC |
| $03 | Stored (confirmed) emission-related DTCs |
| $04 | Clear/reset emission-related diagnostic information |
| $05 | Oxygen sensor monitoring test results (non-CAN vehicles) |
| $06 | On-board monitoring test results for specific monitored systems |
| $07 | Pending DTCs (detected during the current or last driving cycle) |
| $08 | Control of on-board system, test or component |
| $09 | Vehicle information (e.g. VIN, calibration IDs) |
| $0A | Permanent DTCs (on vehicles that support them) |

Communication protocols seen on OBD-II vehicles include SAE J1850 (PWM/VPW), ISO 9141-2, ISO 14230-4 (KWP2000) and ISO 15765-4 (CAN). Which one a given vehicle uses is vehicle-specific: verify it.

## DTC structure (SAE J2012 / ISO 15031-6)

- First character: system. `P` powertrain, `B` body, `C` chassis, `U` network.
- Second character: who defines the code. `0` is a generic (SAE/ISO-defined) code. Ranges such as `P1xxx`, `P30xx-P33xx`, `B1/B2`, `C1/C2` and `U1/U2` are manufacturer-controlled in the default policy (`manufacturer_specific_dtc_patterns`). Verify the exact ranges against the current standard before stating them in content.
- A manufacturer-controlled code needs the make/model/year whose service information defines it; QC gate G5 fails such a code on a `generic` item.

## Codes versus root causes

A DTC records that the control unit detected a condition. It does not name the failed part. For each candidate cause, write the test that would confirm it and the source of that test procedure. Typical structure for a misfire topic (illustrative; every row needs its own verified claim):

| Code | Candidate cause group | Confirming test | Source needed |
|---|---|---|---|
| Misfire code | Ignition | OEM ignition test for the vehicle | OEM service information |
| Misfire code | Fuel delivery | OEM fuel-system test | OEM service information |
| Misfire code | Air/vacuum leak | Smoke test or fuel-trim analysis | Textbook or OEM |
| Misfire code | Mechanical (compression) | Compression/leak-down test | Textbook or OEM |

## Clearing codes

When content mentions clearing codes, register claims that say what clearing does and does not do (Service $04), and that a fault returns while its cause remains. QC gate G5 fails narration that mentions clearing without that caveat, and fails wording that presents clearing as a repair.

## Vehicle and market differences

- OBD-II and EOBD requirements come from US and EU regulation. Do not assume they describe every vehicle sold in Vietnam: check the vehicle's market, model year and engine.
- Diesel, hybrid and EV systems differ from gasoline ones; high-voltage systems need the `high-voltage` safety flag and a qualified human technical review.

## Writing claims that can be checked

- One fact per claim, phrased the way the script will say it.
- Avoid absolute words ("luôn luôn", "100%", "tất cả các dòng xe") unless the source says exactly that.
- Name the scope inside the claim when it is vehicle-specific: "Trên Toyota Vios 2018 1.5L (theo tài liệu sửa chữa của hãng)…".

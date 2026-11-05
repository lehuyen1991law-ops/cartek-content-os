# data/

Spreadsheet data in three layers, plus reference data. Everything here except `reference/` is written by [`scripts/import_sheet.py`](../scripts/import_sheet.py): do not edit it by hand. The importer refuses to overwrite a generated file that was edited by hand (exit code 2), and `validate_content.py` reports such edits as errors.

| Path | Layer | Content |
|---|---|---|
| `source/*.json` | Raw | One snapshot per tab, values exactly as captured (formatted values, hyperlinks, notes, data-validation rules, capture method and time). Long runs of identical rows are stored as `{"repeat": n, "row": [...]}`. Schema: [source-snapshot](../schemas/source-snapshot.schema.json). |
| `normalized/*.json` | Normalized | Stable records with cell-level provenance (`source.ref`, e.g. `'Content Direction'!F12`). Schema: [normalized-data](../schemas/normalized-data.schema.json). |
| `id-registry.json` | IDs | Permanent content IDs. Never reused; records that disappear upstream become `missing-upstream`. Test IDs use 9001–9999. |
| `import-manifest.json` | Audit | Per-tab hashes, grid sizes, populated ranges, issue counts, output hashes (used to detect hand edits), linked spreadsheets. |
| `reference/cartek-2-feature-register.yaml` | Reference | The only allowed source of Cartek 2 capabilities. Maintained by hand by the product team ([process](../strategy/product-facts.md)). |

## Normalized files

| File | From tab(s) | Records |
|---|---|---|
| `competitors.json` | Đối thủ | 5 competitor channels; reach metrics flagged `historical-unverified` |
| `personas.json` | Khán giả | 4 personas (`garage-owner`, `technician`, `automotive-student`, `car-owner`) |
| `channel.json` | Content Direction, Short | Channel topic, video types, durations, CTAs, linked resources |
| `taxonomy.json` | Content Direction, Short | Pillars P1–P5, Shorts categories S1–S4 |
| `ideas.json` | Content Direction, Short | 28 planning ideas with IDs |
| `tracker.json` | Video Publish, Short Publish | Row classification and production records (currently none) |

The full reconciliation is in [reports/import-report.md](../reports/import-report.md). How to refresh: [workflows/sheet-import.md](../workflows/sheet-import.md).

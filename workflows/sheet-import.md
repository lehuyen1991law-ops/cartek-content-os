# Sheet import

How the Google Sheet "Cartek: Youtube Release" becomes versioned data in this repository. The import is **read-only**: no command writes to the spreadsheet. It never writes into `content/` either.

**Skills used:** none required. Any agent can run it; [cartek-content-strategist](../skills/cartek-content-strategist/SKILL.md) uses the results.

**Done when:** `python3 scripts/import_sheet.py --check` passes, [reports/import-report.md](../reports/import-report.md) shows every tab as `imported`, and every warning in it has been read.

## What each tab becomes

Configured in [config/sources.yaml](../config/sources.yaml). Raw snapshots live in `data/source/`, normalized records in `data/normalized/`.

| Tab | Raw snapshot | Normalized output | Content |
|---|---|---|---|
| Đối thủ | `data/source/00-doi-thu.json` | [competitors.json](../data/normalized/competitors.json) | 5 competitor channels; reach metrics flagged `historical-unverified` |
| Khán giả | `data/source/01-khan-gia.json` | [personas.json](../data/normalized/personas.json) | 4 personas; "Chủ xe ô tô (ít)" becomes `car-owner` with priority `low` |
| Content Direction | `data/source/02-content-direction.json` | [channel.json](../data/normalized/channel.json), [taxonomy.json](../data/normalized/taxonomy.json), [ideas.json](../data/normalized/ideas.json) | Channel topic, video types, 5-8 phút, long-form CTA, pillars P1-P5, 16 ideas |
| Short | `data/source/03-short.json` | channel.json, taxonomy.json, ideas.json | < 60 giây, Shorts CTA, categories S1-S4, 12 ideas |
| Video Publish | `data/source/04-video-publish.json` | [tracker.json](../data/normalized/tracker.json) | Long-form tracker rows, classified |
| Short Publish | `data/source/05-short-publish.json` | tracker.json | Shorts tracker rows, classified |

Every normalized record keeps its provenance: tab, sheet ID and cell reference, for example `'Content Direction'!F12`. Values that changed during cleaning keep the raw cell value.

Also written: `data/id-registry.json` (permanent IDs), `data/import-manifest.json` (hashes of every output), and `reports/import-report.md`.

## Commands

```bash
python3 scripts/import_sheet.py                    # re-normalize the committed snapshots (offline)
python3 scripts/import_sheet.py --check            # CI: fail if committed outputs are stale; writes nothing
python3 scripts/import_sheet.py --fetch api        # capture the live sheet via the Sheets API, then normalize
python3 scripts/import_sheet.py --fetch csv        # capture via public CSV export (link-shared sheets only)
python3 scripts/import_sheet.py --snapshot-file <bundle.json>   # ingest a capture bundle, then normalize
python3 scripts/import_sheet.py --force            # overwrite generated files that were edited by hand
```

| Exit code | Meaning |
|---|---|
| 0 | Done, or already up to date |
| 1 | Error-level issues, an invalid capture bundle, or stale outputs with `--check` |
| 2 | Generated files were edited by hand; nothing was written |

## Capture methods

All methods only read. They produce a *capture bundle* ([schemas/source-capture.schema.json](../schemas/source-capture.schema.json)) that is validated, then stored tab by tab.

### 1. Sheets API (`--fetch api`)

- Credentials come from the environment, or from a local `.env` file at the repository root that never goes into Git. Existing environment variables win over `.env`.
  - `GOOGLE_OAUTH_ACCESS_TOKEN`: an OAuth access token with read access to the sheet.
  - `GOOGLE_API_KEY`: works only when the sheet is shared "anyone with the link".
- Every request is a GET to `sheets.googleapis.com`: sheet metadata, formatted values per tab, then hyperlinks, notes and data-validation rules from the grid data.
- Never commit tokens, keys, service-account files or `.env`.

### 2. CSV export (`--fetch csv`)

- Works only for link-shared sheets. A private sheet returns a sign-in page; the command stops with an error.
- CSV cannot carry hyperlinks, notes or validation rules. Those are carried over from the previous snapshot and the snapshot notes say so.
- In the 2026-11-05 build environment the network proxy blocked `docs.google.com` (`CONNECT tunnel failed, response 403`), so this method was not available there.

### 3. Capture bundle (`--snapshot-file`)

Use this when an AI agent can read the sheet through a Google Sheets connector. The 2026-11-05 capture was made this way (`capture_method: google-sheets-connector (values.get FORMATTED_VALUE + spreadsheets.get gridData)`).

1. Read the spreadsheet properties and each tab's `sheetId`, `title`, `index` and grid size (`spreadsheets.get`, fields `properties` and `sheets.properties`).
2. For every tab, read the whole tab with `values.get` (formatted values). Keep values exactly: leading and trailing spaces included. Dates stay as the sheet shows them (dd/MM/yyyy).
3. Read hyperlinks, notes and validation rules with `spreadsheets.get`, `includeGridData` true, fields `sheets.data.rowData.values.hyperlink`, `.note` and `.dataValidation` over the populated range. The field `sheets.dataValidations` does not exist; ask per cell.
4. Assemble the bundle:

```json
{
  "capture_format": 1,
  "spreadsheet": {"id": "1r4dfNOPGx50rXMuhZL6Tm0B5XG8nb47t7mSjVdDY-F4", "title": "Cartek: Youtube Release", "locale": "en_US", "time_zone": "America/Los_Angeles"},
  "captured_at": "2026-11-05T06:10:44Z",
  "capture_method": "google-sheets-connector (values.get FORMATTED_VALUE + spreadsheets.get gridData)",
  "capture_notes": ["what was read, when, and what was verified"],
  "tabs": [
    {
      "sheet_id": 2144511491, "title": "Video Publish", "index": 4,
      "grid": {"row_count": 1015, "column_count": 27, "frozen_row_count": 1},
      "values": [["Tiêu đề", "Thể loại", "Hãng xe"], [], {"repeat": 1007, "row": ["", "", "0"]}],
      "hyperlinks": {}, "notes": {}, "data_validation": [],
      "capture_notes": ["ranges checked for hyperlinks/notes/validation"]
    }
  ]
}
```

   - `hyperlinks` and `notes` map A1 references to text, e.g. `{"B2": "https://..."}`; `data_validation` lists `{"ref": "F2", "rule": {...}}`.
   - A long block of identical rows may be written as `{"repeat": n, "row": [...]}`. Verify the block first with targeted reads (empty ranges and the last row) and say so in `capture_notes`.
   - `captured_at` is UTC in the form `YYYY-MM-DDTHH:MM:SSZ`.
5. Save the bundle outside the repository (a scratch folder), then run `python3 scripts/import_sheet.py --snapshot-file <path>`.

The spreadsheet ID in the bundle must match [config/sources.yaml](../config/sources.yaml); otherwise the import stops.

## Idempotency

- A captured tab whose content hash is unchanged keeps its existing snapshot file, including its original capture time. The hash covers values, hyperlinks, notes, validation rules, grid size, title and sheet ID; not the capture time.
- Normalization is deterministic. Running the import twice writes nothing the second time.
- The report and manifest describe state, not "what happened in this run", so `--check` stays green after a normal import.

## Stable IDs

[data/id-registry.json](../data/id-registry.json) holds every ID ever issued.

- Planning ideas get `CTK-L-0001`… (long-form) and `CTK-S-0001`… (Shorts) in sheet order on first import.
- An idea is recognised by its format and its title (case and spacing aside). Moving it to another cell keeps its ID.
- Editing a title in place between two imports keeps the ID; the old title goes to `previous_titles`.
- An idea that disappears becomes `missing-upstream`. Its ID is never reused. If the same title returns, the ID is reactivated.
- A tracker row that names a registered content ID (for example `CTK-L-0015` in "Kịch bản") is linked to that ID (`link_method: explicit-id`). Otherwise a row whose title equals an idea title of the same format reuses the idea's ID (`link_method: title`). Any other titled row gets a new ID with origin `sheet-tracker` (`link_method: new-tracker-id`). See [publishing.md](publishing.md#how-the-import-links-the-sheet-row-to-the-content-id).
- `new_content.py` allocates IDs for manual items (`manual`) and test items (`test`, numbers 9001-9999) in the same registry.

## Tracker row classification

Rows 2+ of `Video Publish` and `Short Publish` are classified ([scripts/ctk/sheet.py](../scripts/ctk/sheet.py) → `parse_tracker`). Placeholder values are `0`, `NONE`, `N/A`, `-`, `--`.

| Classification | Rule | Result |
|---|---|---|
| `production-record` | has a real title ("Tiêu đề") | imported with checks (below) |
| `incomplete-record` | no title, but a date, link or script | warning `record-without-title`; not imported |
| `template-example` | category/status/brand values but no title, date or link | not imported; a "Đã xuất bản" example gets an info note |
| `placeholder-filler` | only placeholder values | ignored |
| `blank` | every cell empty or whitespace | ignored |

Checks on production records: unknown category or status, invalid date (expects dd/MM/yyyy), date before 2005-04-23, non-YouTube or invalid link, duplicate titles, and "Đã xuất bản" without both date and link (`published-without-evidence`; not treated as published).

On 2026-11-05 both trackers held 6 template rows, 1 blank row and 1,007 filler rows each: **0 production records**.

## Protection of local edits

- Generated files (`data/normalized/*.json`, `reports/import-report.md`) carry their hash in `data/import-manifest.json`. If one was edited by hand, the import stops with exit code 2 and writes nothing.
- Move the edit to where it belongs: `content/` for editorial work, `config/` for mappings. Or discard it with `--force`.
- `scripts/validate_content.py` also reports hand-edited generated files as errors.
- Editorial workspaces are never written. When an upstream idea changes, the import prints a `workspace drift` line and `validate_content.py` warns; a person decides what to change.

## Continuous integration

CI runs `python3 scripts/import_sheet.py --check` offline against the committed snapshots. It needs no Google credentials. A failure means someone changed snapshots, config or code without re-running the import.

## Linked spreadsheet (audited, not imported)

`'Content Direction'!D1` links to a second spreadsheet, "Cartek_Youtube Channel" (`10gh0Fd2VK6lrZFizf3SNkTSV7rMhve7V0bSaFzihevI`). It was read on 2026-11-05 and holds only sample data: example tracker rows without titles or links (one marked published with the date 28/08/1999) and five identical sample vehicle tabs. It is listed in [config/sources.yaml](../config/sources.yaml) → `linked_sources` with `import: false`. If the team starts using it, add it as a source deliberately.

## Adding or changing a tab

1. **Same layout as an existing tab** (another tracker, for example): add an entry under `tabs` in [config/sources.yaml](../config/sources.yaml) with `title`, `sheet_id`, `parser` (`competitors`, `personas`, `long-form-direction`, `short-direction` or `tracker` with `format`), `snapshot` (`data/source/NN-slug.json`) and `outputs`. Capture and import.
2. **New column or row label:** add it to `tracker_columns`, `competitor_fields`, `persona_fields` or `direction_fields` in the same file. Unmapped labels are kept under `extra` and reported.
3. **New persona:** add its canonical ID and the sheet name to [config/taxonomy.yaml](../config/taxonomy.yaml) → `personas`.
4. **New layout:** write a parser in [scripts/ctk/sheet.py](../scripts/ctk/sheet.py), wire it into `build()` in [scripts/ctk/importer.py](../scripts/ctk/importer.py), add its output kind to [schemas/normalized-data.schema.json](../schemas/normalized-data.schema.json), and add tests to `tests/test_import.py`.

Until a tab is configured, a capture stores its raw snapshot as `data/source/extra-<sheet-id>-<slug>.json` and the report lists it as unconfigured.

## Reading the report

[reports/import-report.md](../reports/import-report.md) lists, per tab: grid size, populated range, non-empty cells, status (`imported`, `blocked` when the snapshot is missing, `error`), records and issue counts. It then shows the tracker reconciliation row by row, all sheet IDs with their state, and every issue with its cell reference. Read every warning before relying on new data.

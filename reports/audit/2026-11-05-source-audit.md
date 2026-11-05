# Source and environment audit — 2026-11-05

Phase 1 audit performed by Claude Code before building the repository. Point-in-time record: do not edit; add a new dated audit for later checks.

## Environment

| Check | Result |
|---|---|
| Local repository | `/home/user/cartek-content-os`, existing clone with one commit (`3b3b075`, README "Cartek INNOVA"). No other project files, so nothing could be overwritten. |
| GitHub repository | `lehuyen1991law-ops/cartek-content-os` already exists and is **private** (GitHub search API: `"private": true`). Default branch `main`. |
| Working branch | `claude/epic-turing-1lotwr` (designated for this session) |
| Git | 2.43.0. HTTPS fetch/push works through the environment's authenticated git proxy. |
| GitHub CLI | `gh` 2.89.0 installed, but `gh auth status` reports the token in `GH_TOKEN` as invalid. Repository creation through `gh` was therefore not possible; it was not needed because the repository exists. |
| GitHub connector | Authenticated as `lehuyen1991law-ops`; used for read-only verification. |
| Python | 3.13; PyYAML and jsonschema available; pytest not installed, so tests use the standard `unittest`. |

## Spreadsheet access

| Method | Result |
|---|---|
| Google Sheets connector | Works: spreadsheet metadata, `values.get` (formatted values) and `spreadsheets.get` grid data (hyperlinks, notes, data validation, formats). Used for the capture. |
| Google Drive connector | `get_file_metadata` returned "Requested entity was not found": no Drive-level access, so no file modification time or comments. |
| Public CSV export | Blocked by the environment's network proxy (`CONNECT tunnel failed, response 403` for docs.google.com). |
| Sheets API with own credentials | No Google OAuth token for the user's sheet in this environment. The importer supports it (`--fetch api`) for later use. |

The sheet was only read. Nothing was written to it.

## Spreadsheet: "Cartek: Youtube Release"

ID `1r4dfNOPGx50rXMuhZL6Tm0B5XG8nb47t7mSjVdDY-F4`, locale `en_US`, time zone `America/Los_Angeles`.

| # | Tab | Sheet ID | Grid | Frozen rows | Populated range | Non-empty cells | Layout |
|---|---|---|---|---|---|---|---|
| 0 | Đối thủ | 331744519 | 997×25 | 0 | A1:F8 | 43 | Transposed: labels in A, five competitors in B–F |
| 1 | Khán giả | 546980374 | 998×25 | 0 | A1:E6 | 30 | Transposed: labels in A, four personas in B–E |
| 2 | Content Direction | 991115479 | 996×24 | 0 | A1:G13 | 40 | Settings rows 1–4; pillar rows with ideas in D–G |
| 3 | Short | 1717813101 | 997×25 | 0 | A1:F11 | 30 | Settings rows 1–3; category rows with ideas in D–F |
| 4 | Video Publish | 2144511491 | 1015×27 | 1 | A1:I1015 | 1037 | Tracker: header row, example rows, filler |
| 5 | Short Publish | 1044477468 | 1015×27 | 1 | A1:I1015 | 1037 | Tracker: header row, example rows, filler |

### Findings per tab

- **Đối thủ**: five channels (Ecuboot, OBD Viet Nam, ASCOM - Thiết bị Garage, Kênh kiến thức ô tô, VATC - Huấn luyện kỹ thuật ô tô) with link, content strategy, reach metrics, strengths, weaknesses and keywords. Links in B2:F2 are real hyperlinks. C8 holds a single space. The reach metrics have no date: they are treated as historical and unverified.
- **Khán giả**: four personas with demographics, interests, pain points, online behaviour and preferred content. The fourth is labelled "Chủ xe ô tô (ít)".
- **Content Direction**: channel topic (B1) with a hyperlink in D1 to a second spreadsheet, video types, "5-8 phút", the long-form CTA, five pillars and 16 ideas (four each for pillars 1–4; pillar 5 has none). The CTA spells "subcribe".
- **Short**: video types, "< 60 giây", CTA "Cartek - Check your car", four categories and 12 ideas. Category 2 is written "Giới thiệu sản phẩm/ thiết bị" in B6 and "Giới thiệu sản phẩm/thiết bị" in D6.
- **Video Publish / Short Publish**: header `Tiêu đề, Thể loại, Hãng xe, Model, Người phụ trách, Trạng thái, Ngày đăng, Kịch bản, Link xuất bản`. Rows 2–7 have no title, date, script or link: they show one example per category/status (owner "NONE"). Rows 2–7 include "Đã xuất bản" statuses without any publishing evidence. Row 8 is empty. Rows 9–1015 hold only the literal text "0" in column C. Sampled formats: C and D plain text, G date `dd/MM/yyyy`.

### Formulas, validation, notes

- No formulas in the checked ranges (all user-entered values are text). The "0" filler is literal text (checked at C9, C10, C500, C501).
- No data-validation rules were returned for the checked ranges, so statuses and categories are typed values, not enforced dropdowns.
- No cell notes.

### Linked spreadsheet "Cartek_Youtube Channel"

ID `10gh0Fd2VK6lrZFizf3SNkTSV7rMhve7V0bSaFzihevI`, linked from `'Content Direction'!D1`. Tabs: VIDEO PUBLISH, Short, How-To Tutorials, Intro - Function, Promo, Q&A. VIDEO PUBLISH has six example rows without titles or links (one marked published on 28/08/1999, an impossible YouTube date); the other five tabs repeat the same five sample vehicle rows. It holds no verifiable production records and is outside the declared source of truth, so it was audited and not imported.

## Decisions

1. Capture through the Sheets connector; store raw values per tab in `data/source/` with capture notes; normalize separately.
2. The 28 ideas are real planning entries: each gets a permanent ID and a `planning-idea` record. They are not videos.
3. Tracker rows without a title are classified (template-example, placeholder-filler, blank) and not imported. A status of "Đã xuất bản" never counts without a date and a link.
4. Competitor metrics stay labelled historical and unverified.
5. No Cartek 2 capability is documented in the sheet, so the feature register starts empty and QC blocks product claims.
6. The existing private repository is used; work is pushed to the designated branch.

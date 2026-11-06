# Publishing

From an approved item to a live video, a recorded URL and an updated sheet. Nothing in this repository uploads to YouTube or writes to the spreadsheet: both are human steps.

**Skills used:** none required. A producer/editor uploads; [youtube-seo-specialist](../skills/youtube-seo-specialist/SKILL.md) can help check metadata.

**Done when:** the video is live, `item.yaml` records the real URL and publish date (stage `PUBLISHED`), the sheet row is updated by hand, the import has been re-run, and `scripts/validate_content.py` reports no errors.

## Before you start

1. The item is `APPROVED`: `qc_content.py approve` set it, and the approval still matches the content.

```bash
python3 scripts/qc_content.py status <ID>
```

2. The pre-approval checklist in `seo.md` was ticked before approval (gate G8 requires it). Do not edit `brief.md`, `research.md`, `script.md`, `seo.md`, `storyboard.md` or the fingerprinted fields of `item.yaml` after approval: any change voids the approval and `set_status.py` will refuse to publish. If something must change, go back through QC.
3. Fields you may still change after approval without voiding it: `owner`, `target_publish_date`, `publication` (including `publication.upload_checklist`), `corrections`, `internal_notes`.

## Procedure

1. **Release package.** `qc_content.py approve` already wrote `exports/production-package.json` (`package_status: APPROVED`). Regenerate it if needed:

```bash
python3 scripts/export_package.py <ID>
```

   The command refuses test items, unapproved items and stale approvals. Production consumers must reject any package whose `package_status` is not `APPROVED` ([schemas/production-package.schema.json](../schemas/production-package.schema.json)).

2. **Produce the video** from the package: narration, shot list, on-screen text, B-roll, assets, timing, and `visual_style` (fonts, typography roles, effects with their "never use" notes, mandatory captions; see [strategy/visual-identity.md](../strategy/visual-identity.md)).
3. **Upload by hand in YouTube Studio.** Copy the values from the release package (`exports/production-package.json` → `seo`):
   - Title: `seo.title`.
   - Description: `seo.description_with_chapters` (the description followed by one chapter line per chapter, "00:00 Mở đầu"). YouTube builds chapters from those lines; gate G6 already checked that the whole text fits 5,000 characters.
   - Tags: `seo.tags`; hashtags: `seo.hashtags`.
   - Thumbnail: the chosen concept from `seo.thumbnail_concepts`.
   - Visibility: `publication.visibility_plan`; playlist: `publication.playlist`.
   - End screen, cards (`seo.related_content`) and pinned comment (`seo.pinned_comment`).
4. **Work through the upload checklist** in `item.yaml` → `publication.upload_checklist` (approved cut uploaded, metadata pasted, thumbnail, end screen and cards, Vietnamese captions checked against the final voice-over, visibility or schedule, pinned comment). Set `done: true` on each step only when it is true. These steps happen after approval, so they live outside the content fingerprint and do not void it.
5. **Record the publication** with the real URL and the real date (not in the future):

```bash
python3 scripts/set_status.py <ID> --stage PUBLISHED --url "https://youtu.be/<video-id>" --date YYYY-MM-DD --by "<name>"
```

   The command refuses test items, items not at `APPROVED` (or already `PUBLISHED`, to correct the record), approvals that no longer match the content, an unfinished upload checklist, non-YouTube URLs and future dates. It prints the matching sheet status: `Đã xuất bản`.

6. **Update the spreadsheet by hand.** In "Cartek: Youtube Release", tab `Video Publish` (long-form) or `Short Publish` (Shorts), fill one row:

| Column | Value |
|---|---|
| Tiêu đề | The published title |
| Thể loại | The pillar or category name exactly as in the sheet (e.g. "Kiến thức chuyên sâu về hệ thống OBD2") |
| Hãng xe | Brand, upper case as the sheet uses (e.g. TOYOTA), or leave empty for generic content |
| Model | Model, if any |
| Người phụ trách | The owner |
| Trạng thái | Đã xuất bản |
| Ngày đăng | Publish date as dd/MM/yyyy (e.g. 01/12/2026) |
| Kịch bản | The content ID (e.g. "CTK-L-0015"), optionally followed by a link to the script. The importer reads the ID from this column. |
| Link xuất bản | The YouTube URL |

   A row counts as published in the repository only with both "Ngày đăng" and "Link xuất bản".

7. **Record where the row is** in `item.yaml` → `publication.sheet_row`, for example `"'Video Publish'!A12"`.
8. **Re-run the import** so `data/normalized/tracker.json` reflects the row (see [sheet-import.md](sheet-import.md)). Then validate and refresh the board:

```bash
python3 scripts/import_sheet.py --fetch api
python3 scripts/validate_content.py
python3 scripts/generate_board.py
```

   Without API credentials, capture the sheet another way ([sheet-import.md](sheet-import.md#capture-methods)) and use `--snapshot-file`.

## How the import links the sheet row to the content ID

The importer links a tracker row to a content ID in this order:

1. **Explicit ID.** A registered content ID of the right format written anywhere in the row ("Kịch bản" is the convention, "Tiêu đề" also works). `link_method: explicit-id` in `data/normalized/tracker.json`. An unregistered ID is reported as a warning and ignored.
2. **Title match.** "Tiêu đề" equals the title of a planning idea of the same format (case and spacing aside). `link_method: title`.
3. **New ID.** Otherwise the row gets a new ID with origin `sheet-tracker` (`link_method: new-tracker-id`).

The published title usually differs from the idea's working title, so always write the content ID in "Kịch bản". Check [reports/import-report.md](../reports/import-report.md) after the import.

## Corrections after publishing

Two kinds of change are supported:

**A. Corrections communicated on YouTube** (factual or safety errors in a live video):

1. Make the correction on YouTube (pinned comment, description note, cards). Do it quickly.
2. Log it in `item.yaml` → `corrections` with `date`, `description`, `action` and `by`. The log is outside the content fingerprint: the approved record of what was published stays intact.
3. Open an editorial review issue so the lesson reaches [strategy/editorial-guidelines.md](../strategy/editorial-guidelines.md) and future briefs.
4. If the video itself is wrong, plan a corrected video as a new item that references the old one in `seo.related_content`.

**B. Changes to the published metadata** (for example a new title or thumbnail after a performance review):

1. Edit the `seo` block and `seo.md` in a branch. `validate_content.py` reports the published item as changed since approval: that is expected until re-approval.
2. Re-run QC and record the reviews again (`qc_content.py run`, `qc_content.py review`), with a human editorial sign-off.
3. Re-approve with `python3 scripts/qc_content.py approve <ID> --by "<name>"`. For a published item the stage stays `PUBLISHED` (or `PERFORMANCE_REVIEW`); the history records the re-approval and a new release package is written.
4. Apply the change in YouTube Studio and note the date in `performance.yaml` → `actions`, so later snapshots can be compared.

Merge the edit and the re-approval in the same pull request: CI fails in between.

## What QC checks (G8)

[scripts/ctk/qc.py](../scripts/ctk/qc.py) → `gate_g8`:

- `target_publish_date` and `publication.visibility_plan` are set (else FAIL).
- `seo.md` has a pre-approval checklist under "Publishing checklist" (else FAIL) and every item is ticked (else BLOCKED). Upload steps are checked by `set_status.py`, not by G8.
- At `PUBLISHED` or `PERFORMANCE_REVIEW`: `publication.url` is a YouTube URL and `publication.published_at` is set and not in the future (else FAIL).
- Before publishing: no URL or publish date may be recorded (else FAIL).

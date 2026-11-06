# Changelog

All notable changes to this repository. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Content items record their own history in `item.yaml`.

## [1.1.0] - 2026-11-06

### Added

- Visual style layer: `config/visual-style.yaml` (repository default, not a sheet value) with typography roles (`caption`, `lower_third`, `callout`, `dtc_code`, `live_data_number`, `end_screen`), OFL fonts with Vietnamese coverage status (Be Vietnam Pro, Inter, JetBrains Mono, Roboto Mono), placeholder colour tokens, an effects library (`hard-cut`, `soft-dissolve`, `code-popup`, `highlight-circle`, `highlight-arrow`, `zoom-punch`, `lower-third`, `safety-banner`, `freeze-frame-snapshot`, `checklist-tick`, `sfx-whoosh`, `sfx-ui-click`, `sfx-ui-beep`, `sfx-low-thud`), sound rules and mandatory caption rules; explained in `strategy/visual-identity.md`.
- `templates/storyboard.md`: shot-list columns `Effects` and `Text style`, sections "Sound and effects" and "Typography".
- Gate G7 warnings (never FAIL): unknown effect id, unknown typography role, a safety segment without a `safety-banner` shot (only when the storyboard declares effects at all; an old storyboard without the column gets the INFO line instead), an effect above its suggested maximum; INFO line listing the effects used.
- Production package `visual_style` section (fonts, roles and effects used with descriptions, caption and sound rules, source file); schema updated, `typography_roles_used` items declare `weight`, `size_px_1080p`, `colour`, `max_lines`, `max_chars_per_line` and allow no extra properties.
- `config/qc-policy.yaml` → `brand_mark_mentions` and `brand_mark_followers`: gate G5 no longer fails a segment for "Logo Cartek" or the Cartek end screen when the clause ends after the mark or continues with a placement word ("ở góc trên phải", "với video liên quan"); a capability statement in the same clause ("Thương hiệu Cartek chẩn đoán được mọi xe") or anything about Cartek 2 still needs a `cartek-feature` claim.

### Changed

- `storyboard.md` edits (including the new columns) change the full and the technical fingerprint, as before; `config/visual-style.yaml` is not fingerprinted, so release packages must be re-exported after a library change.

## [1.0.0] - 2026-11-05

### Added

- Read-only import of all six tabs of "Cartek: Youtube Release" (`scripts/import_sheet.py`): raw snapshots, normalized records with cell provenance, permanent content IDs, import manifest and reconciliation report.
- 28 planning ideas registered as `CTK-L-0001`–`CTK-L-0016` and `CTK-S-0001`–`CTK-S-0012`; publishing trackers classified (template/example rows only, no production records).
- Content workspace model (`item.yaml` + Markdown deliverables), JSON Schemas, templates for brief, research, long-form and Shorts scripts, SEO package, storyboard, QC report, review and performance records.
- QC gates G1–G8 with PASS/FAIL/BLOCKED evidence, fingerprint-bound independent reviews, human sign-off and guarded approval/publication.
- Production package export (`cartek.production-package/v1`) for external video systems.
- Strategy documents, eight workflows, seven Agent Skills, `CLAUDE.md`, content board, CI workflow, issue and PR templates.
- Cartek 2 feature register (empty pending product-team verification).
- Acceptance test item `CTK-L-9001` (test only, based on idea `CTK-L-0015`).

# Changelog

All notable changes to this repository. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Content items record their own history in `item.yaml`.

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

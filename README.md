# cartek-content-os

Cartek INNOVA — Content Operations System for the Cartek YouTube channel.

This repository turns the planning spreadsheet **"Cartek: Youtube Release"** into a versioned editorial workspace. It imports the sheet read-only, gives every idea a permanent content ID, and runs each video from idea to publication through templates, AI agent skills and independent quality gates. Content is in Vietnamese; the operating docs are in English.

- **Agents start here:** [CLAUDE.md](CLAUDE.md)
- **People start here:** this file, then [workflows/idea-to-publish.md](workflows/idea-to-publish.md)

## What is in it

| Path | Purpose |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Operating guide for Claude Code and other agents |
| [strategy/](strategy/) | Positioning, pillars, personas, competitors, editorial rules, brand voice, product facts |
| [data/](data/README.md) | Raw sheet snapshots, normalized records, ID registry, import manifest, Cartek 2 feature register |
| [content/](content/README.md) | One workspace per video: `item.yaml`, brief, research, script, SEO, storyboard, QC report, exports |
| [templates/](templates/) | Starting files for every deliverable |
| [workflows/](workflows/) | Step-by-step procedures from idea to post-publish analysis |
| [skills/](skills/) | Seven Agent Skills (also linked from `.claude/skills/`) |
| [schemas/](schemas/) | JSON Schemas: content record, production package, performance data, source data |
| [config/](config/) | Workflow stages, QC policy, platform limits, taxonomy, production assumptions, sheet source |
| [scripts/](scripts/) | Import, scaffolding, QC, export, board, validation (Python standard library + PyYAML + jsonschema) |
| [reports/](reports/README.md) | Import report, content board, audit and acceptance reports |
| [tests/](tests/) | Unit and integration tests (`unittest`) |

## Quick start

Requires Python 3.10+ and two packages.

```bash
pip install -r requirements.txt
```

```bash
make check
```

```bash
python3 scripts/new_content.py --list-ideas
```

```bash
python3 scripts/new_content.py --from-idea CTK-L-0015 --audience technician --owner "Tên người phụ trách"
```

```bash
python3 scripts/qc_content.py run CTK-L-0015
```

Everything works offline from the committed snapshots. Only a live re-capture of the sheet needs credentials (see [workflows/sheet-import.md](workflows/sheet-import.md) and `.env.example`).

## The workflow

```
IDEA → RESEARCH → BRIEF → SCRIPT → TECHNICAL_REVIEW → SEO → PRODUCTION_PACKAGE → QC → APPROVED → PUBLISHED → PERFORMANCE_REVIEW
```

- Sheet statuses map onto these stages: `Mới` = IDEA, `Đang thực hiện` = any working stage, `Đã tạm dừng` = on hold, `Đã xuất bản` = PUBLISHED (only with a real date and link).
- Eight QC gates (G1–G8) return PASS, FAIL or BLOCKED with evidence. Approval also needs independent reviews on the exact current content, a qualified human technical review for safety topics, and a human editorial sign-off.
- Approved items export a machine-readable production package ([schemas/production-package.schema.json](schemas/production-package.schema.json)) for an external video system.

## Commands

| Task | Command |
|---|---|
| Re-normalize committed snapshots | `python3 scripts/import_sheet.py` |
| Capture the live sheet (read-only) | `python3 scripts/import_sheet.py --fetch api` |
| CI check that data is current | `python3 scripts/import_sheet.py --check` |
| List ideas / new workspace | `python3 scripts/new_content.py --list-ideas` / `--from-idea <ID>` |
| Move a stage, hold, resume | `python3 scripts/set_status.py <ID> --stage RESEARCH` |
| Narration timing and chapters | `python3 scripts/qc_content.py runtime <ID>` |
| Automated QC | `python3 scripts/qc_content.py run <ID>` |
| Record an independent review | `python3 scripts/qc_content.py review <ID> --file review.yaml` |
| Approval status / approve | `python3 scripts/qc_content.py status <ID>` / `approve <ID> --by "<name>"` |
| Production package | `python3 scripts/export_package.py <ID> [--draft]` |
| Content board | `python3 scripts/generate_board.py` |
| Repository integrity | `python3 scripts/validate_content.py` |

## Current state of the data

- All six tabs were imported on 2026-11-05: [reports/import-report.md](reports/import-report.md).
- 28 planning ideas (16 long-form, 12 Shorts), 5 pillars, 4 Shorts categories, 4 personas and 5 competitors are normalized with cell-level provenance.
- The two publishing trackers contain only template/example rows: no real production records were found, so none were created.
- The Cartek 2 feature register is empty: no product capability can pass QC until the product team confirms it.
- Pipeline and backlog: [reports/content-board.md](reports/content-board.md).

## Principles

- The spreadsheet stays read-only; the repository is the versioned editorial workspace.
- Nothing is invented: no diagnostic data, compatibility, product features or YouTube metrics.
- Writers never approve their own work, and nothing is published automatically.

See [CONTRIBUTING.md](CONTRIBUTING.md) for branches, commits and reviews, and [CHANGELOG.md](CHANGELOG.md) for history.

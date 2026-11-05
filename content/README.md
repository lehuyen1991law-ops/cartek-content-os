# content/

One folder per video: `long-form/<ID>-<slug>/` or `shorts/<ID>-<slug>/`. Create folders only with [`scripts/new_content.py`](../scripts/new_content.py), which registers the ID and copies the templates.

## Files in a workspace

| File | Written by | Purpose |
|---|---|---|
| `item.yaml` | people, agents, scripts | Structured record ([schema](../schemas/content.schema.json), [field guide](../templates/item.yaml)) |
| `brief.md` | cartek-content-strategist | Audience, problem, takeaway, angle, scope, risks |
| `research.md` | automotive-researcher, technical-fact-checker | Findings, standard vs manufacturer-specific, codes vs causes, fact-check log |
| `script.md` | youtube-scriptwriter / shorts-content-specialist | Hooks, outline, segments with VO and visuals, retention notes |
| `seo.md` | youtube-seo-specialist | Search intent, keyword evidence, title rationale, publishing checklist |
| `storyboard.md` | producer | Shot list (required for long-form) |
| `qc-report.md` | `scripts/qc_content.py` | Generated gate results; do not edit |
| `exports/production-package.json` | `scripts/qc_content.py approve` | Approved handoff package (committed) |
| `exports/production-package.draft.json` | `scripts/export_package.py --draft` | Preview only (git-ignored) |
| `performance.yaml` | analyst | Real YouTube Studio data after publishing |

## Rules

- Keep the English `##` headings and the `### Sxx — Title` segment format: QC and export parse them.
- `[TODO ...]` marks unfinished text. HTML comments are guidance and are ignored by QC.
- Every technical statement in a script cites a claim (`- **CLAIMS:** C01`) registered in `item.yaml`.
- Change stages with `scripts/set_status.py`; approval only through `scripts/qc_content.py approve`.
- Test items (`CTK-?-9001`+) carry a banner and `test_item: true`. They are never approved, exported for release or published.

The current pipeline is on the [content board](../reports/content-board.md).

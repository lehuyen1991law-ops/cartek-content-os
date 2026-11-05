# Contributing

This guide covers branches, commits, reviews and the checks every change must pass. Agents follow the same rules ([CLAUDE.md](CLAUDE.md)).

## Branches

| Branch | Use |
|---|---|
| `main` | Reviewed, validated state. No direct pushes. |
| `content/<ID>-<short-slug>` | Work on one content item, e.g. `content/CTK-L-0015-p0300` |
| `strategy/<topic>` | Strategy, pillars, personas, guidelines |
| `ops/<topic>` | Scripts, schemas, config, CI, templates |
| `data/import-<YYYY-MM-DD>` | A fresh spreadsheet capture |

## Commit messages

```
<type>(<scope>): <what changed>
```

| Type | Scope | Example |
|---|---|---|
| `content` | content ID | `content(CTK-L-0015): add research and claim register` |
| `review` | content ID | `review(CTK-L-0015): technical review R004, G5 FAIL` |
| `data` | `import` | `data(import): capture 2026-11-20, 3 new ideas` |
| `strategy` | file or topic | `strategy(personas): add technician hook examples` |
| `ops` | script or area | `ops(qc): warn on long thumbnail text` |
| `docs` | file | `docs(workflows): clarify publishing steps` |

One content item per commit where possible. Never mix a sheet import with editorial changes.

## Before you commit

```bash
make check
```

It runs the tests, verifies `data/normalized` matches the snapshots, validates every content record, checks Markdown links and checks the content board is current. Fix failures; do not weaken checks or tests to pass. If the board is stale, run `python3 scripts/generate_board.py`.

## Pull requests

- Use the PR template. List the content IDs touched and the QC result of each.
- A content PR that moves an item to APPROVED must show the approval reviews (`python3 scripts/qc_content.py status <ID>`).
- Reviewers check the [editorial guidelines](strategy/editorial-guidelines.md), not only CI.
- The writer of a deliverable never records the independent QC or technical review of the same deliverable.

## Issues

- **Content request**: a new video idea, with audience, problem and sources if known.
- **Editorial review**: a review task or a correction to an existing item.

## Rules that are never relaxed

- The Google Sheet is read-only from this repository.
- No secrets in Git: `.env`, OAuth tokens, API keys, service-account files.
- No raw media in Git: link footage from `item.yaml` → `production.footage_links`.
- No invented technical facts, Cartek 2 features or YouTube metrics.
- No automated publishing to YouTube.
- Content IDs are permanent: never renumber, reuse or delete them.

## Language

Scripts, on-screen text and SEO are Vietnamese. Operating docs, code and commit messages are English. Keep the English `##` headings in content files: the QC scripts read them.

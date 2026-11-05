## Summary

<!-- What changed and why. -->

## Content items touched

| ID | Stage before → after | Automated QC (`qc_content.py run`) | Approval status |
|---|---|---|---|
| | | | |

## Checks

- [ ] `make check` passes locally (tests, import check, validate, links, board)
- [ ] Every new technical statement is a claim in `item.yaml` with an accepted source, or is marked `unverified`
- [ ] No Cartek 2 feature is presented as fact unless it is verified in `data/reference/cartek-2-feature-register.yaml`
- [ ] Safety-flagged items have a qualified human technical review
- [ ] No invented metrics, and no CTR/ranking/view promises
- [ ] No secrets, customer data or raw media files added
- [ ] Sheet data changed only through `scripts/import_sheet.py`; the spreadsheet itself was not modified

## Reviewer notes

<!-- Anything the reviewer should look at closely. -->

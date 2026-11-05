# AGENTS.md

This repository's operating guide for AI agents is [CLAUDE.md](CLAUDE.md). It applies to every agent, not only Claude Code.

In short:

- Cartek publishes Vietnamese YouTube content about OBD2 diagnostics and the Cartek 2 tool.
- The Google Sheet is read-only; its data is imported into `data/` by `scripts/import_sheet.py`.
- Content items live in `content/<format>/<ID>-<slug>/`; create them with `scripts/new_content.py`.
- Skills (role instructions) are in `skills/<name>/SKILL.md`.
- Never invent technical facts or Cartek 2 features, never approve your own work, never publish.
- Validate with `make check` before committing.

#!/usr/bin/env python3
"""Import the Cartek spreadsheet (read-only) into versioned, normalized data.

Usage:
  python3 scripts/import_sheet.py                       # re-normalize committed snapshots (offline)
  python3 scripts/import_sheet.py --check               # CI: fail if committed data is stale
  python3 scripts/import_sheet.py --snapshot-file F     # ingest a capture bundle, then normalize
  python3 scripts/import_sheet.py --fetch api           # capture via Sheets API (token from env)
  python3 scripts/import_sheet.py --fetch csv           # capture via public CSV export
  python3 scripts/import_sheet.py --force               # overwrite generated files edited by hand

Exit codes: 0 ok, 1 errors or stale data (--check), 2 local edits block the write.
The spreadsheet is never modified. Nothing in content/ is ever written.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk import fetch, fileio, importer, schema  # noqa: E402
from ctk.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="repository root (default: this checkout)")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--snapshot-file", help="capture bundle JSON (schemas/source-snapshot.schema.json#/$defs/bundle)")
    source.add_argument("--fetch", choices=["api", "csv"], help="capture the live spreadsheet first (read-only)")
    parser.add_argument("--check", action="store_true", help="verify committed data is up to date; write nothing")
    parser.add_argument("--force", action="store_true", help="overwrite generated files even if edited by hand")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    repo = Repo(args.root)
    log = (lambda *a: None) if args.quiet else print

    if args.check and (args.snapshot_file or args.fetch):
        parser.error("--check cannot be combined with a capture option")

    bundle = None
    if args.snapshot_file:
        bundle = fileio.load_json(Path(args.snapshot_file))
    elif args.fetch == "api":
        token, api_key = fetch.env_credentials(repo.root)
        bundle = fetch.fetch_bundle_api(repo.config["sources"]["spreadsheet"]["id"], token=token, api_key=api_key)
    elif args.fetch == "csv":
        cfg = repo.config["sources"]
        bundle = fetch.fetch_bundle_csv(cfg["spreadsheet"]["id"], cfg["tabs"])

    if not args.check and not args.force:
        edited = importer.hand_edited_outputs(repo)
        if edited:
            log("Refusing to import: generated files were edited by hand since the last import (nothing was written):")
            for path in edited:
                log(f"  - {path}")
            log("Move your edits into content/ or config/, or re-run with --force to discard them.")
            return 2

    if bundle is not None:
        errors = schema.validate(bundle, repo.schemas_dir / "source-capture.schema.json")
        if errors:
            log("Capture bundle is invalid:")
            for error in errors:
                log(f"  - {error}")
            return 1
        for event in importer.ingest_bundle(repo, bundle):
            log(f"snapshot {event['event']:<20} {event['tab']}  {event.get('snapshot', event.get('detail', ''))}")

    result = importer.build(repo)

    if args.check:
        stale = importer.check(repo, result)
        if stale:
            log("Committed import outputs are out of date. Run: python3 scripts/import_sheet.py")
            for path in stale:
                log(f"  - {path}")
            return 1
        log("Import outputs are up to date with data/source snapshots.")
        return 1 if result.errors else 0

    if result.errors and not args.force:
        log("Import has errors; nothing was written (use --force to write anyway):")
        for issue in result.errors:
            log(f"  - {issue.tab or ''} {issue.ref or ''} {issue.message}")
        return 1
    outcome = importer.apply(repo, result, force=args.force)
    if outcome["conflicts"]:
        log("Refusing to overwrite generated files that were edited by hand since the last import:")
        for path in outcome["conflicts"]:
            log(f"  - {path}")
        log("Move your edits into content/ or config/, or re-run with --force to discard them.")
        return 2

    for path in outcome["overwritten"]:
        log(f"--force: discarded hand edits in {path}")
    for summary in result.tabs:
        records = ", ".join(f"{v} {k}" for k, v in summary.get("records", {}).items()) or "-"
        log(f"tab {summary['status']:<9} {summary['title']:<18} {records}")
    for event in result.id_events:
        log(f"id  {event['event']:<17} {event['id']}  {event.get('title', '')}")
    for event in result.drift:
        log(f"workspace drift: {event['message']}")
    counts = {level: sum(1 for i in result.issues if i.level == level) for level in ("error", "warning", "info")}
    log(f"issues: {counts['error']} error(s), {counts['warning']} warning(s), {counts['info']} info")
    log("written: " + (", ".join(outcome["written"]) if outcome["written"] else "nothing (already up to date)"))
    log(f"report: {importer.REPORT_PATH}")
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())

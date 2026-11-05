#!/usr/bin/env python3
"""Change a content item's workflow stage or hold state, with history.

Usage:
  python3 scripts/set_status.py <ID> --stage RESEARCH [--note "..."] [--by NAME]
  python3 scripts/set_status.py <ID> --hold "waiting for test vehicle"
  python3 scripts/set_status.py <ID> --resume
  python3 scripts/set_status.py <ID> --stage PUBLISHED --url https://youtu.be/... --date 2026-12-01
  python3 scripts/set_status.py <ID> --stage PERFORMANCE_REVIEW

APPROVED is set only by `qc_content.py approve`. PUBLISHED requires a valid approval
on the current content plus the real URL and date. The spreadsheet is not updated:
copy the new status there by hand (see workflows/publishing.md).
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk import fileio, qc, schema  # noqa: E402
from ctk.context import build_context  # noqa: E402
from ctk.items import PERFORMANCE, find_item  # noqa: E402
from ctk.repo import Repo  # noqa: E402
from ctk.sheet import is_youtube_url  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root")
    parser.add_argument("id")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--stage")
    action.add_argument("--hold", metavar="REASON")
    action.add_argument("--resume", action="store_true")
    parser.add_argument("--url")
    parser.add_argument("--date")
    parser.add_argument("--note", default="")
    parser.add_argument("--by", default="scripts/set_status.py")
    args = parser.parse_args(argv)
    repo = Repo(args.root)
    try:
        item = find_item(repo, args.id)
    except LookupError as exc:
        print(exc)
        return 2
    status = item.data["status"]
    workflow = repo.config["workflow"]

    if args.hold is not None:
        status["on_hold"], status["hold_reason"] = True, args.hold
        item.add_history(item.stage, args.by, f"On hold: {args.hold}", on_hold=True)
        item.save()
        print(f"{item.id} on hold at {item.stage}. Sheet status: {workflow['on_hold_sheet_status']}")
        return 0
    if args.resume:
        status["on_hold"], status["hold_reason"] = False, ""
        item.add_history(item.stage, args.by, "Resumed" + (f": {args.note}" if args.note else ""), on_hold=False)
        item.save()
        print(f"{item.id} resumed at {item.stage}.")
        return 0

    stage = args.stage.upper()
    stages = repo.stage_ids()
    if stage not in stages:
        parser.error(f"unknown stage {stage}. Stages: {', '.join(stages)}")
    if stage == "APPROVED":
        print("APPROVED can only be set by: python3 scripts/qc_content.py approve <ID> --by <NAME>")
        return 1
    if stage in ("PUBLISHED", "PERFORMANCE_REVIEW") and item.is_test:
        print("Test items can never be published.")
        return 1
    if stage == "PUBLISHED":
        if item.stage not in ("APPROVED", "PUBLISHED"):
            print(f"{item.id} is at {item.stage}; only APPROVED content can be published.")
            return 1
        ctx = build_context(repo, item)
        approval_info = qc.approval(ctx, qc.run_gates(ctx))
        if approval_info["status"] != "APPROVABLE":
            print("The approval is not valid for the current content (it changed after approval or reviews are missing). Re-run QC.")
            return 1
        if not args.url or not is_youtube_url(args.url):
            print("--url must be the real YouTube URL of the published video.")
            return 1
        try:
            published = date.fromisoformat(args.date or "")
        except ValueError:
            print("--date must be the real publish date as YYYY-MM-DD.")
            return 1
        if published > date.today():
            print("--date is in the future; record the publication after the video is live.")
            return 1
        checklist = item.data["publication"].get("upload_checklist") or []
        pending = [entry["item"] for entry in checklist if not entry.get("done")]
        if not checklist or pending:
            print("Finish publication.upload_checklist in item.yaml first (set done: true for each step):")
            for entry in pending or ["(checklist missing: copy it from templates/item.yaml)"]:
                print(f"  - {entry}")
            return 1
        item.data["publication"].update({"url": args.url, "published_at": published.isoformat()})
    if stage == "PERFORMANCE_REVIEW":
        if item.stage not in ("PUBLISHED", "PERFORMANCE_REVIEW"):
            print("Only published items can move to PERFORMANCE_REVIEW.")
            return 1
        performance = item.file(PERFORMANCE)
        if not performance.exists():
            print(f"Create {repo.rel(performance)} from templates/performance.yaml with real YouTube Studio data first.")
            return 1
        errors = schema.validate(fileio.load_yaml(performance), repo.schemas_dir / "performance.schema.json")
        if errors:
            print("performance.yaml is invalid:")
            for error in errors:
                print(f"  - {error}")
            return 1
    status["stage"] = stage
    item.add_history(stage, args.by, args.note or f"Stage set to {stage}.")
    item.save()
    sheet_status = next(s["sheet_status"] for s in workflow["stages"] if s["id"] == stage)
    print(f"{item.id} -> {stage}. Matching sheet status: {sheet_status} (update the sheet by hand).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Export a content item as a production package for an external video system.

Usage:
  python3 scripts/export_package.py <ID>            # release package; only for approved content
  python3 scripts/export_package.py <ID> --draft    # draft package with blocking issues listed
  python3 scripts/export_package.py <ID> --stdout   # print instead of writing

Contract: schemas/production-package.schema.json. Release packages are written to
<workspace>/exports/production-package.json (committed); drafts to
production-package.draft.json (git-ignored). Consumers must reject anything whose
package_status is not APPROVED.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk import export, fileio, qc, schema  # noqa: E402
from ctk.context import build_context  # noqa: E402
from ctk.items import DRAFT_EXPORT, EXPORT_DIR, RELEASE_EXPORT, find_item  # noqa: E402
from ctk.repo import Repo  # noqa: E402

RELEASE_STAGES = ("APPROVED", "PUBLISHED", "PERFORMANCE_REVIEW")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root")
    parser.add_argument("id")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args(argv)
    repo = Repo(args.root)
    try:
        item = find_item(repo, args.id)
    except LookupError as exc:
        print(exc)
        return 2
    ctx = build_context(repo, item)
    results = qc.run_gates(ctx)
    approval_info = qc.approval(ctx, results)

    if args.draft:
        blocking = [f"{gate} {level}: {evidence}" for gate, result in results.items() for level, evidence, _ in result.findings if level in (qc.FAIL, qc.BLOCKED)]
        blocking += [f"Approval: {r['requirement']} — {r['detail']}" for r in approval_info["requirements"] if not r["satisfied"]]
        package = export.build_package(ctx, approved=False, blocking=blocking)
        target = item.file(EXPORT_DIR) / DRAFT_EXPORT
    else:
        problems = []
        if item.is_test:
            problems.append("Test items never get a release package (use --draft).")
        if item.stage not in RELEASE_STAGES:
            problems.append(f"Stage is {item.stage}; approve first with `qc_content.py approve`.")
        if approval_info["status"] != "APPROVABLE":
            problems += [f"{r['requirement']}: {r['detail']}" for r in approval_info["requirements"] if not r["satisfied"]]
        if problems:
            print(f"Release export refused for {item.id}:")
            for problem in problems:
                print(f"  - {problem}")
            print("Use --draft for a non-production preview.")
            return 1
        reviews = [r["id"] for r in item.data["reviews"] if ctx.is_current(r)]
        package = export.build_package(ctx, approved=True, blocking=[], approval_reviews=reviews)
        target = item.file(EXPORT_DIR) / RELEASE_EXPORT

    errors = schema.validate(package, repo.schemas_dir / "production-package.schema.json")
    if errors:
        print("Package does not validate against schemas/production-package.schema.json:")
        for error in errors:
            print(f"  - {error}")
        return 1
    text = fileio.dumps_json(package)
    if args.stdout:
        print(text, end="")
        return 0
    fileio.write_text(target, text)
    print(f"{package['package_status']} package for {item.id}: {repo.rel(target)} ({len(package['script']['segments'])} segments, {len(package['blocking_issues'])} blocking issues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

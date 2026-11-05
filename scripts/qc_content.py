#!/usr/bin/env python3
"""Quality control for content items (gates G1-G8) and the approval decision.

Usage:
  python3 scripts/qc_content.py run <ID> [--record]       # automated gates -> qc-report.md
  python3 scripts/qc_content.py run --all [--summary F]   # every item (CI summary table)
  python3 scripts/qc_content.py review <ID> --file R.yaml # record an independent judgment review
  python3 scripts/qc_content.py status <ID>               # approval requirements
  python3 scripts/qc_content.py approve <ID> --by NAME    # set APPROVED + release export, only if approvable
  python3 scripts/qc_content.py runtime <ID>              # narration timing and chapter starts

The automated gates evaluate the files only; the stage a writer sets is never
taken as evidence. Approval needs automated PASS plus independent reviews on
the current content fingerprint (config/qc-policy.yaml -> approval).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk import export, fileio, mdparse, qc, schema  # noqa: E402
from ctk.context import build_context, describe_target  # noqa: E402
from ctk.items import EXPORT_DIR, QC_REPORT, RELEASE_EXPORT, find_item, find_items, today  # noqa: E402
from ctk.repo import Repo  # noqa: E402

GATE_RESULTS = ("PASS", "FAIL", "BLOCKED")


def evaluate(repo: Repo, content_id: str):
    item = find_item(repo, content_id)
    ctx = build_context(repo, item)
    results = qc.run_gates(ctx)
    return item, ctx, results, qc.approval(ctx, results)


def write_report(ctx, results, approval_info) -> None:
    fileio.write_text(ctx.item.file(QC_REPORT), qc.render_report(ctx, results, approval_info))


def print_summary(ctx, results, approval_info) -> None:
    print(f"{ctx.item.id}  stage={ctx.item.stage}  automated={qc.overall(results)}  approval={approval_info['status']}")
    for gate, result in results.items():
        print(f"  {gate} {result.result:<8} {result.summary()}")


def cmd_run(repo: Repo, args) -> int:
    if args.all:
        rows = ["| Item | Stage | " + " | ".join(qc.GATES) + " | Automated | Approval |", "|---|---|" + "---|" * len(qc.GATES) + "---|---|"]
        for item in find_items(repo):
            ctx = build_context(repo, item)
            results = qc.run_gates(ctx)
            approval_info = qc.approval(ctx, results)
            label = item.id + (" (test)" if item.is_test else "")
            rows.append(f"| {label} | {item.stage} | " + " | ".join(results[g].result for g in qc.GATES) + f" | {qc.overall(results)} | {approval_info['status']} |")
            if args.write_reports:
                write_report(ctx, results, approval_info)
        table = "\n".join(rows) + "\n"
        print(table)
        if args.summary:
            with open(args.summary, "a", encoding="utf-8") as handle:
                handle.write("## Content QC (automated gates)\n\n" + table)
        return 0
    if not args.id:
        print("Give a content ID or --all.")
        return 2
    item, ctx, results, approval_info = evaluate(repo, args.id)
    if args.record:
        review = qc.automated_review(ctx, results)
        item.data.setdefault("reviews", []).append(review)
        item.save()
        print(f"Recorded automated review {review['id']} on {ctx.fingerprint[:19]}…")
        item, ctx, results, approval_info = evaluate(repo, args.id)
    write_report(ctx, results, approval_info)
    print_summary(ctx, results, approval_info)
    print(f"Report: {repo.rel(item.file(QC_REPORT))}")
    return 0


def validate_review(review: dict) -> list[str]:
    problems = []
    if not str(review.get("reviewer", "")).strip():
        problems.append("reviewer is empty")
    if review.get("reviewer_type") not in ("agent", "human"):
        problems.append("reviewer_type must be agent or human (automated reviews come from `run --record`)")
    if review.get("role") not in ("qc", "technical", "editorial"):
        problems.append("role must be qc, technical or editorial")
    gates = review.get("gates") or {}
    if review.get("role") != "editorial" and not gates:
        problems.append("gates is empty")
    for gate, entry in gates.items():
        if gate not in qc.GATES:
            problems.append(f"unknown gate {gate}")
            continue
        if (entry or {}).get("result") not in GATE_RESULTS:
            problems.append(f"{gate}: result must be PASS, FAIL or BLOCKED")
        if len(str((entry or {}).get("evidence", "")).strip()) < 15:
            problems.append(f"{gate}: evidence must say what was checked (at least 15 characters)")
        if (entry or {}).get("result") in ("FAIL", "BLOCKED") and not (entry or {}).get("corrections"):
            problems.append(f"{gate}: a FAIL or BLOCKED result needs at least one correction")
    if review.get("decision") not in GATE_RESULTS:
        problems.append("decision must be PASS, FAIL or BLOCKED")
    if review.get("role") == "editorial" and review.get("reviewer_type") != "human":
        problems.append("the editorial sign-off must be a human")
    return problems


def cmd_review(repo: Repo, args) -> int:
    review = fileio.load_yaml(Path(args.file)) or {}
    problems = validate_review(review)
    if problems:
        print("Review not recorded:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    item, ctx, _, _ = evaluate(repo, args.id)
    record = {
        "id": qc.next_review_id(item.data),
        "date": today(),
        "reviewer": str(review["reviewer"]).strip(),
        "reviewer_type": review["reviewer_type"],
        "role": review["role"],
        "qualified": bool(review.get("qualified", False)),
        "fingerprint": ctx.fingerprint_for(review["role"]),
        "gates": {
            gate: {"result": entry["result"], "evidence": str(entry["evidence"]).strip(), "corrections": [str(c) for c in entry.get("corrections") or []]}
            for gate, entry in (review.get("gates") or {}).items()
        },
        "decision": review["decision"],
        "notes": str(review.get("notes") or ""),
    }
    item.data.setdefault("reviews", []).append(record)
    item.save()
    item, ctx, results, approval_info = evaluate(repo, args.id)
    write_report(ctx, results, approval_info)
    print(f"Recorded review {record['id']} ({record['role']}, {record['reviewer_type']}: {record['reviewer']}) on the current content.")
    print(f"Approval status: {approval_info['status']}")
    return 0


def cmd_status(repo: Repo, args) -> int:
    _, ctx, results, approval_info = evaluate(repo, args.id)
    print(f"{ctx.item.id}  approval={approval_info['status']}  fingerprint={ctx.fingerprint}")
    for req in approval_info["requirements"]:
        print(f"  [{'x' if req['satisfied'] else ' '}] {req['requirement']}: {req['detail']}")
    return 0


def cmd_approve(repo: Repo, args) -> int:
    item, ctx, results, approval_info = evaluate(repo, args.id)
    if approval_info["status"] != "APPROVABLE":
        print(f"{item.id} cannot be approved:")
        for req in approval_info["requirements"]:
            if not req["satisfied"]:
                print(f"  - {req['requirement']}: {req['detail']}")
        return 1
    automated = qc.automated_review(ctx, results)
    item.data.setdefault("reviews", []).append(automated)
    if item.stage in ("PUBLISHED", "PERFORMANCE_REVIEW"):
        # Post-publication change (e.g. SEO refinement): re-approve without moving the stage back.
        item.add_history(item.stage, args.by, f"Re-approved after a post-publication change on {ctx.fingerprint}; automated review {automated['id']}.")
    else:
        item.data["status"]["stage"] = "APPROVED"
        item.add_history("APPROVED", args.by, f"Approved on {ctx.fingerprint}; automated review {automated['id']}.")
    item.save()
    item, ctx, results, approval_info = evaluate(repo, args.id)
    review_ids = [r["id"] for r in item.data["reviews"] if ctx.is_current(r)]
    package = export.build_package(ctx, approved=True, blocking=[], approval_reviews=review_ids)
    errors = schema.validate(package, repo.schemas_dir / "production-package.schema.json")
    if errors:
        print("Approved, but the release package does not validate:")
        for error in errors:
            print(f"  - {error}")
        return 1
    target = item.file(EXPORT_DIR) / RELEASE_EXPORT
    fileio.write_text(target, fileio.dumps_json(package))
    write_report(ctx, results, approval_info)
    print(f"{item.id} approved at stage {item.stage}. Release package: {repo.rel(target)}")
    return 0


def cmd_runtime(repo: Repo, args) -> int:
    _, ctx, _, _ = evaluate(repo, args.id)
    rate = ctx.production["speech_rate_syllables_per_minute"][ctx.item.format]
    calibrated = "calibrated" if ctx.production.get("speech_rate_calibrated") else "NOT calibrated (planning assumption)"
    print(f"{ctx.item.id}: speech rate {rate} syllables/min, {calibrated}; target {describe_target(ctx.target)}")
    print(f"{'Start':>6}  {'Seg':<4} {'Type':<7} {'Syll':>5} {'VO s':>6} {'Demo s':>6} {'Total s':>7}")
    for row in ctx.timing:
        print(f"{mdparse.format_timestamp(row['start_seconds']):>6}  {row['segment']:<4} {row['type']:<7} {row['syllables']:>5} {row['vo_seconds']:>6} {row['demo_seconds']:>6} {row['seconds']:>7}")
    print(f"Estimated total: {mdparse.format_timestamp(ctx.total_seconds)} ({ctx.total_seconds} s)")
    if ctx.script.todo_count:
        print(f"Note: script.md still has {ctx.script.todo_count} [TODO] marker(s); unfinished narration is not counted.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("id", nargs="?")
    run.add_argument("--all", action="store_true")
    run.add_argument("--record", action="store_true", help="append the automated result to the review history")
    run.add_argument("--summary", help="append a Markdown summary table to this file (e.g. $GITHUB_STEP_SUMMARY)")
    run.add_argument("--write-reports", action="store_true", help="with --all: also rewrite each qc-report.md")
    review = sub.add_parser("review")
    review.add_argument("id")
    review.add_argument("--file", required=True)
    status = sub.add_parser("status")
    status.add_argument("id")
    approve = sub.add_parser("approve")
    approve.add_argument("id")
    approve.add_argument("--by", required=True, help="person approving (recorded in history)")
    runtime = sub.add_parser("runtime")
    runtime.add_argument("id")
    args = parser.parse_args(argv)
    repo = Repo(args.root)
    handlers = {"run": cmd_run, "review": cmd_review, "status": cmd_status, "approve": cmd_approve, "runtime": cmd_runtime}
    try:
        return handlers[args.command](repo, args)
    except LookupError as exc:
        print(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())

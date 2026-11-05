#!/usr/bin/env python3
"""Validate repository integrity: schemas, source data, content records, skills, templates.

Usage:
  python3 scripts/validate_content.py            # exit 1 on errors; warnings are printed
  python3 scripts/validate_content.py --strict   # warnings also fail

Checks include: item.yaml against schemas/content.schema.json; registered and unique
IDs; vocabularies; approvals that still match the content; published items with a
real URL and date; stale release packages; hand-edited generated data; skill
front matter and .claude/skills links. Work-in-progress content is not an error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk.repo import Repo  # noqa: E402
from ctk.validate import validate_repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    findings = validate_repo(Repo(args.root))
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]
    for finding in errors + warnings:
        print(f"{finding.level.upper():<7} {finding.where}: {finding.message}")
    print(f"validate_content: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())

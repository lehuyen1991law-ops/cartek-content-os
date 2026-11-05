#!/usr/bin/env python3
"""Check that relative links in Markdown files point to existing files.

External links (http, https, mailto) are not fetched: the check works offline
and needs no credentials. Exit 1 if a relative link is broken.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk.repo import Repo  # noqa: E402

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        if not any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            yield path


def broken_links(root: Path) -> list[str]:
    problems = []
    for path in iter_markdown(root):
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`[^`\n]*`", "", text)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        for target in LINK.findall(text):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            file_part = unquote(target.split("#", 1)[0])
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            if not resolved.exists():
                problems.append(f"{path.relative_to(root)}: broken link -> {target}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root")
    args = parser.parse_args(argv)
    root = Repo(args.root).root
    problems = broken_links(root)
    for problem in problems:
        print(problem)
    print(f"check_links: {len(problems)} broken relative link(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

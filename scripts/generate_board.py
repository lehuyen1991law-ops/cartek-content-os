#!/usr/bin/env python3
"""Generate reports/content-board.md (pipeline, workspaces, QC state, idea backlog).

Usage:
  python3 scripts/generate_board.py           # write the board
  python3 scripts/generate_board.py --check   # exit 1 if the committed board is stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk import fileio  # noqa: E402
from ctk.board import BOARD_PATH, render_board  # noqa: E402
from ctk.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args(argv)
    repo = Repo(args.root)
    board = render_board(repo)
    path = repo.path(BOARD_PATH)
    if args.stdout:
        print(board, end="")
        return 0
    if args.check:
        if not path.exists() or fileio.read_text(path) != board:
            print(f"{BOARD_PATH} is out of date. Run: python3 scripts/generate_board.py")
            return 1
        print(f"{BOARD_PATH} is up to date.")
        return 0
    changed = fileio.write_text(path, board)
    print(f"{BOARD_PATH} {'updated' if changed else 'unchanged'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

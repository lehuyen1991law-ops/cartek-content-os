"""Content ID registry (data/id-registry.json).

IDs are never reused. Production IDs run from 0001 to 8999 per format
(CTK-L-0001, CTK-S-0001); 9001-9999 is reserved for test items.
"""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any

from . import fileio

ID_PATTERN = re.compile(r"^CTK-(?P<code>[LS])-(?P<num>\d{4})$")
TEST_BASE = 9000
PRODUCTION_MAX = 8999


def make_id(code: str, number: int) -> str:
    return f"CTK-{code}-{number:04d}"


def parse_id(content_id: str) -> tuple[str, int] | None:
    match = ID_PATTERN.match(content_id or "")
    return (match.group("code"), int(match.group("num"))) if match else None


def is_test_id(content_id: str) -> bool:
    parsed = parse_id(content_id)
    return bool(parsed and parsed[1] > TEST_BASE)


class Registry:
    FORMAT = 1

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = data or {"registry_format": self.FORMAT, "entries": {}}
        self.data.setdefault("entries", {})

    @classmethod
    def load(cls, path: Path) -> "Registry":
        return cls(fileio.load_json(path)) if path.exists() else cls()

    def copy(self) -> "Registry":
        return Registry(copy.deepcopy(self.data))

    @property
    def entries(self) -> dict[str, dict[str, Any]]:
        return self.data["entries"]

    def to_text(self) -> str:
        ordered = {
            "registry_format": self.FORMAT,
            "policy": "IDs are permanent and never reused. 0001-8999 = production, 9001-9999 = test items.",
            "entries": {cid: self.entries[cid] for cid in sorted(self.entries)},
        }
        return fileio.dumps_json(ordered)

    def find_by_key(self, key: str) -> str | None:
        for cid in sorted(self.entries):
            if self.entries[cid].get("key") == key:
                return cid
        return None

    def next_number(self, code: str, test: bool = False) -> int:
        numbers = [n for cid in self.entries if (p := parse_id(cid)) and p[0] == code for n in [p[1]]]
        if test:
            used = [n for n in numbers if n > TEST_BASE]
            number = max(used, default=TEST_BASE) + 1
            if number > 9999:
                raise ValueError(f"Test ID range exhausted for {code}")
        else:
            used = [n for n in numbers if n <= PRODUCTION_MAX]
            number = max(used, default=0) + 1
            if number > PRODUCTION_MAX:
                raise ValueError(f"Production ID range exhausted for {code}")
        return number

    def allocate(
        self,
        code: str,
        *,
        origin: str,
        title: str,
        allocated_at: str,
        key: str | None = None,
        source_ref: str | None = None,
        test: bool = False,
    ) -> str:
        content_id = make_id(code, self.next_number(code, test=test))
        entry: dict[str, Any] = {
            "origin": origin,
            "title": title,
            "state": "active",
            "allocated_at": allocated_at,
        }
        if key:
            entry["key"] = key
        if source_ref:
            entry["source_ref"] = source_ref
        self.entries[content_id] = entry
        return content_id

    def rename(self, content_id: str, *, key: str, title: str, source_ref: str | None) -> None:
        entry = self.entries[content_id]
        aliases = entry.setdefault("previous_titles", [])
        if entry.get("title") and entry["title"] not in aliases:
            aliases.append(entry["title"])
        entry.update({"key": key, "title": title, "state": "active"})
        if source_ref:
            entry["source_ref"] = source_ref

    def set_state(self, content_id: str, state: str) -> None:
        self.entries[content_id]["state"] = state

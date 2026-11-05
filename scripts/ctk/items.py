"""Content workspaces: discovery, loading, saving, content fingerprints.

A workspace is ``content/<long-form|shorts>/<ID>-<slug>/`` holding ``item.yaml``
plus the Markdown deliverables. The *fingerprint* identifies the reviewed
content: QC approvals are only valid for the fingerprint they were recorded on.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from . import fileio, mdparse
from .repo import Repo

DELIVERABLES = {
    "brief": "brief.md",
    "research": "research.md",
    "script": "script.md",
    "seo": "seo.md",
    "storyboard": "storyboard.md",
}
QC_REPORT = "qc-report.md"
PERFORMANCE = "performance.yaml"
EXPORT_DIR = "exports"
RELEASE_EXPORT = "production-package.json"
DRAFT_EXPORT = "production-package.draft.json"

# Fields that may change after approval without invalidating the reviewed content.
FINGERPRINT_EXCLUDED = ("status", "history", "reviews", "publication", "owner", "target_publish_date", "internal_notes", "corrections")

# The technical scope leaves out work that happens after the technical review.
TECHNICAL_EXCLUDED = ("seo", "production")
TECHNICAL_FILES = ("brief", "research", "script")
REVIEW_SCOPES = {"technical": "technical"}  # role -> scope; every other role reviews the full content

ITEM_HEADER = (
    "Content record. Schema: schemas/content.schema.json. Field guide: templates/item.yaml.\n"
    "Edit values freely, except: status.stage APPROVED/PUBLISHED and reviews/history are written by\n"
    "scripts/qc_content.py and scripts/set_status.py."
)


def today() -> str:
    return date.today().isoformat()


@dataclass
class Item:
    path: Path
    data: dict[str, Any]

    @property
    def id(self) -> str:
        return str(self.data.get("id", ""))

    @property
    def format(self) -> str:
        return str(self.data.get("format", ""))

    @property
    def stage(self) -> str:
        return str((self.data.get("status") or {}).get("stage", ""))

    @property
    def is_test(self) -> bool:
        return bool(self.data.get("test_item"))

    def file(self, name: str) -> Path:
        return self.path / name

    def deliverable(self, key: str) -> Path:
        return self.path / DELIVERABLES[key]

    def text(self, key: str) -> str:
        path = self.deliverable(key)
        return fileio.read_text(path) if path.exists() else ""

    def fingerprint(self, scope: str = "full") -> str:
        """Hash of the reviewed content.

        ``full``: everything a reader or viewer sees (all deliverables and fields except
        workflow bookkeeping). ``technical``: only what a technical review judges (brief,
        research, script, claims, sources, vehicle, safety), so later SEO and production
        work does not void a technical review.
        """
        excluded = FINGERPRINT_EXCLUDED + (TECHNICAL_EXCLUDED if scope == "technical" else ())
        record = {k: v for k, v in copy.deepcopy(self.data).items() if k not in excluded}
        files = {}
        for key, name in DELIVERABLES.items():
            if scope == "technical" and key not in TECHNICAL_FILES:
                continue
            path = self.path / name
            if path.exists():
                text = mdparse.visible(fileio.read_text(path)).replace("\r\n", "\n")
                files[name] = "\n".join(line.rstrip() for line in text.split("\n")).strip()
        return "sha256:" + fileio.sha256_obj({"item": record, "files": files})

    def save(self) -> None:
        fileio.write_text(self.path / "item.yaml", fileio.dumps_yaml(self.data, header=ITEM_HEADER))

    def add_history(self, stage: str, by: str, note: str, on_hold: bool | None = None) -> None:
        history = self.data.setdefault("history", [])
        version = (history[-1]["version"] + 1) if history else 1
        entry: dict[str, Any] = {"version": version, "date": today(), "stage": stage, "by": by, "note": note}
        if on_hold is not None:
            entry["on_hold"] = on_hold
        history.append(entry)


def load_item(workspace: Path) -> Item:
    return Item(workspace, fileio.load_yaml(workspace / "item.yaml") or {})


def find_items(repo: Repo) -> list[Item]:
    items = []
    for item_file in sorted(repo.content_dir.glob("*/*/item.yaml")):
        items.append(load_item(item_file.parent))
    return items


def workspace_for(repo: Repo, content_id: str) -> Path | None:
    for candidate in sorted(repo.content_dir.glob(f"*/{content_id}*")):
        if candidate.is_dir() and (candidate.name == content_id or candidate.name.startswith(content_id + "-")):
            return candidate
    return None


def find_item(repo: Repo, content_id: str) -> Item:
    workspace = workspace_for(repo, content_id)
    if workspace is None or not (workspace / "item.yaml").exists():
        raise LookupError(f"No workspace for {content_id} under content/. Create it with scripts/new_content.py.")
    return load_item(workspace)

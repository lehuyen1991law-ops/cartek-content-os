"""Shared test helpers: sandboxed repository copies and synthetic fixtures.

Synthetic fixtures exist only inside temporary directories created by the tests.
They are labelled SYNTHETIC and are never real research.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ctk import fileio  # noqa: E402
from ctk.items import find_item  # noqa: E402
from ctk.repo import Repo  # noqa: E402
from ctk.sheet import TabSnapshot  # noqa: E402

COPY_DIRS = ("config", "schemas", "scripts", "templates", "data")
COPY_FILES = ("reports/import-report.md",)


class Sandbox:
    """A temporary copy of the repository without editorial content."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="ctk-test-")
        self.root = Path(self._tmp.name)
        for name in COPY_DIRS:
            shutil.copytree(REPO_ROOT / name, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
        for name in COPY_FILES:
            (self.root / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / name, self.root / name)
        for sub in ("content/long-form", "content/shorts"):
            (self.root / sub).mkdir(parents=True, exist_ok=True)

    @property
    def repo(self) -> Repo:
        return Repo(self.root)

    def cleanup(self) -> None:
        self._tmp.cleanup()


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(f"script_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(name: str, root: Path, *args: str) -> tuple[int, str]:
    """Run scripts/<name>.py main() with --root; return (exit code, stdout)."""
    module = load_script(name)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        try:
            code = module.main(["--root", str(root), *args])
        except SystemExit as exc:  # argparse errors
            code = exc.code if isinstance(exc.code, int) else 2
    return code, buffer.getvalue()


def created_id(output: str) -> str:
    """Content ID printed by new_content.py ("Created CTK-L-9002 at ...")."""
    import re

    match = re.search(r"Created (CTK-[LS]-[0-9]{4})", output)
    assert match, output
    return match.group(1)


def edit_snapshot(repo: Repo, title: str, edit) -> None:
    """Apply ``edit(rows)`` to the raw snapshot of a tab (simulates a sheet change)."""
    tab = next(t for t in repo.config["sources"]["tabs"] if t["title"] == title)
    path = repo.path(tab["snapshot"])
    snapshot = TabSnapshot.from_dict(fileio.load_json(path))
    edit(snapshot.rows)
    fileio.write_text(path, snapshot.to_text())


# ---------------------------------------------------------------------------
# Synthetic "complete" long-form item (passes every automated gate)
# ---------------------------------------------------------------------------
FILLER = "Đây là lời thoại mẫu tổng hợp chỉ dùng cho kiểm thử tự động của hệ thống."  # 17 syllables


def narration(sentences: int) -> str:
    return " ".join([FILLER] * sentences)


def write_complete_fixture(repo: Repo, content_id: str = "CTK-L-0015") -> Path:
    code, out = run("new_content", repo.root, "--from-idea", content_id, "--audience", "technician", "--owner", "Test Owner")
    assert code == 0, out
    item = find_item(repo, content_id)
    ws = item.path
    (ws / "brief.md").write_text(
        "# Brief (SYNTHETIC TEST FIXTURE)\n\n"
        "## Audience\n\nSynthetic audience description for automated tests.\n\n"
        "## Problem\n\nSynthetic problem statement.\n\n"
        "## Takeaway\n\nSynthetic takeaway.\n\n"
        "## Angle\n\nSynthetic angle.\n\n"
        "## Scope\n\nSynthetic scope.\n\n"
        "## Risks\n\nNone in this synthetic fixture.\n",
        encoding="utf-8",
    )
    (ws / "research.md").write_text(
        "# Research (SYNTHETIC TEST FIXTURE)\n\n"
        "## Research question\n\nSynthetic question.\n\n"
        "## Findings\n\nSynthetic finding [C01].\n\n"
        "## Standard vs manufacturer-specific\n\nSynthetic comparison.\n\n"
        "## Open questions\n\nNone.\n",
        encoding="utf-8",
    )
    segments = [
        ("S01", "Hook", "hook", narration(4) + " Mã P0300 xuất hiện trong ví dụ này."),
        ("S02", "Intro", "intro", narration(10)),
        ("S03", "Body", "body", narration(14)),
        ("S04", "Demo", "demo", narration(12)),
        ("S05", "Body two", "body", narration(14)),
        ("S06", "Recap", "recap", narration(10)),
        ("S07", "CTA", "cta", narration(4) + " Cartek - Check your car"),
    ]
    script = ["# Script (SYNTHETIC TEST FIXTURE)", "", "## Hook candidates", "", "1. Synthetic hook one.", "2. Synthetic hook two.", "3. Synthetic hook three.", "",
              "## Selected hook", "", "- **HOOK:** Synthetic hook one.", "- **RATIONALE:** Synthetic rationale.", "",
              "## Outline", "", "1. One", "2. Two", "3. Three", "", "## Script", ""]
    for seg_id, title, seg_type, vo in segments:
        script += [f"### {seg_id} — {title}", "", f"- **TYPE:** {seg_type}", f"- **VO:** {vo}", "- **VISUAL:** Synthetic visual.", "- **ON-SCREEN:** Synthetic text"]
        script += ["- **CLAIMS:** C01" if seg_id == "S01" else "- **CLAIMS:**", ""]
    script += ["## Retention notes", "", "- Synthetic open loop."]
    (ws / "script.md").write_text("\n".join(script) + "\n", encoding="utf-8")
    (ws / "seo.md").write_text(
        "# SEO (SYNTHETIC TEST FIXTURE)\n\n## Search intent\n\nSynthetic.\n\n## Keyword notes\n\nSynthetic.\n\n"
        "## Title rationale\n\nSynthetic.\n\n## Publishing checklist\n\n- [x] Synthetic item one\n- [x] Synthetic item two\n",
        encoding="utf-8",
    )
    (ws / "storyboard.md").write_text(
        "# Storyboard (SYNTHETIC TEST FIXTURE)\n\n## Shot list\n\n| Shot | Segment | Framing | Description |\n|---|---|---|---|\n| 1 | S01 | Wide | Synthetic shot |\n",
        encoding="utf-8",
    )
    data = item.data
    data.update(
        {
            "problem": "Synthetic problem.",
            "takeaway": "Synthetic takeaway.",
            "target_publish_date": "2026-12-01",
        }
    )
    data["keywords"] = {"primary": "p0300", "secondary": ["synthetic"]}
    data["sources"] = [{"id": "SRC01", "title": "Synthetic standard reference (test fixture)", "type": "standard", "citation": "SYNTHETIC citation for unit tests"}]
    data["claims"] = [
        {"id": "C01", "text": "SYNTHETIC fixture claim mentioning P0300 for unit tests.", "category": "dtc-definition", "sources": ["SRC01"], "status": "verified", "feature_id": None, "verified_by": "unit-test", "verified_on": "2026-11-05", "notes": ""}
    ]
    data["seo"].update(
        {
            "title_candidates": ["Synthetic P0300 title A", "Synthetic P0300 title B", "Synthetic P0300 title C"],
            "recommended_title": "Synthetic P0300 title A",
            "title_rationale": "Synthetic rationale.",
            "description": "Synthetic description about p0300.",
            "tags": ["synthetic one", "synthetic two", "synthetic three"],
            "chapters": [{"time": "00:00", "title": "Mở đầu"}, {"time": "01:00", "title": "Giải thích"}, {"time": "03:00", "title": "Demo"}],
            "thumbnail_concepts": [{"concept": "Synthetic concept A", "on_image_text": "P0300?"}, {"concept": "Synthetic concept B", "on_image_text": "Bỏ máy"}],
        }
    )
    data["production"]["assets_required"] = [{"item": "Synthetic asset", "type": "tool", "status": "confirmed", "notes": ""}]
    data["production"]["demo_setup"] = {"tool": "Cartek 2", "tool_version": "test", "vehicle": "Synthetic test vehicle", "location": "Test bay"}
    data["publication"]["visibility_plan"] = "scheduled"
    item.save()
    return ws


def review_file(directory: Path, name: str, **fields) -> Path:
    path = directory / name
    path.write_text(fileio.dumps_yaml(fields), encoding="utf-8")
    return path


def record_passing_reviews(repo: Repo, content_id: str, directory: Path, human_technical: bool = False) -> None:
    evidence = "Checked every segment and claim in the synthetic fixture."
    qc_review = review_file(directory, "qc.yaml", reviewer="content-qc-inspector (agent)", reviewer_type="agent", role="qc",
                            gates={g: {"result": "PASS", "evidence": evidence, "corrections": []} for g in ("G2", "G4", "G6", "G7")}, decision="PASS")
    tech = review_file(directory, "tech.yaml", reviewer="Kỹ thuật viên A" if human_technical else "technical-fact-checker (agent)",
                       reviewer_type="human" if human_technical else "agent", role="technical", qualified=human_technical,
                       gates={g: {"result": "PASS", "evidence": evidence, "corrections": []} for g in ("G3", "G5")}, decision="PASS")
    editorial = review_file(directory, "editorial.yaml", reviewer="Biên tập viên B", reviewer_type="human", role="editorial", gates={}, decision="PASS")
    for path in (qc_review, tech, editorial):
        code, out = run("qc_content", repo.root, "review", content_id, "--file", str(path))
        assert code == 0, out

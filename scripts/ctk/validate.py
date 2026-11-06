"""Repository-wide integrity validation (scripts/validate_content.py).

Errors break the repository's guarantees (an approval that no longer matches the
content, a published item without a URL, an unregistered ID...). Warnings point
at work in progress. Incomplete early-stage content is not an error: QC reports it.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from . import export, fileio, importer, mdparse, qc, schema
from .context import build_context
from .items import EXPORT_DIR, PERFORMANCE, RELEASE_EXPORT, find_items, today
from .registry import Registry
from .repo import Repo
from .sheet import TabSnapshot
from .sheet import is_youtube_url

REQUIRED_TEMPLATES = (
    "item.yaml", "content-brief.md", "research-report.md", "long-form-script.md", "short-script.md",
    "seo-package.md", "storyboard.md", "qc-report.md", "review.yaml", "performance.yaml",
)
POST_APPROVAL = ("APPROVED", "PUBLISHED", "PERFORMANCE_REVIEW")
# Deliverable that must be finished once an item has moved PAST the given stage.
STAGE_DELIVERABLES = {"RESEARCH": "research", "BRIEF": "brief", "SCRIPT": "script", "SEO": "seo", "PRODUCTION_PACKAGE": "storyboard"}


@dataclass
class Finding:
    level: str
    where: str
    message: str


def validate_repo(repo: Repo) -> list[Finding]:
    findings: list[Finding] = []
    findings += check_schemas(repo)
    findings += check_data(repo)
    findings += check_items(repo)
    findings += check_skills(repo)
    findings += check_templates(repo)
    findings += check_board(repo)
    return findings


def check_schemas(repo: Repo) -> list[Finding]:
    out = []
    for path in sorted(repo.schemas_dir.glob("*.schema.json")):
        try:
            data = fileio.load_json(path)
            if "$id" not in data:
                out.append(Finding("error", repo.rel(path), "Schema has no $id."))
            schema.validate({}, path)
        except Exception as exc:  # noqa: BLE001
            out.append(Finding("error", repo.rel(path), f"Invalid schema: {exc}"))
    return out


def check_data(repo: Repo) -> list[Finding]:
    out = []
    for tab in repo.config["sources"]["tabs"]:
        path = repo.path(tab["snapshot"])
        if not path.exists():
            out.append(Finding("error", tab["snapshot"], f"Snapshot for tab '{tab['title']}' is missing: tab is BLOCKED for import."))
            continue
        raw = fileio.load_json(path)
        for error in schema.validate(raw, repo.schemas_dir / "source-snapshot.schema.json"):
            out.append(Finding("error", tab["snapshot"], error))
        if TabSnapshot.from_dict(raw).content_hash() != raw.get("content_sha256"):
            out.append(Finding("error", tab["snapshot"], "Raw snapshot was edited by hand (content_sha256 no longer matches its values). Restore it from Git or re-capture the sheet."))
    for path in sorted(repo.normalized_dir.glob("*.json")):
        for error in schema.validate(fileio.load_json(path), repo.schemas_dir / "normalized-data.schema.json"):
            out.append(Finding("error", repo.rel(path), error))
    if repo.manifest_path.exists():
        manifest = fileio.load_json(repo.manifest_path)
        for rel, info in manifest.get("outputs", {}).items():
            path = repo.path(rel)
            if not path.exists():
                out.append(Finding("error", rel, "Listed in data/import-manifest.json but missing. Re-run scripts/import_sheet.py."))
            elif fileio.sha256_file(path) != info.get("sha256"):
                out.append(Finding("error", rel, "Generated file was edited by hand (hash differs from the import manifest). Re-run scripts/import_sheet.py --force, or move the edit to content/ or config/."))
    else:
        out.append(Finding("error", "data/import-manifest.json", "Missing: run scripts/import_sheet.py."))
    return out


def check_items(repo: Repo) -> list[Finding]:
    out = []
    items = find_items(repo)
    seen: dict[str, str] = {}
    ideas = {i["id"]: i for i in (repo.normalized("ideas") or {}).get("records", []) if "duplicate_of" not in i}
    for item in items:
        where = repo.rel(item.path)
        if item.id in seen:
            out.append(Finding("error", where, f"ID {item.id} is also used by {seen[item.id]}."))
        seen[item.id] = where
        errors = schema.validate(item.data, repo.schemas_dir / "content.schema.json")
        for error in errors:
            out.append(Finding("error", where + "/item.yaml", error))
        if errors:
            continue
        ctx = build_context(repo, item)
        for evidence, _ in qc.integrity_problems(ctx):
            out.append(Finding("error", where, evidence))
        out += _stage_rules(repo, ctx)
        out += _exports_and_performance(repo, ctx)
        reviews = [r["id"] for r in item.data["reviews"]]
        if len(reviews) != len(set(reviews)):
            out.append(Finding("error", where, "Duplicate review IDs in reviews."))
        out += _checklist_drift(repo, ctx)
        history = item.data["history"]
        if history and history[-1]["stage"] != item.stage:
            out.append(Finding("warning", where, f"Stage is {item.stage} but the last history entry says {history[-1]['stage']}; use scripts/set_status.py so changes are recorded."))
    for event in importer.workspace_drift(repo, ideas, Registry.load(repo.registry_path)):
        out.append(Finding("warning", str(event.get("item")), event["message"]))
    return out


def _stage_rules(repo: Repo, ctx) -> list[Finding]:
    out = []
    item, data = ctx.item, ctx.data
    where = repo.rel(item.path)
    stage = item.stage
    publication = data["publication"]
    if stage in POST_APPROVAL:
        if item.is_test:
            out.append(Finding("error", where, f"Test item is at {stage}; test items can never be approved or published."))
        approval_info = qc.approval(ctx, qc.run_gates(ctx))
        if approval_info["status"] != "APPROVABLE":
            tracker = {r["id"]: r for r in (repo.normalized("tracker") or {}).get("records", [])}
            source = tracker.get(data["provenance"].get("source_record") or item.id) or {}
            # Only a video the sheet itself records as published (date + link) may predate this QC system.
            legacy = data["provenance"]["origin"] == "sheet-tracker" and stage != "APPROVED" and source.get("stage_hint") == "PUBLISHED"
            level = "warning" if legacy else "error"
            missing = "; ".join(r["requirement"] for r in approval_info["requirements"] if not r["satisfied"])
            out.append(Finding(level, where, f"Stage {stage} without a valid approval on the current content ({missing}). Re-run QC and approve again."))
    if stage in ("PUBLISHED", "PERFORMANCE_REVIEW"):
        if not publication.get("url") or not is_youtube_url(publication["url"]):
            out.append(Finding("error", where, "Published item without a YouTube URL."))
        if not publication.get("published_at"):
            out.append(Finding("error", where, "Published item without a publish date."))
    elif publication.get("url") or publication.get("published_at"):
        out.append(Finding("error", where, f"Publish URL/date recorded at stage {stage}."))
    stage_ids = repo.stage_ids()
    for done_stage, key in STAGE_DELIVERABLES.items():
        if key == "storyboard" and item.format == "short":
            continue
        if stage_ids.index(stage) > stage_ids.index(done_stage) and mdparse.todo_count(ctx.texts[key]):
            out.append(Finding("warning", where, f"Stage {stage} is past {done_stage} but {key}.md still has [TODO] markers."))
    return out


def _checklist_drift(repo: Repo, ctx) -> list[Finding]:
    """Warn when an item's pre-approval checklist no longer matches the template."""
    template = mdparse.checkboxes(mdparse.find_section(fileio.read_text(repo.templates_dir / "seo-package.md"), "Publishing checklist"))
    current = mdparse.checkboxes(mdparse.find_section(ctx.texts["seo"], "Publishing checklist"))
    if not current or not template:
        return []
    missing = [label for _, label in template if label not in {l for _, l in current}]
    extra = [label for _, label in current if label not in {l for _, l in template}]
    if not missing and not extra:
        return []
    detail = []
    if missing:
        detail.append(f"missing {len(missing)} template item(s)")
    if extra:
        detail.append(f"{len(extra)} item(s) not in the template (upload steps belong in publication.upload_checklist)")
    return [Finding("warning", repo.rel(ctx.item.path) + "/seo.md", "Publishing checklist differs from templates/seo-package.md: " + "; ".join(detail) + ".")]


def _exports_and_performance(repo: Repo, ctx) -> list[Finding]:
    out = []
    item = ctx.item
    where = repo.rel(item.path)
    release = item.file(EXPORT_DIR) / RELEASE_EXPORT
    if item.stage in ("APPROVED", "PUBLISHED", "PERFORMANCE_REVIEW") and not release.exists() and not item.is_test:
        out.append(Finding("error", where, f"Stage {item.stage} but no release package: run python3 scripts/export_package.py {item.id}."))
    if release.exists() and item.stage not in ("APPROVED", "PUBLISHED", "PERFORMANCE_REVIEW"):
        out.append(Finding("error", repo.rel(release), f"Release package present but the stage is {item.stage}: delete it and approve again."))
    if release.exists():
        package = fileio.load_json(release)
        for error in schema.validate(package, repo.schemas_dir / "production-package.schema.json"):
            out.append(Finding("error", repo.rel(release), error))
        if package.get("package_status") != "APPROVED":
            out.append(Finding("error", repo.rel(release), "Only APPROVED packages may be committed as production-package.json."))
        if (package.get("generated") or {}).get("content_fingerprint") != ctx.fingerprint:
            out.append(Finding("error", repo.rel(release), "Release package is stale: the content changed after export. Re-run QC, approve, export."))
        if package.get("content_id") != item.id:
            out.append(Finding("error", repo.rel(release), "Release package belongs to another content ID."))
        # The committed package must be exactly what the exporter builds from the approved content.
        expected = export.build_package(ctx, approved=True, blocking=[], approval_reviews=(package.get("generated") or {}).get("approval_reviews") or [])
        for pkg in (expected, package):
            pkg.get("generated", {}).pop("date", None)
        if expected != package:
            out.append(Finding("error", repo.rel(release), "Release package differs from what the approved content produces (edited by hand?). Regenerate it with export_package.py."))
        known = {r["id"] for r in item.data["reviews"] if ctx.is_current(r)}
        if not set((package.get("generated") or {}).get("approval_reviews") or []) <= known:
            out.append(Finding("error", repo.rel(release), "Release package cites reviews that are not current reviews of this item."))
    performance = item.file(PERFORMANCE)
    if performance.exists():
        data = fileio.load_yaml(performance)
        for error in schema.validate(data, repo.schemas_dir / "performance.schema.json"):
            out.append(Finding("error", repo.rel(performance), error))
        if isinstance(data, dict) and data.get("content_id") != item.id:
            out.append(Finding("error", repo.rel(performance), "content_id does not match the workspace."))
        if isinstance(data, dict):
            if data.get("video_url") != item.data["publication"].get("url"):
                out.append(Finding("error", repo.rel(performance), "video_url differs from publication.url."))
            for snap in data.get("snapshots") or []:
                if not any(v is not None for v in (snap.get("metrics") or {}).values()):
                    out.append(Finding("error", repo.rel(performance), f"Snapshot {snap.get('captured_on')} has no real metric value."))
                if str(snap.get("captured_on", "")) > today():
                    out.append(Finding("error", repo.rel(performance), f"Snapshot date {snap.get('captured_on')} is in the future."))
        if item.stage not in ("PUBLISHED", "PERFORMANCE_REVIEW"):
            out.append(Finding("error", repo.rel(performance), "Performance data exists for an unpublished item."))
    return out


_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def check_skills(repo: Repo) -> list[Finding]:
    out = []
    skills_dir = repo.path("skills")
    for skill in sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.exists() else []:
        skill_file = skill / "SKILL.md"
        where = repo.rel(skill_file)
        if not skill_file.exists():
            out.append(Finding("error", repo.rel(skill), "Skill folder has no SKILL.md."))
            continue
        match = _FRONT_MATTER.match(fileio.read_text(skill_file))
        meta = fileio.loads_yaml(match.group(1)) if match else None
        if not isinstance(meta, dict):
            out.append(Finding("error", where, "SKILL.md must start with YAML front matter (--- name/description ---)."))
            continue
        if meta.get("name") != skill.name:
            out.append(Finding("error", where, f"Front matter name '{meta.get('name')}' must equal the folder name '{skill.name}'."))
        description = str(meta.get("description") or "")
        if not 30 <= len(description) <= 1024:
            out.append(Finding("error", where, "description must be 30-1024 characters and say when to use the skill."))
        link = repo.path(".claude", "skills", skill.name)
        if not link.exists():
            out.append(Finding("error", repo.rel(skill), f"Missing .claude/skills/{skill.name} (symlink to ../../skills/{skill.name}) for Claude Code discovery."))
        elif not (link / "SKILL.md").exists() or os.path.realpath(link) != os.path.realpath(skill):
            out.append(Finding("error", f".claude/skills/{skill.name}", f"Must point to skills/{skill.name}."))
    return out


def check_templates(repo: Repo) -> list[Finding]:
    return [Finding("error", f"templates/{name}", "Required template is missing.") for name in REQUIRED_TEMPLATES if not (repo.templates_dir / name).exists()]


def check_board(repo: Repo) -> list[Finding]:
    from .board import BOARD_PATH, render_board  # local import: board depends on qc

    path = repo.path(BOARD_PATH)
    if not path.exists() or fileio.read_text(path) != render_board(repo):
        return [Finding("warning", BOARD_PATH, "Content board is out of date: run python3 scripts/generate_board.py")]
    return []

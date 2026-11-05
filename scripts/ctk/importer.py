"""Import orchestration: raw snapshots -> normalized data, stable IDs, manifest, report.

``build`` is pure (reads files, returns results). ``apply`` writes them, refusing
to overwrite generated files that were edited by hand since the last import.
The importer never writes into ``content/``: editorial workspaces are only
compared with upstream data and differences are reported.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from . import fileio, sheet
from . import textutil as tu
from .registry import Registry
from .repo import Repo
from .sheet import Issue, TabSnapshot

GENERATED_BY = "scripts/import_sheet.py"
NORMALIZED_FORMAT = 1
REPORT_PATH = "reports/import-report.md"
DIRECTION_PARSERS = {"long-form-direction": "long-form", "short-direction": "short"}


@dataclass
class ImportResult:
    outputs: dict[str, str]
    registry: Registry
    manifest: dict[str, Any]
    issues: list[Issue]
    id_events: list[dict[str, Any]]
    drift: list[dict[str, Any]]
    tabs: list[dict[str, Any]]

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.level == "error"]


# ---------------------------------------------------------------------------
# Capture ingestion
# ---------------------------------------------------------------------------
def ingest_bundle(repo: Repo, bundle: dict[str, Any]) -> list[dict[str, Any]]:
    """Store a capture bundle as per-tab snapshots. Unchanged tabs keep their file."""
    cfg = repo.config["sources"]
    expected_id = cfg["spreadsheet"]["id"]
    bundle_id = (bundle.get("spreadsheet") or {}).get("id")
    if bundle_id != expected_id:
        raise ValueError(f"Capture is for spreadsheet {bundle_id!r}, expected {expected_id!r}.")
    by_title = {t["title"]: t for t in cfg["tabs"]}
    by_sheet_id = {t.get("sheet_id"): t for t in cfg["tabs"]}
    events: list[dict[str, Any]] = []
    seen: set[str] = set()
    for tab in bundle.get("tabs", []):
        data = dict(tab)
        data.setdefault("captured_at", bundle["captured_at"])
        data.setdefault("capture_method", bundle["capture_method"])
        new = TabSnapshot.from_dict(data, expected_id)
        tab_cfg = by_title.get(new.title) or by_sheet_id.get(new.sheet_id)
        if tab_cfg is None:
            path = repo.source_dir / f"extra-{new.sheet_id}-{tu.slugify(new.title)}.json"
        else:
            seen.add(tab_cfg["title"])
            path = repo.path(tab_cfg["snapshot"])
            if tab_cfg["title"] != new.title:
                events.append({"tab": new.title, "event": "tab-renamed", "detail": f"configured as {tab_cfg['title']!r}"})
        old = TabSnapshot.from_dict(fileio.load_json(path), expected_id) if path.exists() else None
        if old is not None:
            for attr in ("hyperlinks", "notes", "data_validation", "grid", "formats_sampled", "sheet_id", "index"):
                if getattr(new, attr) is None and getattr(old, attr) is not None:
                    setattr(new, attr, getattr(old, attr))
                    if attr in ("hyperlinks", "notes", "data_validation"):
                        new.capture_notes.append(f"{attr} carried over from the {old.captured_at} capture (not readable by {new.capture_method}).")
            if new.content_hash() == old.content_hash():
                events.append({"tab": new.title, "event": "unchanged", "snapshot": repo.rel(path)})
                continue
        fileio.write_text(path, new.to_text())
        events.append({"tab": new.title, "event": "updated" if old else "created", "snapshot": repo.rel(path)})
    for title in by_title:
        if title not in seen:
            events.append({"tab": title, "event": "missing-from-capture", "detail": "previous snapshot kept"})
    return events


# ---------------------------------------------------------------------------
# Build (pure)
# ---------------------------------------------------------------------------
def load_snapshots(repo: Repo) -> tuple[dict[str, TabSnapshot], list[dict[str, Any]], list[Issue]]:
    cfg = repo.config["sources"]
    sid = cfg["spreadsheet"]["id"]
    snaps: dict[str, TabSnapshot] = {}
    issues: list[Issue] = []
    for tab_cfg in cfg["tabs"]:
        path = repo.path(tab_cfg["snapshot"])
        if path.exists():
            snaps[tab_cfg["title"]] = TabSnapshot.from_dict(fileio.load_json(path), sid)
        else:
            issues.append(Issue("error", "snapshot-missing", f"No snapshot at {tab_cfg['snapshot']}; tab is BLOCKED until it is captured.", tab_cfg["title"]))
    extras = []
    for path in sorted(repo.source_dir.glob("extra-*.json")):
        snap = TabSnapshot.from_dict(fileio.load_json(path), sid)
        extras.append({"title": snap.title, "sheet_id": snap.sheet_id, "snapshot": repo.rel(path), "populated_range": snap.populated_range(), "non_empty_cells": snap.non_empty_cells()})
        issues.append(Issue("warning", "unconfigured-tab", "Captured tab has no parser in config/sources.yaml; raw snapshot kept only.", snap.title))
    return snaps, extras, issues


def build(repo: Repo) -> ImportResult:
    cfg = repo.config["sources"]
    taxonomy_cfg = repo.config["taxonomy"]
    status_map = repo.config["workflow"]["sheet_statuses"]
    tagline = repo.config["qc-policy"].get("brand_tagline", "")
    snaps, extra_tabs, issues = load_snapshots(repo)
    registry = Registry.load(repo.registry_path).copy()
    codes = repo.format_codes()

    tabs: list[dict[str, Any]] = []
    tab_issue_lists: dict[str, list[Issue]] = {}
    # Snapshot titles can differ from configured titles after a tab rename.
    alias = {snap.title: title for title, snap in snaps.items()}

    def issues_for(tab_title: str) -> list[Issue]:
        return tab_issue_lists.setdefault(alias.get(tab_title, tab_title), [])

    competitors: list[dict[str, Any]] | None = None
    personas: list[dict[str, Any]] | None = None
    directions: dict[str, tuple[TabSnapshot, dict[str, Any]]] = {}
    tracker_cfgs = []

    for tab_cfg in cfg["tabs"]:
        title = tab_cfg["title"]
        snap = snaps.get(title)
        tab_issues: list[Issue] = []
        tab_issue_lists[title] = tab_issues
        summary: dict[str, Any] = {
            "title": title,
            "sheet_id": tab_cfg.get("sheet_id"),
            "parser": tab_cfg["parser"],
            "snapshot": tab_cfg["snapshot"],
            "outputs": tab_cfg.get("outputs", []),
            "records": {},
        }
        tabs.append(summary)
        if snap is None:
            summary["status"] = "blocked"
            continue
        if tab_cfg.get("sheet_id") and snap.sheet_id and snap.sheet_id != tab_cfg["sheet_id"]:
            tab_issues.append(Issue("warning", "sheet-id-changed", f"Sheet ID {snap.sheet_id} differs from configured {tab_cfg['sheet_id']}.", title))
        summary.update(
            {
                "sheet_id": snap.sheet_id,
                "index": snap.index,
                "grid": snap.grid,
                "captured_at": snap.captured_at,
                "capture_method": snap.capture_method,
                "content_sha256": snap.content_hash(),
                "populated_range": snap.populated_range(),
                "non_empty_cells": snap.non_empty_cells(),
            }
        )
        parser = tab_cfg["parser"]
        if parser == "competitors":
            competitors = sheet.build_competitors(snap, cfg["competitor_fields"], tab_issues)
            summary["records"] = {"competitors": len(competitors)}
        elif parser == "personas":
            personas = sheet.build_personas(snap, cfg["persona_fields"], taxonomy_cfg["personas"], tab_issues)
            summary["records"] = {"personas": len(personas)}
        elif parser in DIRECTION_PARSERS:
            result = sheet.parse_direction(snap, DIRECTION_PARSERS[parser], cfg["direction_fields"], tab_issues)
            directions[parser] = (snap, result)
            kind = "pillars" if parser == "long-form-direction" else "short_categories"
            summary["records"] = {"settings": len(result["settings"]), kind: len(result["groups"]), "ideas": len(result["ideas"])}
        elif parser == "tracker":
            tracker_cfgs.append((tab_cfg, snap, summary))
        else:
            tab_issues.append(Issue("error", "unknown-parser", f"Unknown parser {parser!r}.", title))

    # ---- ideas and IDs -------------------------------------------------------------
    ideas: list[dict[str, Any]] = []
    for parser in DIRECTION_PARSERS:
        if parser in directions:
            ideas.extend(directions[parser][1]["ideas"])
    parsed_formats = {DIRECTION_PARSERS[p] for p in directions}
    captured = {fmt: directions[p][0].captured_at for p, fmt in DIRECTION_PARSERS.items() if p in directions}
    id_events: list[dict[str, Any]] = []
    first_by_key: dict[str, dict[str, Any]] = {}
    for idea in ideas:
        idea_key = f"idea:{idea['format']}:{tu.key(idea['title'])}"
        idea["_key"] = idea_key
        if idea_key in first_by_key:
            idea["duplicate_of"] = first_by_key[idea_key]["source"]["ref"]
            issues_for(idea["source"]["tab"]).append(
                Issue("warning", "duplicate-idea", f"Idea {idea['title']!r} repeats {idea['duplicate_of']}; it shares that ID.", idea["source"]["tab"], idea["source"]["ref"])
            )
        else:
            first_by_key[idea_key] = idea
    loose_seen: dict[str, dict[str, Any]] = {}
    for idea in first_by_key.values():
        lk = tu.loose_key(idea["title"])
        other = loose_seen.get(lk)
        if other and other["_key"] != idea["_key"]:
            issues_for(idea["source"]["tab"]).append(
                Issue("warning", "near-duplicate-idea", f"Idea {idea['title']!r} is nearly identical to {other['title']!r} ({other['source']['ref']}).", idea["source"]["tab"], idea["source"]["ref"])
            )
        loose_seen.setdefault(lk, idea)

    unique = list(first_by_key.values())
    current_keys = {idea["_key"] for idea in unique}
    pending = []
    for idea in unique:
        cid = registry.find_by_key(idea["_key"])
        if not cid:
            pending.append(idea)
            continue
        idea["id"] = cid
        entry = registry.entries[cid]
        if entry.get("state") != "active":
            registry.set_state(cid, "active")
            id_events.append({"id": cid, "event": "reactivated", "title": idea["title"], "source_ref": idea["source"]["ref"]})
        if entry.get("source_ref") != idea["source"]["ref"]:
            id_events.append({"id": cid, "event": "moved", "title": idea["title"], "source_ref": idea["source"]["ref"], "previous_ref": entry.get("source_ref")})
            entry["source_ref"] = idea["source"]["ref"]
    for idea in pending:
        code = codes[idea["format"]]
        ref = idea["source"]["ref"]
        renamed = next(
            (
                cid
                for cid, entry in sorted(registry.entries.items())
                if entry.get("origin") == "sheet-idea"
                and entry.get("state") == "active"  # only a change between two consecutive imports is a rename
                and cid.startswith(f"CTK-{code}-")
                and entry.get("key") not in current_keys
                and entry.get("source_ref") == ref
            ),
            None,
        )
        if renamed:
            previous = registry.entries[renamed]["title"]
            registry.rename(renamed, key=idea["_key"], title=idea["title"], source_ref=ref)
            idea["id"] = renamed
            id_events.append({"id": renamed, "event": "renamed", "title": idea["title"], "previous_title": previous, "source_ref": ref})
        else:
            cid = registry.allocate(code, origin="sheet-idea", title=idea["title"], allocated_at=captured[idea["format"]], key=idea["_key"], source_ref=ref)
            idea["id"] = cid
            id_events.append({"id": cid, "event": "allocated", "title": idea["title"], "source_ref": ref})
    for idea in ideas:
        if "duplicate_of" in idea:
            idea["id"] = first_by_key[idea["_key"]]["id"]
    code_to_format = {code: fmt for fmt, code in codes.items()}
    for cid, entry in sorted(registry.entries.items()):
        fmt = code_to_format.get(cid.split("-")[1])
        if entry.get("origin") == "sheet-idea" and entry.get("state") == "active" and fmt in parsed_formats and entry.get("key") not in current_keys:
            registry.set_state(cid, "missing-upstream")
            id_events.append({"id": cid, "event": "missing-upstream", "title": entry.get("title"), "source_ref": entry.get("source_ref")})

    # ---- taxonomy ------------------------------------------------------------------------
    pillars = directions["long-form-direction"][1]["groups"] if "long-form-direction" in directions else []
    categories = directions["short-direction"][1]["groups"] if "short-direction" in directions else []
    groups_by_format = {"long-form": pillars, "short": categories}
    group_names = {g["code"]: g["name"] for g in [*pillars, *categories]}

    # ---- trackers ------------------------------------------------------------------------
    idea_ids = {(idea["format"], tu.key(idea["title"])): idea["id"] for idea in unique}
    tracker_tabs = []
    tracker_records: list[dict[str, Any]] = []
    tracker_keys: dict[str, set[str]] = {}
    for tab_cfg, snap, summary in tracker_cfgs:
        fmt = tab_cfg["format"]
        tab_issues = tab_issue_lists[tab_cfg["title"]]
        result = sheet.parse_tracker(snap, fmt, cfg, groups_by_format[fmt], status_map, tab_issues)
        keys = tracker_keys.setdefault(fmt, set())
        for record in result["records"]:
            title_key = tu.key(record["title"])
            explicit = _explicit_id(record, codes[fmt])
            if explicit and explicit in registry.entries:
                record["id"] = explicit
                record["linked_idea"] = explicit in {i["id"] for i in unique}
                record["link_method"] = "explicit-id"
                continue
            if explicit:
                tab_issues.append(Issue("warning", "unknown-content-id", f"Row {record['source']['row']} names {explicit}, which is not a registered ID; matched by title instead.", tab_cfg["title"], f"A{record['source']['row']}"))
            if (fmt, title_key) in idea_ids:
                record["id"] = idea_ids[(fmt, title_key)]
                record["linked_idea"] = True
                record["link_method"] = "title"
                continue
            key = f"tracker:{fmt}:{title_key}"
            keys.add(key)
            cid = registry.find_by_key(key)
            if not cid:
                cid = registry.allocate(codes[fmt], origin="sheet-tracker", title=record["title"], allocated_at=snap.captured_at, key=key, source_ref=record["source"]["ref"])
                id_events.append({"id": cid, "event": "allocated", "title": record["title"], "source_ref": record["source"]["ref"]})
            elif registry.entries[cid].get("state") != "active":
                registry.set_state(cid, "active")
                id_events.append({"id": cid, "event": "reactivated", "title": record["title"], "source_ref": record["source"]["ref"]})
            record["id"] = cid
            record["linked_idea"] = False
            record["link_method"] = "new-tracker-id"
        summary["records"] = {"production_records": len(result["records"])}
        summary["rows"] = result["counts"]
        tracker_tabs.append({k: v for k, v in result.items() if k != "records"})
        tracker_records.extend(result["records"])
    for cid, entry in sorted(registry.entries.items()):
        fmt = code_to_format.get(cid.split("-")[1])
        if entry.get("origin") == "sheet-tracker" and entry.get("state") == "active" and fmt in tracker_keys and entry.get("key") not in tracker_keys[fmt]:
            registry.set_state(cid, "missing-upstream")
            id_events.append({"id": cid, "event": "missing-upstream", "title": entry.get("title"), "source_ref": entry.get("source_ref")})

    # ---- channel settings ------------------------------------------------------------------
    channel: dict[str, Any] = {}
    links: list[dict[str, Any]] = []
    for parser, fmt in DIRECTION_PARSERS.items():
        if parser not in directions:
            continue
        snap, result = directions[parser]
        channel[fmt] = _channel_section(result["settings"], tagline, issues_for(snap.title), snap.title)
        links.extend(result["links"])

    # ---- tab statuses -----------------------------------------------------------------------
    for summary in tabs:
        tab_issues = tab_issue_lists.get(summary["title"], [])
        if summary.get("status") != "blocked":
            summary["status"] = "error" if any(i.level == "error" for i in tab_issues) else "imported"
        summary["issues"] = {level: sum(1 for i in tab_issues if i.level == level) for level in ("error", "warning", "info")}
        issues.extend(tab_issues)

    # ---- documents ---------------------------------------------------------------------------
    def inputs(*titles: str) -> list[dict[str, Any]]:
        out = []
        for tab_cfg in cfg["tabs"]:
            if tab_cfg["title"] in titles and tab_cfg["title"] in snaps:
                snap = snaps[tab_cfg["title"]]
                out.append({"tab": snap.title, "snapshot": tab_cfg["snapshot"], "captured_at": snap.captured_at, "content_sha256": snap.content_hash()})
        return out

    def titles_for(*parsers: str) -> list[str]:
        return [t["title"] for t in cfg["tabs"] if t["parser"] in parsers]

    def doc(kind: str, parsers: tuple[str, ...], payload: dict[str, Any]) -> dict[str, Any]:
        return {"kind": kind, "normalized_format": NORMALIZED_FORMAT, "generated_by": GENERATED_BY, "inputs": inputs(*titles_for(*parsers)), **payload}

    idea_records = []
    for idea in sorted(ideas, key=lambda i: (i["id"], i["source"]["ref"])):
        record = {
            "id": idea["id"],
            "format": idea["format"],
            "group": idea["group"],
            "group_name": group_names.get(idea["group"], ""),
            "title": idea["title"],
            "record_type": "planning-idea",
            "source": idea["source"],
        }
        if "duplicate_of" in idea:
            record["duplicate_of"] = idea["duplicate_of"]
        idea_records.append(record)

    def group_doc(group: dict[str, Any]) -> dict[str, Any]:
        ids = [i["id"] for i in idea_records if i["group"] == group["code"] and "duplicate_of" not in i]
        return {**group, "idea_ids": ids, "idea_count": len(ids)}

    documents: dict[str, dict[str, Any]] = {}
    if competitors is not None:
        documents["data/normalized/competitors.json"] = doc(
            "competitors",
            ("competitors",),
            {"note": "Reach metrics are historical values recorded in the sheet at an unknown date; they are not current verified statistics.", "records": competitors},
        )
    if personas is not None:
        documents["data/normalized/personas.json"] = doc("personas", ("personas",), {"records": personas})
    if directions:
        documents["data/normalized/channel.json"] = doc("channel", tuple(DIRECTION_PARSERS), {"settings": channel, "linked_resources": links})
        documents["data/normalized/taxonomy.json"] = doc(
            "taxonomy", tuple(DIRECTION_PARSERS), {"pillars": [group_doc(g) for g in pillars], "short_categories": [group_doc(g) for g in categories]}
        )
        documents["data/normalized/ideas.json"] = doc("ideas", tuple(DIRECTION_PARSERS), {"records": idea_records})
    if tracker_cfgs:
        documents["data/normalized/tracker.json"] = doc(
            "tracker",
            ("tracker",),
            {
                "note": "Only rows with a title are production records. Template/example rows, placeholder filler and blank rows are classified, not imported.",
                "tabs": tracker_tabs,
                "records": sorted(tracker_records, key=lambda r: (r["format"], r["source"]["row"])),
            },
        )

    # Workspace drift depends on content/, so it is printed and validated, not written
    # into the committed report (keeps --check independent of editorial work).
    drift = workspace_drift(repo, {r["id"]: r for r in idea_records if "duplicate_of" not in r}, registry)

    outputs = {path: fileio.dumps_json(data) for path, data in documents.items()}
    report = render_report(repo, tabs, extra_tabs, documents, issues, registry, tracker_tabs)
    outputs[REPORT_PATH] = report
    manifest = build_manifest(repo, tabs, extra_tabs, outputs, documents)
    return ImportResult(outputs=outputs, registry=registry, manifest=manifest, issues=issues, id_events=id_events, drift=drift, tabs=tabs)


def _explicit_id(record: dict[str, Any], code: str) -> str | None:
    """A content ID written in the row (title, "Kịch bản" or an extra column) links it explicitly."""
    texts = [record.get("title") or "", record.get("script_ref") or "", *(record.get("extra") or {}).values()]
    for text in texts:
        match = re.search(rf"\bCTK-{code}-[0-9]{{4}}\b", str(text))
        if match:
            return match.group(0)
    return None


def _channel_section(settings: dict[str, Any], tagline: str, issues: list[Issue], tab_title: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if "channel_topic" in settings:
        out["channel_topic"] = settings["channel_topic"]
    if "video_types_raw" in settings:
        raw = settings["video_types_raw"]
        out["video_types"] = {
            "values": [tu.clean(v).rstrip(".") for v in raw["value"].split(",") if tu.clean(v)],
            "raw": raw["value"],
            "ref": raw["ref"],
        }
    if "duration_raw" in settings:
        raw = settings["duration_raw"]
        parsed = sheet.parse_duration(raw["value"])
        if parsed is None:
            issues.append(Issue("warning", "unparsed-duration", f"Duration {raw['value']!r} could not be parsed.", tab_title, raw["ref"]))
        out["duration"] = {"raw": raw["value"], "ref": raw["ref"], **(parsed or {})}
    if "cta" in settings:
        raw = settings["cta"]
        out["cta"] = {"text": raw["value"], "ref": raw["ref"], "includes_brand_tagline": bool(tagline) and tagline in raw["value"]}
    return out


def workspace_drift(repo: Repo, ideas_by_id: dict[str, dict[str, Any]], registry: Registry) -> list[dict[str, Any]]:
    """Compare editorial workspaces with upstream records. Never modifies them."""
    events = []
    for item_path in sorted(repo.content_dir.glob("*/*/item.yaml")):
        rel = repo.rel(item_path)
        try:
            data = fileio.load_yaml(item_path) or {}
        except Exception as exc:  # noqa: BLE001 - report and continue
            events.append({"item": rel, "event": "unreadable", "message": f"{rel} could not be read: {exc}"})
            continue
        provenance = data.get("provenance") or {}
        source_id = provenance.get("source_record")
        if not source_id:
            continue
        upstream = ideas_by_id.get(source_id)
        if upstream is None:
            state = registry.entries.get(source_id, {}).get("state", "unknown")
            if registry.entries.get(source_id, {}).get("origin") == "sheet-idea":
                events.append({"item": data.get("id"), "event": "source-missing", "message": f"{data.get('id')}: source idea {source_id} is {state} upstream; workspace left unchanged."})
            continue
        if tu.clean(provenance.get("source_title")) != upstream["title"]:
            events.append(
                {
                    "item": data.get("id"),
                    "event": "source-changed",
                    "message": f"{data.get('id')}: upstream title of {source_id} is now {upstream['title']!r} (workspace recorded {provenance.get('source_title')!r}); workspace left unchanged for manual review.",
                }
            )
    return events


def build_manifest(repo: Repo, tabs, extra_tabs, outputs: dict[str, str], documents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    cfg = repo.config["sources"]
    output_info = {}
    for path in sorted(outputs):
        info: dict[str, Any] = {"sha256": fileio.sha256_text(outputs[path])}
        records = documents.get(path, {}).get("records")
        if isinstance(records, list):
            info["records"] = len(records)
        output_info[path] = info
    captures = sorted({t.get("captured_at") for t in tabs if t.get("captured_at")})
    return {
        "manifest_format": 1,
        "generated_by": GENERATED_BY,
        "spreadsheet": {k: cfg["spreadsheet"][k] for k in ("id", "title", "url", "access")},
        "latest_capture_at": captures[-1] if captures else None,
        "tabs": tabs,
        "unconfigured_tabs": extra_tabs,
        "outputs": output_info,
        "id_registry": "data/id-registry.json",
        "linked_sources": cfg.get("linked_sources", []),
    }


# ---------------------------------------------------------------------------
# Apply / check
# ---------------------------------------------------------------------------
def apply(repo: Repo, result: ImportResult, force: bool = False) -> dict[str, list[str]]:
    old_manifest = fileio.load_json(repo.manifest_path) if repo.manifest_path.exists() else {}
    recorded = old_manifest.get("outputs", {})
    conflicts = []
    for rel, text in result.outputs.items():
        path = repo.path(rel)
        if not path.exists():
            continue
        current = fileio.sha256_file(path)
        if current == fileio.sha256_text(text):
            continue
        if current != recorded.get(rel, {}).get("sha256"):
            conflicts.append(rel)
    if conflicts and not force:
        return {"written": [], "conflicts": conflicts, "overwritten": []}
    written = []
    for rel, text in sorted(result.outputs.items()):
        if fileio.write_text(repo.path(rel), text):
            written.append(rel)
    if fileio.write_text(repo.registry_path, result.registry.to_text()):
        written.append(repo.rel(repo.registry_path))
    if fileio.write_text(repo.manifest_path, fileio.dumps_json(result.manifest)):
        written.append(repo.rel(repo.manifest_path))
    return {"written": written, "conflicts": [], "overwritten": conflicts}


def check(repo: Repo, result: ImportResult) -> list[str]:
    """Paths whose committed content differs from what the import would produce."""
    expected = dict(result.outputs)
    expected[repo.rel(repo.registry_path)] = result.registry.to_text()
    expected[repo.rel(repo.manifest_path)] = fileio.dumps_json(result.manifest)
    stale = []
    for rel, text in sorted(expected.items()):
        path = repo.path(rel)
        if not path.exists() or fileio.read_text(path) != text:
            stale.append(rel)
    return stale


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ") if value not in (None, "") else "—"


def render_report(repo, tabs, extra_tabs, documents, issues, registry, tracker_tabs) -> str:
    cfg = repo.config["sources"]
    lines: list[str] = []
    add = lines.append
    captures = sorted({(t.get("captured_at"), t.get("capture_method")) for t in tabs if t.get("captured_at")})
    add("# Spreadsheet import report")
    add("")
    add("> Generated by `scripts/import_sheet.py` from the raw snapshots in `data/source/`. Do not edit by hand.")
    add("")
    add(f"- **Source:** [{cfg['spreadsheet']['title']}]({cfg['spreadsheet']['url']}) (read-only, ID `{cfg['spreadsheet']['id']}`)")
    for captured_at, method in captures:
        add(f"- **Capture:** {captured_at} via `{method}`")
    add("")
    add("## Tabs")
    add("")
    add("| # | Tab | Sheet ID | Grid | Populated range | Non-empty cells | Status | Records | Issues (E/W/I) |")
    add("|---|---|---|---|---|---|---|---|---|")
    for summary in tabs:
        grid = summary.get("grid") or {}
        grid_text = f"{grid.get('row_count', '?')}×{grid.get('column_count', '?')}" if grid else "—"
        records = ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in summary.get("records", {}).items()) or "—"
        if summary.get("rows"):
            records += " (rows: " + ", ".join(f"{v} {k}" for k, v in summary["rows"].items()) + ")"
        counts = summary.get("issues", {})
        add(
            f"| {_cell(summary.get('index'))} | {summary['title']} | {_cell(summary.get('sheet_id'))} | {grid_text} | {_cell(summary.get('populated_range'))} "
            f"| {_cell(summary.get('non_empty_cells'))} | {summary['status']} | {records} | {counts.get('error', 0)}/{counts.get('warning', 0)}/{counts.get('info', 0)} |"
        )
    if extra_tabs:
        add("")
        add("Tabs captured without a configured parser (raw snapshot kept, not normalized):")
        for extra in extra_tabs:
            add(f"- {extra['title']} (`{extra['snapshot']}`, {extra['non_empty_cells']} non-empty cells)")
    add("")
    add("## Source records and generated records")
    add("")
    add("Everything below `data/` is derived from the spreadsheet. Editorial workspaces in `content/` are created in this repository and are never written by the importer.")
    add("")
    add("| Normalized file | Records |")
    add("|---|---|")
    for path, data in documents.items():
        if isinstance(data.get("records"), list):
            count = str(len(data["records"]))
        elif data.get("kind") == "taxonomy":
            count = f"{len(data['pillars'])} pillars, {len(data['short_categories'])} Shorts categories"
        else:
            count = "settings"
        add(f"| `{path}` | {count} |")
    if tracker_tabs:
        add("")
        add("## Publishing tracker reconciliation")
        add("")
        add("A row becomes a production record only when it has a title. Rows marked published also need a publish date and a link before the repository treats them as published.")
        for tracker in tracker_tabs:
            add("")
            add(f"### {tracker['tab']} ({tracker['format']})")
            add("")
            add("| Rows | Count | Classification | Values | Decision |")
            add("|---|---|---|---|---|")
            for group in tracker["row_groups"]:
                values = "; ".join(f"{k}={v}" for k, v in group["values"].items()) or "—"
                add(f"| {group['rows']} | {group['count']} | {group['classification']} | {_cell(values)} | {_decision(group['classification'])} |")
    add("")
    add("## Content IDs from the sheet")
    add("")
    add("Permanent IDs from `data/id-registry.json`. IDs are never reused: a record that disappears upstream is marked `missing-upstream`, and a title edited in place keeps its ID (previous titles are listed).")
    add("")
    add("| ID | Origin | State | Title | Source | Previous titles |")
    add("|---|---|---|---|---|---|")
    for cid, entry in sorted(registry.entries.items()):
        if entry.get("origin") not in ("sheet-idea", "sheet-tracker"):
            continue
        previous = "; ".join(entry.get("previous_titles", []))
        add(f"| {cid} | {entry['origin']} | {entry.get('state')} | {_cell(entry.get('title'))} | {_cell(entry.get('source_ref'))} | {_cell(previous)} |")
    add("")
    add("## Issues")
    add("")
    for level in ("error", "warning", "info"):
        level_issues = [i for i in issues if i.level == level]
        add(f"### {level.capitalize()} ({len(level_issues)})")
        add("")
        if not level_issues:
            add("None.")
        for issue in level_issues:
            where = f"{issue.tab} {issue.ref}".strip() if issue.tab or issue.ref else ""
            add(f"- `{issue.code}` {('(' + where + ') ') if where else ''}{issue.message}")
        add("")
    add("## Linked spreadsheets (audited, not imported)")
    add("")
    for linked in cfg.get("linked_sources", []):
        add(f"- **{linked['title']}** (`{linked['id']}`), referenced from {linked['referenced_from']}, audited {linked['audit_date']}: {linked['audit_summary']}")
    return "\n".join(lines).rstrip() + "\n"


def _decision(classification: str) -> str:
    return {
        "production-record": "Imported as a production record",
        "incomplete-record": "Not imported: has publishing data but no title (flagged)",
        "template-example": "Not imported: example/template row with no title, date or link",
        "placeholder-filler": "Ignored: placeholder values only",
        "blank": "Ignored: empty row",
    }.get(classification, classification)

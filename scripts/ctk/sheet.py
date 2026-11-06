"""Raw spreadsheet snapshots and the per-tab normalizers.

A *snapshot* preserves one tab exactly as captured (formatted cell values,
hyperlinks, notes, data-validation rules). Normalizers turn snapshots into
stable records and report every cell they ignore, so nothing is dropped silently.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Any
from urllib.parse import urlparse

from . import fileio
from . import textutil as tu

CAPTURE_FORMAT = 1
RLE_MIN_RUN = 5


# ---------------------------------------------------------------------------
# Cell references
# ---------------------------------------------------------------------------
def col_letter(index: int) -> str:
    """0 -> 'A', 25 -> 'Z', 26 -> 'AA'."""
    letters = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def a1(row: int, col: int) -> str:
    """A1 reference for a 1-based row and a 0-based column."""
    return f"{col_letter(col)}{row}"


def qualified(tab: str, ref: str) -> str:
    return f"'{tab}'!{ref}"


def row_span(rows: list[int]) -> str:
    """[9, 10, 11] -> '9-11'; [4] -> '4'."""
    return str(rows[0]) if len(rows) == 1 else f"{rows[0]}-{rows[-1]}"


# ---------------------------------------------------------------------------
# Value encoding (run-length encoding for long blocks of identical rows)
# ---------------------------------------------------------------------------
def canonical_row(row: list[Any]) -> list[Any]:
    out = ["" if value is None else value for value in row]
    while out and out[-1] == "":
        out.pop()
    return out


def expand_values(values: list[Any]) -> list[list[Any]]:
    rows: list[list[Any]] = []
    for entry in values:
        if isinstance(entry, dict):
            row = canonical_row(list(entry["row"]))
            rows.extend([list(row) for _ in range(int(entry["repeat"]))])
        else:
            rows.append(canonical_row(list(entry)))
    while rows and not rows[-1]:
        rows.pop()
    return rows


def compress_rows(rows: list[list[Any]], min_run: int = RLE_MIN_RUN) -> list[Any]:
    out: list[Any] = []
    i = 0
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and rows[j + 1] == rows[i]:
            j += 1
        run = j - i + 1
        if run >= min_run:
            out.append({"repeat": run, "row": rows[i]})
        else:
            out.extend(rows[i : j + 1])
        i = j + 1
    return out


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------
@dataclass
class Issue:
    level: str  # error | warning | info
    code: str
    message: str
    tab: str | None = None
    ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------
@dataclass
class TabSnapshot:
    spreadsheet_id: str
    title: str
    rows: list[list[Any]]
    captured_at: str
    capture_method: str
    sheet_id: int | None = None
    index: int | None = None
    grid: dict[str, Any] | None = None
    hyperlinks: dict[str, str] | None = None
    notes: dict[str, str] | None = None
    data_validation: list[dict[str, Any]] | None = None
    formats_sampled: dict[str, Any] | None = None
    capture_notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any], spreadsheet_id: str | None = None) -> "TabSnapshot":
        return cls(
            spreadsheet_id=data.get("spreadsheet_id") or spreadsheet_id or "",
            title=data.get("sheet_title") or data.get("title") or "",
            rows=expand_values(data.get("values") or []),
            captured_at=data.get("captured_at") or "",
            capture_method=data.get("capture_method") or "",
            sheet_id=data.get("sheet_id"),
            index=data.get("sheet_index", data.get("index")),
            grid=data.get("grid"),
            hyperlinks=data.get("hyperlinks"),
            notes=data.get("notes"),
            data_validation=data.get("data_validation"),
            formats_sampled=data.get("formats_sampled"),
            capture_notes=list(data.get("capture_notes") or []),
        )

    def content_hash(self) -> str:
        return fileio.sha256_obj(
            {
                "title": self.title,
                "sheet_id": self.sheet_id,
                "grid": self.grid or {},
                "values": self.rows,
                "hyperlinks": self.hyperlinks or {},
                "notes": self.notes or {},
                "data_validation": self.data_validation or [],
            }
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "capture_format": CAPTURE_FORMAT,
            "spreadsheet_id": self.spreadsheet_id,
            "sheet_id": self.sheet_id,
            "sheet_title": self.title,
            "sheet_index": self.index,
            "grid": self.grid,
            "captured_at": self.captured_at,
            "capture_method": self.capture_method,
            "capture_notes": self.capture_notes,
            "content_sha256": self.content_hash(),
            "populated_range": self.populated_range(),
            "non_empty_cells": self.non_empty_cells(),
            "hyperlinks": self.hyperlinks,
            "notes": self.notes,
            "data_validation": self.data_validation,
            "formats_sampled": self.formats_sampled,
            "values_encoding": "rows; {repeat, row} = identical consecutive rows",
            "values": compress_rows(self.rows),
        }
        return data

    def to_text(self) -> str:
        return dumps_snapshot(self.to_dict())

    def cell(self, row: int, col: int) -> Any:
        """Raw value for a 1-based row and 0-based column ('' when absent)."""
        if row < 1 or row > len(self.rows):
            return ""
        values = self.rows[row - 1]
        return values[col] if col < len(values) else ""

    def non_empty_cells(self) -> int:
        return sum(1 for row in self.rows for value in row if value != "")

    def populated_range(self) -> str | None:
        cells = [(r + 1, c) for r, row in enumerate(self.rows) for c, v in enumerate(row) if v != ""]
        if not cells:
            return None
        rows = [r for r, _ in cells]
        cols = [c for _, c in cells]
        return f"{a1(min(rows), min(cols))}:{a1(max(rows), max(cols))}"


def dumps_snapshot(data: dict[str, Any]) -> str:
    """JSON with one spreadsheet row per line (readable diffs)."""
    values = data.get("values", [])
    head = {k: v for k, v in data.items() if k != "values"}
    text = json.dumps(head, ensure_ascii=False, indent=2)
    if values:
        body = ",\n".join("    " + json.dumps(row, ensure_ascii=False) for row in values)
        block = '  "values": [\n' + body + "\n  ]"
    else:
        block = '  "values": []'
    return text[:-2] + ",\n" + block + "\n}\n"


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------
def _lookup(mapping: dict[str, str]) -> dict[str, str]:
    return {tu.key(label): name for label, name in mapping.items()}


def looks_like_url(value: str) -> bool:
    parsed = urlparse(value.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


_YOUTUBE_VIDEO = re.compile(
    r"^https://(?:(?:www\.|m\.)?youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|live/)|youtu\.be/)[A-Za-z0-9_-]{6,}(?:[?&#].*)?$"
)


def is_youtube_url(value: str) -> bool:
    """A link to one YouTube video (watch, shorts, live or youtu.be), not a channel or a look-alike host."""
    return bool(_YOUTUBE_VIDEO.match((value or "").strip()))


def parse_date(raw: str, formats: list[str]) -> date | None:
    text = tu.clean(raw)
    if not text:
        return None
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    if re.fullmatch(r"\d{4,6}(\.\d+)?", text):  # Sheets serial number (unformatted value)
        serial = float(text)
        if 20000 < serial < 80000:
            return date.fromordinal(date(1899, 12, 30).toordinal() + int(serial))
    return None


_DURATION = re.compile(r"^(?P<op><=|<|)\s*(?P<a>\d+)\s*(?:-\s*(?P<b>\d+)\s*)?(?P<unit>phut|giay|p|s)$")


def parse_duration(raw: str) -> dict[str, Any] | None:
    """'5-8 phút' -> 300..480 s; '< 60 giây' -> max 60 s (exclusive)."""
    match = _DURATION.match(tu.match_text(raw).replace(" - ", "-"))
    if not match:
        return None
    unit = 60 if match.group("unit") in ("phut", "p") else 1
    a = int(match.group("a")) * unit
    b = int(match.group("b")) * unit if match.group("b") else None
    op = match.group("op")
    if b is not None:
        return {"min_seconds": a, "max_seconds": b, "max_inclusive": True}
    if op == "<":
        return {"min_seconds": None, "max_seconds": a, "max_inclusive": False}
    if op == "<=":
        return {"min_seconds": None, "max_seconds": a, "max_inclusive": True}
    return {"min_seconds": None, "max_seconds": a, "max_inclusive": True}


# ---------------------------------------------------------------------------
# Transposed research tabs ("Đối thủ", "Khán giả")
# ---------------------------------------------------------------------------
def parse_transposed(tab: TabSnapshot, mapping: dict[str, str], issues: list[Issue]) -> list[dict[str, Any]]:
    """Column A holds field labels; each further column is one entity."""
    lookup = _lookup(mapping)
    if not tab.rows:
        issues.append(Issue("error", "empty-tab", "Tab has no data.", tab.title))
        return []
    header = tab.rows[0]
    if lookup.get(tu.key(header[0] if header else "")) != "name":
        issues.append(
            Issue("error", "unexpected-header", f"A1 should be the entity header, found {header[0] if header else ''!r}.", tab.title, "A1")
        )
    entity_cols = [c for c in range(1, len(header)) if not tu.is_blank(header[c])]
    entities: list[dict[str, Any]] = []
    for col in entity_cols:
        entity: dict[str, Any] = {"_col": col, "fields": {"name": tu.clean(header[col])}, "raw": {}, "links": {}, "extra": {}}
        if header[col] != entity["fields"]["name"]:
            entity["raw"]["name"] = header[col]
        entities.append(entity)

    for r_index in range(1, len(tab.rows)):
        rownum = r_index + 1
        row = tab.rows[r_index]
        label = tu.clean(row[0] if row else "")
        present = [c for c in range(1, len(row)) if row[c] != ""]
        if not label:
            if not present:
                continue
            refs = ", ".join(a1(rownum, c) for c in present)
            if all(tu.is_blank(row[c]) for c in present):
                issues.append(Issue("info", "whitespace-cells", f"Whitespace-only cell(s) ignored: {refs}.", tab.title, a1(rownum, present[0])))
            else:
                issues.append(Issue("warning", "unlabelled-values", f"Values without a row label were not imported: {refs}.", tab.title, a1(rownum, present[0])))
            continue
        name = lookup.get(tu.key(label))
        if name is None:
            issues.append(Issue("warning", "unmapped-label", f"Row label {label!r} is not mapped; values kept under 'extra'.", tab.title, a1(rownum, 0)))
        for entity in entities:
            col = entity["_col"]
            raw = row[col] if col < len(row) else ""
            value = tu.clean(raw)
            bucket = entity["fields"] if name else entity["extra"]
            slot = name or label
            bucket[slot] = value
            if raw not in ("", value):
                entity["raw"][slot] = raw
            link = (tab.hyperlinks or {}).get(a1(rownum, col))
            if link:
                entity["links"][slot] = link
        stray = [c for c in present if c not in entity_cols and not tu.is_blank(row[c])]
        if stray:
            refs = ", ".join(a1(rownum, c) for c in stray)
            issues.append(Issue("warning", "stray-cells", f"Cells outside entity columns were not imported: {refs}.", tab.title, a1(rownum, stray[0])))
    return entities


def last_labelled_row(tab: TabSnapshot) -> int:
    """Last row with a label in column A (transposed tabs)."""
    rows = [r + 1 for r, row in enumerate(tab.rows) if row and not tu.is_blank(row[0])]
    return rows[-1] if rows else 1


def _source_block(tab: TabSnapshot, col: int, last_row: int) -> dict[str, Any]:
    return {
        "tab": tab.title,
        "sheet_id": tab.sheet_id,
        "column": col_letter(col),
        "range": qualified(tab.title, f"{a1(1, col)}:{a1(last_row, col)}"),
    }


_METRIC = re.compile(r"(avg views|avg comments|subscribers?)\s*:\s*([^,]+)", re.IGNORECASE)
_METRIC_KEYS = {"avg views": "avg_views", "avg comments": "avg_comments", "subscriber": "subscribers", "subscribers": "subscribers"}


def build_competitors(tab: TabSnapshot, mapping: dict[str, str], issues: list[Issue]) -> list[dict[str, Any]]:
    entities = parse_transposed(tab, mapping, issues)
    records = []
    seen: set[str] = set()
    for entity in entities:
        fields = entity["fields"]
        slug = tu.slugify(fields["name"])
        if slug in seen:
            issues.append(Issue("warning", "duplicate-competitor", f"Competitor {fields['name']!r} appears twice.", tab.title))
        seen.add(slug)
        metrics_raw = fields.get("reach_metrics_raw", "")
        parsed = {_METRIC_KEYS[m.group(1).lower()]: m.group(2).strip() for m in _METRIC.finditer(metrics_raw)}
        keywords_raw = fields.get("seo_keywords_raw", "")
        url = entity["links"].get("youtube_url") or fields.get("youtube_url", "")
        record = {
            "id": slug,
            "name": fields["name"],
            "youtube_url": url,
            "content_strategy": fields.get("content_strategy", ""),
            "strengths": fields.get("strengths", ""),
            "weaknesses": fields.get("weaknesses", ""),
            "reach_metrics": {
                "raw": metrics_raw,
                "parsed": parsed,
                "status": "historical-unverified",
                "note": "Recorded in the sheet at an unknown date. Not current, not verified.",
            },
            "seo_keywords": [tu.clean(k) for k in re.findall(r'"([^"]+)"', keywords_raw)],
            "seo_keywords_raw": keywords_raw,
            "source": _source_block(tab, entity["_col"], last_labelled_row(tab)),
        }
        if entity["extra"]:
            record["extra"] = entity["extra"]
        if entity["raw"]:
            record["raw_values"] = entity["raw"]
        if url and not looks_like_url(url):
            issues.append(Issue("warning", "invalid-url", f"Competitor {fields['name']!r} has an invalid link.", tab.title))
        records.append(record)
    return records


def build_personas(tab: TabSnapshot, mapping: dict[str, str], persona_aliases: dict[str, list[str]], issues: list[Issue]) -> list[dict[str, Any]]:
    alias_index = {tu.key(alias): pid for pid, spec in persona_aliases.items() for alias in spec.get("aliases", [])}
    entities = parse_transposed(tab, mapping, issues)
    records = []
    for entity in entities:
        fields = entity["fields"]
        label = fields["name"]
        priority = "standard"
        name = label
        match = re.match(r"^(.*?)\s*\(ít\)\s*$", label)
        if match:
            priority, name = "low", match.group(1)
        pid = alias_index.get(tu.key(label)) or alias_index.get(tu.key(name))
        if not pid:
            pid = tu.slugify(name)
            issues.append(Issue("warning", "unknown-persona", f"Persona {label!r} has no canonical ID in config/taxonomy.yaml; using {pid!r}.", tab.title))
        demo_raw = fields.get("demographics_raw", "")
        demographics: dict[str, Any] = {"raw": demo_raw}
        rest = []
        for part in [p.strip() for p in demo_raw.split(",")]:
            low = tu.match_text(part)
            if low.startswith("tuoi:"):
                demographics["age_range"] = part.split(":", 1)[1].strip()
            elif low.startswith("gioi tinh:"):
                demographics["gender"] = part.split(":", 1)[1].strip()
            elif part:
                rest.append(part)
        if rest:
            demographics["description"] = ", ".join(rest)
        record = {
            "id": pid,
            "name": name,
            "label": label,
            "priority": priority,
            "demographics": demographics,
            "interests": fields.get("interests", ""),
            "pain_points": fields.get("pain_points", ""),
            "online_behavior": fields.get("online_behavior", ""),
            "preferred_content": fields.get("preferred_content", ""),
            "source": _source_block(tab, entity["_col"], last_labelled_row(tab)),
        }
        if priority == "low":
            record["priority_basis"] = "Label suffix '(ít)' (= few/less) in the sheet."
        if entity["extra"]:
            record["extra"] = entity["extra"]
        if entity["raw"]:
            record["raw_values"] = entity["raw"]
        records.append(record)
    return records


# ---------------------------------------------------------------------------
# Direction tabs ("Content Direction", "Short")
# ---------------------------------------------------------------------------
_GROUP_LABEL = {
    "long-form": (re.compile(r"^content pillar\s*(\d+)$"), "P"),
    "short": (re.compile(r"^the loai\s*(\d+)$"), "S"),
}


def parse_direction(tab: TabSnapshot, fmt: str, mapping: dict[str, str], issues: list[Issue]) -> dict[str, Any]:
    """Key/value settings rows, numbered group rows, and idea rows (columns D+)."""
    lookup = _lookup(mapping)
    pattern, prefix = _GROUP_LABEL[fmt]
    settings: dict[str, Any] = {}
    groups: list[dict[str, Any]] = []
    ideas: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    hyperlinks = tab.hyperlinks or {}

    for r_index, row in enumerate(tab.rows):
        rownum = r_index + 1
        if not any(value != "" for value in row):
            continue
        label = tu.clean(row[0] if row else "")
        if label:
            match = pattern.match(tu.match_text(label))
            if match:
                code = f"{prefix}{int(match.group(1))}"
                name_b = tu.clean(tab.cell(rownum, 1))
                name_d = tu.clean(tab.cell(rownum, 3))
                name = name_b or name_d
                variants = sorted({v for v in (name_b, name_d) if v and v != name})
                if name_b and name_d and tu.loose_key(name_b) != tu.loose_key(name_d):
                    issues.append(Issue("warning", "group-name-mismatch", f"{code}: column B {name_b!r} differs from column D {name_d!r}.", tab.title, a1(rownum, 1)))
                elif variants:
                    issues.append(Issue("info", "group-name-variant", f"{code}: spelling variant {variants[0]!r} (column D) of {name!r}; both map to {code}.", tab.title, a1(rownum, 3)))
                if any(g["code"] == code for g in groups):
                    issues.append(Issue("error", "duplicate-group", f"{code} is defined twice.", tab.title, a1(rownum, 0)))
                current = {
                    "code": code,
                    "name": name,
                    "variants": variants,
                    "label": label,
                    "source": {"tab": tab.title, "sheet_id": tab.sheet_id, "ref": qualified(tab.title, a1(rownum, 1))},
                }
                groups.append(current)
                extra = [c for c in range(4, len(row)) if not tu.is_blank(row[c])]
                if extra:
                    refs = ", ".join(a1(rownum, c) for c in extra)
                    issues.append(Issue("warning", "stray-cells", f"Unexpected cells on a group row were not imported: {refs}.", tab.title, a1(rownum, extra[0])))
                continue
            name = lookup.get(tu.key(label))
            if name:
                raw = tab.cell(rownum, 1)
                entry: dict[str, Any] = {"value": tu.clean(raw), "ref": qualified(tab.title, a1(rownum, 1))}
                if raw not in ("", entry["value"]):
                    entry["raw"] = raw
                settings[name] = entry
                for col in range(2, len(row)):
                    value = tu.clean(row[col])
                    link = hyperlinks.get(a1(rownum, col))
                    if link or (value and looks_like_url(value)):
                        links.append({"url": link or value, "text": value, "ref": qualified(tab.title, a1(rownum, col)), "context": name})
                    elif value:
                        issues.append(Issue("warning", "stray-cells", f"Unexpected cell {a1(rownum, col)} was not imported.", tab.title, a1(rownum, col)))
                continue
            issues.append(Issue("warning", "unmapped-label", f"Row label {label!r} is not mapped and was not imported; ideas below it are not attached to the previous group.", tab.title, a1(rownum, 0)))
            current = None
            continue

        unexpected = [c for c in (1, 2) if not tu.is_blank(tab.cell(rownum, c))]
        if unexpected:
            refs = ", ".join(a1(rownum, c) for c in unexpected)
            issues.append(Issue("warning", "stray-cells", f"Unexpected cells on an idea row were not imported: {refs}.", tab.title, a1(rownum, unexpected[0])))
        idea_cols = [c for c in range(3, len(row)) if not tu.is_blank(row[c])]
        if not idea_cols:
            continue
        if current is None:
            refs = ", ".join(a1(rownum, c) for c in idea_cols)
            issues.append(Issue("warning", "orphan-ideas", f"Ideas before any group row were not imported: {refs}.", tab.title, a1(rownum, idea_cols[0])))
            continue
        for col in idea_cols:
            raw = row[col]
            idea = {
                "format": fmt,
                "group": current["code"],
                "title": tu.clean(raw),
                "source": {
                    "tab": tab.title,
                    "sheet_id": tab.sheet_id,
                    "ref": qualified(tab.title, a1(rownum, col)),
                    "row": rownum,
                    "column": col_letter(col),
                },
            }
            if raw != idea["title"]:
                idea["source"]["raw"] = raw
            ideas.append(idea)
    return {"settings": settings, "groups": groups, "ideas": ideas, "links": links}


# ---------------------------------------------------------------------------
# Tracker tabs ("Video Publish", "Short Publish")
# ---------------------------------------------------------------------------
def parse_tracker(
    tab: TabSnapshot,
    fmt: str,
    sources_cfg: dict[str, Any],
    groups: list[dict[str, Any]],
    status_map: dict[str, Any],
    issues: list[Issue],
) -> dict[str, Any]:
    column_lookup = _lookup(sources_cfg["tracker_columns"])
    placeholders = {tu.key(p) for p in sources_cfg.get("placeholder_values", [])}
    formats = sources_cfg.get("date_formats", ["%d/%m/%Y"])
    earliest = date.fromisoformat(sources_cfg.get("earliest_plausible_date", "2005-04-23"))
    group_index = {}
    for group in groups:
        for name in [group["name"], *group.get("variants", [])]:
            group_index[tu.loose_key(name)] = group["code"]
    status_lookup = {tu.key(name): spec or {} for name, spec in status_map.items()}

    header = tab.rows[0] if tab.rows else []
    columns: dict[int, str] = {}
    extra_columns: dict[int, str] = {}
    for col, value in enumerate(header):
        hkey = tu.key(value)
        if not hkey:
            continue
        name = column_lookup.get(hkey)
        if name and name not in columns.values():
            columns[col] = name
        else:
            extra_columns[col] = tu.clean(value)
            issues.append(Issue("info", "unmapped-column", f"Column {col_letter(col)} {tu.clean(value)!r} is not mapped; values kept under 'extra'.", tab.title, a1(1, col)))
    for required in ("title", "category", "status"):
        if required not in columns.values():
            issues.append(Issue("error", "missing-column", f"Required column for {required!r} not found in row 1.", tab.title, "1:1"))
    last_col = col_letter(max([*columns, *extra_columns, 0]))

    classified: list[tuple[int, str, dict[str, str]]] = []
    records: list[dict[str, Any]] = []
    for r_index in range(1, len(tab.rows)):
        rownum = r_index + 1
        row = tab.rows[r_index]
        cleaned = {name: tu.clean(row[col] if col < len(row) else "") for col, name in columns.items()}
        for col, name in columns.items():
            link = (tab.hyperlinks or {}).get(a1(rownum, col))
            if name == "publish_url" and link and not looks_like_url(cleaned.get(name, "")):
                cleaned[name] = link
        extras = {extra_columns[c]: tu.clean(row[c]) for c in extra_columns if c < len(row) and not tu.is_blank(row[c])}
        meaningful = {k: v for k, v in cleaned.items() if v and tu.key(v) not in placeholders}
        if all(tu.is_blank(v) for v in row):
            cls = "blank"
        elif not meaningful and not extras:
            cls = "placeholder-filler"
        elif meaningful.get("title"):
            cls = "production-record"
        elif any(meaningful.get(k) for k in ("publish_date", "publish_url", "script")):
            cls = "incomplete-record"
            issues.append(Issue("warning", "record-without-title", f"Row {rownum} has publishing data but no title; not imported. Add a title in the sheet.", tab.title, f"A{rownum}"))
        else:
            cls = "template-example"
            spec = status_lookup.get(tu.key(cleaned.get("status", ""))) or {}
            if spec.get("stage") == "PUBLISHED":
                issues.append(Issue("info", "template-published-status", f"Row {rownum} says {cleaned['status']!r} but has no title, date or link; not treated as a published video.", tab.title, f"A{rownum}"))
        visible = {k: v for k, v in cleaned.items() if v}
        visible.update({f"extra:{k}": v for k, v in extras.items()})
        classified.append((rownum, cls, visible))
        if cls != "production-record":
            continue

        record = _tracker_record(tab, fmt, rownum, last_col, cleaned, meaningful, extras, group_index, status_lookup, formats, earliest, issues)
        records.append(record)

    by_title: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_title.setdefault(tu.key(record["title"]), []).append(record)
    for dupes in by_title.values():
        if len(dupes) > 1:
            rows = ", ".join(str(d["source"]["row"]) for d in dupes)
            issues.append(Issue("warning", "duplicate-title", f"Title {dupes[0]['title']!r} appears in rows {rows}; only the first row is linked to an ID.", tab.title))
            for dupe in dupes[1:]:
                dupe["duplicate_of_row"] = dupes[0]["source"]["row"]

    groups_out = []
    for rownum, cls, visible in classified:
        if groups_out and groups_out[-1]["classification"] == cls and groups_out[-1]["values"] == visible and groups_out[-1]["rows"][-1] == rownum - 1:
            groups_out[-1]["rows"].append(rownum)
        else:
            groups_out.append({"rows": [rownum], "classification": cls, "values": visible})
    row_groups = [
        {"rows": row_span(g["rows"]), "count": len(g["rows"]), "classification": g["classification"], "values": g["values"]}
        for g in groups_out
    ]
    counts: dict[str, int] = {}
    for _, cls, _ in classified:
        counts[cls] = counts.get(cls, 0) + 1
    return {
        "tab": tab.title,
        "format": fmt,
        "columns": {col_letter(c): name for c, name in sorted(columns.items())},
        "row_groups": row_groups,
        "counts": dict(sorted(counts.items())),
        "records": records,
    }


def _tracker_record(tab, fmt, rownum, last_col, cleaned, meaningful, extras, group_index, status_lookup, formats, earliest, issues):
    ref = f"A{rownum}"
    flags: list[str] = []
    category = cleaned.get("category", "")
    group = group_index.get(tu.loose_key(category)) if category else None
    if category and not group:
        flags.append("unknown-category")
        issues.append(Issue("warning", "unknown-category", f"Row {rownum}: category {category!r} matches no pillar/category.", tab.title, ref))
    status = cleaned.get("status", "")
    spec = status_lookup.get(tu.key(status)) if status else None
    if status and spec is None:
        flags.append("unknown-status")
        issues.append(Issue("warning", "unknown-status", f"Row {rownum}: status {status!r} is not a known sheet status.", tab.title, ref))
    spec = spec or {}

    publish_date = None
    raw_date = cleaned.get("publish_date", "")
    if raw_date:
        parsed = parse_date(raw_date, formats)
        if parsed is None:
            flags.append("invalid-date")
            issues.append(Issue("warning", "invalid-date", f"Row {rownum}: publish date {raw_date!r} is not a valid date (expected dd/MM/yyyy).", tab.title, ref))
        elif parsed < earliest:
            flags.append("implausible-date")
            issues.append(Issue("warning", "implausible-date", f"Row {rownum}: publish date {raw_date!r} is before YouTube existed.", tab.title, ref))
        else:
            publish_date = parsed.isoformat()

    url = cleaned.get("publish_url", "")
    publish_url = None
    if url:
        if is_youtube_url(url):
            publish_url = url
        elif looks_like_url(url):
            publish_url = url
            flags.append("non-youtube-url")
            issues.append(Issue("warning", "non-youtube-url", f"Row {rownum}: publish link is not a YouTube URL.", tab.title, ref))
        else:
            flags.append("invalid-url")
            issues.append(Issue("warning", "invalid-url", f"Row {rownum}: publish link {url!r} is not a URL.", tab.title, ref))

    stage_hint = spec.get("stage")
    if stage_hint == "PUBLISHED" and publish_date and publish_date > date.today().isoformat():
        flags.append("future-publish-date")
        issues.append(Issue("warning", "future-publish-date", f"Row {rownum} is marked 'Đã xuất bản' with a future date {publish_date}; not treated as published.", tab.title, ref))
        publish_date_evidence = None
    else:
        publish_date_evidence = publish_date
    if stage_hint == "PUBLISHED":
        missing = [name for name, value in (("publish_date", publish_date_evidence), ("publish_url", publish_url if publish_url and is_youtube_url(publish_url) else None)) if not value]
        if missing:
            stage_hint = None
            flags.append("published-without-evidence")
            issues.append(Issue("warning", "published-without-evidence", f"Row {rownum} is marked 'Đã xuất bản' but lacks {', '.join(missing)}; not treated as published.", tab.title, ref))

    record = {
        "format": fmt,
        "title": cleaned["title"],
        "category_raw": category,
        "group": group,
        "brand": meaningful.get("brand"),
        "model": meaningful.get("model"),
        "owner": meaningful.get("owner"),
        "sheet_status": status or None,
        "stage_hint": stage_hint,
        "on_hold": bool(spec.get("on_hold")),
        "publish_date": publish_date,
        "publish_date_raw": raw_date or None,
        "publish_url": publish_url,
        "script_ref": meaningful.get("script"),
        "flags": flags,
        "source": {"tab": tab.title, "sheet_id": tab.sheet_id, "row": rownum, "ref": qualified(tab.title, f"A{rownum}:{last_col}{rownum}")},
    }
    if extras:
        record["extra"] = extras
    return record

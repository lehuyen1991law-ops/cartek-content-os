"""Parsing of the machine-readable Markdown conventions used in content workspaces.

Conventions (see templates/long-form-script.md):
  * ``## <English key> (Vietnamese label)`` level-2 sections, matched by the English key.
  * Inside ``## Script``: ``### Sxx — Title`` segments with ``- **FIELD:** value`` lines.
  * ``[TODO ...]`` marks unfinished text. HTML comments are guidance and are ignored.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from . import textutil as tu

TODO = re.compile(r"\[TODO\b", re.IGNORECASE)
SEGMENT_FIELDS = ("TYPE", "VO", "VISUAL", "ON-SCREEN", "B-ROLL", "CLAIMS", "DEMO-SECONDS", "SAFETY", "NOTES")
SEGMENT_TYPES = ("hook", "intro", "body", "demo", "safety", "recap", "cta")
_FIELD_LINE = re.compile(r"^\s*[-*]\s+\*\*([A-Z][A-Z\-]*)\s*:\*\*\s?(.*)$")
_SEGMENT_HEAD = re.compile(r"^(S[0-9]{2,3})\b\s*[—–:-]*\s*(.*)$")
_LIST_ITEM = re.compile(r"^\s*(?:[0-9]+[.)]|[-*])\s+(.*)$")
_CHECKBOX = re.compile(r"^\s*[-*]\s+\[( |x|X)\]\s+(.*)$")


def visible(text: str) -> str:
    """Text without HTML comments (guidance)."""
    return tu.strip_html_comments(text or "")


def todo_count(text: str) -> int:
    return len(TODO.findall(visible(text)))


_TODO_SPAN = re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)


def without_todos(text: str) -> str:
    """Visible text with template prompts ``[TODO: ...]`` removed (they are not content)."""
    return _TODO_SPAN.sub(" ", visible(text))


def split_sections(text: str, level: int = 2) -> list[tuple[str, str]]:
    """[(heading, body)] for headings of exactly ``level``; text before the first heading is skipped."""
    marker = "#" * level
    pattern = re.compile(rf"^{marker}\s+(.+?)\s*$")
    sections: list[tuple[str, list[str]]] = []
    for line in visible(text).splitlines():
        match = pattern.match(line)
        if match and not line.startswith(marker + "#"):
            sections.append((match.group(1).strip(), []))
        elif sections:
            sections[-1][1].append(line)
    return [(heading, "\n".join(body).strip()) for heading, body in sections]


def find_section(text: str, key: str, level: int = 2) -> str | None:
    """Body of the first section whose heading starts with ``key`` (case-insensitive)."""
    wanted = key.casefold()
    for heading, body in split_sections(text, level):
        if heading.casefold().startswith(wanted):
            return body
    return None


def list_items(body: str | None) -> list[str]:
    """Top-level list items (numbered or bulleted), continuation lines joined."""
    items: list[str] = []
    for line in (body or "").splitlines():
        match = _LIST_ITEM.match(line)
        if match and not line.startswith((" " * 4, "\t")):
            items.append(match.group(1).strip())
        elif items and line.strip() and line.startswith((" ", "\t")):
            items[-1] += " " + line.strip()
    return [item for item in items if item]


def checkboxes(body: str | None) -> list[tuple[bool, str]]:
    return [(m.group(1).lower() == "x", m.group(2).strip()) for line in (body or "").splitlines() if (m := _CHECKBOX.match(line))]


def parse_fields(body: str) -> tuple[dict[str, str], list[str]]:
    """``- **KEY:** value`` lines; following non-field lines continue the value."""
    fields: dict[str, str] = {}
    unknown: list[str] = []
    current: str | None = None
    for line in body.splitlines():
        match = _FIELD_LINE.match(line)
        if match:
            current = match.group(1)
            if current not in SEGMENT_FIELDS and current not in ("HOOK", "RATIONALE"):
                unknown.append(current)
            fields[current] = match.group(2).strip()
        elif current and line.strip():
            fields[current] = (fields[current] + "\n" + line.strip().lstrip("> ").strip()).strip()
    return fields, unknown


def parse_table(body: str | None) -> list[dict[str, str]]:
    """First Markdown table in ``body`` as a list of row dicts (header -> cell)."""
    lines = [line.strip() for line in (body or "").splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return []
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not any(cells):
            continue
        rows.append({header[i]: (cells[i] if i < len(cells) else "") for i in range(len(header))})
    return rows


@dataclass
class Segment:
    id: str
    title: str
    fields: dict[str, str]

    def get(self, name: str) -> str:
        return self.fields.get(name, "").strip()

    @property
    def type(self) -> str:
        return self.get("TYPE").lower()

    @property
    def claims(self) -> list[str]:
        return [c for c in re.split(r"[,\s]+", self.get("CLAIMS")) if re.fullmatch(r"C[0-9]{2,3}", c)]

    @property
    def demo_seconds(self) -> float:
        try:
            return float(self.get("DEMO-SECONDS") or 0)
        except ValueError:
            return -1.0


@dataclass
class ScriptDoc:
    hook_candidates: list[str] = field(default_factory=list)
    selected_hook: dict[str, str] = field(default_factory=dict)
    outline: list[str] = field(default_factory=list)
    segments: list[Segment] = field(default_factory=list)
    retention_notes: list[str] = field(default_factory=list)
    missing_sections: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    todo_count: int = 0


REQUIRED_SCRIPT_SECTIONS = ("Hook candidates", "Selected hook", "Outline", "Script")


def parse_script(text: str) -> ScriptDoc:
    doc = ScriptDoc(todo_count=todo_count(text))
    for name in REQUIRED_SCRIPT_SECTIONS:
        if find_section(text, name) is None:
            doc.missing_sections.append(name)
    doc.hook_candidates = list_items(find_section(text, "Hook candidates"))
    selected, _ = parse_fields(find_section(text, "Selected hook") or "")
    doc.selected_hook = selected
    doc.outline = list_items(find_section(text, "Outline"))
    doc.retention_notes = list_items(find_section(text, "Retention notes"))
    body = find_section(text, "Script") or ""
    seen: set[str] = set()
    for heading, seg_body in split_sections(body, level=3):
        match = _SEGMENT_HEAD.match(heading)
        if not match:
            doc.problems.append(f"Heading '### {heading}' inside ## Script is not a segment (expected '### S01 — Title').")
            continue
        seg_id = match.group(1)
        if seg_id in seen:
            doc.problems.append(f"Segment {seg_id} appears more than once.")
        seen.add(seg_id)
        fields, unknown = parse_fields(seg_body)
        for name in unknown:
            doc.problems.append(f"Segment {seg_id}: unknown field **{name}:**")
        doc.segments.append(Segment(seg_id, match.group(2).strip(), fields))
    return doc


# ---------------------------------------------------------------------------
# Runtime estimate
# ---------------------------------------------------------------------------
def estimate_timing(segments: list[Segment], syllables_per_minute: float, transition_seconds: float) -> list[dict[str, Any]]:
    rows = []
    clock = 0.0
    for index, segment in enumerate(segments):
        vo = segment.get("VO")
        spoken = "" if TODO.search(vo) else vo
        syllables = tu.count_syllables(spoken)
        vo_seconds = syllables / syllables_per_minute * 60 if syllables_per_minute else 0
        demo = max(segment.demo_seconds, 0)
        gap = transition_seconds if index < len(segments) - 1 else 0
        total = vo_seconds + demo + gap
        rows.append(
            {
                "segment": segment.id,
                "type": segment.type,
                "syllables": syllables,
                "vo_seconds": round(vo_seconds, 1),
                "demo_seconds": demo,
                "start_seconds": round(clock, 1),
                "seconds": round(total, 1),
            }
        )
        clock += total
    return rows


def format_timestamp(seconds: float) -> str:
    seconds = int(round(seconds))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def parse_timestamp(value: str) -> int | None:
    parts = (value or "").strip().split(":")
    if not 2 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
        return None
    numbers = [int(p) for p in parts]
    if any(n >= 60 for n in numbers[1:]):
        return None
    total = 0
    for number in numbers:
        total = total * 60 + number
    return total

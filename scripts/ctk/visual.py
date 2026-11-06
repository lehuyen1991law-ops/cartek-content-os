"""Visual style layer: the effects/typography library (config/visual-style.yaml) applied to a storyboard.

The storyboard shot list may carry two optional columns:
  * ``Effects``     comma-separated effect ids from the library (e.g. ``code-popup, sfx-ui-beep``)
  * ``Text style``  comma-separated typography role ids (e.g. ``caption, dtc_code``)

Old storyboards without these columns parse to empty lists; nothing here raises on them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from . import mdparse

EFFECTS_COLUMN = "effects"
TEXT_STYLE_COLUMN = "text style"
SAFETY_EFFECT = "safety-banner"
_ID_SPLIT = re.compile(r"[,;\s]+")


def effects_index(library: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """{effect id: effect record} from config/visual-style.yaml."""
    return {e["id"]: e for e in (library or {}).get("effects") or [] if isinstance(e, dict) and e.get("id")}


def roles_index(library: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """{typography role id: role record}."""
    return dict(((library or {}).get("typography") or {}).get("roles") or {})


def split_ids(cell: str | None) -> list[str]:
    """Ids in a storyboard cell, in order, duplicates kept; TODO prompts and '-'/'none' ignored."""
    text = mdparse.without_todos(cell or "")
    return [p.lower() for p in _ID_SPLIT.split(text) if p and p.lower() not in ("-", "—", "none", "n/a")]


def column(row: dict[str, str], name: str) -> str:
    """Cell of the column whose header starts with ``name`` (case-insensitive), or ''."""
    wanted = name.casefold()
    for header, value in row.items():
        if header.casefold().startswith(wanted):
            return value or ""
    return ""


@dataclass
class Shot:
    shot: str
    segment: str
    effects: list[str] = field(default_factory=list)
    text_styles: list[str] = field(default_factory=list)


def shots(storyboard_text: str) -> list[Shot]:
    rows = mdparse.parse_table(mdparse.find_section(storyboard_text or "", "Shot list"))
    out = []
    for index, row in enumerate(rows, start=1):
        out.append(
            Shot(
                shot=column(row, "shot") or str(index),
                segment=column(row, "segment").upper(),
                effects=split_ids(column(row, EFFECTS_COLUMN)),
                text_styles=split_ids(column(row, TEXT_STYLE_COLUMN)),
            )
        )
    return out


@dataclass
class Usage:
    """What a storyboard uses from the library, and what it names that the library lacks."""

    shots: list[Shot]
    effects_used: dict[str, list[str]]        # effect id -> shot ids (ordered, duplicates kept)
    text_styles_used: dict[str, list[str]]    # role id -> shot ids
    unknown_effects: list[str]                # sorted, unique
    unknown_text_styles: list[str]
    segments_with_safety_banner: set[str]


def usage(storyboard_text: str, library: dict[str, Any]) -> Usage:
    effects = effects_index(library)
    roles = roles_index(library)
    rows = shots(storyboard_text)
    effects_used: dict[str, list[str]] = {}
    styles_used: dict[str, list[str]] = {}
    unknown_effects: set[str] = set()
    unknown_styles: set[str] = set()
    banner_segments: set[str] = set()
    for shot in rows:
        for eid in shot.effects:
            if eid in effects:
                effects_used.setdefault(eid, []).append(shot.shot)
                if eid == SAFETY_EFFECT and shot.segment:
                    banner_segments.add(shot.segment)
            else:
                unknown_effects.add(eid)
        for rid in shot.text_styles:
            if rid in roles:
                styles_used.setdefault(rid, []).append(shot.shot)
            else:
                unknown_styles.add(rid)
    return Usage(
        shots=rows,
        effects_used=dict(sorted(effects_used.items())),
        text_styles_used=dict(sorted(styles_used.items())),
        unknown_effects=sorted(unknown_effects),
        unknown_text_styles=sorted(unknown_styles),
        segments_with_safety_banner=banner_segments,
    )


def package_section(storyboard_text: str, library: dict[str, Any], source: str = "config/visual-style.yaml") -> dict[str, Any]:
    """The ``visual_style`` object of the production package (deterministic, no dates)."""
    use = usage(storyboard_text, library)
    effects = effects_index(library)
    roles = roles_index(library)
    fonts = (library or {}).get("fonts") or {}
    role_font_keys = {str(roles[r].get("font")) for r in use.text_styles_used if isinstance(roles.get(r), dict)}
    return {
        "source": source,
        "guide": str((library or {}).get("guide") or ""),
        "status": str((library or {}).get("status") or ""),
        "fonts": [
            {
                "id": key,
                "name": str(spec.get("name", "")),
                "role": str(spec.get("role", "")),
                "licence": str(spec.get("licence", "")),
                "source": str(spec.get("source", "")),
                "vietnamese_coverage": str(spec.get("vietnamese_coverage", "unconfirmed")),
                "used_by_storyboard": key in role_font_keys,
            }
            for key, spec in sorted(fonts.items())
            if isinstance(spec, dict)
        ],
        "typography_roles_used": [
            {
                "id": rid,
                "font": str(roles[rid].get("font", "")),
                "weight": roles[rid].get("weight"),
                "size_px_1080p": roles[rid].get("size_px_1080p"),
                "colour": str(roles[rid].get("colour", "")),
                "max_lines": roles[rid].get("max_lines"),
                "max_chars_per_line": roles[rid].get("max_chars_per_line"),
                "shots": shots_,
            }
            for rid, shots_ in use.text_styles_used.items()
        ],
        "effects_used": [
            {
                "id": eid,
                "kind": str(effects[eid].get("kind", "")),
                "description": str(effects[eid].get("description", "")),
                "never_use": str(effects[eid].get("never_use", "")),
                "shots": shots_,
            }
            for eid, shots_ in use.effects_used.items()
        ],
        "unknown_effects": use.unknown_effects,
        "unknown_text_styles": use.unknown_text_styles,
        "text_rules": [str(r) for r in (library or {}).get("text_rules") or []],
        "sound_rules": [str(r) for r in (library or {}).get("sound_rules") or []],
        "caption_rules": {
            "mandatory": bool(((library or {}).get("captions") or {}).get("mandatory", True)),
            "delivery": str(((library or {}).get("captions") or {}).get("delivery", "")),
            "rules": [str(r) for r in ((library or {}).get("captions") or {}).get("rules") or []],
        },
    }

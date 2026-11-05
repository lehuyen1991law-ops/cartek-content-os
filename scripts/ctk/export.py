"""Production package export: the handoff contract for an external video system.

Contract: schemas/production-package.schema.json (format cartek.production-package/v1).
A package is APPROVED only when the item's approval status is APPROVABLE for the
current content; otherwise it is a DRAFT_NOT_APPROVED package that must not be
used for production.
"""

from __future__ import annotations

from typing import Any

from . import mdparse
from .context import Context, within_target
from .items import today


def description_with_chapters(seo: dict[str, Any]) -> str:
    """The description as uploaded: text, then one 'MM:SS Title' line per chapter."""
    description = (seo.get("description") or "").rstrip()
    chapters = seo.get("chapters") or []
    if not chapters:
        return description
    lines = "\n".join(f"{c['time']} {c['title']}" for c in chapters)
    return f"{description}\n\n{lines}" if description else lines

PACKAGE_FORMAT = "cartek.production-package/v1"


def build_package(ctx: Context, approved: bool, blocking: list[str], approval_reviews: list[str] | None = None) -> dict[str, Any]:
    data = ctx.data
    timing = {row["segment"]: row for row in ctx.timing}
    segments = []
    for segment in ctx.script.segments:
        row = timing.get(segment.id, {})
        segments.append(
            {
                "id": segment.id,
                "type": segment.type,
                "title": segment.title,
                "narration": segment.get("VO"),
                "visual": segment.get("VISUAL"),
                "on_screen_text": segment.get("ON-SCREEN"),
                "broll": segment.get("B-ROLL"),
                "safety_note": segment.get("SAFETY"),
                "claims": segment.claims,
                "demo_seconds": max(segment.demo_seconds, 0),
                "estimated_start_seconds": row.get("start_seconds", 0),
                "estimated_seconds": row.get("seconds", 0),
            }
        )
    rate = ctx.production["speech_rate_syllables_per_minute"][ctx.item.format]
    group = ctx.groups.get(data.get("pillar"), {})
    seo = data.get("seo") or {}
    storyboard = mdparse.parse_table(mdparse.find_section(ctx.texts.get("storyboard", ""), "Shot list"))
    package: dict[str, Any] = {
        "package_format": PACKAGE_FORMAT,
        "package_status": "APPROVED" if approved else "DRAFT_NOT_APPROVED",
        "test_item": ctx.item.is_test,
        "content_id": ctx.item.id,
        "format": ctx.item.format,
        "language": data.get("language", "vi"),
        "generated": {
            "by": "scripts/export_package.py",
            "date": today(),
            "content_fingerprint": ctx.fingerprint,
            "approval_reviews": approval_reviews or [],
        },
        "delivery": {
            "platform": "youtube",
            "aspect_ratio": ctx.taxonomy["formats"][ctx.item.format]["aspect_ratio"],
        },
        "titles": {"working_title": data.get("working_title", ""), "final_title": seo.get("recommended_title", "")},
        "classification": {
            "pillar": data.get("pillar"),
            "pillar_name": group.get("name", ""),
            "video_type": data.get("video_type"),
            "audience": data.get("audience"),
            "vehicle": data.get("vehicle"),
        },
        "hook": {"selected": ctx.script.selected_hook.get("HOOK", ""), "rationale": ctx.script.selected_hook.get("RATIONALE", "")},
        "script": {"segments": segments},
        "voiceover": {
            "language": data.get("language", "vi"),
            "full_text": "\n\n".join(s["narration"] for s in segments if s["narration"]),
            "segments": [
                {
                    "segment_id": s.id,
                    "text": s.get("VO"),
                    "syllables": timing.get(s.id, {}).get("syllables", 0),
                    "estimated_seconds": timing.get(s.id, {}).get("vo_seconds", 0),
                }
                for s in ctx.script.segments
            ],
            "speech_rate_syllables_per_minute": rate,
            "speech_rate_calibrated": bool(ctx.production.get("speech_rate_calibrated")),
        },
        "shot_list": [
            {
                "shot_id": f"{s['id']}-01",
                "segment_id": s["id"],
                "visual": s["visual"],
                "broll": s["broll"],
                "on_screen_text": s["on_screen_text"],
                "estimated_seconds": s["estimated_seconds"],
            }
            for s in segments
        ],
        "storyboard_shots": storyboard,
        "on_screen_text": [{"segment_id": s["id"], "text": s["on_screen_text"]} for s in segments if s["on_screen_text"]],
        "broll_and_animation": [{"segment_id": s["id"], "instruction": s["broll"]} for s in segments if s["broll"]],
        "assets": (data.get("production") or {}).get("assets_required", []),
        "demo_setup": (data.get("production") or {}).get("demo_setup"),
        "timing": {
            "estimated_total_seconds": ctx.total_seconds,
            "target": {k: ctx.target.get(k) for k in ("min_seconds", "max_seconds", "max_inclusive", "source")},
            "within_target": within_target(ctx.total_seconds, ctx.target),
            "method": "Vietnamese syllables / speech rate (config/production.yaml) + DEMO-SECONDS + transitions",
        },
        "seo": {
            "title": seo.get("recommended_title", ""),
            "description": seo.get("description", ""),
            "description_with_chapters": description_with_chapters(seo) if ctx.item.format == "long-form" else seo.get("description", ""),
            "tags": seo.get("tags", []),
            "hashtags": seo.get("hashtags", []),
            "chapters": seo.get("chapters", []),
            "thumbnail_concepts": seo.get("thumbnail_concepts", []),
            "pinned_comment": seo.get("pinned_comment", ""),
        },
        "technical_claims": data.get("claims", []),
        "sources": data.get("sources", []),
        "safety": {
            "flags": (data.get("safety") or {}).get("flags", []),
            "dismissed": (data.get("safety") or {}).get("dismissed", []),
            "notes": [s["safety_note"] for s in segments if s["safety_note"]],
        },
        "blocking_issues": [] if approved else blocking,
    }
    return package

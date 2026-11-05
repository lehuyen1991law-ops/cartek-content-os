#!/usr/bin/env python3
"""Create a content workspace from a spreadsheet idea or from scratch.

Usage:
  python3 scripts/new_content.py --list-ideas [--search P0300] [--format long-form|short]
  python3 scripts/new_content.py --from-idea CTK-L-0015 [--audience technician] [--owner NAME]
  python3 scripts/new_content.py --format short --title "..." --pillar S1 [--audience car-owner]
  python3 scripts/new_content.py --from-idea CTK-L-0015 --test     # test item, ID range 9001+

Never overwrites an existing workspace. IDs come from data/id-registry.json.
"""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctk import fileio, qc  # noqa: E402
from ctk import textutil as tu  # noqa: E402
from ctk.items import Item, workspace_for, today  # noqa: E402
from ctk.registry import Registry  # noqa: E402
from ctk.repo import Repo  # noqa: E402

FORMAT_LABELS = {"long-form": "Long-form (16:9)", "short": "Shorts (9:16)"}


def runtime_text(repo: Repo, fmt: str) -> str:
    channel = repo.normalized("channel") or {}
    duration = ((channel.get("settings") or {}).get(fmt) or {}).get("duration") or {}
    return f"{duration.get('raw', 'n/a')} (nguồn: sheet {duration.get('ref', '')})".strip()


def cta_text(repo: Repo, fmt: str) -> str:
    channel = repo.normalized("channel") or {}
    text = (((channel.get("settings") or {}).get(fmt) or {}).get("cta") or {}).get("text", "")
    # The sheet's long-form CTA spells "subcribe"; strategy/brand-voice.md records the fix.
    return text.replace("subcribe", "subscribe")


def render(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    lines = template.split("\n")
    out: list[str] = []
    for line in lines:
        if line == "" and out and out[-1] == "":
            continue
        out.append(line)
    return "\n".join(out).rstrip() + "\n"


def list_ideas(repo: Repo, search: str | None, fmt: str | None) -> int:
    ideas = (repo.normalized("ideas") or {}).get("records", [])
    needle = tu.match_text(search) if search else ""
    rows = []
    for idea in ideas:
        if fmt and idea["format"] != fmt:
            continue
        if needle and needle not in tu.match_text(idea["title"]) and needle not in tu.match_text(idea["id"]):
            continue
        workspace = workspace_for(repo, idea["id"])
        rows.append(f"{idea['id']}  {idea['group']:<3} {'[workspace]' if workspace else '           '}  {idea['title']}")
    print("\n".join(rows) if rows else "No matching ideas.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root")
    parser.add_argument("--list-ideas", action="store_true")
    parser.add_argument("--search")
    parser.add_argument("--from-idea", metavar="ID")
    parser.add_argument("--format", choices=["long-form", "short"])
    parser.add_argument("--title")
    parser.add_argument("--pillar", help="P1..P5 for long-form, S1..S4 for Shorts")
    parser.add_argument("--audience", help="primary persona ID (data/normalized/personas.json)")
    parser.add_argument("--owner", default="")
    parser.add_argument("--test", action="store_true", help="create a clearly marked test item (ID 9001+)")
    parser.add_argument("--by", default="scripts/new_content.py", help="name recorded in the history")
    args = parser.parse_args(argv)
    repo = Repo(args.root)

    if args.list_ideas:
        return list_ideas(repo, args.search, args.format)

    taxonomy = repo.config["taxonomy"]
    registry = Registry.load(repo.registry_path)
    groups = {g["code"]: g for doc in [repo.normalized("taxonomy") or {}] for g in [*doc.get("pillars", []), *doc.get("short_categories", [])]}
    idea = None
    if args.from_idea:
        ideas = {i["id"]: i for i in (repo.normalized("ideas") or {}).get("records", [])}
        idea = ideas.get(args.from_idea)
        if idea is None:
            parser.error(f"{args.from_idea} is not in data/normalized/ideas.json (try --list-ideas).")
        fmt, title, pillar = idea["format"], idea["title"], idea["group"]
    else:
        if not (args.format and args.title and args.pillar):
            parser.error("give --from-idea, or all of --format, --title and --pillar")
        fmt, title, pillar = args.format, tu.clean(args.title), args.pillar
    if pillar not in groups or not pillar.startswith("P" if fmt == "long-form" else "S"):
        parser.error(f"{pillar} is not a {fmt} pillar/category. Options: {', '.join(c for c in groups if c.startswith('P' if fmt == 'long-form' else 'S'))}")

    code = repo.format_codes()[fmt]
    if args.test:
        content_id = registry.allocate(code, origin="test", title=f"TEST: {title}", allocated_at=today(), test=True, source_ref=idea["source"]["ref"] if idea else None)
        origin = "test"
    elif idea:
        content_id = idea["id"]
        origin = "sheet-idea"
    else:
        content_id = registry.allocate(code, origin="manual", title=title, allocated_at=today())
        origin = "manual"

    existing = workspace_for(repo, content_id)
    if existing:
        print(f"{content_id} already has a workspace: {repo.rel(existing)}. Nothing was changed.")
        return 1

    defaults = (taxonomy.get("pillar_defaults") or {}).get(pillar, {})
    audience = args.audience or defaults.get("audience", "technician")
    personas = {p["id"]: p for p in (repo.normalized("personas") or {}).get("records", [])}
    if audience not in personas:
        parser.error(f"unknown audience {audience!r}. Options: {', '.join(personas)}")
    depth = ((taxonomy.get("persona_defaults") or {}).get(audience) or {}).get("technical_depth", "intermediate")

    slug = ("test-" if args.test else "") + tu.slugify(title, 50)
    workspace = repo.format_dir(fmt) / f"{content_id}-{slug}"

    data = copy.deepcopy(fileio.load_yaml(repo.templates_dir / "item.yaml"))
    data.update(
        {
            "id": content_id,
            "format": fmt,
            "test_item": bool(args.test),
            "working_title": title,
            "pillar": pillar,
            "video_type": defaults.get("video_type", "explainer"),
            "search_intent": defaults.get("search_intent", "informational"),
            "owner": args.owner,
        }
    )
    data["audience"] = {"primary": audience, "secondary": [], "technical_depth": depth}
    data["status"] = {"stage": "IDEA", "on_hold": False, "hold_reason": ""}
    data["provenance"] = {
        "origin": origin,
        "source_record": idea["id"] if idea else None,
        "source_ref": idea["source"]["ref"] if idea else None,
        "source_title": idea["title"] if idea else None,
        "source_sha256": fileio.sha256_obj(idea) if idea else None,
        "created": today(),
    }
    note = f"Workspace created from {idea['id']} ({idea['source']['ref']})" if idea else "Workspace created manually"
    if args.test:
        note = "TEST ITEM for workflow acceptance. " + note
    item = Item(workspace, data)
    item.add_history("IDEA", args.by, note + ".")

    persona = personas[audience]
    values = {
        "id": content_id,
        "working_title": title,
        "format_label": FORMAT_LABELS[fmt],
        "pillar": pillar,
        "pillar_name": groups[pillar]["name"],
        "source_ref": f"{idea['id']} — {idea['source']['ref']}" if idea else "manual (not from the sheet)",
        "runtime_target": runtime_text(repo, fmt),
        "primary_audience": f"{persona['name']} (`{audience}`)",
        "brand_tagline": repo.config["qc-policy"]["brand_tagline"],
        "cta_text": cta_text(repo, fmt),
        "test_banner": qc.test_banner(bool(args.test)),
    }
    files = {
        "brief.md": "content-brief.md",
        "research.md": "research-report.md",
        "script.md": "long-form-script.md" if fmt == "long-form" else "short-script.md",
        "seo.md": "seo-package.md",
        "storyboard.md": "storyboard.md",
    }
    workspace.mkdir(parents=True, exist_ok=False)
    for target, template in files.items():
        fileio.write_text(workspace / target, render(fileio.read_text(repo.templates_dir / template), values))
    item.save()
    if registry.entries.get(content_id, {}).get("origin") in ("test", "manual"):
        fileio.write_text(repo.registry_path, registry.to_text())

    print(f"Created {content_id} at {repo.rel(workspace)}")
    print(f"  format={fmt} pillar={pillar} audience={audience} ({depth}) origin={origin}")
    if not args.audience:
        print(f"  note: primary audience defaulted to '{audience}' (config/taxonomy.yaml pillar_defaults); confirm it in the brief.")
    print("Next: research -> brief -> script (see CLAUDE.md). Check progress with:")
    print(f"  python3 scripts/qc_content.py run {content_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

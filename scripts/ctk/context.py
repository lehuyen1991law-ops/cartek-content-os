"""Everything QC and export need to know about one content item, loaded once."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import fileio, mdparse
from .items import DELIVERABLES, REVIEW_SCOPES, Item
from .registry import Registry
from .repo import Repo


@dataclass
class Context:
    repo: Repo
    item: Item
    policy: dict[str, Any]
    taxonomy: dict[str, Any]
    platform: dict[str, Any]
    production: dict[str, Any]
    groups: dict[str, dict[str, Any]]
    personas: dict[str, dict[str, Any]]
    ideas: dict[str, dict[str, Any]]
    registry: Registry
    features: dict[str, dict[str, Any]]
    texts: dict[str, str]
    script: mdparse.ScriptDoc
    timing: list[dict[str, Any]]
    total_seconds: float
    target: dict[str, Any]
    fingerprint: str
    technical_fingerprint: str = ""
    visual_style: dict[str, Any] = field(default_factory=dict)  # config/visual-style.yaml

    @property
    def data(self) -> dict[str, Any]:
        return self.item.data

    def fingerprint_for(self, role: str) -> str:
        return self.technical_fingerprint if REVIEW_SCOPES.get(role) == "technical" else self.fingerprint

    def is_current(self, review: dict[str, Any]) -> bool:
        """True when the review was recorded on the content it is responsible for, unchanged since."""
        return review.get("fingerprint") == self.fingerprint_for(review.get("role", ""))


def load_feature_register(repo: Repo) -> dict[str, dict[str, Any]]:
    if not repo.feature_register_path.exists():
        return {}
    register = fileio.load_yaml(repo.feature_register_path) or {}
    return {f["id"]: f for f in register.get("features") or [] if isinstance(f, dict) and f.get("id")}


def runtime_target(repo: Repo, item: Item) -> dict[str, Any]:
    exception = ((item.data.get("production") or {}).get("runtime_exception")) or None
    if exception:
        return {
            "min_seconds": exception.get("min_seconds"),
            "max_seconds": exception.get("max_seconds"),
            "max_inclusive": True,
            "source": "production.runtime_exception: " + str(exception.get("rationale", "")),
        }
    setting = repo.config["production"].get("runtime_targets", "from-source")
    if setting == "from-source":
        channel = repo.normalized("channel") or {}
        duration = ((channel.get("settings") or {}).get(item.format) or {}).get("duration") or {}
        return {
            "min_seconds": duration.get("min_seconds"),
            "max_seconds": duration.get("max_seconds"),
            "max_inclusive": duration.get("max_inclusive", True),
            "source": f"sheet {duration.get('ref')} \"{duration.get('raw')}\"",
        }
    target = dict(setting.get(item.format) or {})
    target.setdefault("max_inclusive", True)
    target["source"] = "config/production.yaml runtime_targets"
    return target


def describe_target(target: dict[str, Any]) -> str:
    lo, hi = target.get("min_seconds"), target.get("max_seconds")
    if lo is not None and hi is not None:
        return f"{mdparse.format_timestamp(lo)}-{mdparse.format_timestamp(hi)}"
    if hi is not None:
        return ("≤ " if target.get("max_inclusive", True) else "< ") + mdparse.format_timestamp(hi)
    return "no target"


def within_target(total: float, target: dict[str, Any]) -> bool:
    lo, hi = target.get("min_seconds"), target.get("max_seconds")
    if lo is not None and total < lo:
        return False
    if hi is not None:
        return total <= hi if target.get("max_inclusive", True) else total < hi
    return True


def build_context(repo: Repo, item: Item) -> Context:
    config = repo.config
    taxonomy_doc = repo.normalized("taxonomy") or {}
    groups = {g["code"]: g for g in [*taxonomy_doc.get("pillars", []), *taxonomy_doc.get("short_categories", [])]}
    personas = {p["id"]: p for p in (repo.normalized("personas") or {}).get("records", [])}
    ideas = {i["id"]: i for i in (repo.normalized("ideas") or {}).get("records", []) if "duplicate_of" not in i}
    texts = {key: item.text(key) for key in DELIVERABLES}
    script = mdparse.parse_script(texts["script"])
    fmt = item.format if item.format in ("long-form", "short") else "long-form"
    rate = config["production"]["speech_rate_syllables_per_minute"][fmt]
    transition = config["production"]["segment_transition_seconds"][fmt]
    timing = mdparse.estimate_timing(script.segments, rate, transition)
    return Context(
        repo=repo,
        item=item,
        policy=config["qc-policy"],
        taxonomy=config["taxonomy"],
        platform=config["platform-limits"],
        production=config["production"],
        groups=groups,
        personas=personas,
        ideas=ideas,
        registry=Registry.load(repo.registry_path),
        features=load_feature_register(repo),
        texts=texts,
        script=script,
        timing=timing,
        total_seconds=round(sum(row["seconds"] for row in timing), 1),
        target=runtime_target(repo, item),
        fingerprint=item.fingerprint(),
        technical_fingerprint=item.fingerprint("technical"),
        visual_style=config.get("visual-style") or {},
    )

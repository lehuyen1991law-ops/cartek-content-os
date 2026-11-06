"""Repository context: paths and configuration for one checkout.

Every script accepts ``--root`` so tests can run against a temporary copy.
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import Any

from . import fileio

DEFAULT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_FILES = ("sources", "taxonomy", "workflow", "qc-policy", "platform-limits", "production", "visual-style")


class Repo:
    def __init__(self, root: Path | str | None = None) -> None:
        self.root = Path(root).resolve() if root else DEFAULT_ROOT

    # ---- paths -----------------------------------------------------------------
    def path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    def rel(self, path: Path) -> str:
        return Path(path).resolve().relative_to(self.root).as_posix()

    @property
    def source_dir(self) -> Path:
        return self.path("data", "source")

    @property
    def normalized_dir(self) -> Path:
        return self.path("data", "normalized")

    @property
    def registry_path(self) -> Path:
        return self.path("data", "id-registry.json")

    @property
    def manifest_path(self) -> Path:
        return self.path("data", "import-manifest.json")

    @property
    def feature_register_path(self) -> Path:
        return self.path("data", "reference", "cartek-2-feature-register.yaml")

    @property
    def content_dir(self) -> Path:
        return self.path("content")

    @property
    def templates_dir(self) -> Path:
        return self.path("templates")

    @property
    def schemas_dir(self) -> Path:
        return self.path("schemas")

    @property
    def reports_dir(self) -> Path:
        return self.path("reports")

    # ---- configuration -----------------------------------------------------------
    @cached_property
    def config(self) -> dict[str, Any]:
        loaded: dict[str, Any] = {}
        for name in CONFIG_FILES:
            loaded[name] = fileio.load_yaml(self.path("config", f"{name}.yaml")) or {}
        return loaded

    def normalized(self, name: str) -> dict[str, Any] | None:
        path = self.normalized_dir / f"{name}.json"
        return fileio.load_json(path) if path.exists() else None

    def stage_ids(self) -> list[str]:
        return [stage["id"] for stage in self.config["workflow"]["stages"]]

    def stage_index(self, stage: str) -> int:
        return self.stage_ids().index(stage)

    def format_codes(self) -> dict[str, str]:
        """{'long-form': 'L', 'short': 'S'}"""
        return {name: spec["code"] for name, spec in self.config["taxonomy"]["formats"].items()}

    def format_dir(self, fmt: str) -> Path:
        return self.path(*self.config["taxonomy"]["formats"][fmt]["directory"].split("/"))

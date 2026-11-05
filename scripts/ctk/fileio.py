"""Deterministic file reading/writing and hashing helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


class _Loader(yaml.SafeLoader):
    """SafeLoader that keeps dates as strings (schemas expect 'YYYY-MM-DD' strings)."""


_Loader.yaml_implicit_resolvers = {
    first: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class _Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data: Any) -> bool:  # never emit &anchors
        return True


def _str_representer(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    # Values are never altered: block style only when it can represent the text exactly.
    if "\n" in data and not any(line != line.rstrip() for line in data.split("\n")):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if data.startswith("'"):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_Dumper.add_representer(str, _str_representer)


def load_yaml(path: Path) -> Any:
    with open(path, encoding="utf-8") as handle:
        return yaml.load(handle, Loader=_Loader)


def loads_yaml(text: str) -> Any:
    return yaml.load(text, Loader=_Loader)


def dumps_yaml(data: Any, header: str | None = None) -> str:
    body = yaml.dump(
        data,
        Dumper=_Dumper,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=100000,
    )
    if header:
        lines = "".join(f"# {line}\n" if line else "#\n" for line in header.splitlines())
        return lines + body
    return body


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def dumps_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(data: Any) -> str:
    return sha256_text(canonical_json(data))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> bool:
    """Write text (UTF-8, LF). Returns True when the file content changed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return True

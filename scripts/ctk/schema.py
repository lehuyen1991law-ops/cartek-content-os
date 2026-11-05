"""JSON Schema validation helpers (Draft 2020-12).

All schemas in ``schemas/`` are registered by their ``$id`` so relative
``$ref`` links between them resolve offline (no network access needed).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from . import fileio


@lru_cache(maxsize=None)
def _registry(schemas_dir: str) -> Registry:
    resources = []
    for path in sorted(Path(schemas_dir).glob("*.schema.json")):
        contents = fileio.load_json(path)
        resources.append((contents["$id"], Resource.from_contents(contents, default_specification=DRAFT202012)))
    return Registry().with_resources(resources)


@lru_cache(maxsize=None)
def _validator(schema_path: str) -> Draft202012Validator:
    path = Path(schema_path)
    schema = fileio.load_json(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, registry=_registry(str(path.parent)), format_checker=FormatChecker())


def validate(data: Any, schema_path: Path) -> list[str]:
    """Return human-readable error messages ('(root)' = document root)."""
    validator = _validator(str(Path(schema_path).resolve()))
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path]):
        location = "/".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"{location}: {error.message}")
    return errors

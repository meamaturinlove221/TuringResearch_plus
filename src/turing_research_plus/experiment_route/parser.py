"""Parser for the Experiment Route DSL."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.experiment_route.models import ExperimentRouteSpec


def parse_experiment_route(source: Path | dict[str, Any]) -> ExperimentRouteSpec:
    """Parse a route from JSON/YAML-like text or an in-memory mapping."""

    if isinstance(source, dict):
        return ExperimentRouteSpec.model_validate(source)

    text = source.read_text(encoding="utf-8")
    data = _parse_text(text)
    return ExperimentRouteSpec.model_validate(data)


def _parse_text(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None
    else:
        if isinstance(payload, dict):
            return payload
        raise ValueError("route spec must parse to a mapping")
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:
        raise ValueError("YAML route parsing requires PyYAML or JSON input") from exc
    loaded = yaml.safe_load(text)
    if not isinstance(loaded, dict):
        raise ValueError("route spec must parse to a mapping")
    return loaded

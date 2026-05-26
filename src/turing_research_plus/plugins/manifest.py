"""Load plugin manifests from local JSON or simple YAML."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.plugins.models import PluginCapability, PluginManifest


def load_plugin_manifest(path: Path) -> PluginManifest:
    """Load one local plugin manifest without importing plugin code."""

    payload = load_plugin_manifest_payload(path)
    return PluginManifest(**payload)


def load_plugin_manifest_payload(path: Path) -> dict[str, Any]:
    """Load one local plugin manifest payload without validating it."""

    payload = _load_mapping(path)
    payload["manifest_path"] = path
    if "capabilities" in payload:
        payload["capabilities"] = [
            PluginCapability(**capability) for capability in payload["capabilities"]
        ]
    return payload


def _load_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = _parse_simple_plugin_yaml(text)
    if not isinstance(data, dict):
        raise ValueError("plugin manifest must contain a mapping")
    return data


def _parse_simple_plugin_yaml(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by plugin fixtures."""

    result: dict[str, Any] = {}
    current_list_key: str | None = None
    current_mapping_list_item: dict[str, Any] | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0 and line.endswith(":"):
            key = line[:-1]
            result[key] = [] if key != "config_schema" else {}
            current_list_key = key
            current_mapping_list_item = None
            continue

        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = _parse_scalar(value.strip())
            current_list_key = None
            current_mapping_list_item = None
            continue

        if indent == 2 and current_list_key == "capabilities" and line.startswith("- "):
            item: dict[str, Any] = {}
            result[current_list_key].append(item)
            current_mapping_list_item = item
            remainder = line[2:].strip()
            if remainder:
                key, value = remainder.split(":", 1)
                item[key.strip()] = _parse_scalar(value.strip())
            continue

        if indent == 2 and current_list_key and line.startswith("- "):
            result[current_list_key].append(_parse_scalar(line[2:].strip()))
            current_mapping_list_item = None
            continue

        if indent == 4 and current_mapping_list_item is not None and ":" in line:
            key, value = line.split(":", 1)
            current_mapping_list_item[key.strip()] = _parse_scalar(value.strip())
            continue

        raise ValueError(f"unsupported plugin manifest YAML line: {raw_line!r}")

    return result


def _parse_scalar(value: str) -> object:
    if value == "":
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None"}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value

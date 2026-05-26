"""Load MCP plugin registry declarations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.mcp_plugins.models import MCPPluginEntry, MCPPluginRegistry


def load_mcp_plugin_registry(path: Path) -> MCPPluginRegistry:
    """Load a local MCP plugin registry manifest without starting MCP."""

    payload = _load_mapping(path)
    entries = [MCPPluginEntry(**entry) for entry in payload.get("entries", [])]
    return MCPPluginRegistry(
        registry_id=payload["registry_id"],
        entries=entries,
        warnings=list(payload.get("warnings", [])),
        requires_human_review=payload.get("requires_human_review", True),
    )


def _load_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = _parse_simple_mcp_registry_yaml(text)
    if not isinstance(data, dict):
        raise ValueError("MCP plugin registry must contain a mapping")
    return data


def _parse_simple_mcp_registry_yaml(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_list_key: str | None = None
    current_entry: dict[str, Any] | None = None
    current_entry_list_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0 and line.endswith(":"):
            key = line[:-1]
            result[key] = []
            current_list_key = key
            current_entry = None
            current_entry_list_key = None
            continue

        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = _parse_scalar(value.strip())
            current_list_key = None
            current_entry = None
            current_entry_list_key = None
            continue

        if indent == 2 and current_list_key == "entries" and line.startswith("- "):
            current_entry = {}
            result[current_list_key].append(current_entry)
            remainder = line[2:].strip()
            if remainder:
                key, value = remainder.split(":", 1)
                current_entry[key.strip()] = _parse_scalar(value.strip())
            continue

        if indent == 2 and current_list_key and line.startswith("- "):
            result[current_list_key].append(_parse_scalar(line[2:].strip()))
            continue

        if indent == 4 and current_entry is not None and line.endswith(":"):
            key = line[:-1]
            current_entry[key] = []
            current_entry_list_key = key
            continue

        if indent == 4 and current_entry is not None and ":" in line:
            key, value = line.split(":", 1)
            current_entry[key.strip()] = _parse_scalar(value.strip())
            current_entry_list_key = None
            continue

        if indent == 6 and current_entry is not None and current_entry_list_key:
            if line.startswith("- "):
                current_entry[current_entry_list_key].append(_parse_scalar(line[2:].strip()))
            continue

        raise ValueError(f"unsupported MCP plugin registry YAML line: {raw_line!r}")

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

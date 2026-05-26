"""Load docs-site navigation without third-party YAML dependencies."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from turing_research_plus.docs_site.models import (
    DocsSiteManifest,
    DocsSiteNav,
    DocsSiteNavItem,
)


def load_docs_site_nav(path: Path) -> DocsSiteNav:
    """Load the minimal docs-site nav YAML shape."""

    data = _parse_nav_yaml(path.read_text(encoding="utf-8"))
    return DocsSiteNav(
        site_title=str(data["site_title"]),
        status=str(data["status"]),
        items=[
            DocsSiteNavItem(
                item_id=str(item["id"]),
                title=str(item["title"]),
                page=str(item["page"]),
                source_docs=[
                    str(source)
                    for source in cast(list[object], item.get("source_docs", []))
                ],
            )
            for item in cast(list[dict[str, object]], data["items"])
        ],
    )


def load_docs_site_manifest(path: Path) -> DocsSiteManifest:
    """Load the minimal docs-site manifest YAML shape."""

    data = _parse_manifest_yaml(path.read_text(encoding="utf-8"))
    return DocsSiteManifest(
        site_id=str(data["site_id"]),
        status=str(data["status"]),
        source_of_truth=str(data["source_of_truth"]),
        local_first=bool(data.get("local_first", True)),
        deployment=str(data.get("deployment", "none")),
        cloud_dependency=bool(data.get("cloud_dependency", False)),
        large_frontend_framework=bool(data.get("large_frontend_framework", False)),
        private_data_required=bool(data.get("private_data_required", False)),
        fake_links_allowed=bool(data.get("fake_links_allowed", False)),
        required_sections=[
            str(section) for section in cast(list[object], data["required_sections"])
        ],
    )


def validate_nav_against_manifest(nav: DocsSiteNav, manifest: DocsSiteManifest) -> list[str]:
    """Return warnings for nav/manifest drift."""

    nav_ids = {item.item_id for item in nav.items}
    required = set(manifest.required_sections)
    warnings: list[str] = []
    missing = sorted(required - nav_ids)
    extra = sorted(nav_ids - required)
    if missing:
        warnings.append(f"missing required nav sections: {', '.join(missing)}")
    if extra:
        warnings.append(f"extra nav sections: {', '.join(extra)}")
    return warnings


def _parse_nav_yaml(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    items: list[dict[str, object]] = []
    current_item: dict[str, object] | None = None
    in_source_docs = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            key, value = _split_scalar(line)
            if key == "items":
                data["items"] = items
            else:
                data[key] = _parse_scalar(value)
            in_source_docs = False
            continue
        stripped = line.strip()
        if stripped.startswith("- id: "):
            current_item = {"id": stripped.split(": ", 1)[1], "source_docs": []}
            items.append(current_item)
            in_source_docs = False
            continue
        if current_item is None:
            continue
        if stripped == "source_docs:":
            current_item["source_docs"] = []
            in_source_docs = True
            continue
        if in_source_docs and stripped.startswith("- "):
            source_docs = cast(list[str], current_item.setdefault("source_docs", []))
            source_docs.append(stripped[2:])
            continue
        if ": " in stripped:
            key, value = _split_scalar(stripped)
            current_item[key] = _parse_scalar(value)
            in_source_docs = False

    data["items"] = items
    return data


def _parse_manifest_yaml(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list_key: str | None = None
    skip_nested = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            skip_nested = False
            if line.endswith(":"):
                key = line[:-1]
                if key == "required_sections":
                    data[key] = []
                    current_list_key = key
                else:
                    current_list_key = None
                    skip_nested = True
                continue
            key, value = _split_scalar(line)
            data[key] = _parse_scalar(value)
            current_list_key = None
            continue
        stripped = line.strip()
        if skip_nested:
            continue
        if current_list_key and stripped.startswith("- "):
            cast(list[str], data[current_list_key]).append(stripped[2:])

    return data


def _split_scalar(line: str) -> tuple[str, str]:
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> object:
    if value == "true":
        return True
    if value == "false":
        return False
    return value.strip('"').strip("'")

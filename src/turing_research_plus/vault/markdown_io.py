"""Markdown IO for Wiki Vault pages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.vault.models import VaultEntityType, VaultPage


def page_path(root: str | Path, page_id: str) -> Path:
    """Return the page path for a vault page ID."""

    return Path(root) / f"{page_id}.md"


def write_page(root: str | Path, page: VaultPage) -> Path:
    """Write a vault page as Markdown with JSON frontmatter."""

    path = page_path(root, page.page_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = {
        "page_id": page.page_id,
        "title": page.title,
        "entity_type": page.entity_type,
        "evidence": [evidence.model_dump(mode="json") for evidence in page.evidence],
        "artifact_id": page.artifact_id,
        "tags": page.tags,
        "metadata": page.metadata,
    }
    path.write_text(
        "---\n"
        + json.dumps(frontmatter, sort_keys=True)
        + "\n---\n\n"
        + page.body.strip()
        + "\n",
        encoding="utf-8",
    )
    return path


def read_page(path: str | Path) -> VaultPage:
    """Read a vault page from Markdown with JSON frontmatter."""

    text = Path(path).read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    return VaultPage(
        page_id=str(frontmatter["page_id"]),
        title=str(frontmatter["title"]),
        entity_type=VaultEntityType(str(frontmatter["entity_type"])),
        body=body.strip(),
        evidence=[EvidenceRef.model_validate(item) for item in frontmatter.get("evidence", [])],
        artifact_id=frontmatter.get("artifact_id"),
        tags=list(frontmatter.get("tags", [])),
        metadata=dict(frontmatter.get("metadata", {})),
    )


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split JSON frontmatter from Markdown body."""

    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    try:
        raw_frontmatter, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("missing closing frontmatter") from exc
    return json.loads(raw_frontmatter), body


def list_page_paths(root: str | Path) -> list[Path]:
    """List Markdown page paths."""

    path = Path(root)
    if not path.exists():
        return []
    return sorted(path.glob("*.md"))

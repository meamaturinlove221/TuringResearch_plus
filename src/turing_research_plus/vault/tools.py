"""Thin vault.* tool wrappers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tuling_research_plus.artifacts.models import EvidenceRef, ResearchArtifact
from tuling_research_plus.vault.models import VaultEdge, VaultPage
from tuling_research_plus.vault.service import VaultService


def _service(root: str | Path) -> VaultService:
    return VaultService(root)


def vault_search(root: str | Path, query: str, limit: int = 10) -> list[dict[str, Any]]:
    return [item.model_dump(mode="json") for item in _service(root).search(query, limit)]


def vault_ingest_source(
    root: str | Path,
    page_id: str,
    title: str,
    body: str,
    evidence: list[EvidenceRef],
) -> dict[str, Any]:
    return _service(root).ingest_source(page_id, title, body, evidence).model_dump(mode="json")


def vault_ingest_artifact(root: str | Path, artifact: ResearchArtifact) -> dict[str, Any]:
    return _service(root).ingest_artifact(artifact).model_dump(mode="json")


def vault_compile_page(root: str | Path, page: VaultPage) -> str:
    return str(_service(root).compile_page(page))


def vault_add_edge(root: str | Path, edge: VaultEdge) -> dict[str, Any]:
    return _service(root).add_edge(edge).model_dump(mode="json")


def vault_query_graph(root: str | Path, page_id: str, depth: int = 1) -> list[str]:
    return _service(root).query_graph(page_id, depth)


def vault_graph_stats(root: str | Path) -> dict[str, Any]:
    return _service(root).graph_stats().model_dump(mode="json")


def vault_lint(root: str | Path) -> list[dict[str, Any]]:
    return [issue.model_dump(mode="json") for issue in _service(root).lint()]


def vault_edge_audit(root: str | Path) -> list[dict[str, Any]]:
    return [edge.model_dump(mode="json") for edge in _service(root).edge_audit()]

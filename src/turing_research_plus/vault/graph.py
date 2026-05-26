"""Typed graph edge store for Wiki Vault."""

from __future__ import annotations

import json
from pathlib import Path

from tuling_research_plus.vault.markdown_io import list_page_paths, read_page
from tuling_research_plus.vault.models import VaultEdge, VaultGraphStats


class DuplicateEdgeError(ValueError):
    """Raised when adding a duplicate vault edge."""


class VaultGraph:
    """JSON edge store for vault graph relations."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.edge_path = self.root / "edges.json"
        if not self.edge_path.exists():
            self.edge_path.write_text("[]", encoding="utf-8")

    def list_edges(self) -> list[VaultEdge]:
        raw = json.loads(self.edge_path.read_text(encoding="utf-8"))
        return [VaultEdge.model_validate(item) for item in raw]

    def add_edge(self, edge: VaultEdge) -> VaultEdge:
        edges = self.list_edges()
        if edge.edge_key in {existing.edge_key for existing in edges}:
            raise DuplicateEdgeError("duplicate vault edge")
        edges.append(edge)
        self.edge_path.write_text(
            json.dumps([item.model_dump(mode="json") for item in edges], indent=2),
            encoding="utf-8",
        )
        return edge

    def neighbors(self, page_id: str, depth: int = 1) -> list[str]:
        edges = self.list_edges()
        seen: set[str] = set()
        frontier = {page_id}
        for _ in range(depth):
            next_frontier: set[str] = set()
            for edge in edges:
                if edge.source_id in frontier and edge.target_id not in seen:
                    next_frontier.add(edge.target_id)
                if edge.target_id in frontier and edge.source_id not in seen:
                    next_frontier.add(edge.source_id)
            seen.update(next_frontier)
            frontier = next_frontier
        seen.discard(page_id)
        return sorted(seen)

    def stats(self) -> VaultGraphStats:
        pages = [read_page(path) for path in list_page_paths(self.root)]
        edges = self.list_edges()
        connected = {edge.source_id for edge in edges} | {edge.target_id for edge in edges}
        orphans = [page for page in pages if page.page_id not in connected]
        return VaultGraphStats(
            page_count=len(pages),
            edge_count=len(edges),
            orphan_count=len(orphans),
        )

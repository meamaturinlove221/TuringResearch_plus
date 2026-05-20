"""Citation graph expansion."""

from __future__ import annotations

from collections import deque

from tuling_research_plus.semantic_graph.client import SemanticGraphAdapter
from tuling_research_plus.semantic_graph.models import (
    CitationEdge,
    CitationGraphExpandInput,
    CitationGraphOutput,
    GraphDirection,
    GraphStatus,
    PaperNode,
)


class CitationGraphBuilder:
    """Build citation graphs through an adapter boundary."""

    def __init__(self, adapter: SemanticGraphAdapter) -> None:
        self.adapter = adapter

    def expand(self, request: CitationGraphExpandInput) -> CitationGraphOutput:
        """Expand citation graph from seed papers."""

        nodes: dict[str, PaperNode] = {}
        edges: dict[tuple[str, str, GraphDirection], CitationEdge] = {}
        frontier: dict[str, PaperNode] = {}
        queue: deque[tuple[str, int]] = deque((paper_id, 0) for paper_id in request.seed_paper_ids)
        seen_depth: dict[str, int] = {}

        while queue and len(nodes) < request.max_nodes:
            paper_id, depth = queue.popleft()
            if seen_depth.get(paper_id, request.depth_limit + 1) <= depth:
                continue
            seen_depth[paper_id] = depth

            paper = self.adapter.paper_lookup(paper_id)
            if paper is not None and self._passes_filters(paper, request):
                nodes[paper.paper_id] = paper

            if depth >= request.depth_limit:
                if paper is not None:
                    frontier[paper.paper_id] = paper
                continue

            neighbors = self._neighbors(paper_id, request.direction)
            for neighbor, relation in neighbors:
                if not self._passes_filters(neighbor, request):
                    continue
                if len(nodes) >= request.max_nodes and neighbor.paper_id not in nodes:
                    frontier[neighbor.paper_id] = neighbor
                    continue
                nodes[neighbor.paper_id] = neighbor
                source, target = self._edge_direction(paper_id, neighbor.paper_id, relation)
                edges[(source, target, relation)] = CitationEdge(
                    source_id=source,
                    target_id=target,
                    relation=relation,
                )
                if neighbor.paper_id not in seen_depth:
                    queue.append((neighbor.paper_id, depth + 1))

        recommendations = self._recommend_next_reads(nodes, request)
        return CitationGraphOutput(
            status=GraphStatus.OK,
            nodes=list(nodes.values()),
            edges=list(edges.values()),
            frontier_nodes=list(frontier.values()),
            recommended_next_reads=recommendations,
        )

    def _neighbors(
        self,
        paper_id: str,
        direction: GraphDirection,
    ) -> list[tuple[PaperNode, GraphDirection]]:
        neighbors: list[tuple[PaperNode, GraphDirection]] = []
        if direction in (GraphDirection.BACKWARD, GraphDirection.BOTH):
            neighbors.extend(
                (paper, GraphDirection.BACKWARD)
                for paper in self.adapter.references(paper_id, limit=100)
            )
        if direction in (GraphDirection.FORWARD, GraphDirection.BOTH):
            neighbors.extend(
                (paper, GraphDirection.FORWARD)
                for paper in self.adapter.citations(paper_id, limit=100)
            )
        return neighbors

    def _passes_filters(self, paper: PaperNode, request: CitationGraphExpandInput) -> bool:
        if request.min_year is not None and (paper.year is None or paper.year < request.min_year):
            return False
        if request.max_year is not None and (paper.year is None or paper.year > request.max_year):
            return False
        if request.min_citation_count is not None:
            if paper.citation_count < request.min_citation_count:
                return False
        if request.open_access_only and not paper.is_open_access:
            return False
        return True

    def _edge_direction(
        self,
        paper_id: str,
        neighbor_id: str,
        relation: GraphDirection,
    ) -> tuple[str, str]:
        if relation == GraphDirection.BACKWARD:
            return paper_id, neighbor_id
        return neighbor_id, paper_id

    def _recommend_next_reads(
        self,
        nodes: dict[str, PaperNode],
        request: CitationGraphExpandInput,
    ) -> list[PaperNode]:
        candidates = self.adapter.recommendations(
            list(nodes.keys()),
            request.recommendation_limit * 2,
        )
        filtered = [
            paper
            for paper in candidates
            if paper.paper_id not in nodes and self._passes_filters(paper, request)
        ]
        filtered.sort(key=lambda paper: (paper.citation_count, paper.year or 0), reverse=True)
        return filtered[: request.recommendation_limit]

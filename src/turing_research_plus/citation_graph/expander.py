"""Citation graph expansion with fake, manual, and live-optional paths."""

from __future__ import annotations

from collections import deque
from typing import SupportsInt

from turing_research_plus.adapters.fake import FakeSemanticScholarAdapter
from turing_research_plus.adapters.models import (
    SemanticScholarPaperIdLookup,
    SemanticScholarPaperListLookup,
    SemanticScholarPaperLookup,
)
from turing_research_plus.adapters.semantic_scholar import SemanticScholarLiveAdapter
from turing_research_plus.citation_graph.frontier import select_frontier_nodes
from turing_research_plus.citation_graph.models import (
    CitationGraph,
    CitationGraphEdge,
    CitationGraphEdgeType,
    CitationGraphNode,
    CitationGraphRequest,
    CitationGraphRetrievalStatus,
    CitationGraphSourceAdapter,
)

SemanticScholarRequest = (
    SemanticScholarPaperLookup | SemanticScholarPaperListLookup | SemanticScholarPaperIdLookup
)


class CitationGraphExpander:
    """Expand a citation graph without networking by default."""

    def __init__(
        self,
        adapter: FakeSemanticScholarAdapter | SemanticScholarLiveAdapter | None = None,
    ) -> None:
        self.adapter = adapter or FakeSemanticScholarAdapter()

    def expand(self, request: CitationGraphRequest) -> CitationGraph:
        """Expand a graph using fake, manual, or explicitly live adapter mode."""

        if request.source_adapter == CitationGraphSourceAdapter.MANUAL:
            return self._manual_graph(request)
        if request.source_adapter == CitationGraphSourceAdapter.LIVE_SEMANTIC_SCHOLAR:
            return self._adapter_graph(request, live=True)
        return self._adapter_graph(request, live=False)

    def fake_vggt_related_work_graph(self) -> CitationGraph:
        """Build a deterministic VGGT-related fake graph."""

        seeds = [
            CitationGraphNode(
                paper_id="fake-vggt",
                title="VGGT fake seed",
                year=2025,
                topics=["VGGT", "human prior"],
            ),
            CitationGraphNode(
                paper_id="fake-smplx",
                title="SMPL-X fake seed",
                year=2019,
                topics=["SMPL-X"],
            ),
        ]
        request = CitationGraphRequest(
            graph_id="fake-vggt-related-work",
            seed_papers=seeds,
            seed_topics=[
                "VGGT",
                "SMPL-X",
                "NeuralBody",
                "HumanRAM",
                "HART",
                "VGGT-HPE",
                "HGGT",
                "Fus3D",
                "SparseConv3D",
                "human prior",
            ],
            expansion_depth=1,
            max_nodes=16,
            source_adapter=CitationGraphSourceAdapter.FAKE,
        )
        return self.expand(request)

    def _manual_graph(self, request: CitationGraphRequest) -> CitationGraph:
        nodes = self._dedupe_nodes(request.seed_papers)
        graph = CitationGraph(
            graph_id=request.graph_id,
            seed_papers=request.seed_papers,
            nodes=nodes,
            edges=request.manual_edges,
            frontier_nodes=[],
            expansion_depth=request.expansion_depth,
            filters=request.filters,
            source_adapter=request.source_adapter,
            retrieval_status=CitationGraphRetrievalStatus.MANUAL,
            limitations=[
                "Manual graph only; not a complete related work review.",
                "Requires human paper review before research conclusions.",
            ],
            requires_human_review=True,
        )
        graph.frontier_nodes = select_frontier_nodes(graph)
        return graph

    def _adapter_graph(self, request: CitationGraphRequest, *, live: bool) -> CitationGraph:
        nodes: dict[str, CitationGraphNode] = {
            node.paper_id: node
            for node in request.seed_papers
            if self._passes_filters(node, request)
        }
        edges: dict[tuple[str, str, CitationGraphEdgeType], CitationGraphEdge] = {}
        limitations = [
            "Citation graph is not a complete related work review.",
            "Live or fake retrieval is not human-verified by default.",
        ]
        queue: deque[tuple[CitationGraphNode, int]] = deque((node, 0) for node in nodes.values())

        if not nodes and request.seed_topics:
            for topic in request.seed_topics:
                lookup = SemanticScholarPaperLookup(query=topic, limit=1)
                self._configure_context(lookup, live=live)
                result = self.adapter.paper_lookup(lookup)
                if result.error is not None:
                    limitations.append(result.error.message)
                    continue
                for paper in result.papers:
                    node = self._node_from_paper(paper, topics=[topic])
                    nodes[node.paper_id] = node
                    queue.append((node, 0))

        while queue and len(nodes) < request.max_nodes:
            current, depth = queue.popleft()
            if depth >= request.expansion_depth:
                continue

            for neighbor, edge_type in self._neighbors(current.paper_id, live=live):
                if not self._passes_filters(neighbor, request):
                    continue
                edge = self._edge(current.paper_id, neighbor.paper_id, edge_type)
                edges[(edge.source_id, edge.target_id, edge.edge_type)] = edge
                if neighbor.paper_id not in nodes and len(nodes) < request.max_nodes:
                    nodes[neighbor.paper_id] = neighbor
                    queue.append((neighbor, depth + 1))

        graph = CitationGraph(
            graph_id=request.graph_id,
            seed_papers=request.seed_papers or list(nodes.values())[: len(request.seed_topics)],
            nodes=list(nodes.values()),
            edges=list(edges.values()),
            frontier_nodes=[],
            expansion_depth=request.expansion_depth,
            filters=request.filters,
            source_adapter=request.source_adapter,
            retrieval_status=(
                CitationGraphRetrievalStatus.RETRIEVED
                if live
                else CitationGraphRetrievalStatus.FAKE
            ),
            limitations=limitations,
            requires_human_review=True,
        )
        graph.frontier_nodes = select_frontier_nodes(graph)
        return graph

    def _neighbors(
        self, paper_id: str, *, live: bool
    ) -> list[tuple[CitationGraphNode, CitationGraphEdgeType]]:
        request = SemanticScholarPaperListLookup(paper_id=paper_id, limit=3)
        self._configure_context(request, live=live)
        refs = self.adapter.references(request)
        cites = self.adapter.citations(request)
        neighbors: list[tuple[CitationGraphNode, CitationGraphEdgeType]] = []
        if refs.error is None:
            neighbors.extend(
                (self._node_from_paper(paper), CitationGraphEdgeType.CITES)
                for paper in refs.papers
            )
        if cites.error is None:
            neighbors.extend(
                (self._node_from_paper(paper), CitationGraphEdgeType.CITED_BY)
                for paper in cites.papers
            )
        return neighbors

    def _configure_context(
        self,
        request: SemanticScholarRequest,
        *,
        live: bool,
    ) -> None:
        request.context.live_enabled = live
        request.context.dry_run = not live

    def _node_from_paper(
        self, paper: dict[str, object], topics: list[str] | None = None
    ) -> CitationGraphNode:
        paper_id = str(
            paper.get("paperId") or paper.get("paper_id") or paper.get("id") or "unknown"
        )
        authors = paper.get("authors")
        author_names = self._author_names(authors)
        return CitationGraphNode(
            paper_id=paper_id,
            title=str(paper.get("title") or "Untitled paper"),
            year=self._int_or_none(paper.get("year")),
            authors=author_names,
            citation_count=max(self._int_or_none(paper.get("citationCount")) or 0, 0),
            is_open_access=bool(paper.get("isOpenAccess") or paper.get("is_open_access") or False),
            topics=topics or self._infer_topics(str(paper.get("title") or "")),
            source_metadata={
                "provider": "semantic_scholar",
                "retrieval_status": "retrieved",
            },
            human_verified=False,
        )

    def _edge(
        self, source_id: str, target_id: str, edge_type: CitationGraphEdgeType
    ) -> CitationGraphEdge:
        if edge_type == CitationGraphEdgeType.CITED_BY:
            return CitationGraphEdge(
                source_id=target_id,
                target_id=source_id,
                edge_type=edge_type,
                evidence="adapter citation edge",
            )
        return CitationGraphEdge(
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            evidence="adapter citation edge",
        )

    def _passes_filters(self, node: CitationGraphNode, request: CitationGraphRequest) -> bool:
        filters = request.filters
        if filters.min_year is not None and (node.year is None or node.year < filters.min_year):
            return False
        if filters.max_year is not None and (node.year is None or node.year > filters.max_year):
            return False
        if filters.open_access_only and not node.is_open_access:
            return False
        if (
            filters.min_citation_count is not None
            and node.citation_count < filters.min_citation_count
        ):
            return False
        return True

    def _infer_topics(self, title: str) -> list[str]:
        lower = title.lower()
        topics = []
        for topic in [
            "VGGT",
            "SMPL-X",
            "NeuralBody",
            "HumanRAM",
            "HART",
            "VGGT-HPE",
            "HGGT",
            "Fus3D",
            "SparseConv3D",
            "human prior",
        ]:
            if topic.lower() in lower:
                topics.append(topic)
        return topics

    def _author_names(self, authors: object) -> list[str]:
        if not isinstance(authors, list):
            return []
        names: list[str] = []
        for author in authors:
            if isinstance(author, str):
                names.append(author)
            elif isinstance(author, dict) and author.get("name"):
                names.append(str(author["name"]))
        return names

    def _dedupe_nodes(self, nodes: list[CitationGraphNode]) -> list[CitationGraphNode]:
        return list({node.paper_id: node for node in nodes}.values())

    def _int_or_none(self, value: object) -> int | None:
        if value is None:
            return None
        if not isinstance(value, str | bytes | bytearray | SupportsInt):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

from __future__ import annotations

from tests.workflow.example_helpers import assert_example_contract, read_json, to_pretty_json

from turing_research_plus.semantic_graph.models import (
    CitationGraphExpandInput,
    GraphDirection,
    GraphStatus,
    PaperNode,
)
from turing_research_plus.semantic_graph.service import SemanticGraphService


class FakeSemanticGraphAdapter:
    def __init__(self) -> None:
        self.papers = {
            "seed-vggt-1": PaperNode(
                paper_id="seed-vggt-1",
                title="Seed VGGT Paper",
                year=2024,
                citation_count=42,
                is_open_access=True,
            ),
            "ref-human-priors": PaperNode(
                paper_id="ref-human-priors",
                title="Human Priors for Reconstruction",
                year=2023,
                citation_count=30,
                is_open_access=True,
            ),
            "cite-scene-priors": PaperNode(
                paper_id="cite-scene-priors",
                title="Scene Priors After VGGT",
                year=2025,
                citation_count=12,
                is_open_access=True,
            ),
            "next-read-1": PaperNode(
                paper_id="next-read-1",
                title="Recommended Human Geometry Read",
                year=2025,
                citation_count=50,
                is_open_access=True,
            ),
        }

    def paper_lookup(self, paper_id: str) -> PaperNode | None:
        return self.papers.get(paper_id)

    def paper_batch(self, paper_ids: list[str]) -> list[PaperNode]:
        return [self.papers[paper_id] for paper_id in paper_ids if paper_id in self.papers]

    def references(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        if paper_id == "seed-vggt-1":
            return [self.papers["ref-human-priors"]]
        return []

    def citations(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        if paper_id == "seed-vggt-1":
            return [self.papers["cite-scene-priors"]]
        return []

    def recommendations(self, paper_ids: list[str], limit: int = 10) -> list[PaperNode]:
        return [self.papers["next-read-1"]][:limit]

    def author(self, author_id: str) -> None:
        return None

    def author_papers(self, author_id: str) -> list[PaperNode]:
        return []


def test_citation_graph_example_dry_run_outputs_required_artifacts() -> None:
    required = {"CitationGraph", "recommended_next_reads", "frontier nodes"}
    assert_example_contract("citation-graph-demo", required)
    request = read_json("citation-graph-demo/input/request.json")

    graph = SemanticGraphService(FakeSemanticGraphAdapter()).citation_graph_expand(
        CitationGraphExpandInput(
            seed_paper_ids=request["seed_paper_ids"],
            direction=GraphDirection(request["direction"]),
            depth_limit=request["depth_limit"],
            max_nodes=request["max_nodes"],
            recommendation_limit=request["recommendation_limit"],
        )
    )
    output = {
        "CitationGraph": graph.model_dump(mode="json"),
        "recommended_next_reads": [
            paper.model_dump(mode="json") for paper in graph.recommended_next_reads
        ],
        "frontier nodes": [paper.model_dump(mode="json") for paper in graph.frontier_nodes],
    }
    markdown = "\n".join(
        [
            "# Citation Graph Demo Dry Run",
            f"- Nodes: {len(graph.nodes)}",
            f"- Frontier nodes: {len(graph.frontier_nodes)}",
            f"- Recommended next reads: {len(graph.recommended_next_reads)}",
        ]
    )

    assert set(output) == required
    assert graph.status == GraphStatus.OK
    assert graph.nodes
    assert graph.frontier_nodes
    assert graph.recommended_next_reads
    assert "Recommended next reads" in markdown
    assert "next-read-1" in to_pretty_json(output)

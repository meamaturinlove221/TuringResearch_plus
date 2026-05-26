from __future__ import annotations

from pathlib import Path

from turing_research_plus.vault_graph.backlink_index import build_backlink_index
from turing_research_plus.vault_graph.dangling_link_report import (
    build_dangling_link_report,
)
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.edge_quality import evaluate_edge_quality
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.wiki_export import build_wiki_vault_export

ROOT = Path(__file__).resolve().parents[2]


def test_yogsoth_vault_parity_fake_workflow_is_review_only() -> None:
    graph = VaultGraph(
        graph_id="yogsoth-vault-parity-fake",
        nodes=[
            build_concept_node("north-star", "North Star", source_refs=["demo"]),
            build_concept_node("hypothesis", "Hypothesis", source_refs=["demo"]),
            build_concept_node("artifact", "Artifact Audit", confidence=0.4),
        ],
        edges=[
            build_edge("north-star", "hypothesis", VaultGraphEdgeType.MAPS_TO),
            build_edge("hypothesis", "artifact", VaultGraphEdgeType.SUPPORTS),
            build_edge("artifact", "missing-result", VaultGraphEdgeType.RELATED_TO),
        ],
    )

    backlinks = build_backlink_index(graph)
    dangling = build_dangling_link_report(graph)
    edge_quality = evaluate_edge_quality(graph)
    wiki_export = build_wiki_vault_export(graph)

    assert backlinks.by_node_id()["hypothesis"].backlinks == ["north-star"]
    assert dangling.release_blocker is True
    assert "hypothesis->artifact:supports" in edge_quality.missing_edges
    assert "Artifact Audit" in wiki_export.pages
    assert wiki_export.requires_human_review is True


def test_yogsoth_vault_parity_docs_and_contract_exist() -> None:
    expected_paths = [
        ROOT / "contracts" / "yogsoth_vault_parity.yaml",
        ROOT / "docs" / "yogsoth-vault-parity.md",
        ROOT / "docs" / "wiki-vault-export.md",
        ROOT / "docs" / "vault-edge-audit.md",
    ]

    for path in expected_paths:
        assert path.exists(), path

    contract = (ROOT / "contracts" / "yogsoth_vault_parity.yaml").read_text(
        encoding="utf-8"
    )
    assert "graph_database: false" in contract
    assert "review_only: true" in contract

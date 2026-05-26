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
DEMO = ROOT / "examples" / "vault_wiki_demo"


def _demo_graph() -> VaultGraph:
    return VaultGraph(
        graph_id="vault-wiki-demo",
        nodes=[
            build_concept_node(
                "north-star",
                "North Star",
                source_refs=["fake-demo"],
                confidence=0.85,
            ),
            build_concept_node(
                "hypothesis",
                "Hypothesis",
                source_refs=["fake-demo"],
                confidence=0.7,
            ),
            build_concept_node("artifact", "Artifact Audit", confidence=0.4),
        ],
        edges=[
            build_edge(
                "north-star",
                "hypothesis",
                VaultGraphEdgeType.MAPS_TO,
                source_refs=["fake-demo"],
                confidence=0.8,
            ),
            build_edge("hypothesis", "artifact", VaultGraphEdgeType.SUPPORTS),
            build_edge(
                "artifact",
                "missing-result",
                VaultGraphEdgeType.RELATED_TO,
                confidence=0.3,
            ),
        ],
    )


def test_vault_wiki_export_demo_files_exist() -> None:
    expected = [
        DEMO / "README.md",
        DEMO / "wiki" / "North Star.md",
        DEMO / "wiki" / "Hypothesis.md",
        DEMO / "wiki" / "Artifact Audit.md",
        DEMO / "edge_audit_report.md",
        ROOT / "docs" / "vault-wiki-export-demo.md",
    ]

    for path in expected:
        assert path.exists(), path


def test_vault_wiki_export_demo_matches_runtime_reports() -> None:
    graph = _demo_graph()
    export = build_wiki_vault_export(graph)
    backlinks = build_backlink_index(graph)
    dangling = build_dangling_link_report(graph)
    quality = evaluate_edge_quality(graph)

    assert "North Star" in export.pages
    assert "Hypothesis" in export.pages
    assert "Artifact Audit" in export.pages
    assert backlinks.by_node_id()["hypothesis"].backlinks == ["north-star"]
    assert backlinks.by_node_id()["artifact"].outgoing_links == ["missing-result"]
    assert dangling.release_blocker is True
    assert dangling.dangling_links[0].target_id == "missing-result"
    assert "hypothesis->artifact:supports" in quality.missing_edges
    assert "artifact->missing-result:related_to" in quality.weak_edges
    assert quality.requires_review_nodes == ["north-star", "hypothesis", "artifact"]


def test_vault_wiki_export_demo_markdown_covers_audit_terms() -> None:
    combined = "\n".join(
        [
            (DEMO / "README.md").read_text(encoding="utf-8"),
            (DEMO / "edge_audit_report.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "vault-wiki-export-demo.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    required = [
        "wikilink",
        "backlink",
        "dangling",
        "missing evidence-bearing edge",
        "weak edge",
        "requires-review",
        "graph summary",
        "[[North Star]]",
        "[[Hypothesis]]",
        "[[Artifact Audit]]",
    ]
    for term in required:
        assert term in combined


def test_vault_wiki_export_demo_is_public_safe() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            DEMO / "README.md",
            DEMO / "wiki" / "North Star.md",
            DEMO / "wiki" / "Hypothesis.md",
            DEMO / "wiki" / "Artifact Audit.md",
            DEMO / "edge_audit_report.md",
            ROOT / "docs" / "vault-wiki-export-demo.md",
        ]
    )

    assert "fake/demo only" in combined
    assert "no graph database" in combined
    assert "no private data" in combined
    assert "no Evidence Ledger mutation" in combined

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined

from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.vault_graph.backlink_index import (
    build_backlink_index,
    render_backlink_index,
)
from turing_research_plus.vault_graph.dangling_link_report import (
    build_dangling_link_report,
    render_dangling_link_report,
)
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.edge_quality import (
    evaluate_edge_quality,
    render_edge_quality_report,
)
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.wiki_export import (
    build_wiki_vault_export,
    render_wiki_vault_export,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "vault_wiki_demo" / "e2e"
NOTES = DEMO / "notes"
GENERATED = DEMO / "generated"

WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


def _slug(label: str) -> str:
    return label.strip().lower().replace("/", "-").replace(" ", "-")


def _note_titles() -> dict[str, str]:
    return {_slug(path.stem): path.stem for path in sorted(NOTES.glob("*.md"))}


def _edge_config(
    source_id: str,
    target_id: str,
) -> tuple[VaultGraphEdgeType, list[str], float]:
    if source_id == "claim-review" and target_id == "artifact-audit":
        return VaultGraphEdgeType.SUPPORTS, [], 0.65
    if source_id == "artifact-audit" and target_id == "missing-evidence":
        return VaultGraphEdgeType.SUPPORTS, [], 0.3
    if source_id == "research-catalog":
        return VaultGraphEdgeType.MAPS_TO, ["fake-demo-note"], 0.82
    if source_id == "experiment-runbook":
        return VaultGraphEdgeType.REQUIRES, ["fake-demo-note"], 0.7
    return VaultGraphEdgeType.RELATED_TO, ["fake-demo-note"], 0.75


def _graph_from_markdown_notes() -> VaultGraph:
    titles = _note_titles()
    nodes = [
        build_concept_node(
            node_id,
            title,
            source_refs=["fake-demo-note"],
            confidence=0.44 if node_id == "artifact-audit" else 0.78,
        )
        for node_id, title in sorted(titles.items())
    ]
    edges = []
    for path in sorted(NOTES.glob("*.md")):
        source_id = _slug(path.stem)
        text = path.read_text(encoding="utf-8")
        for link_label in WIKILINK_PATTERN.findall(text):
            target_id = _slug(link_label)
            edge_type, source_refs, confidence = _edge_config(source_id, target_id)
            edges.append(
                build_edge(
                    source_id,
                    target_id,
                    edge_type,
                    source_refs=source_refs,
                    confidence=confidence,
                )
            )
    return VaultGraph(graph_id="vault-wiki-e2e", nodes=nodes, edges=edges)


def test_vault_wiki_e2e_demo_files_exist() -> None:
    expected = [
        DEMO / "README.md",
        NOTES / "Research Catalog.md",
        NOTES / "Stress Test.md",
        NOTES / "Experiment Runbook.md",
        NOTES / "Claim Review.md",
        NOTES / "Artifact Audit.md",
        GENERATED / "backlink_index.md",
        GENERATED / "dangling_link_report.md",
        GENERATED / "edge_audit_report.md",
        GENERATED / "wiki_export_index.md",
        ROOT / "docs" / "vault-wiki-e2e.md",
    ]

    for path in expected:
        assert path.exists(), path


def test_vault_wiki_e2e_parses_markdown_wikilinks_into_graph() -> None:
    graph = _graph_from_markdown_notes()

    assert graph.graph_id == "vault-wiki-e2e"
    assert len(graph.nodes) == 5
    assert len(graph.edges) == 6
    assert {node.label for node in graph.nodes} == {
        "Artifact Audit",
        "Claim Review",
        "Experiment Runbook",
        "Research Catalog",
        "Stress Test",
    }
    assert any(
        edge.source_id == "artifact-audit" and edge.target_id == "missing-evidence"
        for edge in graph.edges
    )


def test_vault_wiki_e2e_builds_backlinks_edge_audit_and_export() -> None:
    graph = _graph_from_markdown_notes()
    backlinks = build_backlink_index(graph)
    dangling = build_dangling_link_report(graph)
    quality = evaluate_edge_quality(graph)
    export = build_wiki_vault_export(graph)

    entries = backlinks.by_node_id()
    assert entries["stress-test"].backlinks == ["research-catalog"]
    assert entries["artifact-audit"].backlinks == [
        "claim-review",
        "experiment-runbook",
    ]
    assert entries["artifact-audit"].outgoing_links == ["missing-evidence"]
    assert backlinks.dangling_targets == ["missing-evidence"]

    assert dangling.release_blocker is True
    assert dangling.dangling_links[0].target_id == "missing-evidence"

    assert quality.release_blocker is True
    assert "claim-review->artifact-audit:supports" in quality.missing_edges
    assert "artifact-audit->missing-evidence:supports" in quality.missing_edges
    assert "artifact-audit->missing-evidence:supports" in quality.weak_edges
    assert quality.graph_summary["nodes"] == 5
    assert quality.graph_summary["edges"] == 6

    assert set(export.pages) == {
        "Artifact Audit",
        "Claim Review",
        "Experiment Runbook",
        "Research Catalog",
        "Stress Test",
    }
    assert "[[Stress Test]]" in export.pages["Research Catalog"]
    assert "[[Experiment Runbook]]" in export.pages["Artifact Audit"]
    assert export.requires_human_review is True


def test_vault_wiki_e2e_static_reports_match_runtime_surfaces() -> None:
    graph = _graph_from_markdown_notes()
    runtime_reports = "\n".join(
        [
            render_backlink_index(build_backlink_index(graph)),
            render_dangling_link_report(build_dangling_link_report(graph)),
            render_edge_quality_report(evaluate_edge_quality(graph)),
            render_wiki_vault_export(build_wiki_vault_export(graph)),
        ]
    )
    static_reports = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(GENERATED.glob("*.md"))
    )

    required = [
        "`research-catalog`",
        "`artifact-audit`",
        "`missing-evidence`",
        "`claim-review->artifact-audit:supports`",
        "`artifact-audit->missing-evidence:supports`",
        "[[Research Catalog]]",
        "[[Stress Test]]",
        "Pages: `5`",
    ]
    for item in required:
        assert item in runtime_reports
        assert item in static_reports


def test_vault_wiki_e2e_docs_preserve_safety_boundaries() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            DEMO / "README.md",
            ROOT / "docs" / "vault-wiki-e2e.md",
            GENERATED / "edge_audit_report.md",
        ]
    )

    required = [
        "fake/demo only",
        "no graph database",
        "no private data",
        "no default network",
        "no Evidence Ledger mutation",
        "no automatic truth inference",
        "human review required",
    ]
    for item in required:
        assert item in combined

    assert ("Tuling" + "Research") not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert ('"status": "' + 'observed"') not in combined

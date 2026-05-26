from __future__ import annotations

from turing_research_plus.vault_graph.alias_resolver import (
    normalize_alias,
    render_alias_resolution_report,
    resolve_aliases,
)
from turing_research_plus.vault_graph.models import VaultGraph
from turing_research_plus.vault_graph.node_builder import build_concept_node


def test_alias_resolver_matches_declared_aliases_and_reports_unresolved() -> None:
    graph = VaultGraph(
        graph_id="alias-demo",
        nodes=[
            build_concept_node(
                "human-prior",
                "Human Prior",
                aliases=["human prior model", "HP"],
                source_refs=["demo"],
            )
        ],
    )

    report = resolve_aliases(graph, ["human-prior model", "unknown"])

    assert normalize_alias("Human/Prior Model") == "humanpriormodel"
    assert report.by_alias()["human-prior model"].canonical_node_id == "human-prior"
    assert report.unresolved_aliases == ["unknown"]
    assert report.requires_human_review is True

    markdown = render_alias_resolution_report(report)
    assert "`human-prior model` -> `human-prior`" in markdown
    assert "`unknown`" in markdown


def test_alias_resolver_reports_duplicate_aliases() -> None:
    graph = VaultGraph(
        graph_id="duplicate-alias-demo",
        nodes=[
            build_concept_node("a", "Concept A", aliases=["shared"]),
            build_concept_node("b", "Concept B", aliases=["shared"]),
        ],
    )

    report = resolve_aliases(graph, ["shared"])

    assert report.candidates == []
    assert report.duplicate_aliases == ["shared"]

from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType
from turing_research_plus.related_work.models import RelatedWorkPositioningInput
from turing_research_plus.related_work.positioning import build_related_work_positioning
from turing_research_plus.skills.router import route_skill
from turing_research_plus.vault_graph.edge_audit import audit_vault_graph
from turing_research_plus.vault_graph.models import (
    VaultGraph,
    VaultGraphEdge,
    VaultGraphEdgeType,
    VaultGraphNode,
    VaultGraphNodeType,
)
from turing_research_plus.vault_graph.wikilink_export import export_wikilink_summary
from turing_research_plus.web.content_cache import WebContentCache
from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import SourceType, WebFetchRequest

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_ROOT = ROOT / "examples" / "vggt-human-prior-survey"
PACK_ROOT = EXAMPLE_ROOT / "research_knowledge_pack"


def test_v0_3_sprint2_web_to_related_work_fake_flow() -> None:
    cache = WebContentCache()
    fetcher = WebFetcher(cache=cache)
    fixture_path = EXAMPLE_ROOT / "web_fetch_fixtures" / "neuralbody_project_page.fixture.html"
    result = fetcher.fetch(
        WebFetchRequest(
            url="https://example.org/neuralbody",
            source_type=SourceType.PROJECT_PAGE,
            fixture_path=fixture_path,
        )
    )

    assert result.source_metadata.human_verified is False
    assert result.requires_human_review is True
    assert cache.cache_status("https://example.org/neuralbody") == "hit"

    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody fixture",
            source_type=PaperSourceType.HTML_SUMMARY,
            source_text=result.text_content or "",
            requires_real_paper_review=True,
        )
    )
    report = build_related_work_positioning(
        RelatedWorkPositioningInput(
            method_cards=[card.model_dump(mode="json")],
            citation_graph={"retrieval_status": "fake"},
            collision_report={
                "risk_scores": [
                    {"paper_id": "hart", "title": "HART requires-real-paper-review"}
                ]
            },
            web_summaries=[result.model_dump(mode="json")],
        )
    )

    assert report.requires_human_review is True
    assert report.safe_claims
    assert any("SparseConv3D" in claim.text for claim in report.unsafe_claims)
    assert any("HART" in item.item for item in report.missing_evidence)


def test_v0_3_sprint2_skill_routing_and_entry_consistency() -> None:
    decision = route_skill("fetch project page and position related work for VGGT")
    entry = (ROOT / ".agents" / "ENTRY.md").read_text(encoding="utf-8")

    assert decision.ranked_skills
    assert decision.recommended_skill.startswith("turingresearch-")
    assert "turingresearch-master-orchestrator" in entry
    assert "turingresearch-" in entry
    assert decision.does_not_execute is True


def test_v0_3_sprint2_vault_graph_to_wikilink_flow() -> None:
    graph = VaultGraph(
        graph_id="v0_3_sprint2_fake",
        nodes=[
            VaultGraphNode(
                node_id="vggt",
                label="VGGT",
                node_type=VaultGraphNodeType.CONCEPT,
                confidence=0.8,
            ),
            VaultGraphNode(
                node_id="smplx",
                label="SMPL-X",
                node_type=VaultGraphNodeType.CONCEPT,
                confidence=0.8,
            ),
            VaultGraphNode(
                node_id="sparseconv",
                label="SparseConv3D",
                node_type=VaultGraphNodeType.METHOD,
                confidence=0.4,
            ),
        ],
        edges=[
            VaultGraphEdge(
                source_id="smplx",
                target_id="vggt",
                edge_type=VaultGraphEdgeType.MAPS_TO,
                source_refs=["research_knowledge_pack/current_state.md"],
            ),
            VaultGraphEdge(
                source_id="sparseconv",
                target_id="vggt",
                edge_type=VaultGraphEdgeType.SUPPORTS,
            ),
        ],
    )

    audit = audit_vault_graph(graph)
    wikilinks = export_wikilink_summary(graph)

    assert audit.checked_nodes == 3
    assert audit.missing_edges
    assert "sparseconv" in audit.low_confidence_nodes
    assert "[[VGGT]]" in wikilinks
    assert "[[SparseConv3D]]" in wikilinks


def test_v0_3_sprint2_knowledge_pack_flow_is_conservative() -> None:
    manifest = (PACK_ROOT / "manifest.yaml").read_text(encoding="utf-8")
    current_state = (PACK_ROOT / "current_state.md").read_text(encoding="utf-8")
    related_work = (PACK_ROOT / "related_work_positioning.md").read_text(encoding="utf-8")
    vault_graph = (PACK_ROOT / "vault_graph.md").read_text(encoding="utf-8")

    assert "no_sparseconv3d_success_claim" in manifest
    assert "| V260 | hard-blocked |" in current_state
    assert "| V999-SparseConv3D | not-enough-evidence |" in current_state
    assert "requires-real-paper-review" in related_work
    assert "requires human review" in vault_graph.lower()

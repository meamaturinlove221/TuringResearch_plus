from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.adapters.fake import FakeSemanticScholarAdapter
from turing_research_plus.adapters.models import SemanticScholarPaperListLookup
from turing_research_plus.collision.models import PaperComparisonInput
from turing_research_plus.collision.tools import collision_risk_detect
from turing_research_plus.related_work.markdown_export import (
    export_related_work_positioning_markdown,
)
from turing_research_plus.related_work.models import RelatedWorkPositioningInput
from turing_research_plus.related_work.positioning import build_related_work_positioning
from turing_research_plus.scholar_tools import (
    PaperReferenceToolRequest,
    run_paper_reference_tool,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "scholar_demo" / "paper_reference_e2e"


def test_paper_reference_e2e_to_related_work_and_collision_inputs() -> None:
    metadata = json.loads((DEMO / "paper_metadata.json").read_text("utf-8"))

    references = run_paper_reference_tool(
        PaperReferenceToolRequest(paper_id=metadata["paper_id"], limit=3)
    )
    citations = FakeSemanticScholarAdapter().citations(
        SemanticScholarPaperListLookup(paper_id=metadata["paper_id"], limit=2)
    )

    assert references.tool_name == "scholar.paper_reference"
    assert references.source == "semantic_scholar"
    assert len(references.references) == 3
    assert references.live_enabled is False
    assert references.paywall_bypass_allowed is False
    assert references.automatic_full_paper_download is False
    assert references.requires_human_review is True
    assert references.release_blocker is False
    assert len(citations.papers) == 2

    related_seed = json.loads((DEMO / "related_work_seed.json").read_text("utf-8"))
    assert [item["title"] for item in related_seed["references"]] == [
        item["title"] for item in references.references
    ]
    assert [item["title"] for item in related_seed["citations"]] == [
        str(item["title"]) for item in citations.papers
    ]
    assert all(item["verified"] is False for item in related_seed["references"])
    assert all(item["verified"] is False for item in related_seed["citations"])

    collision_input = json.loads((DEMO / "collision_matrix_input.json").read_text("utf-8"))
    collision = collision_risk_detect(
        PaperComparisonInput(
            target_project=collision_input["target_project"],
            compared_papers=collision_input["compared_papers"],
            source_status=collision_input["source_status"],
        )
    )
    related = build_related_work_positioning(
        RelatedWorkPositioningInput(
            project_topic=metadata["title"],
            collision_report=collision.model_dump(mode="json"),
            manual_notes=[
                "Fake references and citations are related-work seeds only.",
            ],
        )
    )
    related_markdown = export_related_work_positioning_markdown(related)

    assert collision.requires_human_review is True
    assert collision.overlap_matrix.rows
    assert collision.missing_evidence
    assert related.requires_human_review is True
    assert related.paper_groups
    assert related.unsafe_claims
    assert "# Related Work Positioning Report" in related_markdown


def test_paper_reference_e2e_docs_keep_public_safety_boundary() -> None:
    combined = "\n".join(
        [
            (ROOT / "docs" / "paper-reference-e2e.md").read_text("utf-8"),
            (DEMO / "README.md").read_text("utf-8"),
            (DEMO / "reference_e2e_report.md").read_text("utf-8"),
        ]
    )

    for required in [
        "fake/default",
        "no API key required",
        "no automatic full paper download",
        "no paywall bypass",
        "no fake citation is marked as verified",
        "human review required",
    ]:
        assert required in combined

    for forbidden in [
        "D:/vggt",
        "D:\\vggt",
        "local_project_links.yaml",
        "ghp_",
        "sk-",
    ]:
        assert forbidden not in combined

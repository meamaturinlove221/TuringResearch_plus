from __future__ import annotations

from turing_research_plus.paper_digest.digest_builder import build_paper_digest
from turing_research_plus.paper_digest.models import (
    PaperDigestInput,
    PaperDigestSourceStatus,
)


def test_digest_builder_extracts_fixture_sections() -> None:
    digest = build_paper_digest(
        PaperDigestInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            source_text="""
# NeuralBody Fixture
core method: body-prior sparse voxel rendering scaffold.

## Key Figures

- figure 1 architecture

## What To Borrow

- sparse voxel comparison vocabulary

## What Not To Copy

- paper text
""",
        )
    )

    assert digest.paper_id == "neuralbody-fixture"
    assert digest.source_status == PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE
    assert digest.figures_to_inspect == ["figure 1 architecture"]
    assert digest.what_to_borrow == ["sparse voxel comparison vocabulary"]
    assert any("Sparse or voxel" in note for note in digest.collision_notes)
    assert digest.requires_human_review is True
    assert digest.requires_real_paper is True

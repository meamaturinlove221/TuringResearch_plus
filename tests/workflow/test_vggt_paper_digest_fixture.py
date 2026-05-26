from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_digest.digest_builder import build_paper_digest
from turing_research_plus.paper_digest.markdown_export import export_paper_digest_markdown
from turing_research_plus.paper_digest.method_bridge import digest_to_method_card
from turing_research_plus.paper_digest.models import (
    PaperDigestInput,
    PaperDigestSourceStatus,
)

ROOT = Path(__file__).resolve().parents[2]
METHOD_FIXTURES = ROOT / "examples" / "vggt-human-prior-survey" / "paper_method_cards"
DIGEST_FIXTURES = ROOT / "examples" / "vggt-human-prior-survey" / "paper_digest"


def test_neuralbody_digest_fixture_is_not_complete_review() -> None:
    text = (METHOD_FIXTURES / "neuralbody.fixture.md").read_text(encoding="utf-8")
    digest = build_paper_digest(
        PaperDigestInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            source_text=text,
        )
    )
    markdown = export_paper_digest_markdown(digest)

    assert digest.requires_real_paper is True
    assert "not a complete paper review" in markdown
    assert "No citation is fabricated" in markdown
    assert "Use as body-prior / sparse-voxel" in markdown


def test_humanram_digest_fixture_bridges_to_method_card() -> None:
    text = (METHOD_FIXTURES / "humanram.fixture.md").read_text(encoding="utf-8")
    digest = build_paper_digest(
        PaperDigestInput(
            paper_id="humanram-fixture",
            title="HumanRAM Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            source_text=text,
        )
    )
    card = digest_to_method_card(digest)

    assert card.requires_human_review is True
    assert "tri-plane" in "\n".join(digest.collision_notes).lower()
    assert card.mapping_to_vggt.smpl_role.startswith("SMPL")


def test_committed_digest_examples_keep_boundaries() -> None:
    neuralbody = (DIGEST_FIXTURES / "neuralbody_digest.fixture.md").read_text(
        encoding="utf-8"
    )
    humanram = (DIGEST_FIXTURES / "humanram_digest.fixture.md").read_text(
        encoding="utf-8"
    )

    assert "fake-or-manual-note" in neuralbody
    assert "requires real paper" in neuralbody.lower()
    assert "complete paper review" in neuralbody
    assert "fake-or-manual-note" in humanram
    assert "No citation is fabricated" in humanram
    assert "fully read" not in neuralbody
    assert "fully read" not in humanram

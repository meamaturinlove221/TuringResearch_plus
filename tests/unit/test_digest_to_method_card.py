from __future__ import annotations

from turing_research_plus.paper_digest.digest_builder import build_paper_digest
from turing_research_plus.paper_digest.method_bridge import digest_to_method_card
from turing_research_plus.paper_digest.models import (
    PaperDigestInput,
    PaperDigestSourceStatus,
)
from turing_research_plus.paper_method.models import PaperSourceType


def test_digest_converts_to_review_required_method_card() -> None:
    digest = build_paper_digest(
        PaperDigestInput(
            paper_id="humanram-fixture",
            title="HumanRAM Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            source_text="# HumanRAM\nSMPL-X tri-plane token geometry scaffold.",
        )
    )

    card = digest_to_method_card(digest)

    assert card.paper_id == "humanram-fixture"
    assert card.source_type == PaperSourceType.FAKE_OR_MANUAL_NOTE
    assert card.requires_human_review is True
    assert "Fixture is fake-or-manual-note" in "\n".join(card.limitations)

from __future__ import annotations

from turing_research_plus.related_work.claim_safety import (
    build_missing_evidence,
    build_safe_claims,
    build_unsafe_claims,
)
from turing_research_plus.related_work.models import PaperGroup, PaperGroupEntry


def test_claim_safety_keeps_sparseconv_success_unsafe() -> None:
    unsafe = build_unsafe_claims()

    assert any("SparseConv3D integration has succeeded" in claim.text for claim in unsafe)
    assert all(claim.requires_human_review for claim in unsafe)


def test_safe_claims_and_missing_evidence_are_conservative() -> None:
    groups = [
        PaperGroupEntry(
            paper_id="humanram",
            title="HumanRAM",
            group=PaperGroup.HUMANRAM_TRIPLANE_RASTER,
            rationale="fixture",
        )
    ]

    safe = build_safe_claims(groups)
    missing = build_missing_evidence(groups)

    assert any("HumanRAM" in claim.text for claim in safe)
    assert any("EvidenceRef" in item.item for item in missing)

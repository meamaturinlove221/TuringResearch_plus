from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.evidence_linker import (
    build_vggt_evidence_requirements,
    missing_evidence_report,
)

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_PACK = (
    ROOT / "examples" / "vggt-human-prior-survey" / "research_knowledge_pack"
)


def test_build_vggt_evidence_requirements_lists_required_review_items() -> None:
    requirements = build_vggt_evidence_requirements(KNOWLEDGE_PACK)
    ids = {item.requirement_id for item in requirements}

    assert ids == {
        "exp-real-sparse-backend",
        "visual-board-inventory",
        "related-work-paper-review",
    }
    assert all(item.required_before_claim for item in requirements)
    assert any(item.status == "requires-human-review" for item in requirements)


def test_missing_evidence_report_keeps_missing_and_review_status() -> None:
    requirements = build_vggt_evidence_requirements(KNOWLEDGE_PACK)

    report = "\n".join(missing_evidence_report(requirements))

    assert "`exp-real-sparse-backend`" in report
    assert "[missing]" in report
    assert "`related-work-paper-review`" in report
    assert "[requires-human-review]" in report

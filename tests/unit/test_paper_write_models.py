from __future__ import annotations

import pytest

from turing_research_plus.paper_write.models import (
    EvidenceRequirement,
    PaperScaffold,
    PaperSectionPlan,
    PaperSectionStatus,
)


def _section(section_id: str, status: PaperSectionStatus) -> PaperSectionPlan:
    return PaperSectionPlan(
        section_id=section_id,
        title=section_id.replace("_", " ").title(),
        status=status,
        bullets=["Plan-only placeholder."],
    )


def _scaffold(**overrides: object) -> PaperScaffold:
    payload: dict[str, object] = {
        "scaffold_id": "paper-scaffold-test",
        "topic": "Demo Research Topic",
        "title_candidates": ["Evidence-gated Research Paper"],
        "abstract_status": PaperSectionStatus.NEEDS_EVIDENCE,
        "introduction_plan": _section(
            "introduction", PaperSectionStatus.NEEDS_HUMAN_REVIEW
        ),
        "related_work_plan": _section(
            "related_work", PaperSectionStatus.NEEDS_EVIDENCE
        ),
        "method_plan": _section("method", PaperSectionStatus.OUTLINE_ONLY),
        "experiment_plan": _section("experiments", PaperSectionStatus.NEEDS_EVIDENCE),
        "results_status": PaperSectionStatus.NEEDS_EVIDENCE,
        "limitation_plan": _section(
            "limitations", PaperSectionStatus.NEEDS_HUMAN_REVIEW
        ),
        "evidence_requirements": [
            EvidenceRequirement(
                requirement_id="req-1",
                section="experiments",
                description="Real experiment evidence.",
                status="missing",
            )
        ],
        "missing_experiments": ["Run the real experiment before writing results."],
        "unsafe_claims": ["Do not claim success without evidence."],
        "requires_human_review": True,
    }
    payload.update(overrides)
    return PaperScaffold(**payload)


def test_paper_scaffold_serializes_required_boundary_fields() -> None:
    scaffold = _scaffold()

    payload = scaffold.model_dump(mode="json")

    assert payload["title_candidates"] == ["Evidence-gated Research Paper"]
    assert payload["generated_final_abstract"] is False
    assert payload["generated_final_results"] is False
    assert payload["requires_human_review"] is True
    assert payload["results_status"] == "needs-evidence"


def test_paper_scaffold_rejects_final_abstract_generation() -> None:
    with pytest.raises(ValueError, match="final abstract"):
        _scaffold(generated_final_abstract=True)


def test_paper_scaffold_rejects_final_results_generation() -> None:
    with pytest.raises(ValueError, match="final results"):
        _scaffold(generated_final_results=True)


def test_paper_scaffold_rejects_results_ready_without_evidence() -> None:
    with pytest.raises(ValueError, match="results cannot be ready"):
        _scaffold(results_status=PaperSectionStatus.READY_FOR_DRAFTING)


def test_paper_scaffold_requires_missing_experiments() -> None:
    with pytest.raises(ValueError, match="missing experiments"):
        _scaffold(missing_experiments=[])

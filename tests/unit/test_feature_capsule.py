from pathlib import Path

import pytest

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.race.feature_capsule import (
    FeatureCapsuleRequest,
    create_feature_capsule,
    race_feature_capsule_create,
)
from turing_research_plus.race.models import IdeaCard, SourceHygieneGate, SourceHygieneStatus


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="public-src",
        locator="README",
        quote="Public source describes a useful feature.",
    )


def gate(status: SourceHygieneStatus = SourceHygieneStatus.PASSED) -> SourceHygieneGate:
    if status == SourceHygieneStatus.PASSED:
        return SourceHygieneGate(status=status, checked_sources=[evidence()])
    return SourceHygieneGate(
        status=status,
        checked_sources=[evidence()],
        blocked_reason="Source hygiene blocked.",
    )


def idea(status: SourceHygieneStatus = SourceHygieneStatus.PASSED) -> IdeaCard:
    return IdeaCard(
        idea_id="idea-1",
        title="Priority Capsule",
        raw_text="Urgent public feature idea.",
        normalized_summary="Urgent public feature idea.",
        inferred_intent="Create a capsule skeleton.",
        source="public-src",
        value_score=0.78,
        feasibility_score=0.74,
        urgency_score=0.75,
        novelty_score=0.7,
        evidence_refs=[evidence()],
        hygiene_gate=gate(status),
    )


def test_feature_capsule_factory_writes_required_skeleton_files(tmp_path: Path) -> None:
    result = create_feature_capsule(
        FeatureCapsuleRequest(
            idea=idea(),
            feature_name="priority_capsule",
            workspace_root=tmp_path,
            strategic_fit=0.7,
        )
    )

    expected = [
        tmp_path / "race" / "feature_capsules" / "priority_capsule" / "FEATURE.md",
        tmp_path / "race" / "feature_capsules" / "priority_capsule" / "contract.yaml",
        tmp_path / "race" / "feature_capsules" / "priority_capsule" / "SKILL.md",
        tmp_path / "src" / "turing_research_plus" / "race" / "priority_capsule.py",
        tmp_path / "tests" / "unit" / "test_priority_capsule.py",
        tmp_path / "docs" / "features" / "priority_capsule.md",
        tmp_path / "sop_graphs" / "feature_graphs" / "priority_capsule.mmd",
    ]

    assert result.skipped_reason is None
    assert result.capsule.idea_cards == ["idea-1"]
    assert all(path.exists() for path in expected)


def test_feature_md_contains_required_sections(tmp_path: Path) -> None:
    create_feature_capsule(
        FeatureCapsuleRequest(
            idea=idea(),
            feature_name="priority_capsule",
            workspace_root=tmp_path,
            strategic_fit=0.7,
        )
    )
    content = (
        tmp_path / "race" / "feature_capsules" / "priority_capsule" / "FEATURE.md"
    ).read_text()

    for heading in [
        "Problem",
        "User story",
        "Input",
        "Output",
        "Data model",
        "Public tools",
        "Internal service",
        "Risks",
        "Tests",
        "Done criteria",
    ]:
        assert f"## {heading}" in content
    assert "idea-1" in content


def test_feature_capsule_requires_passed_hygiene() -> None:
    with pytest.raises(ValueError):
        create_feature_capsule(
            FeatureCapsuleRequest(
                idea=idea(SourceHygieneStatus.BLOCKED),
                feature_name="blocked_capsule",
                write_files=False,
            )
        )


def test_feature_capsule_skips_non_p0_p1(tmp_path: Path) -> None:
    low_idea = idea().model_copy(
        update={
            "value_score": 0.3,
            "urgency_score": 0.2,
            "feasibility_score": 0.3,
            "novelty_score": 0.2,
        }
    )
    result = create_feature_capsule(
        FeatureCapsuleRequest(
            idea=low_idea,
            feature_name="low_capsule",
            workspace_root=tmp_path,
            strategic_fit=0.2,
        )
    )

    assert result.skipped_reason == "idea is not P0/P1"
    assert not (tmp_path / "race" / "feature_capsules" / "low_capsule").exists()


def test_race_feature_capsule_create_tool_returns_json_payload(tmp_path: Path) -> None:
    payload = race_feature_capsule_create(
        FeatureCapsuleRequest(
            idea=idea(),
            feature_name="priority_capsule",
            workspace_root=tmp_path,
            strategic_fit=0.7,
        )
    )

    assert payload["feature_name"] == "priority_capsule"
    assert payload["capsule"]["idea_cards"] == ["idea-1"]

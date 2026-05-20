from pathlib import Path

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.race.architecture_box import race_architecture_box_build
from tuling_research_plus.race.feature_capsule import FeatureCapsuleRequest, create_feature_capsule
from tuling_research_plus.race.idea_radar import IdeaRadarInput, race_idea_extract
from tuling_research_plus.race.models import IdeaCard, SourceHygieneGate, SourceHygieneStatus
from tuling_research_plus.race.priority_elevator import race_priority_score
from tuling_research_plus.race.source_hygiene import (
    SourceKind,
    SourceMaterial,
    race_source_hygiene_check,
)
from tuling_research_plus.race.upstream_watch import (
    UpstreamSnapshot,
    UpstreamWatchInput,
    race_upstream_watch,
)


def evidence(source_id: str = "public-src") -> EvidenceRef:
    return EvidenceRef(source_id=source_id, locator="README", quote="Public source.")


def source(kind: SourceKind = SourceKind.PUBLIC_README) -> SourceMaterial:
    return SourceMaterial(
        source_id="public-src",
        kind=kind,
        license="MIT",
        public=True,
        authorized=True,
        intended_use="concept",
        evidence=evidence(),
    )


def idea() -> IdeaCard:
    return IdeaCard(
        idea_id="idea-1",
        title="Feature Capsule",
        raw_text="Urgent new MCP local cache improvement should reduce regression.",
        normalized_summary="Urgent new MCP local cache improvement should reduce regression.",
        inferred_intent="Improve MCP-first workflow tooling.",
        source="public-src",
        value_score=0.9,
        feasibility_score=0.9,
        urgency_score=0.9,
        novelty_score=0.9,
        evidence_refs=[evidence()],
        hygiene_gate=SourceHygieneGate(
            status=SourceHygieneStatus.PASSED,
            checked_sources=[evidence()],
        ),
    )


def test_race_public_tools_contract_payloads(tmp_path: Path) -> None:
    hygiene = race_source_hygiene_check([source()])
    extracted = race_idea_extract(
        IdeaRadarInput(text="Urgent new MCP local cache improvement.", source=source())
    )
    priority = race_priority_score(idea())
    create_feature_capsule(
        FeatureCapsuleRequest(
            idea=idea(),
            feature_name="qa_feature",
            workspace_root=tmp_path,
            strategic_fit=0.9,
        )
    )
    architecture = race_architecture_box_build()
    upstream = race_upstream_watch(
        UpstreamWatchInput(
            source=source(SourceKind.PUBLIC_RELEASE_NOTES),
            current_snapshot=UpstreamSnapshot(
                snapshot_id="snapshot-1",
                project_name="Public Reference",
                version="1.0.0",
            ),
        )
    )

    assert hygiene["decision"] == "allow"
    assert extracted["ideas"][0]["idea_id"].startswith("idea-")
    assert priority["priority"] in {"P0", "P1", "P2", "P3"}
    assert (tmp_path / "race" / "feature_capsules" / "qa_feature" / "contract.yaml").exists()
    assert (tmp_path / "race" / "feature_capsules" / "qa_feature" / "SKILL.md").exists()
    assert (tmp_path / "tests" / "unit" / "test_qa_feature.py").exists()
    assert (tmp_path / "sop_graphs" / "feature_graphs" / "qa_feature.mmd").exists()
    assert len(architecture["boxes"]) == 16
    assert upstream["watch_items"]


def test_source_hygiene_blocks_non_public_implementation() -> None:
    private_source = SourceMaterial(
        source_id="private-src",
        kind=SourceKind.PRIVATE_REPO_CONTENT,
        license="proprietary",
        public=False,
        authorized=False,
        intended_use="copy code",
        evidence=evidence("private-src"),
    )

    result = race_source_hygiene_check([private_source])

    assert result["decision"] == "block"
    assert result["safe_implementation_mode"] == "documentation_only_watch"

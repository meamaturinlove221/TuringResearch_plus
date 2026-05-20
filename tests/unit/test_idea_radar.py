from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.race.idea_radar import IdeaRadarInput, extract_idea, race_idea_extract
from tuling_research_plus.race.models import IdeaPriority, RecommendedAction
from tuling_research_plus.race.source_hygiene import (
    SourceKind,
    SourceMaterial,
)


def evidence(source_id: str = "public-src") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="README",
        quote="Public README says the workflow can improve cache and ledger reliability.",
    )


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


def test_idea_extract_corrects_tts_terms_without_preserving_errors() -> None:
    result = extract_idea(
        IdeaRadarInput(
            text="We need m c p first support and cash plus letter reliability.",
            source=source(),
        )
    )
    idea = result.ideas[0]

    assert "MCP" in idea.normalized_summary
    assert "cache" in idea.normalized_summary
    assert "ledger" in idea.normalized_summary
    assert "cash" not in idea.normalized_summary.lower()


def test_uncertain_terms_make_speculative_document_action() -> None:
    result = extract_idea(
        IdeaRadarInput(
            text="Maybe a new local cache idea from some unknownish term.",
            source=source(),
        )
    )
    idea = result.ideas[0]

    assert idea.uncertain_terms
    assert "speculative" in idea.tags
    assert idea.recommended_action == RecommendedAction.DOCUMENT


def test_public_authorized_high_confidence_can_enter_implementation() -> None:
    result = extract_idea(
        IdeaRadarInput(
            text=(
                "Urgent new MCP local cache improvement should reduce regression "
                "and improve workflow reliability."
            ),
            source=source(),
        )
    )
    idea = result.ideas[0]

    assert idea.priority == IdeaPriority.HIGH
    assert idea.recommended_action == RecommendedAction.IMPLEMENT


def test_unknown_source_can_only_watch_or_document() -> None:
    unknown = SourceMaterial(
        source_id="unknown-src",
        kind=SourceKind.UNKNOWN,
        license=None,
        public=None,
        authorized=None,
        intended_use="concept",
        evidence=evidence("unknown-src"),
    )
    result = extract_idea(
        IdeaRadarInput(
            text="Urgent new MCP local cache improvement.",
            source=unknown,
        )
    )

    assert result.source_hygiene.decision == "watch"
    assert result.ideas[0].recommended_action == RecommendedAction.WATCH
    assert result.skipped_reason == "watch only"


def test_private_source_is_skipped() -> None:
    private = SourceMaterial(
        source_id="private-src",
        kind=SourceKind.PRIVATE_REPO_CONTENT,
        license="proprietary",
        public=False,
        authorized=False,
        intended_use="concept",
        evidence=evidence("private-src"),
    )
    result = extract_idea(IdeaRadarInput(text="Private roadmap idea.", source=private))

    assert result.ideas == []
    assert result.skipped_reason == "source hygiene blocked idea extraction"


def test_race_idea_extract_tool_returns_json_payload() -> None:
    payload = race_idea_extract(
        IdeaRadarInput(
            text="Urgent new MCP local cache improvement should reduce regression.",
            source=source(),
        )
    )

    assert payload["ideas"][0]["idea_id"].startswith("idea-")
    assert payload["ideas"][0]["evidence_refs"]


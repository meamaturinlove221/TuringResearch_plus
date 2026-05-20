from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.budget.models import BudgetGate, BudgetLimit, BudgetUnit
from tuling_research_plus.campaign.models import (
    CampaignMode,
    CampaignSpec,
    QualityGateSpec,
    SOPExecutionMode,
    SOPSpec,
    StrategySpec,
    TacticSpec,
)
from tuling_research_plus.ledger.models import StateLedger
from tuling_research_plus.race.models import FeatureCapsule, SourceHygieneGate, SourceHygieneStatus
from tuling_research_plus.sop.models import SOPGenerationRequest, SOPGraphType
from tuling_research_plus.sop.sop_graph import (
    generate_campaign_sop_graph,
    generate_feature_sop_graph,
    paper_sop_graph_generate,
    sop_graph_generate,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="source-1", locator="README", quote="Public evidence.")


def campaign() -> CampaignSpec:
    return CampaignSpec(
        campaign_id="campaign-1",
        title="Survey Campaign",
        mode=CampaignMode.DRY_RUN,
        budget_gate=BudgetGate(
            gate_id="budget-1",
            limits=[BudgetLimit(unit=BudgetUnit.REQUESTS, limit=10)],
        ),
        state_ledger=StateLedger(ledger_id="ledger-1", lane="lane-06"),
        inputs={"ResearchBrief": "brief-1"},
        strategies=[
            StrategySpec(
                strategy_id="strategy-1",
                title="Strategy",
                tactics=[
                    TacticSpec(
                        tactic_id="tactic-1",
                        title="Tactic",
                        sops=[
                            SOPSpec(
                                sop_id="sop-1",
                                title="Run survey",
                                execution_mode=SOPExecutionMode.DIRECT,
                                handler="research.survey_run",
                            )
                        ],
                    )
                ],
            )
        ],
        quality_gates=[QualityGateSpec(gate_id="evidence", description="EvidenceRef present")],
    )


def feature_capsule() -> FeatureCapsule:
    return FeatureCapsule(
        feature_id="feature-docflow",
        title="DocFlow Feature",
        idea_cards=["idea-1"],
        evidence=[evidence()],
        hygiene_gate=SourceHygieneGate(
            status=SourceHygieneStatus.PASSED,
            checked_sources=[evidence()],
        ),
    )


def test_campaign_graph_generated() -> None:
    graph = generate_campaign_sop_graph(campaign())

    assert graph.graph_type == SOPGraphType.CAMPAIGN
    assert "ResearchBrief" in graph.input_artifacts
    assert "research.survey_run" in graph.tools
    assert graph.quality_gates == ["EvidenceRef present"]


def test_feature_graph_generated() -> None:
    graph = generate_feature_sop_graph(feature_capsule())

    assert graph.graph_type == SOPGraphType.FEATURE
    assert "FeatureCapsule" in graph.output_artifacts
    assert "race.feature_capsule_create" in graph.tools


def test_graph_contains_quality_and_failure_gates() -> None:
    graph = generate_feature_sop_graph(feature_capsule())

    assert graph.quality_gates
    assert graph.failure_gates
    assert any(node.kind.value == "quality_gate" for node in graph.nodes)
    assert any(node.kind.value == "failure_gate" for node in graph.nodes)


def test_sop_graph_generate_renders_mermaid_and_optional_outputs() -> None:
    result = sop_graph_generate(
        SOPGenerationRequest(
            graph_type=SOPGraphType.RELEASE,
            source_id="release-1",
            title="Release SOP",
            input_artifacts=["contracts"],
            output_artifacts=["ReleaseChecklist"],
            tools=["python -m pytest"],
            quality_gates=["Tests pass"],
            failure_gates=["Test failure"],
            include_skill_skeleton=True,
            include_codex_prompt=True,
        )
    )

    assert result.mermaid_text.startswith("flowchart TD")
    assert result.sop_markdown.startswith("# TulingResearch Plus SOP: Release SOP")
    assert result.skill_skeleton is not None
    assert result.codex_prompt is not None


def test_paper_sop_graph_generate_tool_returns_json_payload() -> None:
    payload = paper_sop_graph_generate(
        SOPGenerationRequest(
            graph_type=SOPGraphType.PAPER,
            source_id="paper-1",
            title="Paper SOP",
            input_artifacts=["ArticleBlock"],
            output_artifacts=["PaperDraft"],
        )
    )

    assert payload["graph"]["graph_type"] == "paper"
    assert payload["mermaid_text"].startswith("flowchart TD")

"""SOP graph builders for TulingResearch Plus."""

from __future__ import annotations

from tuling_research_plus.campaign.models import CampaignSpec
from tuling_research_plus.experiment.models import ExperimentPlan
from tuling_research_plus.paper.models import ArticleBlock
from tuling_research_plus.race.models import FeatureCapsule
from tuling_research_plus.sop.mermaid_export import export_mermaid, export_sop_markdown
from tuling_research_plus.sop.models import (
    SOPEdge,
    SOPGenerationRequest,
    SOPGenerationResult,
    SOPGraph,
    SOPGraphType,
    SOPNode,
    SOPNodeKind,
)
from tuling_research_plus.sop.prompt_generator import generate_codex_prompt
from tuling_research_plus.sop.skill_skeleton import generate_skill_skeleton


def generate_campaign_sop_graph(campaign: CampaignSpec) -> SOPGraph:
    """Generate a campaign SOP graph from a CampaignSpec."""

    nodes = [
        SOPNode(node_id="campaign", label=campaign.title),
        SOPNode(node_id="budget_gate", label="BudgetGate", kind=SOPNodeKind.QUALITY_GATE),
        SOPNode(node_id="state_ledger", label="StateLedger", kind=SOPNodeKind.ARTIFACT),
    ]
    edges = [
        SOPEdge(source="campaign", target="budget_gate"),
        SOPEdge(source="budget_gate", target="state_ledger"),
    ]
    previous = "state_ledger"
    tools: list[str] = []
    for strategy in campaign.strategies:
        strategy_id = f"strategy_{strategy.strategy_id}"
        nodes.append(SOPNode(node_id=strategy_id, label=strategy.title))
        edges.append(SOPEdge(source=previous, target=strategy_id))
        previous = strategy_id
        for tactic in strategy.tactics:
            tactic_id = f"tactic_{tactic.tactic_id}"
            nodes.append(SOPNode(node_id=tactic_id, label=tactic.title))
            edges.append(SOPEdge(source=previous, target=tactic_id))
            previous = tactic_id
            for sop in tactic.sops:
                sop_id = f"sop_{sop.sop_id}"
                nodes.append(SOPNode(node_id=sop_id, label=sop.title, kind=SOPNodeKind.TOOL))
                edges.append(SOPEdge(source=previous, target=sop_id))
                previous = sop_id
                tools.append(sop.handler)
    nodes.append(
        SOPNode(
            node_id="failure_gate",
            label="Stop on blocker",
            kind=SOPNodeKind.FAILURE_GATE,
        )
    )
    edges.append(SOPEdge(source=previous, target="failure_gate"))
    return SOPGraph(
        graph_id=f"campaign-{campaign.campaign_id}",
        graph_type=SOPGraphType.CAMPAIGN,
        title=campaign.title,
        nodes=nodes,
        edges=edges,
        input_artifacts=list(campaign.inputs.keys()),
        output_artifacts=["ResearchArtifact", "CampaignResult"],
        tools=tools or ["campaign.runner"],
        quality_gates=(
            [gate.description for gate in campaign.quality_gates] or ["BudgetGate passes"]
        ),
        failure_gates=["BudgetGate blocked", "Quality gate failed", "StateLedger blocker"],
    )


def generate_feature_sop_graph(capsule: FeatureCapsule) -> SOPGraph:
    """Generate a feature SOP graph from a FeatureCapsule."""

    return SOPGraph(
        graph_id=f"feature-{capsule.feature_id}",
        graph_type=SOPGraphType.FEATURE,
        title=capsule.title,
        nodes=[
            SOPNode(node_id="idea", label="Source IdeaCard", kind=SOPNodeKind.ARTIFACT),
            SOPNode(node_id="hygiene", label="Source Hygiene Gate", kind=SOPNodeKind.QUALITY_GATE),
            SOPNode(node_id="capsule", label="Feature Capsule", kind=SOPNodeKind.ARTIFACT),
            SOPNode(node_id="contract", label="Contract Review"),
            SOPNode(node_id="tests", label="Unit Tests", kind=SOPNodeKind.QUALITY_GATE),
            SOPNode(
                node_id="blocked",
                label="Do not implement unsafe source",
                kind=SOPNodeKind.FAILURE_GATE,
            ),
        ],
        edges=[
            SOPEdge(source="idea", target="hygiene"),
            SOPEdge(source="hygiene", target="capsule", label="passed"),
            SOPEdge(source="hygiene", target="blocked", label="blocked"),
            SOPEdge(source="capsule", target="contract"),
            SOPEdge(source="contract", target="tests"),
        ],
        input_artifacts=["IdeaCard", "SourceHygieneGate"],
        output_artifacts=["FeatureCapsule", "contract.yaml", "SKILL.md"],
        tools=["race.feature_capsule_create"],
        quality_gates=["Source Hygiene Gate passed", "Feature capsule has tests"],
        failure_gates=["Source hygiene blocked", "Missing source evidence"],
    )


def generate_paper_sop_graph(blocks: list[ArticleBlock]) -> SOPGraph:
    """Generate a paper SOP graph from ArticleBlocks."""

    block_nodes = [
        SOPNode(
            node_id=_block_node_id(block),
            label=block.block_kind.value if block.block_kind else block.section.value,
            kind=SOPNodeKind.ARTIFACT,
        )
        for block in blocks
    ]
    nodes = [
        SOPNode(node_id="docflow", label="DocFlow Status", kind=SOPNodeKind.TOOL),
        *block_nodes,
        SOPNode(node_id="evidence_gate", label="EvidenceRef Gate", kind=SOPNodeKind.QUALITY_GATE),
        SOPNode(node_id="draft_gate", label="ExperimentReport Gate", kind=SOPNodeKind.FAILURE_GATE),
    ]
    edges = [SOPEdge(source="docflow", target=node.node_id) for node in block_nodes]
    if block_nodes:
        edges.append(SOPEdge(source=block_nodes[-1].node_id, target="evidence_gate"))
    edges.append(SOPEdge(source="evidence_gate", target="draft_gate"))
    return SOPGraph(
        graph_id="paper-docflow",
        graph_type=SOPGraphType.PAPER,
        title="Paper DocFlow",
        nodes=nodes,
        edges=edges,
        input_artifacts=["ResearchBrief", "LiteratureSurveyArtifact", "ExperimentReport"],
        output_artifacts=["ArticleBlock", "PaperDraft"],
        tools=["paper.docflow_status", "paper.article_block_update", "paper.missing_evidence"],
        quality_gates=["Every block has EvidenceRef", "Required figures available"],
        failure_gates=["ExperimentReport missing", "Missing evidence refs"],
    )


def generate_experiment_sop_graph(plan: ExperimentPlan) -> SOPGraph:
    """Generate an experiment SOP graph from an ExperimentPlan."""

    return SOPGraph(
        graph_id=f"experiment-{plan.plan_id}",
        graph_type=SOPGraphType.EXPERIMENT,
        title=f"Experiment SOP: {plan.plan_id}",
        nodes=[
            SOPNode(node_id="hypothesis", label="Hypothesis", kind=SOPNodeKind.ARTIFACT),
            SOPNode(node_id="variables", label="Variables and Controls"),
            SOPNode(node_id="metrics", label="Metrics and Baselines"),
            SOPNode(node_id="ablations", label="Ablations"),
            SOPNode(node_id="repro", label="Reproducibility Gate", kind=SOPNodeKind.QUALITY_GATE),
            SOPNode(node_id="failure", label="Reject weak plan", kind=SOPNodeKind.FAILURE_GATE),
        ],
        edges=[
            SOPEdge(source="hypothesis", target="variables"),
            SOPEdge(source="variables", target="metrics"),
            SOPEdge(source="metrics", target="ablations"),
            SOPEdge(source="ablations", target="repro"),
            SOPEdge(source="repro", target="failure", label="failed"),
        ],
        input_artifacts=["Hypothesis", "ExperimentPlan"],
        output_artifacts=["ExperimentReport", "ResultSchema"],
        tools=["research.experiment_design", "research.result_schema_generate"],
        quality_gates=[
            "Controls present",
            "Metrics present",
            "Ablations present",
            "Reproducibility checklist present",
        ],
        failure_gates=["Missing controls", "Missing metrics", "Missing ablations"],
    )


def generate_release_sop_graph(title: str = "Release SOP") -> SOPGraph:
    """Generate a release SOP graph."""

    return SOPGraph(
        graph_id="release-default",
        graph_type=SOPGraphType.RELEASE,
        title=title,
        nodes=[
            SOPNode(node_id="contracts", label="Contract Review", kind=SOPNodeKind.QUALITY_GATE),
            SOPNode(node_id="tests", label="Tests", kind=SOPNodeKind.QUALITY_GATE),
            SOPNode(node_id="docs", label="Docs"),
            SOPNode(node_id="ledger", label="Lane Ledger", kind=SOPNodeKind.ARTIFACT),
            SOPNode(node_id="stop", label="Stop Release", kind=SOPNodeKind.FAILURE_GATE),
        ],
        edges=[
            SOPEdge(source="contracts", target="tests"),
            SOPEdge(source="tests", target="docs"),
            SOPEdge(source="docs", target="ledger"),
            SOPEdge(source="tests", target="stop", label="failed"),
        ],
        input_artifacts=["contracts", "tests", "docs"],
        output_artifacts=["ReleaseChecklist", "LaneLedger"],
        tools=["python -m pytest", "python -m ruff check .", "python -m mypy src"],
        quality_gates=["Contracts updated", "Tests pass", "Docs updated"],
        failure_gates=["Test failure", "Naming violation", "Missing ledger update"],
    )


def sop_graph_generate(request: SOPGenerationRequest) -> SOPGenerationResult:
    """Generate a generic SOP graph from a request."""

    graph = _generic_graph(request)
    return _generation_result(
        graph,
        include_skill_skeleton=request.include_skill_skeleton,
        include_codex_prompt=request.include_codex_prompt,
    )


def paper_sop_graph_generate(request: SOPGenerationRequest) -> dict[str, object]:
    """Thin paper.sop_graph_generate wrapper."""

    return sop_graph_generate(request).model_dump(mode="json")


def _generic_graph(request: SOPGenerationRequest) -> SOPGraph:
    quality_gates = request.quality_gates or ["EvidenceRef present", "StateLedger updated"]
    failure_gates = request.failure_gates or ["Missing evidence", "Blocked gate"]
    tools = request.tools or ["paper.sop_graph_generate"]
    return SOPGraph(
        graph_id=f"{request.graph_type}-{request.source_id}",
        graph_type=request.graph_type,
        title=request.title,
        nodes=[
            SOPNode(node_id="input", label="Input artifacts", kind=SOPNodeKind.ARTIFACT),
            SOPNode(node_id="tool", label=tools[0], kind=SOPNodeKind.TOOL),
            SOPNode(node_id="quality", label=quality_gates[0], kind=SOPNodeKind.QUALITY_GATE),
            SOPNode(node_id="failure", label=failure_gates[0], kind=SOPNodeKind.FAILURE_GATE),
            SOPNode(node_id="output", label="Output artifacts", kind=SOPNodeKind.ARTIFACT),
        ],
        edges=[
            SOPEdge(source="input", target="tool"),
            SOPEdge(source="tool", target="quality"),
            SOPEdge(source="quality", target="output", label="passed"),
            SOPEdge(source="quality", target="failure", label="failed"),
        ],
        input_artifacts=request.input_artifacts,
        output_artifacts=request.output_artifacts,
        tools=tools,
        quality_gates=quality_gates,
        failure_gates=failure_gates,
    )


def _generation_result(
    graph: SOPGraph,
    include_skill_skeleton: bool = False,
    include_codex_prompt: bool = False,
) -> SOPGenerationResult:
    mermaid_text = export_mermaid(graph)
    return SOPGenerationResult(
        graph=graph,
        mermaid_text=mermaid_text,
        sop_markdown=export_sop_markdown(graph, mermaid_text),
        skill_skeleton=generate_skill_skeleton(graph) if include_skill_skeleton else None,
        codex_prompt=generate_codex_prompt(graph) if include_codex_prompt else None,
    )


def _block_node_id(block: ArticleBlock) -> str:
    if block.block_kind is not None:
        return block.block_kind.value
    return f"section_{block.section.value}"

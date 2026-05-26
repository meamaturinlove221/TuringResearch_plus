"""Executable review plans for ontology SOP parity."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.alias_resolver import (
    AliasResolutionReport,
    resolve_aliases,
)
from turing_research_plus.vault_graph.models import (
    OntologySOPResult,
    VaultGraph,
    VaultGraphStatus,
)
from turing_research_plus.vault_graph.ontology import ONTOLOGY_SOPS, run_ontology_sop
from turing_research_plus.vault_graph.ontology_gap_detector import (
    OntologyGapReport,
    detect_ontology_gaps,
)


class OntologySOPRunPlan(BaseModel):
    """Review-only ontology SOP run package."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    requested_sops: list[str] = Field(default_factory=list)
    steps: list[OntologySOPResult] = Field(default_factory=list)
    alias_report: AliasResolutionReport
    gap_report: OntologyGapReport
    proposed_outputs: list[str] = Field(default_factory=list)
    status: VaultGraphStatus = VaultGraphStatus.REVIEW
    requires_human_review: bool = True
    final_knowledge_graph_generated: bool = False
    network_required: bool = False


def run_ontology_sop_plan(
    graph: VaultGraph,
    *,
    sop_names: list[str] | None = None,
    aliases: list[str] | None = None,
) -> OntologySOPRunPlan:
    """Build a deterministic SOP run plan without external side effects."""

    requested_sops = sop_names or list(ONTOLOGY_SOPS)
    steps = [
        run_ontology_sop(sop_name, inputs=[graph.graph_id])
        for sop_name in requested_sops
    ]
    alias_report = resolve_aliases(graph, aliases or [])
    gap_report = detect_ontology_gaps(graph)
    proposed_outputs = [
        f"review:{step.sop_name}:{output}"
        for step in steps
        for output in step.outputs
    ]
    return OntologySOPRunPlan(
        graph_id=graph.graph_id,
        requested_sops=requested_sops,
        steps=steps,
        alias_report=alias_report,
        gap_report=gap_report,
        proposed_outputs=proposed_outputs,
    )


def render_ontology_sop_runbook(plan: OntologySOPRunPlan) -> str:
    """Render a SOP run package as Markdown."""

    step_lines = [f"- `{step.sop_name}` -> {', '.join(step.outputs)}" for step in plan.steps]
    output_lines = [f"- `{item}`" for item in plan.proposed_outputs] or ["- none"]
    lines = [
        f"# Ontology SOP Runbook: {plan.graph_id}",
        "",
        f"- Status: `{plan.status.value}`",
        f"- Requires human review: `{str(plan.requires_human_review).lower()}`",
        "- Final knowledge graph generated: `false`",
        "- Network required: `false`",
        "",
        "## Steps",
        "",
        *step_lines,
        "",
        "## Proposed Outputs",
        "",
        *output_lines,
        "",
        "## Gap Summary",
        "",
        f"- Gaps: `{len(plan.gap_report.gaps)}`",
        f"- Release blocker: `{str(plan.gap_report.release_blocker).lower()}`",
        "",
        "## Alias Summary",
        "",
        f"- Candidates: `{len(plan.alias_report.candidates)}`",
        f"- Unresolved: `{len(plan.alias_report.unresolved_aliases)}`",
    ]
    return "\n".join(lines) + "\n"

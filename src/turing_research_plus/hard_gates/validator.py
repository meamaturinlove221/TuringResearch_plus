"""Hard gate validation."""

from __future__ import annotations

from turing_research_plus.hard_gates.library import default_vggt_gate_library
from turing_research_plus.hard_gates.models import (
    GateInputRef,
    GateOutcome,
    GateResult,
    HardGateValidationInput,
    HardGateValidationReport,
)


def validate_hard_gates(
    request: HardGateValidationInput,
    library: dict[str, object] | None = None,
) -> HardGateValidationReport:
    """Validate gates against local input refs without external side effects."""

    gate_library = library or default_vggt_gate_library()
    input_map = {item.ref_id: item for item in request.inputs}
    results: list[GateResult] = []

    for gate_id in request.gate_ids:
        if gate_id not in gate_library:
            results.append(
                GateResult(
                    gate_id=gate_id,
                    outcome=GateOutcome.REQUIRES_HUMAN_REVIEW,
                    reasons=[f"Unknown gate: {gate_id}"],
                    missing_inputs=[gate_id],
                )
            )
            continue
        results.append(_evaluate_gate(gate_id, input_map, request.allow_human_review))

    blocked = sum(1 for result in results if result.outcome == GateOutcome.BLOCK)
    review = sum(1 for result in results if result.outcome == GateOutcome.REQUIRES_HUMAN_REVIEW)
    insufficient = sum(
        1 for result in results if result.outcome == GateOutcome.NOT_ENOUGH_EVIDENCE
    )
    summary = (
        f"{len(results)} gates checked; {blocked} blocked; "
        f"{review} require human review; {insufficient} lack evidence."
    )
    return HardGateValidationReport(
        report_id=_report_id(request),
        route_id=request.route_id,
        stage_id=request.stage_id,
        results=results,
        summary=summary,
    )


def _evaluate_gate(
    gate_id: str,
    input_map: dict[str, GateInputRef],
    allow_human_review: bool,
) -> GateResult:
    item = input_map.get(gate_id)
    if item is None:
        return GateResult(
            gate_id=gate_id,
            outcome=GateOutcome.REQUIRES_HUMAN_REVIEW
            if allow_human_review
            else GateOutcome.NOT_ENOUGH_EVIDENCE,
            reasons=[f"Missing input for gate {gate_id}"],
            missing_inputs=[gate_id],
        )

    status = item.status
    if status in {"pass", "observed", "local-observed"} and item.evidence_refs:
        return GateResult(
            gate_id=gate_id,
            outcome=GateOutcome.PASS,
            evidence_refs=item.evidence_refs,
        )
    if status in {"hard-blocked", "failed", "blocked"}:
        return GateResult(
            gate_id=gate_id,
            outcome=GateOutcome.BLOCK,
            reasons=[item.summary],
            evidence_refs=item.evidence_refs,
        )
    if status in {"planned", "requires-real-experiment", "not-enough-evidence"}:
        return GateResult(
            gate_id=gate_id,
            outcome=GateOutcome.NOT_ENOUGH_EVIDENCE,
            reasons=[item.summary],
            evidence_refs=item.evidence_refs,
        )
    return GateResult(
        gate_id=gate_id,
        outcome=GateOutcome.REQUIRES_HUMAN_REVIEW,
        reasons=[item.summary],
        evidence_refs=item.evidence_refs,
    )


def _report_id(request: HardGateValidationInput) -> str:
    route = request.route_id or "route"
    stage = request.stage_id or "all"
    return f"hard-gates-{route}-{stage}"

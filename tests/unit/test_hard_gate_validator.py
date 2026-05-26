from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.hard_gates.models import (
    GateInputRef,
    GateOutcome,
    HardGateValidationInput,
)
from turing_research_plus.hard_gates.validator import validate_hard_gates


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="fixture", locator="line 1", quote="observed")


def test_gate_passes_with_observed_evidence() -> None:
    report = validate_hard_gates(
        HardGateValidationInput(
            gate_ids=["sha256_required"],
            inputs=[
                GateInputRef(
                    ref_id="sha256_required",
                    ref_type="artifact",
                    status="observed",
                    summary="checksum present",
                    evidence_refs=[evidence()],
                )
            ],
        )
    )

    assert report.passed is True


def test_gate_blocks_hard_blocked_input() -> None:
    report = validate_hard_gates(
        HardGateValidationInput(
            gate_ids=["real_backend_required"],
            inputs=[
                GateInputRef(
                    ref_id="real_backend_required",
                    ref_type="backend",
                    status="hard-blocked",
                    summary="backend unavailable",
                )
            ],
        )
    )

    assert report.results[0].outcome == GateOutcome.BLOCK


def test_missing_gate_requires_human_review() -> None:
    report = validate_hard_gates(HardGateValidationInput(gate_ids=["visual_board_required"]))

    assert report.results[0].outcome == GateOutcome.REQUIRES_HUMAN_REVIEW
    assert "visual_board_required" in report.results[0].missing_inputs


def test_planned_gate_is_not_enough_evidence() -> None:
    report = validate_hard_gates(
        HardGateValidationInput(
            gate_ids=["sparse_backend_probe_required"],
            inputs=[
                GateInputRef(
                    ref_id="sparse_backend_probe_required",
                    ref_type="backend",
                    status="planned",
                    summary="probe is planned",
                )
            ],
        )
    )

    assert report.results[0].outcome == GateOutcome.NOT_ENOUGH_EVIDENCE

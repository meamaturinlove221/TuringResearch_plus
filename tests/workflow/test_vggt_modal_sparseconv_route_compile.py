from pathlib import Path

from turing_research_plus.experiment_route.compiler import compile_experiment_route
from turing_research_plus.experiment_route.models import ExperimentRouteCompileInput
from turing_research_plus.hard_gates.models import (
    GateInputRef,
    GateOutcome,
    HardGateValidationInput,
)
from turing_research_plus.hard_gates.validator import validate_hard_gates

FIXTURE = Path("examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml")


def test_vggt_modal_sparseconv_route_compile_keeps_planned_status() -> None:
    route, prompt = compile_experiment_route(ExperimentRouteCompileInput(route_path=FIXTURE))

    assert route.status == "requires-real-experiment"
    assert "not executed by TuringResearch" in route.final_states
    assert "run Modal" in route.forbidden_actions
    assert "requires-real-experiment" in prompt.warnings


def test_vggt_modal_sparseconv_hard_gates_do_not_pass_without_real_backend() -> None:
    report = validate_hard_gates(
        HardGateValidationInput(
            route_id="modal_sparseconv_v0",
            gate_ids=["real_backend_required", "sparse_backend_probe_required"],
            inputs=[
                GateInputRef(
                    ref_id="real_backend_required",
                    ref_type="backend",
                    status="requires-real-experiment",
                    summary="real backend has not run",
                ),
                GateInputRef(
                    ref_id="sparse_backend_probe_required",
                    ref_type="backend",
                    status="planned",
                    summary="probe planned only",
                ),
            ],
        )
    )

    assert report.passed is False
    assert {result.outcome for result in report.results} == {GateOutcome.NOT_ENOUGH_EVIDENCE}

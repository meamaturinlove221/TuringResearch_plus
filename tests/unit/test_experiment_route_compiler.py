from pathlib import Path

import pytest

from turing_research_plus.experiment_route.compiler import compile_experiment_route
from turing_research_plus.experiment_route.models import ExperimentRouteCompileInput

FIXTURE = Path("examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml")


def test_compile_modal_sparseconv_route() -> None:
    route, prompt = compile_experiment_route(ExperimentRouteCompileInput(route_path=FIXTURE))

    assert route.route_id == "modal_sparseconv_v0"
    assert prompt.route_id == route.route_id
    assert "not executed by TuringResearch" in prompt.warnings


def test_compile_rejects_unknown_gate() -> None:
    route_data = {
        "route_id": "bad",
        "goal": "bad",
        "context": "bad",
        "forbidden_actions": ["claim experiment completion"],
        "stages": [{"id": "s1", "name": "bad", "purpose": "bad", "hard_gates": ["missing"]}],
    }

    with pytest.raises(ValueError, match="unknown hard gate"):
        compile_experiment_route(ExperimentRouteCompileInput(route_data=route_data))

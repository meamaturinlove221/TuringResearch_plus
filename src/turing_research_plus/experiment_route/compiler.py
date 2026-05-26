"""Compile Experiment Route DSL specs."""

from __future__ import annotations

from turing_research_plus.experiment_route.models import (
    ControllerPromptDraft,
    ExperimentRouteCompileInput,
    ExperimentRouteSpec,
)
from turing_research_plus.experiment_route.parser import parse_experiment_route
from turing_research_plus.experiment_route.prompt_renderer import render_controller_prompt
from turing_research_plus.hard_gates.library import default_vggt_gate_library


def compile_experiment_route(
    request: ExperimentRouteCompileInput,
) -> tuple[ExperimentRouteSpec, ControllerPromptDraft]:
    """Compile a route spec and prompt draft without executing the route."""

    route = parse_experiment_route(request.route_data or request.route_path)  # type: ignore[arg-type]
    _validate_gate_ids(route)
    return route, render_controller_prompt(route)


def _validate_gate_ids(route: ExperimentRouteSpec) -> None:
    library = default_vggt_gate_library()
    unknown = sorted(
        {
            gate
            for gate in route.hard_gates
            + [stage_gate for stage in route.stages for stage_gate in stage.hard_gates]
            if gate not in library
        }
    )
    if unknown:
        raise ValueError(f"unknown hard gate ids: {', '.join(unknown)}")

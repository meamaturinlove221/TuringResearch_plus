"""Capsule-local tool wrappers for Experiment Route DSL."""

from __future__ import annotations

from typing import Any

from turing_research_plus.experiment_route.compiler import compile_experiment_route
from turing_research_plus.experiment_route.models import ExperimentRouteCompileInput


def experiment_route_compile(request: ExperimentRouteCompileInput) -> dict[str, Any]:
    """Compile a route and return JSON-safe route plus prompt payload."""

    route, prompt = compile_experiment_route(request)
    return {
        "route": route.model_dump(mode="json"),
        "controller_prompt": prompt.model_dump(mode="json"),
    }

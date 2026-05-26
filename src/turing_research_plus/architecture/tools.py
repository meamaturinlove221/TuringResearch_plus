"""Capsule-local tool wrappers for Figure-to-Architecture."""

from __future__ import annotations

from typing import Any

from turing_research_plus.architecture.graph_builder import (
    build_architecture_from_method_card,
    build_architecture_from_route,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec
from turing_research_plus.paper_method.models import PaperMethodCard


def paper_figure_to_architecture_from_method_card(card: PaperMethodCard) -> dict[str, Any]:
    """Build architecture spec from a method card."""

    return build_architecture_from_method_card(card).model_dump(mode="json")


def paper_figure_to_architecture_from_route(route: ExperimentRouteSpec) -> dict[str, Any]:
    """Build architecture spec from an experiment route."""

    return build_architecture_from_route(route).model_dump(mode="json")

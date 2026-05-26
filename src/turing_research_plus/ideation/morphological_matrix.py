"""Morphological matrix construction."""

from __future__ import annotations

from turing_research_plus.hypothesis.models import Hypothesis
from turing_research_plus.ideation.models import MorphologicalAxis, MorphologicalMatrix


def build_morphological_matrix(
    hypothesis: Hypothesis,
    matrix_id: str | None = None,
) -> MorphologicalMatrix:
    """Build a deterministic morphological matrix from a hypothesis."""

    return MorphologicalMatrix(
        matrix_id=matrix_id or f"matrix-{hypothesis.hypothesis_id}",
        hypothesis_link=hypothesis.hypothesis_id,
        axes=[
            MorphologicalAxis(
                name="mechanism",
                options=[
                    hypothesis.mechanism,
                    "counterfactual evidence audit",
                ],
            ),
            MorphologicalAxis(
                name="required_data",
                options=hypothesis.required_experiment.required_data,
            ),
            MorphologicalAxis(
                name="model_component",
                options=[
                    hypothesis.independent_variables[0],
                    hypothesis.dependent_variables[0],
                ],
            ),
            MorphologicalAxis(
                name="evaluation_target",
                options=hypothesis.dependent_variables,
            ),
            MorphologicalAxis(
                name="risk_profile",
                options=[hypothesis.risk_level],
            ),
        ],
    )


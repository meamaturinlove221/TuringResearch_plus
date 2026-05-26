from pathlib import Path

from turing_research_plus.experiment_route.parser import parse_experiment_route
from turing_research_plus.experiment_route.prompt_renderer import render_controller_prompt


def test_prompt_renderer_marks_planning_boundary() -> None:
    route = parse_experiment_route(
        Path("examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml")
    )
    prompt = render_controller_prompt(route)

    assert "does not execute VGGT" in prompt.body
    assert "planned route only" in prompt.warnings
    assert "requires-real-experiment" in prompt.warnings

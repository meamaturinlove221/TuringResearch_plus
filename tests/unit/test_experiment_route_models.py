import pytest

from turing_research_plus.experiment_route.models import ExperimentRouteSpec


def route_payload() -> dict[str, object]:
    return {
        "route_id": "route-1",
        "goal": "plan route",
        "context": "dry-run context",
        "forbidden_actions": ["claim experiment completion"],
        "stages": [
            {
                "id": "s1",
                "name": "stage",
                "purpose": "test",
                "hard_gates": ["no_promotion"],
            }
        ],
    }


def test_experiment_route_model_validates_minimal_route() -> None:
    route = ExperimentRouteSpec.model_validate(route_payload())

    assert route.route_id == "route-1"
    assert route.stages[0].id == "s1"
    assert "not executed" in route.to_markdown()


def test_experiment_route_requires_forbidden_completion_claim_boundary() -> None:
    payload = route_payload()
    payload["forbidden_actions"] = ["run something"]

    with pytest.raises(ValueError, match="forbid claiming experiment completion"):
        ExperimentRouteSpec.model_validate(payload)

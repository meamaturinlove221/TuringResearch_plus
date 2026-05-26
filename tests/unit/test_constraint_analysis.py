from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.experiment.constraints import analyze_constraints
from turing_research_plus.experiment.design import design_experiment
from turing_research_plus.experiment.models import ComputeBudget
from turing_research_plus.experiment.service import ExperimentExecutionService
from turing_research_plus.experiment.tools import research_constraint_analyze
from turing_research_plus.hypothesis.falsifiability import build_hypothesis
from turing_research_plus.hypothesis.models import GapPriority, Hypothesis


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def hypothesis() -> Hypothesis:
    return build_hypothesis(
        GapPriority(
            gap_id="gap-1",
            description="Few studies validate workflow gates.",
            score=0.9,
            rationale="High confidence and enough evidence.",
            evidence=[evidence()],
        )
    )


def test_constraint_analysis_marks_feasible_plan() -> None:
    analysis = analyze_constraints(design_experiment(hypothesis()))

    assert analysis.feasible is True
    assert analysis.blockers == []
    assert analysis.constraints


def test_constraint_analysis_flags_tiny_compute_budget() -> None:
    plan = design_experiment(hypothesis()).model_copy(
        update={
            "compute_budget": ComputeBudget(
                max_runtime_minutes=1,
                max_cost_units=0.0,
                resource_class="local-dry-run",
            )
        }
    )
    analysis = analyze_constraints(plan)

    assert analysis.feasible is False
    assert "compute budget too small" in analysis.blockers


def test_constraint_analyze_tool_returns_json_payload() -> None:
    payload = research_constraint_analyze(
        design_experiment(hypothesis()),
        ExperimentExecutionService(),
    )

    assert payload["feasible"] is True
    assert payload["mitigation_options"]

"""Scenario catalog for review-only stress tests."""

from __future__ import annotations

from turing_research_plus.stress_test.models import (
    StressScenario,
    StressScenarioId,
    StressSeverity,
)


def list_stress_scenarios() -> list[StressScenario]:
    """Return the fixed v1.2 stress scenario catalog."""

    return [
        StressScenario(
            scenario_id=StressScenarioId.MISSING_EVIDENCE,
            purpose="Detect claims or routes without evidence references.",
            risk_question="Can this claim be traced to evidence?",
            default_severity=StressSeverity.HIGH,
            recommended_action="Add evidence refs or mark the claim as blocked.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.FAKE_RESULT_RISK,
            purpose="Prevent fake/demo outputs from becoming observed results.",
            risk_question="Could a demo fixture be read as a real result?",
            default_severity=StressSeverity.CRITICAL,
            recommended_action="Keep fake/demo status explicit and block observed wording.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.OVERCLAIM,
            purpose="Catch success or final-paper overclaiming.",
            risk_question="Does the text claim more than the evidence supports?",
            default_severity=StressSeverity.HIGH,
            recommended_action="Downgrade to planned/review-only wording.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.ARTIFACT_MISSING,
            purpose="Check whether required artifacts are present.",
            risk_question="Can outputs be inspected by a reviewer?",
            default_severity=StressSeverity.HIGH,
            recommended_action="Add artifact refs or keep the route blocked.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.WEAK_RELATED_WORK,
            purpose="Surface weak or missing related work.",
            risk_question="Is the literature context enough for review?",
            default_severity=StressSeverity.MEDIUM,
            recommended_action="Add related work refs or mark the section incomplete.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.UNSAFE_PLUGIN,
            purpose="Detect unsafe plugin permissions.",
            risk_question="Could a plugin execute code or access secrets by default?",
            default_severity=StressSeverity.CRITICAL,
            recommended_action="Disable unsafe permissions and require review.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.PRIVACY_LEAK,
            purpose="Detect private data, local paths, or credential leakage risk.",
            risk_question="Could public output expose private data?",
            default_severity=StressSeverity.CRITICAL,
            recommended_action="Redact, remove, or block public release.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.ROUTE_CONTRADICTION,
            purpose="Detect route claims that contradict hard gates or forbidden actions.",
            risk_question="Does the route claim completion that its gates forbid?",
            default_severity=StressSeverity.HIGH,
            recommended_action="Resolve route contradiction before convergence.",
        ),
        StressScenario(
            scenario_id=StressScenarioId.ADVISOR_PACK_UNSUPPORTED_CLAIM,
            purpose="Detect advisor-pack claims without supporting evidence.",
            risk_question="Could advisor-facing output overstate support?",
            default_severity=StressSeverity.HIGH,
            recommended_action="Link advisor claims to evidence or block them.",
        ),
    ]


def get_stress_scenario(scenario_id: StressScenarioId) -> StressScenario:
    """Return one scenario by id."""

    scenarios = {scenario.scenario_id: scenario for scenario in list_stress_scenarios()}
    return scenarios[scenario_id]

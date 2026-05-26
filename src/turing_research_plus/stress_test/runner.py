"""Deterministic stress-test runner for v1.2 parity."""

from __future__ import annotations

import re

from turing_research_plus.stress_test.models import (
    StressFinding,
    StressScenario,
    StressScenarioId,
    StressSeverity,
    StressStatus,
    StressTestInput,
    StressTestReport,
)
from turing_research_plus.stress_test.scenarios import list_stress_scenarios

PRIVATE_MARKERS = (
    "D:/",
    "D:\\",
    ".env",
    "local_project_links.yaml",
    "private_data",
    "raw data",
    "patient data",
)
SECRET_PATTERN = re.compile(r"(sk-[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9_]{8,})")
OVERCLAIM_MARKERS = (
    "final paper",
    "camera-ready",
    "experiment succeeded",
    "proves",
    "verified success",
)
UNSAFE_PLUGIN_PERMISSIONS = {
    "execute_code",
    "shell",
    "network",
    "secrets",
    "filesystem_write",
}


def run_stress_test(request: StressTestInput) -> StressTestReport:
    """Run all stress scenarios locally without network or agent runtime."""

    findings = [_evaluate_scenario(scenario, request) for scenario in list_stress_scenarios()]
    blockers = [
        finding.scenario_id.value
        for finding in findings
        if finding.status == StressStatus.FAIL
    ]
    warnings = [
        finding.scenario_id.value
        for finding in findings
        if finding.status == StressStatus.WARN
    ]
    status = (
        StressStatus.FAIL
        if blockers
        else StressStatus.WARN
        if warnings
        else StressStatus.PASS
    )
    return StressTestReport(
        target_id=request.target_id,
        findings=findings,
        status=status,
        blockers=blockers,
        warnings=warnings,
        convergence_recommendation=_recommend_convergence(status, blockers, warnings),
    )


def _evaluate_scenario(
    scenario: StressScenario,
    request: StressTestInput,
) -> StressFinding:
    checks = {
        StressScenarioId.MISSING_EVIDENCE: _check_missing_evidence,
        StressScenarioId.FAKE_RESULT_RISK: _check_fake_result_risk,
        StressScenarioId.OVERCLAIM: _check_overclaim,
        StressScenarioId.ARTIFACT_MISSING: _check_artifact_missing,
        StressScenarioId.WEAK_RELATED_WORK: _check_weak_related_work,
        StressScenarioId.UNSAFE_PLUGIN: _check_unsafe_plugin,
        StressScenarioId.PRIVACY_LEAK: _check_privacy_leak,
        StressScenarioId.ROUTE_CONTRADICTION: _check_route_contradiction,
        StressScenarioId.ADVISOR_PACK_UNSUPPORTED_CLAIM: _check_advisor_claims,
    }
    status, message, evidence = checks[scenario.scenario_id](request)
    severity = (
        scenario.default_severity
        if status != StressStatus.PASS
        else StressSeverity.INFORMATIONAL
    )
    return StressFinding(
        scenario_id=scenario.scenario_id,
        status=status,
        severity=severity,
        message=message,
        evidence=evidence,
        recommended_action=scenario.recommended_action,
    )


def _check_missing_evidence(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    if request.evidence_refs:
        return StressStatus.PASS, "Evidence refs are present.", request.evidence_refs
    return StressStatus.FAIL, "No evidence refs were provided.", []


def _check_fake_result_risk(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    text = _combined_text(request)
    if request.fake_demo_only and "observed" in text:
        return (
            StressStatus.FAIL,
            "Fake/demo context contains observed-result wording.",
            ["observed"],
        )
    if "demo only" in text or request.fake_demo_only:
        return StressStatus.PASS, "Fake/demo boundary is explicit.", []
    return StressStatus.WARN, "Fake/live boundary is not explicit.", []


def _check_overclaim(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    text = _combined_text(request)
    hits = [marker for marker in OVERCLAIM_MARKERS if marker in text]
    if hits:
        return StressStatus.FAIL, "Overclaim markers were found.", hits
    return StressStatus.PASS, "No overclaim markers found.", []


def _check_artifact_missing(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    if request.artifact_refs:
        return StressStatus.PASS, "Artifact refs are present.", request.artifact_refs
    return StressStatus.FAIL, "No artifact refs were provided.", []


def _check_weak_related_work(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    if len(request.related_work_refs) >= 2:
        return (
            StressStatus.PASS,
            "Related work refs are sufficient for review.",
            request.related_work_refs,
        )
    return StressStatus.WARN, "Related work refs are thin.", request.related_work_refs


def _check_unsafe_plugin(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    unsafe = sorted(set(request.plugin_permissions) & UNSAFE_PLUGIN_PERMISSIONS)
    if unsafe:
        return StressStatus.FAIL, "Unsafe plugin permissions requested.", unsafe
    return StressStatus.PASS, "No unsafe plugin permissions requested.", []


def _check_privacy_leak(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    text = _combined_text(request)
    hits = [marker for marker in PRIVATE_MARKERS if marker.lower() in text]
    hits.extend(SECRET_PATTERN.findall(text))
    if request.data_sensitivity == "private":
        hits.append("data_sensitivity:private")
    if hits:
        return StressStatus.FAIL, "Privacy or secret markers were found.", sorted(set(hits))
    return StressStatus.PASS, "No privacy markers found.", []


def _check_route_contradiction(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    hard_gate_text = " ".join([*request.route_hard_gates, *request.route_forbidden_actions]).lower()
    claim_text = " ".join(request.route_claims).lower()
    contradictions = []
    if "claim experiment completion" in hard_gate_text and "completed" in claim_text:
        contradictions.append("completion-claim")
    if "no live" in hard_gate_text and request.live_mode_enabled:
        contradictions.append("live-mode-enabled")
    if contradictions:
        return StressStatus.FAIL, "Route contradiction detected.", contradictions
    return StressStatus.PASS, "No route contradictions detected.", []


def _check_advisor_claims(request: StressTestInput) -> tuple[StressStatus, str, list[str]]:
    if request.advisor_claims and not request.evidence_refs:
        return StressStatus.FAIL, "Advisor claims have no evidence refs.", request.advisor_claims
    return (
        StressStatus.PASS,
        "Advisor claims are evidence-linked or absent.",
        request.advisor_claims,
    )


def _recommend_convergence(
    status: StressStatus,
    blockers: list[str],
    warnings: list[str],
) -> str:
    if status == StressStatus.FAIL:
        return f"Do not converge yet; resolve blockers: {', '.join(blockers)}."
    if status == StressStatus.WARN:
        return f"Converge only after human review of warnings: {', '.join(warnings)}."
    return "Ready for human-reviewed convergence; keep execution outside this report."


def _combined_text(request: StressTestInput) -> str:
    return " ".join(
        [
            request.task_summary,
            *request.route_claims,
            *request.advisor_claims,
            *request.text_blocks,
        ]
    ).lower()

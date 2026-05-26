from __future__ import annotations

from turing_research_plus.plugins.future_sandbox import build_future_sandbox_roadmap
from turing_research_plus.plugins.risk_report import build_plugin_sandbox_report
from turing_research_plus.plugins.sandbox_policy import SandboxPermission, SandboxRiskLevel


def test_plugin_sandbox_report_marks_blockers() -> None:
    report = build_plugin_sandbox_report(
        "unsafe_plugin",
        [
            SandboxPermission.READ_PROJECT_FILES,
            SandboxPermission.EXECUTE_CODE,
            SandboxPermission.SECRETS_ACCESS,
        ],
    )

    assert report.release_blocker is True
    assert report.severity == SandboxRiskLevel.CRITICAL
    assert SandboxPermission.EXECUTE_CODE in report.denied_permissions
    assert SandboxPermission.SECRETS_ACCESS in report.denied_permissions
    assert report.requires_human_review is True
    assert report.implements_os_sandbox is False


def test_plugin_sandbox_report_allows_scoped_read() -> None:
    report = build_plugin_sandbox_report(
        "read_only_plugin",
        [SandboxPermission.READ_PROJECT_FILES],
        scoped=True,
    )

    assert report.release_blocker is False
    assert report.allowed_permissions == [SandboxPermission.READ_PROJECT_FILES]
    assert report.denied_permissions == []


def test_future_sandbox_roadmap_is_not_current_os_sandbox() -> None:
    roadmap = build_future_sandbox_roadmap()

    assert roadmap.implements_os_sandbox_now is False
    assert roadmap.requires_human_review is True
    assert {milestone.milestone_id for milestone in roadmap.milestones} >= {
        "threat-model",
        "dependency-isolation",
        "filesystem-scope",
        "network-policy",
        "provenance",
    }

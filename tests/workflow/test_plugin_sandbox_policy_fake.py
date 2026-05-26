from __future__ import annotations

from turing_research_plus.plugins.sandbox_policy import SandboxPermission
from turing_research_plus.plugins.tools import (
    plugin_future_sandbox_roadmap,
    plugin_sandbox_check,
)


def test_plugin_sandbox_policy_fake_workflow() -> None:
    report = plugin_sandbox_check(
        "trusted_local_demo_plugin",
        [
            SandboxPermission.READ_PROJECT_FILES,
            SandboxPermission.ARTIFACT_EXPORT,
            SandboxPermission.NETWORK_ACCESS,
        ],
        scoped=True,
    )
    roadmap = plugin_future_sandbox_roadmap()

    assert report.plugin_id == "trusted_local_demo_plugin"
    assert report.release_blocker is True
    assert SandboxPermission.READ_PROJECT_FILES in report.allowed_permissions
    assert SandboxPermission.NETWORK_ACCESS in report.denied_permissions
    assert report.future_sandbox_requirements
    assert roadmap.implements_os_sandbox_now is False

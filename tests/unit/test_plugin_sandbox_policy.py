from __future__ import annotations

import pytest

from turing_research_plus.plugins.sandbox_policy import (
    PluginSandboxPolicy,
    SandboxPermission,
    default_plugin_sandbox_policy,
)


def test_default_plugin_sandbox_policy_declares_required_categories() -> None:
    policy = default_plugin_sandbox_policy()

    assert SandboxPermission.READ_PROJECT_FILES in policy.allowed_permissions
    assert SandboxPermission.EXECUTE_CODE in policy.denied_permissions
    assert SandboxPermission.SHELL_ACCESS in policy.denied_permissions
    assert SandboxPermission.SECRETS_ACCESS in policy.denied_permissions
    assert SandboxPermission.REMOTE_WRITE in policy.denied_permissions
    assert SandboxPermission.NETWORK_ACCESS in policy.explicit_permissions
    assert SandboxPermission.WRITE_PROJECT_FILES in policy.explicit_permissions
    assert SandboxPermission.READ_PROJECT_FILES in policy.scoped_permissions
    assert policy.implements_os_sandbox is False
    assert policy.requires_human_review is True


def test_plugin_sandbox_policy_rejects_claimed_os_sandbox() -> None:
    with pytest.raises(ValueError, match="does not implement an OS sandbox"):
        PluginSandboxPolicy(implements_os_sandbox=True)

from __future__ import annotations

import pytest

from turing_research_plus.plugins.models import (
    PluginManifest,
    PluginSafetyLevel,
    PluginStatus,
    PluginType,
)
from turing_research_plus.plugins.trust_policy import (
    PluginTrustSource,
    PluginTrustStatus,
    evaluate_plugin_trust,
)


def manifest(*, permissions: list[str], third_party: bool = False) -> PluginManifest:
    return PluginManifest(
        plugin_id="trusted_demo",
        name="Trusted Demo",
        version="0.1.0",
        type=PluginType.EXPORTER,
        required_permissions=permissions,
        safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        status=PluginStatus.DISABLED,
        third_party=third_party,
    )


def test_built_in_demo_plugin_is_allowed_as_metadata() -> None:
    decision = evaluate_plugin_trust(
        manifest(permissions=["read_demo_markdown"]),
        source=PluginTrustSource.BUILT_IN_DEMO,
    )

    assert decision.status == PluginTrustStatus.ALLOWED
    assert decision.trusted is True
    assert decision.allowed_to_load_manifest is True
    assert decision.expose_capabilities_disabled is True


def test_workspace_local_plugin_requires_explicit_trusted_flag() -> None:
    decision = evaluate_plugin_trust(
        manifest(permissions=["read_demo_markdown"]),
        source=PluginTrustSource.WORKSPACE_LOCAL,
    )

    assert decision.status == PluginTrustStatus.DISABLED_BY_DEFAULT
    assert decision.allowed_to_load_manifest is False

    trusted = evaluate_plugin_trust(
        manifest(permissions=["read_demo_markdown"]),
        source=PluginTrustSource.WORKSPACE_LOCAL,
        explicit_trusted=True,
    )
    assert trusted.status == PluginTrustStatus.ALLOWED


def test_third_party_plugin_is_disabled_by_default() -> None:
    decision = evaluate_plugin_trust(
        manifest(permissions=["read_demo_markdown"], third_party=True),
        source=PluginTrustSource.THIRD_PARTY,
    )

    assert decision.status == PluginTrustStatus.DISABLED_BY_DEFAULT
    assert decision.trusted is False


@pytest.mark.parametrize("permission", ["execute_code", "secrets_access", "remote_write"])
def test_blocked_permissions_are_blocked(permission: str) -> None:
    decision = evaluate_plugin_trust(
        manifest(permissions=[permission]),
        source=PluginTrustSource.BUILT_IN_DEMO,
    )

    assert decision.status == PluginTrustStatus.BLOCKED
    assert decision.allowed_to_load_manifest is False


def test_network_access_requires_explicit_live_flag() -> None:
    decision = evaluate_plugin_trust(
        manifest(permissions=["network_access"]),
        source=PluginTrustSource.BUILT_IN_DEMO,
    )

    assert decision.status == PluginTrustStatus.REQUIRES_LIVE_FLAG

    live = evaluate_plugin_trust(
        manifest(permissions=["network_access"]),
        source=PluginTrustSource.BUILT_IN_DEMO,
        explicit_live=True,
    )
    assert live.status == PluginTrustStatus.ALLOWED

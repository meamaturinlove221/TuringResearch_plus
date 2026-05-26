from __future__ import annotations

from turing_research_plus.capabilities.collector import (
    collect_capability_manifest,
    collect_core_capabilities,
)
from turing_research_plus.capabilities.models import CapabilityCategory


def test_collect_core_capabilities_covers_required_categories() -> None:
    capabilities = collect_core_capabilities()

    categories = {entry.category for entry in capabilities}

    assert categories == set(CapabilityCategory)
    assert len(capabilities) >= 16


def test_collect_core_capabilities_keeps_live_modes_explicit() -> None:
    capabilities = collect_core_capabilities()

    live_capabilities = [entry for entry in capabilities if entry.live_mode]

    assert live_capabilities
    assert all(entry.required_env for entry in live_capabilities)
    assert all(entry.fake_mode is True for entry in capabilities)


def test_collect_capability_manifest_is_static_and_review_only() -> None:
    manifest = collect_capability_manifest()

    assert manifest.manifest_id == "turingresearch_capabilities"
    assert manifest.generated_from_static_catalog is True
    assert manifest.starts_mcp_server is False
    assert manifest.executes_tools is False
    assert manifest.requires_human_review is True

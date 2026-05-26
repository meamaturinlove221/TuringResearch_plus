from __future__ import annotations

import pytest

from turing_research_plus.capabilities.models import (
    CapabilityCategory,
    CapabilityEntry,
    CapabilityManifest,
    CapabilitySafetyLevel,
)


def test_capability_entry_records_required_fields() -> None:
    entry = CapabilityEntry(
        capability_id="demo.capability",
        name="Demo Capability",
        category=CapabilityCategory.PLUGIN,
        tool_name="plugins.demo",
        command="turing plugins demo",
        module="turing_research_plus.plugins",
        input_model="DemoInput",
        output_model="DemoOutput",
        live_mode=False,
        fake_mode=True,
        required_env=[],
        safety_level=CapabilitySafetyLevel.LOCAL_REVIEW,
        docs=["docs/plugin-architecture.md"],
        tests=["tests/unit/test_plugin_models.py"],
        related_skills=["turingresearch-qa-release"],
    )

    assert entry.capability_id == "demo.capability"
    assert entry.tool_name == "plugins.demo"
    assert entry.fake_mode is True
    assert entry.live_mode is False


def test_live_capability_requires_env_gate() -> None:
    with pytest.raises(ValueError, match="required_env"):
        CapabilityEntry(
            capability_id="demo.live",
            name="Demo Live Capability",
            category=CapabilityCategory.REMOTE_ARTIFACT,
            tool_name="remote.demo",
            module="turing_research_plus.remote_artifacts",
            input_model="Input",
            output_model="Output",
            live_mode=True,
            fake_mode=True,
            docs=["docs/remote-artifact-integration.md"],
            tests=["tests/workflow/test_remote_artifact_integration_fake.py"],
        )


def test_capability_manifest_requires_unique_ids() -> None:
    entry = CapabilityEntry(
        capability_id="demo.capability",
        name="Demo Capability",
        category=CapabilityCategory.PLUGIN,
        module="turing_research_plus.plugins",
        input_model="DemoInput",
        output_model="DemoOutput",
        docs=["docs/plugin-architecture.md"],
        tests=["tests/unit/test_plugin_models.py"],
    )

    with pytest.raises(ValueError, match="unique"):
        CapabilityManifest(manifest_id="demo", capabilities=[entry, entry])

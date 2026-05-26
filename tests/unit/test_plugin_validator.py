from __future__ import annotations

from turing_research_plus.plugins.models import PluginSafetyLevel, PluginStatus
from turing_research_plus.plugins.validator import validate_plugin_manifest


def test_plugin_validator_rejects_python_entrypoint() -> None:
    report = validate_plugin_manifest(
        {
            "plugin_id": "unsafe_plugin",
            "name": "Unsafe Plugin",
            "version": "0.1.0",
            "type": "adapter",
            "entry_kind": "manifest-only",
            "capabilities": [
                {
                    "capability_id": "unsafe",
                    "name": "Unsafe",
                    "category": "adapter",
                    "description": "Unsafe entrypoint.",
                }
            ],
            "required_permissions": ["read_demo"],
            "config_schema": {},
            "inputs": ["DemoInput"],
            "outputs": ["DemoOutput"],
            "safety_level": "public-demo",
            "status": "disabled",
            "third_party": True,
            "executes_code": False,
            "python_entrypoint": "unsafe.module:main",
        }
    )

    assert report.valid is False
    assert report.status == PluginStatus.DISABLED
    assert report.safety_level == PluginSafetyLevel.DISABLED
    assert any("Python entrypoints" in issue.message for issue in report.issues)


def test_plugin_validator_accepts_manifest_only_disabled_plugin() -> None:
    report = validate_plugin_manifest(
        {
            "plugin_id": "safe_plugin",
            "name": "Safe Plugin",
            "version": "0.1.0",
            "type": "renderer",
            "entry_kind": "manifest-only",
            "capabilities": [
                {
                    "capability_id": "render_demo",
                    "name": "Render Demo",
                    "category": "renderer",
                    "description": "Render demo metadata.",
                }
            ],
            "required_permissions": ["read_demo"],
            "config_schema": {},
            "inputs": ["DemoInput"],
            "outputs": ["DemoOutput"],
            "safety_level": "public-demo",
            "status": "disabled",
            "third_party": True,
            "executes_code": False,
        }
    )

    assert report.valid is True
    assert report.executes_code is False
    assert report.loads_entrypoint is False

from __future__ import annotations

import pytest

from turing_research_plus.plugins.compat_report import (
    PluginCompatibilityMatrix,
    PluginCompatibilityReport,
    PluginCompatibilityStatus,
)


def test_plugin_compatibility_report_is_review_only() -> None:
    report = PluginCompatibilityReport(
        plugin_id="demo_plugin",
        status=PluginCompatibilityStatus.NEEDS_REVIEW,
        matrix=PluginCompatibilityMatrix(),
    )

    assert report.requires_human_review is True
    assert report.executes_plugin_code is False
    assert report.loads_entrypoint is False
    assert report.starts_mcp_server is False
    assert report.enables_plugin is False


def test_plugin_compatibility_report_rejects_execution_claim() -> None:
    with pytest.raises(ValueError, match="must not execute"):
        PluginCompatibilityReport(
            plugin_id="demo_plugin",
            status=PluginCompatibilityStatus.NEEDS_REVIEW,
            matrix=PluginCompatibilityMatrix(),
            executes_plugin_code=True,
        )


def test_plugin_compatibility_matrix_all_passed_property() -> None:
    matrix = PluginCompatibilityMatrix(
        manifest_schema_valid=True,
        capability_ids_valid=True,
        required_permissions_declared=True,
        safety_policy_satisfied=True,
        mcp_mapping_valid=True,
        docs_present=True,
        tests_declared=True,
        no_core_tool_override=True,
        no_old_project_naming=True,
        no_forbidden_permission=True,
    )

    assert matrix.all_passed is True

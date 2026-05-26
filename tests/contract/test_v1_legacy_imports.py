from __future__ import annotations

import importlib

LEGACY_IMPORTS = {
    "turing_research_plus": "PACKAGE_NAME",
    "turing_research_plus.workspace": "Workspace",
    "turing_research_plus.privacy": "PrivacyScanReport",
    "turing_research_plus.quality": "QualityReport",
    "turing_research_plus.project_template": "ResearchProjectTemplate",
    "turing_research_plus.paper_write": "PaperScaffold",
    "turing_research_plus.paper_review": "DeepReviewReport",
    "turing_research_plus.artifact_audit": "ArtifactAuditReport",
    "turing_research_plus.experiment_route": "ExperimentRouteSpec",
    "turing_research_plus.hard_gates": "HardGateValidationReport",
    "turing_research_plus.ui": "DashboardCard",
    "turing_research_plus.plugins": "PluginManifest",
    "turing_research_plus.benchmark": "BenchmarkReport",
}


def test_v1_legacy_imports_still_work() -> None:
    for module_name, symbol in LEGACY_IMPORTS.items():
        module = importlib.import_module(module_name)

        assert hasattr(module, symbol), f"{module_name} missing {symbol}"


def test_v1_legacy_plus_namespace_is_marked_as_compatibility_entry() -> None:
    plus = importlib.import_module("turing_research_plus")
    compat = importlib.import_module("turing_research_plus.compat")

    assert plus.PACKAGE_NAME == "turing_research_plus"
    assert compat.COMPATIBILITY_NAMESPACE == "turing_research_plus"
    assert "turing_research_core" in compat.TARGET_NAMESPACES

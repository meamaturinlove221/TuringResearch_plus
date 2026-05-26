from __future__ import annotations

import importlib

NEW_IMPORTS = {
    "turing_research_core": "Workspace",
    "turing_research_paper": "PaperScaffold",
    "turing_research_artifact": "ArtifactAuditReport",
    "turing_research_experiment": "ExperimentRouteSpec",
    "turing_research_dashboard": "DashboardCard",
    "turing_research_plugins": "PluginManifest",
    "turing_research_cases": "BenchmarkReport",
}


def test_v1_new_namespace_imports_work() -> None:
    for namespace, symbol in NEW_IMPORTS.items():
        module = importlib.import_module(namespace)

        assert module.NAMESPACE == namespace
        assert module.COMPATIBILITY_NAMESPACE == "turing_research_plus"
        assert hasattr(module, symbol), f"{namespace} missing {symbol}"


def test_v1_new_namespace_public_api_imports_work() -> None:
    for namespace, symbol in NEW_IMPORTS.items():
        module = importlib.import_module(f"{namespace}.public_api")

        assert module.NAMESPACE == namespace
        assert module.COMPATIBILITY_NAMESPACE == "turing_research_plus"
        assert hasattr(module, symbol), f"{namespace}.public_api missing {symbol}"


def test_v1_new_namespace_model_modules_import() -> None:
    for namespace in NEW_IMPORTS:
        module = importlib.import_module(f"{namespace}.models")

        assert module is not None

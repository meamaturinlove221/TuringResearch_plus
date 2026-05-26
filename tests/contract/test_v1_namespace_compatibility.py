from __future__ import annotations

import importlib

from turing_research_plus.compat import aliases_for_namespace, legacy_module_for

NAMESPACES = {
    "turing_research_core": "beta",
    "turing_research_paper": "experimental",
    "turing_research_artifact": "experimental",
    "turing_research_experiment": "beta",
    "turing_research_dashboard": "experimental",
    "turing_research_plugins": "experimental",
    "turing_research_cases": "experimental",
}

REPRESENTATIVE_SYMBOLS = {
    "turing_research_core": "Workspace",
    "turing_research_paper": "PaperScaffold",
    "turing_research_artifact": "ArtifactAuditReport",
    "turing_research_experiment": "ExperimentRouteSpec",
    "turing_research_dashboard": "DashboardCard",
    "turing_research_plugins": "PluginManifest",
    "turing_research_cases": "BenchmarkReport",
}


def test_v1_legacy_and_new_namespace_imports_are_available() -> None:
    plus = importlib.import_module("turing_research_plus")

    assert plus.PACKAGE_NAME == "turing_research_plus"

    for namespace in NAMESPACES:
        package = importlib.import_module(namespace)
        public_api = importlib.import_module(f"{namespace}.public_api")

        assert package.NAMESPACE == namespace
        assert public_api.NAMESPACE == namespace
        assert public_api.COMPATIBILITY_NAMESPACE == "turing_research_plus"


def test_v1_new_namespaces_expose_expected_stability() -> None:
    for namespace, stability in NAMESPACES.items():
        package = importlib.import_module(namespace)
        public_api = importlib.import_module(f"{namespace}.public_api")

        assert package.STABILITY == stability
        assert public_api.STABILITY == stability


def test_v1_new_namespace_facades_expose_representative_symbols() -> None:
    for namespace, symbol in REPRESENTATIVE_SYMBOLS.items():
        package = importlib.import_module(namespace)
        public_api = importlib.import_module(f"{namespace}.public_api")

        assert hasattr(package, symbol)
        assert hasattr(public_api, symbol)
        assert symbol in package.__all__
        assert symbol in public_api.__all__


def test_v1_compat_aliases_resolve_for_each_namespace() -> None:
    for namespace in NAMESPACES:
        aliases = aliases_for_namespace(namespace)

        assert aliases, f"missing aliases for {namespace}"
        for alias in aliases:
            assert alias.target_namespace == namespace
            assert alias.legacy_module.startswith("turing_research_plus.") or (
                alias.legacy_module.startswith("examples/")
            )

    assert legacy_module_for("turing_research_core", "workspace") == (
        "turing_research_plus.workspace"
    )

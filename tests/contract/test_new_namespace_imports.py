from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NEW_NAMESPACES = [
    "turing_research_core",
    "turing_research_paper",
    "turing_research_artifact",
    "turing_research_experiment",
    "turing_research_dashboard",
    "turing_research_plugins",
    "turing_research_cases",
]


def test_new_namespace_packages_import() -> None:
    for namespace in NEW_NAMESPACES:
        module = importlib.import_module(namespace)
        public_api = importlib.import_module(f"{namespace}.public_api")
        models = importlib.import_module(f"{namespace}.models")

        assert module.NAMESPACE == namespace
        assert public_api.NAMESPACE == namespace
        assert public_api.COMPATIBILITY_NAMESPACE == "turing_research_plus"
        assert isinstance(public_api.PUBLIC_MODULE_ALIASES, dict)
        assert models is not None


def test_new_namespace_public_api_exports_representative_symbols() -> None:
    expectations = {
        "turing_research_core": "Workspace",
        "turing_research_paper": "PaperScaffold",
        "turing_research_artifact": "ArtifactAuditReport",
        "turing_research_experiment": "ExperimentRouteSpec",
        "turing_research_dashboard": "DashboardCard",
        "turing_research_plugins": "PluginManifest",
        "turing_research_cases": "BenchmarkReport",
    }

    for namespace, symbol in expectations.items():
        public_api = importlib.import_module(f"{namespace}.public_api")
        assert hasattr(public_api, symbol)


def test_package_discovery_includes_new_namespaces() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    include = metadata["tool"]["setuptools"]["packages"]["find"]["include"]

    for namespace in NEW_NAMESPACES:
        assert f"{namespace}*" in include


def test_mypy_package_list_includes_new_namespaces() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    packages = metadata["tool"]["mypy"]["packages"]

    for namespace in NEW_NAMESPACES:
        assert namespace in packages

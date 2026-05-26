from __future__ import annotations

import importlib

from turing_research_plus.compat import (
    COMPATIBILITY_NAMESPACE,
    TARGET_NAMESPACES,
    aliases_for_namespace,
    legacy_module_for,
    list_module_aliases,
)


def test_legacy_plus_namespace_still_imports() -> None:
    plus = importlib.import_module("turing_research_plus")

    assert plus.PACKAGE_NAME == "turing_research_plus"


def test_compat_alias_registry_lists_target_namespaces() -> None:
    assert COMPATIBILITY_NAMESPACE == "turing_research_plus"
    assert set(TARGET_NAMESPACES) == {
        "turing_research_core",
        "turing_research_paper",
        "turing_research_artifact",
        "turing_research_experiment",
        "turing_research_dashboard",
        "turing_research_plugins",
        "turing_research_cases",
    }
    assert list_module_aliases()


def test_aliases_resolve_to_legacy_modules() -> None:
    assert legacy_module_for("turing_research_core", "workspace") == (
        "turing_research_plus.workspace"
    )
    assert legacy_module_for("turing_research_dashboard", "ui") == "turing_research_plus.ui"
    assert legacy_module_for("turing_research_plugins", "plugins") == (
        "turing_research_plus.plugins"
    )
    assert legacy_module_for("turing_research_core", "unknown") is None


def test_alias_targets_and_legacy_modules_import() -> None:
    for alias in list_module_aliases():
        assert importlib.import_module(alias.target_namespace)
        if alias.legacy_module.startswith("turing_research_plus."):
            assert importlib.import_module(alias.legacy_module)


def test_aliases_for_namespace_are_scoped() -> None:
    aliases = aliases_for_namespace("turing_research_core")

    assert aliases
    assert {alias.target_namespace for alias in aliases} == {"turing_research_core"}

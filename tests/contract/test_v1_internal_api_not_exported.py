from __future__ import annotations

import importlib

PUBLIC_APIS = [
    "turing_research_core.public_api",
    "turing_research_paper.public_api",
    "turing_research_artifact.public_api",
    "turing_research_experiment.public_api",
    "turing_research_dashboard.public_api",
    "turing_research_plugins.public_api",
    "turing_research_cases.public_api",
]

INTERNAL_TOKENS = (
    "internal",
    "fixture",
    "template_helper",
    "live_client",
    "dynamic_import",
    "sandbox_probe",
    "private",
    "raw_data",
)


def test_public_api_all_does_not_export_internal_helper_names() -> None:
    offenders: list[str] = []

    for module_name in PUBLIC_APIS:
        module = importlib.import_module(module_name)
        for exported in module.__all__:
            lowered = exported.lower()
            if any(token in lowered for token in INTERNAL_TOKENS):
                offenders.append(f"{module_name}:{exported}")

    assert offenders == []


def test_public_api_modules_do_not_export_dunder_private_names() -> None:
    offenders: list[str] = []

    for module_name in PUBLIC_APIS:
        module = importlib.import_module(module_name)
        for exported in module.__all__:
            if exported.startswith("_"):
                offenders.append(f"{module_name}:{exported}")

    assert offenders == []


def test_public_api_imports_do_not_execute_plugin_or_live_side_effects() -> None:
    for module_name in PUBLIC_APIS:
        module = importlib.import_module(module_name)

        assert module.COMPATIBILITY_NAMESPACE == "turing_research_plus"
        assert hasattr(module, "PUBLIC_MODULE_ALIASES")

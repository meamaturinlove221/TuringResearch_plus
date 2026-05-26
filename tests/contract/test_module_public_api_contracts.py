from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

API_CONTRACTS = [
    ROOT / "contracts" / "core_api.yaml",
    ROOT / "contracts" / "paper_api.yaml",
    ROOT / "contracts" / "artifact_api.yaml",
    ROOT / "contracts" / "experiment_api.yaml",
    ROOT / "contracts" / "dashboard_api.yaml",
    ROOT / "contracts" / "plugin_api.yaml",
    ROOT / "contracts" / "case_api.yaml",
]

REQUIRED_FIELDS = {
    "module_name",
    "purpose",
    "public_models",
    "public_functions_tools",
    "input_schema",
    "output_schema",
    "stability",
    "internal_only_modules",
    "deprecated_aliases",
    "tests",
    "docs",
}

ALLOWED_STABILITY = {"experimental", "beta", "stable", "internal"}


def field_value(text: str, field: str) -> str | None:
    match = re.search(rf"^{field}:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1) if match else None


def test_module_api_contract_files_exist() -> None:
    missing = [str(path.relative_to(ROOT)) for path in API_CONTRACTS if not path.exists()]

    assert missing == []


def test_module_api_contracts_have_required_fields() -> None:
    offenders: list[str] = []

    for path in API_CONTRACTS:
        text = path.read_text(encoding="utf-8")
        for field in REQUIRED_FIELDS:
            if not re.search(rf"^{field}:", text, re.MULTILINE):
                offenders.append(f"{path.relative_to(ROOT)} missing {field}")

    assert offenders == []


def test_module_api_contract_stability_values_are_known() -> None:
    offenders: list[str] = []

    for path in API_CONTRACTS:
        text = path.read_text(encoding="utf-8")
        stability = field_value(text, "stability")
        if stability not in ALLOWED_STABILITY:
            offenders.append(f"{path.relative_to(ROOT)} invalid stability {stability}")

    assert offenders == []


def test_experimental_contracts_are_not_marked_stable() -> None:
    stable_contracts = []

    for path in API_CONTRACTS:
        text = path.read_text(encoding="utf-8")
        if field_value(text, "stability") == "stable":
            stable_contracts.append(str(path.relative_to(ROOT)))

    assert stable_contracts == []


def test_contracts_keep_plus_compatibility_namespace() -> None:
    offenders: list[str] = []

    for path in API_CONTRACTS:
        text = path.read_text(encoding="utf-8")
        if field_value(text, "current_compatibility_namespace") != "turing_research_plus":
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []


def test_contracts_reference_docs_and_tests() -> None:
    offenders: list[str] = []

    for path in API_CONTRACTS:
        text = path.read_text(encoding="utf-8")
        if "tests/contract/test_module_public_api_contracts.py" not in text:
            offenders.append(f"{path.relative_to(ROOT)} missing contract test reference")
        if "docs/module-public-api-contracts.md" not in text:
            offenders.append(f"{path.relative_to(ROOT)} missing docs reference")

    assert offenders == []

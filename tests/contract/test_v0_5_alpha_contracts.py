from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_v0_5_alpha_docs_exist() -> None:
    required = [
        "docs/v0.5.0-alpha-integration-report.md",
        "docs/v0.5.0-alpha-known-limitations.md",
        "docs/v0.5.0-alpha-release-readiness.md",
        "docs/lightweight-dashboard-ui.md",
        "docs/advisor-pdf-pptx-export.md",
        "docs/project-template-generator.md",
        "docs/packaging-polish.md",
        "docs/public-demo-suite.md",
    ]

    for relative_path in required:
        assert (ROOT / relative_path).exists()


def test_v0_5_alpha_contracts_exist() -> None:
    required = [
        "contracts/lightweight_dashboard.yaml",
        "contracts/advisor_export.yaml",
        "contracts/project_template.yaml",
    ]

    for relative_path in required:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        assert "status: implemented_minimal" in text
        assert "network_behavior: no_network" in text


def test_v0_5_alpha_packaging_surface_is_stable() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    scripts = project["scripts"]

    assert project["name"] == "turingresearch-plus"
    assert scripts["turingresearch-plus"] == "turing_research.mcp_server:main"
    assert scripts["turingresearch-plus-mcp"] == "turing_research.mcp_server:main"


def test_v0_5_alpha_mcp_example_disables_live_tests() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]

    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert env["APIFY_TOKEN"] == ""
    assert env["OPENAI_API_KEY"] == ""
    assert env["GITHUB_TOKEN"] == ""


def test_v0_5_alpha_report_states_boundaries() -> None:
    report = (ROOT / "docs" / "v0.5.0-alpha-integration-report.md").read_text(
        encoding="utf-8"
    )

    assert "GO WITH REVIEW" in report
    assert "No real PDF or PPTX is generated" in report
    assert "SparseConv3D success remains not established" in report
    assert "No legacy project naming" in report

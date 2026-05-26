from __future__ import annotations

import importlib
import json
import tomllib
from pathlib import Path

from tests.workflow.test_v1_benchmark_replay import load_v1_public_demo_scenario

from turing_research_plus.benchmark.replay_runner import run_benchmark_scenario

ROOT = Path(__file__).resolve().parents[2]

NAMESPACES = [
    "turing_research_plus",
    "turing_research_core",
    "turing_research_paper",
    "turing_research_artifact",
    "turing_research_experiment",
    "turing_research_dashboard",
    "turing_research_plugins",
    "turing_research_cases",
]


def test_v1_api_install_chain_imports_without_live_side_effects() -> None:
    for namespace in NAMESPACES:
        module = importlib.import_module(namespace)
        assert module is not None

    for namespace in NAMESPACES[1:]:
        public_api = importlib.import_module(f"{namespace}.public_api")
        assert public_api.COMPATIBILITY_NAMESPACE == "turing_research_plus"
        assert public_api.NAMESPACE == namespace


def test_v1_cli_mcp_fake_default_config_supports_quickstart() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["turingresearch-plus"]
    env = server["env"]

    assert pyproject["project"]["name"] == "turingresearch-plus"
    assert scripts["turingresearch-plus-mcp"] == "turing_research.mcp_server:main"
    assert server["command"] == "turingresearch-plus-mcp"
    assert server["args"] == ["--manifest"]
    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"
    assert env["OPENAI_API_KEY"] == ""


def test_v1_public_quickstart_and_demo_replay_stay_aligned() -> None:
    quickstart = (ROOT / "docs" / "v1.0.0-quickstart.md").read_text(encoding="utf-8")
    demo_manifest = (ROOT / "examples" / "public_demo" / "demo_manifest.yaml").read_text(
        encoding="utf-8"
    )
    report = run_benchmark_scenario(load_v1_public_demo_scenario())

    required_terms = [
        "public demo",
        "evidence ledger",
        "dashboard",
        "advisor markdown bundle",
        "related work",
        "live adapters are disabled by default",
    ]
    for term in required_terms:
        assert term in quickstart.lower()

    assert "status: demo-only" in demo_manifest
    assert "requires_human_review: true" in demo_manifest
    assert "generated_observed_results: false" in demo_manifest
    assert report.status == "pass"
    assert report.missing_outputs == []
    assert report.regression_flags == []


def test_v1_api_install_integration_reports_exist_and_record_boundaries() -> None:
    required = [
        ROOT / "docs" / "v1.0.0-api-install-integration-report.md",
        ROOT / "docs" / "v1.0.0-api-install-known-limitations.md",
    ]
    for path in required:
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "no network" in text or "network" in text
        assert "no real experiment" in text
        assert "no unknown plugin" in text or "unknown plugin" in text
        assert "human review" in text

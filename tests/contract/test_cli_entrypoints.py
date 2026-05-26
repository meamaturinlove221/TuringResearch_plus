from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_cli_entrypoints_are_declared_and_resolvable() -> None:
    project = pyproject()["project"]
    assert isinstance(project, dict)
    scripts = project["scripts"]
    assert isinstance(scripts, dict)

    expected = {
        "turingresearch-plus": "turing_research.mcp_server:main",
        "turingresearch-plus-mcp": "turing_research.mcp_server:main",
        "turingresearch-session": "turing_research_plus.session_runtime.cli:main",
    }
    assert expected.items() <= scripts.items()

    for target in scripts.values():
        module_name, function_name = target.split(":", 1)
        module = importlib.import_module(module_name)
        assert callable(getattr(module, function_name))


def test_cli_reference_documents_entrypoints() -> None:
    text = (ROOT / "docs" / "cli-reference.md").read_text(encoding="utf-8")

    assert "package name: `turingresearch-plus`" in text
    assert "`turingresearch-plus`" in text
    assert "`turingresearch-plus-mcp`" in text
    assert "`turingresearch-session`" in text
    assert "turing_research.mcp_server:main" in text
    assert "turing_research_plus.session_runtime.cli:main" in text
    assert "do not require live API keys" in text or "do not require live API" in text


def test_env_example_uses_current_package_prefix_only() -> None:
    text = (ROOT / ".env.example").read_text(encoding="utf-8")

    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in text
    assert "TURINGRESEARCH_CACHE=" in text
    assert "TURINGRESEARCH_VAULT_ROOT=" in text
    prior_env_prefix = "TULING" + "_RESEARCH"
    assert prior_env_prefix not in text

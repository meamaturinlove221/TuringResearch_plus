from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _pyproject() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_v1_package_name_and_cli_entrypoints_are_stable() -> None:
    project = _pyproject()["project"]
    assert isinstance(project, dict)
    scripts = project["scripts"]
    assert isinstance(scripts, dict)

    assert project["name"] == "turingresearch-plus"
    assert scripts["turingresearch-plus"] == "turing_research.mcp_server:main"
    assert scripts["turingresearch-plus-mcp"] == "turing_research.mcp_server:main"


def test_v1_cli_entrypoint_targets_are_importable() -> None:
    scripts = _pyproject()["project"]["scripts"]
    assert isinstance(scripts, dict)

    for target in scripts.values():
        module_name, function_name = target.split(":", 1)
        module = importlib.import_module(module_name)
        assert callable(getattr(module, function_name))


def test_v1_cli_docs_name_commands_and_fake_boundary() -> None:
    docs = [
        ROOT / "docs" / "cli-reference.md",
        ROOT / "docs" / "install.md",
        ROOT / "docs" / "quickstart.md",
        ROOT / "docs" / "v1.0.0-cli-mcp-sanity.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in docs)

    assert "turingresearch-plus" in text
    assert "turingresearch-plus-mcp" in text
    assert "turing_research.mcp_server:main" in text
    assert "fake" in text.lower()
    assert "live adapters" in text.lower() or "live mode" in text.lower()

from __future__ import annotations

import importlib
import tomllib
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def resolve_entry_point(target: str) -> Callable[..., object]:
    module_name, function_name = target.split(":", 1)
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)
    assert callable(function)
    return function


def test_console_scripts_point_to_mcp_server_main() -> None:
    metadata = pyproject()
    project = metadata["project"]
    assert isinstance(project, dict)
    scripts = project["scripts"]
    assert isinstance(scripts, dict)

    assert scripts["turingresearch-plus"] == "turing_research.mcp_server:main"
    assert scripts["turingresearch-plus-mcp"] == "turing_research.mcp_server:main"

    for target in scripts.values():
        assert resolve_entry_point(target).__name__ == "main"


def test_mcp_entry_point_can_emit_manifest_without_network(capsys) -> None:
    main = resolve_entry_point("turing_research.mcp_server:main")

    result = main(["--manifest"])
    captured = capsys.readouterr()

    assert result == 0
    assert captured.err == ""
    assert '"server_name": "turingresearch-plus"' in captured.out
    assert '"transport": "stdio"' in captured.out


def test_optional_extras_cover_dev_pdf_mcp_and_all() -> None:
    metadata = pyproject()
    project = metadata["project"]
    assert isinstance(project, dict)
    extras = project["optional-dependencies"]
    assert isinstance(extras, dict)

    assert {"dev", "pdf", "mcp", "all"} <= set(extras)
    assert "pytest>=8.0" in extras["dev"]
    assert "pytest-asyncio>=0.23" in extras["dev"]
    assert "pymupdf>=1.24" in extras["pdf"]
    assert "httpx>=0.27" in extras["mcp"]
    assert "typer>=0.12" in extras["mcp"]
    assert "rich>=13.7" in extras["mcp"]
    assert "pymupdf>=1.24" in extras["all"]

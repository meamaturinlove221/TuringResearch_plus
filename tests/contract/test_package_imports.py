from __future__ import annotations

import importlib
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_core_and_plus_packages_import() -> None:
    core = importlib.import_module("tuling_research")
    plus = importlib.import_module("tuling_research_plus")
    pdf = importlib.import_module("tuling_research.pdf")

    assert core.__version__ == "0.1.0"
    assert core.PACKAGE_NAME == "tuling_research"
    assert plus.__version__ == "0.1.0"
    assert plus.PACKAGE_NAME == "tuling_research_plus"
    assert hasattr(pdf, "PDFMarkdownOutput")


def test_mcp_server_module_import_is_safe(capsys) -> None:
    sys.modules.pop("tuling_research.mcp_server", None)

    module = importlib.import_module("tuling_research.mcp_server")
    captured = capsys.readouterr()

    assert module.MCP_SERVER_NAME == "tulingresearch-plus"
    assert callable(module.main)
    assert captured.out == ""
    assert captured.err == ""


def test_package_metadata_is_readable_from_pyproject() -> None:
    metadata = pyproject()
    project = metadata["project"]
    assert isinstance(project, dict)

    assert project["name"] == "tulingresearch-plus"
    assert project["requires-python"] == ">=3.11"
    assert "pydantic>=2.7" in project["dependencies"]
    assert "pydantic-settings>=2.2" in project["dependencies"]
    assert "httpx>=0.27" in project["dependencies"]


def test_package_discovery_covers_core_and_plus_packages() -> None:
    metadata = pyproject()
    tool = metadata["tool"]
    assert isinstance(tool, dict)
    setuptools = tool["setuptools"]
    assert isinstance(setuptools, dict)
    find = setuptools["packages"]["find"]
    assert isinstance(find, dict)

    assert find["where"] == ["src"]
    assert "tuling_research*" in find["include"]
    assert "tuling_research_plus*" in find["include"]

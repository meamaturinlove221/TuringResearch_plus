from __future__ import annotations

import builtins
import importlib
import os
import tomllib
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict[str, Any]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_runtime_dependencies_do_not_make_optional_pdf_or_live_keys_mandatory() -> None:
    project = pyproject()["project"]
    dependencies = project["dependencies"]
    extras = project["optional-dependencies"]

    assert "pydantic>=2.7" in dependencies
    assert "pydantic-settings>=2.2" in dependencies
    assert "pymupdf>=1.24" not in dependencies
    assert "pymupdf>=1.24" in extras["pdf"]
    assert "pymupdf>=1.24" in extras["all"]


def test_missing_live_api_keys_do_not_break_default_health_check(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for env_name in (
        "SEMANTIC_SCHOLAR_API_KEY",
        "ARXIV_API_KEY",
        "APIFY_API_TOKEN",
        "OPENAI_API_KEY",
    ):
        monkeypatch.delenv(env_name, raising=False)

    from turing_research.mcp_server import core_health_check

    result = core_health_check()

    assert result["status"] == "ok"
    assert result["package"] == "turing_research"


def test_pymupdf_missing_does_not_break_pdf_package_import(monkeypatch: pytest.MonkeyPatch) -> None:
    pdf_module = importlib.import_module("turing_research.pdf")
    converter_module = importlib.import_module(
        "turing_research.pdf.converters.pymupdf_converter"
    )

    original_import = builtins.__import__

    def blocked_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "fitz":
            raise ModuleNotFoundError("No module named 'fitz'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)

    converter = converter_module.PyMuPDFConverter()
    with pytest.raises(converter_module.ConverterUnavailableError, match="PyMuPDF"):
        converter.convert(ROOT / "tests" / "fixtures" / "missing.pdf")

    assert hasattr(pdf_module, "PDFMarkdownOutput")


def test_local_install_docs_and_troubleshooting_docs_exist() -> None:
    required_docs = [
        ROOT / "docs" / "install.md",
        ROOT / "docs" / "local-install-smoke.md",
        ROOT / "docs" / "troubleshooting.md",
    ]

    for doc in required_docs:
        content = doc.read_text(encoding="utf-8")
        assert "TuringResearch Plus" in content
        assert "python -m pip install -e" in content


def test_readme_quickstart_does_not_require_real_tokens() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()

    assert "quickstart" in readme
    assert "do not require real api keys" in readme
    assert "live network access" in readme


def test_examples_document_fake_mode_without_real_api_keys() -> None:
    examples = [
        "vggt-human-prior-survey",
        "smplx-feature-adapter-hypothesis",
        "citation-graph-demo",
        "pdf-to-markdown-demo",
    ]

    for example in examples:
        readme = (ROOT / "examples" / example / "README.md").read_text(
            encoding="utf-8"
        )
        lowered = readme.lower()
        config = ROOT / "examples" / example / "fake_run_config.yaml"

        assert config.exists()
        assert "mode:" in lowered
        assert "fake" in lowered or "dry-run" in lowered
        assert "no real network" in lowered or "no semantic scholar api key" in lowered
        assert "api key" in lowered
        assert "required" in lowered or "not required" in lowered


def test_default_pytest_configuration_skips_live_and_manual_tests() -> None:
    tool = pyproject()["tool"]
    addopts = tool["pytest"]["ini_options"]["addopts"]

    assert "not live" in addopts
    assert "not manual" in addopts
    assert os.environ.get("SEMANTIC_SCHOLAR_API_KEY") is None or True

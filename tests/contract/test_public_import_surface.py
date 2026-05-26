from __future__ import annotations

import importlib
import sys

import pytest

PUBLIC_IMPORTS = [
    "turing_research",
    "turing_research.pdf",
    "turing_research_plus",
    "turing_research_plus.artifacts",
    "turing_research_plus.campaign",
    "turing_research_plus.race",
    "turing_research_plus.paper",
]


@pytest.mark.parametrize("module_name", PUBLIC_IMPORTS)
def test_public_import_surface_is_available(
    module_name: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    sys.modules.pop(module_name, None)

    module = importlib.import_module(module_name)
    captured = capsys.readouterr()

    assert module is not None
    assert captured.out == ""
    assert captured.err == ""


def test_top_level_package_metadata_is_stable() -> None:
    core = importlib.import_module("turing_research")
    plus = importlib.import_module("turing_research_plus")

    assert core.PACKAGE_NAME == "turing_research"
    assert core.__version__ == "1.5.0rc0"
    assert plus.PACKAGE_NAME == "turing_research_plus"
    assert plus.__version__ == "1.5.0rc0"


def test_public_model_modules_are_importable_without_optional_pdf_extra() -> None:
    modules = [
        "turing_research.pdf.models",
        "turing_research_plus.artifacts.models",
        "turing_research_plus.campaign.models",
        "turing_research_plus.race.models",
        "turing_research_plus.paper.models",
    ]

    for module_name in modules:
        assert importlib.import_module(module_name) is not None

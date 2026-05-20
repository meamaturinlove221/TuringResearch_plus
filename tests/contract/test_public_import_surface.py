from __future__ import annotations

import importlib
import sys

import pytest

PUBLIC_IMPORTS = [
    "tuling_research",
    "tuling_research.pdf",
    "tuling_research_plus",
    "tuling_research_plus.artifacts",
    "tuling_research_plus.campaign",
    "tuling_research_plus.race",
    "tuling_research_plus.paper",
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
    core = importlib.import_module("tuling_research")
    plus = importlib.import_module("tuling_research_plus")

    assert core.PACKAGE_NAME == "tuling_research"
    assert core.__version__ == "0.1.0"
    assert plus.PACKAGE_NAME == "tuling_research_plus"
    assert plus.__version__ == "0.1.0"


def test_public_model_modules_are_importable_without_optional_pdf_extra() -> None:
    modules = [
        "tuling_research.pdf.models",
        "tuling_research_plus.artifacts.models",
        "tuling_research_plus.campaign.models",
        "tuling_research_plus.race.models",
        "tuling_research_plus.paper.models",
    ]

    for module_name in modules:
        assert importlib.import_module(module_name) is not None

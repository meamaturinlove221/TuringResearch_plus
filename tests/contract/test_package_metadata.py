from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_package_metadata_matches_public_names() -> None:
    project = pyproject()["project"]
    assert isinstance(project, dict)

    assert project["name"] == "turingresearch-plus"
    assert project["version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert project["requires-python"] == ">=3.11"


def test_package_import_names_are_documented() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs" / "install.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "packaging-polish.md").read_text(encoding="utf-8"),
        ]
    )

    assert "`turingresearch-plus`" in docs
    assert "`turing_research`" in docs
    assert "`turing_research_plus`" in docs


def test_example_configs_have_no_real_key_values() -> None:
    files = [
        ROOT / ".env.example",
        ROOT / ".mcp.example.json",
    ]
    forbidden_value = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    prior_display_name = "Tuling" + "Research"
    prior_env_prefix = "TULING" + "_RESEARCH"

    for path in files:
        text = path.read_text(encoding="utf-8")
        assert not forbidden_value.search(text)
        assert prior_display_name not in text
        assert prior_env_prefix not in text


def test_packaging_polish_docs_keep_live_disabled_by_default() -> None:
    text = (ROOT / "docs" / "packaging-polish.md").read_text(encoding="utf-8")

    assert "Live adapters disabled by default" in text
    assert "Live tests skipped by default" in text
    assert "No PyPI publish" in text

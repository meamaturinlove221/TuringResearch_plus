from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def pyproject() -> dict[str, object]:
    return tomllib.loads(read_text("pyproject.toml"))


def project_metadata() -> dict[str, object]:
    project = pyproject()["project"]
    assert isinstance(project, dict)
    return project


def test_project_metadata_uses_public_display_name() -> None:
    project = project_metadata()
    readme = read_text("README.md")

    assert readme.startswith("# TuringResearch")
    assert project["description"] == "TuringResearch local-first research workflow engine."
    legacy_public_name = "TuringResearch" + " Plus"
    assert legacy_public_name not in project["description"]


def test_distribution_name_is_documented_compatibility_surface() -> None:
    project = project_metadata()
    readiness = read_text("docs/packaging-readiness-v1.6.md")
    audit = read_text("docs/package-metadata-audit.md")

    assert project["name"] == "turingresearch-plus"
    assert "`turingresearch-plus`" in readiness
    assert "`turing_research_plus`" in readiness
    assert "compatibility distribution name" in audit
    assert "NO-GO for PyPI publication" in audit


def test_version_metadata_matches_version_file() -> None:
    project = project_metadata()
    version = read_text("VERSION").strip()

    assert project["version"] == version
    assert version == "1.5.0rc0"
    assert "Current package metadata reports `1.5.0rc0`" in read_text("README.md")


def test_license_authors_and_python_requirement_are_present() -> None:
    project = project_metadata()

    assert project["requires-python"] == ">=3.11"
    assert project["readme"] == "README.md"
    assert project["license"] == {"text": "Proprietary"}
    assert project["authors"] == [{"name": "TuringResearch"}]
    assert "final license decision" in read_text("docs/package-release-non-goals.md")


def test_entry_points_dependencies_and_extras_are_declared() -> None:
    metadata = pyproject()
    project = project_metadata()

    scripts = project["scripts"]
    assert isinstance(scripts, dict)
    assert scripts["turingresearch-plus"] == "turing_research.mcp_server:main"
    assert scripts["turingresearch-plus-mcp"] == "turing_research.mcp_server:main"
    assert scripts["turingresearch-session"] == "turing_research_plus.session_runtime.cli:main"

    dependencies = project["dependencies"]
    assert isinstance(dependencies, list)
    assert {"pydantic>=2.7", "pydantic-settings>=2.2", "httpx>=0.27"}.issubset(
        set(dependencies)
    )

    optional_dependencies = project["optional-dependencies"]
    assert isinstance(optional_dependencies, dict)
    assert {"dev", "pdf", "mcp", "all"}.issubset(optional_dependencies)

    find = metadata["tool"]["setuptools"]["packages"]["find"]
    assert "turing_research*" in find["include"]
    assert "turing_research_plus*" in find["include"]


def test_readme_install_quickstart_are_public_safe() -> None:
    combined = "\n".join(
        [
            read_text("README.md"),
            read_text("docs/install.md"),
            read_text("docs/quickstart.md"),
        ]
    )

    legacy_misspelling = "Tuling" + "Research"
    legacy_public_name = "TuringResearch" + " Plus"
    forbidden_patterns = [
        re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
        re.compile(r"ghp_[A-Za-z0-9_]{12,}"),
        re.compile(r"https://" + r"github\.com/[^`\s<>()]+/turingresearch-(?:vggt-case|examples)"),
    ]

    assert legacy_misspelling not in combined
    assert f"{legacy_public_name} Install Guide" not in combined
    assert "automatically complete research" in combined
    assert "No default live networking" in combined or "default to live networking" in combined

    for pattern in forbidden_patterns:
        assert not pattern.search(combined)


def test_round_378_docs_record_release_non_goals() -> None:
    docs = "\n".join(
        [
            read_text("docs/packaging-readiness-v1.6.md"),
            read_text("docs/package-metadata-audit.md"),
            read_text("docs/package-release-non-goals.md"),
        ]
    )

    assert "No PyPI publish" in docs
    assert "No tag creation" in docs
    assert "No package distribution rename" in docs
    assert "No import namespace removal" in docs
    assert "No live adapter execution" in docs

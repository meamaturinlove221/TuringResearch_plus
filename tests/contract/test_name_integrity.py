from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_EXTENSIONS = {".py", ".md", ".yaml", ".toml"}
OLD_NAME_ALLOWED_FILES = {
    Path("docs/rename-tuling-to-turing-report.md"),
    Path("docs/round38-pre-rename-checkpoint.md"),
    Path("docs/round38-rename-risk-register.md"),
    Path("lanes/18_round38_pre_rename_checkpoint.md"),
}
IGNORED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "turingresearch_plus.egg-info",
}


def iter_text_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_EXTENSIONS
        and not (set(path.parts) & IGNORED_PARTS)
    )


def forbidden_exact_terms() -> list[str]:
    bad_prefix = "neo" + "cortica"
    return [
        bad_prefix + "-plus",
        bad_prefix + "_plus",
        "src/" + bad_prefix + "_plus",
        "import " + bad_prefix + "_plus",
        "Neo" + "cortica++",
    ]


def forbidden_skill_pattern() -> re.Pattern[str]:
    bad_prefix = "neo" + "cortica"
    return re.compile(rf"\b{bad_prefix}-[A-Za-z0-9_-]+\b")


def old_name_terms() -> list[str]:
    display = "Tul" + "ingResearch"
    root = display + "_plus"
    core = "tul" + "ing_research"
    plus = core + "_plus"
    slug = "tul" + "ingresearch"
    return [
        display,
        root,
        core,
        plus,
        slug + "-plus",
        slug + "-",
    ]


def test_repository_text_does_not_contain_forbidden_project_names() -> None:
    offenders: list[str] = []
    skill_pattern = forbidden_skill_pattern()
    for path in iter_text_files():
        content = path.read_text(encoding="utf-8")
        for term in forbidden_exact_terms():
            if term in content:
                offenders.append(f"{path.relative_to(ROOT)} contains forbidden legacy term")
        for match in skill_pattern.finditer(content):
            if match.group(0) != ("neo" + "cortica"):
                offenders.append(f"{path.relative_to(ROOT)} contains forbidden legacy skill name")

    assert offenders == []


def test_prior_project_names_only_appear_in_rename_checkpoint_docs() -> None:
    offenders: list[str] = []
    for path in iter_text_files():
        relative = path.relative_to(ROOT)
        if relative in OLD_NAME_ALLOWED_FILES:
            continue
        content = path.read_text(encoding="utf-8")
        for term in old_name_terms():
            if term in content:
                offenders.append(f"{relative} contains prior project name term")

    assert offenders == []


def test_required_turingresearch_names_are_present_in_project_metadata() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    mcp_docs = (ROOT / "docs" / "mcp-tools.md").read_text(encoding="utf-8")

    assert "TuringResearch Plus" in agents
    assert "TuringResearch/TuringResearch_plus" in agents
    assert "turing_research" in pyproject
    assert "turing_research_plus" in pyproject
    assert "turingresearch-plus" in pyproject
    assert "turingresearch-plus" in mcp_docs


def test_python_imports_do_not_reference_legacy_or_unknown_local_packages() -> None:
    bad_prefix = "neo" + "cortica"
    allowed_local_roots = {"turing_research", "turing_research_plus"}
    offenders: list[str] = []

    for path in sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            module_name: str | None = None
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    if module_name.startswith(bad_prefix):
                        offenders.append(f"{path.relative_to(ROOT)} imports legacy package")
            elif isinstance(node, ast.ImportFrom) and node.module:
                module_name = node.module
                if module_name.startswith(bad_prefix):
                    offenders.append(f"{path.relative_to(ROOT)} imports legacy package")

                if module_name.startswith("src."):
                    offenders.append(f"{path.relative_to(ROOT)} imports via src package path")

            if module_name and module_name.startswith("tuling_"):
                root = module_name.split(".", 1)[0]
                if root not in allowed_local_roots:
                    offenders.append(
                        f"{path.relative_to(ROOT)} imports unknown local package {root}"
                    )

    assert offenders == []

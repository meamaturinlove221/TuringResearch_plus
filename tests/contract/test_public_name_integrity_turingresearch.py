from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PUBLIC_ENTRY_FILES = [
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "install.md",
    ROOT / "docs" / "local-install-smoke.md",
    ROOT / "docs" / "faq.md",
    ROOT / "docs" / "examples.md",
    ROOT / "docs" / "docs-index.md",
    ROOT / "docs" / "mcp-tools.md",
    ROOT / "docs" / "troubleshooting.md",
    ROOT / "docs" / "public-showcase.md",
    ROOT / ".mcp.example.json",
    ROOT / "pyproject.toml",
    ROOT / "CHANGELOG.md",
    ROOT / "VERSION",
]

PUBLIC_TREES = [
    ROOT / "docs-site",
    ROOT / "examples",
    ROOT / "split_ready",
    ROOT / "split_manual",
]

TEXT_SUFFIXES = {".css", ".html", ".json", ".md", ".toml", ".txt", ".yaml", ".yml"}

COMPATIBILITY_TERMS = [
    "turingresearch-plus",
    "turingresearch-plus-mcp",
    "turing_research_plus",
    "src/turing_research_plus/",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _iter_public_files() -> list[Path]:
    files = {path.resolve() for path in PUBLIC_ENTRY_FILES if path.exists()}
    for tree in PUBLIC_TREES:
        if not tree.exists():
            continue
        for path in tree.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                files.add(path.resolve())
    return sorted(files)


def _prior_project_terms() -> list[str]:
    display = "Tul" + "ingResearch"
    return [
        display,
        display + "_plus",
        ("tul" + "ingresearch") + "-plus",
        ("tul" + "ing_research") + "_plus",
    ]


def test_public_front_door_uses_turingresearch_brand() -> None:
    assert _read(ROOT / "README.md").splitlines()[0] == "# TuringResearch"
    assert "TuringResearch helps researchers" in _read(ROOT / "README.md")
    assert "# TuringResearch Docs" in _read(ROOT / "docs" / "README.md")
    assert "# TuringResearch Install Guide" in _read(ROOT / "docs" / "install.md")
    assert "# TuringResearch FAQ" in _read(ROOT / "docs" / "faq.md")
    assert "# TuringResearch Examples" in _read(ROOT / "examples" / "README.md")
    assert "TuringResearch local-first MCP server" in _read(ROOT / ".mcp.example.json")
    assert "description = \"TuringResearch MCP-first" in _read(ROOT / "pyproject.toml")


def test_public_files_do_not_use_plus_as_display_brand() -> None:
    offenders: list[str] = []
    for path in _iter_public_files():
        text = _read(path)
        if "TuringResearch Plus" in text or "TuringResearch_plus" in text:
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []


def test_prior_public_project_name_is_absent_from_public_surfaces() -> None:
    offenders: list[str] = []
    for path in _iter_public_files():
        text = _read(path)
        for term in _prior_project_terms():
            if term in text:
                offenders.append(f"{path.relative_to(ROOT)} contains prior project name")

    assert offenders == []


def test_compatibility_names_remain_documented_but_not_public_brand() -> None:
    readme = _read(ROOT / "README.md")
    pyproject = _read(ROOT / "pyproject.toml")
    mcp_example = _read(ROOT / ".mcp.example.json")
    install = _read(ROOT / "docs" / "install.md")

    for term in COMPATIBILITY_TERMS[:3]:
        assert term in (readme + pyproject + mcp_example + install)

    assert 'name = "turingresearch-plus"' in pyproject
    assert '"turingresearch-plus": {' in mcp_example
    assert '"command": "turingresearch-plus-mcp"' in mcp_example
    assert "turing_research_plus.session_runtime.cli:main" in pyproject
    assert "# TuringResearch Plus" not in readme


def test_public_docs_do_not_contain_fake_github_urls() -> None:
    offenders: list[str] = []
    fake_url_markers = [
        "github.com/OWNER/",
        "github.com/example/",
        "github.com/meamaturinlove221/TuringResearch",
        "https://github.com/turingresearch/",
    ]
    for path in _iter_public_files():
        text = _read(path)
        for marker in fake_url_markers:
            if marker in text:
                offenders.append(f"{path.relative_to(ROOT)} contains {marker}")

    assert offenders == []


def test_public_docs_site_manifests_do_not_expose_local_root_path() -> None:
    combined = "\n".join(
        [
            _read(ROOT / "docs-site" / "dist_manifest.yaml"),
            _read(ROOT / "docs-site" / "release_bundle" / "dist_manifest.yaml"),
        ]
    )

    assert "TuringResearch_plus" not in combined
    assert ("Tul" + "ingResearch") not in combined
    assert "E:/TuringResearch" not in combined
    assert "dist_root: docs-site/dist" in combined

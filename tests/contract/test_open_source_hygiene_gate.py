from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MCP = ROOT / ".mcp.example.json"
README = ROOT / "README.md"
TEXT_SUFFIXES = {".cff", ".css", ".html", ".json", ".md", ".toml", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".env.example"}
ALLOWED_ENV_FIXTURES = {
    "examples/vggt-human-prior-survey/shared_store_fixture/.env",
}
REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    ".mcp.example.json",
]
PUBLIC_ENTRY_FILES = [
    README,
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "install.md",
    ROOT / "docs" / "quickstart.md",
    ROOT / "docs" / "faq.md",
    ROOT / "docs" / "examples.md",
    ROOT / "docs" / "docs-index.md",
    ROOT / "docs" / "public-showcase.md",
    ROOT / "docs" / "open-source-license-decision.md",
    ROOT / "docs" / "open-source-compliance-checklist.md",
    ROOT / "docs" / "mcp-public-config-guide.md",
    ROOT / "docs" / "env-block-public-hygiene.md",
    ROOT / "docs" / "no-dotenv-public-policy.md",
    MCP,
    ROOT / ".env.example",
    ROOT / "pyproject.toml",
    ROOT / "CITATION.cff",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    ROOT / "SECURITY.md",
]
PUBLIC_TREES = [
    ROOT / "docs-site",
    ROOT / "examples" / "README.md",
    ROOT / "examples" / "public_demo",
    ROOT / "split_ready",
    ROOT / "split_manual",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _public_files() -> list[Path]:
    files = {path.resolve() for path in PUBLIC_ENTRY_FILES if path.exists()}
    for surface in PUBLIC_TREES:
        if not surface.exists():
            continue
        if surface.is_file():
            files.add(surface.resolve())
            continue
        tree = surface
        for path in tree.rglob("*"):
            if path.is_file() and (
                path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES
            ):
                files.add(path.resolve())
    return sorted(files)


def _mcp_env() -> dict[str, str]:
    config = json.loads(MCP.read_text(encoding="utf-8"))
    return config["mcpServers"]["turingresearch-plus"]["env"]


def _open_source_hygiene_blockers() -> list[str]:
    blockers: list[str] = []

    for relative in REQUIRED_ROOT_FILES:
        if not (ROOT / relative).exists():
            blockers.append(f"missing-required-file:{relative}")

    readme = _read(README) if README.exists() else ""
    if not readme.startswith("# TuringResearch"):
        blockers.append("public-name:not-turingresearch")
    for required in [
        "TuringResearch helps researchers",
        "fake/demo-first by default",
        "Fake / Live Boundary",
        "Privacy-first",
        "ARIS remains deferred",
    ]:
        if required not in readme:
            blockers.append(f"readme-missing:{required}")

    fake_url_markers = [
        "github.com/" + "OWNER/",
        "github.com/" + "example/",
        "github.com/" + "meamaturinlove221/TuringResearch",
        "https://github.com/" + "turingresearch/",
    ]
    prior_terms = [
        "Tul" + "ingResearch",
        "Tul" + "ingResearch_plus",
        ("tul" + "ingresearch") + "-plus",
        ("tul" + "ing_research") + "_plus",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    private_path_markers = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "E:" + "/TuringResearch",
        "E:" + "\\TuringResearch",
        "/home/",
    ]

    for path in _public_files():
        text = _read(path)
        relative = path.relative_to(ROOT).as_posix()
        if any(term in text for term in prior_terms):
            blockers.append(f"old-name:{relative}")
        if any(marker in text for marker in fake_url_markers):
            blockers.append(f"fake-github-url:{relative}")
        if token_like.search(text):
            blockers.append(f"token-like-value:{relative}")
        if any(marker in text for marker in private_path_markers):
            blockers.append(f"private-path:{relative}")

    for path in ROOT.rglob(".env"):
        relative = path.relative_to(ROOT).as_posix()
        if relative not in ALLOWED_ENV_FIXTURES:
            blockers.append(f"dotenv-file:{relative}")

    payload_suffixes = {".npz", ".pkl"}
    payload_name_markers = {
        "predictions.npz",
        "local_project_links.yaml",
    }
    payload_path_markers = {
        "raw_data",
        "private_data",
    }
    for surface in [
        ROOT / "examples" / "public_demo",
        ROOT / "split_ready",
        ROOT / "split_manual",
        ROOT / "docs-site" / "dist",
        ROOT / "docs-site" / "release_bundle",
    ]:
        if not surface.exists():
            continue
        for path in surface.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            lower_parts = {part.lower() for part in path.parts}
            if path.suffix.lower() in payload_suffixes:
                blockers.append(f"payload-file:{relative}")
            if path.name in payload_name_markers:
                blockers.append(f"payload-name:{relative}")
            if lower_parts & payload_path_markers:
                blockers.append(f"payload-path:{relative}")

    env = _mcp_env()
    expected = {
        "TURINGRESEARCH_MODE": "fake",
        "TURINGRESEARCH_ENABLE_LIVE_TESTS": "0",
        "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "0",
        "TURINGRESEARCH_ENABLE_WEB_LIVE": "0",
        "TURINGRESEARCH_ENABLE_APIFY_LIVE": "0",
        "TURINGRESEARCH_ENABLE_SFTP_LIVE": "0",
        "TURINGRESEARCH_ENABLE_PLUGINS": "0",
        "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE": "0",
    }
    for key, value in expected.items():
        if env.get(key) != value:
            blockers.append(f"mcp-env:{key}")
    for key, value in env.items():
        if key not in expected and value != "":
            blockers.append(f"mcp-secret-placeholder:{key}")

    license_docs = "\n".join(
        _read(path)
        for path in [
            ROOT / "LICENSE",
            ROOT / "CITATION.cff",
            ROOT / "CONTRIBUTING.md",
            ROOT / "SECURITY.md",
            ROOT / "docs" / "open-source-license-decision.md",
        ]
        if path.exists()
    )
    for required in [
        "Proprietary",
        "TuringResearch",
        "Do not commit",
        "human approval",
    ]:
        if required not in license_docs:
            blockers.append(f"governance-missing:{required}")

    return blockers


def test_open_source_hygiene_gate_has_no_blockers() -> None:
    assert _open_source_hygiene_blockers() == []


def test_open_source_hygiene_gate_documents_current_status() -> None:
    report = (ROOT / "docs" / "open-source-hygiene-gate-report.md").read_text(
        encoding="utf-8"
    )
    blockers = (ROOT / "docs" / "open-source-blockers.md").read_text(encoding="utf-8")

    assert "Status: pass with human license review pending" in report
    assert "Project public name is TuringResearch" in report
    assert "README exists and is public-ready" in report
    assert "ARIS deferred" in report
    assert "No Active Blockers" in blockers
    assert "Human Review Remains Required" in blockers

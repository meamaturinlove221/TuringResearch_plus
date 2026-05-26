from __future__ import annotations

import importlib
import re
from pathlib import Path

from turing_research_plus.privacy.models import PrivacyFindingType
from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
SPLIT_ROOT = ROOT / "examples" / "split_repos"
NEW_NAMESPACES = [
    "turing_research_core",
    "turing_research_paper",
    "turing_research_artifact",
    "turing_research_experiment",
    "turing_research_dashboard",
    "turing_research_plugins",
    "turing_research_cases",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_v0_8_repo_strategy_and_module_boundary_docs_are_complete() -> None:
    required_docs = [
        "docs/repository-strategy.md",
        "docs/module-split-readiness-matrix.md",
        "docs/module-public-api-contracts.md",
        "docs/monorepo-modular-layout.md",
        "docs/module-split-readiness-gate.md",
        "docs/split-readiness-integration-report.md",
        "docs/main-repo-public-launch-plan.md",
        "docs/readme-visual-asset-plan.md",
    ]
    missing = [path for path in required_docs if not (ROOT / path).exists()]

    assert missing == []
    assert "short-term monorepo" in _read("docs/repository-strategy.md")
    assert "facade/re-export" in _read("docs/monorepo-modular-layout.md")
    assert "not-ready-for-code-split" in _read("docs/module-split-readiness-gate.md")


def test_v0_8_new_namespace_imports_still_work() -> None:
    for namespace in NEW_NAMESPACES:
        module = importlib.import_module(namespace)
        public_api = importlib.import_module(f"{namespace}.public_api")

        assert module.NAMESPACE == namespace
        assert public_api.COMPATIBILITY_NAMESPACE == "turing_research_plus"


def test_v0_8_split_candidates_are_safe_design_skeletons() -> None:
    expected = {
        "turingresearch-vggt-case": ["README.md", "CASE_STUDY.md", "PRIVACY.md", "manifest.yaml"],
        "turingresearch-examples": ["README.md", "examples_manifest.yaml"],
        "turingresearch-plugins": ["README.md", "PLUGIN_POLICY.md", "plugins_manifest.yaml"],
    }

    for repo_id, filenames in expected.items():
        repo = SPLIT_ROOT / repo_id
        assert repo.exists()
        readme = (repo / "README.md").read_text(encoding="utf-8").lower()
        assert "flagship" in readme
        assert "not a real repository" in readme
        for filename in filenames:
            assert (repo / filename).exists(), f"{repo_id}/{filename}"


def test_v0_8_readme_positioning_is_honest_and_flagship_centered() -> None:
    readme = _read("README.md")
    lower = readme.lower()

    assert "local-first research os" in lower
    assert "fake/demo-first" in lower
    assert "human review" in lower
    assert (
        "does not automatically complete research" in lower
        or "not an autonomous scientist" in lower
    )
    assert (
        "does not write final paper conclusions" in lower
        or "not a final-paper generator" in lower
        or "not a\nfinal-paper generator" in lower
        or "automatically write final paper conclusions" in lower
    )
    assert (
        "does not claim vggt or sparseconv3d experiment success" in lower
        or (
            "not proof that any vggt experiment succeeded" in lower
            and "sparseconv3d" in lower
        )
    )
    assert "flagship" in lower
    assert "visual tour" in lower


def test_v0_8_launch_plan_is_complete_without_fake_social_proof() -> None:
    launch = _read("docs/main-repo-public-launch-plan.md").lower()
    social = _read("docs/social-proof-plan.md").lower()

    for phrase in [
        "readme first screen",
        "architecture diagram",
        "quickstart",
        "public demo",
        "vggt case study",
        "comparison with ordinary literature tools",
        "fake / live boundary",
        "screenshots and demo gifs",
        "issues and discussions",
        "roadmap",
        "license and safety",
    ]:
        assert phrase in launch
    assert "not allowed" in social
    assert "fake user quotes" in social
    assert "fake benchmark wins" in social
    assert "fake internship or offer association" in social


def test_v0_8_public_surfaces_have_no_sensitive_payload_patterns() -> None:
    surfaces = [
        ROOT / "README.md",
        ROOT / "docs" / "main-repo-public-launch-plan.md",
        ROOT / "docs" / "split-readiness-integration-report.md",
        ROOT / "docs" / "readme-visual-asset-plan.md",
        ROOT / "examples" / "split_repos",
    ]
    report = scan_privacy_paths(surfaces)
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for surface in surfaces
        for path in ([surface] if surface.is_file() else surface.rglob("*"))
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".mmd"}
    )
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "BEGIN " + "PRIVATE KEY",
        "local_project_links" + ".yaml",
        "SMPLX" + "_",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    allowed_policy_mentions = {PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK}

    assert report.release_blocker is False
    assert all(finding.release_blocker is False for finding in report.findings)
    assert {finding.finding_type for finding in report.findings} <= allowed_policy_mentions
    assert all(
        "examples/split_repos" in finding.path
        or finding.path.replace("\\", "/").endswith("/README.md")
        for finding in report.findings
    )
    for item in forbidden:
        assert item not in text
    assert not token_like.search(text)

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def assert_public_safe(text: str) -> None:
    legacy_misspelling = "Tuling" + "Research"
    forbidden_patterns = [
        re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
        re.compile(r"ghp_[A-Za-z0-9_]{12,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{12,}"),
        re.compile(r"https://" + r"github\.com/[^`\s<>()]+/turingresearch-(?:vggt-case|examples)"),
        re.compile(r"[A-Za-z]:\\vggt", re.IGNORECASE),
        re.compile(r"/home/[^/\s]+/"),
        re.compile(r"local_project_links\.yaml"),
    ]

    assert legacy_misspelling not in text
    assert ("status" + ": observed") not in text.lower()
    assert ("SparseConv3D" + " success") not in text
    for pattern in forbidden_patterns:
        assert pattern.search(text) is None


def test_integration_report_records_all_required_gates() -> None:
    report = read_text("docs/v1.6.0-package-docs-split-integration-report.md")

    required = [
        "docs bundle pass",
        "split manual pack pass",
        "package metadata pass",
        "install smoke pass",
        "release artifact manifest pass",
        "no secrets",
        "no raw data",
        "no fake URL",
        "GO FOR V1.6 PUBLIC RELEASE EXECUTION REVIEW",
        "NO-GO FOR AUTOMATIC PUBLICATION",
    ]
    for term in required:
        assert term in report


def test_docs_bundle_gate_is_present_and_public_safe() -> None:
    required_paths = [
        "docs/docs-release-bundle.md",
        "docs/v1.6.0-docs-deployment-gate-report.md",
        "docs/v1.6.0-docs-go-no-go.md",
        "docs-site/release_bundle_manifest.yaml",
    ]

    combined = "\n".join(read_text(path) for path in required_paths)

    assert "release bundle pass" in combined or "Status: ready for human review" in combined
    assert "GO FOR GITHUB PAGES-READY" in combined
    assert "NO-GO FOR AUTOMATIC DEPLOYMENT" in combined
    assert "no fake URL" in combined
    assert "no secrets" in combined
    assert_public_safe(combined)


def test_split_manual_gate_is_present_and_public_safe() -> None:
    required_paths = [
        "docs/v1.6.0-physical-split-manual-gate-report.md",
        "docs/v1.6.0-split-manual-go-no-go.md",
        "docs/split-repo-url-placeholder-policy.md",
    ]

    combined = "\n".join(read_text(path) for path in required_paths)

    assert "GO FOR HUMAN REVIEW" in combined
    assert "NO-GO FOR AUTOMATIC SPLIT EXECUTION" in combined
    assert "no fake URL" in combined
    assert "no raw data" in combined
    assert "main TuringResearch repository remains the flagship" in combined
    assert_public_safe(combined)


def test_package_metadata_and_install_smoke_are_aligned() -> None:
    project = tomllib.loads(read_text("pyproject.toml"))["project"]
    assert isinstance(project, dict)

    docs = "\n".join(
        [
            read_text("docs/packaging-readiness-v1.6.md"),
            read_text("docs/package-metadata-audit.md"),
            read_text("docs/install-smoke-test.md"),
            read_text("docs/pipx-install-guide.md"),
            read_text("docs/uv-install-guide.md"),
        ]
    )

    assert project["name"] == "turingresearch-plus"
    assert project["version"] == read_text("VERSION").strip()
    assert project["description"] == "TuringResearch local-first research workflow engine."
    assert "No PyPI package is required" in docs
    assert "No API key" in docs
    assert "No VGGT" in docs
    assert_public_safe(docs)


def test_install_smoke_command_runs_fake_health_check() -> None:
    env = os.environ.copy()
    env["TURINGRESEARCH_MODE"] = "fake"
    env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] = "0"
    env["TURINGRESEARCH_ENABLE_PLUGINS"] = "0"
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, "-m", "turing_research.mcp_server", "--health-check"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["package"] == "turing_research"


def test_release_artifact_manifest_is_present_and_safe() -> None:
    combined = "\n".join(
        [
            read_text("docs/release-artifact-build-v1.6.md"),
            read_text("docs/release-artifact-manifest-v1.6.md"),
        ]
    )

    assert "wheel-v1.6-local" in combined
    assert "sdist-v1.6-local" in combined
    assert "No PyPI publish" in combined
    assert "No package upload" in combined
    assert "no raw data" in combined.lower()
    assert "no SMPL-X model" in combined
    assert_public_safe(combined)


def test_lane_and_ledger_record_round_382() -> None:
    lane = read_text("lanes/360_package_docs_split_integration_gate.md")
    ledger = read_text("lanes/00_master_ledger.md")

    assert "Round 382 - Package / Docs / Split Integration Gate" in lane
    assert "Round 382 - Package / Docs / Split Integration Gate" in ledger
    assert "No PyPI publish" in lane
    assert "No docs deployment" in lane
    assert "No child repository creation" in lane

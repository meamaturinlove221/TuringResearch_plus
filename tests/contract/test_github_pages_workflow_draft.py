from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "docs-pages-dry-run.yml"
DOCS = [
    ROOT / "docs" / "github-pages-workflow-draft.md",
    ROOT / "docs" / "github-pages-manual-enable-guide.md",
    ROOT / "docs" / "github-pages-safety-checklist.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_github_pages_workflow_draft_exists_and_is_manual() -> None:
    workflow = _read(WORKFLOW)

    assert "workflow_dispatch:" in workflow
    assert "dry_run_only:" in workflow
    assert "default: true" in workflow
    assert "push:" not in workflow
    assert "pull_request:" not in workflow
    assert "schedule:" not in workflow


def test_github_pages_workflow_draft_does_not_deploy_pages() -> None:
    workflow = _read(WORKFLOW)

    forbidden = [
        "actions/deploy-pages",
        "pages: write",
        "id-token: write",
        "github-pages",
        "environment:",
        "url:",
    ]
    for term in forbidden:
        assert term not in workflow

    assert "contents: read" in workflow
    assert "actions/upload-artifact@v4" in workflow


def test_github_pages_workflow_draft_runs_docs_only_checks() -> None:
    workflow = _read(WORKFLOW)

    required = [
        "tests/workflow/test_docs_deployment_preflight.py",
        "tests/workflow/test_docs_deployment_dry_run.py",
        "tests/contract/test_public_release_hygiene.py",
        "docs-site/dist/**",
        "docs-site/dist_manifest.yaml",
        "docs-site/preflight_report.md",
        "docs-site/deployment_dry_run_report.md",
    ]
    for term in required:
        assert term in workflow

    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS: \"0\"" in workflow
    assert "TURINGRESEARCH_ENABLE_WEB_LIVE: \"0\"" in workflow
    assert "TURINGRESEARCH_ENABLE_APIFY_LIVE: \"0\"" in workflow
    assert "TURINGRESEARCH_ENABLE_SFTP_LIVE: \"0\"" in workflow


def test_github_pages_docs_record_manual_enable_boundary() -> None:
    combined = "\n".join(_read(path) for path in DOCS)

    required = [
        "dry-run workflow draft",
        "does not deploy",
        "no `actions/deploy-pages`",
        "no `pages: write` permission",
        "no `id-token: write` permission",
        "no API key",
        "no workflow secrets",
        "manual",
        "safety checklist",
        "ARIS remains deferred",
    ]
    for term in required:
        assert term in combined


def test_github_pages_workflow_draft_contains_no_sensitive_material() -> None:
    combined = "\n".join([_read(WORKFLOW), *[_read(path) for path in DOCS]])

    forbidden = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "github_pat_",
        "BEGIN OPENSSH PRIVATE KEY",
        "SMPL-X",
        "status" + ": observed",
        "deployed at",
        "live URL:",
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
    assert re.search(r"sk-[A-Za-z0-9_-]{20,}", combined) is None

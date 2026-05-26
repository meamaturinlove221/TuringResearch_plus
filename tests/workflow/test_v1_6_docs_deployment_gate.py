from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "docs-pages-dry-run.yml"
BUNDLE = ROOT / "docs-site" / "release_bundle"
BUNDLE_MANIFEST = ROOT / "docs-site" / "release_bundle_manifest.yaml"
PREFLIGHT = ROOT / "docs-site" / "preflight_report.md"


def _read(path: str | Path) -> str:
    if isinstance(path, str):
        return (ROOT / path).read_text(encoding="utf-8")
    return path.read_text(encoding="utf-8")


def test_v1_6_docs_deployment_gate_required_artifacts_exist() -> None:
    required = [
        "docs/v1.6.0-final-scope.md",
        "docs/docs-deployment-preflight.md",
        "docs/docs-deployment-blockers.md",
        "docs-site/preflight_report.md",
        ".github/workflows/docs-pages-dry-run.yml",
        "docs/github-pages-workflow-draft.md",
        "docs/github-pages-manual-enable-guide.md",
        "docs/github-pages-safety-checklist.md",
        "docs-site/release_bundle_manifest.yaml",
        "docs-site/release_bundle_report.md",
        "docs/docs-release-bundle.md",
        "docs/v1.6.0-docs-deployment-gate-report.md",
        "docs/v1.6.0-docs-go-no-go.md",
    ]
    for path in required:
        assert (ROOT / path).exists()


def test_v1_6_docs_deployment_gate_preflight_passes() -> None:
    preflight = _read(PREFLIGHT)

    required = [
        "Status: pass with review warnings.",
        "Deployment performed: `false`.",
        "Public URL: `none`.",
        "Missing pages: 0.",
        "Broken links: 0.",
        "Missing source docs: 0.",
        "Private path hits: 0.",
        "Secrets: 0",
        "Raw data: 0",
        "Fake deployment URL: 0",
    ]
    for term in required:
        assert term in preflight


def test_v1_6_docs_deployment_gate_workflow_is_dry_run_only() -> None:
    workflow = _read(WORKFLOW)

    assert "workflow_dispatch:" in workflow
    assert "dry_run_only:" in workflow
    assert "contents: read" in workflow
    assert "actions/upload-artifact@v4" in workflow
    assert "tests/workflow/test_docs_deployment_preflight.py" in workflow
    assert "tests/workflow/test_docs_deployment_dry_run.py" in workflow

    forbidden = [
        "actions/deploy-pages",
        "pages: write",
        "id-token: write",
        "environment:",
        "url:",
        "secrets.",
    ]
    for term in forbidden:
        assert term not in workflow


def test_v1_6_docs_deployment_gate_release_bundle_passes() -> None:
    manifest = _read(BUNDLE_MANIFEST)
    paths = re.findall(r"^\s+- path:\s+(.+)$", manifest, re.M)

    assert BUNDLE.exists()
    assert (BUNDLE / "site" / "index.html").exists()
    assert (BUNDLE / "site" / "quickstart.html").exists()
    assert (BUNDLE / "site" / "original-repo-parity.html").exists()
    assert (BUNDLE / "site" / "public-demo.html").exists()
    assert (BUNDLE / "site" / "privacy.html").exists()
    assert "deployment_performed: false" in manifest
    assert "public_url: none" in manifest
    assert "no_fake_public_url: true" in manifest
    assert paths


def test_v1_6_docs_deployment_gate_reports_go_no_go() -> None:
    combined = "\n".join(
        [
            _read("docs/v1.6.0-docs-deployment-gate-report.md"),
            _read("docs/v1.6.0-docs-go-no-go.md"),
            _read("docs/docs-deployment-preflight.md"),
            _read("docs/github-pages-workflow-draft.md"),
            _read("docs/docs-release-bundle.md"),
        ]
    )

    required = [
        "GO FOR GITHUB PAGES-READY",
        "NO-GO FOR AUTOMATIC DEPLOYMENT",
        "preflight pass",
        "workflow draft pass",
        "release bundle pass",
        "no fake URL",
        "no secrets",
        "no private paths",
        "no raw data",
        "no old naming",
        "not proof that a public site exists",
    ]
    for term in required:
        assert term in combined


def test_v1_6_docs_deployment_gate_contains_no_sensitive_material() -> None:
    paths = [
        ROOT / "docs" / "v1.6.0-docs-deployment-gate-report.md",
        ROOT / "docs" / "v1.6.0-docs-go-no-go.md",
        WORKFLOW,
        BUNDLE_MANIFEST,
        PREFLIGHT,
        *[path for path in BUNDLE.rglob("*") if path.is_file()],
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "github_pat_",
        "sk-",
        "BEGIN OPENSSH PRIVATE KEY",
        "SMPL-X",
        "status" + ": observed",
        "deployed at",
        "live URL:",
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined

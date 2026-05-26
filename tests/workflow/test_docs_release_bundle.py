from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "docs-site" / "release_bundle"
MANIFEST = ROOT / "docs-site" / "release_bundle_manifest.yaml"
REPORT = ROOT / "docs-site" / "release_bundle_report.md"
DOC = ROOT / "docs" / "docs-release-bundle.md"


def _sha256(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() in {".css", ".html", ".json", ".md", ".txt", ".yaml", ".yml"}:
        data = data.replace(b"\r\n", b"\n")
    digest = hashlib.sha256()
    digest.update(data)
    return digest.hexdigest()


def _manifest_paths() -> list[str]:
    return re.findall(r"^\s+- path:\s+(.+)$", MANIFEST.read_text(encoding="utf-8"), re.M)


def test_docs_release_bundle_contains_static_site_and_review_files() -> None:
    required = [
        "site/index.html",
        "site/quickstart.html",
        "site/original-repo-parity.html",
        "site/public-demo.html",
        "site/privacy.html",
        "site/site.css",
        "nav.yaml",
        "site_manifest.yaml",
        "dist_manifest.yaml",
        "preflight_report.md",
        "deployment_dry_run_report.md",
    ]

    for relative in required:
        assert (BUNDLE / relative).exists()

    assert not (BUNDLE / "static_export_manifest.json").exists()


def test_docs_release_bundle_manifest_records_all_hashes() -> None:
    manifest = MANIFEST.read_text(encoding="utf-8")

    assert "status: release-bundle-dry-run" in manifest
    assert "deployment_performed: false" in manifest
    assert "public_url: none" in manifest
    assert "requires_human_review: true" in manifest

    paths = _manifest_paths()
    assert paths
    assert set(paths) == {
        path.relative_to(BUNDLE).as_posix()
        for path in BUNDLE.rglob("*")
        if path.is_file()
    }
    for relative in paths:
        path = BUNDLE / relative
        assert path.exists()
        assert f"    sha256: {_sha256(path)}" in manifest


def test_docs_release_bundle_report_records_manual_boundary() -> None:
    combined = "\n".join(
        [
            MANIFEST.read_text(encoding="utf-8"),
            REPORT.read_text(encoding="utf-8"),
            DOC.read_text(encoding="utf-8"),
        ]
    )

    required = [
        "READY FOR HUMAN REVIEW",
        "Deployment performed: `false`",
        "Public URL: `none`",
        "static HTML",
        "assets",
        "nav",
        "manifest",
        "Hashes are recorded",
        "no public deployment",
        "no fake public URL",
        "human review required",
    ]
    for term in required:
        assert term in combined


def test_docs_release_bundle_contains_no_sensitive_material() -> None:
    paths = [
        *[path for path in BUNDLE.rglob("*") if path.is_file()],
        MANIFEST,
        REPORT,
        DOC,
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

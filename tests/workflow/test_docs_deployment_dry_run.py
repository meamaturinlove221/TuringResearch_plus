from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "docs-site" / "dist"
MANIFEST = ROOT / "docs-site" / "dist_manifest.yaml"
REPORT = ROOT / "docs-site" / "deployment_dry_run_report.md"
DOC = ROOT / "docs" / "docs-deployment-dry-run.md"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest_paths() -> list[str]:
    return re.findall(r"^\s+- path:\s+(.+)$", MANIFEST.read_text(encoding="utf-8"), re.M)


def test_docs_deployment_dry_run_dist_exists() -> None:
    assert DIST.exists()
    assert (DIST / "index.html").exists()
    assert (DIST / "quickstart.html").exists()
    assert (DIST / "original-repo-parity.html").exists()
    assert (DIST / "public-demo.html").exists()
    assert (DIST / "roadmap.html").exists()
    assert (DIST / "site.css").exists()
    assert not (DIST / "static_export_manifest.json").exists()


def test_docs_deployment_dry_run_manifest_records_hashes() -> None:
    manifest = MANIFEST.read_text(encoding="utf-8")
    assert "deployment_performed: false" in manifest
    assert "public_url: none" in manifest
    assert "requires_human_review: true" in manifest

    for relative in _manifest_paths():
        path = DIST / relative
        assert path.exists()
        digest = _sha256(path)
        assert f"    sha256: {digest}" in manifest


def test_docs_deployment_dry_run_report_is_not_public_deployment() -> None:
    combined = "\n".join(
        [
            MANIFEST.read_text(encoding="utf-8"),
            REPORT.read_text(encoding="utf-8"),
            DOC.read_text(encoding="utf-8"),
        ]
    )
    assert "Deployment performed: `false`" in combined
    assert "Public URL: `none`" in combined
    assert "no public deployment" in combined
    assert "no real public URL" in combined
    assert "GitHub Pages-ready evidence" in combined


def test_docs_deployment_dry_run_contains_no_sensitive_material() -> None:
    paths = [
        *[path for path in DIST.rglob("*") if path.is_file()],
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
        "sk-",
        "SMPL-X",
        "status" + ": observed",
        "deployed at",
        "live URL:",
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined

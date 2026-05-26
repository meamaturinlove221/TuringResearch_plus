from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPLIT_EXPORTS = ROOT / "examples" / "split_exports"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined_export_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in SPLIT_EXPORTS.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}
    )


def test_v0_9_split_exports_are_complete_and_dry_run_only() -> None:
    candidates = {
        "turingresearch-vggt-case": [
            "README.md",
            "CASE_STUDY.md",
            "PRIVACY.md",
            "manifest.yaml",
            "split_manifest.yaml",
            "safety_report.md",
        ],
        "turingresearch-examples": [
            "README.md",
            "examples_manifest.yaml",
            "split_manifest.yaml",
            "safety_report.md",
        ],
    }

    for candidate, files in candidates.items():
        export_dir = SPLIT_EXPORTS / candidate
        assert export_dir.exists()
        for filename in files:
            assert (export_dir / filename).exists(), f"{candidate}/{filename}"
        manifest = _read(export_dir / "split_manifest.yaml")
        safety = _read(export_dir / "safety_report.md")
        assert "dry_run_only: true" in manifest
        assert "creates_github_repo: false" in manifest
        assert "pushes_git: false" in manifest
        assert "release_blocker: `false`" in safety
        assert "requires_human_review: `true`" in safety


def test_v0_9_split_exports_keep_readmes_clear_and_flagship_centered() -> None:
    for candidate in ["turingresearch-vggt-case", "turingresearch-examples"]:
        readme = _read(SPLIT_EXPORTS / candidate / "README.md").lower()
        assert "flagship" in readme
        assert "install" in readme
        assert "star" in readme
        assert "not a real repository" in readme
        assert "human review" in readme or "reviewed" in readme


def test_v0_9_split_exports_have_no_sensitive_payload_patterns() -> None:
    text = _combined_export_text()
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "BEGIN " + "PRIVATE KEY",
        "local_project_links" + ".yaml",
        "SMPLX" + "_",
    ]
    token_like = re.compile(
        r"(?<![A-Za-z0-9])(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,})"
    )

    for item in forbidden:
        assert item not in text
    assert not token_like.search(text)
    assert "demo result is observed evidence" not in text.lower()
    assert "demo result was observed evidence" not in text.lower()
    assert "sparseconv3d succeeded" not in text.lower()
    assert "vggt experiment succeeded" not in text.lower()


def test_v0_9_main_repo_strategy_preserves_flagship_and_install_path() -> None:
    docs = "\n".join(
        [
            _read(ROOT / "docs" / "post-split-main-repo-strategy.md"),
            _read(ROOT / "docs" / "post-split-readme-plan.md"),
            _read(ROOT / "docs" / "post-split-docs-linking.md"),
            _read(ROOT / "docs" / "post-split-star-protection.md"),
        ]
    ).lower()

    assert "main repository remains the only flagship" in docs
    assert "install path" in docs
    assert "quickstart" in docs
    assert "optional demo/case" in docs
    assert "does not replace the main repo" in docs


def test_v0_9_split_go_no_go_docs_are_consistent() -> None:
    report = _read(ROOT / "docs" / "v0.9.0-split-readiness-report.md")
    go_no_go = _read(ROOT / "docs" / "v0.9.0-split-go-no-go.md")
    blockers = _read(ROOT / "docs" / "v0.9.0-split-blockers.md")

    assert "GO FOR FINAL HUMAN REVIEW" in report
    assert "NO-GO FOR AUTOMATIC PHYSICAL SPLIT" in go_no_go
    assert "maintainer approval" in blockers
    assert "no secrets" in report.lower()
    assert "no raw data" in report.lower()
    assert "no SMPL-X" in report

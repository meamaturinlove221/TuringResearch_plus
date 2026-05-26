from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.repo_split.dry_run_exporter import export_split_dry_run
from turing_research_plus.repo_split.models import RepoSplitDryRunRequest, RepoSplitStatus

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "examples" / "split_repos" / "turingresearch-vggt-case"


def test_vggt_case_split_dry_run_exports_public_safe_skeleton(tmp_path: Path) -> None:
    result = export_split_dry_run(
        RepoSplitDryRunRequest(
            candidate_id="turingresearch-vggt-case",
            source_root=SOURCE,
            output_root=tmp_path / "split_exports",
        )
    )
    export_dir = tmp_path / "split_exports" / "turingresearch-vggt-case"

    assert result.status == RepoSplitStatus.PASS_WITH_WARNINGS
    assert (export_dir / "README.md").exists()
    assert (export_dir / "CASE_STUDY.md").exists()
    assert (export_dir / "PRIVACY.md").exists()
    assert (export_dir / "manifest.yaml").exists()
    assert (export_dir / "split_manifest.yaml").exists()
    assert (export_dir / "safety_report.md").exists()
    assert result.manifest.pushes_git is False
    assert result.manifest.creates_github_repo is False
    assert result.safety_report.release_blocker is False

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in export_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml"}
    )
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "BEGIN " + "PRIVATE KEY",
        "local_project_links" + ".yaml",
        "SMPLX" + "_",
    ]
    token_like = re.compile(
        r"(?<![A-Za-z0-9])(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9_]{20,})"
    )

    for item in forbidden:
        assert item not in combined
    assert not token_like.search(combined)
    assert "SparseConv3D succeeded" not in combined
    assert "SparseConv3D is successful" not in combined
    assert "dry_run_only: true" in (export_dir / "split_manifest.yaml").read_text(
        encoding="utf-8"
    )

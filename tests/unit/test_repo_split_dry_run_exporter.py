from __future__ import annotations

from pathlib import Path

from turing_research_plus.repo_split.dry_run_exporter import (
    collect_split_candidate_files,
    export_split_dry_run,
)
from turing_research_plus.repo_split.models import RepoSplitDryRunRequest, RepoSplitStatus


def test_collect_split_candidate_files_returns_relative_paths(tmp_path: Path) -> None:
    source = tmp_path / "source"
    (source / "docs").mkdir(parents=True)
    (source / "README.md").write_text("# Demo\n", encoding="utf-8")
    (source / "docs" / "plan.md").write_text("# Plan\n", encoding="utf-8")

    assert set(collect_split_candidate_files(source)) == {
        Path("README.md"),
        Path("docs") / "plan.md",
    }


def test_dry_run_exporter_copies_safe_files_and_writes_reports(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "README.md").write_text("# Demo\n", encoding="utf-8")
    (source / "manifest.yaml").write_text("status: split-repo-skeleton-only\n", encoding="utf-8")

    result = export_split_dry_run(
        RepoSplitDryRunRequest(
            candidate_id="demo",
            source_root=source,
            output_root=tmp_path / "exports",
        )
    )

    export_dir = tmp_path / "exports" / "demo"
    assert result.status == RepoSplitStatus.PASS
    assert (export_dir / "README.md").exists()
    assert (export_dir / "manifest.yaml").exists()
    assert (export_dir / "split_manifest.yaml").exists()
    assert (export_dir / "safety_report.md").exists()
    assert {item.relative_path for item in result.manifest.included_files} == {
        "README.md",
        "manifest.yaml",
    }


def test_dry_run_exporter_omits_unsafe_files(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "README.md").write_text("# Demo\n", encoding="utf-8")
    (source / ".env").write_text("API_KEY=secret\n", encoding="utf-8")

    result = export_split_dry_run(
        RepoSplitDryRunRequest(
            candidate_id="demo",
            source_root=source,
            output_root=tmp_path / "exports",
        )
    )

    export_dir = tmp_path / "exports" / "demo"
    assert result.status == RepoSplitStatus.BLOCKED
    assert (export_dir / "README.md").exists()
    assert not (export_dir / ".env").exists()
    assert {item.relative_path for item in result.manifest.omitted_files} == {".env"}
    assert result.safety_report.release_blocker is True

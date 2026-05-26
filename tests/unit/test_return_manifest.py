from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.return_manifest import (
    REQUIRED_RETURN_FILES,
    load_return_manifest,
    load_sha256sums,
)


def test_load_sha256sums_parses_manifest(tmp_path: Path) -> None:
    sums = tmp_path / "SHA256SUMS.txt"
    sums.write_text(f"{'a' * 64}  RUN_STATUS.json\n", encoding="utf-8")

    assert load_sha256sums(sums) == {"RUN_STATUS.json": "a" * 64}


def test_load_return_manifest_reports_missing_required_files(tmp_path: Path) -> None:
    (tmp_path / "RUN_STATUS.json").write_text("{}", encoding="utf-8")

    manifest = load_return_manifest(tmp_path)

    assert "RUN_STATUS.json" in manifest.present_files
    assert "FINAL_STATUS.json" in manifest.missing_required_files
    assert set(manifest.required_files) == set(REQUIRED_RETURN_FILES)


def test_load_return_manifest_includes_extra_files(tmp_path: Path) -> None:
    (tmp_path / "RUN_STATUS.json").write_text("{}", encoding="utf-8")
    (tmp_path / "EXTRA.md").write_text("review\n", encoding="utf-8")

    manifest = load_return_manifest(tmp_path)

    assert "EXTRA.md" in [item.path for item in manifest.files if not item.required]

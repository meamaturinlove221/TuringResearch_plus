from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.archive_safety import (
    audit_context_pack_candidates,
    is_safe_pack_entry,
    normalize_pack_entry,
)


def test_normalize_pack_entry_uses_posix_relative_paths() -> None:
    assert normalize_pack_entry(".\\PROJECT_CONTEXT.md") == "PROJECT_CONTEXT.md"


def test_safe_pack_entry_accepts_required_context_file() -> None:
    check = is_safe_pack_entry("PROJECT_CONTEXT.md")

    assert check.included is True
    assert check.reasons == []


def test_safe_pack_entry_blocks_dotfiles_and_private_payloads() -> None:
    env = is_safe_pack_entry(".env")
    model = is_safe_pack_entry("SMPLX_model.pkl")
    raw = is_safe_pack_entry("raw_data/input.json")

    assert env.included is False
    assert "hidden-dotfile-excluded" in env.reasons
    assert model.included is False
    assert "forbidden-body-model-file" in model.reasons
    assert raw.included is False
    assert "forbidden-private-or-raw-path" in raw.reasons


def test_audit_context_pack_candidates_excludes_unallowlisted_files(tmp_path: Path) -> None:
    (tmp_path / "PROJECT_CONTEXT.md").write_text("project\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("supporting but not allowlisted\n", encoding="utf-8")

    report = audit_context_pack_candidates(tmp_path)

    assert "PROJECT_CONTEXT.md" in report.included_paths
    excluded = {Path(path).name for path in report.excluded_paths}
    assert "notes.md" in excluded


def test_huge_npz_is_excluded(tmp_path: Path) -> None:
    path = tmp_path / "predictions.npz"
    path.write_bytes(b"0" * 6_000_001)

    report = audit_context_pack_candidates(tmp_path)
    check = report.checks[0]

    assert check.included is False
    assert "summary-only-npz-required" in check.reasons
    assert "huge-npz-forbidden" in check.reasons

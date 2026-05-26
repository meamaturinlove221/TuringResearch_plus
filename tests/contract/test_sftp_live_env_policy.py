from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "sftp-live-optional-guide.md"
EXAMPLE = ROOT / "examples" / "session_runtime" / "sftp_live_optional"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_sftp_live_optional_docs_lock_default_fake_mode() -> None:
    text = _text(DOC)

    assert "SFTP live transfer is optional" in text
    assert "TURINGRESEARCH_MODE=fake" in text
    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in text
    assert "TURINGRESEARCH_ENABLE_SFTP_LIVE=0" in text
    assert "TURINGRESEARCH_SFTP_CREDENTIAL=" in text
    assert "TURINGRESEARCH_SFTP_KEY_PATH=<private local key path placeholder>" in text
    assert "TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target" in text


def test_sftp_live_optional_example_contains_no_password_or_key_path() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(EXAMPLE.rglob("*"))
        if path.is_file()
    )

    assert "TURINGRESEARCH_SFTP_CREDENTIAL=" in combined
    assert "<private local credential reference>" in combined
    assert "<private local key path placeholder>" in combined
    assert "password=" not in combined.lower()
    assert "BEGIN OPENSSH PRIVATE KEY" not in combined
    assert "D:/vggt" not in combined
    assert "D:\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined


def test_sftp_live_optional_policy_blocks_remote_commands_and_delete() -> None:
    combined = "\n".join([_text(DOC), _text(EXAMPLE / "README.md")])

    assert "SFTP live disabled by default" in combined
    assert "no remote command" in combined
    assert "no remote delete" in combined
    assert "transfer target must be explicit" in combined
    assert "path traversal blocked" in combined


def test_sftp_live_optional_report_records_skip_defaults() -> None:
    report = _text(EXAMPLE / "live_skip_report.md")

    assert "Status: skipped by default." in report
    assert "SFTP live disabled by default: pass" in report
    assert "no password in repo: pass" in report
    assert "transfer target explicit: pass" in report

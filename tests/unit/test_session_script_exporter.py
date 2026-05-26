from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.script_exporter import (
    SCRIPT_ORDER,
    SessionScriptExportRequest,
    SessionScriptExportStatus,
    build_session_script_specs,
    export_session_scripts,
    render_session_script_export_report,
)


def test_build_session_script_specs_have_expected_names_and_safety() -> None:
    specs = build_session_script_specs(
        SessionScriptExportRequest(output_dir=Path("tmp/session-script-export"))
    )

    assert [spec.name for spec in specs] == SCRIPT_ORDER
    assert all(spec.safety.release_blocker is False for spec in specs)
    assert all("# shellcheck shell=bash" in spec.content for spec in specs)
    assert all("MANUAL LIVE STEP" in spec.content for spec in specs)
    assert all("ssh " not in spec.content.lower() for spec in specs)
    assert all("rm " not in spec.content.lower() for spec in specs)


def test_export_session_scripts_writes_scripts_and_sop(tmp_path: Path) -> None:
    report = export_session_scripts(SessionScriptExportRequest(output_dir=tmp_path))
    markdown = render_session_script_export_report(report)

    assert report.status == SessionScriptExportStatus.EXPORTED
    assert report.release_blocker is False
    assert report.scripts_executed is False
    assert report.remote_execution_enabled is False
    assert report.live_ssh_enabled is False
    assert report.automatic_evidence_ledger_write is False
    assert "Scripts executed during export: `false`" in markdown
    for name in SCRIPT_ORDER:
        assert (tmp_path / name).exists()
        assert (tmp_path / f"{name}.safety.md").exists()
    assert (tmp_path / "SESSION_SCRIPT_SOP.md").exists()


def test_exported_scripts_use_quoted_variables(tmp_path: Path) -> None:
    export_session_scripts(SessionScriptExportRequest(output_dir=tmp_path))

    for path in tmp_path.glob("*.sh"):
        text = path.read_text(encoding="utf-8")
        assert "${" in text
        assert "$SOURCE_DIR" not in text
        assert "$TARGET_DIR" not in text
        assert "API_KEY=" not in text
        assert "TOKEN=" not in text

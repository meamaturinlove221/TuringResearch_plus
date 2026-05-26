from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.script_exporter import (
    SCRIPT_ORDER,
    SessionScriptExportRequest,
    export_session_scripts,
)

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_DIR = ROOT / "examples" / "session_runtime" / "scripts"


def test_session_script_export_fake_fixture(tmp_path: Path) -> None:
    report = export_session_scripts(SessionScriptExportRequest(output_dir=tmp_path))

    assert [script.name for script in report.scripts] == SCRIPT_ORDER
    assert report.status == "exported"
    assert report.scripts_executed is False
    assert report.release_blocker is False

    combined = "\n".join(path.read_text(encoding="utf-8") for path in tmp_path.glob("*.sh"))
    assert "python -m turing_research_plus.session_runtime.cli session preflight" in combined
    assert "python -m turing_research_plus.session_runtime.cli session pack" in combined
    assert "python -m turing_research_plus.session_runtime.cli session transfer --fake" in combined
    assert "python -m turing_research_plus.session_runtime.cli session verify-return" in combined
    assert "python -m turing_research_plus.session_runtime.cli session replay" in combined
    assert "ssh " not in combined.lower()
    assert "sftp " not in "\n".join(
        line for line in combined.lower().splitlines() if not line.strip().startswith("#")
    )


def test_checked_in_session_scripts_demo_is_public_safe() -> None:
    expected = set(SCRIPT_ORDER)
    actual = {path.name for path in EXAMPLE_DIR.glob("*.sh")}

    assert expected <= actual
    combined = "\n".join(path.read_text(encoding="utf-8") for path in EXAMPLE_DIR.glob("*"))
    assert "MANUAL LIVE STEP" in combined
    assert "shellcheck" in combined.lower()
    assert "API_KEY=" not in combined
    assert "TOKEN=" not in combined
    assert "local_project_links.yaml" not in combined
    assert "D:/vggt" not in combined
    assert "rm -" not in combined
    assert "automatic Evidence Ledger write" in combined

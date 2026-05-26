from __future__ import annotations

import pytest

from turing_research_plus.session_runtime.script_safety import (
    ScriptSafetyStatus,
    audit_shell_script,
    render_script_safety_report,
)


def test_script_safety_passes_generated_style() -> None:
    script = "\n".join(
        [
            "#!/usr/bin/env bash",
            "# shellcheck shell=bash",
            "# MANUAL LIVE STEP (disabled): live SSH/SFTP requires review.",
            "set -euo pipefail",
            'readonly SOURCE_DIR="tmp/source"',
            'python -m turing_research_plus.session_runtime.cli session report \\',
            '  --output "${SOURCE_DIR}/report.md"',
        ]
    )

    report = audit_shell_script("safe.sh", script)
    markdown = render_script_safety_report(report)

    assert report.status == ScriptSafetyStatus.PASS
    assert report.release_blocker is False
    assert report.has_shellcheck_notes is True
    assert report.has_manual_live_marker is True
    assert "Contains active remote execution: `false`" in markdown


@pytest.mark.parametrize(
    ("script", "finding_id"),
    [
        ("rm -rf \"$TARGET_DIR\"", "destructive-command"),
        ("ssh \"$HOST\" \"uptime\"", "remote-execution"),
        ("API_KEY=notarealbutlongsecret", "secret-assignment"),
        ("python tool.py --source $SOURCE_DIR", "unquoted-variable"),
        ("# live SSH later\nsftp \"$HOST\"", "active-live-step"),
    ],
)
def test_script_safety_blocks_unsafe_patterns(script: str, finding_id: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        audit_shell_script("unsafe.sh", "# shellcheck shell=bash\n" + script)

    expected_terms = {
        "destructive-command": "destructive",
        "remote-execution": "remote",
        "secret-assignment": "secret",
        "unquoted-variable": "unquoted",
        "active-live-step": "live",
    }
    assert expected_terms[finding_id] in str(exc_info.value)

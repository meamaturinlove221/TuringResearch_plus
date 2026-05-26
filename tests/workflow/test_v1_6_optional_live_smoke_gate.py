from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPORT = ROOT / "docs" / "v1.6.0-optional-live-smoke-gate-report.md"
GO_NO_GO = ROOT / "docs" / "v1.6.0-optional-live-smoke-go-no-go.md"
LANE = ROOT / "lanes" / "355_optional_live_smoke_gate.md"

SCHOLAR_LANE = ROOT / "lanes" / "351_scholar_optional_live_smoke.md"
WEB_APIFY_LANE = ROOT / "lanes" / "352_web_apify_optional_live_smoke.md"
SFTP_LANE = ROOT / "lanes" / "353_sftp_optional_live_smoke.md"
REDACTION_LANE = ROOT / "lanes" / "354_live_output_redaction_gate.md"

SCHOLAR_DOC = ROOT / "docs" / "scholar-optional-live-smoke.md"
WEB_APIFY_DOC = ROOT / "docs" / "web-apify-optional-live-smoke.md"
SFTP_DOC = ROOT / "docs" / "sftp-optional-live-smoke.md"
REDACTION_DOC = ROOT / "docs" / "live-output-redaction-gate.md"

LIVE_TESTS = [
    ROOT / "tests" / "live" / "test_scholar_live_smoke_skipped_by_default.py",
    ROOT / "tests" / "live" / "test_web_apify_live_smoke_skipped_by_default.py",
    ROOT / "tests" / "live" / "test_sftp_live_smoke_skipped_by_default.py",
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def test_v1_6_optional_live_smoke_gate_docs_exist() -> None:
    for path in [REPORT, GO_NO_GO, LANE]:
        assert path.exists(), path.relative_to(ROOT).as_posix()


def test_v1_6_optional_live_smoke_gate_inputs_exist() -> None:
    for path in [
        SCHOLAR_LANE,
        WEB_APIFY_LANE,
        SFTP_LANE,
        REDACTION_LANE,
        SCHOLAR_DOC,
        WEB_APIFY_DOC,
        SFTP_DOC,
        REDACTION_DOC,
        *LIVE_TESTS,
    ]:
        assert path.exists(), path.relative_to(ROOT).as_posix()


def test_v1_6_optional_live_smoke_gate_records_required_passes() -> None:
    text = _combined([REPORT, GO_NO_GO, LANE])

    assert "GO FOR OPTIONAL LIVE SMOKE RELEASE-CANDIDATE REVIEW" in text
    assert "NO-GO FOR DEFAULT LIVE" in text
    assert "scholar fake smoke pass" in text
    assert "web/apify fake smoke pass" in text
    assert "sftp fake smoke pass" in text
    assert "all live tests skipped by default" in text
    assert "redaction gate pass" in text
    assert "no secrets" in text
    assert "no default network" in text


def test_v1_6_optional_live_smoke_gate_evidence_lanes_pass() -> None:
    text = _combined([SCHOLAR_LANE, WEB_APIFY_LANE, SFTP_LANE, REDACTION_LANE])

    assert "Scholar fake smoke: passed with 3 tests." in text
    assert "Web / Apify fake smoke: passed with 3 tests." in text
    assert "SFTP fake smoke: passed with 3 tests." in text
    assert text.count("skipped live test selected via `-m live`") >= 3
    assert "Live redaction tests: passed with 7 tests." in text
    assert "Live providers remain disabled by default." in text


def test_v1_6_optional_live_smoke_gate_live_tests_are_marked_live_and_skip() -> None:
    for path in LIVE_TESTS:
        text = _text(path)
        assert "@pytest.mark.live" in text
        assert "pytest.skip" in text
        assert "delenv" in text


def test_v1_6_optional_live_smoke_gate_docs_block_default_network() -> None:
    text = _combined([SCHOLAR_DOC, WEB_APIFY_DOC, SFTP_DOC, REDACTION_DOC, GO_NO_GO])

    assert "live skipped by default" in text
    assert "No-go Conditions Still In Force" in text
    assert "No live provider call by default." in text
    assert "No default network" in text or "no default network" in text
    assert "No automatic Evidence Ledger write" in text
    assert "No raw live output is retained." in text


def test_v1_6_optional_live_smoke_gate_is_public_safe() -> None:
    paths = [
        REPORT,
        GO_NO_GO,
        LANE,
        SCHOLAR_DOC,
        WEB_APIFY_DOC,
        SFTP_DOC,
        REDACTION_DOC,
    ]
    combined = _combined(paths)
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"
    private_win_drive = "D:" + "\\vggt"
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|"
        r"ghp_[A-Za-z0-9_]{8,}|"
        r"github_pat_[A-Za-z0-9_]{8,}|"
        r"BEGIN [A-Z ]*PRIVATE KEY)"
    )

    assert old_name not in combined
    assert private_drive not in combined
    assert private_win_drive not in combined
    assert token_like.search(combined) is None
    assert "https://" + "github.com/" not in combined
    assert "password" + "=" not in combined.lower()

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "live_output_redaction_gate.yaml"
DOC = ROOT / "docs" / "live-output-redaction-gate.md"
LANE = ROOT / "lanes" / "354_live_output_redaction_gate.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_live_output_redaction_contract_exists_and_lists_required_redactions() -> None:
    contract = _text(CONTRACT)

    assert "contract_id: live_output_redaction_gate" in contract
    assert "status: active" in contract
    for item in [
        "API keys",
        "tokens",
        "passwords",
        "private paths",
        "SSH host aliases",
        "local usernames",
        "cookies",
        "raw private content",
    ]:
        assert f"  - {item}" in contract


def test_live_output_redaction_contract_blocks_raw_output_and_evidence_write() -> None:
    contract = _text(CONTRACT)

    assert "no_raw_output_retained: true" in contract
    assert "no_automatic_evidence_write: true" in contract
    assert "requires_human_review: true" in contract
    assert "live_disabled_by_default: true" in contract
    assert "block_when_redactions_present: true" in contract


def test_live_output_redaction_docs_and_lane_record_gate() -> None:
    combined = "\n".join([_text(DOC), _text(LANE)])

    assert "Live Output Redaction Gate" in combined
    assert "API keys" in combined
    assert "tokens" in combined
    assert "passwords" in combined
    assert "private paths" in combined
    assert "SSH host aliases" in combined
    assert "local usernames" in combined
    assert "cookies" in combined
    assert "raw private content" in combined
    assert "No raw live output is retained." in combined
    assert "No automatic Evidence Ledger write." in combined

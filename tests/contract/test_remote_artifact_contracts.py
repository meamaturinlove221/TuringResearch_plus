from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "remote_artifacts.yaml"


def test_remote_artifact_contract_declares_all_sources() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "status: integration_gate" in text
    for source in ["github", "ssh_sftp", "nas_smb", "cloud_object"]:
        assert f"- {source}" in text


def test_remote_artifact_contract_preserves_evidence_boundary() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "proposed_imports_only: true" in text
    assert "no_evidence_ledger_auto_write: true" in text
    assert "no_human_verified_remote_artifacts: true" in text
    assert "no_default_network: true" in text

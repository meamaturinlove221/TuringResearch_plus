import json
from pathlib import Path

EXAMPLE_ROOT = Path("examples") / "vggt-human-prior-survey"


def test_vggt_visual_evidence_dry_run_outputs_are_conservative() -> None:
    scorecard = json.loads((EXAMPLE_ROOT / "visual_evidence_scorecard.json").read_text())
    report = (EXAMPLE_ROOT / "visual_evidence_audit_report.md").read_text(encoding="utf-8")
    missing_items = (EXAMPLE_ROOT / "visual_evidence_missing_items.md").read_text(
        encoding="utf-8"
    )

    assert scorecard["read_only"] is True
    assert scorecard["network_used"] is False
    assert scorecard["vggt_code_run"] is False
    assert scorecard["vggt_project_modified"] is False
    assert scorecard["advisor_ready_visual_proof"] is False
    assert scorecard["overall_status"] == "requires-human-review"
    assert scorecard["required_visual_evidence"]["full_body"] == "missing"
    assert scorecard["required_visual_evidence"]["hairline"] == "missing"
    assert scorecard["required_visual_evidence"]["hand_close_up"] == "missing"
    assert scorecard["claim_boundary"]["sparseconv3d_success"] == "not-enough-evidence"
    assert scorecard["inputs"]["local_scan_evidence_ledger.json"] == "local-observed"
    assert "blocked" in report
    assert "advisor-ready visual claim is allowed" in report
    assert "Mask boards without provenance" in missing_items


def test_vggt_visual_evidence_private_inputs_remain_uncommitted() -> None:
    assert not (EXAMPLE_ROOT / "local_project_links.yaml").exists()
    assert (EXAMPLE_ROOT / "local_scan_visual_inventory.md").exists()
    assert (EXAMPLE_ROOT / "local_scan_evidence_ledger.json").exists()

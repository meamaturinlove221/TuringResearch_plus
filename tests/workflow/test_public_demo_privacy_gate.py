from __future__ import annotations

from pathlib import Path

from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"


def test_public_demo_privacy_gate_has_no_release_blockers() -> None:
    report = scan_privacy_paths([PUBLIC_DEMO])

    assert report.requires_human_review is True
    assert report.release_blocker is False
    assert report.findings == []
    assert all("D:/vggt" not in path for path in report.scanned_paths)

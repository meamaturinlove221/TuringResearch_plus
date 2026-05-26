from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCAFFOLD = ROOT / "examples" / "vggt-human-prior-survey" / "paper_scaffold"


def test_paper_assembly_report_blocks_unready_sections() -> None:
    report = (SCAFFOLD / "paper_assembly_report.md").read_text(encoding="utf-8")

    assert "Gate status: `blocked`" in report
    assert "| Related Work | `blocked` |" in report
    assert "| Experiments | `blocked` |" in report
    assert "| Results | `blocked` |" in report
    assert "| Conclusion | `blocked` |" in report
    assert "Final abstract: `blocked`" in report
    assert "No final paper text is generated." in report


def test_paper_assembly_ready_sections_are_only_partial_or_review() -> None:
    ready = (SCAFFOLD / "ready_sections.md").read_text(encoding="utf-8")

    assert "No section is fully `ready`" in ready
    assert "`introduction`" in ready
    assert "`method`" in ready
    assert "Partial does not mean camera-ready." in ready
    assert "verified" in ready


def test_paper_assembly_blocked_sections_preserve_missing_evidence() -> None:
    blocked = (SCAFFOLD / "blocked_sections.md").read_text(encoding="utf-8")

    assert "`abstract`" in blocked
    assert "`related_work`" in blocked
    assert "`experiments`" in blocked
    assert "`results`" in blocked
    assert "result_tables_allowed=false" in blocked
    assert "SparseConv3D success is not established." in blocked
    assert "No planned item is promoted to observed." in blocked


def test_paper_assembly_inputs_remain_review_only() -> None:
    citation = (SCAFFOLD / "citation_safety_report.md").read_text(encoding="utf-8")
    result_guard = (SCAFFOLD / "result_table_missing_items.md").read_text(
        encoding="utf-8"
    )
    method = (SCAFFOLD / "method_section_skeleton.md").read_text(encoding="utf-8")

    assert "Fake fixtures are not final citations." in citation
    assert "Result tables allowed: `false`" in result_guard
    assert "No method verification is claimed." in method

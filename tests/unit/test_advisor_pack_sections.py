from pathlib import Path

from tests.unit.test_advisor_pack_builder import request_for_example

from turing_research_plus.advisor.pack_builder import build_advisor_pack
from turing_research_plus.advisor.sections import (
    render_current_status,
    render_evidence_summary,
    render_failure_analysis,
    render_next_actions,
    render_visual_readiness,
)


def test_sections_render_expected_titles() -> None:
    pack = build_advisor_pack(request_for_example(Path("unused")))

    assert render_current_status(pack).startswith("# Current Status")
    assert render_evidence_summary(pack).startswith("# Evidence Summary")
    assert render_visual_readiness(pack).startswith("# Visual Readiness")
    assert render_failure_analysis(pack).startswith("# Failure Analysis")
    assert render_next_actions(pack).startswith("# Next Actions")
    assert "Review-ready is not promotion" in render_failure_analysis(pack)


def test_pack_sections_are_addressable() -> None:
    pack = build_advisor_pack(request_for_example())

    assert pack.section("visual_readiness").title == "Visual Readiness"
    assert pack.section("next_actions").body.startswith("# Next Actions")

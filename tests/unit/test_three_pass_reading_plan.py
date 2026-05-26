from __future__ import annotations

from turing_research_plus.scholar_pipeline.reading_plan import build_three_pass_reading_plan


def test_three_pass_reading_plan_outputs_method_and_collision_tasks() -> None:
    plan = build_three_pass_reading_plan("p1", "VGGT Related Paper")

    assert "method card" in plan.outputs
    assert "collision notes" in plan.outputs
    assert "VGGT mapping" in plan.outputs
    assert plan.requires_real_paper_review is True
    assert plan.human_verified is False
    assert "Pass 1" in plan.to_markdown()

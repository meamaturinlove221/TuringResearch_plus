from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.north_star.models import NorthStarInput
from tuling_research_plus.north_star.service import NorthStarService
from tuling_research_plus.north_star.tools import (
    research_direction_rank,
    research_goal_decompose,
    research_north_star_init,
    research_obstacle_analyze,
    research_research_brief_generate,
)


class FakePaperService:
    def evidence_for_topic(self, topic: str) -> list[EvidenceRef]:
        return [EvidenceRef(source_id="paper", locator="abstract", quote=topic)]


def test_north_star_dry_run_tool_flow() -> None:
    service = NorthStarService(paper_service=FakePaperService())
    workflow_input = NorthStarInput(
        vague_user_intent="Agent workflow evaluation",
        current_research_context="Campaign runtime exists.",
        advisor_comments=["Focus on evaluation criteria."],
    )

    result = service.init(workflow_input)
    init_payload = research_north_star_init(workflow_input, service)
    brief_payload = research_research_brief_generate(
        workflow_input,
        result.north_star,
        service,
    )
    goal_payload = research_goal_decompose(result.research_brief, service)
    obstacle_payload = research_obstacle_analyze(workflow_input, service)
    direction_payload = research_direction_rank(workflow_input, service)

    assert init_payload["research_brief"]["problem"] == "Focus on evaluation criteria."
    assert brief_payload["title"]
    assert goal_payload["root"]["children"]
    assert obstacle_payload["obstacles"]
    assert (
        direction_payload["candidates"][0]["score"]
        >= direction_payload["candidates"][1]["score"]
    )

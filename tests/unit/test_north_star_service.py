from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.north_star.models import NorthStarInput, StartMode
from turing_research_plus.north_star.service import NorthStarService


class FakePaperService:
    def evidence_for_topic(self, topic: str) -> list[EvidenceRef]:
        return [
            EvidenceRef(
                source_id="paper-1",
                locator="abstract",
                quote=f"Paper evidence for {topic}.",
            )
        ]


class FakeWebService:
    def evidence_for_topic(self, topic: str) -> list[EvidenceRef]:
        return [
            EvidenceRef(
                source_id="web-1",
                locator="page",
                quote=f"Web evidence for {topic}.",
            )
        ]


def service() -> NorthStarService:
    return NorthStarService(paper_service=FakePaperService(), web_service=FakeWebService())


def test_hot_start_with_clear_topic() -> None:
    result = service().init(
        NorthStarInput(
            vague_user_intent="Build evidence gated research workflow runtime",
            current_research_context="Existing campaign runtime and survey modules.",
        )
    )

    assert result.north_star.mode == StartMode.HOT
    assert "evidence-backed workflow" in result.north_star.statement
    assert result.research_brief.evidence[0].source_id == "paper-1"


def test_warm_start_with_vague_field() -> None:
    result = service().init(
        NorthStarInput(
            vague_user_intent="AI research tools",
            current_research_context="",
        )
    )

    assert result.north_star.mode == StartMode.WARM
    assert result.goal_tree.root.children


def test_cold_start_with_no_direction() -> None:
    result = service().init(NorthStarInput())

    assert result.north_star.mode == StartMode.COLD
    assert "under-specified research direction" in result.north_star.statement


def test_obstacle_rejection_backtracks() -> None:
    result = service().init(
        NorthStarInput(
            vague_user_intent="Study private inaccessible data",
            known_constraints=["no data available"],
            current_research_context="Existing workflow.",
        )
    )

    assert result.backtracked is True
    assert result.obstacle_map.has_rejection is True
    assert result.direction_candidates.candidates[0].direction_id == "direction-2"
    assert result.direction_candidates.candidates[1].rejected is True

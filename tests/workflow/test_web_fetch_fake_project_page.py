from __future__ import annotations

from pathlib import Path

from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import (
    RetrievalStatus,
    SourceType,
    WebFetchRequest,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "examples" / "vggt-human-prior-survey" / "web_fetch_fixtures"


def test_vggt_project_page_fixtures_are_retrieved_without_network() -> None:
    fetcher = WebFetcher()
    results = [
        fetcher.fetch(
            WebFetchRequest(
                url=f"https://example.com/{name}",
                fixture_path=FIXTURE_ROOT / filename,
                source_type=SourceType.LOCAL_FIXTURE,
            )
        )
        for name, filename in [
            ("neuralbody", "neuralbody_project_page.fixture.html"),
            ("humanram", "humanram_project_page.fixture.html"),
        ]
    ]

    assert {result.retrieval_status for result in results} == {RetrievalStatus.RETRIEVED}
    assert all(result.source_metadata.human_verified is False for result in results)
    assert all(result.requires_human_review for result in results)
    assert "NeuralBody" in (results[0].text_content or "")
    assert "HumanRAM" in (results[1].text_content or "")

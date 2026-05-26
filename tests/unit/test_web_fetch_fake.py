from __future__ import annotations

from pathlib import Path

from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import (
    RetrievalStatus,
    SourceType,
    WebFetchRequest,
)

ROOT = Path(__file__).resolve().parents[2]


def test_fake_web_fetch_does_not_require_network() -> None:
    result = WebFetcher().fetch(WebFetchRequest(url="https://example.com/fake"))

    assert result.retrieval_status == RetrievalStatus.DRY_RUN
    assert result.source_type == SourceType.FAKE
    assert result.source_metadata.human_verified is False
    assert result.requires_human_review is True
    assert result.title == "Fake Web Fetch"


def test_fixture_web_fetch_extracts_title_and_text() -> None:
    fixture = (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "web_fetch_fixtures"
        / "neuralbody_project_page.fixture.html"
    )
    request = WebFetchRequest(
        url="https://example.com/neuralbody",
        fixture_path=fixture,
        source_type=SourceType.LOCAL_FIXTURE,
    )

    result = WebFetcher().fetch(request)

    assert result.retrieval_status == RetrievalStatus.RETRIEVED
    assert result.source_type == SourceType.LOCAL_FIXTURE
    assert result.title == "NeuralBody Project Page Fixture"
    assert "NeuralBody" in (result.text_content or "")
    assert result.source_metadata.human_verified is False


def test_blocked_source_hygiene_returns_no_content() -> None:
    result = WebFetcher().fetch(
        WebFetchRequest(
            url="https://example.com/private",
            source_hygiene_status="restricted",
        )
    )

    assert result.retrieval_status == RetrievalStatus.SOURCE_BLOCKED
    assert result.html_content is None
    assert result.requires_human_review is True

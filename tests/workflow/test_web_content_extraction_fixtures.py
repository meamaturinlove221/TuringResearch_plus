from __future__ import annotations

from pathlib import Path

from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import RetrievalStatus, SourceType, WebFetchRequest
from turing_research_plus.web.web_content_tool import web_content_from_fetch_result
from turing_research_plus.web_tools import build_web_cache_manifest_entry

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "examples" / "web_demo" / "content_fixtures"


def _fixture_result(name: str, url: str):
    fetcher = WebFetcher()
    return fetcher.fetch(
        WebFetchRequest(
            url=url,
            fixture_path=FIXTURES / name,
            dry_run=True,
            live_enabled=False,
        )
    )


def test_web_content_project_page_fixture_extracts_review_text() -> None:
    result = _fixture_result(
        "project_page.html",
        "https://example.com/demo-project?utm_source=test",
    )
    content = web_content_from_fetch_result(result)

    assert result.retrieval_status == RetrievalStatus.RETRIEVED
    assert result.source_type == SourceType.LOCAL_FIXTURE
    assert result.cache_hit is False
    assert content.title == "Demo Project Page"
    assert content.text_content is not None
    assert "local-first research workflow" in content.text_content
    assert "source metadata" in content.text_content
    assert "do-not-extract" not in content.text_content
    assert content.human_verified is False
    assert content.requires_human_review is True


def test_web_content_paper_fixture_stays_unverified_context() -> None:
    result = _fixture_result(
        "paper_abstract.html",
        "https://example.com/fake-paper",
    )
    content = web_content_from_fetch_result(result)

    assert content.text_content is not None
    assert "contribution notes" in content.text_content
    assert "does not verify any citation" in content.text_content
    assert content.human_verified is False
    assert "not human verified" in " ".join(content.limitations)


def test_noisy_fixture_removes_script_and_style_content() -> None:
    result = _fixture_result(
        "noisy_navigation.html",
        "https://example.com/noisy-page",
    )
    content = web_content_from_fetch_result(result)

    assert content.text_content is not None
    assert "Primary content explains extraction" in content.text_content
    assert "tracking-code-should-not-appear" not in content.text_content
    assert "color: #111" not in content.text_content


def test_fixture_extraction_can_emit_cache_manifest_entry() -> None:
    result = _fixture_result(
        "project_page.html",
        "https://example.com/demo-project?utm_source=test",
    )
    content = web_content_from_fetch_result(result)
    assert content.text_content is not None

    entry = build_web_cache_manifest_entry(
        source_url=result.url,
        content=content.text_content,
        fetch_time=result.retrieval_time,
        retrieval_status=result.retrieval_status,
        source_type=result.source_type,
        provider=result.source_metadata.provider,
    )

    assert entry.source_url == result.url
    assert entry.normalized_url == "https://example.com/demo-project"
    assert entry.fetch_time == result.retrieval_time
    assert len(entry.content_hash) == 64
    assert entry.network_used is False
    assert entry.release_blocker is False


def test_fixture_docs_mark_demo_safety_boundaries() -> None:
    readme = (FIXTURES / "README.md").read_text(encoding="utf-8")
    expected = (FIXTURES / "expected_extraction.md").read_text(encoding="utf-8")
    combined = f"{readme}\n{expected}".lower()

    assert "demo-only" in combined
    assert "no live network" in combined
    assert "no cookies" in combined
    assert "no paywall bypass" in combined
    assert "human review required" in combined
    assert "verified evidence" in combined

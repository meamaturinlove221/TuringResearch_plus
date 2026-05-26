from __future__ import annotations

import json
import re
from pathlib import Path

from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import RetrievalStatus, SourceType, WebFetchRequest
from turing_research_plus.web.web_content_tool import web_content_from_fetch_result
from turing_research_plus.web_tools import (
    WebCacheLiveStatus,
    build_web_cache_manifest_entry,
    normalize_url,
)

ROOT = Path(__file__).resolve().parents[2]
WEB_FIXTURES = ROOT / "examples" / "web_demo" / "content_fixtures"
APIFY_REPORT = ROOT / "examples" / "apify_workflows" / "fake_live_report"


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_web_production_gate_required_docs_exist() -> None:
    required = [
        "docs/url-normalization-hardening.md",
        "docs/web-cache-manifest.md",
        "docs/web-content-extraction-fixtures.md",
        "docs/apify-fake-live-integration-report.md",
        "docs/web-production-parity-gate-report.md",
        "docs/web-production-parity-go-no-go.md",
        "lanes/286_url_normalization_hardening.md",
        "lanes/287_web_cache_manifest.md",
        "lanes/288_web_content_extraction_fixtures.md",
        "lanes/289_apify_fake_live_integration_report.md",
    ]

    for path in required:
        assert (ROOT / path).exists(), path


def test_web_production_gate_url_normalization_passes() -> None:
    normalized = normalize_url("HTTPS://Example.COM:443//Project/?utm_source=x&b=2&a=1#top")

    assert normalized.normalized_url == "https://example.com/Project?a=1&b=2"
    assert normalized.web_meta["normUrl"] == normalized.normalized_url
    assert normalized.fragment_removed is True
    assert normalized.tracking_params_removed == ["utm_source"]
    assert len(normalized.cache_key) == 64


def test_web_production_gate_cache_manifest_passes() -> None:
    entry = build_web_cache_manifest_entry(
        source_url="https://example.com/project?utm_source=gate",
        content="fake web cache content for gate review",
    )

    assert entry.source_url == "https://example.com/project?utm_source=gate"
    assert entry.normalized_url == "https://example.com/project"
    assert entry.live_status == WebCacheLiveStatus.FAKE
    assert entry.network_used is False
    assert entry.human_verified is False
    assert entry.requires_human_review is True
    assert entry.release_blocker is False


def test_web_production_gate_content_fixtures_pass() -> None:
    result = WebFetcher().fetch(
        WebFetchRequest(
            url="https://example.com/demo-project",
            fixture_path=WEB_FIXTURES / "project_page.html",
            dry_run=True,
            live_enabled=False,
        )
    )
    content = web_content_from_fetch_result(result)

    assert result.retrieval_status == RetrievalStatus.RETRIEVED
    assert result.source_type == SourceType.LOCAL_FIXTURE
    assert content.text_content is not None
    assert "local-first research workflow" in content.text_content
    assert "do-not-extract" not in content.text_content
    assert content.human_verified is False
    assert content.requires_human_review is True


def test_web_production_gate_apify_fake_live_report_passes() -> None:
    report = json.loads((APIFY_REPORT / "fake_integration_report.json").read_text("utf-8"))
    skip_report = (APIFY_REPORT / "live_skip_report.md").read_text("utf-8").lower()

    assert report["mode"] == "fake"
    assert report["status"] == "dry-run"
    assert report["live_enabled"] is False
    assert report["network_used"] is False
    assert report["requires_token"] is False
    assert report["human_verified"] is False
    assert report["requires_human_review"] is True
    assert report["safety"]["private_content_scraping"] is False
    assert "skipped by default" in skip_report
    assert "not proof that apify live integration succeeded" in skip_report


def test_web_production_gate_docs_record_go_no_go_boundaries() -> None:
    combined = "\n".join(
        [
            _read("docs/web-production-parity-gate-report.md"),
            _read("docs/web-production-parity-go-no-go.md"),
            _read("docs/url-normalization-hardening.md"),
            _read("docs/web-cache-manifest.md"),
            _read("docs/web-content-extraction-fixtures.md"),
            _read("docs/apify-fake-live-integration-report.md"),
        ]
    ).lower()

    for boundary in [
        "url normalization pass",
        "cache manifest pass",
        "content fixtures pass",
        "apify fake/live report pass",
        "no default live",
        "no secrets",
        "no private scraping",
        "human review",
    ]:
        assert boundary in combined

    assert "go for v1.4 fake/default web production parity" in combined
    assert "no-go for default live network" in combined


def test_web_production_gate_has_no_secrets_or_private_scraping() -> None:
    combined = "\n".join(
        [
            _read("docs/web-production-parity-gate-report.md"),
            _read("docs/web-production-parity-go-no-go.md"),
            _read("docs/web-cache-manifest.md"),
            _read("docs/web-content-extraction-fixtures.md"),
            _read("docs/apify-fake-live-integration-report.md"),
            (APIFY_REPORT / "fake_integration_report.json").read_text("utf-8"),
        ]
    )

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assert not token_like.search(combined)
    assert "Tuling" + "Research" not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert "private_content_scraping: true" not in combined
    assert '"private_content_scraping": true' not in combined
    assert "default network use: false" in combined.lower()

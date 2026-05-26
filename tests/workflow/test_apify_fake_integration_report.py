from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.web.apify import ApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunStatus

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / "examples" / "apify_workflows"
REPORT = WORKFLOWS / "fake_live_report"
TEMPLATES = [
    WORKFLOWS / "project_page_fetch.yaml",
    WORKFLOWS / "search_result_fetch.yaml",
    WORKFLOWS / "content_extract.yaml",
]


def test_apify_fake_integration_report_matches_fake_adapter() -> None:
    payload = json.loads((REPORT / "fake_integration_report.json").read_text(encoding="utf-8"))
    result = ApifyAdapter().run(
        ApifyRunRequest(
            actor_id=payload["actor_id"],
            input={"url": "https://example.com/project-page"},
        )
    )

    assert result.status == ApifyRunStatus.DRY_RUN
    assert result.run_id == payload["run_id"]
    assert payload["mode"] == "fake"
    assert payload["live_enabled"] is False
    assert payload["network_used"] is False
    assert payload["requires_token"] is False
    assert payload["human_verified"] is False
    assert payload["requires_human_review"] is True
    assert payload["automatic_evidence_promotion"] is False
    assert result.requires_human_review is True


def test_apify_fake_live_report_references_all_templates() -> None:
    payload = json.loads((REPORT / "fake_integration_report.json").read_text(encoding="utf-8"))
    template_text = "\n".join(path.read_text(encoding="utf-8") for path in TEMPLATES)

    for template_id in payload["template_ids"]:
        assert template_id in template_text
    for path in TEMPLATES:
        text = path.read_text(encoding="utf-8")
        assert "live_enabled: false" in text
        assert "requires_token: false" in text
        assert "no_key_behavior: graceful_skip" in text


def test_apify_fake_live_docs_preserve_boundaries() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "docs" / "apify-fake-live-integration-report.md",
            REPORT / "README.md",
            REPORT / "live_skip_report.md",
            REPORT / "integration_summary.md",
        ]
    ).lower()

    assert "fake integration" in combined
    assert "live" in combined
    assert "skipped by default" in combined
    assert "no token" in combined
    assert "no apify request" in combined
    assert "no paywall bypass" in combined
    assert "no private content scraping" in combined
    assert "human review" in combined
    assert "not proof that apify live integration succeeded" in combined


def test_apify_fake_live_report_contains_no_secret_values() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in [*REPORT.rglob("*"), *TEMPLATES]
        if path.is_file()
    )

    assert "APIFY_TOKEN=" not in combined
    assert "ghp_" not in combined
    assert "sk-" not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined

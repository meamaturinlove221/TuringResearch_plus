from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.web.apify_models import ApifyRunStatus
from turing_research_plus.web.tools import apify_run_optional

ROOT = Path(__file__).resolve().parents[2]
SMOKE = ROOT / "examples" / "apify_workflows" / "live_smoke"
DOC = ROOT / "docs" / "web-apify-optional-live-smoke.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_web_apify_fake_smoke_files_are_public_safe() -> None:
    data = json.loads(_text(SMOKE / "fake_web_apify_smoke.json"))
    combined = "\n".join(
        _text(path)
        for path in [
            DOC,
            SMOKE / "README.md",
            SMOKE / "fake_web_apify_smoke.json",
            SMOKE / "expected_fake_smoke_report.md",
            SMOKE / "live_skip_report.md",
        ]
    )

    assert data["mode"] == "fake"
    assert data["requires_token"] is False
    assert data["live_mode_enabled"] is False
    assert data["network_used"] is False
    assert data["private_scraping"] is False
    assert data["login_bypass"] is False
    assert data["paywall_bypass"] is False
    assert data["cookie_storage"] is False
    assert data["requires_human_review"] is True
    assert data["automatic_evidence_promotion"] is False
    assert "`APIFY_TOKEN` optional" in combined
    assert "no token in repo" in combined
    assert "no private scraping" in combined
    assert "no login bypass" in combined
    assert "no paywall bypass" in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "D:" + "/vggt" not in combined
    assert "D:" + "\\vggt" not in combined


def test_web_apify_fake_smoke_runs_without_token() -> None:
    data = json.loads(_text(SMOKE / "fake_web_apify_smoke.json"))

    result = apify_run_optional(
        actor_id=data["actor_id"],
        input={"url": data["url"]},
        live_enabled=False,
        dry_run=True,
    )

    assert result.status == ApifyRunStatus.DRY_RUN
    assert result.actor_id == data["actor_id"]
    assert result.requires_human_review is True
    assert result.output_items
    assert result.output_items[0]["human_verified"] is False
    assert any("no Apify request" in warning for warning in result.warnings)


def test_web_apify_fake_smoke_docs_define_live_skip_policy() -> None:
    combined = "\n".join(
        [
            _text(DOC),
            _text(ROOT / "docs" / "web-apify-live-optional-guide.md"),
            _text(ROOT / "docs" / "optional-live-safety-policy.md"),
            _text(SMOKE / "live_skip_report.md"),
        ]
    )

    assert "live skipped by default" in combined
    assert "live requires explicit env" in combined
    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in combined
    assert "TURINGRESEARCH_ENABLE_WEB_LIVE=0" in combined
    assert "TURINGRESEARCH_ENABLE_APIFY_LIVE=0" in combined
    assert "APIFY_TOKEN=" in combined
    assert "APIFY_TOKEN=<private local value>" in combined
    assert "no cookie storage" in combined
    assert "no automatic Evidence Ledger write" in combined
    assert "live Web/Apify output is not observed evidence" in combined

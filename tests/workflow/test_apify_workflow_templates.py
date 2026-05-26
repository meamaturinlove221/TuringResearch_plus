from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / "examples" / "apify_workflows"
TEMPLATES = [
    WORKFLOWS / "project_page_fetch.yaml",
    WORKFLOWS / "search_result_fetch.yaml",
    WORKFLOWS / "content_extract.yaml",
]


def _read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_apify_workflow_templates_exist_and_are_fake_default() -> None:
    assert all(path.exists() for path in TEMPLATES)

    for path in TEMPLATES:
        text = _read_template(path)
        assert "status: template-only" in text
        assert "mode: fake-default" in text
        assert "live_enabled: false" in text
        assert "requires_token: false" in text
        assert "token_env: APIFY_TOKEN" in text
        assert "requires_human_review: true" in text


def test_apify_workflow_templates_preserve_safety_boundaries() -> None:
    for path in TEMPLATES:
        text = _read_template(path)
        assert "login_bypass: false" in text
        assert "paywall_bypass: false" in text
        assert "private_content_scraping: false" in text
        assert "stores_cookies: false" in text
        assert "automatic_evidence_promotion: false" in text
        assert "no_key_behavior: graceful_skip" in text
        assert "human_verified: false" in text


def test_apify_workflow_docs_explain_private_live_opt_in() -> None:
    docs = (ROOT / "docs" / "apify-workflow-templates.md").read_text(encoding="utf-8")
    readme = (WORKFLOWS / "README.md").read_text(encoding="utf-8")

    assert "APIFY_TOKEN is optional" in docs
    assert "live disabled by default" in docs
    assert "no login bypass" in docs
    assert "no private content scraping" in docs
    assert "TURINGRESEARCH_ENABLE_APIFY_LIVE=1" in docs
    assert "They are not executed by default" in readme


def test_apify_workflow_templates_contain_no_secret_or_private_path() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in [
            ROOT / "docs" / "apify-workflow-templates.md",
            WORKFLOWS / "README.md",
            *TEMPLATES,
        ]
    )

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
    assert "APIFY_TOKEN=" not in combined
    assert "observed " + "success" not in combined.lower()

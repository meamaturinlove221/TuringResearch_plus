from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.parity_showcase import (
    build_parity_showcase_page,
    render_parity_showcase_html,
    write_parity_showcase,
)

ROOT = Path(__file__).resolve().parents[2]
PARITY = ROOT / "examples" / "public_demo" / "dashboard_showcase" / "parity.html"
DOC = ROOT / "docs" / "parity-showcase-view.md"
LANE = ROOT / "lanes" / "330_parity_showcase_view.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_parity_showcase_model_contains_reference_repos_and_aris() -> None:
    page = build_parity_showcase_page()

    upstreams = [row.upstream for row in page.rows]
    assert upstreams == [
        "Neocortica-Session",
        "Neocortica-Scholar",
        "Neocortica-Web",
        "yogsoth-ai",
        "ARIS",
    ]
    assert page.status == "static-local-first-demo"
    assert "ARIS remains deferred." in page.safety_summary


def test_parity_showcase_example_matches_renderer() -> None:
    expected = render_parity_showcase_html()

    assert PARITY.exists()
    assert _text(PARITY) == expected
    assert "<script" not in expected.lower()
    assert "http://" not in expected
    assert "https://" not in expected


def test_parity_showcase_displays_required_columns() -> None:
    combined = "\n".join([_text(PARITY), _text(DOC), _text(LANE)])

    required = [
        "upstream capability",
        "our equivalent",
        "status",
        "tests",
        "docs",
        "safety enhancement",
        "deferred items",
        "ARIS deferred",
    ]
    for term in required:
        assert term in combined


def test_parity_showcase_write_helper(tmp_path: Path) -> None:
    output = write_parity_showcase(tmp_path / "parity.html")

    assert output.exists()
    assert output.read_text(encoding="utf-8") == render_parity_showcase_html()


def test_parity_showcase_records_our_enhancements() -> None:
    html = _text(PARITY)

    assert "manual confirmation before import" in html
    assert "no fake citation marked verified" in html
    assert "no private scraping" in html
    assert "No autonomous agent runtime" in html
    assert "research-automation and claim-authority risk" in html


def test_parity_showcase_public_safety() -> None:
    combined = "\n".join([_text(PARITY), _text(DOC), _text(LANE)])
    old_name = "Tuling" + "Research"

    forbidden = [
        old_name,
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "github_pat_",
        "sk-",
        "BEGIN OPENSSH PRIVATE KEY",
        "status" + ": observed",
        "deployed at",
        "live URL:",
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "No default network access." in combined
    assert "No remote command execution." in combined
    assert "No automatic Evidence Ledger write." in combined
    assert "No fake/demo result promotion." in combined

from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.interview_demo_view import (
    build_interview_demo_view,
    render_interview_demo_html,
    write_interview_demo_view,
)

ROOT = Path(__file__).resolve().parents[2]
INTERVIEW = ROOT / "examples" / "public_demo" / "dashboard_showcase" / "interview.html"
DOC = ROOT / "docs" / "interview-demo-dashboard-view.md"
LANE = ROOT / "lanes" / "331_interview_demo_view.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_interview_demo_view_model_contains_required_sections() -> None:
    view = build_interview_demo_view()

    assert view.status == "static-local-first-demo"
    assert [section.title for section in view.sections] == [
        "Architecture",
        "Modules",
        "Original Repo Parity",
        "Safety Gates",
        "Tests / Contracts",
        "Public Demo",
        "Split Strategy",
        "Why ARIS Deferred",
    ]
    assert len(view.closing_points) == 4


def test_interview_demo_view_example_matches_renderer() -> None:
    expected = render_interview_demo_html()

    assert INTERVIEW.exists()
    assert _text(INTERVIEW) == expected
    assert "<script" not in expected.lower()
    assert "http://" not in expected
    assert "https://" not in expected


def test_interview_demo_view_contains_requested_content() -> None:
    combined = "\n".join([_text(INTERVIEW), _text(DOC), _text(LANE)])

    required = [
        "Architecture",
        "Modules",
        "Original Repo Parity",
        "Safety Gates",
        "Tests / Contracts",
        "Public Demo",
        "Split Strategy",
        "Why ARIS Deferred",
        "3-10 minute",
    ]
    for term in required:
        assert term in combined


def test_interview_demo_view_write_helper(tmp_path: Path) -> None:
    output = write_interview_demo_view(tmp_path / "interview.html")

    assert output.exists()
    assert output.read_text(encoding="utf-8") == render_interview_demo_html()


def test_interview_demo_view_public_safety() -> None:
    combined = "\n".join([_text(INTERVIEW), _text(DOC), _text(LANE)])
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

    assert "does not run providers" in combined
    assert "No live provider call" in combined
    assert "No remote command execution" in combined
    assert "No planned or demo output promoted to observed evidence" in combined


def test_interview_demo_view_explains_aris_deferral() -> None:
    combined = "\n".join([_text(INTERVIEW), _text(DOC)])

    assert "ARIS deferred" in combined
    assert "cross-model review" in combined
    assert "proof checking" in combined
    assert "meta optimization" in combined
    assert "paper claim audit" in combined
    assert "research-automation and claim-authority risk" in combined

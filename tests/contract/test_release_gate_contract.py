from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_public_release_docs_exist_and_name_project_correctly() -> None:
    required = [
        "docs/public-release-checklist.md",
        "docs/public-readme-draft.md",
        "docs/release-plan.md",
        "docs/examples.md",
        "README.md",
    ]

    for relative in required:
        content = (ROOT / relative).read_text(encoding="utf-8")
        assert "TuringResearch Plus" in content
        assert "turingresearch-plus" in content or relative.endswith("examples.md")


def test_mcp_tools_document_marks_implemented_release_tools() -> None:
    content = (ROOT / "docs" / "mcp-tools.md").read_text(encoding="utf-8")

    for tool in [
        "race.idea_extract",
        "race.source_hygiene_check",
        "race.priority_score",
        "race.feature_capsule_create",
        "race.architecture_box_build",
        "race.upstream_watch",
        "paper.docflow_status",
        "paper.sop_graph_generate",
        "paper.figure_register",
        "paper.caption_generate",
        "paper.draft_generate",
        "paper.latex_export",
    ]:
        assert f"`{tool}`" in content
        line = next(line for line in content.splitlines() if f"`{tool}`" in line)
        assert "implemented_minimal" in line or "implemented_dry_run" in line


def test_no_forbidden_project_names_in_release_docs() -> None:
    checked_files = [
        "README.md",
        "docs/public-readme-draft.md",
        "docs/public-release-checklist.md",
        "docs/release-plan.md",
    ]
    forbidden = [
        "neo" + "cortica-plus",
        "neo" + "cortica_plus",
        "Neo" + "cortica++",
    ]

    for relative in checked_files:
        content = (ROOT / relative).read_text(encoding="utf-8")
        for value in forbidden:
            assert value not in content

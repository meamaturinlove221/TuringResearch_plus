from turing_research_plus.race.architecture_box import (
    build_architecture_boxes,
    race_architecture_box_build,
)


def test_default_architecture_has_16_boxes() -> None:
    result = build_architecture_boxes()

    assert len(result.boxes) == 16
    assert [box.name for box in result.boxes] == [
        "Idea Radar",
        "Priority Elevator",
        "Source Hygiene",
        "Upstream Watch",
        "Feature Capsule",
        "SOP Graph",
        "Core Paper Tools",
        "Core Web Tools",
        "PDF Markdown",
        "Semantic Graph",
        "Literature Survey",
        "Vault",
        "Context",
        "Hypothesis / Ideation",
        "Convergence / Stress / Experiment",
        "Paper / Figure Pipeline",
    ]


def test_every_box_has_owner_skill() -> None:
    result = build_architecture_boxes()

    assert all(box.owner_skill.startswith("turingresearch-") for box in result.boxes)
    assert all(box.public_tools for box in result.boxes)
    assert all(box.internal_modules for box in result.boxes)
    assert all(box.input_artifacts for box in result.boxes)
    assert all(box.output_artifacts for box in result.boxes)
    assert all(box.tests for box in result.boxes)
    assert all(box.priority in {"P0", "P1", "P2", "P3"} for box in result.boxes)


def test_no_orphan_dependency() -> None:
    result = build_architecture_boxes()
    box_ids = {box.box_id for box in result.boxes}

    for box in result.boxes:
        assert all(dependency in box_ids for dependency in box.dependencies)


def test_graph_generated() -> None:
    result = build_architecture_boxes()

    assert result.mermaid_graph.startswith("flowchart TD")
    assert 'B01["1. Idea Radar"]' in result.mermaid_graph
    assert "B03 --> B01" in result.mermaid_graph
    assert "B15 --> B16" in result.mermaid_graph


def test_tool_wrapper_returns_json_payload() -> None:
    payload = race_architecture_box_build()

    assert len(payload["boxes"]) == 16
    assert payload["boxes"][0]["owner_skill"] == "turingresearch-race-idea-radar"
    assert payload["mermaid_graph"].startswith("flowchart TD")

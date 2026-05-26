from pathlib import Path

import pytest

from turing_research_plus.experiment_route.parser import parse_experiment_route

FIXTURE = Path("examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml")


def test_parse_modal_sparseconv_fixture() -> None:
    route = parse_experiment_route(FIXTURE)

    assert route.route_id == "modal_sparseconv_v0"
    assert route.status == "requires-real-experiment"


def test_parse_route_rejects_non_mapping(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")

    with pytest.raises(ValueError, match="route spec"):
        parse_experiment_route(path)

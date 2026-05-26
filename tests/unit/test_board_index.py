from __future__ import annotations

from turing_research_plus.run_compare.board_index import board_ref_from_path, index_boards
from turing_research_plus.run_compare.models import BoardStatus, RunComparisonInput


def test_board_ref_from_path_marks_proxy_boards() -> None:
    board = board_ref_from_path("V129", "boards/hairline_delta.png")

    assert board.status == BoardStatus.PROXY_ONLY
    assert board.warnings == ["proxy board is not advisor-ready proof"]


def test_index_boards_records_missing_inventory() -> None:
    available, missing = index_boards([RunComparisonInput(run_id="V260")])

    assert available == []
    assert missing[0].run_id == "V260"
    assert missing[0].status == BoardStatus.MISSING


def test_index_boards_splits_available_and_missing() -> None:
    run = RunComparisonInput(
        run_id="V770",
        boards=[
            board_ref_from_path("V770", "boards/full_body.png"),
            board_ref_from_path("V770", "boards/proxy_mask.png"),
        ],
    )

    available, missing = index_boards([run])

    assert [item.board_id for item in available] == ["full_body.png"]
    assert [item.board_id for item in missing] == ["proxy_mask.png"]

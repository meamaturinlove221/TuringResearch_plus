"""Build a board index from lightweight run metadata."""

from __future__ import annotations

from collections.abc import Iterable

from turing_research_plus.run_compare.models import (
    BoardRef,
    BoardStatus,
    RunComparisonInput,
)


def index_boards(runs: Iterable[RunComparisonInput]) -> tuple[list[BoardRef], list[BoardRef]]:
    """Return available and missing board refs for comparison."""

    available: list[BoardRef] = []
    missing: list[BoardRef] = []
    for run in runs:
        if not run.boards:
            missing.append(
                BoardRef(
                    run_id=run.run_id,
                    board_id="board_inventory",
                    status=BoardStatus.MISSING,
                    warnings=["board inventory missing"],
                )
            )
            continue
        for board in run.boards:
            if board.status == BoardStatus.AVAILABLE:
                available.append(board)
            else:
                missing.append(board)
    return available, missing


def board_ref_from_path(run_id: str, path: str, board_type: str = "board") -> BoardRef:
    """Create a board reference from a path-like string."""

    lowered = path.lower()
    status = BoardStatus.AVAILABLE
    warnings: list[str] = []
    if any(marker in lowered for marker in ("mask", "delta", "proxy", "heatmap")):
        status = BoardStatus.PROXY_ONLY
        warnings.append("proxy board is not advisor-ready proof")
    return BoardRef(
        run_id=run_id,
        board_id=path.rsplit("/", 1)[-1].rsplit("\\", 1)[-1],
        path=path,
        status=status,
        board_type=board_type,
        warnings=warnings,
    )

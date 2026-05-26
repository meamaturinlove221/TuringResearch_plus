from __future__ import annotations

from turing_research_plus.collision.models import OverlapDimension
from turing_research_plus.collision.overlap import build_overlap_matrix, overlap_matrix_to_csv


def test_overlap_matrix_covers_required_dimensions() -> None:
    matrix = build_overlap_matrix(
        [
            {
                "paper_id": "neuralbody",
                "title": "NeuralBody",
                "task": "human reconstruction",
                "representation": ["SMPL structured latent", "sparse voxel"],
                "limitations": ["requires-real-paper-review"],
            }
        ]
    )

    dimensions = {row.dimension for row in matrix.rows}

    assert OverlapDimension.TASK in dimensions
    assert OverlapDimension.SMPL_SMPLX_ENCODING in dimensions
    assert OverlapDimension.VGGT_TOKEN_INTEGRATION in dimensions
    assert all(row.requires_real_paper_review for row in matrix.rows)


def test_overlap_matrix_exports_csv() -> None:
    matrix = build_overlap_matrix([{"paper_id": "p", "title": "SMPL-X voxel feature"}])

    csv = overlap_matrix_to_csv(matrix)

    assert csv.startswith("paper_id,dimension,score")
    assert '"p"' in csv

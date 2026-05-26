"""Overlap matrix construction."""

from __future__ import annotations

from turing_research_plus.collision.models import (
    OverlapDimension,
    OverlapMatrix,
    OverlapScore,
)

TARGET_TERMS = {
    OverlapDimension.TASK: {"point", "completion", "geometry", "reconstruction", "human"},
    OverlapDimension.INPUT: {"image", "pose", "camera", "smpl", "smpl-x"},
    OverlapDimension.OUTPUT: {"geometry", "point", "mesh", "rendered", "latent"},
    OverlapDimension.REPRESENTATION: {"voxel", "sparse", "triplane", "latent", "texture"},
    OverlapDimension.MODEL_COMPONENT: {"sparseconv", "transformer", "decoder", "raster"},
    OverlapDimension.HUMAN_PRIOR_USAGE: {"human", "body", "smpl", "smpl-x", "pose"},
    OverlapDimension.SMPL_SMPLX_ENCODING: {"smpl", "smpl-x", "canonical", "voxel"},
    OverlapDimension.VGGT_TOKEN_INTEGRATION: {"vggt", "token", "residual", "injection"},
    OverlapDimension.EVALUATION_TARGET: {"visual", "geometry", "full body", "hairline", "hand"},
    OverlapDimension.DATASET: {"dataset", "neuralbody", "humanram", "hart"},
    OverlapDimension.CLAIMED_CONTRIBUTION: {"contribution", "novel", "adapter", "feature"},
}


def build_overlap_matrix(compared_papers: list[dict[str, object]]) -> OverlapMatrix:
    """Build a conservative lexical overlap matrix."""

    rows: list[OverlapScore] = []
    for paper in compared_papers:
        paper_id = str(paper.get("paper_id") or paper.get("paperId") or paper.get("title"))
        text = _paper_text(paper)
        for dimension, terms in TARGET_TERMS.items():
            hits = [term for term in terms if term in text]
            score = min(len(hits) / max(len(terms), 1), 1.0)
            rows.append(
                OverlapScore(
                    paper_id=paper_id,
                    dimension=dimension,
                    score=round(score, 3),
                    rationale=_rationale(dimension, hits),
                    requires_real_paper_review=_requires_review(paper),
                )
            )
    return OverlapMatrix(rows=rows)


def overlap_matrix_to_csv(matrix: OverlapMatrix) -> str:
    """Render overlap matrix rows as CSV text."""

    lines = ["paper_id,dimension,score,requires_real_paper_review,rationale"]
    for row in matrix.rows:
        rationale = row.rationale.replace('"', '""')
        lines.append(
            f'"{row.paper_id}","{row.dimension}",{row.score},'
            f'{str(row.requires_real_paper_review).lower()},"{rationale}"'
        )
    return "\n".join(lines) + "\n"


def _paper_text(paper: dict[str, object]) -> str:
    parts: list[str] = []
    for value in paper.values():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif isinstance(value, dict):
            parts.extend(str(item) for item in value.values())
    return " ".join(parts).lower()


def _rationale(dimension: OverlapDimension, hits: list[str]) -> str:
    if hits:
        return f"Possible {dimension} overlap via terms: {', '.join(sorted(hits))}."
    return f"No strong {dimension} overlap in fixture text; requires review."


def _requires_review(paper: dict[str, object]) -> bool:
    text = _paper_text(paper)
    return (
        "fake-or-manual-note" in text
        or "requires-real-paper-review" in text
        or not paper.get("evidence_refs")
    )

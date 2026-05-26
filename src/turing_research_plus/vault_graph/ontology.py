"""Ontology SOP definitions and minimal execution records."""

from __future__ import annotations

from turing_research_plus.vault_graph.models import OntologySOPResult, VaultGraphStatus

ONTOLOGY_SOPS = [
    "seed-concept-search",
    "source-gathering",
    "concept-page-creation",
    "alias-resolution",
    "edge-batch-creation",
    "hierarchy-visualization",
    "gap-detection",
    "merge-candidates",
    "confidence-update",
    "ontology-export",
]


def list_ontology_sops() -> list[str]:
    """Return supported ontology SOP names."""

    return list(ONTOLOGY_SOPS)


def run_ontology_sop(
    sop_name: str,
    *,
    inputs: list[str] | None = None,
) -> OntologySOPResult:
    """Return a review-oriented SOP result without external side effects."""

    if sop_name not in ONTOLOGY_SOPS:
        raise ValueError(f"unsupported ontology SOP: {sop_name}")
    return OntologySOPResult(
        sop_name=sop_name,
        status=VaultGraphStatus.REVIEW,
        inputs=inputs or [],
        outputs=[f"{sop_name}-review-output"],
        required_human_review=True,
        notes=["SOP output is a planning/review artifact, not final ontology truth."],
    )

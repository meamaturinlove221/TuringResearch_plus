"""Structured output template generation."""

from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.git_handoff.models import (
    StructuredOutputFileName,
    StructuredOutputTemplate,
    json_stub,
)


def build_structured_output_template(
    *,
    template_id: str = "vggt-modal-sparseconv-output-template",
    route_id: str = "modal_sparseconv_real_v0",
) -> StructuredOutputTemplate:
    """Return structured output template metadata."""

    return StructuredOutputTemplate(
        template_id=template_id,
        route_id=route_id,
        instructions=[
            "Do not report planned work as executed.",
            "Do not claim SparseConv3D success without real sparse backend evidence.",
            "Return failure analysis even when the route fails.",
            "Populate SHA256SUMS.txt for all returned artifacts.",
        ],
        requires_human_review=True,
    )


def write_structured_output_template(output_dir: Path, template: StructuredOutputTemplate) -> None:
    """Write structured output template files to output_dir."""

    output_dir.mkdir(parents=True, exist_ok=True)
    run_status = json_stub(
        "replace-with-run-id",
        template.route_id,
        status="UNKNOWN",
        backend_status="unknown",
    )
    final_status = json_stub(
        "replace-with-run-id",
        template.route_id,
        status="UNKNOWN",
        promotion_status="not_promoted",
        sparseconv3d_success_claimed=False,
    )
    evidence_updates = {
        "updates": [],
        "policy": "proposed updates only; do not overwrite Evidence Ledger automatically",
        "requires_human_review": True,
    }
    _write_json(output_dir / StructuredOutputFileName.RUN_STATUS.value, run_status)
    _write_json(output_dir / StructuredOutputFileName.FINAL_STATUS.value, final_status)
    (output_dir / StructuredOutputFileName.ARTIFACT_INDEX.value).write_text(
        "# Artifact Index\n\n- Populate returned artifacts here.\n",
        encoding="utf-8",
    )
    (output_dir / StructuredOutputFileName.FAILURE_REPORT.value).write_text(
        "# Failure Report\n\nRecord failure categories, evidence refs, and next actions.\n",
        encoding="utf-8",
    )
    _write_json(
        output_dir / StructuredOutputFileName.PROPOSED_EVIDENCE_UPDATES.value,
        evidence_updates,
    )
    (output_dir / StructuredOutputFileName.ADVISOR_SUMMARY_DRAFT.value).write_text(
        "# Advisor Summary Draft\n\nDo not claim experimental success without evidence.\n",
        encoding="utf-8",
    )
    (output_dir / StructuredOutputFileName.SHA256SUMS.value).write_text(
        "# Fill with sha256 sums for returned artifacts.\n",
        encoding="utf-8",
    )
    (output_dir / "README.md").write_text(template.to_markdown(), encoding="utf-8")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

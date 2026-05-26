from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.artifact_audit.auditor import audit_artifacts
from turing_research_plus.artifact_audit.models import ArtifactAuditInput
from turing_research_plus.git_handoff.memory_policy import validate_memory_text
from turing_research_plus.pod_workflow.models import PodWorkflowPackBuildInput
from turing_research_plus.pod_workflow.pack_builder import build_vggt_modal_pod_workflow_pack
from turing_research_plus.run_ingest.local_bundle_ingestor import ingest_local_bundle
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType

ROUTE_PACK = Path("examples") / "vggt-human-prior-survey" / "modal_sparseconv_route_pack"


def test_context_handoff_flow_builds_review_only_pod_pack(tmp_path: Path) -> None:
    pack = build_vggt_modal_pod_workflow_pack(
        PodWorkflowPackBuildInput(route_pack_dir=ROUTE_PACK, output_dir=tmp_path)
    )

    assert pack.context_package.requires_human_review is True
    assert pack.context_package.git_transport_policy.remote_execution_allowed is False
    assert (tmp_path / "PROJECT_CONTEXT.md").exists()
    assert (tmp_path / "MEMORY.md").exists()
    assert (tmp_path / "STRUCTURED_OUTPUT_TEMPLATE" / "FINAL_STATUS.json").exists()
    memory = (tmp_path / "MEMORY.md").read_text(encoding="utf-8")
    memory_warnings = validate_memory_text(memory)
    assert "possible-secret-value" not in memory_warnings
    assert "memory-cannot-be-only-source-of-truth" not in memory_warnings
    final_status = json.loads(
        (tmp_path / "STRUCTURED_OUTPUT_TEMPLATE" / "FINAL_STATUS.json").read_text(
            encoding="utf-8"
        )
    )
    assert final_status["execution_status"] == "not_executed_by_turingresearch"
    assert final_status["sparseconv3d_success_claimed"] is False


def test_return_flow_template_to_run_ingest_and_artifact_audit(tmp_path: Path) -> None:
    pack = build_vggt_modal_pod_workflow_pack(
        PodWorkflowPackBuildInput(route_pack_dir=ROUTE_PACK, output_dir=tmp_path)
    )
    output = tmp_path / "STRUCTURED_OUTPUT_TEMPLATE"
    (output / "final_status.json").write_text(
        json.dumps(
            {
                "run_id": "v0.3-sprint1-fixture",
                "route_id": pack.route_id,
                "status": "UNKNOWN",
                "backend_status": "real_backend_missing",
                "artifacts": ["failure_report.md"],
            }
        ),
        encoding="utf-8",
    )

    ingest = ingest_local_bundle(
        RunIngestRequest(
            source_type=RunSourceType.THIN_REVIEW_BUNDLE,
            source_path=output,
            route_id=pack.route_id,
        )
    )
    audit = audit_artifacts(ArtifactAuditInput(source_path=output / "ARTIFACT_INDEX.md"))

    assert ingest.evidence_updates[0]["status"] == "not-enough-evidence"
    assert "predictions.npz" in ingest.missing_artifacts
    assert audit.warnings
    assert ingest.requires_human_review is True
    assert all(update["status"] != "observed" for update in ingest.evidence_updates)

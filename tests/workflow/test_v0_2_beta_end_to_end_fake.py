from __future__ import annotations

from pathlib import Path

from turing_research_plus.adapters.fake import FakeSemanticScholarAdapter
from turing_research_plus.artifact_audit.auditor import audit_artifacts
from turing_research_plus.artifact_audit.models import ArtifactAuditInput
from turing_research_plus.citation_graph.expander import CitationGraphExpander
from turing_research_plus.citation_graph.markdown_export import citation_graph_to_markdown
from turing_research_plus.collision.models import PaperComparisonInput
from turing_research_plus.collision.tools import collision_risk_detect
from turing_research_plus.experiment_route.compiler import compile_experiment_route
from turing_research_plus.experiment_route.models import ExperimentRouteCompileInput
from turing_research_plus.failure.attribution import build_failure_attribution_report
from turing_research_plus.failure.models import FailureCategory, FailureInstance
from turing_research_plus.handoff.importer import import_handoff_bundle
from turing_research_plus.handoff.models import HandoffImportRequest
from turing_research_plus.hard_gates.models import GateInputRef, HardGateValidationInput
from turing_research_plus.hard_gates.validator import validate_hard_gates
from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.markdown_export import export_method_card_markdown
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType
from turing_research_plus.run_ingest.local_bundle_ingestor import ingest_local_bundle
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType
from turing_research_plus.vggt.evidence_ledger import build_vggt_evidence_ledger
from turing_research_plus.vggt.evidence_models import VGGTEvidenceLedgerBuildInput

EXAMPLE = Path("examples") / "vggt-human-prior-survey"
ROUTE = EXAMPLE / "route_specs" / "modal_sparseconv_v0.yaml"
RUN_FIXTURE = EXAMPLE / "run_ingest_fixtures" / "modal_run_fixture"
HANDOFF_FIXTURE = EXAMPLE / "handoff_bundle_fixture"
METHOD_FIXTURE = EXAMPLE / "paper_method_cards" / "neuralbody.fixture.md"
ARTIFACT_INDEX = EXAMPLE / "local_scan_artifact_index.md"
SUMMARY = EXAMPLE / "local_scan_summary.md"


def test_beta_paper_intelligence_fake_flow() -> None:
    graph = CitationGraphExpander(
        adapter=FakeSemanticScholarAdapter()
    ).fake_vggt_related_work_graph()
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=METHOD_FIXTURE,
        )
    )
    collision = collision_risk_detect(
        PaperComparisonInput(
            compared_papers=[
                card.model_dump(mode="json"),
                {
                    "paper_id": "hart-requires-review",
                    "title": "HART",
                    "task": "human reconstruction",
                    "representation": ["requires-real-paper-review"],
                },
            ],
            citation_graph=graph.model_dump(mode="json"),
        )
    )

    assert graph.model_dump(mode="json")
    assert card.model_dump(mode="json")
    assert collision.model_dump(mode="json")
    assert "# Citation Graph:" in citation_graph_to_markdown(graph)
    assert "# Method Card:" in export_method_card_markdown(card)
    assert collision.safe_claims
    assert collision.unsafe_claims
    assert collision.requires_human_review is True
    assert all(not node.human_verified for node in graph.nodes)
    assert "definitively no collision" not in " ".join(
        claim.text.lower() for claim in collision.safe_claims
    )


def test_beta_experiment_intelligence_fake_flow() -> None:
    route, prompt = compile_experiment_route(ExperimentRouteCompileInput(route_path=ROUTE))
    gate_report = validate_hard_gates(
        HardGateValidationInput(
            route_id=route.route_id,
            gate_ids=["real_backend_required", "visual_board_required"],
            inputs=[
                GateInputRef(
                    ref_id="real_backend_required",
                    ref_type="backend",
                    status="requires-real-experiment",
                    summary="real backend has not run",
                )
            ],
        )
    )
    run_report = ingest_local_bundle(
        RunIngestRequest(
            source_type=RunSourceType.MODAL_FIXTURE,
            source_path=RUN_FIXTURE,
            route_id=route.route_id,
        )
    )
    failure = build_failure_attribution_report(
        FailureInstance(
            failure_id="beta-run-ingest",
            related_route_id=route.route_id,
            related_run_id=run_report.run_id,
            text="missing board proof and no real experiment evidence",
        )
    )
    ledger = build_vggt_evidence_ledger(
        VGGTEvidenceLedgerBuildInput(
            local_scan_summary_path=SUMMARY,
            local_scan_artifact_index_path=ARTIFACT_INDEX,
            local_scan_evidence_ledger_path=EXAMPLE / "local_scan_evidence_ledger.json",
        )
    )

    assert route.model_dump(mode="json")
    assert prompt.model_dump(mode="json")
    assert gate_report.model_dump(mode="json")
    assert run_report.model_dump(mode="json")
    assert failure.model_dump(mode="json")
    assert ledger.model_dump(mode="json")
    assert gate_report.passed is False
    assert run_report.evidence_updates[0]["status"] == "not-enough-evidence"
    assert FailureCategory.REAL_BACKEND_UNAVAILABLE in run_report.failure_categories
    assert FailureCategory.SPARSE_BACKEND_UNAVAILABLE in run_report.failure_categories
    assert failure.requires_human_review is True
    assert ledger.row_for("V999-SparseConv3D").status.value == "not-enough-evidence"
    assert "not executed by TuringResearch" in route.final_states


def test_beta_artifact_handoff_advisor_inputs_fake_flow() -> None:
    artifact_report = audit_artifacts(ArtifactAuditInput(source_path=ARTIFACT_INDEX))
    handoff_report = import_handoff_bundle(HandoffImportRequest(bundle_dir=HANDOFF_FIXTURE))
    failure = build_failure_attribution_report(
        FailureInstance(
            failure_id="beta-handoff-review",
            text="handoff bundle requires human review before evidence ledger update",
        )
    )
    advisor_inputs = {
        "artifact_report_id": artifact_report.report_id,
        "handoff_bundle_id": handoff_report.bundle_id,
        "failure_id": failure.failure_id,
        "visual_status": "requires-human-review",
        "collision_status": "requires-human-review",
    }

    assert artifact_report.model_dump(mode="json")
    assert handoff_report.model_dump(mode="json")
    assert "# Handoff Import Report:" in handoff_report.to_markdown()
    assert handoff_report.proposed_updates[0]["status"] == "requires-human-review"
    assert all("SMPLX" not in path for path in handoff_report.verified_files)
    assert handoff_report.manual_review_required is True
    assert advisor_inputs["handoff_bundle_id"] == "handoff_bundle_fixture"

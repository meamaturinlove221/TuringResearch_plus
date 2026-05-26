from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.markdown_bundle import (
    build_advisor_markdown_bundle,
)
from turing_research_plus.advisor_export.models import AdvisorMarkdownBundleRequest
from turing_research_plus.collision.models import PaperComparisonInput
from turing_research_plus.collision.tools import collision_risk_detect
from turing_research_plus.dashboard.run_dashboard import build_run_dashboard
from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import GitHubArtifactSyncRequest
from turing_research_plus.object_store.importer import build_object_artifact_index
from turing_research_plus.object_store.index import load_object_artifact_index
from turing_research_plus.object_store.models import ObjectArtifactIndexRequest
from turing_research_plus.paper_digest.digest_builder import build_paper_digest
from turing_research_plus.paper_digest.method_bridge import digest_to_method_card
from turing_research_plus.paper_digest.models import (
    PaperDigestInput,
    PaperDigestSourceStatus,
)
from turing_research_plus.related_work.models import RelatedWorkPositioningInput
from turing_research_plus.related_work.positioning import build_related_work_positioning
from turing_research_plus.remote_artifacts.models import RemoteArtifactSourceKind
from turing_research_plus.remote_artifacts.unified_report import (
    build_unified_remote_artifact_report,
)
from turing_research_plus.remote_readers.models import RemoteReaderRequest
from turing_research_plus.remote_readers.tools import read_remote_artifacts
from turing_research_plus.run_compare.comparator import compare_runs, input_from_dashboard
from turing_research_plus.run_ingest.modal_ingestor import ingest_modal_run
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType
from turing_research_plus.shared_store.local_mount_reader import scan_local_mount
from turing_research_plus.shared_store.models import SharedStoreScanRequest

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey"


def test_v0_4_remote_artifact_to_review_inputs_fake() -> None:
    github_report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="example/vggt-review-artifacts",
            source_ref="modal-sparseconv-review",
            fixture_index_path=EXAMPLE
            / "github_artifact_sync_fixture"
            / "artifact_index.json",
        )
    )
    remote_report = read_remote_artifacts(
        RemoteReaderRequest(
            host_label="fake-vggt-remote",
            root_path="/remote/vggt/review_bundle",
            fixture_index_path=EXAMPLE / "remote_reader_fixture" / "artifact_index.json",
        )
    )
    shared_report = scan_local_mount(
        SharedStoreScanRequest(
            mount_label="fake-shared-store",
            root_path=EXAMPLE / "shared_store_fixture",
        )
    )
    fixture_index = load_object_artifact_index(
        EXAMPLE / "object_store_fixture" / "artifact_index.json"
    )
    object_index = build_object_artifact_index(
        ObjectArtifactIndexRequest(
            provider=fixture_index.provider,
            bucket_or_container=fixture_index.bucket_or_container,
            prefix=fixture_index.prefix,
        ),
        objects=fixture_index.objects,
    )

    report = build_unified_remote_artifact_report(
        github_reports=[github_report],
        remote_reader_reports=[remote_report],
        shared_store_reports=[shared_report],
        object_indexes=[object_index],
    )

    assert {source.kind for source in report.sources} == {
        RemoteArtifactSourceKind.GITHUB,
        RemoteArtifactSourceKind.SSH_SFTP,
        RemoteArtifactSourceKind.NAS_SMB,
        RemoteArtifactSourceKind.CLOUD_OBJECT,
    }
    assert report.proposed_imports
    assert report.requires_human_review is True
    assert report.human_verified is False
    assert report.unsafe_artifacts


def test_v0_4_dashboard_to_run_comparison_fake() -> None:
    run_report = ingest_modal_run(
        RunIngestRequest(
            source_type=RunSourceType.MODAL_FIXTURE,
            source_path=EXAMPLE / "run_ingest_fixtures" / "modal_run_fixture",
        )
    )
    dashboard = build_run_dashboard(run_report)
    comparison = compare_runs([input_from_dashboard(dashboard)])

    assert dashboard.experiment_executed_by_dashboard is False
    assert dashboard.backend_status == "real_backend_missing"
    assert "modal-sparseconv-fixture-001" in comparison.compared_runs
    assert any("real sparse backend evidence" in item for item in comparison.next_actions)
    assert any(
        "SparseConv3D success requires real backend evidence" in item
        for item in comparison.unsupported_claims
    )


def test_v0_4_paper_digest_to_related_work_and_collision_fake() -> None:
    text = (EXAMPLE / "paper_method_cards" / "humanram.fixture.md").read_text(
        encoding="utf-8"
    )
    digest = build_paper_digest(
        PaperDigestInput(
            paper_id="humanram-fixture",
            title="HumanRAM Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            source_text=text,
        )
    )
    method_card = digest_to_method_card(digest)
    collision_request = PaperComparisonInput(
        target_project="VGGT/SMPL-X feature adapter",
        compared_papers=[method_card.model_dump(mode="json")],
        source_status="fake-or-manual-note",
    )
    collision = collision_risk_detect(collision_request)
    related = build_related_work_positioning(
        RelatedWorkPositioningInput(
            method_cards=[method_card.model_dump(mode="json")],
            collision_report=collision.model_dump(mode="json"),
        )
    )

    assert collision_request.source_status == "fake-or-manual-note"
    assert digest.requires_real_paper is True
    assert method_card.requires_human_review is True
    assert collision.requires_human_review is True
    assert related.requires_human_review is True
    assert related.unsafe_claims


def test_v0_4_vggt_knowledge_to_advisor_markdown_bundle_fake(tmp_path: Path) -> None:
    manifest = (EXAMPLE / "research_knowledge_pack" / "manifest.yaml").read_text(
        encoding="utf-8"
    )
    route_pack = (EXAMPLE / "modal_sparseconv_route_pack" / "README.md").read_text(
        encoding="utf-8"
    )
    bundle = build_advisor_markdown_bundle(
        AdvisorMarkdownBundleRequest(
            output_dir=tmp_path,
            advisor_pack_dir=EXAMPLE / "advisor_pack",
            knowledge_pack_dir=EXAMPLE / "research_knowledge_pack",
        )
    )
    report_source = (tmp_path / "advisor_report_source.md").read_text(encoding="utf-8")

    assert "no_sparseconv3d_success_claim" in manifest
    assert "not executed" in route_pack.lower()
    assert bundle.generated_pdf is False
    assert bundle.generated_pptx is False
    assert "Planned work is not observed evidence" in report_source
    assert "SparseConv3D success is not claimed" in report_source

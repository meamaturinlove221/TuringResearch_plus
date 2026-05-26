from __future__ import annotations

import importlib
import json
from pathlib import Path

from turing_research_plus.case_study.gallery import (
    load_case_gallery_manifest,
    render_case_gallery_markdown,
)
from turing_research_plus.dashboard_api.export import (
    build_public_demo_dashboard_data,
    export_json,
)
from turing_research_plus.docs_site.builder import build_docs_site_from_repo
from turing_research_plus.local_server.app import create_local_dashboard_server
from turing_research_plus.local_server.models import LocalDashboardRequest
from turing_research_plus.local_server.tools import preview_public_demo_route
from turing_research_plus.paper_write.claim_guard import evaluate_paper_claims
from turing_research_plus.paper_write.draft_assembly import assemble_paper_draft_beta
from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permission
from turing_research_plus.plugins.sandbox_policy import (
    SandboxDecisionStatus,
    SandboxPermission,
)
from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
SPLIT_READY = ROOT / "split_ready"
GALLERY_MANIFEST = PUBLIC_DEMO / "case_gallery" / "gallery_manifest.yaml"
PAPER_SCAFFOLD = (
    ROOT / "examples" / "vggt-human-prior-survey" / "paper_scaffold"
)
WORKFLOWS = ROOT / ".github" / "workflows"

NAMESPACES = [
    "turing_research_plus",
    "turing_research_core",
    "turing_research_paper",
    "turing_research_artifact",
    "turing_research_experiment",
    "turing_research_dashboard",
    "turing_research_plugins",
    "turing_research_cases",
]


def test_v1_1_full_fake_replay_main_entry_and_namespace_compatibility() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "docs" / "quickstart.md").read_text(encoding="utf-8")
    mcp_config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))

    for namespace in NAMESPACES:
        assert importlib.import_module(namespace) is not None

    for namespace in NAMESPACES[1:]:
        public_api = importlib.import_module(f"{namespace}.public_api")
        assert public_api.COMPATIBILITY_NAMESPACE == "turing_research_plus"

    env = mcp_config["mcpServers"]["turingresearch-plus"]["env"]
    assert "v1.0 Public Quickstart" in readme
    assert "Planned Split Repositories" in readme
    assert "live" in quickstart.lower()
    assert "disabled" in quickstart.lower()
    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"


def test_v1_1_full_fake_replay_docs_dashboard_and_local_server(
    tmp_path: Path,
) -> None:
    site = build_docs_site_from_repo(ROOT, output_root=tmp_path / "site")
    dashboard = json.loads(export_json(build_public_demo_dashboard_data(PUBLIC_DEMO)))
    server = create_local_dashboard_server(
        LocalDashboardRequest(repo_root=ROOT, public_demo_dir=PUBLIC_DEMO, port=0)
    )
    try:
        assert server.server_address[0] == "127.0.0.1"
        assert server.request_config.safety.localhost_only is True
        assert server.request_config.safety.read_only is True
        assert server.request_config.safety.executes_commands is False
    finally:
        server.server_close()

    generated = {path.name for path in site.generated_files}
    assert {"index.html", "showcase.html", "case-study-gallery.html"} <= generated
    assert dashboard["read_only"] is True
    assert dashboard["supports_json_export"] is True
    assert dashboard["no_secrets"] is True
    assert dashboard["no_raw_data"] is True
    assert preview_public_demo_route(ROOT, "/dashboard")["status_code"] == 200


def test_v1_1_full_fake_replay_split_bundles_demo_cases_and_gallery() -> None:
    required_split_dirs = [
        SPLIT_READY / "turingresearch-vggt-case",
        SPLIT_READY / "turingresearch-examples",
    ]
    manifest = load_case_gallery_manifest(GALLERY_MANIFEST)
    gallery_markdown = render_case_gallery_markdown(manifest)

    for split_dir in required_split_dirs:
        readme = (split_dir / "README.md").read_text(encoding="utf-8")
        safety = (split_dir / "safety_report.md").read_text(encoding="utf-8")
        assert "not yet a GitHub repository" in readme
        assert "flagship" in readme.lower()
        assert "safe_to_export" in safety
        assert "release_blocker" in safety
        assert "false" in safety.lower()

    assert len(manifest.cases) >= 5
    assert "vggt_public_safe_case" in gallery_markdown
    assert "robotics_paper_survey_demo" in gallery_markdown
    assert "medical_imaging_experiment_demo" in gallery_markdown
    assert "Demo outputs are not observed research evidence." in gallery_markdown


def test_v1_1_full_fake_replay_paper_beta_and_plugin_safety() -> None:
    package = assemble_paper_draft_beta(PAPER_SCAFFOLD)
    claim_report = evaluate_paper_claims(
        {
            "blocked": "Do not report SparseConv3D success without evidence.",
            "risky": "SparseConv3D success improves all benchmark results.",
        }
    )
    execute_code = evaluate_sandbox_permission(SandboxPermission.EXECUTE_CODE)
    secrets_access = evaluate_sandbox_permission(SandboxPermission.SECRETS_ACCESS)

    assert "Result tables allowed: `false`" in package.results_blocked_section
    assert "Fake observed claim blocked: `true`" in package.unsafe_claim_report
    assert "Fabricated citation blocked: `true`" in package.citation_status_report
    assert claim_report.blocked_claims
    assert claim_report.risky_unblocked_claims
    assert execute_code.status == SandboxDecisionStatus.DENIED
    assert secrets_access.status == SandboxDecisionStatus.DENIED


def test_v1_1_full_fake_replay_privacy_and_ci_workflow_boundaries() -> None:
    privacy = scan_privacy_paths([PUBLIC_DEMO])
    workflow_text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [
            WORKFLOWS / "ci.yml",
            WORKFLOWS / "docs-check.yml",
            WORKFLOWS / "privacy-gate.yml",
        ]
    )

    assert privacy.release_blocker is False
    assert privacy.findings == []
    assert "actions/checkout" in workflow_text
    assert "actions/setup-python" in workflow_text
    assert "test_v1_1_paper_demo_integration.py" in workflow_text
    assert "turingresearch_enable_live_tests: \"0\"" in workflow_text
    assert "actions/upload-artifact" not in workflow_text
    assert "secrets." not in workflow_text
    assert "pypi" not in workflow_text
    assert "gh release" not in workflow_text
    assert "git tag" not in workflow_text

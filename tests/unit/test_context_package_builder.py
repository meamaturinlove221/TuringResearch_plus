from __future__ import annotations

from pathlib import Path

from turing_research_plus.git_handoff.context_package import build_context_package
from turing_research_plus.git_handoff.models import ContextPackageBuildInput


def test_context_package_builder_writes_required_files(tmp_path: Path) -> None:
    package = build_context_package(
        ContextPackageBuildInput(
            output_dir=tmp_path,
            project_context="VGGT route context.",
            memory_summary="Route planned. Evidence Ledger remains source of truth.",
            route_spec_text="route_id: modal_sparseconv_real_v0\nstatus: planned\n",
            hard_gates_text="# Hard Gates\n\n- real backend required\n",
            artifact_requirements_text="# Artifact Requirements\n\n- final_status.json\n",
            failure_taxonomy_text="# Failure Taxonomy\n\n- NOT_ENOUGH_EVIDENCE\n",
            advisor_intent="Summarize status without overclaiming.",
        )
    )

    required = {
        "PROJECT_CONTEXT.md",
        "MEMORY.md",
        "ROUTE_SPEC.yaml",
        "HARD_GATES.md",
        "ARTIFACT_REQUIREMENTS.md",
        "FAILURE_TAXONOMY.md",
        "ADVISOR_INTENT.md",
        "HANDOFF_MANIFEST.yaml",
        "README.md",
        "SHA256SUMS.txt",
        "context_package.json",
    }
    assert required <= {path.name for path in tmp_path.iterdir()}
    assert package.route_id == "modal_sparseconv_real_v0"
    assert set(package.sha256_manifest) >= {
        "PROJECT_CONTEXT.md",
        "MEMORY.md",
        "ROUTE_SPEC.yaml",
    }
    assert package.omitted_items == []


def test_context_package_builder_omits_secret_like_memory(tmp_path: Path) -> None:
    package = build_context_package(
        ContextPackageBuildInput(
            output_dir=tmp_path,
            project_context="safe context",
            memory_summary="API_KEY=secretvalue12345",
            route_spec_text="route_id: route\n",
            hard_gates_text="gates",
            artifact_requirements_text="requirements",
            failure_taxonomy_text="taxonomy",
            advisor_intent="intent",
        )
    )

    assert any(item.item == "MEMORY.md" for item in package.omitted_items)
    assert not (tmp_path / "MEMORY.md").exists()

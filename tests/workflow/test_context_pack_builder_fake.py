from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.context_pack_builder import (
    ContextPackBuildRequest,
    build_context_pack,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "session_runtime" / "context_pack_fixture"


def test_context_pack_builder_fake_fixture_builds_safe_pack(tmp_path: Path) -> None:
    manifest = build_context_pack(
        ContextPackBuildRequest(
            package_id="ctx-v1-3-fake-pack",
            route_id="route-session-runtime-fake",
            source_dir=FIXTURE / "source",
            output_dir=tmp_path / "context_pack",
        )
    )

    output = tmp_path / "context_pack"
    required = {
        "PROJECT_CONTEXT.md",
        "MEMORY.md",
        "ROUTE_SPEC.yaml",
        "HARD_GATES.md",
        "ARTIFACT_REQUIREMENTS.md",
        "FAILURE_TAXONOMY.md",
        "HANDOFF_MANIFEST.yaml",
        "SHA256SUMS.txt",
    }
    assert required <= {path.name for path in output.iterdir()}
    assert manifest.missing_required_files == []
    assert manifest.remote_execution_allowed is False
    assert manifest.live_network_allowed is False
    assert manifest.proposed_updates_only is True
    assert manifest.requires_human_review is True
    assert "local_project_links.example.yaml" in {item.path for item in manifest.omitted_files}
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in output.iterdir()
        if path.is_file()
    )
    assert "not-for-pack" not in combined
    assert "must not enter the generated context pack" not in combined
    assert "observed " + "success" not in combined.lower()

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from turing_research_plus.session_runtime.context_pack_builder import (
    ContextPackBuildRequest,
    build_context_pack,
)


def _source(root: Path) -> Path:
    source = root / "source"
    source.mkdir()
    files = {
        "PROJECT_CONTEXT.md": "# Project\n",
        "MEMORY.md": "# Memory\n",
        "ROUTE_SPEC.yaml": "route_id: route-demo\n",
        "HARD_GATES.md": "# Hard Gates\n",
        "ARTIFACT_REQUIREMENTS.md": "# Artifact Requirements\n",
        "FAILURE_TAXONOMY.md": "# Failure Taxonomy\n",
        ".env": "PLACEHOLDER=not-for-pack\n",
        "local_project_links.yaml": "project: private\n",
        "notes.md": "not allowlisted\n",
    }
    for name, text in files.items():
        (source / name).write_text(text, encoding="utf-8")
    return source


def test_context_pack_builder_writes_required_pack_and_excludes_unsafe_files(
    tmp_path: Path,
) -> None:
    source = _source(tmp_path)
    output = tmp_path / "pack"

    manifest = build_context_pack(
        ContextPackBuildRequest(
            package_id="ctx-runtime-demo",
            route_id="route-runtime-demo",
            source_dir=source,
            output_dir=output,
        )
    )

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
    assert not (output / ".env").exists()
    assert not (output / "local_project_links.yaml").exists()
    assert not (output / "notes.md").exists()
    assert manifest.status == "built-with-exclusions"
    assert manifest.release_blocker is False
    assert manifest.remote_execution_allowed is False
    assert manifest.live_network_allowed is False
    assert manifest.requires_human_review is True
    omitted = {item.path for item in manifest.omitted_files}
    assert {".env", "local_project_links.yaml", "notes.md"} <= omitted


def test_context_pack_builder_rejects_live_or_remote_modes(tmp_path: Path) -> None:
    source = _source(tmp_path)
    with pytest.raises(ValidationError):
        ContextPackBuildRequest(
            package_id="ctx",
            route_id="route",
            source_dir=source,
            output_dir=tmp_path / "pack",
            remote_execution_enabled=True,
        )
    with pytest.raises(ValidationError):
        ContextPackBuildRequest(
            package_id="ctx",
            route_id="route",
            source_dir=source,
            output_dir=tmp_path / "pack",
            live_network_enabled=True,
        )

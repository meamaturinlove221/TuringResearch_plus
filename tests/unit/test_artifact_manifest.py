from pathlib import Path

from turing_research_plus.artifact_audit.manifest import infer_file_type, load_manifest_like_index
from turing_research_plus.artifact_audit.models import ArtifactFileType


def test_infer_file_type() -> None:
    assert infer_file_type("board.png") == ArtifactFileType.PNG
    assert infer_file_type("bundle.npz") == ArtifactFileType.NPZ
    assert infer_file_type("unknown.bin") == ArtifactFileType.UNKNOWN


def test_markdown_index_with_metadata_records_is_local_only() -> None:
    manifest = load_manifest_like_index(
        Path("examples") / "vggt-human-prior-survey" / "local_scan_artifact_index.md"
    )

    paths = {record.path for record in manifest.records}

    assert "VGGT parent workspace" in paths
    assert "Candidate" not in paths
    assert all(record.safety_flags for record in manifest.records)
    assert manifest.warnings == []


def test_json_manifest_records(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(
        """
{
  "manifest_id": "fixture",
  "records": [
    {"path": "predictions.npz", "file_type": "npz", "included": true},
    {"path": "missing.png", "file_type": "png", "included": false, "omitted_reason": "missing"}
  ]
}
""".strip(),
        encoding="utf-8",
    )

    manifest = load_manifest_like_index(path)

    assert len(manifest.records) == 2
    assert manifest.records[1].included is False

from pathlib import Path

from turing_research_plus.artifact_audit.auditor import audit_artifacts
from turing_research_plus.artifact_audit.models import ArtifactAuditInput, ArtifactSafetyFlag


def test_artifact_audit_from_empty_vggt_local_scan() -> None:
    report = audit_artifacts(
        ArtifactAuditInput(
            source_path=Path("examples")
            / "vggt-human-prior-survey"
            / "local_scan_artifact_index.md"
        )
    )

    assert report.records == []
    assert "Artifact audit found no artifact records." in report.warnings


def test_artifact_audit_does_not_read_private_vggt_paths(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        """
{
  "records": [
    {"path": "D:/vggt/private-result.npz", "file_type": "npz", "included": true}
  ]
}
""".strip(),
        encoding="utf-8",
    )

    report = audit_artifacts(ArtifactAuditInput(source_path=manifest))

    assert report.records[0].included is False
    assert ArtifactSafetyFlag.PRIVATE_PATH_NOT_READ in report.records[0].safety_flags


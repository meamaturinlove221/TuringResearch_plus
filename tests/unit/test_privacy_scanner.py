from __future__ import annotations

from pathlib import Path

from turing_research_plus.privacy.models import PrivacyFindingType
from turing_research_plus.privacy.policy import DEFAULT_HUGE_NPZ_BYTES
from turing_research_plus.privacy.scanner import scan_privacy_paths


def test_privacy_scanner_detects_required_path_and_content_patterns(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("APIFY_TOKEN=abc123456789\n", encoding="utf-8")
    (tmp_path / "local_project_links.yaml").write_text("project: local\n", encoding="utf-8")
    private_dir = tmp_path / "private_data"
    private_dir.mkdir()
    (private_dir / "notes.md").write_text("private advisor feedback\n", encoding="utf-8")
    (tmp_path / "SMPLX_model.pkl").write_text("tiny placeholder\n", encoding="utf-8")
    (tmp_path / "paths.md").write_text(
        "local path C:\\Users\\researcher\\secret_project\n",
        encoding="utf-8",
    )

    report = scan_privacy_paths([tmp_path])
    finding_types = {finding.finding_type for finding in report.findings}

    assert PrivacyFindingType.ENV_FILE in finding_types
    assert PrivacyFindingType.TOKEN_PATTERN in finding_types
    assert PrivacyFindingType.LOCAL_PROJECT_LINKS in finding_types
    assert PrivacyFindingType.PRIVATE_DATA_PATH in finding_types
    assert PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK in finding_types
    assert PrivacyFindingType.SMPLX_MODEL_FILE in finding_types
    assert PrivacyFindingType.PERSONAL_PATH in finding_types
    assert report.release_blocker is True


def test_privacy_scanner_marks_huge_npz_metadata_only(tmp_path: Path) -> None:
    npz_path = tmp_path / "large_predictions.npz"
    npz_path.write_bytes(b"0" * (DEFAULT_HUGE_NPZ_BYTES + 1))

    report = scan_privacy_paths([npz_path])

    assert any(
        finding.finding_type == PrivacyFindingType.HUGE_NPZ
        for finding in report.findings
    )
    assert report.release_blocker is True

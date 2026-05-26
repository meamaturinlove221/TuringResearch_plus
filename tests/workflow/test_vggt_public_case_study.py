from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PUBLIC_CASE_FILES = [
    (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "public_case_study"
        / "case_study_draft.md"
    ),
    (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "public_case_study"
        / "redaction_report.md"
    ),
    (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "public_case_study"
        / "claim_safety_report.md"
    ),
    ROOT / "split_ready/turingresearch-vggt-case/CASE_STUDY.md",
    ROOT / "split_ready/turingresearch-vggt-case/CLAIM_SAFETY.md",
    ROOT / "split_ready/turingresearch-vggt-case/PRIVACY.md",
    ROOT / "docs/vggt-case-study-refresh-v1.5.md",
]

FORBIDDEN_PUBLIC_PATTERNS = [
    "D:/",
    "D:\\",
    "C:/",
    "C:\\",
    "local_report_auxiliary",
    "vggt-main",
    "vggt-feature-adapter",
    ".npz",
    ".ply",
    ".zip",
    ".pt",
    ".pth",
    ".ckpt",
    ".safetensors",
    "api_key",
    "secret_key",
    "BEGIN " + "PRIVATE KEY",
]

UNSUPPORTED_CLAIMS = [
    "SparseConv3D success | observed",
    "SparseConv3D success | local-observed",
    "advisor approval | observed",
    "promotion | observed",
    "candidate_promoted: true",
    "status: promoted",
]


def test_vggt_public_case_study_files_are_public_safe() -> None:
    combined = ""
    for path in PUBLIC_CASE_FILES:
        assert path.exists(), f"missing public case file: {path}"
        text = path.read_text(encoding="utf-8")
        combined += "\n" + text
        for pattern in FORBIDDEN_PUBLIC_PATTERNS:
            assert pattern not in text
        for claim in UNSUPPORTED_CLAIMS:
            assert claim not in text

    assert "requires-human-review" in combined
    assert "local-observed" in combined
    assert "main TuringResearch repository remains flagship" in combined

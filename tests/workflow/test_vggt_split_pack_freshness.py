from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SPLIT_READY_FILES = [
    ROOT / "split_ready/turingresearch-vggt-case/CASE_STUDY.md",
    ROOT / "split_ready/turingresearch-vggt-case/CLAIM_SAFETY.md",
    ROOT / "split_ready/turingresearch-vggt-case/PRIVACY.md",
]

FRESHNESS_FILES = [
    ROOT / "docs/vggt-split-pack-freshness-verification.md",
    ROOT / "split_manual/turingresearch-vggt-case/FRESHNESS_CHECK.md",
    ROOT / "lanes/343_5_split_pack_freshness_verification.md",
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


def test_split_ready_matches_round_338_public_safe_baseline() -> None:
    combined = ""
    for path in SPLIT_READY_FILES:
        assert path.exists(), f"missing split-ready file: {path}"
        text = path.read_text(encoding="utf-8")
        combined += "\n" + text

    assert "Round: Optional 338.5" in combined
    assert "requires-human-review" in combined
    assert "main TuringResearch Plus repository remains flagship" in combined


def test_split_pack_freshness_files_are_public_safe_and_guarded() -> None:
    combined = ""
    for path in FRESHNESS_FILES:
        assert path.exists(), f"missing freshness file: {path}"
        text = path.read_text(encoding="utf-8")
        combined += "\n" + text
        for pattern in FORBIDDEN_PUBLIC_PATTERNS:
            assert pattern not in text
        for claim in UNSUPPORTED_CLAIMS:
            assert claim not in text

    assert "fresh-manual-draft" in combined
    assert "requires-human-review" in combined
    assert "not created and not pushed" in combined
    assert "main TuringResearch Plus repository" in combined

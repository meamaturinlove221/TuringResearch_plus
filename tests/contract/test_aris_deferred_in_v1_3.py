from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ARIS_DOCS = [
    ROOT / "docs" / "v1.3.0-aris-deferral-reconfirm.md",
    ROOT / "docs" / "aris-implementation-blocklist-v1.3.md",
    ROOT / "docs" / "aris-reference-only-policy.md",
    ROOT / "docs" / "v1.3.0-aris-still-deferred.md",
]

BLOCKED_FEATURES = [
    "cross-model review",
    "proof-checker",
    "meta-optimize",
    "paper-claim-audit",
    "session stop hook",
    "automated sleep research loop",
]


def _combined() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in ARIS_DOCS)


def test_v1_3_aris_deferral_docs_exist() -> None:
    missing = [str(path.relative_to(ROOT)) for path in ARIS_DOCS if not path.exists()]

    assert missing == []


def test_v1_3_aris_is_reference_only_and_deferred() -> None:
    text = _combined().lower()

    required_phrases = [
        "future reference",
        "deferred",
        "study only",
        "not v1.3 implementation",
        "requires design and safety review",
        "aris deferred from v1.3 implementation",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_v1_3_aris_blocklist_covers_required_features() -> None:
    text = _combined().lower()

    for feature in BLOCKED_FEATURES:
        assert feature in text

    assert "model review replacing human review" in text
    assert "aris paper-writing automation" in text


def test_v1_3_aris_docs_do_not_claim_runtime_implementation() -> None:
    reconfirm = (ROOT / "docs" / "v1.3.0-aris-deferral-reconfirm.md").read_text(
        encoding="utf-8"
    ).lower()
    reference_policy = (ROOT / "docs" / "aris-reference-only-policy.md").read_text(
        encoding="utf-8"
    ).lower()
    positive_surface = f"{reconfirm}\n{reference_policy}"
    blocklist = (ROOT / "docs" / "aris-implementation-blocklist-v1.3.md").read_text(
        encoding="utf-8"
    ).lower()

    forbidden_claims = [
        "aris is implemented",
        "cross-model review is enabled",
        "proof-checker is available",
        "meta-optimize is available",
        "paper-claim audit is available",
        "session stop hook is active",
        "automated sleep research loop is active",
        "aris replaces human review",
    ]
    for claim in forbidden_claims:
        assert claim not in positive_surface
        assert claim in blocklist

    assert "v1.3 does not implement" in positive_surface
    assert "blocked runtime features" in blocklist

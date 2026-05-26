from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_RELEASE_DOCS = [
    "docs/v1.0.0-final-scope.md",
    "docs/v1.0.0-release-criteria.md",
    "docs/v1.0.0-public-api.md",
    "docs/v1.0.0-namespace-compatibility-report.md",
    "docs/v1.0.0-cli-mcp-sanity.md",
    "docs/v1.0.0-quickstart.md",
    "docs/v1.0.0-demo-refresh-report.md",
    "docs/v1.0.0-security-audit.md",
    "docs/v1.0.0-privacy-audit.md",
    "docs/v1.0.0-public-launch-rc-report.md",
    "docs/v1.0.0-split-readiness-summary.md",
    "docs/v1.0.0-split-execution-go-no-go.md",
]

REQUIRED_CONTRACTS = [
    "contracts/v1_public_api.yaml",
    "contracts/campaign_catalog.yaml",
    "contracts/pod_context_lifecycle.yaml",
    "contracts/plugin_sandbox_policy.yaml",
    "contracts/plugin_compatibility.yaml",
    "contracts/export_quality_gate.yaml",
]


def test_v1_release_docs_exist_and_cover_required_surfaces() -> None:
    missing = [path for path in REQUIRED_RELEASE_DOCS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_release_contracts_exist() -> None:
    missing = [path for path in REQUIRED_CONTRACTS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_release_docs_preserve_public_boundaries() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in REQUIRED_RELEASE_DOCS
    )
    required_terms = [
        "human review",
        "fake",
        "privacy",
        "plugin",
        "quickstart",
        "no automatic",
    ]

    for term in required_terms:
        assert term in combined


def test_v1_split_execution_contract_keeps_main_repo_flagship() -> None:
    text = (ROOT / "docs" / "v1.0.0-split-execution-go-no-go.md").read_text(
        encoding="utf-8"
    )

    assert "NO-GO FOR PHYSICAL SPLIT BEFORE v1.0 PUBLIC LAUNCH" in text
    assert "GO FOR MAIN REPOSITORY PUBLIC LAUNCH PREPARATION" in text
    assert "Do not create GitHub repositories" in text
    assert "Do not add nonexistent GitHub URLs" in text

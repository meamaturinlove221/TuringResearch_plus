from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_V1_6_DOCS = [
    "README.md",
    "docs/turingresearch-public-naming-policy.md",
    "docs/open-source-hygiene-gate-report.md",
    "docs/public-launch-checklist-v1.6.md",
    "docs/public-launch-go-no-go-v1.6.md",
    "docs/public-launch-human-actions-v1.6.md",
    "docs/screenshot-demo-asset-pack-v1.6.md",
    "docs/v1.6.0-docs-deployment-gate-report.md",
    "docs/docs-release-bundle.md",
    "docs/split-final-safety-refresh-v1.6.md",
    "docs/optional-live-safety-gate.md",
    "docs/local-install-smoke.md",
    "docs/v1.6.0-final-archive.md",
    "docs/v1.6.0-handoff.md",
    "docs/v1.6.0-what-is-ready.md",
    "docs/v1.6.0-what-is-not-ready.md",
    "docs/v1.6.0-next-human-actions.md",
    "docs/v1.6.0-aris-still-deferred.md",
    "docs/v1.6.0-full-regression-report.md",
    "docs/v1.6.0-regression-failures.md",
]

REQUIRED_V1_6_ARTIFACTS = [
    "docs-site/release_bundle_manifest.yaml",
    "docs-site/release_bundle_report.md",
    "docs-site/release_bundle/site/index.html",
    "split_manual/turingresearch-vggt-case/manifest.yaml",
    "split_manual/turingresearch-examples/manifest.yaml",
    "assets/screenshots/SCREENSHOT_MANIFEST.yaml",
    "assets/screenshots/SCREENSHOT_TODO.md",
    "assets/demo_gif/DEMO_GIF_SCRIPT.md",
    "examples/public_demo/dashboard_showcase/landing.html",
    "examples/public_demo/dashboard_showcase/parity.html",
    "examples/public_demo/dashboard_showcase/interview.html",
    "pyproject.toml",
]

REQUIRED_V1_6_TESTS = [
    "tests/workflow/test_v1_6_docs_deployment_gate.py",
    "tests/workflow/test_docs_release_bundle.py",
    "tests/contract/test_open_source_hygiene_gate.py",
    "tests/contract/test_public_release_hygiene.py",
    "tests/contract/test_v1_6_release_contracts.py",
    "tests/workflow/test_v1_6_full_replay.py",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_v1_6_release_docs_artifacts_and_tests_exist() -> None:
    required = [*REQUIRED_V1_6_DOCS, *REQUIRED_V1_6_ARTIFACTS, *REQUIRED_V1_6_TESTS]
    missing = [path for path in required if not (ROOT / path).exists()]

    assert missing == []


def test_v1_6_release_contracts_cover_required_surfaces() -> None:
    combined = "\n".join(
        _read(path)
        for path in [
            "docs/v1.6.0-full-regression-report.md",
            "docs/v1.6.0-final-archive.md",
            "docs/v1.6.0-what-is-ready.md",
            "docs/public-launch-checklist-v1.6.md",
        ]
    )

    required_terms = [
        "docs deployment",
        "split manual pack",
        "optional live smoke",
        "package readiness",
        "dashboard showcase",
        "release artifact",
        "privacy/security",
        "ARIS remains deferred",
        "PASS WITH REVIEW",
    ]
    for term in required_terms:
        assert term in combined


def test_v1_6_release_contracts_preserve_manual_publication_boundary() -> None:
    combined = "\n".join(
        _read(path)
        for path in [
            "docs/v1.6.0-full-regression-report.md",
            "docs/public-launch-go-no-go-v1.6.md",
            "docs/public-launch-human-actions-v1.6.md",
            "docs/v1.6.0-what-is-not-ready.md",
        ]
    ).lower()

    required_boundaries = [
        "no automatic publication",
        "no tag",
        "no github release",
        "no pypi publication",
        "no github pages deployment",
        "no split repository creation",
        "no live provider",
        "no aris implementation",
    ]
    for boundary in required_boundaries:
        assert boundary in combined

    forbidden_claims = [
        "public site is live",
        "github pages deployed",
        "pypi package published",
        "child repositories created",
        "live provider succeeded",
        "aris implemented",
    ]
    for claim in forbidden_claims:
        assert claim not in combined


def test_v1_6_package_metadata_stays_compatibility_first() -> None:
    pyproject = _read("pyproject.toml")
    readme = _read("README.md")
    local_install = _read("docs/local-install-smoke.md")

    assert 'name = "turingresearch-plus"' in pyproject
    assert 'version = "1.5.0rc0"' in pyproject
    assert "TuringResearch" in readme
    assert "Not implied: PyPI publication or package rename." in _read(
        "docs/v1.6.0-what-is-ready.md"
    )
    assert "It does not publish a package" in local_install


def test_v1_6_release_contracts_have_no_public_old_name_or_fake_urls() -> None:
    public_paths = [
        "README.md",
        "docs/v1.6.0-full-regression-report.md",
        "docs/v1.6.0-regression-failures.md",
        "docs/public-launch-checklist-v1.6.md",
        "docs/public-launch-go-no-go-v1.6.md",
        "docs/public-launch-human-actions-v1.6.md",
    ]
    combined = "\n".join(_read(path) for path in public_paths)
    old_name = "Tul" + "ingResearch"

    forbidden = [
        old_name,
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "ghp_",
        "github_pat_",
        "BEGIN OPENSSH PRIVATE KEY",
        "sk-" + "live",
        "public_url: https://",
    ]
    for marker in forbidden:
        assert marker not in combined

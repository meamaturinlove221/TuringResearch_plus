"""Quality metric collectors."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.quality.models import QualityMetric, QualityReport, QualityStatus

DEFAULT_DOCS = [
    "README.md",
    "docs/public-release-hardening.md",
    "docs/security-checklist.md",
    "docs/benchmark-replay-suite.md",
]
DEFAULT_TESTS = [
    "tests/contract/test_name_integrity.py",
    "tests/contract/test_public_release_hygiene.py",
    "tests/workflow/test_public_demo_suite.py",
]
DEFAULT_CONTRACTS = [
    "contracts/benchmark_replay.yaml",
    "contracts/quality_regression_gate.yaml",
]
DEFAULT_EXAMPLES = [
    "examples/public_demo/README.md",
    "examples/benchmarks/public_demo_replay.yaml",
]


def evaluate_quality_metrics(root: Path) -> list[QualityMetric]:
    """Evaluate lightweight quality metrics for the local repository."""

    return [
        _completeness_metric(root, "docs-completeness", "Docs completeness", DEFAULT_DOCS),
        _completeness_metric(
            root, "test-coverage-proxy", "Test coverage proxy", DEFAULT_TESTS
        ),
        _completeness_metric(
            root,
            "contract-consistency",
            "Contract consistency",
            DEFAULT_CONTRACTS,
        ),
        _completeness_metric(
            root, "example-readiness", "Example readiness", DEFAULT_EXAMPLES
        ),
        _contains_metric(
            root / "docs" / "security-checklist.md",
            "safety-readiness",
            "Safety readiness",
            ["secret", "raw data", "SMPL-X"],
        ),
        _contains_metric(
            root / "docs" / "live-test-policy.md",
            "fake-live-boundary",
            "Fake/live boundary",
            ["disabled by default", "explicit"],
        ),
        QualityMetric(
            metric_id="old-name-absence",
            name="Prior project name absence",
            score=1.0,
            status=QualityStatus.PASS,
            details=["Delegated to regression gate scanner."],
        ),
        QualityMetric(
            metric_id="privacy-gate-pass",
            name="Privacy gate pass",
            score=1.0
            if (root / "docs" / "privacy-data-policy-layer.md").exists()
            else 0.0,
            status=QualityStatus.PASS
            if (root / "docs" / "privacy-data-policy-layer.md").exists()
            else QualityStatus.FAIL,
            details=["Privacy policy documentation exists."],
        ),
        QualityMetric(
            metric_id="release-readiness",
            name="Release readiness",
            score=1.0
            if (root / "docs" / "v0.5.0-alpha-release-readiness.md").exists()
            else 0.5,
            status=QualityStatus.PASS
            if (root / "docs" / "v0.5.0-alpha-release-readiness.md").exists()
            else QualityStatus.WARN,
            details=["Release readiness docs are present for latest prepared release line."],
        ),
    ]


def build_quality_report(root: Path, *, report_id: str = "quality_report") -> QualityReport:
    """Build a quality report from local metrics."""

    metrics = evaluate_quality_metrics(root)
    blockers = [metric for metric in metrics if metric.status == QualityStatus.FAIL]
    warnings = [
        f"{metric.metric_id}: {detail}"
        for metric in metrics
        if metric.status == QualityStatus.WARN
        for detail in metric.details
    ]
    status = QualityStatus.PASS
    if blockers:
        status = QualityStatus.FAIL
    elif warnings:
        status = QualityStatus.WARN
    return QualityReport(
        report_id=report_id,
        metrics=metrics,
        status=status,
        warnings=warnings,
        release_ready=status == QualityStatus.PASS,
        requires_human_review=True,
    )


def _completeness_metric(
    root: Path, metric_id: str, name: str, relative_paths: list[str]
) -> QualityMetric:
    missing = [path for path in relative_paths if not (root / path).exists()]
    score = (len(relative_paths) - len(missing)) / len(relative_paths)
    status = QualityStatus.PASS if not missing else QualityStatus.FAIL
    details = ["All required files exist."] if not missing else [f"Missing `{p}`" for p in missing]
    return QualityMetric(
        metric_id=metric_id,
        name=name,
        score=score,
        status=status,
        details=details,
    )


def _contains_metric(
    path: Path, metric_id: str, name: str, required_terms: list[str]
) -> QualityMetric:
    if not path.exists():
        return QualityMetric(
            metric_id=metric_id,
            name=name,
            score=0.0,
            status=QualityStatus.FAIL,
            details=[f"Missing `{path.as_posix()}`"],
        )
    text = path.read_text(encoding="utf-8").lower()
    missing = [term for term in required_terms if term.lower() not in text]
    status = QualityStatus.PASS if not missing else QualityStatus.WARN
    score = (len(required_terms) - len(missing)) / len(required_terms)
    details = (
        ["Required quality terms present."]
        if not missing
        else [f"Missing term `{term}`" for term in missing]
    )
    return QualityMetric(
        metric_id=metric_id,
        name=name,
        score=score,
        status=status,
        details=details,
    )

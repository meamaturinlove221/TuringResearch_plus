"""Regression gate checks for local release safety."""

from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.quality.models import (
    QualityStatus,
    RegressionGateCheck,
    RegressionGateReport,
)

TEXT_EXTENSIONS = {".py", ".md", ".yaml", ".toml", ".json", ".html"}
IGNORED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "turingresearch_plus.egg-info",
}
PLACEHOLDER_SECRET_MARKERS = {
    "dummy",
    "example",
    "fake",
    "not-real",
    "not_real",
    "placeholder",
    "redacted",
}


def run_regression_gate(
    root: Path, *, gate_id: str = "quality_regression_gate"
) -> RegressionGateReport:
    """Run local regression gate checks."""

    checks = [
        check_prior_name_absent(root),
        check_no_secrets(root),
        check_public_demo_present(root),
        check_contracts_present(root),
        check_fake_results_not_observed(root),
        check_live_tests_not_required_by_default(root),
    ]
    blockers = [
        blocker
        for check in checks
        for blocker in check.blockers
        if not check.passed
    ]
    warnings = [warning for check in checks for warning in check.warnings]
    status = QualityStatus.PASS if not blockers else QualityStatus.FAIL
    return RegressionGateReport(
        gate_id=gate_id,
        checks=checks,
        status=status,
        blockers=blockers,
        warnings=warnings,
        requires_human_review=True,
    )


def check_prior_name_absent(root: Path) -> RegressionGateCheck:
    """Fail when prior project naming appears outside allowed historical docs."""

    allowed = {
        Path("docs/rename-tuling-to-turing-report.md"),
        Path("docs/round38-pre-rename-checkpoint.md"),
        Path("docs/round38-rename-risk-register.md"),
        Path("lanes/18_round38_pre_rename_checkpoint.md"),
    }
    terms = _prior_name_terms()
    offenders: list[str] = []
    for path in _iter_text_files(root):
        relative = path.relative_to(root)
        if relative in allowed:
            continue
        text = path.read_text(encoding="utf-8")
        if any(term in text for term in terms):
            offenders.append(relative.as_posix())
    return RegressionGateCheck(
        check_id="old-name-absence",
        description="Fail if prior project naming appears.",
        passed=not offenders,
        blockers=[f"prior-name:{item}" for item in offenders],
    )


def check_no_secrets(root: Path) -> RegressionGateCheck:
    """Fail on committed secret-like values or forbidden local config filenames."""

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|"
        r"xox[baprs]-[A-Za-z0-9-]{20,}|"
        r"(api[_-]?key|token|secret)\s*[:=]\s*[A-Za-z0-9_./-]{24,})",
        re.IGNORECASE,
    )
    forbidden_names = {".env", "local_project_links.yaml"}
    allowlist = {
        "examples/vggt-human-prior-survey/shared_store_fixture/.env",
    }
    blockers: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or set(path.parts) & IGNORED_PARTS:
            continue
        relative = path.relative_to(root).as_posix()
        if path.name in forbidden_names and relative not in allowlist:
            blockers.append(f"forbidden-file:{relative}")
        if path.suffix.lower() in TEXT_EXTENSIONS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(
                not any(
                    marker in match.group(0).lower()
                    for marker in PLACEHOLDER_SECRET_MARKERS
                )
                for match in token_like.finditer(text)
            ):
                blockers.append(f"token-like-value:{relative}")
    return RegressionGateCheck(
        check_id="secret-scan",
        description="Fail if secrets or forbidden local config files are detected.",
        passed=not blockers,
        blockers=blockers,
    )


def check_public_demo_present(root: Path) -> RegressionGateCheck:
    """Fail when public demo files are missing."""

    required = [
        "README.md",
        "demo_research_intent.md",
        "demo_evidence_ledger.json",
        "demo_artifact_index.md",
        "demo_visual_inventory.md",
        "demo_related_work.md",
        "demo_advisor_pack.md",
        "demo_dashboard.html",
    ]
    demo_root = root / "examples" / "public_demo"
    missing = [name for name in required if not (demo_root / name).exists()]
    return RegressionGateCheck(
        check_id="public-demo-present",
        description="Fail if public demo files are missing.",
        passed=not missing,
        blockers=[f"missing-demo:{item}" for item in missing],
    )


def check_contracts_present(root: Path) -> RegressionGateCheck:
    """Fail when key contracts are missing."""

    required = [
        "contracts/benchmark_replay.yaml",
        "contracts/quality_regression_gate.yaml",
        "contracts/paper_writing_scaffold.yaml",
    ]
    missing = [path for path in required if not (root / path).exists()]
    return RegressionGateCheck(
        check_id="contract-consistency",
        description="Fail if required contracts are missing.",
        passed=not missing,
        blockers=[f"missing-contract:{item}" for item in missing],
    )


def check_fake_results_not_observed(root: Path) -> RegressionGateCheck:
    """Fail when demo evidence promotes fake results to observed."""

    demo_ledger = root / "examples" / "public_demo" / "demo_evidence_ledger.json"
    blockers: list[str] = []
    if demo_ledger.exists() and '"status": "observed"' in demo_ledger.read_text(
        encoding="utf-8"
    ):
        blockers.append("public-demo-fake-result-observed")
    return RegressionGateCheck(
        check_id="fake-result-not-observed",
        description="Fail if fake/demo result is marked observed.",
        passed=not blockers,
        blockers=blockers,
    )


def check_live_tests_not_required_by_default(root: Path) -> RegressionGateCheck:
    """Fail when live test policy no longer states default skip behavior."""

    policy = root / "docs" / "live-test-policy.md"
    blockers: list[str] = []
    text = policy.read_text(encoding="utf-8").lower() if policy.exists() else ""
    if not policy.exists():
        blockers.append("missing-live-test-policy")
    has_default_skip = (
        "skips" in text
        and "default" in text
        and ("live tests" in text or "markers" in text)
    )
    has_disabled_default = "disabled by default" in text or "skipped by default" in text
    if not has_default_skip and not has_disabled_default:
        blockers.append("live-tests-default-boundary-missing")
    return RegressionGateCheck(
        check_id="live-tests-default-skip",
        description="Fail if live tests are required by default.",
        passed=not blockers,
        blockers=blockers,
    )


def _iter_text_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_EXTENSIONS
        and not (set(path.parts) & IGNORED_PARTS)
    )


def _prior_name_terms() -> list[str]:
    display = "Tul" + "ingResearch"
    core = "tul" + "ing_research"
    slug = "tul" + "ingresearch"
    return [
        display,
        display + "_plus",
        core,
        core + "_plus",
        slug + "-plus",
        slug + "-",
    ]

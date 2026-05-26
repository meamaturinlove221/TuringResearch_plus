from __future__ import annotations

from pathlib import Path

from turing_research_plus.quality.regression_gate import (
    check_fake_results_not_observed,
    check_live_tests_not_required_by_default,
    check_public_demo_present,
    run_regression_gate,
)

ROOT = Path(__file__).resolve().parents[2]


def test_regression_gate_passes_current_public_demo_surface() -> None:
    report = run_regression_gate(ROOT)

    assert report.status == "pass"
    assert report.blockers == []
    assert report.requires_human_review is True
    assert {check.check_id for check in report.checks} == {
        "old-name-absence",
        "secret-scan",
        "public-demo-present",
        "contract-consistency",
        "fake-result-not-observed",
        "live-tests-default-skip",
    }


def test_public_demo_gate_detects_missing_demo(tmp_path: Path) -> None:
    check = check_public_demo_present(tmp_path)

    assert check.passed is False
    assert any(item.startswith("missing-demo:") for item in check.blockers)


def test_fake_result_gate_blocks_observed_demo(tmp_path: Path) -> None:
    demo = tmp_path / "examples" / "public_demo"
    demo.mkdir(parents=True)
    (demo / "demo_evidence_ledger.json").write_text(
        '{"entries": [{"status": "observed"}]}',
        encoding="utf-8",
    )

    check = check_fake_results_not_observed(tmp_path)

    assert check.passed is False
    assert check.blockers == ["public-demo-fake-result-observed"]


def test_live_tests_gate_requires_default_skip_policy(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    (docs / "live-test-policy.md").write_text("live tests are mandatory", encoding="utf-8")

    check = check_live_tests_not_required_by_default(tmp_path)

    assert check.passed is False
    assert "live-tests-default-boundary-missing" in check.blockers

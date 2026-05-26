from __future__ import annotations

from pathlib import Path

from turing_research_plus.repo_split.safety import evaluate_split_file


def test_split_safety_allows_public_markdown(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    path = source / "README.md"
    path.write_text("# Demo\n\nNo raw data is bundled.\n", encoding="utf-8")

    safe, findings = evaluate_split_file(
        path,
        source_root=source,
        allowed_suffixes={".md"},
        max_file_size_bytes=10_000,
    )

    assert safe is True
    assert findings == []


def test_split_safety_blocks_env_and_model_payload(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    env_path = source / ".env"
    env_path.write_text("API_KEY=secret\n", encoding="utf-8")
    model_path = source / "SMPLX_NEUTRAL.npz"
    model_path.write_bytes(b"fake")

    env_safe, env_findings = evaluate_split_file(
        env_path,
        source_root=source,
        allowed_suffixes={".md"},
        max_file_size_bytes=10_000,
    )
    model_safe, model_findings = evaluate_split_file(
        model_path,
        source_root=source,
        allowed_suffixes={".md"},
        max_file_size_bytes=10_000,
    )

    assert env_safe is False
    assert model_safe is False
    assert any(finding.release_blocker for finding in env_findings)
    assert any(finding.finding_type == "blocked-suffix" for finding in model_findings)


def test_split_safety_allows_policy_mentions_without_release_blocker(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    path = source / "PRIVACY.md"
    path.write_text("- private advisor feedback is excluded.\n", encoding="utf-8")

    safe, findings = evaluate_split_file(
        path,
        source_root=source,
        allowed_suffixes={".md"},
        max_file_size_bytes=10_000,
    )

    assert safe is True
    assert findings
    assert all(finding.release_blocker is False for finding in findings)
    assert {finding.finding_type for finding in findings} == {
        "policy-mention:private_advisor_feedback"
    }

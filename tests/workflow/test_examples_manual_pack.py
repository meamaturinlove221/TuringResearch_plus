from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "split_manual" / "turingresearch-examples"
SOURCE = ROOT / "split_ready" / "turingresearch-examples"
REPORT = ROOT / "docs" / "examples-repo-manual-pack-report.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined_text(path: Path) -> str:
    return "\n".join(
        item.read_text(encoding="utf-8")
        for item in sorted(path.rglob("*"))
        if item.is_file()
    )


def test_examples_manual_pack_has_required_files() -> None:
    required = {
        "README.md",
        "CREATE_REPO_MANUALLY.md",
        "PUSH_COMMANDS.md",
        "SAFETY_CHECKLIST.md",
        "manifest.yaml",
    }

    assert PACK.exists()
    actual = {item.name for item in PACK.iterdir() if item.is_file()}
    assert required.issubset(actual)
    assert SOURCE.exists()
    assert REPORT.exists()


def test_examples_manual_pack_keeps_manual_boundaries() -> None:
    manifest = _text(PACK / "manifest.yaml")
    readme = _text(PACK / "README.md")
    create = _text(PACK / "CREATE_REPO_MANUALLY.md")

    assert "creates_github_repo: false" in manifest
    assert "pushes_external_repo: false" in manifest
    assert "writes_real_url: false" in manifest
    assert "requires_human_confirmation: true" in manifest
    assert "manual execution pack / not a GitHub repository" in readme
    assert "human instructions only" in create
    assert "main TuringResearch repository remains the flagship" in readme


def test_examples_manual_pack_has_safe_push_reference_only() -> None:
    push = _text(PACK / "PUSH_COMMANDS.md")

    assert "Status: reference-only command notes." in push
    assert "# git init" in push
    assert "# git push -u origin main" in push
    assert "<approved-real-repository-url>" in push
    assert "Do not use placeholder URLs as remotes." in push


def test_examples_manual_pack_is_public_safe() -> None:
    combined = "\n".join([_combined_text(PACK), _text(REPORT)])
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"

    assert old_name not in combined
    assert private_drive not in combined
    assert "D:" + "\\vggt" not in combined
    assert ".env=" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "https://github.com/" not in combined
    assert "demo_only: true" in combined
    assert "no_raw_data: true" in combined
    assert "no_private_path: true" in combined
    assert "no_api_key: true" in combined
    assert "no_huge_artifact: true" in combined
    assert "no_unsupported_claim: true" in combined
    assert "Not proof of research success." in combined


def test_examples_manual_pack_report_records_gate_result() -> None:
    report = _text(REPORT)

    assert "Status: manual pack generated." in report
    assert "| demo only | pass |" in report
    assert "| no raw data | pass |" in report
    assert "| no private path | pass |" in report
    assert "| no API key | pass |" in report
    assert "| no huge artifact | pass |" in report
    assert "| no unsupported claim | pass |" in report
    assert "No GitHub repository was created." in report

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = ROOT / "split_ready" / "turingresearch-plugins"


def _text_files() -> list[Path]:
    return sorted(path for path in EXPORT_DIR.rglob("*") if path.is_file())


def test_v1_plugins_final_export_required_files_exist() -> None:
    required = {
        "README.md",
        "PLUGIN_POLICY.md",
        "plugins_manifest.yaml",
        "safety_report.md",
    }

    assert EXPORT_DIR.exists()
    assert required == {path.name for path in _text_files()}


def test_v1_plugins_final_export_policy_is_safe() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in _text_files())
    combined_lower = combined.lower()
    old_name = "Tuling" + "Research"

    assert old_name not in combined
    assert "third-party plugins are disabled by default" in combined_lower
    assert "execute_code_default: denied" in combined
    assert "secrets_access: forbidden" in combined
    assert "unknown_plugin_code_execution: disabled" in combined
    assert "No `execute_code` default: pass" in combined
    assert "No secrets access: pass" in combined
    assert "main_repo_keeps_core_plugin_framework: true" in combined
    assert "main repository keeps core plugin loading" in combined_lower


def test_v1_plugins_manifest_records_release_blockers() -> None:
    manifest = (EXPORT_DIR / "plugins_manifest.yaml").read_text(encoding="utf-8")

    assert "ready_to_create_after_human_approval: true" in manifest
    assert "third_party_disabled_by_default: true" in manifest
    assert "manifest_required: true" in manifest
    assert "sandbox_policy_required: true" in manifest
    assert "enabled_third_party_plugin" in manifest
    assert "missing_human_review" in manifest
    assert "no_github_repo_creation_without_approval: true" in manifest

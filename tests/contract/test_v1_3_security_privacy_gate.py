from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]

V1_3_PUBLIC_SURFACES = [
    ROOT / "README.md",
    ROOT / ".mcp.example.json",
    ROOT / "docs" / "v1.3.0-full-original-parity-replay-report.md",
    ROOT / "docs" / "v1.3.0-docs-polish-report.md",
    ROOT / "docs" / "original-reference-parity-summary.md",
    ROOT / "docs" / "reference-parity-dashboard.md",
    ROOT / "docs" / "aris-still-deferred-v1.3.md",
    ROOT / "docs" / "session-runtime-gate-report.md",
    ROOT / "docs" / "scholar-web-parity-gate-report.md",
    ROOT / "docs" / "yogsoth-full-parity-gate-report.md",
    ROOT / "docs" / "campaign-execution-trace.md",
    ROOT / "docs" / "research-catalog-dashboard.md",
    ROOT / "docs" / "vault-wiki-export-demo.md",
    ROOT / "docs" / "ontology-runbook-demo.md",
    ROOT / "docs" / "stress-scenario-library.md",
    ROOT / "docs" / "convergence-decision-report.md",
    ROOT / "docs" / "v1.3.0-aris-deferral-reconfirm.md",
    ROOT / "docs" / "aris-implementation-blocklist-v1.3.md",
    ROOT / "examples" / "public_demo" / "v1_3_original_parity_demo",
    ROOT / "examples" / "session_runtime",
    ROOT / "examples" / "scholar_demo",
    ROOT / "examples" / "apify_workflows",
    ROOT / "examples" / "research_catalog",
    ROOT / "examples" / "vault_wiki_demo",
    ROOT / "examples" / "ontology_demo",
    ROOT / "examples" / "stress_scenarios",
    ROOT / "examples" / "convergence_demo",
]

V1_3_CODE_SURFACES = [
    ROOT / "src" / "turing_research_plus" / "session_runtime",
    ROOT / "src" / "turing_research_plus" / "scholar_tools",
    ROOT / "src" / "turing_research_plus" / "web_tools",
    ROOT / "src" / "turing_research_plus" / "campaigns",
    ROOT / "src" / "turing_research_plus" / "vault_graph",
    ROOT / "src" / "turing_research_plus" / "stress_test",
    ROOT / "src" / "turing_research_plus" / "convergence",
    ROOT / "contracts" / "session_preflight_runner.yaml",
    ROOT / "contracts" / "context_pack_builder_runtime.yaml",
    ROOT / "contracts" / "optional_sftp_transfer_runner.yaml",
    ROOT / "contracts" / "remote_return_verifier_runtime.yaml",
    ROOT / "contracts" / "scholar_full_tool_surface.yaml",
    ROOT / "contracts" / "web_full_tool_surface.yaml",
    ROOT / "contracts" / "campaign_execution_trace.yaml",
    ROOT / "contracts" / "convergence_decision_report.yaml",
]

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".toml", ".py", ".html", ".txt"}

ALLOWED_SECURITY_FIXTURES = {
    "examples/vggt-human-prior-survey/shared_store_fixture/.env",
    "examples/vggt-human-prior-survey/shared_store_fixture/large/predictions.npz",
    "examples/vggt-human-prior-survey/shared_store_fixture/private/"
    + "SMPLX"
    + "_model.pkl",
}


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _text_files_under(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
        elif path.is_dir():
            files.extend(
                item
                for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES
            )
    return sorted(set(files))


def test_v1_3_public_surfaces_have_no_privacy_release_blockers() -> None:
    report = scan_privacy_paths(V1_3_PUBLIC_SURFACES)

    assert report.release_blocker is False
    assert report.findings == []
    assert report.requires_human_review is True


def test_v1_3_no_new_env_or_local_project_links_in_release_surface() -> None:
    offenders: list[str] = []
    for path in V1_3_PUBLIC_SURFACES + V1_3_CODE_SURFACES:
        if path.is_file():
            candidates = [path]
        elif path.is_dir():
            candidates = [item for item in path.rglob("*") if item.is_file()]
        else:
            candidates = []
        for candidate in candidates:
            relative = _relative(candidate)
            if relative in ALLOWED_SECURITY_FIXTURES:
                continue
            if candidate.name in {".env", "local_project_links" + ".yaml"}:
                offenders.append(relative)

    assert offenders == []


def test_v1_3_no_token_or_api_key_values_in_original_parity_surface() -> None:
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assignment_like = re.compile(
        r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret)\s*[:=]\s*"
        r"['\"]?[A-Za-z0-9][A-Za-z0-9_-]{11,}"
    )
    offenders: list[str] = []

    for path in _text_files_under(V1_3_PUBLIC_SURFACES + V1_3_CODE_SURFACES):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(),
            start=1,
        ):
            if token_like.search(line) or assignment_like.search(line):
                if "risk-register.md" in line:
                    continue
                offenders.append(f"{_relative(path)}:{line_number}")

    assert offenders == []


def test_v1_3_no_private_path_or_old_name_in_public_text() -> None:
    private_drive_path = "D:" + "/vggt"
    private_win_path = "D:" + "\\\\vggt"
    private_path_like = re.compile(
        rf"([A-Za-z]:\\Users\\[^\\\s]+|/home/[^/\s]+|{re.escape(private_drive_path)}|"
        rf"{re.escape(private_win_path)})"
    )
    old_name = "Tuling" + "Research"
    offenders: list[str] = []

    for path in _text_files_under(V1_3_PUBLIC_SURFACES):
        text = path.read_text(encoding="utf-8", errors="replace")
        if private_path_like.search(text) or old_name in text:
            offenders.append(_relative(path))

    assert offenders == []


def test_v1_3_no_raw_data_or_restricted_model_payloads_in_original_parity_surface() -> None:
    offenders: list[str] = []
    for path in V1_3_PUBLIC_SURFACES + V1_3_CODE_SURFACES:
        candidates = (
            [path]
            if path.is_file()
            else list(path.rglob("*"))
            if path.is_dir()
            else []
        )
        for candidate in candidates:
            if not candidate.is_file():
                continue
            relative = _relative(candidate)
            if relative in ALLOWED_SECURITY_FIXTURES:
                continue
            lowered_parts = {part.lower() for part in candidate.parts}
            if candidate.name.startswith("SMPLX" + "_") and candidate.suffix.lower() in {
                ".npz",
                ".pkl",
            }:
                offenders.append(relative)
            if candidate.name == "predictions.npz":
                offenders.append(relative)
            if "raw_data" in lowered_parts or "private_data" in lowered_parts:
                offenders.append(relative)

    assert offenders == []


def test_v1_3_no_unsafe_remote_execution_or_live_ssh_default() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in _text_files_under(V1_3_PUBLIC_SURFACES + V1_3_CODE_SURFACES)
    ).lower()

    blocked_enabled_phrases = [
        "remote execution enabled: `true`",
        "live ssh enabled by default",
        "live_ssh_enabled: true",
        "ssh provision enabled",
        "tmux attach enabled",
        "automatic git push enabled",
        "execute_unknown_plugin: true",
        "shell_access: true",
        "secrets_access: true",
    ]
    for phrase in blocked_enabled_phrases:
        assert phrase not in combined
    assert "\nremote_command_execution: true" not in combined

    required_boundaries = [
        "no remote command execution",
        "live ssh",
        "disabled by default",
        "human review",
    ]
    for boundary in required_boundaries:
        assert boundary in combined


def test_v1_3_no_paywall_bypass_or_default_live_network() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in _text_files_under(V1_3_PUBLIC_SURFACES + V1_3_CODE_SURFACES)
    ).lower()

    blocked_enabled_phrases = [
        "paywall bypass enabled",
        "paywall_bypass_allowed: true",
        "default network enabled",
        "default_network: true",
        "private content scraping enabled",
        "stores_cookies: true",
    ]
    for phrase in blocked_enabled_phrases:
        assert phrase not in combined

    assert "no paywall bypass" in combined
    assert "no default network" in combined or "no default live network" in combined


def test_v1_3_security_privacy_reports_exist_and_are_review_only() -> None:
    required = [
        ROOT / "docs" / "v1.3.0-security-audit.md",
        ROOT / "docs" / "v1.3.0-privacy-audit.md",
        ROOT / "docs" / "v1.3.0-secret-scan-report.md",
    ]

    for path in required:
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "pass with review" in text
        assert "human review" in text
        assert "not a certification" in text or "not legal advice" in text

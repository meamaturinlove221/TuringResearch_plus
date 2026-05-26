from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]

V1_2_DOCS = [
    ROOT / "docs" / "v1.2.0-final-scope.md",
    ROOT / "docs" / "v1.2.0-original-reference-parity-first.md",
    ROOT / "docs" / "reference-parity-dashboard.md",
    ROOT / "docs" / "turingresearch-research-catalog.md",
    ROOT / "docs" / "v1.2.0-full-workflow-replay-report.md",
    ROOT / "docs" / "v1.2.0-public-demo-refresh.md",
    ROOT / "docs" / "v1.2.0-interview-pack.md",
    ROOT / "docs" / "v1.2.0-architecture-story.md",
    ROOT / "docs" / "v1.2.0-reference-parity-story.md",
    ROOT / "docs" / "v1.2.0-why-not-aris-yet.md",
    ROOT / "docs" / "v1.2.0-interview-faq.md",
    ROOT / "docs" / ("neocortica" + "-parity-gate-report.md"),
    ROOT / "docs" / ("yogsoth" + "-parity-gate-report.md"),
    ROOT / "docs" / ("yogsoth" + "-vault-parity.md"),
    ROOT / "docs" / ("yogsoth" + "-ontology-parity.md"),
    ROOT / "docs" / ("yogsoth" + "-stress-test-parity.md"),
    ROOT / "docs" / ("yogsoth" + "-experiment-execution-parity.md"),
]

V1_2_PUBLIC_SURFACES = [
    *V1_2_DOCS,
    ROOT / ".mcp.example.json",
    ROOT / "examples" / "public_demo" / "v1_2_demo",
    ROOT / "examples" / "public_demo" / "reference_parity_dashboard.json",
    ROOT / "docs-site" / "pages" / "reference-parity.md",
]

V1_2_CODE_SURFACES = [
    ROOT / "src" / "turing_research_plus" / "pod_lifecycle",
    ROOT / "src" / "turing_research_plus" / "scholar_pipeline",
    ROOT / "src" / "turing_research_plus" / "web",
    ROOT / "src" / "turing_research_plus" / "campaigns",
    ROOT / "src" / "turing_research_plus" / "vault_graph",
    ROOT / "src" / "turing_research_plus" / "stress_test",
    ROOT / "src" / "turing_research_plus" / "experiment_execution",
    ROOT / "contracts" / "neocortica_session_parity.yaml",
    ROOT / "contracts" / "neocortica_scholar_parity.yaml",
    ROOT / "contracts" / "neocortica_web_parity.yaml",
    ROOT / "contracts" / "yogsoth_campaign_parity.yaml",
    ROOT / "contracts" / "yogsoth_vault_parity.yaml",
    ROOT / "contracts" / "yogsoth_ontology_parity.yaml",
    ROOT / "contracts" / "yogsoth_stress_test_parity.yaml",
    ROOT / "contracts" / "yogsoth_experiment_execution_parity.yaml",
]

ALLOWED_SECURITY_FIXTURES = {
    "examples/vggt-human-prior-survey/shared_store_fixture/.env",
    "examples/vggt-human-prior-survey/shared_store_fixture/large/predictions.npz",
    "examples/vggt-human-prior-survey/shared_store_fixture/private/"
    + "SMPLX"
    + "_model.pkl",
}

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".toml", ".py", ".html", ".txt"}


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


def test_v1_2_public_surfaces_have_no_privacy_release_blockers() -> None:
    report = scan_privacy_paths(V1_2_PUBLIC_SURFACES)

    assert report.release_blocker is False
    assert report.findings == []
    assert report.requires_human_review is True


def test_v1_2_no_env_or_local_project_links_in_release_surface() -> None:
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        if path.name in {".env", "local_project_links" + ".yaml"}:
            offenders.append(relative)

    assert offenders == []


def test_v1_2_no_token_or_api_key_values_in_public_surface() -> None:
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assignment_like = re.compile(
        r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret)\s*[:=]\s*"
        r"['\"]?[A-Za-z0-9][A-Za-z0-9_-]{11,}"
    )

    offenders: list[str] = []
    for path in _text_files_under(V1_2_PUBLIC_SURFACES + V1_2_CODE_SURFACES):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(),
            start=1,
        ):
            token_match = token_like.search(line)
            assignment_match = assignment_like.search(line)
            if not token_match and not assignment_match:
                continue
            if "v1.0.0-risk-register.md" in line:
                continue
            offenders.append(f"{_relative(path)}:{line_number}")

    assert offenders == []


def test_v1_2_no_private_path_or_old_name_in_public_text() -> None:
    private_drive_path = "D:" + "/vggt"
    private_win_path = "D:" + "\\\\vggt"
    private_path_like = re.compile(
        rf"([A-Za-z]:\\Users\\[^\\\s]+|/home/[^/\s]+|{re.escape(private_drive_path)}|"
        rf"{re.escape(private_win_path)})"
    )
    old_name = "Tuling" + "Research"
    offenders: list[str] = []

    for path in _text_files_under(V1_2_PUBLIC_SURFACES):
        text = path.read_text(encoding="utf-8", errors="replace")
        if private_path_like.search(text) or old_name in text:
            offenders.append(_relative(path))

    assert offenders == []


def test_v1_2_no_raw_data_or_restricted_model_payload_files() -> None:
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        if path.name.startswith("SMPLX" + "_") and path.suffix.lower() in {
            ".npz",
            ".pkl",
        }:
            offenders.append(relative)
        if path.name == "predictions.npz":
            offenders.append(relative)
        if "private_data" in path.parts or "secrets" in path.parts:
            offenders.append(relative)

    assert offenders == []


def test_v1_2_no_huge_npz_payloads_outside_allowed_fixtures() -> None:
    offenders: list[str] = []
    for path in ROOT.rglob("*.npz"):
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        if path.stat().st_size > 5_000_000:
            offenders.append(relative)

    assert offenders == []


def test_v1_2_no_unsafe_remote_execution_surface_enabled() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in _text_files_under(V1_2_PUBLIC_SURFACES + V1_2_CODE_SURFACES)
    ).lower()

    blocked_enabled_phrases = [
        "remote execution enabled",
        "ssh provision enabled",
        "tmux attach enabled",
        "automatic git push enabled",
        "modal execution enabled",
        "execute_unknown_plugin: true",
        "shell_access: true",
        "secrets_access: true",
    ]
    for phrase in blocked_enabled_phrases:
        assert phrase not in combined

    required_boundaries = [
        "no default networking",
        "no automatic experiment execution",
        "human review",
    ]
    for boundary in required_boundaries:
        assert boundary in combined


def test_v1_2_security_privacy_audit_reports_exist() -> None:
    required = [
        ROOT / "docs" / "v1.2.0-security-audit.md",
        ROOT / "docs" / "v1.2.0-privacy-audit.md",
        ROOT / "docs" / "v1.2.0-secret-scan-report.md",
    ]

    for path in required:
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "pass with review" in text
        assert "human review" in text
        assert "not a certification" in text or "not legal advice" in text

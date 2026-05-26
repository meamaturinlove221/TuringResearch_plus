from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TEXT_SUFFIXES = {".css", ".html", ".json", ".md", ".txt", ".yaml", ".yml"}

V1_5_SURFACES = [
    ROOT / "docs-site" / "dist",
    ROOT / "docs-site" / "dist_manifest.yaml",
    ROOT / "docs-site" / "deployment_dry_run_report.md",
    ROOT / "split_manual",
    ROOT / "examples" / "scholar_demo" / "live_optional",
    ROOT / "examples" / "apify_workflows" / "live_optional",
    ROOT / "examples" / "session_runtime" / "sftp_live_optional",
    ROOT / "examples" / "public_demo" / "dashboard_showcase",
    ROOT / "docs" / "v1.5.0-docs-sprint-gate-report.md",
    ROOT / "docs" / "v1.5.0-split-sprint-gate-report.md",
    ROOT / "docs" / "v1.5.0-optional-live-sprint-gate-report.md",
    ROOT / "docs" / "v1.5.0-dashboard-ux-gate-report.md",
    ROOT / "docs" / "v1.5.0-full-replay-report.md",
    ROOT / "docs" / "v1.5.0-security-audit.md",
    ROOT / "docs" / "v1.5.0-privacy-audit.md",
    ROOT / "docs" / "v1.5.0-secret-scan-report.md",
]


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


def _combined(paths: list[Path]) -> str:
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in _text_files_under(paths)
    )


def test_v1_5_security_privacy_reports_exist_and_are_review_only() -> None:
    for path in [
        ROOT / "docs" / "v1.5.0-security-audit.md",
        ROOT / "docs" / "v1.5.0-privacy-audit.md",
        ROOT / "docs" / "v1.5.0-secret-scan-report.md",
    ]:
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "pass with review" in text
        assert "human review" in text
        assert "not a certification" in text or "not legal advice" in text


def test_v1_5_required_public_surfaces_are_in_scope() -> None:
    required = [
        ROOT / "docs-site" / "dist" / "index.html",
        ROOT / "docs-site" / "dist_manifest.yaml",
        ROOT / "split_manual" / "turingresearch-vggt-case" / "manifest.yaml",
        ROOT / "split_manual" / "turingresearch-examples" / "manifest.yaml",
        ROOT / "examples" / "scholar_demo" / "live_optional" / "env.example",
        ROOT / "examples" / "apify_workflows" / "live_optional" / "env.example",
        ROOT / "examples" / "session_runtime" / "sftp_live_optional" / "env.example",
        ROOT / "examples" / "public_demo" / "dashboard_showcase" / "landing.html",
        ROOT / "examples" / "public_demo" / "dashboard_showcase" / "parity.html",
        ROOT / "examples" / "public_demo" / "dashboard_showcase" / "interview.html",
    ]
    for path in required:
        assert path.exists()


def test_v1_5_no_token_or_api_key_values() -> None:
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,}|"
        r"xox[baprs]-[A-Za-z0-9-]+)"
    )
    assignment_like = re.compile(
        r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret|password)\s*[:=]\s*"
        r"['\"]?[A-Za-z0-9][A-Za-z0-9_-]{11,}"
    )
    offenders: list[str] = []

    for path in _text_files_under(V1_5_SURFACES):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(),
            start=1,
        ):
            if token_like.search(line) or assignment_like.search(line):
                offenders.append(f"{_relative(path)}:{line_number}")

    assert offenders == []


def test_v1_5_no_env_files_or_local_project_links() -> None:
    offenders: list[str] = []
    for root in V1_5_SURFACES:
        candidates = (
            [root]
            if root.is_file()
            else list(root.rglob("*"))
            if root.is_dir()
            else []
        )
        for path in candidates:
            if path.is_file() and path.name in {".env", "local_project_links.yaml"}:
                offenders.append(_relative(path))

    assert offenders == []


def test_v1_5_no_private_paths_old_name_or_fake_urls() -> None:
    combined = _combined(V1_5_SURFACES)
    old_name = "Tuling" + "Research"
    private_drive_path = "D:" + "/vggt"
    private_win_path = "D:" + "\\vggt"
    private_path_like = re.compile(
        rf"([A-Za-z]:\\Users\\[^\\\s<]+|/home/[^/\s<]+|"
        rf"{re.escape(private_drive_path)}|{re.escape(private_win_path)})"
    )
    fake_url_like = re.compile(r"https?://(example\.com|github\.com/[^<\s)]+)")

    assert old_name not in combined
    assert "local_project_links.yaml" not in combined
    assert private_path_like.search(combined) is None
    assert fake_url_like.search(combined) is None
    assert "deployed at" not in combined
    assert "live URL:" not in combined


def test_v1_5_no_raw_data_or_restricted_model_payloads() -> None:
    offenders: list[str] = []
    blocked_names = {
        "predictions.npz",
        "private_data",
        "raw_data",
    }

    for root in V1_5_SURFACES:
        candidates = (
            [root]
            if root.is_file()
            else list(root.rglob("*"))
            if root.is_dir()
            else []
        )
        for path in candidates:
            relative = _relative(path)
            lowered_parts = {part.lower() for part in path.parts}
            if any(part in blocked_names for part in lowered_parts):
                offenders.append(relative)
            if path.name.startswith("SMPL" + "-X") or path.name.startswith("SMPLX_"):
                offenders.append(relative)
            if path.suffix.lower() in {".npz", ".pkl", ".pt", ".pth"}:
                offenders.append(relative)

    assert offenders == []


def test_v1_5_docs_site_dist_is_dry_run_only() -> None:
    manifest = (ROOT / "docs-site" / "dist_manifest.yaml").read_text(encoding="utf-8")
    report = (ROOT / "docs-site" / "deployment_dry_run_report.md").read_text(
        encoding="utf-8"
    )
    combined = manifest + "\n" + report

    assert "deployment_performed: false" in manifest
    assert "public_url: none" in manifest
    assert "deployment_performed: false" in combined
    assert "public_url: none" in combined
    assert "no_analytics: true" in manifest
    assert "analytics_enabled: true" not in manifest.lower()


def test_v1_5_optional_live_examples_use_blank_placeholders_only() -> None:
    combined = _combined(
        [
            ROOT / "examples" / "scholar_demo" / "live_optional",
            ROOT / "examples" / "apify_workflows" / "live_optional",
            ROOT / "examples" / "session_runtime" / "sftp_live_optional",
        ]
    )

    assert "SEMANTIC_SCHOLAR_API_KEY=" in combined
    assert "APIFY_TOKEN=" in combined
    assert "TURINGRESEARCH_SFTP_CREDENTIAL=" in combined
    assert "<private local value>" in combined
    assert "<private local key path placeholder>" in combined
    assert "BEGIN OPENSSH PRIVATE KEY" not in combined
    assert "password=" not in combined.lower()


def test_v1_5_dashboard_showcase_is_static_and_public_safe() -> None:
    combined = _combined([ROOT / "examples" / "public_demo" / "dashboard_showcase"])

    assert "static-local-first" in combined
    assert "<script" not in combined.lower()
    assert "http://" not in combined
    assert "https://" not in combined
    assert "No live provider call" in combined
    assert "No remote command execution" in combined
    assert "No automatic Evidence Ledger write" in combined

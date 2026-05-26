"""Read-only privacy scanner."""

from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.privacy.models import (
    PrivacyFinding,
    PrivacyPolicyRule,
    PrivacyScanReport,
    path_to_scan_label,
)
from turing_research_plus.privacy.policy import default_privacy_policy
from turing_research_plus.privacy.redaction import propose_redaction

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".html",
    ".csv",
}


def scan_privacy_paths(
    paths: list[Path],
    *,
    rules: list[PrivacyPolicyRule] | None = None,
    max_text_bytes: int = 500_000,
) -> PrivacyScanReport:
    """Scan files or directories without modifying them."""

    policy = rules or default_privacy_policy()
    files = _expand_files(paths)
    findings: list[PrivacyFinding] = []

    for path in files:
        label = path_to_scan_label(path)
        normalized = label.replace("\\", "/")
        size = path.stat().st_size
        findings.extend(_scan_path_rules(path, normalized, size, policy))
        if _is_text_file(path) and size <= max_text_bytes:
            text = path.read_text(encoding="utf-8", errors="replace")
            findings.extend(_scan_content_rules(normalized, text, policy))

    return PrivacyScanReport(
        scanned_paths=[path_to_scan_label(path) for path in files],
        findings=findings,
        requires_human_review=True,
        limitations=[
            "Scanner is pattern based and may have false positives or false negatives.",
            "Scanner never deletes files and never overwrites redactions.",
            "Human review is required before release or handoff.",
        ],
    )


def _expand_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        files.extend(item for item in path.rglob("*") if item.is_file())
    return sorted(files)


def _scan_path_rules(
    path: Path,
    normalized: str,
    size: int,
    rules: list[PrivacyPolicyRule],
) -> list[PrivacyFinding]:
    findings: list[PrivacyFinding] = []
    for rule in rules:
        path_match = any(re.search(pattern, normalized) for pattern in rule.path_patterns)
        size_match = (
            rule.max_size_bytes is not None
            and path.suffix.lower() == ".npz"
            and size > rule.max_size_bytes
        )
        if not path_match and not size_match:
            continue
        findings.append(
            PrivacyFinding(
                path=normalized,
                finding_type=rule.finding_type,
                safety_level=rule.safety_level,
                severity=rule.severity,
                matched_rule=rule.rule_id,
                message=rule.description,
                recommended_action=rule.recommended_action,
                redaction_possible=rule.redaction_possible,
                release_blocker=rule.release_blocker,
                proposed_redaction=None,
            )
        )
    return findings


def _scan_content_rules(
    normalized: str,
    text: str,
    rules: list[PrivacyPolicyRule],
) -> list[PrivacyFinding]:
    findings: list[PrivacyFinding] = []
    lines = text.splitlines()
    for rule in rules:
        for pattern in rule.content_patterns:
            for index, line in enumerate(lines, start=1):
                if not re.search(pattern, line):
                    continue
                findings.append(
                    PrivacyFinding(
                        path=normalized,
                        finding_type=rule.finding_type,
                        safety_level=rule.safety_level,
                        severity=rule.severity,
                        matched_rule=rule.rule_id,
                        message=rule.description,
                        recommended_action=rule.recommended_action,
                        redaction_possible=rule.redaction_possible,
                        release_blocker=rule.release_blocker,
                        line_number=index,
                        proposed_redaction=propose_redaction(normalized, line, rule),
                    )
                )
    return findings


def _is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {".env", ".env.example"}

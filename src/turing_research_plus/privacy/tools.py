"""Local tool wrappers for privacy policy scanning."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.privacy.models import PrivacyScanReport
from turing_research_plus.privacy.report import render_privacy_scan_report_markdown
from turing_research_plus.privacy.scanner import scan_privacy_paths


def privacy_scan(paths: list[Path]) -> PrivacyScanReport:
    """Run a read-only privacy scan."""

    return scan_privacy_paths(paths)


def privacy_scan_markdown(paths: list[Path]) -> str:
    """Run a read-only privacy scan and render Markdown."""

    return render_privacy_scan_report_markdown(privacy_scan(paths))

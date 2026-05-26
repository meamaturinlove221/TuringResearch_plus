"""Docs-site link and public-safety checks."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

FindingKind = Literal[
    "broken_link",
    "missing_page",
    "missing_source_doc",
    "orphan_page",
    "private_path",
]

Severity = Literal["warning", "error"]

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\((?P<target>[^)]+)\)")
PRIVATE_PATH_PATTERNS = (
    re.compile(r"\bD:[\\/]+vggt\b", re.IGNORECASE),
    re.compile(r"\blocal_project_links\.yaml\b", re.IGNORECASE),
    re.compile(r"\.env(?:\b|$)", re.IGNORECASE),
    re.compile(r"\bghp_[A-Za-z0-9_]+\b"),
    re.compile(r"\bsk-[A-Za-z0-9_]+\b"),
    re.compile(r"\b[A-Za-z]:[\\/]+Users[\\/]+[^`\s)]+", re.IGNORECASE),
)


class DocsSiteLinkFinding(BaseModel):
    """One docs-site hardening finding."""

    model_config = ConfigDict(extra="forbid")

    kind: FindingKind
    path: str = Field(min_length=1)
    target: str = ""
    message: str = Field(min_length=1)
    severity: Severity = "error"


class DocsSiteLinkCheckReport(BaseModel):
    """Structured report for docs-site links and source docs."""

    model_config = ConfigDict(extra="forbid")

    docs_site_root: Path
    nav_path: Path
    manifest_path: Path
    nav_validation_warnings: list[str] = Field(default_factory=list)
    broken_links: list[DocsSiteLinkFinding] = Field(default_factory=list)
    missing_pages: list[DocsSiteLinkFinding] = Field(default_factory=list)
    missing_source_docs: list[DocsSiteLinkFinding] = Field(default_factory=list)
    orphan_pages: list[DocsSiteLinkFinding] = Field(default_factory=list)
    private_path_hits: list[DocsSiteLinkFinding] = Field(default_factory=list)
    checked_pages: list[str] = Field(default_factory=list)
    checked_source_docs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def hardening_report_requires_review(self) -> DocsSiteLinkCheckReport:
        if not self.requires_human_review:
            raise ValueError("docs-site link check report requires human review")
        return self

    @property
    def has_blockers(self) -> bool:
        return any(
            (
                self.broken_links,
                self.missing_pages,
                self.missing_source_docs,
                self.private_path_hits,
            )
        )


def check_docs_site_links(
    repo_root: Path,
    *,
    docs_site_root: Path | None = None,
    nav_path: Path | None = None,
    manifest_path: Path | None = None,
) -> DocsSiteLinkCheckReport:
    """Check docs-site nav pages, source docs, local Markdown links, and safety."""

    root = repo_root.resolve()
    site_root = (docs_site_root or root / "docs-site").resolve()
    nav_file = (nav_path or site_root / "nav.yaml").resolve()
    manifest_file = (manifest_path or site_root / "site_manifest.yaml").resolve()

    nav = load_docs_site_nav(nav_file)
    manifest = load_docs_site_manifest(manifest_file)
    nav_warnings = validate_nav_against_manifest(nav, manifest)

    expected_pages = {item.page for item in nav.items}
    checked_pages: list[str] = []
    checked_source_docs: list[str] = []
    broken_links: list[DocsSiteLinkFinding] = []
    missing_pages: list[DocsSiteLinkFinding] = []
    missing_sources: list[DocsSiteLinkFinding] = []

    for item in nav.items:
        page_path = _resolve_within(site_root, item.page)
        checked_pages.append(_display(page_path, root))
        for source_doc in item.source_docs:
            source_path = _resolve_within(site_root, source_doc)
            checked_source_docs.append(source_doc)
            if source_path is None or not source_path.exists():
                missing_sources.append(
                    DocsSiteLinkFinding(
                        kind="missing_source_doc",
                        path=item.page,
                        target=source_doc,
                        message=f"source doc is missing: {source_doc}",
                    )
                )
        if page_path is None or not page_path.exists():
            missing_pages.append(
                DocsSiteLinkFinding(
                    kind="missing_page",
                    path=item.page,
                    message=f"nav page is missing: {item.page}",
                )
            )
            continue
        broken_links.extend(_check_markdown_links(page_path, root))

    actual_pages = {
        _relative_posix(path, site_root)
        for path in (site_root / "pages").glob("*.md")
        if path.is_file()
    }
    orphan_pages = [
        DocsSiteLinkFinding(
            kind="orphan_page",
            path=page,
            message=f"docs-site page is not referenced by nav: {page}",
            severity="warning",
        )
        for page in sorted(actual_pages - expected_pages)
    ]

    page_files = sorted((site_root / "pages").glob("*.md"))
    private_hits = _scan_private_paths([nav_file, manifest_file, *page_files], root)

    return DocsSiteLinkCheckReport(
        docs_site_root=site_root,
        nav_path=nav_file,
        manifest_path=manifest_file,
        nav_validation_warnings=nav_warnings,
        broken_links=broken_links,
        missing_pages=missing_pages,
        missing_source_docs=missing_sources,
        orphan_pages=orphan_pages,
        private_path_hits=private_hits,
        checked_pages=checked_pages,
        checked_source_docs=checked_source_docs,
    )


def render_link_check_markdown(report: DocsSiteLinkCheckReport) -> str:
    """Render a concise Markdown link-check report."""

    status = "blocked" if report.has_blockers else "pass"
    lines = [
        "# Docs Site Link Check Report",
        "",
        f"Status: {status}.",
        "",
        f"Checked pages: {len(report.checked_pages)}.",
        f"Checked source docs: {len(report.checked_source_docs)}.",
        f"Requires human review: {str(report.requires_human_review).lower()}.",
        "",
    ]
    sections = [
        ("Nav validation warnings", report.nav_validation_warnings),
        ("Missing pages", [item.message for item in report.missing_pages]),
        ("Broken links", [item.message for item in report.broken_links]),
        ("Missing source docs", [item.message for item in report.missing_source_docs]),
        ("Orphan pages", [item.message for item in report.orphan_pages]),
        ("Private path hits", [item.message for item in report.private_path_hits]),
    ]
    for title, items in sections:
        lines.extend([f"## {title}", ""])
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _check_markdown_links(page_path: Path, repo_root: Path) -> list[DocsSiteLinkFinding]:
    findings: list[DocsSiteLinkFinding] = []
    text = page_path.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group("target").strip()
        if _is_external_or_anchor(target):
            continue
        clean_target = target.split("#", 1)[0]
        if not clean_target:
            continue
        target_path = (page_path.parent / clean_target).resolve()
        if not target_path.exists():
            findings.append(
                DocsSiteLinkFinding(
                    kind="broken_link",
                    path=_display(page_path, repo_root),
                    target=target,
                    message=f"broken local link in {_display(page_path, repo_root)}: {target}",
                )
            )
    return findings


def _scan_private_paths(paths: list[Path], repo_root: Path) -> list[DocsSiteLinkFinding]:
    findings: list[DocsSiteLinkFinding] = []
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in PRIVATE_PATH_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        DocsSiteLinkFinding(
                            kind="private_path",
                            path=_display(path, repo_root),
                            target=f"line {line_number}",
                            message=(
                                f"possible private path or secret marker in "
                                f"{_display(path, repo_root)}:{line_number}"
                            ),
                        )
                    )
    return findings


def _resolve_within(base: Path, target: str) -> Path | None:
    resolved = (base / target).resolve()
    try:
        resolved.relative_to(base.parent)
    except ValueError:
        return None
    return resolved


def _relative_posix(path: Path, base: Path) -> str:
    return path.resolve().relative_to(base.resolve()).as_posix()


def _display(path: Path | None, repo_root: Path) -> str:
    if path is None:
        return "<invalid>"
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _is_external_or_anchor(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
    )

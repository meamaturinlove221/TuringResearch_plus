"""Markdown reports for upstream baselines and diffs."""

from __future__ import annotations

from turing_research_plus.upstream.models import UpstreamBaselineSet, UpstreamDiffReport


def render_baseline_report(baseline: UpstreamBaselineSet) -> str:
    """Render a baseline set as Markdown."""

    lines = [
        "# TuringResearch Plus Upstream Watch Baseline",
        "",
        f"- Baseline ID: `{baseline.baseline_id}`",
        f"- Generated at: `{baseline.generated_at}`",
        "- This is a public metadata baseline; it does not copy upstream code.",
        "- If this is the first baseline, it cannot prove newly added upstream features.",
        "",
        "## Repositories",
        "",
        "| Repository | Status | Default branch | Latest commit | Focus files |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for repo in baseline.repositories:
        status = "unresolved" if repo.unresolved_reason else "resolved"
        commit = repo.latest_commit_sha[:12] if repo.latest_commit_sha else ""
        lines.append(
            f"| `{repo.repository_full_name}` | {status} | `{repo.default_branch}` | "
            f"`{commit}` | {len(repo.file_hashes)} |"
        )
        if repo.unresolved_reason:
            lines.append(
                f"| `{repo.repository_full_name}` reason | {repo.unresolved_reason} |  |  |  |"
            )
    return "\n".join(lines) + "\n"


def render_diff_report(report: UpstreamDiffReport) -> str:
    """Render a diff report as Markdown."""

    title = "Initial Baseline" if report.is_initial_baseline else "Diff Report"
    lines = [
        f"# TuringResearch Plus Upstream Watch {title}",
        "",
        f"- Report ID: `{report.report_id}`",
        f"- New baseline: `{report.new_baseline_id}`",
    ]
    if report.old_baseline_id:
        lines.append(f"- Old baseline: `{report.old_baseline_id}`")
    if report.is_initial_baseline:
        lines.append("- This is the first baseline; do not treat entries as newly added changes.")
    lines.extend(["", "## Changes", ""])
    if not report.changes:
        lines.append("- No changes detected.")
    for change in report.changes:
        path = f" `{change.path}`" if change.path else ""
        lines.append(
            f"- `{change.repository_full_name}` `{change.category.value}`{path}: "
            f"{change.summary}"
        )
    return "\n".join(lines) + "\n"

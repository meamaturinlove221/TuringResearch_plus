"""Markdown rendering for compliance reports."""

from __future__ import annotations

from turing_research_plus.compliance.models import ComplianceAsset, ComplianceReport


def render_compliance_report_markdown(report: ComplianceReport) -> str:
    """Render a compliance report as Markdown."""

    lines = [
        f"# Compliance Report: {report.report_id}",
        "",
        f"- Redistribution risk: `{report.redistribution_risk}`",
        f"- Publication risk: `{report.publication_risk}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        f"- Disclaimer: {report.disclaimer}",
        "",
        "## Datasets",
        "",
        *_render_asset_list(report.datasets),
        "",
        "## Models",
        "",
        *_render_asset_list(report.models),
        "",
        "## Papers",
        "",
        *_render_asset_list(report.papers),
        "",
        "## Code Repositories",
        "",
        *_render_asset_list(report.code_repos),
        "",
        "## Licenses",
        "",
        *_render_text_list(report.licenses, code=True),
        "",
        "## Usage Restrictions",
        "",
        *_render_text_list(report.usage_restrictions),
        "",
        "## Missing License Info",
        "",
        *_render_text_list(report.missing_license_info, code=True),
        "",
        "## Findings",
        "",
    ]
    if report.findings:
        for finding in report.findings:
            lines.append(
                "- "
                f"`{finding.risk_level}` `{finding.asset_type}` `{finding.asset_id}`: "
                f"{finding.message} Action: {finding.recommended_action} "
                f"Release blocker: `{str(finding.release_blocker).lower()}`"
            )
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This report is a compliance checklist, not legal advice.",
            "- It does not download licenses or package restricted assets.",
            "- Human review is required before publication or redistribution.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_asset_list(assets: list[ComplianceAsset]) -> list[str]:
    if not assets:
        return ["- none"]
    lines: list[str] = []
    for asset in assets:
        restrictions = "; ".join(asset.usage_restrictions) or "none recorded"
        lines.append(
            "- "
            f"`{asset.asset_id}` {asset.name} "
            f"(license: `{asset.license_name}`, status: `{asset.license_status}`, "
            f"bundled: `{str(asset.bundled).lower()}`, "
            f"public release allowed: `{str(asset.public_release_allowed).lower()}`, "
            f"requires human review: `{str(asset.requires_human_review).lower()}`) "
            f"restrictions: {restrictions}"
        )
    return lines


def _render_text_list(items: list[str], *, code: bool = False) -> list[str]:
    if not items:
        return ["- none"]
    if code:
        return [f"- `{item}`" for item in items]
    return [f"- {item}" for item in items]

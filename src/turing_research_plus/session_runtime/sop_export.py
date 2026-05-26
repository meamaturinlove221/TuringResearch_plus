"""SOP export for generated Session shell script equivalents."""

from __future__ import annotations

from turing_research_plus.session_runtime.script_safety import ScriptSafetyReport


def render_session_script_sop(
    *,
    script_names: list[str],
    safety_reports: list[ScriptSafetyReport],
) -> str:
    """Render the human review SOP for exported Session scripts."""

    safety_by_name = {report.script_name: report for report in safety_reports}
    lines = [
        "# Session Shell Script Equivalent SOP",
        "",
        "Status: review-only export.",
        "",
        "These scripts are generated equivalents for manual review. They are not",
        "executed by TuringResearch during export.",
        "",
        "## Review Order",
        "",
    ]
    lines.extend([f"{index}. `{name}`" for index, name in enumerate(script_names, start=1)])
    lines.extend(
        [
            "",
            "## Safety Rules",
            "",
            "- inspect every script before manual use;",
            "- keep live steps commented unless a human explicitly reviews them;",
            "- do not paste credentials into scripts;",
            "- do not add destructive commands;",
            "- do not add remote command execution;",
            "- do not write Evidence Ledger entries automatically;",
            "",
            "## Script Safety Summary",
            "",
        ]
    )
    for name in script_names:
        report = safety_by_name[name]
        lines.append(f"- `{name}`: `{report.status}`")
    return "\n".join(lines) + "\n"

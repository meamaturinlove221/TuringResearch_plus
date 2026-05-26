"""Markdown export for capability manifests."""

from __future__ import annotations

from collections import defaultdict

from turing_research_plus.capabilities.models import CapabilityManifest


def render_capability_manifest_markdown(manifest: CapabilityManifest) -> str:
    """Render the capability manifest as Markdown."""

    lines = [
        f"# Capability Manifest: {manifest.manifest_id}",
        "",
        f"- Project: `{manifest.project}`",
        f"- Capability count: `{len(manifest.capabilities)}`",
        f"- Categories: `{len(manifest.categories)}`",
        f"- Requires human review: `{str(manifest.requires_human_review).lower()}`",
        f"- Starts MCP server: `{str(manifest.starts_mcp_server).lower()}`",
        f"- Executes tools: `{str(manifest.executes_tools).lower()}`",
        "",
        "| Capability | Category | Tool | Module | Live | Fake | Safety | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in sorted(manifest.capabilities, key=lambda item: item.capability_id):
        tool_name = entry.tool_name or "none"
        lines.append(
            f"| `{entry.capability_id}` | `{entry.category}` | `{tool_name}` | "
            f"`{entry.module}` | `{str(entry.live_mode).lower()}` | "
            f"`{str(entry.fake_mode).lower()}` | `{entry.safety_level}` | "
            f"`{entry.status}` |"
        )

    lines.extend(["", "## Coverage", ""])
    by_category: dict[str, list[str]] = defaultdict(list)
    for entry in manifest.capabilities:
        by_category[entry.category.value].append(entry.capability_id)
    for category in sorted(by_category):
        capability_list = ", ".join(f"`{item}`" for item in sorted(by_category[category]))
        lines.append(f"- `{category}`: {capability_list}")

    lines.extend(
        [
            "",
            "## Safety Boundary",
            "",
            "- The manifest is generated from a static review catalog.",
            "- It does not execute tools.",
            "- It does not start an MCP server.",
            "- Live capabilities remain opt-in and require explicit environment gates.",
            "- Entries describe capability surfaces; they do not verify research claims.",
            "",
        ]
    )
    return "\n".join(lines)

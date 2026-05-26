"""Text templates for pod workflow packs."""

from __future__ import annotations


def project_context(route_id: str) -> str:
    """Return VGGT route project context Markdown."""

    return "\n".join(
        [
            "# PROJECT CONTEXT",
            "",
            "TuringResearch Plus is preparing a review-only context package for a future",
            "VGGT-side Modal SparseConv3D experiment route.",
            "",
            f"- Route: `{route_id}`",
            "- Status: planned",
            "- Execution: not executed by TuringResearch",
            "- Required boundary: do not claim SparseConv3D success without real evidence.",
        ]
    ) + "\n"


def memory_summary(route_id: str) -> str:
    """Return handoff-safe MEMORY.md summary text."""

    return "\n".join(
        [
            f"Route `{route_id}` is planned and requires a real experiment.",
            "SparseConv3D success is not observed.",
            "Evidence Ledger, Artifact Audit, Run Ingest, and Handoff Manifest remain "
            "source of truth.",
            "Future pod outputs must return structured artifacts for review.",
        ]
    ) + "\n"


def readme(pack_id: str, route_id: str) -> str:
    """Return pack README text."""

    return "\n".join(
        [
            f"# {pack_id}",
            "",
            "This is a TuringResearch Plus pod workflow pack for future operator-controlled",
            "VGGT / Modal / RunPod work.",
            "",
            f"- Route: `{route_id}`",
            "- Status: planned",
            "- Execution: not executed by TuringResearch",
            "- Remote execution: not controlled by this package",
            "- Review: required before any Evidence Ledger update",
            "",
            "Use `STRUCTURED_OUTPUT_TEMPLATE/` for returned outputs.",
        ]
    ) + "\n"

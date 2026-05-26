"""Optional Codex prompt generation for SOP outputs."""

from turing_research_plus.sop.models import SOPGraph


def generate_codex_prompt(graph: SOPGraph) -> str:
    """Generate a concise Codex prompt for executing an SOP graph."""

    gates = ", ".join(graph.quality_gates)
    failures = ", ".join(graph.failure_gates)
    return (
        f"Execute the TuringResearch Plus SOP `{graph.graph_id}` in dry-run mode. "
        f"Use tools: {', '.join(graph.tools) or 'none'}. "
        f"Respect quality gates: {gates}. "
        f"Stop on failure gates: {failures}."
    )

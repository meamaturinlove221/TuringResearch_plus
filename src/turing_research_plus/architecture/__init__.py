"""Text architecture diagram generation for TuringResearch Plus."""

from turing_research_plus.architecture.graph_builder import (
    build_architecture_from_method_card,
    build_architecture_from_route,
)
from turing_research_plus.architecture.graphviz_export import export_architecture_graphviz
from turing_research_plus.architecture.markdown_export import export_architecture_markdown
from turing_research_plus.architecture.mermaid_export import export_architecture_mermaid
from turing_research_plus.architecture.models import (
    ArchitectureDiagramSpec,
    ArchitectureEdge,
    ArchitectureNode,
    ArchitectureSourceType,
)

__all__ = [
    "ArchitectureDiagramSpec",
    "ArchitectureEdge",
    "ArchitectureNode",
    "ArchitectureSourceType",
    "build_architecture_from_method_card",
    "build_architecture_from_route",
    "export_architecture_graphviz",
    "export_architecture_markdown",
    "export_architecture_mermaid",
]

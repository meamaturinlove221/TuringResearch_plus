"""Thin local tool wrappers for pod workflow packs."""

from __future__ import annotations

from typing import Any

from turing_research_plus.pod_workflow.models import PodWorkflowPackBuildInput
from turing_research_plus.pod_workflow.pack_builder import build_vggt_modal_pod_workflow_pack


def pod_workflow_pack_build_tool(request: PodWorkflowPackBuildInput) -> dict[str, Any]:
    """Build a local pod workflow pack and return metadata."""

    return build_vggt_modal_pod_workflow_pack(request).model_dump(mode="json")

from pathlib import Path

from turing_research_plus.architecture.graph_builder import (
    build_architecture_from_method_card,
    build_architecture_from_route,
)
from turing_research_plus.architecture.graphviz_export import export_architecture_graphviz
from turing_research_plus.architecture.markdown_export import export_architecture_markdown
from turing_research_plus.architecture.mermaid_export import export_architecture_mermaid
from turing_research_plus.experiment_route.compiler import compile_experiment_route
from turing_research_plus.experiment_route.models import ExperimentRouteCompileInput
from turing_research_plus.failure.attribution import build_failure_attribution_report
from turing_research_plus.failure.models import FailureCategory, FailureInstance
from turing_research_plus.hard_gates.models import (
    GateInputRef,
    GateOutcome,
    HardGateValidationInput,
)
from turing_research_plus.hard_gates.validator import validate_hard_gates
from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.markdown_export import export_method_card_markdown
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType

ROUTE_FIXTURE = Path("examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml")
NEURALBODY_FIXTURE = Path(
    "examples/vggt-human-prior-survey/paper_method_cards/neuralbody.fixture.md"
)


def test_sprint2_fake_route_gate_failure_method_architecture_flow() -> None:
    route, prompt = compile_experiment_route(ExperimentRouteCompileInput(route_path=ROUTE_FIXTURE))
    gate_report = validate_hard_gates(
        HardGateValidationInput(
            route_id=route.route_id,
            gate_ids=["real_backend_required", "visual_board_required"],
            inputs=[
                GateInputRef(
                    ref_id="real_backend_required",
                    ref_type="backend",
                    status="requires-real-experiment",
                    summary="real backend has not run",
                ),
                GateInputRef(
                    ref_id="visual_board_required",
                    ref_type="visual",
                    status="not-enough-evidence",
                    summary="board proof is missing",
                ),
            ],
        )
    )
    failure_report = build_failure_attribution_report(
        FailureInstance(
            failure_id="f-sprint2-visual",
            related_route_id=route.route_id,
            related_stage_id="stage_3",
            text="missing board proof",
        )
    )
    method_card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=NEURALBODY_FIXTURE,
        )
    )
    method_arch = build_architecture_from_method_card(method_card)
    route_arch = build_architecture_from_route(route)

    assert route.model_dump(mode="json")
    assert prompt.model_dump(mode="json")
    assert gate_report.model_dump(mode="json")
    assert failure_report.model_dump(mode="json")
    assert method_card.model_dump(mode="json")
    assert method_arch.model_dump(mode="json")
    assert route_arch.model_dump(mode="json")

    assert "# Experiment Route:" in route.to_markdown()
    assert "# Hard Gate Validation:" in gate_report.to_markdown()
    assert "# Failure Attribution:" in failure_report.to_markdown()
    assert "# Method Card:" in export_method_card_markdown(method_card)
    assert "# Architecture Diagram:" in export_architecture_markdown(method_arch)

    assert gate_report.passed is False
    assert {result.outcome for result in gate_report.results} == {GateOutcome.NOT_ENOUGH_EVIDENCE}
    assert failure_report.category == FailureCategory.VISUAL_PROOF_INSUFFICIENT
    assert failure_report.requires_human_review is True
    assert method_card.requires_human_review is True
    assert "complete paper reading" in " ".join(method_card.limitations)
    assert method_arch.requires_human_review is True
    assert "derived-from-fixture" in " ".join(method_arch.limitations)
    assert route_arch.requires_human_review is True

    mermaid = export_architecture_mermaid(route_arch)
    dot = export_architecture_graphviz(route_arch)
    markdown = export_architecture_markdown(route_arch)
    assert mermaid.startswith("flowchart TB")
    assert "subgraph" in mermaid
    assert dot.startswith('digraph "modal_sparseconv_v0_architecture"')
    assert "```mermaid" in markdown
    assert "not executed by TuringResearch" in route.final_states


def test_sprint2_advisor_linkage_is_referenceable_without_rebuild() -> None:
    route, _prompt = compile_experiment_route(ExperimentRouteCompileInput(route_path=ROUTE_FIXTURE))
    failure_report = build_failure_attribution_report(
        FailureInstance(
            failure_id="f-sprint2-assets",
            related_route_id=route.route_id,
            text="V260 missing adjacent predictions / semantic assets",
        )
    )
    method_card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=NEURALBODY_FIXTURE,
        )
    )
    architecture = build_architecture_from_method_card(method_card)

    advisor_refs = {
        "route_id": route.route_id,
        "failure_id": failure_report.failure_id,
        "method_card_id": method_card.paper_id,
        "architecture_id": architecture.diagram_id,
    }

    assert advisor_refs == {
        "route_id": "modal_sparseconv_v0",
        "failure_id": "f-sprint2-assets",
        "method_card_id": "neuralbody-fixture",
        "architecture_id": "neuralbody_fixture_architecture",
    }

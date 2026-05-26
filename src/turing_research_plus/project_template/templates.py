"""Text templates for generated research project skeletons."""

from __future__ import annotations

from collections.abc import Callable

from turing_research_plus.project_template.models import ProjectTemplateRequest

TemplateRenderer = Callable[[ProjectTemplateRequest], str]


def render_readme(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            f"# {request.project_name}",
            "",
            f"Project ID: `{request.project_id}`",
            f"Topic: {request.topic}",
            "",
            "## North Star",
            "",
            request.north_star,
            "",
            "## Boundary",
            "",
            "- This is a generated research project skeleton.",
            "- It contains no experiment results.",
            "- Planned work must remain planned until evidence is added.",
            "- Human review is required before public use.",
            "",
        ]
    )


def render_north_star(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# North Star",
            "",
            f"Project: {request.project_name}",
            f"Topic: {request.topic}",
            "",
            request.north_star,
            "",
            "## Success Criteria",
            "",
            "- Define evidence-backed research goals.",
            "- Keep experiment plans separate from observed results.",
            "- Record blockers and missing evidence explicitly.",
            "",
        ]
    )


def render_evidence_ledger(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Evidence Ledger",
            "",
            "Status: empty template.",
            "",
            "| Evidence ID | Status | Source Ref | Notes |",
            "| --- | --- | --- | --- |",
            f"| `{request.project_id}-seed` | `planned` | `README.md` | "
            "Initial project skeleton only. |",
            "",
            "Allowed statuses: observed, local-observed, planned, hard-blocked,",
            "not-enough-evidence, requires-human-review.",
            "",
        ]
    )


def render_artifact_plan(_: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Artifact Plan",
            "",
            "## Expected Artifacts",
            "",
            "- manifests",
            "- summaries",
            "- small review files",
            "- sha256 inventories",
            "",
            "## Safety",
            "",
            "- Do not store secrets.",
            "- Do not store raw data by default.",
            "- Large files should be represented by metadata and hashes.",
            "",
        ]
    )


def render_experiment_routes(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Experiment Routes",
            "",
            "Status: planned routes only.",
            "",
            "## Seed Route",
            "",
            f"- Route ID: `{request.project_id}-route-001`",
            "- Status: planned",
            "- Requires real experiment evidence before any success claim.",
            "",
        ]
    )


def render_related_work(_: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Related Work",
            "",
            "Status: requires real paper review.",
            "",
            "## Groups",
            "",
            "- direct baselines",
            "- adjacent methods",
            "- datasets and benchmarks",
            "- unknown or requires review",
            "",
            "Do not write final paper claims from this template alone.",
            "",
        ]
    )


def render_advisor_pack(_: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Advisor Pack",
            "",
            "Status: draft template.",
            "",
            "## Include",
            "",
            "- north star",
            "- current evidence state",
            "- artifact readiness",
            "- risks and blockers",
            "- next actions",
            "",
        ]
    )


def render_master_ledger(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Master Ledger",
            "",
            f"## Bootstrap - {request.project_name}",
            "",
            "- Status: project template generated.",
            "- No experiment has been executed.",
            "- No observed evidence has been added.",
            "- Human review required.",
            "",
        ]
    )


def render_contract_readme(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Contracts",
            "",
            f"Contracts for `{request.project_id}` will live here.",
            "",
            "Start with schema drafts and keep generated outputs JSON-serializable.",
            "",
        ]
    )


def render_examples_readme(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Examples",
            "",
            f"Examples for `{request.project_id}` will live here.",
            "",
            "Use fake or manually reviewed fixtures until real evidence exists.",
            "",
        ]
    )


def render_feature_capsules_readme(request: ProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Feature Capsules",
            "",
            f"Feature capsules for `{request.project_id}` will live here.",
            "",
            "Each capsule should define problem, inputs, outputs, tests, risks,",
            "done criteria, and non-goals.",
            "",
        ]
    )


PROJECT_TEMPLATE_FILES: dict[str, tuple[str, TemplateRenderer]] = {
    "README.md": ("project-readme", render_readme),
    "docs/north_star.md": ("north-star", render_north_star),
    "docs/evidence_ledger.md": ("evidence-ledger", render_evidence_ledger),
    "docs/artifact_plan.md": ("artifact-plan", render_artifact_plan),
    "docs/experiment_routes.md": ("experiment-routes", render_experiment_routes),
    "docs/related_work.md": ("related-work", render_related_work),
    "docs/advisor_pack.md": ("advisor-pack", render_advisor_pack),
    "lanes/00_master_ledger.md": ("master-ledger", render_master_ledger),
    "examples/README.md": ("examples-readme", render_examples_readme),
    "contracts/README.md": ("contracts-readme", render_contract_readme),
    "race/feature_capsules/README.md": (
        "feature-capsules-readme",
        render_feature_capsules_readme,
    ),
}

REQUIRED_DIRECTORIES = [
    "docs",
    "lanes",
    "examples",
    "contracts",
    "race",
    "race/feature_capsules",
]

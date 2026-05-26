"""Renderers for typed reusable research project templates."""

from __future__ import annotations

from collections.abc import Callable

from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.schema import ResearchProjectTemplateRequest

ResearchTemplateRenderer = Callable[[ResearchProjectTemplateRequest], str]


def render_research_template_file(
    relative_path: str,
    request: ResearchProjectTemplateRequest,
) -> str:
    """Render one typed project template file."""

    renderer = RESEARCH_TEMPLATE_RENDERERS[relative_path]
    return renderer(request)


def render_readme(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            f"# {request.project_name}",
            "",
            "Status: template / placeholder.",
            "",
            f"- Project ID: `{request.project_id}`",
            f"- Template type: `{request.template_type}`",
            f"- Topic: {request.topic}",
            f"- Owner: {request.owner}",
            "",
            "## North Star",
            "",
            request.north_star,
            "",
            "## Template Boundary",
            "",
            "- This project was generated from a reusable template.",
            "- It contains no observed evidence.",
            "- It contains no real citations.",
            "- It contains no experiment results.",
            "- Human review is required before public or advisor use.",
            "",
        ]
    )


def render_north_star(request: ResearchProjectTemplateRequest) -> str:
    focus = _template_focus(request.template_type)
    return "\n".join(
        [
            "# North Star",
            "",
            "Status: template / placeholder.",
            "",
            f"Project: {request.project_name}",
            f"Topic: {request.topic}",
            "",
            request.north_star,
            "",
            "## Focus",
            "",
            f"- {focus}",
            "- Convert planned work into observed evidence only after review.",
            "- Keep missing evidence explicit.",
            "",
        ]
    )


def render_research_questions(request: ResearchProjectTemplateRequest) -> str:
    questions = request.research_questions or _default_questions(request.template_type)
    lines = ["# Research Questions", "", "Status: template / placeholder.", ""]
    lines.extend(f"- {question}" for question in questions)
    lines.extend(["", "These questions are planning prompts, not conclusions.", ""])
    return "\n".join(lines)


def render_evidence_ledger(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Evidence Ledger",
            "",
            "Status: template / placeholder.",
            "",
            "| Evidence ID | Status | Source Ref | Notes |",
            "| --- | --- | --- | --- |",
            f"| `{request.project_id}-seed` | `planned` | `README.md` | "
            "Generated template seed; not observed evidence. |",
            "",
            "Allowed statuses: planned, observed, local-observed, hard-blocked,",
            "not-enough-evidence, requires-human-review.",
            "",
            "Do not mark template content as observed.",
            "",
        ]
    )


def render_artifact_plan(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Artifact Plan",
            "",
            "Status: template / placeholder.",
            "",
            "## Expected Artifacts",
            "",
            *_artifact_prompts(request.template_type),
            "",
            "## Safety",
            "",
            "- Do not store secrets.",
            "- Do not store raw data by default.",
            "- Do not store private model files.",
            "- Large files should be represented by metadata and hashes.",
            "",
        ]
    )


def render_experiment_routes(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Experiment Routes",
            "",
            "Status: template / placeholder.",
            "",
            "## Seed Route",
            "",
            f"- Route ID: `{request.project_id}-route-001`",
            "- Status: planned",
            "- Hard gates: define before execution.",
            "- Artifact requirements: define before execution.",
            "- Success claim: not allowed until evidence exists.",
            "",
            *_route_prompts(request.template_type),
            "",
        ]
    )


def render_related_work(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Related Work",
            "",
            "Status: template / placeholder.",
            "",
            "## Review Groups",
            "",
            *_related_work_prompts(request.template_type),
            "",
            "No real citation or final related-work claim is generated here.",
            "",
        ]
    )


def render_failure_taxonomy(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Failure Taxonomy",
            "",
            "Status: template / placeholder.",
            "",
            "## Initial Categories",
            "",
            *_failure_prompts(request.template_type),
            "",
            "Failure categories are planning placeholders until real evidence exists.",
            "",
        ]
    )


def render_advisor_pack(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Advisor Pack",
            "",
            "Status: template / placeholder.",
            "",
            "## Include",
            "",
            "- research north star;",
            "- current evidence state;",
            "- artifact readiness;",
            "- risks and blockers;",
            "- next actions;",
            "- limitations and missing evidence.",
            "",
            f"Project `{request.project_id}` has no advisor-approved result yet.",
            "",
        ]
    )


def render_master_ledger(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Master Ledger",
            "",
            f"## Bootstrap - {request.project_name}",
            "",
            "- Status: template generated.",
            f"- Template type: `{request.template_type}`.",
            "- No experiment has been executed.",
            "- No observed evidence has been added.",
            "- Human review required.",
            "",
        ]
    )


def render_contracts_readme(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Contracts",
            "",
            "Status: template / placeholder.",
            "",
            f"Contracts for `{request.project_id}` will live here.",
            "Start with schema drafts and keep generated outputs JSON-serializable.",
            "",
        ]
    )


def render_examples_readme(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Examples",
            "",
            "Status: template / placeholder.",
            "",
            f"Examples for `{request.project_id}` will live here.",
            "Use fake or manually reviewed fixtures until real evidence exists.",
            "",
        ]
    )


def render_feature_capsules_readme(request: ResearchProjectTemplateRequest) -> str:
    return "\n".join(
        [
            "# Feature Capsules",
            "",
            "Status: template / placeholder.",
            "",
            f"Feature capsules for `{request.project_id}` will live here.",
            "Each capsule should define problem, inputs, outputs, tests, risks,",
            "done criteria, and non-goals.",
            "",
        ]
    )


RESEARCH_TEMPLATE_RENDERERS: dict[str, ResearchTemplateRenderer] = {
    "README.md": render_readme,
    "docs/north_star.md": render_north_star,
    "docs/research_questions.md": render_research_questions,
    "docs/evidence_ledger.md": render_evidence_ledger,
    "docs/artifact_plan.md": render_artifact_plan,
    "docs/experiment_routes.md": render_experiment_routes,
    "docs/related_work.md": render_related_work,
    "docs/failure_taxonomy.md": render_failure_taxonomy,
    "docs/advisor_pack.md": render_advisor_pack,
    "lanes/00_master_ledger.md": render_master_ledger,
    "contracts/README.md": render_contracts_readme,
    "examples/README.md": render_examples_readme,
    "race/feature_capsules/README.md": render_feature_capsules_readme,
}


def _template_focus(template_type: ResearchProjectType) -> str:
    return {
        ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT: (
            "Plan evidence-backed experiment routes without inheriting VGGT claims."
        ),
        ResearchProjectType.PAPER_SURVEY_PROJECT: (
            "Build paper digest, method card, and related-work scaffolds."
        ),
        ResearchProjectType.EXPERIMENT_HEAVY_PROJECT: (
            "Track run artifacts, hard gates, and failure modes."
        ),
        ResearchProjectType.SOFTWARE_TOOLING_PROJECT: (
            "Organize package, CLI/MCP, docs, demo, and release evidence."
        ),
        ResearchProjectType.MIXED_RESEARCH_PROJECT: (
            "Balance paper review, artifacts, experiments, and advisor updates."
        ),
    }[template_type]


def _default_questions(template_type: ResearchProjectType) -> list[str]:
    return {
        ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT: [
            "What feature encoding should be tested?",
            "Which hard gates must pass before promotion?",
            "Which artifacts are required to support any success claim?",
        ],
        ResearchProjectType.PAPER_SURVEY_PROJECT: [
            "Which papers define the method landscape?",
            "Which claims require real paper review?",
            "What related-work positioning is safe?",
        ],
        ResearchProjectType.EXPERIMENT_HEAVY_PROJECT: [
            "Which route should run first?",
            "Which failures are expected?",
            "Which artifacts prove or block promotion?",
        ],
        ResearchProjectType.SOFTWARE_TOOLING_PROJECT: [
            "Which public interface is being stabilized?",
            "Which tests define release readiness?",
            "Which examples are safe for public demo?",
        ],
        ResearchProjectType.MIXED_RESEARCH_PROJECT: [
            "What is the research hypothesis?",
            "What evidence is missing?",
            "What should be shown to an advisor next?",
        ],
    }[template_type]


def _artifact_prompts(template_type: ResearchProjectType) -> list[str]:
    common = ["- manifest files", "- small summaries", "- sha256 inventories"]
    extra = {
        ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT: [
            "- route output summaries",
            "- visual board inventory",
        ],
        ResearchProjectType.PAPER_SURVEY_PROJECT: [
            "- paper digest notes",
            "- method card summaries",
        ],
        ResearchProjectType.EXPERIMENT_HEAVY_PROJECT: [
            "- run status reports",
            "- failure attribution reports",
        ],
        ResearchProjectType.SOFTWARE_TOOLING_PROJECT: [
            "- CLI/MCP smoke logs",
            "- package metadata checks",
        ],
        ResearchProjectType.MIXED_RESEARCH_PROJECT: [
            "- paper notes",
            "- experiment route summaries",
        ],
    }[template_type]
    return [*common, *extra]


def _route_prompts(template_type: ResearchProjectType) -> list[str]:
    if template_type == ResearchProjectType.PAPER_SURVEY_PROJECT:
        return ["## Reading Route", "", "- Status: planned", "- Output: digest and method card"]
    if template_type == ResearchProjectType.SOFTWARE_TOOLING_PROJECT:
        return ["## Tooling Route", "", "- Status: planned", "- Output: package smoke report"]
    return ["## Experiment Route Notes", "", "- Status: planned", "- Output: run ingest report"]


def _related_work_prompts(template_type: ResearchProjectType) -> list[str]:
    if template_type == ResearchProjectType.SOFTWARE_TOOLING_PROJECT:
        return ["- comparable tools", "- packaging patterns", "- interface conventions"]
    return [
        "- direct baselines",
        "- adjacent methods",
        "- datasets and benchmarks",
        "- unknown or requires review",
    ]


def _failure_prompts(template_type: ResearchProjectType) -> list[str]:
    if template_type == ResearchProjectType.PAPER_SURVEY_PROJECT:
        return [
            "- missing paper",
            "- incomplete reading",
            "- unsafe claim",
            "- citation uncertainty",
        ]
    if template_type == ResearchProjectType.SOFTWARE_TOOLING_PROJECT:
        return ["- package import failure", "- CLI mismatch", "- docs drift", "- demo unsafe"]
    return ["- missing artifact", "- hard gate failure", "- regression", "- not enough evidence"]

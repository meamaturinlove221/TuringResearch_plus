"""Registry of reusable research project templates."""

from __future__ import annotations

from turing_research_plus.project_template.research_types import (
    PROJECT_TYPE_DESCRIPTIONS,
    ResearchProjectType,
)
from turing_research_plus.project_template.schema import (
    ResearchProjectTemplate,
    ResearchTemplateSection,
)

REQUIRED_RESEARCH_TEMPLATE_SECTIONS: list[ResearchTemplateSection] = [
    ResearchTemplateSection(relative_path="README.md", title="README", role="project-readme"),
    ResearchTemplateSection(
        relative_path="docs/north_star.md",
        title="North Star",
        role="north-star",
    ),
    ResearchTemplateSection(
        relative_path="docs/research_questions.md",
        title="Research Questions",
        role="research-questions",
    ),
    ResearchTemplateSection(
        relative_path="docs/evidence_ledger.md",
        title="Evidence Ledger",
        role="evidence-ledger",
    ),
    ResearchTemplateSection(
        relative_path="docs/artifact_plan.md",
        title="Artifact Plan",
        role="artifact-plan",
    ),
    ResearchTemplateSection(
        relative_path="docs/experiment_routes.md",
        title="Experiment Routes",
        role="experiment-routes",
    ),
    ResearchTemplateSection(
        relative_path="docs/related_work.md",
        title="Related Work",
        role="related-work",
    ),
    ResearchTemplateSection(
        relative_path="docs/failure_taxonomy.md",
        title="Failure Taxonomy",
        role="failure-taxonomy",
    ),
    ResearchTemplateSection(
        relative_path="docs/advisor_pack.md",
        title="Advisor Pack",
        role="advisor-pack",
    ),
    ResearchTemplateSection(
        relative_path="lanes/00_master_ledger.md",
        title="Master Ledger",
        role="master-ledger",
    ),
    ResearchTemplateSection(
        relative_path="contracts/README.md",
        title="Contracts",
        role="contracts-readme",
    ),
    ResearchTemplateSection(
        relative_path="examples/README.md",
        title="Examples",
        role="examples-readme",
    ),
    ResearchTemplateSection(
        relative_path="race/feature_capsules/README.md",
        title="Feature Capsules",
        role="feature-capsules-readme",
    ),
]


def list_research_project_templates() -> list[ResearchProjectTemplate]:
    """Return all built-in research project templates."""

    return [get_research_project_template(template_type) for template_type in ResearchProjectType]


def get_research_project_template(template_type: ResearchProjectType) -> ResearchProjectTemplate:
    """Return one built-in research project template definition."""

    return ResearchProjectTemplate(
        template_id=template_type,
        display_name=_display_name(template_type),
        description=PROJECT_TYPE_DESCRIPTIONS[template_type],
        recommended_for=_recommended_for(template_type),
        sections=REQUIRED_RESEARCH_TEMPLATE_SECTIONS,
        safety_notes=[
            "Generated content is template / placeholder material.",
            "Generated templates contain no observed evidence.",
            "Do not add secrets, raw data, or private model files.",
            "Human review is required before public use.",
        ],
        requires_human_review=True,
    )


def _display_name(template_type: ResearchProjectType) -> str:
    return {
        ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT: "VGGT-like Experiment Project",
        ResearchProjectType.PAPER_SURVEY_PROJECT: "Paper Survey Project",
        ResearchProjectType.EXPERIMENT_HEAVY_PROJECT: "Experiment-heavy Project",
        ResearchProjectType.SOFTWARE_TOOLING_PROJECT: "Software Tooling Project",
        ResearchProjectType.MIXED_RESEARCH_PROJECT: "Mixed Research Project",
    }[template_type]


def _recommended_for(template_type: ResearchProjectType) -> list[str]:
    return {
        ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT: [
            "geometry experiments",
            "artifact-heavy research",
            "route and hard-gate planning",
        ],
        ResearchProjectType.PAPER_SURVEY_PROJECT: [
            "literature surveys",
            "paper digest workflows",
            "related-work positioning",
        ],
        ResearchProjectType.EXPERIMENT_HEAVY_PROJECT: [
            "repeatable experiments",
            "remote artifact review",
            "failure taxonomy tracking",
        ],
        ResearchProjectType.SOFTWARE_TOOLING_PROJECT: [
            "research tools",
            "MCP or CLI package work",
            "public demo suites",
        ],
        ResearchProjectType.MIXED_RESEARCH_PROJECT: [
            "early-stage research",
            "combined paper and experiment workflows",
            "general project bootstrap",
        ],
    }[template_type]

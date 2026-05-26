"""Local helper wrappers for project template generation."""

from __future__ import annotations

from turing_research_plus.project_template.generator import (
    generate_project_template,
    generate_research_project_template,
    summarize_project_template,
    summarize_research_project_template,
)
from turing_research_plus.project_template.models import (
    ProjectTemplateRequest,
    ProjectTemplateResult,
)
from turing_research_plus.project_template.schema import (
    ResearchProjectTemplateManifest,
    ResearchProjectTemplateRequest,
)


def project_template_generate(request: ProjectTemplateRequest) -> ProjectTemplateResult:
    """Generate a local research project template."""

    return generate_project_template(request)


def project_template_summary(result: ProjectTemplateResult) -> str:
    """Render a project template generation summary."""

    return summarize_project_template(result)


def research_project_template_generate(
    request: ResearchProjectTemplateRequest,
) -> ResearchProjectTemplateManifest:
    """Generate a typed reusable research project template."""

    return generate_research_project_template(request)


def research_project_template_summary(result: ResearchProjectTemplateManifest) -> str:
    """Render a typed research project template generation summary."""

    return summarize_research_project_template(result)

"""Race Mode Feature Capsule Factory."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.race.models import FeatureCapsule, IdeaCard, SourceHygieneStatus
from turing_research_plus.race.priority_elevator import RacePriority, priority_score


class FeatureCapsuleRequest(BaseModel):
    """Request to create a feature capsule skeleton."""

    model_config = ConfigDict(extra="forbid")

    idea: IdeaCard
    feature_name: str | None = None
    domain: str = Field(default="race", min_length=1)
    strategic_fit: float = Field(default=0.7, ge=0.0, le=1.0)
    workspace_root: Path = Path(".")
    write_files: bool = True


class FeatureCapsuleCreateResult(BaseModel):
    """Created feature capsule skeleton."""

    model_config = ConfigDict(extra="forbid")

    feature_name: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    capsule: FeatureCapsule
    files: list[Path] = Field(min_length=1)
    skipped_reason: str | None = None

    @model_validator(mode="after")
    def require_files_for_created_capsule(self) -> FeatureCapsuleCreateResult:
        if self.skipped_reason is None and not self.files:
            raise ValueError("created feature capsule requires file paths")
        return self


def create_feature_capsule(request: FeatureCapsuleRequest) -> FeatureCapsuleCreateResult:
    """Create a minimal self-contained feature capsule skeleton."""

    recommendation = priority_score(request.idea, strategic_fit=request.strategic_fit)
    feature_name = _feature_name(request.feature_name or request.idea.title)
    capsule = FeatureCapsule(
        feature_id=f"feature-{feature_name}",
        title=request.idea.title,
        idea_cards=[request.idea.idea_id],
        evidence=request.idea.evidence_refs,
        hygiene_gate=request.idea.hygiene_gate,
    )
    if request.idea.hygiene_gate.status != SourceHygieneStatus.PASSED:
        return FeatureCapsuleCreateResult(
            feature_name=feature_name,
            domain=request.domain,
            capsule=capsule,
            files=_planned_paths(request.workspace_root, request.domain, feature_name),
            skipped_reason="source hygiene did not pass",
        )
    if recommendation.priority not in {RacePriority.P0, RacePriority.P1}:
        return FeatureCapsuleCreateResult(
            feature_name=feature_name,
            domain=request.domain,
            capsule=capsule,
            files=_planned_paths(request.workspace_root, request.domain, feature_name),
            skipped_reason="idea is not P0/P1",
        )

    files = _planned_paths(request.workspace_root, request.domain, feature_name)
    if request.write_files:
        _write_capsule_files(request.workspace_root, request.domain, feature_name, request.idea)
    return FeatureCapsuleCreateResult(
        feature_name=feature_name,
        domain=request.domain,
        capsule=capsule,
        files=files,
    )


def race_feature_capsule_create(request: FeatureCapsuleRequest) -> dict[str, object]:
    """Thin race.feature_capsule_create wrapper."""

    return create_feature_capsule(request).model_dump(mode="json")


def _planned_paths(root: Path, domain: str, feature_name: str) -> list[Path]:
    capsule_dir = root / "race" / "feature_capsules" / feature_name
    return [
        capsule_dir / "FEATURE.md",
        capsule_dir / "contract.yaml",
        capsule_dir / "SKILL.md",
        root / "src" / "turing_research_plus" / domain / f"{feature_name}.py",
        root / "tests" / "unit" / f"test_{feature_name}.py",
        root / "docs" / "features" / f"{feature_name}.md",
        root / "sop_graphs" / "feature_graphs" / f"{feature_name}.mmd",
    ]


def _write_capsule_files(root: Path, domain: str, feature_name: str, idea: IdeaCard) -> None:
    for path in _planned_paths(root, domain, feature_name):
        path.parent.mkdir(parents=True, exist_ok=True)
    files = {
        root / "race" / "feature_capsules" / feature_name / "FEATURE.md": _feature_md(
            feature_name,
            idea,
        ),
        root / "race" / "feature_capsules" / feature_name / "contract.yaml": _contract_yaml(
            feature_name,
            idea,
        ),
        root / "race" / "feature_capsules" / feature_name / "SKILL.md": _skill_md(
            feature_name,
            idea,
        ),
        root / "src" / "turing_research_plus" / domain / f"{feature_name}.py": _module_py(
            feature_name,
        ),
        root / "tests" / "unit" / f"test_{feature_name}.py": _test_py(feature_name, domain),
        root / "docs" / "features" / f"{feature_name}.md": _docs_md(feature_name, idea),
        root / "sop_graphs" / "feature_graphs" / f"{feature_name}.mmd": _sop_graph(
            feature_name,
        ),
    }
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")


def _feature_md(feature_name: str, idea: IdeaCard) -> str:
    return f"""# TuringResearch Plus Feature Capsule: {feature_name}

## Problem
{idea.normalized_summary}

## User story
As a TuringResearch Plus maintainer, I need a reviewed feature skeleton before implementation.

## Input
- Source IdeaCard: `{idea.idea_id}`

## Output
- Minimal feature module, contract, docs, tests, and SOP graph.

## Data model
- Pending contract review.

## Public tools
- Pending contract review.

## Internal service
- Pending implementation.

## Risks
- Scope creep beyond the source IdeaCard.

## Tests
- `tests/unit/test_{feature_name}.py`

## Done criteria
- Contract reviewed.
- Unit test placeholder passes.
- SOP graph present.
"""


def _contract_yaml(feature_name: str, idea: IdeaCard) -> str:
    return f"""feature_name: {feature_name}
project: TuringResearch Plus
source_idea_card: {idea.idea_id}
implementation_status: skeleton
tools: []
tests:
  - tests/unit/test_{feature_name}.py
"""


def _skill_md(feature_name: str, idea: IdeaCard) -> str:
    return f"""---
name: turingresearch-{feature_name}
description: Use when reviewing the {feature_name} feature capsule.
---

# TuringResearch Plus Feature Capsule Skill

Source IdeaCard: `{idea.idea_id}`

Keep this capsule in skeleton mode until contracts are approved.
"""


def _module_py(feature_name: str) -> str:
    return f'''"""Skeleton feature module for {feature_name}."""


def feature_status() -> str:
    """Return skeleton feature status."""

    return "skeleton"
'''


def _test_py(feature_name: str, domain: str) -> str:
    return f'''from turing_research_plus.{domain}.{feature_name} import feature_status


def test_{feature_name}_feature_status() -> None:
    assert feature_status() == "skeleton"
'''


def _docs_md(feature_name: str, idea: IdeaCard) -> str:
    return f"""# TuringResearch Plus Feature: {feature_name}

Source IdeaCard: `{idea.idea_id}`

This is a generated feature capsule skeleton. Business implementation is intentionally absent.
"""


def _sop_graph(feature_name: str) -> str:
    return f"""flowchart TD
    A[Source IdeaCard] --> B[Feature Capsule: {feature_name}]
    B --> C[Contract Review]
    C --> D[Implementation Round]
    C --> E[Tests]
"""


def _feature_name(value: str) -> str:
    lowered = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
    return slug or "feature_capsule"

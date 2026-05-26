from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.case_study.gallery import (
    CaseGalleryItem,
    load_case_gallery_manifest,
    render_case_gallery_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "examples" / "public_demo" / "case_gallery" / "gallery_manifest.yaml"


def test_case_gallery_manifest_loads_public_demo_cases() -> None:
    manifest = load_case_gallery_manifest(MANIFEST)

    assert manifest.gallery_id == "public_demo_case_gallery"
    assert manifest.status == "demo-only"
    assert manifest.published is False
    assert len(manifest.cases) == 5
    assert {item.case_id for item in manifest.cases} >= {
        "vggt_public_safe_case",
        "robotics_paper_survey_demo",
        "medical_imaging_experiment_demo",
        "software_tooling_research_demo",
        "multimodal_model_eval_demo",
    }


def test_case_gallery_item_rejects_external_fake_urls() -> None:
    with pytest.raises(ValueError):
        CaseGalleryItem(
            case_id="bad",
            title="Bad",
            domain="bad",
            research_type="bad",
            demo_status="demo-only",
            privacy_level="public-demo",
            dashboard_link="https://github.com/example/not-real",
            advisor_pack_link="advisor.md",
        )


def test_case_gallery_markdown_renders_required_fields() -> None:
    manifest = load_case_gallery_manifest(MANIFEST)
    markdown = render_case_gallery_markdown(manifest)

    assert "Case Study Gallery" in markdown
    assert "`vggt_public_safe_case`" in markdown
    assert "robotics_paper_survey_demo" in markdown
    assert "Available artifacts" in markdown
    assert "Dashboard" in markdown
    assert "Advisor pack" in markdown
    assert "Demo outputs are not observed research evidence." in markdown

from __future__ import annotations

from pathlib import Path

from turing_research_plus.skill_market.catalog import (
    build_skill_marketplace_index,
    review_skill_marketplace,
)

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / ".agents" / "skills"


def test_skill_catalog_matches_agents_skills() -> None:
    index = build_skill_marketplace_index(SKILLS_ROOT)
    skill_dirs = sorted(path.name for path in SKILLS_ROOT.iterdir() if path.is_dir())
    indexed = sorted(entry.skill_name for entry in index.entries)

    assert indexed == skill_dirs
    assert len(index.entries) == 30


def test_skill_catalog_entries_have_required_review_metadata() -> None:
    index = build_skill_marketplace_index(SKILLS_ROOT)

    assert all(entry.skill_name.startswith("turingresearch-") for entry in index.entries)
    assert all(entry.status for entry in index.entries)
    assert all(entry.docs for entry in index.entries)
    assert all(entry.tests for entry in index.entries)
    assert all(entry.related_contracts for entry in index.entries)


def test_skill_marketplace_review_report_is_valid_for_repo_skills() -> None:
    index = build_skill_marketplace_index(SKILLS_ROOT)
    report = review_skill_marketplace(index, SKILLS_ROOT)

    assert report.valid is True
    assert report.checked_skills == len(index.entries)
    assert report.missing_skills == []
    assert report.invalid_names == []
    assert report.missing_metadata == []
    assert report.remote_publish is False

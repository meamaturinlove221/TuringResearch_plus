from __future__ import annotations

from pathlib import Path

from turing_research_plus.skills.registry import load_skill_registry, skill_names

ROOT = Path(__file__).resolve().parents[2]


def test_load_skill_registry_reads_local_skills() -> None:
    entries = load_skill_registry(ROOT / ".agents" / "skills")
    names = {entry.skill_name for entry in entries}

    assert "turingresearch-master-orchestrator" in names
    assert "turingresearch-race-feature-capsule-factory" in names
    assert all(entry.path.as_posix().startswith(".agents/skills/") for entry in entries)


def test_skill_names_matches_skill_directories() -> None:
    names = skill_names(ROOT / ".agents" / "skills")
    dirs = {path.name for path in (ROOT / ".agents" / "skills").iterdir() if path.is_dir()}

    assert names == dirs

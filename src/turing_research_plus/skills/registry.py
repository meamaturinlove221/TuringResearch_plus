"""Load skill registry entries from local SKILL.md files."""

from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.skills.models import SkillRegistryEntry, SkillStatus

ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = ROOT / ".agents" / "skills"


def load_skill_registry(skills_root: Path = SKILLS_ROOT) -> list[SkillRegistryEntry]:
    """Load all local skill entries from `.agents/skills`."""

    entries: list[SkillRegistryEntry] = []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = skill_file.read_text(encoding="utf-8")
        entries.append(
            SkillRegistryEntry(
                skill_name=_frontmatter_name(text) or skill_dir.name,
                path=skill_file.relative_to(ROOT),
                role=_section(text, "Role"),
                when_to_use=_section_items(text, "When to use"),
                inputs=_section_items(text, "Inputs"),
                outputs=_section_items(text, "Outputs"),
                related_contracts=_section_items(text, "Related contracts"),
                related_lanes=_section_items(text, "Related lanes"),
                related_modules=_section_items(text, "Required files"),
                status=_status_from_text(text),
                release_target=_release_target_from_text(text),
            )
        )
    return entries


def skill_names(skills_root: Path = SKILLS_ROOT) -> set[str]:
    """Return all skill names."""

    return {entry.skill_name for entry in load_skill_registry(skills_root)}


def _frontmatter_name(text: str) -> str | None:
    match = re.search(r"^name:\s*(turingresearch-[a-z0-9-]+)\s*$", text, re.MULTILINE)
    return match.group(1) if match else None


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        return "Not specified."
    body = match.group("body").strip()
    return body or "Not specified."


def _section_items(text: str, heading: str) -> list[str]:
    body = _section(text, heading)
    items = [
        line.strip()[2:].strip()
        for line in body.splitlines()
        if line.strip().startswith("- ")
    ]
    return items or ([body] if body != "Not specified." else [])


def _status_from_text(text: str) -> SkillStatus:
    match = re.search(r"Implementation status:\s*`?([a-z-]+)`?", text)
    if match:
        value = match.group(1).replace("-", "_")
        if value in SkillStatus:
            return SkillStatus(value)
    if "Implementation status: `locked`" in text or "Implementation status: locked" in text:
        return SkillStatus.LOCKED
    if "locked" in text.lower():
        return SkillStatus.LOCKED
    return SkillStatus.USABLE


def _release_target_from_text(text: str) -> str:
    match = re.search(r"Release requirement:\s*`?([^`\n]+)`?", text)
    if match:
        return match.group(1).strip()
    return "current"

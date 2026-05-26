"""Markdown export for the local skill marketplace."""

from __future__ import annotations

from collections import defaultdict

from turing_research_plus.skill_market.models import SkillMarketplaceIndex


def render_skill_marketplace_markdown(index: SkillMarketplaceIndex) -> str:
    """Render the local marketplace index as Markdown."""

    lines = [
        f"# Skill Marketplace: {index.marketplace_id}",
        "",
        f"- Skills: `{len(index.entries)}`",
        f"- Categories: `{len(index.categories)}`",
        f"- Local only: `{str(index.local_only).lower()}`",
        f"- Remote publish: `{str(index.remote_publish).lower()}`",
        f"- Requires human review: `{str(index.requires_human_review).lower()}`",
        "",
        "| Skill | Category | Status | Docs | Tests |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in sorted(index.entries, key=lambda item: item.skill_name):
        docs = "<br>".join(f"`{item}`" for item in entry.docs)
        tests = "<br>".join(f"`{item}`" for item in entry.tests)
        lines.append(
            f"| `{entry.skill_name}` | `{entry.category}` | `{entry.status}` | {docs} | {tests} |"
        )

    lines.extend(["", "## Categories", ""])
    by_category: dict[str, list[str]] = defaultdict(list)
    for entry in index.entries:
        by_category[entry.category.value].append(entry.skill_name)
    for category in sorted(by_category):
        skills = ", ".join(f"`{skill}`" for skill in sorted(by_category[category]))
        lines.append(f"- `{category}`: {skills}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This marketplace is local documentation only.",
            "- It does not upload, install, or execute skills.",
            "- Feature Capsule `SKILL.md` files are related planning material, "
            "not automatically published marketplace entries.",
            "",
        ]
    )
    return "\n".join(lines)

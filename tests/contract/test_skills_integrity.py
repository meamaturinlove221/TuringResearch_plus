from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / ".agents" / "skills"
SKILLS_INDEX = ROOT / "docs" / "skills-index.md"

REQUIRED_SKILLS = [
    "tulingresearch-master-orchestrator",
    "tulingresearch-architecture-contracts",
    "tulingresearch-cache-and-ledger",
    "tulingresearch-qa-release",
    "tulingresearch-core-reproduction",
    "tulingresearch-pdf-markdown-core",
    "tulingresearch-yogsoth-module-audit",
    "tulingresearch-fusion-campaign-engine",
    "tulingresearch-fusion-semantic-graph",
    "tulingresearch-fusion-literature-survey",
    "tulingresearch-fusion-north-star",
    "tulingresearch-fusion-deep-insight",
    "tulingresearch-fusion-hypothesis-formation",
    "tulingresearch-fusion-creative-ideation",
    "tulingresearch-fusion-convergence",
    "tulingresearch-fusion-stress-test",
    "tulingresearch-fusion-experiment-execution",
    "tulingresearch-fusion-wiki-vault",
    "tulingresearch-fusion-context-management",
    "tulingresearch-fusion-subtask-runtime",
    "tulingresearch-race-source-hygiene",
    "tulingresearch-race-idea-radar",
    "tulingresearch-race-priority-elevator",
    "tulingresearch-race-feature-capsule-factory",
    "tulingresearch-race-architecture-box-builder",
    "tulingresearch-race-upstream-watch",
    "tulingresearch-paper-docflow-article-blocks",
    "tulingresearch-paper-sop-graph-generator",
    "tulingresearch-paper-figure-asset-pipeline",
    "tulingresearch-paper-writing-pipeline",
]

REQUIRED_SECTIONS = [
    "## Role",
    "## When to use",
    "## Inputs",
    "## Outputs",
    "## Required files",
    "## Related contracts",
    "## Related lanes",
    "## Required tests",
    "## Rules / constraints",
    "## Done criteria",
]

FORBIDDEN_PARTS = [
    ("neo", "cortica-plus"),
    ("neo", "cortica_plus"),
    ("src/neo", "cortica_plus"),
    ("Neo", "cortica++"),
    ("neo", "cortica-"),
]

CORE_SKILLS = {
    "tulingresearch-master-orchestrator",
    "tulingresearch-architecture-contracts",
    "tulingresearch-cache-and-ledger",
    "tulingresearch-core-reproduction",
    "tulingresearch-pdf-markdown-core",
    "tulingresearch-qa-release",
}

RELEASE_CRITICAL_PREFIXES = (
    "tulingresearch-race-",
    "tulingresearch-paper-",
)


def skill_dirs() -> list[str]:
    return sorted(path.name for path in SKILLS_ROOT.iterdir() if path.is_dir())


def skill_text(skill_name: str) -> str:
    return (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")


def test_all_required_skill_folders_exist_and_no_unlocked_extra_dirs() -> None:
    actual = skill_dirs()

    assert actual == sorted(REQUIRED_SKILLS)


def test_each_skill_has_skill_md_frontmatter_and_matching_name() -> None:
    for skill_name in REQUIRED_SKILLS:
        skill_file = SKILLS_ROOT / skill_name / "SKILL.md"
        assert skill_file.exists()
        content = skill_file.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert f"name: {skill_name}\n" in content
        assert "description: " in content.split("---", maxsplit=2)[1]
        for section in REQUIRED_SECTIONS:
            assert section in content


def test_skills_do_not_use_forbidden_naming() -> None:
    for skill_name in REQUIRED_SKILLS:
        content = skill_text(skill_name)
        for left, right in FORBIDDEN_PARTS:
            assert left + right not in content
            assert left + right not in skill_name


def test_skills_index_matches_actual_folders() -> None:
    content = SKILLS_INDEX.read_text(encoding="utf-8")
    indexed = []
    for line in content.splitlines():
        if line.startswith("| `tulingresearch-"):
            indexed.append(line.split("`", maxsplit=2)[1])

    assert sorted(indexed) == sorted(REQUIRED_SKILLS)
    assert sorted(indexed) == skill_dirs()


def test_core_skill_status_at_least_usable() -> None:
    content = SKILLS_INDEX.read_text(encoding="utf-8")
    allowed = {"usable", "locked"}

    for skill_name in CORE_SKILLS:
        line = next(line for line in content.splitlines() if f"`{skill_name}`" in line)
        status = line.split("|")[3].strip()
        assert status in allowed


def test_release_critical_skills_locked_or_blocker_marked() -> None:
    content = SKILLS_INDEX.read_text(encoding="utf-8")

    for skill_name in REQUIRED_SKILLS:
        if skill_name in CORE_SKILLS or skill_name.startswith(RELEASE_CRITICAL_PREFIXES):
            line = next(line for line in content.splitlines() if f"`{skill_name}`" in line)
            status = line.split("|")[3].strip()
            notes = line.split("|")[-2].strip()
            assert status == "locked" or "blocker" in notes.lower()

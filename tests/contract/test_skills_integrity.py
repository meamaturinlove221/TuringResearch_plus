from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / ".agents" / "skills"
SKILLS_INDEX = ROOT / "docs" / "skills-index.md"

REQUIRED_SKILLS = [
    "turingresearch-master-orchestrator",
    "turingresearch-architecture-contracts",
    "turingresearch-cache-and-ledger",
    "turingresearch-qa-release",
    "turingresearch-core-reproduction",
    "turingresearch-pdf-markdown-core",
    "turingresearch-yogsoth-module-audit",
    "turingresearch-fusion-campaign-engine",
    "turingresearch-fusion-semantic-graph",
    "turingresearch-fusion-literature-survey",
    "turingresearch-fusion-north-star",
    "turingresearch-fusion-deep-insight",
    "turingresearch-fusion-hypothesis-formation",
    "turingresearch-fusion-creative-ideation",
    "turingresearch-fusion-convergence",
    "turingresearch-fusion-stress-test",
    "turingresearch-fusion-experiment-execution",
    "turingresearch-fusion-wiki-vault",
    "turingresearch-fusion-context-management",
    "turingresearch-fusion-subtask-runtime",
    "turingresearch-race-source-hygiene",
    "turingresearch-race-idea-radar",
    "turingresearch-race-priority-elevator",
    "turingresearch-race-feature-capsule-factory",
    "turingresearch-race-architecture-box-builder",
    "turingresearch-race-upstream-watch",
    "turingresearch-paper-docflow-article-blocks",
    "turingresearch-paper-sop-graph-generator",
    "turingresearch-paper-figure-asset-pipeline",
    "turingresearch-paper-writing-pipeline",
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
    "turingresearch-master-orchestrator",
    "turingresearch-architecture-contracts",
    "turingresearch-cache-and-ledger",
    "turingresearch-core-reproduction",
    "turingresearch-pdf-markdown-core",
    "turingresearch-qa-release",
}

RELEASE_CRITICAL_PREFIXES = (
    "turingresearch-race-",
    "turingresearch-paper-",
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
        if line.startswith("| `turingresearch-"):
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

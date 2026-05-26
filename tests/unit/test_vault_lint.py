from turing_research_plus.vault.lint import lint_vault
from turing_research_plus.vault.models import VaultEntityType, VaultPage
from turing_research_plus.vault.service import VaultService


def test_orphan_detection(tmp_path) -> None:
    service = VaultService(tmp_path)
    service.compile_page(
        VaultPage(page_id="orphan", title="Orphan", entity_type=VaultEntityType.TOPIC)
    )

    issues = service.lint()

    assert any(issue.issue_type == "orphan_page" and issue.page_id == "orphan" for issue in issues)


def test_lint_missing_frontmatter(tmp_path) -> None:
    (tmp_path / "bad.md").write_text("No frontmatter here", encoding="utf-8")

    issues = lint_vault(tmp_path)

    assert any(issue.issue_type == "missing_frontmatter" for issue in issues)

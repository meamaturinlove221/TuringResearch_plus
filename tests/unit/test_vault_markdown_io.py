from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.vault.markdown_io import read_page, write_page
from tuling_research_plus.vault.models import VaultEntityType, VaultPage


def test_create_page_round_trip(tmp_path) -> None:
    page = VaultPage(
        page_id="source-1",
        title="Source One",
        entity_type=VaultEntityType.SOURCE,
        body="This source discusses semantic graph memory.",
        evidence=[EvidenceRef(source_id="source-1", locator="body", quote="semantic graph memory")],
    )

    path = write_page(tmp_path, page)
    loaded = read_page(path)

    assert path.exists()
    assert loaded.page_id == "source-1"
    assert loaded.body == "This source discusses semantic graph memory."
    assert loaded.evidence[0].quote == "semantic graph memory"

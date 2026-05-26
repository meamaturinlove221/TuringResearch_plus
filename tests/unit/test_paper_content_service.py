from turing_research.cache.keys import build_cache_key
from turing_research.cache.manager import CacheManager
from turing_research.errors import ErrorCode
from turing_research.scholar.content_service import PaperContentService
from turing_research.scholar.models import PaperContentRequest


def test_paper_content_local_hit(tmp_path) -> None:
    paper_id = "paper-1"
    cache = CacheManager(tmp_path / "paper_content")
    cache.put(
        build_cache_key("core.paper_content", paper_id),
        {"markdown": "# Cached Paper"},
        {"source": "unit-test"},
    )

    result = PaperContentService(tmp_path).get_content(PaperContentRequest(paper_id=paper_id))

    assert result.found is True
    assert result.markdown == "# Cached Paper"
    assert result.metadata == {"source": "unit-test"}


def test_paper_content_local_miss(tmp_path) -> None:
    result = PaperContentService(tmp_path).get_content(
        PaperContentRequest(paper_id="missing-paper")
    )

    assert result.found is False
    assert result.markdown is None
    assert result.error is not None
    assert result.error.code == ErrorCode.CACHE_MISS

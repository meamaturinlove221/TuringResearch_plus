from tuling_research.cache.keys import build_cache_key
from tuling_research.cache.manager import CacheManager
from tuling_research.errors import ErrorCode
from tuling_research.web.content_service import WebContentService
from tuling_research.web.models import WebContentRequest


def test_web_content_local_hit(tmp_path) -> None:
    url = "https://example.com/article"
    cache = CacheManager(tmp_path / "web_content")
    cache.put(
        build_cache_key("core.web_content", url),
        {"markdown": "# Cached Web Page"},
        {"source": "unit-test"},
    )

    result = WebContentService(tmp_path).get_content(WebContentRequest(url=url))

    assert result.found is True
    assert result.markdown == "# Cached Web Page"
    assert result.metadata == {"source": "unit-test"}


def test_web_content_local_miss(tmp_path) -> None:
    result = WebContentService(tmp_path).get_content(
        WebContentRequest(url="https://example.com/missing")
    )

    assert result.found is False
    assert result.markdown is None
    assert result.error is not None
    assert result.error.code == ErrorCode.CACHE_MISS

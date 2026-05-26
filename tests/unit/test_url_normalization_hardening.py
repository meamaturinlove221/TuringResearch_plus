from __future__ import annotations

import pytest

from turing_research_plus.web_tools import (
    UrlNormalizationRequest,
    normalize_url,
    normalize_url_string,
    url_cache_key,
)


def test_normalize_url_lowercases_scheme_host_and_strips_fragment_tracking() -> None:
    result = normalize_url(
        "HTTPS://Example.COM:443//Paper/?utm_source=news&b=2&a=1#section"
    )

    assert result.normalized_url == "https://example.com/Paper?a=1&b=2"
    assert result.scheme == "https"
    assert result.host == "example.com"
    assert result.path == "/Paper"
    assert result.query == "a=1&b=2"
    assert result.fragment_removed is True
    assert result.tracking_params_removed == ["utm_source"]
    assert result.default_port_removed is True
    assert len(result.cache_key) == 64
    assert result.web_meta["normUrl"] == result.normalized_url


def test_normalize_url_keeps_non_default_port_and_path_encoding() -> None:
    result = normalize_url("http://Example.com:8080/a folder/index.html?z=9")

    assert result.normalized_url == "http://example.com:8080/a%20folder/index.html?z=9"
    assert result.default_port_removed is False


def test_normalize_url_blocks_non_http_schemes() -> None:
    with pytest.raises(ValueError, match="http and https"):
        normalize_url("file:///tmp/secret.txt")
    with pytest.raises(ValueError, match="http and https"):
        normalize_url("javascript:alert(1)")


def test_normalize_url_requires_host_and_human_review() -> None:
    with pytest.raises(ValueError, match="requires a host"):
        normalize_url("https:///missing-host")
    with pytest.raises(ValueError, match="requires human review"):
        normalize_url(
            UrlNormalizationRequest(
                url="https://example.com",
                requires_human_review=False,
            )
        )


def test_normalize_url_string_and_cache_key_are_stable() -> None:
    one = "https://example.com/path?b=2&a=1&utm_campaign=x#frag"
    two = "HTTPS://EXAMPLE.COM:443/path?a=1&b=2"

    assert normalize_url_string(one) == normalize_url_string(two)
    assert url_cache_key(one) == url_cache_key(two)

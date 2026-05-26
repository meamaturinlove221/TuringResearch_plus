"""URL normalization helpers for Web tool surfaces."""

from __future__ import annotations

from hashlib import sha256
from typing import Self
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit

from pydantic import BaseModel, ConfigDict, Field, model_validator

TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "igshid",
}
ALLOWED_SCHEMES = {"http", "https"}


class NormalizedUrl(BaseModel):
    """Normalized URL metadata for cache and source tracking."""

    model_config = ConfigDict(extra="forbid")

    original_url: str = Field(min_length=1)
    normalized_url: str = Field(min_length=1)
    scheme: str = Field(min_length=1)
    host: str = Field(min_length=1)
    path: str = Field(min_length=1)
    query: str = ""
    fragment_removed: bool = False
    tracking_params_removed: list[str] = Field(default_factory=list)
    default_port_removed: bool = False
    cache_key: str = Field(min_length=64, max_length=64)
    requires_human_review: bool = True

    @property
    def web_meta(self) -> dict[str, str | bool | list[str]]:
        """Return WebMeta-style metadata for docs/tests."""

        return {
            "original_url": self.original_url,
            "normUrl": self.normalized_url,
            "scheme": self.scheme,
            "host": self.host,
            "path": self.path,
            "query": self.query,
            "fragment_removed": self.fragment_removed,
            "tracking_params_removed": self.tracking_params_removed,
            "default_port_removed": self.default_port_removed,
            "requires_human_review": self.requires_human_review,
        }


class UrlNormalizationRequest(BaseModel):
    """Request for URL normalization."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1)
    strip_fragment: bool = True
    strip_tracking_params: bool = True
    sort_query: bool = True
    require_http: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_review_boundary(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("URL normalization requires human review")
        return self


def normalize_url(
    url: str | UrlNormalizationRequest,
) -> NormalizedUrl:
    """Normalize a public HTTP(S) URL without fetching it."""

    request = url if isinstance(url, UrlNormalizationRequest) else UrlNormalizationRequest(url=url)
    raw = request.url.strip()
    parts = urlsplit(raw)
    scheme = parts.scheme.lower()
    if request.require_http and scheme not in ALLOWED_SCHEMES:
        raise ValueError("URL normalization only allows http and https URLs")

    host = (parts.hostname or "").lower().rstrip(".")
    if not host:
        raise ValueError("URL normalization requires a host")

    default_port_removed = False
    port = parts.port
    if port is not None and not _is_default_port(scheme, port):
        netloc = f"{host}:{port}"
    else:
        netloc = host
        default_port_removed = port is not None

    path = _normalize_path(parts.path)
    query, removed = _normalize_query(
        parts.query,
        strip_tracking_params=request.strip_tracking_params,
        sort_query=request.sort_query,
    )
    fragment = "" if request.strip_fragment else parts.fragment
    normalized = urlunsplit((scheme, netloc, path, query, fragment))
    return NormalizedUrl(
        original_url=raw,
        normalized_url=normalized,
        scheme=scheme,
        host=host,
        path=path,
        query=query,
        fragment_removed=bool(parts.fragment and request.strip_fragment),
        tracking_params_removed=removed,
        default_port_removed=default_port_removed,
        cache_key=sha256(normalized.encode("utf-8")).hexdigest(),
        requires_human_review=request.requires_human_review,
    )


def normalize_url_string(url: str) -> str:
    """Return only the normalized URL string."""

    return normalize_url(url).normalized_url


def url_cache_key(url: str) -> str:
    """Return a stable cache key for a normalized URL."""

    return normalize_url(url).cache_key


def _is_default_port(scheme: str, port: int) -> bool:
    return (scheme == "http" and port == 80) or (scheme == "https" and port == 443)


def _normalize_path(path: str) -> str:
    if not path:
        return "/"
    decoded = unquote(path)
    while "//" in decoded:
        decoded = decoded.replace("//", "/")
    if not decoded.startswith("/"):
        decoded = f"/{decoded}"
    if decoded != "/" and decoded.endswith("/"):
        decoded = decoded.rstrip("/")
    return quote(decoded, safe="/-._~")


def _normalize_query(
    query: str,
    *,
    strip_tracking_params: bool,
    sort_query: bool,
) -> tuple[str, list[str]]:
    pairs = parse_qsl(query, keep_blank_values=True)
    removed: list[str] = []
    kept: list[tuple[str, str]] = []
    for key, value in pairs:
        lowered = key.lower()
        is_tracking = lowered in TRACKING_QUERY_KEYS or any(
            lowered.startswith(prefix) for prefix in TRACKING_QUERY_PREFIXES
        )
        if strip_tracking_params and is_tracking:
            removed.append(key)
            continue
        kept.append((key, value))
    if sort_query:
        kept = sorted(kept, key=lambda item: (item[0].lower(), item[1]))
    return urlencode(kept, doseq=True), removed

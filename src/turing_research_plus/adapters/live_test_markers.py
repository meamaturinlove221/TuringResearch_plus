"""Helpers for explicitly gated live adapter tests."""

from __future__ import annotations

import os
from importlib.util import find_spec

LIVE_TEST_ENV = "TURINGRESEARCH_ENABLE_LIVE_TESTS"
SEMANTIC_SCHOLAR_API_KEY_ENV = "SEMANTIC_SCHOLAR_API_KEY"
APIFY_TOKEN_ENV = "APIFY_TOKEN"


def live_tests_enabled() -> bool:
    """Return whether live tests were explicitly enabled."""

    return os.getenv(LIVE_TEST_ENV) == "1"


def semantic_scholar_api_key_present() -> bool:
    """Return whether a Semantic Scholar API key is configured."""

    return bool(os.getenv(SEMANTIC_SCHOLAR_API_KEY_ENV))


def semantic_scholar_live_skip_reason() -> str | None:
    """Return a skip reason for live Semantic Scholar tests, or None if runnable."""

    if not live_tests_enabled():
        return f"{LIVE_TEST_ENV}=1 is required for live tests"
    if find_spec("httpx") is None:
        return "httpx is required for live Semantic Scholar tests"
    if not semantic_scholar_api_key_present():
        return f"{SEMANTIC_SCHOLAR_API_KEY_ENV} is required for live Semantic Scholar tests"
    return None


def apify_token_present() -> bool:
    """Return whether an Apify token is configured."""

    return bool(os.getenv(APIFY_TOKEN_ENV))


def web_fetch_live_skip_reason() -> str | None:
    """Return a skip reason for live Web Fetch tests, or None if runnable."""

    if not live_tests_enabled():
        return f"{LIVE_TEST_ENV}=1 is required for live tests"
    if find_spec("httpx") is None:
        return "httpx is required for live Web Fetch tests"
    return None


def apify_live_skip_reason() -> str | None:
    """Return a skip reason for live Apify tests, or None if runnable."""

    if not live_tests_enabled():
        return f"{LIVE_TEST_ENV}=1 is required for live tests"
    if find_spec("httpx") is None:
        return "httpx is required for live Apify tests"
    if not apify_token_present():
        return f"{APIFY_TOKEN_ENV} is required for live Apify tests"
    return None

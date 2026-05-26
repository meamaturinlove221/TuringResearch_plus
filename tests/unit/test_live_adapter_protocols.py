from __future__ import annotations

import inspect

from turing_research_plus.adapters.protocols import (
    ArxivAdapter,
    OpenAICompatibleLLMAdapter,
    PDFConverterAdapter,
    SemanticScholarAdapter,
    WebFetchAdapter,
    WebSearchAdapter,
)


def test_required_adapter_protocols_are_declared() -> None:
    protocols = [
        (SemanticScholarAdapter, "paper_lookup"),
        (ArxivAdapter, "search"),
        (WebSearchAdapter, "search"),
        (WebFetchAdapter, "fetch"),
        (OpenAICompatibleLLMAdapter, "complete"),
        (PDFConverterAdapter, "convert"),
    ]

    for protocol, method_name in protocols:
        assert getattr(protocol, "_is_protocol", False) is True
        assert inspect.isfunction(getattr(protocol, method_name))

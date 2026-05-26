from __future__ import annotations

from turing_research_plus.web.html_extract import extract_title, html_to_text


def test_html_extract_title_and_text() -> None:
    html = (
        "<html><head><title> Demo </title><style>.x{}</style></head>"
        "<body><h1>Hello</h1><script>x()</script><p>World</p></body></html>"
    )

    assert extract_title(html) == "Demo"
    text = html_to_text(html)
    assert "Hello" in text
    assert "World" in text
    assert "x()" not in text

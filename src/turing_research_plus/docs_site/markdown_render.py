"""Small Markdown-to-HTML renderer for local docs-site builds."""

from __future__ import annotations

import html
import re

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")


def render_markdown_to_html(markdown: str) -> str:
    """Render a conservative Markdown subset to HTML."""

    blocks: list[str] = []
    list_items: list[str] = []
    in_code = False
    code_lines: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(f"<p>{_inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            blocks.append("<ul>\n" + "\n".join(list_items) + "\n</ul>")
            list_items.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                blocks.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                flush_paragraph()
                flush_list()
                in_code = True
            continue
        if in_code:
            code_lines.append(raw_line)
            continue
        if not line.strip():
            flush_paragraph()
            flush_list()
            continue
        if line.startswith("#"):
            flush_paragraph()
            flush_list()
            level = min(len(line) - len(line.lstrip("#")), 6)
            text = line[level:].strip()
            blocks.append(f"<h{level}>{_inline(text)}</h{level}>")
            continue
        if line.startswith("- "):
            flush_paragraph()
            list_items.append(f"<li>{_inline(line[2:].strip())}</li>")
            continue
        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_list()
            blocks.append(f"<pre>{html.escape(line)}</pre>")
            continue
        paragraph.append(line.strip())

    if in_code:
        blocks.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    flush_paragraph()
    flush_list()
    return "\n".join(blocks)


def _inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = LINK_RE.sub(r'<a href="\2">\1</a>', escaped)
    return INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)

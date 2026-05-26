"""Simple BM25-like index for vault pages."""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

from turing_research_plus.vault.markdown_io import list_page_paths, read_page
from turing_research_plus.vault.models import VaultPage, VaultSearchResult

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    """Tokenize text for simple search."""

    return [token.lower() for token in TOKEN_RE.findall(text)]


class VaultIndex:
    """Small replaceable BM25-like index."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def pages(self) -> list[VaultPage]:
        """Return all readable pages."""

        return [read_page(path) for path in list_page_paths(self.root)]

    def search(self, query: str, limit: int = 10) -> list[VaultSearchResult]:
        """Search pages using a simple BM25-like score."""

        pages = self.pages()
        if not pages:
            return []
        query_terms = tokenize(query)
        docs = {
            page.page_id: tokenize(f"{page.title}\n{page.body}\n{' '.join(page.tags)}")
            for page in pages
        }
        doc_count = len(docs)
        avg_len = sum(len(tokens) for tokens in docs.values()) / max(doc_count, 1)
        scores: dict[str, float] = {}
        for term in query_terms:
            containing = sum(1 for tokens in docs.values() if term in tokens)
            if containing == 0:
                continue
            idf = math.log(1 + (doc_count - containing + 0.5) / (containing + 0.5))
            for page_id, tokens in docs.items():
                freq = Counter(tokens)[term]
                if freq == 0:
                    continue
                doc_len = len(tokens)
                denom = freq + 1.5 * (1 - 0.75 + 0.75 * doc_len / max(avg_len, 1))
                scores[page_id] = scores.get(page_id, 0.0) + idf * (freq * 2.5 / denom)
        page_by_id = {page.page_id: page for page in pages}
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:limit]
        return [
            VaultSearchResult(
                page_id=page_id,
                title=page_by_id[page_id].title,
                score=round(score, 6),
                path=self.root / page_by_id[page_id].filename,
            )
            for page_id, score in ranked
        ]

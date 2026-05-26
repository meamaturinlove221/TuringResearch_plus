"""Author network construction."""

from __future__ import annotations

from collections import deque
from itertools import combinations

from tuling_research_plus.semantic_graph.client import SemanticGraphAdapter
from tuling_research_plus.semantic_graph.models import (
    AuthorEdge,
    AuthorNetworkInput,
    AuthorNetworkOutput,
    AuthorNode,
    GraphStatus,
)


class AuthorGraphBuilder:
    """Build author co-author networks through an adapter boundary."""

    def __init__(self, adapter: SemanticGraphAdapter) -> None:
        self.adapter = adapter

    def expand(self, request: AuthorNetworkInput) -> AuthorNetworkOutput:
        authors: dict[str, AuthorNode] = {}
        edges: dict[tuple[str, str], AuthorEdge] = {}
        frontier: dict[str, AuthorNode] = {}
        queue: deque[tuple[str, int]] = deque(
            (author_id, 0) for author_id in request.seed_author_ids
        )
        seen_depth: dict[str, int] = {}

        while queue and len(authors) < request.max_authors:
            author_id, depth = queue.popleft()
            if seen_depth.get(author_id, request.max_depth + 1) <= depth:
                continue
            seen_depth[author_id] = depth
            author = self.adapter.author(author_id)
            if author is None:
                continue
            authors[author.author_id] = author
            papers = self.adapter.author_papers(author.author_id)
            for paper in papers:
                coauthors = [coauthor for coauthor in paper.authors if coauthor != author.author_id]
                for left, right in combinations([author.author_id, *coauthors], 2):
                    sorted_pair = sorted((left, right))
                    key = (sorted_pair[0], sorted_pair[1])
                    edge = edges.get(key)
                    if edge is None:
                        edge = AuthorEdge(
                            source_author_id=key[0],
                            target_author_id=key[1],
                            shared_paper_ids=[],
                        )
                        edges[key] = edge
                    if paper.paper_id not in edge.shared_paper_ids:
                        edge.shared_paper_ids.append(paper.paper_id)
                if depth >= request.max_depth:
                    continue
                for coauthor_id in coauthors:
                    coauthor = self.adapter.author(coauthor_id)
                    if coauthor is None:
                        continue
                    if len(authors) >= request.max_authors and coauthor.author_id not in authors:
                        frontier[coauthor.author_id] = coauthor
                        continue
                    if coauthor.author_id not in seen_depth:
                        queue.append((coauthor.author_id, depth + 1))

        return AuthorNetworkOutput(
            status=GraphStatus.OK,
            authors=list(authors.values()),
            edges=list(edges.values()),
            frontier_authors=list(frontier.values()),
        )

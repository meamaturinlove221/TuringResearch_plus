"""Route table for the read-only local dashboard server."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.local_server.models import (
    LocalDashboardContentType,
    LocalDashboardResponse,
    LocalDashboardRoute,
)
from turing_research_plus.local_server.static_files import (
    render_json_summary,
    render_markdown_summary,
    render_not_found,
    render_static_html,
)


def build_default_routes(public_demo_dir: Path) -> list[LocalDashboardRoute]:
    """Build the default public demo dashboard route table."""

    return [
        LocalDashboardRoute(
            path="/",
            title="Public Demo Dashboard",
            description="Static public demo dashboard.",
            source_path=public_demo_dir / "demo_dashboard_refined.html",
        ),
        LocalDashboardRoute(
            path="/dashboard",
            title="Public Demo Dashboard",
            description="Static public demo dashboard.",
            source_path=public_demo_dir / "demo_dashboard_refined.html",
        ),
        LocalDashboardRoute(
            path="/project",
            title="Project Overview",
            description="Project overview from public demo intent.",
            source_path=public_demo_dir / "demo_research_intent.md",
        ),
        LocalDashboardRoute(
            path="/evidence",
            title="Evidence Summary",
            description="Evidence summary from demo ledger.",
            source_path=public_demo_dir / "demo_evidence_ledger.json",
        ),
        LocalDashboardRoute(
            path="/artifacts",
            title="Artifact Summary",
            description="Artifact summary from demo index.",
            source_path=public_demo_dir / "demo_artifact_index.md",
        ),
        LocalDashboardRoute(
            path="/paper",
            title="Paper Summary",
            description="Paper and related work summary.",
            source_path=public_demo_dir / "demo_related_work.md",
        ),
        LocalDashboardRoute(
            path="/advisor",
            title="Advisor Bundle Summary",
            description="Advisor bundle summary.",
            source_path=public_demo_dir / "demo_advisor_pack.md",
        ),
        LocalDashboardRoute(
            path="/health",
            title="Health",
            description="Local server health check.",
            content_type=LocalDashboardContentType.JSON,
        ),
    ]


def resolve_route(routes: list[LocalDashboardRoute], route_path: str) -> LocalDashboardRoute | None:
    """Resolve a normalized route path."""

    normalized = route_path.split("?", 1)[0].rstrip("/") or "/"
    for route in routes:
        if route.path == normalized:
            return route
    return None


def render_route(route: LocalDashboardRoute | None, route_path: str) -> LocalDashboardResponse:
    """Render a route into a response."""

    if route is None:
        return render_not_found(route_path)
    if route.path == "/health":
        return LocalDashboardResponse(
            status_code=200,
            content_type=LocalDashboardContentType.JSON,
            body='{"status":"ok","localhost_only":true,"read_only":true}',
            route_path=route.path,
        )
    if route.source_path is None:
        return render_not_found(route_path)
    if route.source_path.suffix == ".html":
        return render_static_html(route.title, route.source_path, route.path)
    if route.source_path.suffix == ".json":
        return render_json_summary(route.title, route.source_path, route.path)
    return render_markdown_summary(route.title, route.source_path, route.path)

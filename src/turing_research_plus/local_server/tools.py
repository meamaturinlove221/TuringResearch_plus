"""Tool wrappers for the local server dashboard."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.local_server.models import LocalDashboardRequest
from turing_research_plus.local_server.routes import (
    build_default_routes,
    render_route,
    resolve_route,
)


def preview_public_demo_route(repo_root: Path, route_path: str) -> dict[str, object]:
    """Preview a local dashboard route without starting a server."""

    public_demo_dir = repo_root / "examples" / "public_demo"
    request = LocalDashboardRequest(repo_root=repo_root, public_demo_dir=public_demo_dir)
    routes = build_default_routes(request.public_demo_dir)
    route = resolve_route(routes, route_path)
    response = render_route(route, route_path)
    return response.model_dump(mode="json")

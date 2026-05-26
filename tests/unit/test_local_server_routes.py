from __future__ import annotations

from pathlib import Path

from turing_research_plus.local_server.routes import (
    build_default_routes,
    render_route,
    resolve_route,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_default_routes_cover_required_summaries() -> None:
    routes = build_default_routes(DEMO)
    paths = {route.path for route in routes}

    assert {
        "/",
        "/dashboard",
        "/project",
        "/evidence",
        "/artifacts",
        "/paper",
        "/advisor",
        "/health",
    } <= paths


def test_render_evidence_route_is_read_only_html() -> None:
    routes = build_default_routes(DEMO)
    response = render_route(resolve_route(routes, "/evidence"), "/evidence")

    assert response.status_code == 200
    assert "Evidence Summary" in response.body
    assert "not observed research evidence" in response.body
    assert response.served_from is not None


def test_unknown_route_returns_404() -> None:
    response = render_route(None, "/missing")

    assert response.status_code == 404
    assert "Route not found" in response.body

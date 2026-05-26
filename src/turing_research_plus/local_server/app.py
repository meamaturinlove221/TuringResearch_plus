"""Minimal localhost HTTP app for the dashboard."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Self

from turing_research_plus.local_server.models import LocalDashboardRequest
from turing_research_plus.local_server.routes import (
    build_default_routes,
    render_route,
    resolve_route,
)


class LocalDashboardHTTPServer(ThreadingHTTPServer):
    """HTTP server with local dashboard request context."""

    request_config: LocalDashboardRequest


def create_local_dashboard_server(request: LocalDashboardRequest) -> LocalDashboardHTTPServer:
    """Create a localhost-only read-only dashboard server."""

    routes = build_default_routes(request.public_demo_dir)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self: Self) -> None:  # noqa: N802
            route = resolve_route(routes, self.path)
            response = render_route(route, self.path)
            self.send_response(response.status_code)
            self.send_header("Content-Type", response.content_type)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(response.body.encode("utf-8"))

        def do_POST(self: Self) -> None:  # noqa: N802
            self.send_response(405)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Read-only local dashboard")

        def log_message(self: Self, format: str, *args: object) -> None:
            return

    server = LocalDashboardHTTPServer((request.host, request.port), Handler)
    server.request_config = request
    return server

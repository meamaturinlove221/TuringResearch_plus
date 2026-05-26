"""Read and render public demo files for the local dashboard server."""

from __future__ import annotations

import html
import json
from pathlib import Path

from turing_research_plus.local_server.models import (
    LocalDashboardContentType,
    LocalDashboardResponse,
)


def render_markdown_summary(
    title: str,
    source_path: Path,
    route_path: str,
) -> LocalDashboardResponse:
    """Render a Markdown file into a small escaped HTML page."""

    text = _read_text(source_path)
    body = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{html.escape(title)}</title></head>
<body>
  <main>
    <h1>{html.escape(title)}</h1>
    <p>Read-only local dashboard view. Human review required.</p>
    <pre>{html.escape(text)}</pre>
  </main>
</body>
</html>
"""
    return LocalDashboardResponse(
        status_code=200,
        content_type=LocalDashboardContentType.HTML,
        body=body,
        route_path=route_path,
        served_from=str(source_path),
    )


def render_json_summary(title: str, source_path: Path, route_path: str) -> LocalDashboardResponse:
    """Render a JSON file as escaped pretty JSON HTML."""

    text = _read_text(source_path)
    try:
        payload = json.dumps(json.loads(text), indent=2, sort_keys=True)
    except json.JSONDecodeError:
        payload = text
    body = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{html.escape(title)}</title></head>
<body>
  <main>
    <h1>{html.escape(title)}</h1>
    <p>Read-only evidence summary. Demo/fake material is not observed research evidence.</p>
    <pre>{html.escape(payload)}</pre>
  </main>
</body>
</html>
"""
    return LocalDashboardResponse(
        status_code=200,
        content_type=LocalDashboardContentType.HTML,
        body=body,
        route_path=route_path,
        served_from=str(source_path),
    )


def render_static_html(title: str, source_path: Path, route_path: str) -> LocalDashboardResponse:
    """Serve a static HTML file from the public demo directory."""

    html_text = _read_text(source_path)
    return LocalDashboardResponse(
        status_code=200,
        content_type=LocalDashboardContentType.HTML,
        body=html_text,
        route_path=route_path,
        served_from=str(source_path),
    )


def render_not_found(route_path: str) -> LocalDashboardResponse:
    """Return a local 404 response."""

    return LocalDashboardResponse(
        status_code=404,
        content_type=LocalDashboardContentType.TEXT,
        body=f"Route not found: {route_path}",
        route_path=route_path,
    )


def _read_text(path: Path) -> str:
    if not path.exists():
        return f"Missing source file: {path}"
    return path.read_text(encoding="utf-8")

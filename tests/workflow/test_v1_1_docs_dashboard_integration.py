from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.dashboard_api.export import (
    build_public_demo_dashboard_data,
    export_json,
)
from turing_research_plus.docs_site.builder import build_docs_site_from_repo
from turing_research_plus.local_server.app import create_local_dashboard_server
from turing_research_plus.local_server.models import LocalDashboardRequest
from turing_research_plus.local_server.tools import preview_public_demo_route

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_docs_site_builds_and_links_readme(tmp_path: Path) -> None:
    result = build_docs_site_from_repo(ROOT, output_root=tmp_path)

    generated = {path.name for path in result.generated_files}
    assert {"index.html", "dashboard.html", "quickstart.html", "site.css"} <= generated
    assert result.requires_human_review is True

    nav_text = (ROOT / "docs-site" / "nav.yaml").read_text(encoding="utf-8")
    assert "../README.md" in nav_text

    dashboard_html = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
    assert "Dashboard" in dashboard_html
    assert "Source Docs" in dashboard_html


def test_dashboard_data_api_exports_public_demo_bundle() -> None:
    bundle = build_public_demo_dashboard_data(DEMO)
    payload = json.loads(export_json(bundle))

    assert payload["read_only"] is True
    assert payload["supports_json_export"] is True
    assert payload["supports_dashboard_rendering"] is True
    assert payload["no_secrets"] is True
    assert payload["no_raw_data"] is True
    assert payload["no_private_path"] is True
    assert "observed" not in payload["evidence"]["status_counts"]


def test_local_server_public_demo_routes_are_read_only_and_localhost() -> None:
    server = create_local_dashboard_server(
        LocalDashboardRequest(repo_root=ROOT, public_demo_dir=DEMO, port=0)
    )
    try:
        assert server.server_address[0] == "127.0.0.1"
        assert server.request_config.safety.localhost_only is True
        assert server.request_config.safety.read_only is True
        assert server.request_config.safety.executes_commands is False
        assert server.request_config.safety.uploads_data is False
    finally:
        server.server_close()

    for route in ["/dashboard", "/project", "/evidence", "/artifacts", "/paper", "/advisor"]:
        response = preview_public_demo_route(ROOT, route)
        assert response["status_code"] == 200
        assert response["content_type"] == "text/html; charset=utf-8"


def test_docs_dashboard_integration_has_no_sensitive_patterns(tmp_path: Path) -> None:
    build_docs_site_from_repo(ROOT, output_root=tmp_path)
    exported = export_json(build_public_demo_dashboard_data(DEMO))
    route_preview = str(preview_public_demo_route(ROOT, "/dashboard"))
    generated_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in tmp_path.glob("*.html")
        if path.name in {"index.html", "dashboard.html", "quickstart.html"}
    )
    combined = "\n".join([exported, route_preview, generated_text])

    assert "D:/vggt" not in combined
    assert "D:\\\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "raw private data included" not in combined.lower()

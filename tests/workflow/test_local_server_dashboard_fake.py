from __future__ import annotations

from pathlib import Path

from turing_research_plus.local_server.app import create_local_dashboard_server
from turing_research_plus.local_server.models import LocalDashboardRequest
from turing_research_plus.local_server.tools import preview_public_demo_route

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_local_server_can_be_created_for_localhost_only() -> None:
    server = create_local_dashboard_server(
        LocalDashboardRequest(repo_root=ROOT, public_demo_dir=DEMO, port=0)
    )
    try:
        assert server.server_address[0] == "127.0.0.1"
        assert server.request_config.safety.localhost_only is True
        assert server.request_config.safety.read_only is True
    finally:
        server.server_close()


def test_preview_public_demo_routes_without_starting_server() -> None:
    for route in ["/dashboard", "/project", "/evidence", "/artifacts", "/paper", "/advisor"]:
        response = preview_public_demo_route(ROOT, route)
        assert response["status_code"] == 200
        assert "private" not in str(response.get("served_from", "")).lower()


def test_local_server_does_not_execute_or_upload() -> None:
    request = LocalDashboardRequest(repo_root=ROOT, public_demo_dir=DEMO)

    assert request.safety.executes_commands is False
    assert request.safety.uploads_data is False
    assert request.safety.default_networking is False
    assert request.safety.displays_secrets is False

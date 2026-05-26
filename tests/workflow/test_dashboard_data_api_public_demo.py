from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.dashboard_api.export import (
    build_public_demo_dashboard_data,
    export_json,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_dashboard_data_api_supports_public_demo_json_export() -> None:
    bundle = build_public_demo_dashboard_data(DEMO)
    payload = json.loads(export_json(bundle))

    assert payload["bundle_id"] == "public_demo_dashboard_data"
    assert payload["read_only"] is True
    assert payload["no_secrets"] is True
    assert payload["no_raw_data"] is True
    assert payload["no_private_path"] is True
    assert payload["supports_json_export"] is True
    assert payload["supports_dashboard_rendering"] is True
    assert payload["evidence"]["status_counts"]["planned"] == 1
    assert "observed" not in payload["evidence"]["status_counts"]


def test_dashboard_data_api_export_has_no_secret_or_private_path_patterns() -> None:
    exported = export_json(build_public_demo_dashboard_data(DEMO))

    assert "D:/vggt" not in exported
    assert "D:\\\\vggt" not in exported
    assert "sk-" not in exported
    assert "ghp_" not in exported
    assert "local_project_links.yaml" not in exported

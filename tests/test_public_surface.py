from __future__ import annotations

import json


def test_canonical_and_legacy_packages_share_version() -> None:
    import tuling_research
    import tuling_research_plus
    import turing_research
    import turing_research_plus

    assert turing_research.__version__ == tuling_research.__version__
    assert turing_research_plus.__version__ == tuling_research_plus.__version__
    assert turing_research.PACKAGE_NAME == "turing_research"
    assert turing_research_plus.PACKAGE_NAME == "turing_research_plus"


def test_canonical_mcp_manifest_import_path() -> None:
    from turing_research.mcp_server import build_stdio_manifest, core_health_check, main

    manifest = build_stdio_manifest()
    assert manifest["server_name"] in {"turingresearch-plus", "tulingresearch-plus"}
    assert manifest["tools"]

    health = core_health_check()
    assert health["status"] == "ok"
    assert "core.health_check" in health["tools"]

    assert main(["--manifest"]) == 0


def test_manifest_is_json_serializable() -> None:
    from turing_research.mcp_server import build_stdio_manifest

    payload = json.dumps(build_stdio_manifest(), ensure_ascii=False)
    assert "core.health_check" in payload

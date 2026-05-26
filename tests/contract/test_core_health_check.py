from turing_research.mcp_server import core_health_check


def test_core_health_check_contract() -> None:
    result = core_health_check()

    assert result["status"] == "ok"
    assert result["package"] == "turing_research"
    assert "core.health_check" in result["tools"]
    assert "core.paper_content" in result["tools"]
    assert "core.web_content" in result["tools"]
    assert "core.session_list" in result["tools"]

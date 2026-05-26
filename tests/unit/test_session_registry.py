from turing_research.session.registry import SessionRegistry


def test_session_list_empty_registry(tmp_path) -> None:
    result = SessionRegistry(tmp_path / "missing_registry.json").list_sessions()

    assert result.sessions == []

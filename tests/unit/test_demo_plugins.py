from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.demo_plugins import (
    DEMO_PLUGIN_ID,
    DEMO_PLUGIN_PATH,
    built_in_demo_plugin_paths,
)


def test_built_in_demo_plugin_path_is_repo_relative() -> None:
    assert DEMO_PLUGIN_ID == "trusted_local_demo_plugin"
    assert DEMO_PLUGIN_PATH == Path("examples/plugins/trusted_local_demo_plugin/plugin.yaml")


def test_built_in_demo_plugin_paths_accept_root(tmp_path: Path) -> None:
    paths = built_in_demo_plugin_paths(tmp_path)

    assert paths == [tmp_path / DEMO_PLUGIN_PATH]

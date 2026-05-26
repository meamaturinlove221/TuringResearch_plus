"""Built-in demo plugin metadata."""

from __future__ import annotations

from pathlib import Path

DEMO_PLUGIN_ID = "trusted_local_demo_plugin"
DEMO_PLUGIN_PATH = Path("examples/plugins/trusted_local_demo_plugin/plugin.yaml")


def built_in_demo_plugin_paths(root: Path | None = None) -> list[Path]:
    """Return built-in demo plugin manifest paths."""

    base = Path.cwd() if root is None else root
    return [base / DEMO_PLUGIN_PATH]

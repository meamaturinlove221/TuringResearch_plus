from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_session_cli_entrypoint_declared_and_resolvable() -> None:
    project = pyproject()["project"]
    assert isinstance(project, dict)
    scripts = project["scripts"]
    assert isinstance(scripts, dict)

    assert scripts["turingresearch-session"] == "turing_research_plus.session_runtime.cli:main"
    module = importlib.import_module("turing_research_plus.session_runtime.cli")
    assert callable(module.main)


def test_session_cli_contract_documents_fake_default_boundary() -> None:
    text = (ROOT / "contracts" / "session_cli_surface.yaml").read_text(encoding="utf-8")

    assert "session preflight" in text
    assert "session pack" in text
    assert "session transfer --fake" in text
    assert "session verify-return" in text
    assert "session replay" in text
    assert "session report" in text
    assert "live_ssh_disabled_by_default: true" in text
    assert "remote_command_execution: false" in text
    assert "automatic_evidence_ledger_write: false" in text


def test_session_cli_docs_reference_entrypoint() -> None:
    text = (ROOT / "docs" / "session-cli-surface.md").read_text(encoding="utf-8")
    guide = (ROOT / "docs" / "session-cli-usage-guide.md").read_text(encoding="utf-8")

    assert "turingresearch-session" in text
    assert "turing_research_plus.session_runtime.cli:main" in text
    assert "session transfer --fake" in guide
    assert "no remote command" in guide.lower()
    assert "no automatic evidence ledger write" in guide.lower()

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tuling_research_plus.artifacts.models import EvidenceRef

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"


def read_json(relative: str) -> Any:
    return json.loads((EXAMPLES / relative).read_text(encoding="utf-8"))


def read_text(relative: str) -> str:
    return (EXAMPLES / relative).read_text(encoding="utf-8")


def example_evidence(source_id: str = "example-source") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="fixture",
        quote="Example dry-run fixture evidence.",
        confidence=0.9,
    )


def assert_example_contract(example_name: str, required_artifacts: set[str]) -> None:
    base = EXAMPLES / example_name
    assert (base / "input").is_dir()
    assert (base / "expected_outputs").is_dir()
    assert (base / "README.md").exists()
    assert (base / "fake_run_config.yaml").exists()
    artifact_list = read_json(f"{example_name}/expected_outputs/artifact_list.json")
    assert set(artifact_list) == required_artifacts
    config = (base / "fake_run_config.yaml").read_text(encoding="utf-8").lower()
    assert "network: disabled" in config
    assert "requires_api_keys: false" in config


def to_pretty_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)

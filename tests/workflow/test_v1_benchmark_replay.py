from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.models import BenchmarkScenario, BenchmarkStep
from turing_research_plus.benchmark.replay_runner import run_benchmark_scenario
from turing_research_plus.benchmark.scenarios import vggt_fake_replay_scenario

ROOT = Path(__file__).resolve().parents[2]
SCENARIO_FILE = ROOT / "examples" / "benchmarks" / "v1_public_demo_replay.yaml"


def _parse_simple_yaml_list(lines: list[str], start: int) -> tuple[list[str], int]:
    values: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if line.startswith("  - "):
            values.append(line[4:].strip())
            index += 1
            continue
        if line and not line.startswith(" "):
            break
        index += 1
    return values, index


def load_v1_public_demo_scenario() -> BenchmarkScenario:
    lines = SCENARIO_FILE.read_text(encoding="utf-8").splitlines()
    fields: dict[str, str | bool | list[str]] = {}
    expected_outputs: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line.startswith(" "):
            index += 1
            continue
        if line == "expected_outputs:":
            expected_outputs, index = _parse_simple_yaml_list(lines, index + 1)
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if value == "true":
                fields[key] = True
            elif value == "false":
                fields[key] = False
            else:
                fields[key] = value
        index += 1

    return BenchmarkScenario(
        scenario_id=str(fields["scenario_id"]),
        name=str(fields["name"]),
        root_path=str(ROOT / str(fields["root_path"])),
        demo_only=bool(fields["demo_only"]),
        no_real_experiment=bool(fields["no_real_experiment"]),
        network_required=bool(fields["network_required"]),
        requires_human_review=bool(fields["requires_human_review"]),
        expected_outputs=expected_outputs,
        steps=[
            BenchmarkStep(
                step_id="v1-public-demo-replay",
                description="Check v1 public demo replay outputs.",
                expected_outputs=expected_outputs,
            )
        ],
    )


def test_v1_public_demo_replay_yaml_exists_and_passes() -> None:
    report = run_benchmark_scenario(load_v1_public_demo_scenario())

    assert report.scenario_id == "v1_public_demo_replay"
    assert report.status == "pass"
    assert report.missing_outputs == []
    assert report.regression_flags == []
    assert report.demo_only is True
    assert report.no_real_experiment is True


def test_v1_benchmark_refresh_keeps_vggt_fake_replay_aligned() -> None:
    report = run_benchmark_scenario(vggt_fake_replay_scenario(ROOT))

    assert report.scenario_id == "vggt_fake_replay"
    assert report.status == "pass"
    assert report.missing_outputs == []
    assert report.demo_only is True
    assert report.no_real_experiment is True

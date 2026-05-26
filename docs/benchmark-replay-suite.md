# Benchmark / Replay Suite

Status: implemented minimal.

The Benchmark / Replay Suite checks local demo and replay fixtures without
running real experiments. It is a regression harness for public demo material,
VGGT fake replay, demo workspace outputs, and paper assembly outputs.

## Built-in Scenarios

- `public_demo_replay`
- `vggt_fake_replay`
- `demo_workspace_replay`
- `paper_assembly_replay`

## Report Fields

`BenchmarkReport` contains:

- `scenario_id`
- `steps`
- `expected_outputs`
- `actual_outputs`
- `missing_outputs`
- `status`
- `duration`
- `warnings`
- `regression_flags`

## Safety Boundary

- Demo-only by default.
- No real experiment execution.
- No VGGT or Modal execution.
- No network access.
- No observed evidence is created.
- Missing outputs are regression flags, not research failures.

## Fixtures

- `examples/benchmarks/public_demo_replay.yaml`
- `examples/benchmarks/vggt_fake_replay.yaml`

## Tests

- `tests/unit/test_benchmark_models.py`
- `tests/unit/test_replay_runner.py`
- `tests/unit/test_benchmark_scenarios.py`
- `tests/unit/test_benchmark_report.py`
- `tests/workflow/test_public_demo_replay.py`
- `tests/workflow/test_vggt_fake_replay_benchmark.py`

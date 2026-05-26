# Lane 161 - Demo / Benchmark Refresh

Status: refresh complete.

Round: 180.

## Goal

Refresh public demo, benchmark replay, and VGGT fake replay alignment for v1.0
quickstart and release demo review.

## Outputs

- `docs/v1.0.0-demo-refresh-report.md`
- `docs/v1.0.0-benchmark-refresh-report.md`
- `examples/public_demo/demo_manifest.yaml`
- `examples/benchmarks/v1_public_demo_replay.yaml`
- `tests/workflow/test_v1_demo_refresh.py`
- `tests/workflow/test_v1_benchmark_replay.py`
- `lanes/00_master_ledger.md`

## Checked

- demo files exist;
- benchmark scenario passes;
- dashboard demo outputs exist;
- advisor bundle demo outputs exist;
- fake/demo status is clear;
- no secrets;
- no raw data;
- no private local paths;
- no restricted model payloads;
- no observed fake result.

## Boundaries

- No feature implementation.
- No real experiment execution.
- No VGGT execution.
- No Modal execution.
- No network access.
- No result claim promotion.

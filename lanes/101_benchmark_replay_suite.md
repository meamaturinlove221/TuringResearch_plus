# Lane 101 - Benchmark / Replay Suite

Status: implemented minimal.

## Scope

Round 120 adds a local benchmark / replay suite for demo-only workflow checks.
It verifies expected local outputs for public demo, VGGT fake replay,
multi-project workspace, and paper assembly outputs.

## Added

- `src/turing_research_plus/benchmark/`
- `contracts/benchmark_replay.yaml`
- `docs/benchmark-replay-suite.md`
- `examples/benchmarks/public_demo_replay.yaml`
- `examples/benchmarks/vggt_fake_replay.yaml`
- benchmark unit and workflow tests

## Built-in Scenarios

- `public_demo_replay`
- `vggt_fake_replay`
- `demo_workspace_replay`
- `paper_assembly_replay`

## Boundaries

- Demo-only replay.
- No real experiment execution.
- No network access.
- No observed evidence generation.
- Missing outputs become regression flags.

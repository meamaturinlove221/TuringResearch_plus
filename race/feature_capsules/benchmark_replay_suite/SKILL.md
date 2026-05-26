# Benchmark / Replay Suite Skill



Status: planning skill draft.



Use this skill when a task is about `benchmark_replay_suite` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `Benchmark / Replay Suite` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- public demo fixtures

- project templates

- dashboard outputs

- advisor bundles

- fake evidence ledgers



## Outputs



- BenchmarkReplayReport

- DemoSuiteManifest

- ReplayReadinessReport



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- benchmark_replay_suite.yaml

- project_template.yaml

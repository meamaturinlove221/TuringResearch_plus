# Benchmark / Replay Suite



Status: feature capsule draft.



Release target: v0.6 Sprint 3.



## 1. Problem



Public users need repeatable fake/default examples that exercise workflows without private data or real experiment claims.



## 2. VGGT / Research Motivating Example



The VGGT dogfooding replay can inspire demo replay patterns, but benchmark outputs must stay demo/replay and not become observed evidence.



## 3. Upstream / Internal Inspiration



Public Demo Suite, VGGT Dogfooding Replay, and v0.5 alpha integration gate.



## 4. User Story



As a maintainer, I want a benchmark suite that proves workflows run locally and safely on demo data.



## 5. Inputs



- public demo fixtures

- project templates

- dashboard outputs

- advisor bundles

- fake evidence ledgers



## 6. Outputs



- BenchmarkReplayReport

- DemoSuiteManifest

- ReplayReadinessReport



## 7. Data Model



BenchmarkReplayReport, BenchmarkScenario, ReplayReadinessReport



## 8. Proposed Commands / Tools



- command: `turing demo replay`; tool: `demo.replay`; output: `BenchmarkReplayReport`



## 9. Related Contracts



- benchmark_replay_suite.yaml

- project_template.yaml



## 10. Related Skills



- turingresearch-qa-release

- turingresearch-master-orchestrator



## 11. Required Tests



- benchmark manifest tests

- demo replay workflow tests

- public hygiene tests



## 12. Risks



- demo result mistaken for real result

- private data leak

- snapshot drift



## 13. Done Criteria



- fake/default replay runs locally

- outputs are clearly demo-only

- hygiene checks pass



## 14. Release Target



v0.6 Sprint 3



## 15. Non-goals



- no real benchmark claims

- no private data

- no live network dependency

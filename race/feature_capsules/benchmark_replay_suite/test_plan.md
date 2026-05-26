# Benchmark / Replay Suite Test Plan



Status: planning.



## Unit Tests



- benchmark manifest tests

- demo replay workflow tests

- public hygiene tests



## Contract Tests



- Contract schema loads.

- Required fields are present.

- Fake/default mode is explicit.

- Safety and human-review fields are present.



## Workflow Tests



- Build a fake/demo fixture.

- Export Markdown or JSON output.

- Confirm no secrets, raw data, private paths, or private model files.

- Confirm fake/demo/planned material is not marked observed.



## Non-goal Checks



- no real benchmark claims

- no private data

- no live network dependency

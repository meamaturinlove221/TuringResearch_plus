# Privacy / Data Policy Test Plan



Status: planning.



## Unit Tests



- privacy model tests

- scanner tests

- release gate contract tests



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



- no destructive cleanup

- no automatic deletion

- no upload of scan results

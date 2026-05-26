# Multi-project Workspace Test Plan



Status: planning.



## Unit Tests



- workspace model tests

- registry loader tests

- demo workspace workflow test



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



- no SaaS workspace

- no cloud account system

- no automatic project discovery outside explicit roots

# Tool Capability Manifest Test Plan



Status: planning.



## Unit Tests



- capability model tests

- collector tests

- manifest export tests

- fake manifest workflow



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



- no automatic tool execution

- no live discovery

- no marketplace publish

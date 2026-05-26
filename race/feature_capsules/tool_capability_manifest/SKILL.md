# Tool Capability Manifest Skill



Status: planning skill draft.



Use this skill when a task is about `tool_capability_manifest` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `Tool Capability Manifest` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- contracts

- docs

- tool names

- module paths

- test references

- skill registry



## Outputs



- CapabilityManifest

- CapabilityIndex

- Markdown capability table



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- tool_capability_manifest.yaml

- skill_routing.yaml

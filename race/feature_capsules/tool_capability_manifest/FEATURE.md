# Tool Capability Manifest



Status: feature capsule draft.



Release target: v0.6 Sprint 2.



## 1. Problem



TuringResearch has many tools, adapters, exporters, and workflows; routing and public docs need a unified capability index.



## 2. VGGT / Research Motivating Example



Advisor export, dashboard, remote artifact readers, and paper digest should each declare live/fake mode, input/output model, safety level, docs, and tests.



## 3. Upstream / Internal Inspiration



Skill routing, MCP docs, and plugin architecture planning.



## 4. User Story



As a user, I want to see which capabilities are stable, fake-only, live-optional, or review-required.



## 5. Inputs



- contracts

- docs

- tool names

- module paths

- test references

- skill registry



## 6. Outputs



- CapabilityManifest

- CapabilityIndex

- Markdown capability table



## 7. Data Model



CapabilityManifest, CapabilityEntry, CapabilitySafetyLevel



## 8. Proposed Commands / Tools



- command: `turing capabilities export`; tool: `capabilities.export`; output: `CapabilityManifest`



## 9. Related Contracts



- tool_capability_manifest.yaml

- skill_routing.yaml



## 10. Related Skills



- turingresearch-master-orchestrator

- turingresearch-qa-release



## 11. Required Tests



- capability model tests

- collector tests

- manifest export tests

- fake manifest workflow



## 12. Risks



- capability status drift

- public docs overclaiming

- missing tests



## 13. Done Criteria



- manifest covers core categories

- fake/live modes are explicit

- docs/tests links are present



## 14. Release Target



v0.6 Sprint 2



## 15. Non-goals



- no automatic tool execution

- no live discovery

- no marketplace publish

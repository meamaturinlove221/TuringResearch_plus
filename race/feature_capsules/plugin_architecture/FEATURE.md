# Plugin Architecture



Status: feature capsule draft.



Release target: v0.6 Sprint 2.



## 1. Problem



TuringResearch needs a public extension boundary without allowing unreviewed code or unsafe live access.



## 2. VGGT / Research Motivating Example



A future project-specific plugin can add a domain route pack, but it must declare capabilities, safety level, docs, and tests.



## 3. Upstream / Internal Inspiration



Round 102 public plugin ecosystem and MCP marketplace readiness planning.



## 4. User Story



As a plugin author, I want a manifest schema that describes what the plugin contributes and what safety gates it requires.



## 5. Inputs



- plugin manifest

- capability declarations

- contracts

- docs

- tests



## 6. Outputs



- PluginManifest

- PluginValidationReport

- PluginSafetyProfile



## 7. Data Model



PluginManifest, PluginCapability, PluginSafetyProfile



## 8. Proposed Commands / Tools



- command: `turing plugin validate`; tool: `plugin.validate`; output: `PluginValidationReport`



## 9. Related Contracts



- plugin_architecture.yaml

- tool_capability_manifest.yaml



## 10. Related Skills



- turingresearch-architecture-contracts

- turingresearch-qa-release



## 11. Required Tests



- plugin manifest tests

- safety profile tests

- schema contract tests



## 12. Risks



- supply-chain risk

- implicit code execution

- license ambiguity



## 13. Done Criteria



- manifest schema is documented

- validation is fake/local

- no automatic plugin execution



## 14. Release Target



v0.6 Sprint 2



## 15. Non-goals



- no plugin marketplace publishing

- no automatic install

- no untrusted code execution

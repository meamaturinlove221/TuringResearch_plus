# Trusted Local Plugin Loading

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

TuringResearch needs a path from manifest-only plugins toward reviewed local
plugin loading without enabling unknown third-party code.

## 2. Research Motivating Example

A lab may want a local domain exporter plugin for advisor bundles, but it must
be explicitly trusted, documented, tested, and disabled until reviewed.

## 3. Inputs

- plugin manifest
- trusted allowlist
- extension safety report
- compatibility harness result

## 4. Outputs

- TrustedPluginLoadPlan
- PluginLoadDecision
- PluginLoadSafetyReport

## 5. Proposed Commands / Tools

- command: `turing plugin trust-plan`
- tool: `plugin.trusted_load_plan`
- output: `TrustedPluginLoadPlan`

## 6. Related Contracts

- trusted_local_plugin_loading.yaml
- plugin_architecture.yaml
- extension_safety.yaml

## 7. Related Skills

- turingresearch-architecture-contracts
- turingresearch-qa-release

## 8. Required Tests

- trusted allowlist tests
- unknown plugin rejection tests
- no default execution tests

## 9. Risks

- accidental execution of untrusted code
- confusing trust with installation
- unsafe permission escalation

## 10. Done Criteria

- only explicitly trusted local plugins can produce a load plan
- third-party plugins remain disabled by default
- unknown entrypoints are rejected

## 11. Non-goals

- no unknown third-party plugin execution
- no online marketplace install
- no automatic permission grant

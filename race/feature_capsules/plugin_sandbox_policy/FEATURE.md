# Plugin Sandbox Policy

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Runtime plugin loading needs a sandbox policy before any plugin can move beyond
manifest-only review.

## 2. Research Motivating Example

A local exporter plugin may need read access to generated advisor bundles, but
should not receive network, secret, remote write, or code execution permissions
without explicit review.

## 3. Inputs

- plugin manifest
- requested permissions
- extension safety policy
- trusted local status

## 4. Outputs

- PluginSandboxPolicy
- SandboxPermissionDecision
- SandboxPolicyReport

## 5. Proposed Commands / Tools

- command: `turing plugin sandbox-check`
- tool: `plugin.sandbox_check`
- output: `SandboxPolicyReport`

## 6. Related Contracts

- plugin_sandbox_policy.yaml
- extension_safety.yaml
- plugin_architecture.yaml

## 7. Related Skills

- turingresearch-architecture-contracts
- turingresearch-qa-release

## 8. Required Tests

- permission matrix tests
- forbidden permission tests
- human-review report tests

## 9. Risks

- policy describes safety but does not enforce it
- permission escalation
- hidden live access

## 10. Done Criteria

- sandbox permissions are explicit
- forbidden permissions are blocked
- policy report requires human review

## 11. Non-goals

- no OS-level sandbox implementation in this capsule
- no secrets access
- no remote write permission by default

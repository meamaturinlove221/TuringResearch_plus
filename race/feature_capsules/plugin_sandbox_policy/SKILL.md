# Plugin Sandbox Policy Skill

Status: planning skill draft.

Use this skill for v0.7 sandbox permission planning and safety review. It does
not execute plugins or enforce OS-level isolation.

## Inputs

- plugin manifest
- requested permissions
- extension safety policy
- trusted local status

## Outputs

- PluginSandboxPolicy
- SandboxPermissionDecision
- SandboxPolicyReport

## Safety Rules

- Treat code execution as forbidden by default.
- Treat remote write as forbidden by default.
- Treat secrets access as forbidden.
- Treat raw data access as restricted and review-blocking.

## Related Contracts

- plugin_sandbox_policy.yaml
- extension_safety.yaml
- plugin_architecture.yaml

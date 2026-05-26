# Future Plugin Sandbox Roadmap

Status: planning roadmap.

The v0.7 plugin sandbox policy is a policy/report layer only. Real runtime or
OS-level sandboxing is future work and must not be implied by current reports.

## Required Milestones

1. Plugin threat model.
2. Dependency isolation.
3. Filesystem scope enforcement.
4. Network policy enforcement.
5. Plugin provenance and disable flow.

## Before Runtime Execution

Before any plugin code execution is considered, TuringResearch needs:

- explicit trusted local plugin identity;
- reviewed permission policy;
- OS/runtime sandbox design;
- dependency isolation strategy;
- no-secret enforcement;
- scoped filesystem access;
- network-disabled default;
- uninstall/disable story;
- maintainer approval.

## Non-goals

- No runtime plugin execution in the current policy layer.
- No shell access.
- No remote write.
- No secrets access.
- No automatic plugin marketplace install.

# Do Not Split Yet List

Status: active guidance.

Round: 156.

This list records modules and surfaces that should stay in the monorepo until
their APIs, docs, tests, and ownership boundaries are stronger.

## Do Not Split Yet

| Surface | Reason |
| --- | --- |
| `turingresearch-core` | It owns workspace, privacy, quality, template, and release gate semantics. Splitting it early would hollow out the flagship. |
| `turingresearch-paper` | Still experimental; section, citation, claim safety, and deep-review APIs need beta hardening. |
| `turingresearch-artifact` | Still coupled to remote adapter safety, handoff, privacy, fake/live boundaries, and compliance review. |
| `turingresearch-dashboard` | Current implementation is static/local-first; standalone packaging should wait for stable DTOs and local dashboard strategy. |
| `turingresearch-plugins` | Plugin loading is trusted-local and policy-gated, not a mature third-party ecosystem. |
| `turingresearch-experiment` | Route, hard-gate, failure, and run-status semantics are shared system language and should stay anchored in the flagship. |

## Core-Specific Warning

Do not split core simply because a facade namespace exists. The facade is an
import boundary, not an extraction boundary.

Core must stay in the main repo while:

- `turing_research_plus` remains the compatibility namespace;
- release gates depend on shared privacy/quality semantics;
- public demo and workspace flows rely on the main package;
- docs and install examples still introduce the system as a single research OS.

## Paper And Artifact Warning

Paper and artifact are promising future packages, but both need stronger public
contracts first.

Paper needs:

- stable section-ready status;
- citation safety contract;
- stronger no-final-paper boundaries;
- more independent examples.

Artifact needs:

- stable handoff/export DTOs;
- clearer adapter permission policy;
- no raw-data packaging guarantees;
- independent fake artifact replay.

## Plugin Warning

Plugin surfaces should not be split until the compatibility harness, MCP
mapping, and sandbox policy can reject unsafe manifests consistently in an
independent package.

Unknown third-party plugins must remain disabled by default.

## Dashboard Warning

Dashboard/export can become a strong public-facing package, but splitting now
would create product expectations before local-server dashboard scope and DTOs
are stable.

## Current Instruction

Keep the monorepo. Continue modularization through facade namespaces,
contracts, and import compatibility tests. Revisit repository splitting only
after the first candidate repos pass a dedicated extraction readiness gate.

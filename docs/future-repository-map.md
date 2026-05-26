# Future Repository Map

Status: planning map.

Round: 151.

This map describes a possible long-term hub-and-spoke repository ecosystem.
It is not a split plan and does not create repositories.

## Hub Repository

### `turingresearch`

Role: flagship repository.

Expected contents:

- primary README and product positioning;
- installation and quickstart;
- docs index;
- core local research OS workflow;
- public demo path;
- integration gates;
- release notes and changelog;
- links to all satellite repositories if they later exist.

Split posture: keep as the main public landing page and star focus.

## Possible Satellite Repositories

### `turingresearch-core`

Role: stable core APIs, CLI/MCP smoke surface, shared contracts, and basic local
utilities.

Split posture: late split only. Core should stay in the flagship until APIs are
stable and the main repo can still tell a complete product story.

### `turingresearch-paper`

Role: paper digest, method cards, related-work review, paper assembly, claim
gates, citation safety, and deep review.

Split posture: possible after paper writing beta has stable contracts and demo
fixtures.

### `turingresearch-artifacts`

Role: evidence ledgers, artifact audits, remote artifact metadata, handoff
bundles, privacy scans, and quality gates.

Split posture: later split because artifact workflows are tightly tied to
privacy, compliance, and release gates.

### `turingresearch-dashboard`

Role: static dashboard and future local server dashboard.

Split posture: possible after local server dashboard stabilizes with safe
defaults, docs, tests, and a static export fallback.

### `turingresearch-plugins`

Role: plugin manifests, compatibility harness, sandbox policy, public registry
draft, and demo plugin catalog.

Split posture: possible after registry metadata, sandbox policy, and review
workflow are stable. Runtime execution must remain separately gated.

### `turingresearch-vggt-case`

Role: public VGGT dogfooding case study.

Split posture: strong early candidate because it is showcase material, but only
after redaction, compliance, and claim-safety checks pass.

### `turingresearch-examples`

Role: expanded public demos and examples.

Split posture: possible early candidate once examples are demo-safe,
self-contained, and linked back to the flagship repo.

## Repository Relationship

```text
turingresearch
  - turingresearch-core
  - turingresearch-paper
  - turingresearch-artifacts
  - turingresearch-dashboard
  - turingresearch-plugins
  - turingresearch-vggt-case
  - turingresearch-examples
```

## Split Readiness Ranking

| Repository | Readiness | Reason |
| --- | --- | --- |
| `turingresearch-vggt-case` | candidate after review | Showcase value, but claim safety and redaction must be strong. |
| `turingresearch-examples` | candidate after demo refresh | Demo-only material can stand alone if fully fake and tested. |
| `turingresearch-plugins` | later | Needs registry governance and safety policy maturity. |
| `turingresearch-dashboard` | later | Needs local server dashboard stabilization. |
| `turingresearch-paper` | later | Needs paper beta contracts and citation safety. |
| `turingresearch-artifacts` | later | Needs stable privacy/compliance integration. |
| `turingresearch-core` | last | Core should not leave before the flagship is mature. |

## Map Maintenance

Update this map only during roadmap, scope-lock, or repository-strategy rounds.
Do not treat entries as promised repositories.

# Upstream Adoption Plan v1.0-v1.2

Status: planning plan.

Round: 175 upstream refresh.

This plan converts the v1.0 prelaunch upstream refresh into release-window
actions. It does not implement any feature.

## v1.0 Adoption

Adopt only documentation, safety, and release-readiness changes:

- Campaign Catalog documentation inspired by de-anthropocentric research
  routing patterns.
- MCP Config Polish for fake/live clarity, `.mcp.example.json`, and env block
  guidance.
- Scholar Pipeline public docs with clear source fallback boundaries.
- Web adapter docs that keep live Apify behavior optional.
- Pod Context Lifecycle Safety Plan and release safety note.

v1.0 must not add:

- remote execution orchestration;
- heavy PDF ingestion runtime;
- default live web/scholar network behavior;
- unknown plugin execution;
- copied upstream implementation code.

## v1.1 Candidates

Potential v1.1 work:

- Pod Lifecycle Manager;
- Context Return Verifier;
- web live mode polish;
- paper source fallback refinement;
- Campaign Router model.

These require contracts, fake/default tests, privacy gates, and explicit live
opt-in before implementation.

## v1.2 Candidates

Potential v1.2 work:

- Apify workflow templates;
- MinerU / heavy PDF fallback;
- remote execution orchestration research;
- research strategy runtime experiments.

These are heavy or live-capable surfaces. They require safety design before any
implementation.

## Decision

Do not reopen the v1.0 product scope. Use the upstream refresh to improve
prelaunch docs and safety notes only.

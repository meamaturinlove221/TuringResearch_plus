# Idea: Example Research Workflow Dashboard

## Contributor

- GitHub username: example-friend
- Display name to credit: Example Friend
- Date: 2026-05-26

## One-line Summary

Add a dashboard view that shows how an idea moves from intake to skill proposal, feature capsule, SOP, and release candidate.

## Problem

TuringResearch can generate many planning artifacts, but new contributors may not understand how a raw idea becomes an accepted project asset.

## Proposed Direction

Create a docs-only dashboard concept that visualizes the lifecycle of a community idea:

```text
idea document -> review -> feature capsule -> skill proposal -> SOP/campaign -> implementation branch -> release notes
```

## Why It Matters

This helps collaborators submit higher-quality idea documents and makes the project easier to explain during open-source review or interviews.

## Target Module

- docs / dashboard
- campaign catalog
- release / open source

## Expected Artifacts

- docs page
- dashboard view
- SOP graph
- community contribution guide

## References / Attribution

Original example created for the community intake template. No external reference.

## Risks

- Could become too broad if it tries to implement a full UI immediately.
- Should remain docs-only until reviewed.

## Non-goals

- No implementation code.
- No React dashboard in the first pass.
- No changes outside `community/`.

## Suggested Conversion Path

- docs-only example
- then SOP graph
- then dashboard feature capsule

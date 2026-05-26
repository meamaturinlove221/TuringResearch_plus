# Interview Launch Version

Status: draft.

Round: 197.

## 30 Seconds

TuringResearch Plus is a local-first Research OS. It keeps evidence, artifacts,
routes, paper review, dashboards, advisor packs, plugin safety, and privacy
gates connected. The main engineering idea is that research state should be
reviewable: planned work should not become observed evidence, demos should not
turn into claims, and extensions should be safety-gated.

## 3 Minutes

The project solves a research-ops problem: real research workflows spread
across papers, artifacts, runs, notes, dashboards, and advisor feedback. That
sprawl makes it easy to overclaim or lose track of what evidence exists.

I built TuringResearch Plus as a local-first system with explicit modules:
workspace, evidence ledger, artifact audit, route DSL, hard gates, paper
review, advisor packs, dashboard export, plugin safety, privacy scanning, and
release gates.

The hardest part was not generating more text. It was keeping boundaries
coherent: fake/live, planned/observed, review/final, plugin metadata/code
execution, public demo/private data. The codebase uses contracts, workflow
tests, mypy, privacy gates, release gates, and split-readiness checks to keep
those boundaries visible.

I dogfooded it on a VGGT-related case study, but the public case does not claim
experiment success. It shows evidence management and route discipline.

## Technical Signals

- modular monorepo with future split strategy;
- public API and namespace compatibility;
- CLI/MCP fake-live config polish;
- plugin manifest and sandbox policy;
- public demo and full regression gates;
- privacy/security launch audit;
- honest README and release notes.

## What I Would Emphasize In Q&A

- This is not simple prompt engineering; it is a contracts-and-gates workflow
  system.
- The project is local-first because research data and credentials are
  sensitive.
- Human review is a design requirement, not a missing feature.
- The future split strategy protects the flagship repo instead of scattering
  attention too early.

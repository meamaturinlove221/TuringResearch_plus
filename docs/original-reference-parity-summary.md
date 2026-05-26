# Original Reference Parity Summary

Status: v1.3 polish.

Round: 286.

TuringResearch v1.3 focuses on original reference parity: selected stable ideas
from Neocortica and yogsoth are now represented as local, review-first
workflows that can be shown, tested, and replayed in fake/default mode.

This is not a claim that TuringResearch copied every upstream feature or adopted
unsafe behavior. The project keeps the flagship monorepo, privacy-first
defaults, and human-review boundaries.

## What Is Complete

| Reference area | TuringResearch surface | Status |
| --- | --- | --- |
| Neocortica Session | preflight, context pack, fake transfer, return verifier, workflow replay, dashboard | fake/default runtime parity |
| Neocortica Scholar | paper searching, content, references, reading plan, fake/live walkthrough | fake/default tool surface parity |
| Neocortica Web | web fetching, content, cache, source metadata, optional Apify templates | fake/default tool surface parity |
| MCP / Skill | `.mcp.example.json` tool mapping and skill SOP docs | documentation-contract parity |
| yogsoth Campaign | fake execution trace and strategy routing | review surface parity |
| yogsoth Research Catalog | dashboard linking campaigns, skills, vault, stress, runbooks, advisor/release | dashboard parity |
| yogsoth Vault / Ontology | wiki export demo, edge audit, ontology runbook demo | demo parity |
| yogsoth Stress / Convergence | scenario library and decision report | review surface parity |

## What Is Deferred

- ARIS cross-model review;
- ARIS proof-checker;
- ARIS meta-optimize;
- ARIS paper-claim-audit;
- live SSH/tmux/provision by default;
- default live network behavior;
- automatic remote command execution;
- automatic experiment execution;
- automatic Evidence Ledger mutation;
- fake/demo output promotion to observed evidence.

## Fake / Live Boundary

Default mode is fake/demo:

- no API keys required;
- no provider credentials required;
- no live network required;
- no remote machine required;
- no private data required.

Live provider paths remain opt-in and must be configured privately. They are not
enabled by public demos or default tests.

## Privacy-First Boundary

Public parity material must not include:

- raw data;
- private local paths;
- credentials;
- restricted model payloads;
- confidential review notes;
- unsupported experiment claims.

## How To Review

Start with:

- `docs/reference-parity-dashboard.md`
- `docs/v1.3.0-full-original-parity-replay-report.md`
- `examples/public_demo/v1_3_original_parity_demo/README.md`
- `docs/aris-still-deferred-v1.3.md`

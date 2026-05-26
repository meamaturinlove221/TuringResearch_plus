# ARIS Still Deferred in v1.4

Status: deferred.

Round: 324.

ARIS remains a future reference for TuringResearch. v1.4 does not implement ARIS
features; it prioritizes original repo production parity for the stable
Neocortica and yogsoth-inspired surfaces.

This page is the public-facing v1.4 deferral note. The detailed scope-lock note
is `docs/v1.4.0-aris-still-deferred.md`.

## Not Implemented

- ARIS runtime.
- Cross-model review.
- Proof-checker.
- Meta-optimize.
- Paper-claim-audit.
- Automated sleep research loop.
- Session stop hook.
- Autonomous paper writing or resubmission machinery.

## Why It Remains Deferred

- v1.4 production parity is about making stable original repo workflows
  runnable, reviewable, dashboarded, and regression-tested.
- ARIS-style review loops need a separate safety and evidence model before
  they can be represented honestly.
- TuringResearch should not present model review, proof checking, or claim
  audit as available until those surfaces have explicit scope, tests, and human
  review gates.

## Re-entry Conditions

ARIS can return only through a future scope lock that explicitly chooses a
study or fake prototype lane. Any such lane must preserve:

- no automatic experiment execution;
- no automatic Evidence Ledger mutation;
- no fake/demo result promotion;
- no default live network;
- human review required.

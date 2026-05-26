# ARIS Still Deferred in v1.3

Status: deferred.

Round: 286.

ARIS remains valuable as a future reference, but it is not part of the v1.3
implementation line.

## Deferred Features

v1.3 does not implement:

- ARIS cross-model review;
- ARIS proof-checker;
- ARIS meta-optimize;
- ARIS paper-claim-audit;
- ARIS session stop hook;
- automated sleep research loop;
- ARIS paper-writing automation;
- model review replacing human review.

## Why It Stays Deferred

v1.3 is about making original reference parity runnable, inspectable, and safe
in fake/default mode. ARIS features would add a new review/runtime layer with
larger correctness and safety questions. They need a separate study track,
design review, and regression gate.

## Allowed Use

Allowed:

- reference-only discussion;
- future study roadmap;
- risk matrix;
- small fake prototype planning after a new scope lock.

Not allowed:

- production runtime;
- automatic review loop;
- correctness proof claims;
- autonomous paper-claim audit;
- session lifecycle hooks with side effects.

## Required Wording

Use:

- future reference;
- deferred;
- study only;
- not v1.3 implementation;
- requires design and safety review.

Do not use:

- implemented;
- enabled;
- production;
- runtime available;
- replaces human review.

# Original Repo Replication - Interview Version

Status: interview narrative.

Round: 330.

## 30-Second Version

I replicated the stable parts of the reference repos first: session runtime
packaging, Scholar/Web tool surfaces, campaign routing, vault/wiki exports,
ontology SOPs, stress tests, convergence reports, and safe experiment runbooks.
Then I made them production-like in the fake/default lane with CLI paths, E2E
tests, dashboards, privacy gates, release contracts, and handoff docs. I
deferred ARIS because cross-model review and claim auditing are higher-risk
automation features that need a separate safety model.

## What Was Replicated

- Neocortica-Session: preflight, context pack, transfer guard, return verifier,
  CLI, script export, archive safety, dry-run plan, human confirmation, E2E.
- Neocortica-Scholar: tool list, paper content/reference/reading, fake/live
  walkthrough, Keshav three-pass reading, optional heavy backend slot.
- Neocortica-Web: fetch/content/cache/metadata surfaces, URL normalization,
  cache manifest, content fixtures, Apify fake/live report.
- yogsoth-ai: campaign trace, Research Catalog, Vault Wiki, Ontology, Stress /
  Convergence, Experiment Runbook E2E.

## What We Added Beyond Replication

- Privacy/security gates.
- Release contracts.
- Full regression.
- Human confirmation before evidence import.
- Dashboard v2.
- Final archive and handoff docs.
- Explicit planned/observed boundary.

## Why Not ARIS Yet

ARIS is interesting, but it is a different class of system. It implies model
review loops, proof checking, claim auditing, and meta-optimization. Shipping
that before the stable operational surfaces were production-ready would make
the project look more advanced while making it less trustworthy.

The engineering decision was: first make the stable workflows runnable and
auditable; then consider ARIS as a later study track.

## Interview Talking Points

- I used parity as a way to avoid premature invention.
- I separated structural parity from runtime parity and production parity.
- I made fake/default workflows runnable before touching live integrations.
- I added gates for privacy, release, and claim safety.
- I explicitly deferred impressive but risky features.
- I can explain what works, what is fake, what is live-opt-in, and what is not
  implemented.

## Best One-Liner

This project shows engineering judgment: I did not just add features; I turned
borrowed stable ideas into tested, reviewable, privacy-safe workflows and knew
when to defer the flashy automation layer.

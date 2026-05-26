# Original Repo Replication Scorecard

Status: v1.4 scorecard.

Round: 330.

## Scorecard

| Area | Structural parity | Runtime parity | Production parity | Notes |
| --- | --- | --- | --- | --- |
| Neocortica Session | complete | complete | complete with deferred live gaps | CLI, context pack, script export, archive hardening, dry-run plan, return confirmation, E2E, dashboard |
| Neocortica Scholar | complete | complete | complete fake/default | tool list, paper content/reference/reading E2E, optional backend slot |
| Neocortica Web | complete | complete | complete fake/default | URL normalization, cache manifest, fixtures, Apify fake/live report |
| yogsoth-ai | complete | complete | complete with review | campaign/catalog/vault/ontology/stress/convergence/experiment E2E |
| ARIS | deferred | deferred | deferred | future study only, maybe v1.6 |

## What TuringResearch Adds

| Added layer | Status | Why it matters |
| --- | --- | --- |
| privacy/security gates | complete | prevents secrets, private paths, raw data, restricted payloads |
| release contracts | complete | keeps release docs, tests, and boundaries coherent |
| full regression | complete | catches drift across old and new parity surfaces |
| handoff archive | complete | makes next human actions explicit |
| dashboard v2 | complete | shows structural/runtime/production/deferred state clearly |
| human confirmation | complete | prevents return artifacts from becoming evidence automatically |

## Deferred / Rejected

| Feature | Status | Reason |
| --- | --- | --- |
| ARIS runtime | deferred | different risk class; needs separate study scope |
| cross-model review | deferred | false-authority risk |
| proof-checker | deferred | requires dedicated correctness model |
| meta-optimize | deferred | not needed for original repo production parity |
| paper-claim-audit | deferred | should not blur into automated paper authority |
| default live SSH/SFTP | rejected by default | private opt-in only |
| remote command execution | rejected by default | safety boundary |
| automatic experiment execution | rejected | review-only runbooks |
| fake/demo result promotion | rejected | planned/observed boundary |

## Overall Result

Decision: `production parity ready for human review`.

This is not a live provider proof, remote execution proof, autonomous research
runtime, or experiment success claim.

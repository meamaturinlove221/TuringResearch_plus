# ARIS Feature Backlog

Status: deferred backlog.

Round: 233.

Every item in this backlog is:

- `deferred`;
- `requires design`;
- `requires safety review`;
- `not v1.2`.

| Feature | Status | Requires design | Requires safety review | v1.2 status | Primary risk | Earliest target |
| --- | --- | --- | --- | --- | --- | --- |
| cross-model review loop | deferred | true | true | not v1.2 | false authority, agent-runtime overreach | v1.3 study |
| claim audit | deferred | true | true | not v1.2 | confusing review aid with proof | v1.3 study |
| result-to-claim verification | deferred | true | true | not v1.2 | missing results inferred as evidence | v1.3 study |
| experiment audit | deferred | true | true | not v1.2 | automatic experiment-success implication | v1.3 study |
| proof checker | deferred | true | true | not v1.2 | overstated correctness | v1.3 study |
| paper compile audit | deferred | true | true | not v1.2 | final-paper automation drift | v1.3 study |
| meta-optimize | deferred | true | true | not v1.2 | opaque behavior tuning | v1.3 study |
| effort levels | deferred | true | true | not v1.2 | hidden budget/quality assumptions | v1.3 study |
| session stop hook | deferred | true | true | not v1.2 | lifecycle side effects and state mutation | v1.3 study |
| paper resubmit pipeline | deferred | true | true | not v1.2 | paper automation and claim overreach | v1.3 study |

## Backlog Rules

- Do not implement backlog items during v1.2.
- Do not add runtime code for backlog items without a later scope lock.
- Do not add public claims that backlog items exist today.
- Do not use backlog items to bypass human review.
- Do not promote fake/demo outputs to observed evidence.

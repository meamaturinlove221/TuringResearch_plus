# yogsoth Parity Remaining Gaps

Status: tracked.

Round: 249.

## Intentional Gaps

| Gap | Status | Reason |
| --- | --- | --- |
| Autonomous agent runtime | rejected | Would overreach TuringResearch's local-first review model. |
| Default live networking | rejected | Conflicts with fake/default and privacy-first policy. |
| Automatic experiment execution | rejected | Real experiments require human approval and external execution. |
| Automatic Evidence Ledger mutation | rejected | Proposed updates require review before promotion. |
| OS-level plugin sandbox | deferred | Requires separate design and threat modeling. |
| Public plugin marketplace | deferred | Needs ecosystem demand and review capacity. |
| ARIS features | deferred | v1.3+ study item, not v1.2 parity. |
| Upstream strict diff specificity | partial | Last scan created a baseline but could not resolve repositories due rate limit. |
| Live provider polish | deferred | Optional and disabled by default. |

## Residual Risks

- Users may overread review reports as execution results unless docs remain
  explicit.
- Deterministic stress checks are useful gates, but not a substitute for domain
  expert review.
- Research Catalog integration can drift if future features are added without
  updating routing and skill maps.

## Next Actions

- Keep v1.2 parity docs synchronized with implementation.
- Run full parity regression before any v1.2 release candidate.
- Refresh upstream strict diff in an explicit upstream scan round.
- Keep ARIS study out of v1.2 implementation work.

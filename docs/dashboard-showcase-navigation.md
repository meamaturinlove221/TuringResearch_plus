# Dashboard Showcase Navigation

Status: navigation scope locked.

Round: 350.

The v1.5 dashboard showcase should use a simple visitor path:

1. Landing
2. Original Repo Parity
3. Session Runtime
4. Scholar/Web
5. Research Catalog
6. Stress/Convergence
7. Split Repos
8. Security/Privacy
9. Interview Demo

## Navigation Model

| Order | Page | Primary question answered |
| --- | --- | --- |
| 1 | Landing | What is TuringResearch? |
| 2 | Original Repo Parity | What has been replicated from the reference repos? |
| 3 | Session Runtime | How does the local fake/default Session workflow run? |
| 4 | Scholar/Web | How are paper and web surfaces demonstrated safely? |
| 5 | Research Catalog | How do campaigns, skills, vault, stress, and runbooks connect? |
| 6 | Stress/Convergence | How are weak claims and route choices reviewed? |
| 7 | Split Repos | Which child repos are manual-ready, and what is not published? |
| 8 | Security/Privacy | Why is the showcase safe to inspect publicly? |
| 9 | Interview Demo | How should a human explain the project briefly? |

## Page-Level Requirements

Every showcase page should identify:

- status;
- data source or source document;
- fake/default versus optional live boundary;
- deferred or manual-only items;
- human review requirement;
- no automatic Evidence Ledger mutation.

## Navigation Constraints

- Do not add a fake public deployment URL.
- Do not imply that split repos already exist.
- Do not imply that live providers have been run.
- Do not imply that ARIS is implemented.
- Do not add analytics or tracking.
- Do not expose private local paths.

## Implementation Note

This navigation can later be reflected in `docs-site/nav.yaml` or a static
showcase page, but Round 350 does not make that UI change.

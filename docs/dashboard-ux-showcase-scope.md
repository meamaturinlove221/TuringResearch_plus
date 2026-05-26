# Dashboard UX Showcase Scope

Status: scope locked.

Round: 350.

v1.5 will present TuringResearch dashboards as a public showcase sequence. This
round only defines the showcase scope and navigation. It does not rebuild the UI,
add a live dashboard server, deploy a public site, or change core runtime
behavior.

## Goal

Make the dashboard story understandable to an external visitor:

1. what the project is;
2. what original repo parity means;
3. how the fake/default workflows run;
4. what research catalog surfaces exist;
5. how stress and convergence reviews work;
6. what split repos are prepared for;
7. where security and privacy boundaries sit;
8. how to explain the project in an interview.

## Showcase Pages

| Page | Purpose | Source evidence |
| --- | --- | --- |
| Landing | orient visitors to the local-first Research OS | `docs/public-showcase.md` |
| Original Repo Parity | show structural, runtime, production, and deferred status | `docs/original-repo-parity-dashboard-v2.md` |
| Session Runtime | show runnable fake/default Session production parity | `docs/session-production-dashboard-v2.md` |
| Scholar/Web | show production parity for paper and web surfaces | `docs/v1.4.0-scholar-web-production-summary.md` |
| Research Catalog | show campaigns, skills, vault, stress, and runbooks | `docs/research-catalog-dashboard.md` |
| Stress/Convergence | show review scenarios and decision reports | `docs/stress-convergence-e2e.md` |
| Split Repos | show manual-ready split packs without fake URLs | `docs/v1.5.0-split-sprint-gate-report.md` |
| Security/Privacy | show no-secrets, no-raw-data, fake/default boundaries | `docs/v1.4.0-security-audit.md` |
| Interview Demo | show concise talking points for demos and interviews | `docs/original-repo-replication-interview-version.md` |

## UX Principles

- Lead with an overview, not a dense matrix.
- Keep dashboards read-only and review-oriented.
- Label fake/default, optional live, deferred, and manual-only surfaces clearly.
- Prefer short tables and status blocks over long prose.
- Keep public pages free of private paths, credentials, raw data, and fake URLs.
- Do not present planned, fake, demo, or live-review context as observed
  evidence.

## Deliverable Boundary

Round 350 creates a scope lock only. Later v1.5 dashboard rounds may create or
polish pages, but this round only defines the target navigation and limits.

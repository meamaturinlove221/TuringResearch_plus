# Future UI Dashboard

Status: future planning.

Round: 102.

The current dashboard is static HTML / Markdown. Future dashboard work should
stay local-first until the research workflow, privacy rules, and release
boundaries are stable.

## Current Baseline

v0.5 alpha provides:

- lightweight static dashboard UI;
- Modal run dashboard in Markdown;
- run comparison reports;
- public demo dashboard;
- VGGT replay dashboard inputs;
- advisor export source packages.

These dashboards are review surfaces. They do not run experiments and do not
create new evidence.

## Future Dashboard Directions

| Direction | Horizon | Purpose |
| --- | --- | --- |
| Static dashboard polish | near-term | Better section rendering and navigation. |
| Multi-project dashboard | near-term | Compare project state, evidence, blockers, and advisor readiness. |
| Run comparison board | near-term | Compare run status and artifact completeness. |
| Advisor view | mid-term | Package concise review updates. |
| Plugin capability view | mid-term | Show installed capabilities and safety levels. |
| Live dashboard server | long-term | Optional local server, not SaaS by default. |

## Dashboard Data Model Needs

- Project summary.
- Evidence status.
- Artifact completeness.
- Visual readiness.
- Run status.
- Related-work status.
- Failure taxonomy.
- Advisor next actions.
- Privacy and release gates.
- Capability manifest.

## Privacy / Data Risks

- Dashboard pages can expose private paths or project names.
- Screenshots can leak raw data or private model references.
- Multi-project dashboards can accidentally mix evidence.
- Polished UI can make uncertain results look final.

## Human Review Required

- Public dashboard exports.
- Advisor dashboard snapshots.
- Any dashboard that includes live/retrieved artifacts.
- Any dashboard used as release material.

## Non-Goals

- No full SaaS UI by default.
- No user account system.
- No automatic remote execution.
- No dashboard-generated experiment conclusions.
- No hidden upload of artifacts.

# Case Study Maintenance

Status: planning policy.

Round: 150.

Case studies are public-facing evidence narratives. They must be maintained
with the same care as release notes, public demos, and compliance reports.

## Case Study Types

| Type | Allowed content | Required label |
| --- | --- | --- |
| Demo case study | Synthetic or fake project material. | demo only |
| Dogfooding case study | Internal workflow narrative with redaction and claim guards. | dogfooding case |
| Evidence-backed public case study | Reviewed artifacts and evidence ledger support. | evidence reviewed |

## Update Policy

Update a case study only when at least one of these is true:

- new reviewed artifact or evidence is available;
- redaction policy changes;
- compliance findings change;
- claim safety report changes;
- public demo structure changes;
- release docs need a case-study reference refresh.

## Required Review Artifacts

- Case study draft.
- Redaction report.
- Claim safety report.
- Privacy scan or public release hygiene check.
- Compliance report when datasets, models, papers, code, or figures are
  discussed.
- Human-review notes for any real project claim.

## VGGT Case Study Update Policy

- Keep VGGT labeled as a dogfooding case unless real public-safe evidence
  supports stronger claims.
- Do not include private local paths.
- Do not include raw data or licensed model payloads.
- Do not include advisor-private feedback.
- Do not claim SparseConv3D success unless real evidence supports it.
- Keep failures, blockers, and what remains human work visible.

## Claim Rules

- Planned experiments must stay planned.
- Missing evidence must stay missing.
- Demo evidence must not become observed.
- Unsupported experiment success must be blocked.
- Case studies may describe what TuringResearch helped organize, but not claim
  the underlying research succeeded unless evidence supports it.

## Public Demo Refresh

Public demo case studies should be refreshed when:

- templates change;
- dashboard outputs change;
- privacy scan rules change;
- public demo workspace structure changes;
- case-study builder output changes.

## Archive Policy

Archive or mark a case study stale when:

- source docs are outdated;
- compliance status is unknown;
- evidence references no longer resolve;
- the project changed direction;
- the case study cannot pass privacy and claim-safety checks.

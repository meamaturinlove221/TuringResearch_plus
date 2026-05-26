# From VGGT Case Study to General Research Template

Status: planning.

Round: 102.

The VGGT / SMPL-X Human Prior line is the reference case study for
TuringResearch Plus. v0.6 should extract reusable project structure from that
case without turning VGGT-specific assumptions into universal defaults.

## What VGGT Proved as a Template Seed

The VGGT case exercised most of the research operating loop:

- research intent and north star;
- evidence ledger;
- artifact and visual audits;
- experiment route specs and hard gates;
- run ingest and failure taxonomy;
- related-work positioning and paper digest;
- vault graph and ontology notes;
- advisor pack and dashboard;
- dogfooding replay and public/demo boundaries.

The case did not prove experiment success. SparseConv3D success remains
unsupported unless future evidence provides real backend logs, predictions or
thin summaries, visual boards, manifests, and cleanup reports.

## Generalizable Components

| VGGT component | General project template equivalent |
| --- | --- |
| North star | `docs/north_star.md` |
| Evidence ledger | `docs/evidence_ledger.md` |
| Artifact audit | `docs/artifact_plan.md` |
| Visual readiness | `docs/visual_evidence.md` |
| Modal route pack | `docs/experiment_routes.md` |
| Hard gates | `docs/hard_gates.md` |
| Failure taxonomy | `docs/failure_taxonomy.md` |
| Paper method cards | `docs/related_work.md` and `docs/paper_digest.md` |
| Vault graph | `docs/knowledge_graph.md` |
| Advisor pack | `docs/advisor_pack.md` |
| Dashboard | `dashboard/index.html` or `dashboard.md` |

## VGGT-specific Components

These should stay domain-specific:

- SMPL-X feature encoding.
- VGGT token integration.
- SparseConv3D backend route.
- Human body reconstruction failure modes.
- Hairline regression and hand-object confusion.
- NeuralBody, HumanRAM, HART, VGGT-HPE, HGGT, and Fus3D positioning.

## Template Rules

- Templates start with planned or empty evidence, never observed evidence.
- Templates can include example sections, but not domain claims.
- Project-specific safety policies must be filled in by humans.
- Private paths, raw data, model files, and API keys must stay out of templates.
- Related work starts as a review scaffold, not a complete literature review.

## v0.6 Generalization Path

1. Stabilize the current project template generator.
2. Add workspace registry support for multiple projects.
3. Add project-level privacy and license policies.
4. Add cross-project graph export for reusable patterns only.
5. Add dashboards that compare status, not truth.
6. Keep every cross-project recommendation marked review-required.

## Human Review Required

- Domain-specific method mappings.
- Any claim that a route improved results.
- Any transfer of evidence or hard gates between projects.
- Any public case study wording.
- Any release of project artifacts.

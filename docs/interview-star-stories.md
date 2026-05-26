# Interview STAR Stories

Status: portfolio draft.

Round: 158.

## STAR 1: Keeping Research Claims Honest

Situation: research project state was scattered across notes, artifacts, route
plans, and paper drafts.

Task: build a system that makes claim status visible without pretending to
complete research automatically.

Action: created evidence ledgers, artifact audits, route DSL, failure taxonomy,
paper scaffold, quality gates, and fake/live boundaries.

Result: project status became reviewable. Missing evidence and unsafe claims
stay visible instead of becoming polished but unsupported text.

## STAR 2: VGGT Dogfooding Without Overclaiming

Situation: VGGT human-prior workflow exploration needed a way to organize
routes, failures, evidence, advisor communication, and public-safe summaries.

Task: turn dogfooding material into structured case-study outputs without
leaking private paths or claiming experiment success.

Action: built dogfooding replay, paper scaffold, dashboard, compliance report,
case-study redaction, and claim safety report.

Result: the case became a public-reviewable story about process and tooling,
not a fake success claim. SparseConv3D success is not claimed.

## STAR 3: Safe Plugin Architecture

Situation: a research OS needs extension points, but executing unknown plugins
is risky.

Task: design a plugin system that documents capabilities before enabling
runtime execution.

Action: implemented manifests, registry, MCP mapping, capability catalog,
trusted local loading, sandbox policy, and compatibility harness.

Result: plugin metadata can be reviewed and tested without executing unknown
third-party code.

## STAR 4: Monorepo To Modular Architecture

Situation: the project grew across evidence, artifacts, paper, dashboard,
plugins, cases, and release gates.

Task: prepare for future split without breaking current imports or hollowing
out the flagship repo.

Action: added public API contracts, namespace facades, compatibility alias
registry, and module split readiness gates.

Result: the project has clearer module boundaries while preserving a complete
main repo and stable compatibility path.

## STAR 5: Public Release Hardening

Situation: public demos and case studies can accidentally leak raw data,
private paths, model files, or unsupported claims.

Task: build a release process that catches those issues before public release.

Action: added privacy gates, public demo policy, compliance assistant, secret
scan reports, quality gates, and public RC checks.

Result: public-facing material can be prepared with explicit safety reports and
human review gates.

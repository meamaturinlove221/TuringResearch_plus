# Interview Technical Highlights

Status: portfolio draft.

Round: 158.

## 1. Evidence-First Design

The Evidence Ledger prevents a project from silently converting plans into
results. Claims need status, source, and review boundaries.

## 2. Artifact Auditor

The artifact layer checks whether outputs exist, whether they are safe to
share, and whether they are complete enough to support downstream claims.

## 3. Route DSL And Failure Taxonomy

Experiment routes are represented as reviewable specs with hard gates and
failure modes. This makes blocked experiments useful instead of invisible.

## 4. Paper Intelligence Without Overclaiming

Paper tools build digest, method-card, related-work, method-section, and
experiment-section skeletons. They do not write final results or conclusions.

## 5. Dashboard And Advisor Pack

The dashboard and advisor pack make project status easy to inspect:

- evidence status;
- artifact readiness;
- visual readiness;
- route status;
- failures and blockers;
- next actions.

## 6. Plugin Safety

The plugin system starts with manifests, compatibility checks, and sandbox
policy before executing any third-party code. Unknown plugins stay disabled by
default.

## 7. Fake/Live Boundary

Default workflows use fake/demo fixtures. Live adapters are optional and must
be explicitly enabled.

## 8. Privacy And Compliance

Privacy scan and compliance reports check for secrets, raw data, model payloads,
license risk, private paths, and public-demo safety. They are review aids, not
legal advice.

## 9. Testing And Contracts

The project uses layered verification:

- unit tests;
- workflow tests;
- contract tests;
- import compatibility tests;
- privacy and hygiene gates;
- replay and regression gates;
- mypy and ruff.

## 10. Modular Evolution

The project keeps a complete flagship monorepo while adding facade namespaces
and public API contracts. It avoids splitting repos before APIs, docs, demos,
and tests are ready.

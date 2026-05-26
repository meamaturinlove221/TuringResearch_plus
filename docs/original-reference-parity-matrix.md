# Original Reference Parity Matrix

Status: planning matrix.

Round: 232.

This matrix compares the original reference repositories with the current
TuringResearch implementation plan. It is a planning artifact only. It does not
copy upstream code, implement features, perform live scans, create child
repositories, or mark planned work as observed.

## Status Legend

- `implemented`: local equivalent exists with docs and tests.
- `partial`: local equivalent exists but needs parity hardening.
- `missing`: no meaningful equivalent yet.
- `deferred`: useful, but intentionally moved later.
- `rejected`: not appropriate for the current product boundary.

## Combined Matrix

| Upstream repo | Upstream module / feature | Upstream purpose | Current TuringResearch equivalent | Status | Implementation priority | Risk | Test requirement | Docs requirement | Target round |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Pthahnix/Neocortica-Session` | Git context transfer | durable context handoff between local and pod-like environments | Pod Context Lifecycle Safety, Git handoff docs | partial | P0 | remote execution confusion | pod lifecycle fake workflow, handoff safety tests | transfer/return policy docs | R234-R235 tentative |
| `Pthahnix/Neocortica-Session` | Pod workflow / launch modules | prepare, provision, transfer, launch, and return context | pod lifecycle models and safety reports only | partial | P0 | accidental SSH/Modal/tmux scope | preflight, transfer policy, return verifier tests | remote execution non-goals | R234-R235 tentative |
| `Pthahnix/Neocortica-Session` | Return metadata handling | verify pod return status and artifacts | return verifier and proposed updates policy | partial | P0 | unreviewed evidence writes | return manifest validation tests | return verification docs | R235 tentative |
| `Pthahnix/Neocortica-Scholar` | MCP config pattern | safe server config and env block | `.mcp.example.json`, MCP config docs | partial | P0 | accidental key leakage | MCP config contract tests | MCP config parity docs | R235-R236 tentative |
| `Pthahnix/Neocortica-Scholar` | paper pipeline / fallback | retrieve and structure paper sources | scholar pipeline refinement, fake adapters | partial | P1 | default networking or heavy PDF dependency | scholar fake pipeline tests | scholar source fallback docs | R235-R236 tentative |
| `Pthahnix/Neocortica-Scholar` | MinerU / heavy PDF fallback | fallback paper ingestion from PDFs | research-only planning | deferred | P3 | dependency/licensing/copyright risk | no default runtime tests; planning gate only | heavy PDF fallback roadmap | v1.3+ |
| `Pthahnix/Neocortica-Web` | `web_fetching` / `web_content` | public web retrieval and content extraction | web fetch adapter, web content cache | partial | P1 | default networking or restricted fetch | fake web fetch tests, live skipped | web adapter parity docs | R236-R237 tentative |
| `Pthahnix/Neocortica-Web` | Apify REST integration | optional richer web workflow backend | Apify fake/live adapter docs | partial | P2 | token/cost/live execution risk | fake Apify tests, live opt-in only | Apify template docs | R236-R237/v1.3 tentative |
| `yogsoth-ai/de-anthropocentric-research-engine` | campaign routing / strategy book | route research tasks through strategy campaigns | Campaign Catalog and deterministic router | implemented | P0 | agent runtime overreach | campaign catalog/router tests | campaign catalog docs | R237-R238 gate |
| `yogsoth-ai/knowledge-structuring` | research catalog | organize research knowledge into reusable structures | campaign catalog, case gallery, docs index | partial | P1 | taxonomy drift | catalog/gallery/docs tests | parity matrix and catalog docs | R237-R239 tentative |
| `yogsoth-ai/wiki-vault` | wiki/vault | persistent local knowledge vault | vault graph enhancement, ontology SOPs | partial | P1 | graph truth overclaim | vault graph/audit tests | vault/ontology parity docs | R237-R239 tentative |
| `yogsoth-ai/knowledge-structuring` | ontology | concept/edge/hierarchy maintenance | Ontology SOPs | implemented | P1 | automatic truth inference | ontology SOP tests | ontology SOP docs | R237-R239 tentative |
| `yogsoth-ai/convergence` | convergence | compare and rank strategies | convergence service and campaign map | partial | P2 | recommendation overclaim | convergence unit tests, campaign routing tests | convergence parity note | R238-R239 tentative |
| `yogsoth-ai/stress-test` | stress-test | challenge plans, claims, and release posture | claim guards, release gates, regression gates | partial | P1 | fake result or overclaim missed | claim guard/regression tests | stress-test parity docs | R238-R239 tentative |
| `yogsoth-ai/experiment-execution` | experiment execution planning | route experiments and hard gates | route DSL, hard gates, failure taxonomy | partial | P1 | automatic real execution scope | route/failure/hard gate tests | experiment parity docs | R238-R239 tentative |
| ARIS future reference | cross-model review loop | multiple model critique/review loop | none in v1.2 | deferred | v1.3 study | agent runtime overreach | roadmap-only gate | v1.3 ARIS study roadmap | v1.3+ |
| ARIS future reference | meta-optimize | optimize strategies across iterations | none in v1.2 | deferred | v1.3 study | opaque optimization and unreviewed claims | roadmap-only gate | v1.3 ARIS study roadmap | v1.3+ |
| ARIS future reference | proof-checker | formal or semi-formal claim checking | claim guards only, not proof checking | deferred | v1.3 study | false proof confidence | roadmap-only gate | v1.3 ARIS study roadmap | v1.3+ |
| ARIS future reference | paper-writing automation | automate paper writing loop | review-only paper beta | rejected for v1.2 | none | final paper overclaim | non-goal gate | non-goals final | not v1.2 |

## v1.2 Target Interpretation

The v1.2 target is not complete feature parity with every upstream experiment.
It is stable parity with the original reference concepts that fit
TuringResearch's local-first, fake/default, human-review boundaries.

## Immediate Gaps

- Round 234 created the first strict machine baseline, but all configured
  upstream targets were unresolved due to public metadata rate limiting.
- No added, modified, or deleted upstream file claim exists yet.
- Target rounds above are tentative execution windows and remain blocked on a
  future resolved baseline/diff before any upstream-change-specific claim can
  be made.
- Neocortica-Session parity needs a stricter matrix and local lifecycle gate.
- Neocortica-Scholar parity needs MCP/source fallback parity docs and tests.
- Neocortica-Web parity needs optional web/live and Apify template boundaries.
- yogsoth parity needs campaign/vault/ontology/stress/experiment execution
  gate reports.
- ARIS belongs in a future study roadmap, not v1.2 implementation.

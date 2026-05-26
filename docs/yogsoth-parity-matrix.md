# yogsoth-ai Parity Matrix

Status: planning matrix.

Round: 232.

This matrix covers the yogsoth-ai stable ideas that fit TuringResearch v1.2:
campaign routing, research catalog, skill routing, wiki/vault, ontology,
convergence, stress-test, and experiment-execution. It does not import a new
agent runtime.

## Matrix

| Upstream repo | Upstream module / feature | Upstream purpose | Current TuringResearch equivalent | Status | Implementation priority | Risk | Test requirement | Docs requirement | Target round |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `yogsoth-ai/de-anthropocentric-research-engine` | campaign routing | route research work through campaigns and preconditions | Campaign Catalog and deterministic router | implemented | P0 | replacing orchestrator | campaign router tests | campaign catalog doc | R237-R238 gate |
| `yogsoth-ai/de-anthropocentric-research-engine` | strategy book | reusable research strategy patterns | Campaign Catalog docs | implemented | P0 | strategy overclaim | catalog tests | campaign catalog doc | R237-R238 gate |
| `yogsoth-ai/knowledge-structuring` | research catalog | organize reusable research knowledge | docs index, case gallery, campaign catalog | partial | P1 | catalog drift | docs/gallery tests | research catalog parity doc | R237-R239 tentative |
| `yogsoth-ai/knowledge-acquisition` | skill routing | direct tasks to specialist skills | skill entry routing and campaign-to-skill map | partial | P1 | wrong skill handoff | skill routing integrity tests | skill SOP parity doc | R237-R239 tentative |
| `yogsoth-ai/wiki-vault` | wiki/vault | persistent local knowledge structure | Vault Graph Enhancement | partial | P1 | graph truth overclaim | vault graph/audit tests | vault parity doc | R237-R239 tentative |
| `yogsoth-ai/knowledge-structuring` | ontology | maintain concepts, aliases, hierarchy, edges | Ontology SOPs | implemented | P1 | automatic truth inference | ontology SOP tests | ontology SOP docs | R237-R239 tentative |
| `yogsoth-ai/convergence` | convergence | compare options and decide next actions | convergence services and scoring | partial | P2 | ranking overclaim | convergence tests | convergence parity doc | R238-R239 tentative |
| `yogsoth-ai/stress-test` | stress-test | challenge claims and plans | claim guards, release gates, risk registers | partial | P1 | weak overclaim detection | claim/stress/regression tests | stress-test parity doc | R238-R239 tentative |
| `yogsoth-ai/experiment-execution` | experiment-execution | plan experiments and execution routes | route DSL, hard gates, failure taxonomy | partial | P1 | automatic real execution | route/failure tests | experiment parity doc | R238-R239 tentative |
| `yogsoth-ai/literature-engine` | literature workflow | structure paper/survey work | paper digest, related work, paper beta | partial | P2 | paper automation overreach | paper beta and citation tests | paper workflow parity doc | R238-R239 tentative |
| `yogsoth-ai/semantic-scholar-mcp` | scholar MCP | scholar tool config and lookup | semantic scholar fake/live adapters and MCP docs | partial | P1 | default live networking | MCP/scholar tests | scholar MCP parity doc | R235-R236 tentative |
| `yogsoth-ai/web-browsing` | web browsing | structured public web retrieval | web fetch / content adapter | partial | P1 | restricted content fetch | fake web tests | web parity doc | R236-R237 tentative |

## v1.2 Interpretation

The v1.2 goal is stable conceptual parity:

- campaign and precondition clarity;
- vault/ontology review discipline;
- stress-test and experiment-planning continuity;
- skill SOP handoff clarity.

The v1.2 goal is not autonomous campaign execution, cross-agent spawning, or
automatic research strategy optimization.

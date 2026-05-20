# TulingResearch Plus Reuse Boundary

Round 4 uses public Yogsoth AI repositories only as references for architecture and workflow design.

## Allowed Reuse

- Architecture patterns such as Campaign -> Strategy -> Tactic -> SOP.
- Workflow patterns such as strategy-book execution, backtracking, budget floors, saturation detection, and context checkpoints.
- Contract ideas such as typed graph edges, evidence gates, quality gates, and result artifacts.
- Data-model concepts such as `ResearchBrief`, `SurveyPlan`, `HypothesisCandidate`, `VaultEdge`, and `ExperimentReport`.
- Testing strategies such as fake-service runs, mocked adapters, dry-run workflow tests, and contract tests.

## Not Allowed

- Copying source code from external repositories without explicit license review.
- Copying prompt text, skill files, or repository-specific instructions verbatim.
- Importing external project names into TulingResearch Plus package names, server names, tool names, skill names, or document titles.
- Reusing external MCP runtime assumptions as direct dependencies.
- Writing real network code in unit or workflow tests.
- Creating external-reference-derived package or directory names, or naming this project after a reference project.

## License Rule

Even when a public repository appears permissively licensed, TulingResearch Plus treats Round 4 as design-only. Any future code reuse requires file-level license verification and an explicit record in the relevant lane ledger before copying or adapting code.

## Naming Rule

All TulingResearch Plus implementation names must use:

- Core package: `tuling_research`
- Plus package: `tuling_research_plus`
- MCP server: `tulingresearch-plus`
- Skill prefix: `tulingresearch-`

External names may appear only in reference citations, audit notes, or source links.

## Adapter Rule

Any idea involving Semantic Scholar, web search, scraping, paper APIs, or other external services must become a service protocol and adapter boundary. Network behavior must be mocked in tests. Workflow dry-run and fake-service modes are mandatory.

## Evidence Rule

All important TulingResearch Plus outputs become `ResearchArtifact`. Any conclusion must include `EvidenceRef`. Race Mode outputs must pass Source Hygiene Gate before becoming implementation work.

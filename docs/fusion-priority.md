# TulingResearch Plus Fusion Priority

Round 4 priority is based on dependency order, safety, testability, and how much of the later workflow stack depends on the module.

## P0: Foundations

| Module | Why P0 | First contract focus |
| --- | --- | --- |
| `src/tuling_research_plus/context/` | Required for resumability, checkpoints, and workflow recovery. | `ContextCheckpoint`, `ContextIndex`, `context.checkpoint`, `context.recover` |
| `src/tuling_research_plus/subtask/` | Needed to represent strategy/tactic/SOP decomposition without spawning extra Codex windows. | `SubtaskSpec`, dependency graph validation, dry-run runtime |
| `src/tuling_research_plus/survey/` | Main evidence acquisition layer; many downstream modules depend on survey artifacts. | `SurveyPlan`, `SurveyRun`, `SurveyStatus`, `SurveyExport` |
| `src/tuling_research_plus/semantic_graph/` | Provides paper/reference/citation/author graph abstractions needed by survey and insight. | paper lookup, citation edge, author edge, graph expansion |
| `src/tuling_research_plus/vault/` | Persistent memory layer for artifacts, evidence, and typed edges. | `VaultRecord`, `VaultEdge`, lint, graph stats |

## P1: Research Formation

| Module | Why P1 | First contract focus |
| --- | --- | --- |
| `src/tuling_research_plus/north_star/` | Useful entry point once context and survey exist. | `ResearchBrief`, `NorthStar`, `GoalTree` |
| `src/tuling_research_plus/insight/` | Converts survey output into structural understanding. | gap analysis, insight artifact, boundary map |
| `src/tuling_research_plus/hypothesis/` | Produces testable hypotheses from evidence-backed gaps. | falsifiability, operationalization, research question |

## P2: Candidate Generation And Decision

| Module | Why P2 | First contract focus |
| --- | --- | --- |
| `src/tuling_research_plus/ideation/` | Generates candidate solution space after hypotheses exist. | idea candidate, diversity filter, saturation marker |
| `src/tuling_research_plus/convergence/` | Scores and ranks candidate sets. | candidate score, portfolio decision, decision audit |
| `src/tuling_research_plus/stress/` | Adversarially validates artifacts and candidate decisions. | weakness report, severity, mitigation proposal |

## P3: Execution Layer

| Module | Why P3 | First contract focus |
| --- | --- | --- |
| `src/tuling_research_plus/experiment/` | Should wait until hypotheses, convergence, and stress artifacts are stable. | experiment design, constraint report, implementation plan, experiment report |

## Recommended Implementation Order

1. `context`, `subtask`, `vault`
2. `semantic_graph`, `survey`
3. `north_star`, `insight`, `hypothesis`
4. `ideation`, `convergence`, `stress`
5. `experiment`

Each step should follow: contracts -> Pydantic models -> fake-service implementation -> contract tests -> workflow tests.

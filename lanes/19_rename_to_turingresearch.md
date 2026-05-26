# Lane 19: Rename To TuringResearch

## Scope

Round 38.5 performs the post-Round38 global rename from the prior incorrect
project naming system to the corrected TuringResearch naming system.

## Renamed Surfaces

- Project display name: TuringResearch Plus
- Repository root reference: `TuringResearch/TuringResearch_plus`
- Core package: `turing_research`
- Plus package: `turing_research_plus`
- MCP server: `turingresearch-plus`
- Skill prefix: `turingresearch-`

## Preserved Round 38 Features

- `src/turing_research_plus/vggt/`
- `src/turing_research_plus/artifact_audit/`
- `contracts/vggt_evidence.yaml`
- `contracts/artifact_audit.yaml`
- Round 38 unit and workflow tests under the new imports.

## Not Done

- No new feature implementation.
- No Visual Evidence Auditor implementation.
- No Advisor Pack Builder implementation.
- No PDF Phase B full extraction implementation.
- No network access.
- No VGGT local path reads.

## Validation Plan

- Name integrity tests.
- Package import tests.
- Skills integrity tests.
- Round 38 Evidence Ledger and Artifact Auditor focused tests.
- Contract tests.
- Workflow tests.

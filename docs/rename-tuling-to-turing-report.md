# TuringResearch Plus Rename Report

Status: post-Round38 global rename report.

Round 38.5 migrates the project from the old TulingResearch naming system to the
corrected TuringResearch naming system after the Round 38.1 checkpoint. This
report is one of the few allowed files that may mention the old name.

## Rename Mapping

| Old | New |
| --- | --- |
| TulingResearch | TuringResearch |
| TulingResearch Plus | TuringResearch Plus |
| TulingResearch_plus | TuringResearch_plus |
| `tuling_research` | `turing_research` |
| `tuling_research_plus` | `turing_research_plus` |
| `tulingresearch-plus` | `turingresearch-plus` |
| `tulingresearch-*` | `turingresearch-*` |

## Path Renames

| Old path | New path |
| --- | --- |
| `src/tuling_research/` | `src/turing_research/` |
| `src/tuling_research_plus/` | `src/turing_research_plus/` |
| `.agents/skills/tulingresearch-*` | `.agents/skills/turingresearch-*` |

## Round 38 Preservation

The Round 38 implementation surface was preserved under the new package path:

| Feature | New path |
| --- | --- |
| VGGT/SMPL-X Evidence Ledger | `src/turing_research_plus/vggt/` |
| Artifact Auditor | `src/turing_research_plus/artifact_audit/` |

No Visual Evidence Auditor, Advisor Pack Builder, or PDF Phase B full extraction
was added in this rename round.

## Package And Entry Points

- `pyproject.toml` project name: `turingresearch-plus`
- Core package: `turing_research`
- Plus package: `turing_research_plus`
- Console scripts: `turingresearch-plus`, `turingresearch-plus-mcp`
- MCP server name: `turingresearch-plus`

## Allowed Old-Name Locations

Old TulingResearch terms are permitted only in:

- `docs/rename-tuling-to-turing-report.md`
- `docs/round38-pre-rename-checkpoint.md`
- `docs/round38-rename-risk-register.md`
- `lanes/18_round38_pre_rename_checkpoint.md`

All other source, tests, contracts, docs, lanes, examples, race files, and skill
files are expected to use TuringResearch naming.

## Constraints Observed

- No new feature implementation.
- No network access.
- No VGGT local path reads.
- No fake experiment results.
- External project references to Neocortica and Yogsoth AI were not renamed.

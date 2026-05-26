# Round 38 Rename Risk Register: TulingResearch To TuringResearch

Status: pre-rename checkpoint risk register.

The future rename from TulingResearch to TuringResearch is high risk because
the project has package names, skill names, MCP names, contracts, docs,
examples, and tests that all encode the old name.

| Risk ID | Area | Risk | Severity | Mitigation for rename round |
| --- | --- | --- | --- | --- |
| R38-R01 | Python import | `tuling_research` or `tuling_research_plus` imports are partially renamed and tests fail. | critical | Rename imports atomically and run full tests. |
| R38-R02 | pyproject package discovery | Package discovery misses renamed Core or Plus package. | critical | Update `pyproject.toml` package include, scripts, metadata, and import tests together. |
| R38-R03 | tests import | Tests still import old package names. | high | Use repository-wide import scan and run unit/contract/workflow tests. |
| R38-R04 | skill name | `.agents/skills/tulingresearch-*` remains old or is partially renamed. | high | Decide new skill prefix first; update folder names, frontmatter, and skills index together. |
| R38-R05 | MCP server name | `tulingresearch-plus` changes without docs/contracts/test update. | high | Freeze new MCP server name and update MCP smoke tests. |
| R38-R06 | docs references | README/docs/contracts contain mixed TulingResearch and TuringResearch naming. | high | Run name integrity tests after adding new allowed/forbidden terms. |
| R38-R07 | workflow references | Examples and lanes refer to old path or old package. | medium | Update workflow docs and example READMEs in the same commit. |
| R38-R08 | Round 38 new modules | New `vggt` and `artifact_audit` modules are missed during package rename. | high | Include these modules in import-surface tests. |
| R38-R09 | public API drift | Proposed `vggt.*` or `artifact.*` names accidentally become public MCP tools during rename. | medium | Keep capsule-local API status until contract promotion. |
| R38-R10 | branch safety | Rename happens on an unstable working tree. | high | Commit this checkpoint to `pre-rename-round38-checkpoint` before rename. |

## Rename Do-Not-Do List

- Do not rename and implement new features in the same round.
- Do not change public MCP namespace without contract and docs updates.
- Do not read VGGT local paths while renaming.
- Do not rewrite Round 38 behavior while doing mechanical rename.

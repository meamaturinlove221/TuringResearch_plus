# TuringResearch Plus Post-Rename Audit Report

Status: Round 38.6 audit complete.

## Scope

Round 38.6 audited the repository after the global rename to TuringResearch. It
checked naming, Python imports, skills, contracts, docs, workflow tests, and the
Round 38 VGGT / SMPL-X Evidence Ledger and Artifact Auditor surface.

## Naming Result

Canonical names:

- Project display name: TuringResearch Plus
- Repository path: `TuringResearch/TuringResearch_plus`
- Core package: `turing_research`
- Plus package: `turing_research_plus`
- MCP server: `turingresearch-plus`
- Skill prefix: `turingresearch-`

Prior incorrect project-name terms are allowed only in the explicit rename
history files:

- `docs/rename-tuling-to-turing-report.md`
- `docs/round38-pre-rename-checkpoint.md`
- `docs/round38-rename-risk-register.md`
- `lanes/18_round38_pre_rename_checkpoint.md`

The name integrity test enforces this allowlist.

## Package Surface Result

The following packages and modules import successfully:

- `turing_research`
- `turing_research_plus`
- `turing_research_plus.vggt`
- `turing_research_plus.artifact_audit`
- `turing_research_plus.vggt.evidence_models`
- `turing_research_plus.vggt.evidence_ledger`
- `turing_research_plus.vggt.edge_audit`
- `turing_research_plus.vggt.markdown_export`
- `turing_research_plus.artifact_audit.models`
- `turing_research_plus.artifact_audit.auditor`
- `turing_research_plus.artifact_audit.npz_summary`
- `turing_research_plus.artifact_audit.manifest`

Round 38.6 added only thin compatibility modules for `edge_audit` and
`markdown_export`. They do not implement Visual Evidence Auditor, Advisor Pack
Builder, or PDF Phase B extraction.

## Skills Result

The repo-scoped skills now use the `turingresearch-*` prefix. The skills
integrity test confirms folder names, `SKILL.md` frontmatter, required sections,
and `docs/skills-index.md` alignment.

## Contracts Result

Contracts use TuringResearch naming and keep existing tool namespaces stable.
The rename did not change public namespace families such as `pdf.*`, `vggt.*`,
`artifact.*`, `visual.*`, `advisor.*`, or `upstream.*`.

## Constraints

- No network access was used.
- No VGGT local path was read.
- No `local_project_links.yaml` was committed.
- No new Visual Evidence Auditor, Advisor Pack Builder, or PDF Phase B code was
  added.
- No test or experiment result was fabricated.

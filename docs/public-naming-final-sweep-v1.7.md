# Public Naming Final Sweep v1.7

Round: 397R
Status: completed

## Decision

Public-facing project name: **TuringResearch**.

PR #1 showcase semantics are not accepted into the public launch line.

Upstream material may be referenced only as:

- reference documentation;
- workflow inspiration;
- related projects;
- docs/tool-surface parity targets.

It must not be described as migrated academic publication output.

## Sweep Scope

Checked:

- `README.md`
- `docs/`
- `docs-site/`
- `examples/`
- `community/` if present on the branch
- `split_ready/`
- `split_manual/`
- `pyproject.toml`
- `.mcp.example.json`
- `CHANGELOG.md`
- `VERSION`

## Findings

| Area | Result |
| --- | --- |
| Public name | `README.md` uses TuringResearch as the public project name |
| PR #1 showcase tree | `examples/original-author-showcase/` is absent on this branch |
| Community intake | `community/` is absent on this release-derived branch; PR #2 remains docs-only in main/integration planning |
| Authorized Academic Showcase wording | only appears in no-go / forbidden wording documents |
| Academic publication migration claim | no accepted migration claim found |
| Upstream references | must use Reference / Inspiration / Related Projects wording |
| Compatibility package names | retained as compatibility surfaces |

## Old Name Handling

The old public spelling is not reintroduced as current branding. Residual old
name mentions are limited to historical rename records and compatibility audit
contexts.

The compatibility names remain allowed for runtime/package stability:

- `turingresearch-plus`
- `turingresearch-plus-mcp`
- `turing_research_plus`

These names are not the public brand.

## PR #1 Semantic Cleanup

PR #1 remains excluded.

Do not write:

- Authorized Academic Showcase;
- Academic Showcase Migration;
- migrated academic publications;
- original author academic outputs;
- upstream academic publication migration.

Use:

- Upstream Reference Docs;
- Workflow Inspiration;
- Related Projects;
- reference parity;
- docs/tool-surface comparison.

## Release Boundary

No README changes were made in this sweep. The current README is already framed
around TuringResearch and does not include PR #1 showcase content.

Future README changes should use
`docs/readme-upstream-reference-wording.md` as the source of truth.

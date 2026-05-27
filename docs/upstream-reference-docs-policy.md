# Upstream Reference Docs Policy

Round: 396R
Status: policy locked

## Decision

Do not use the phrase **Academic Showcase Migration** for upstream materials.

Use **Upstream Reference Docs / Workflow Inspiration** instead.

The upstream materials may be referenced as project documentation, workflow
inspiration, architecture inspiration, and tool-surface comparison material.
They must not be represented as academic publication migration.

## Why

Round 395R found `NO_PUBLICATION_FOUND`.

The confirmed upstream material is primarily:

- README files;
- SKILL.md files;
- workflow docs;
- MCP tool docs;
- research engine architecture docs;
- source-code and tool-surface material.

These are useful engineering and research-workflow references, but they are not
paper PDFs, manuscripts, arXiv records, DOI records, BibTeX entries,
publication pages, accepted paper pages, proceedings links, theses, technical
reports, or author-provided academic output packages.

## Allowed Usage

Allowed:

- cite upstream repositories as inspiration;
- compare workflow structure;
- explain parity against visible tool/docs surfaces;
- reference public README/SKILL/workflow docs with attribution;
- use upstream ideas to guide independent TuringResearch implementation;
- document that publication migration is blocked until concrete source
  artifacts exist.

Not allowed:

- claim academic-output migration;
- call upstream reference material a publication package;
- treat `examples/original-author-showcase` as accepted academic evidence;
- merge PR #1 into the mainline;
- imply that papers were migrated when no paper artifacts were found;
- write README language that promises academic outputs from upstream.

## Publication Package Requirement

If academic-output migration is desired later, it must start from a concrete
publication package supplied or identified by the upstream author:

- exact upstream path and commit;
- paper / manuscript / PDF;
- arXiv / DOI / BibTeX;
- publication page or proceedings link;
- license and permission boundaries.

## README Rule

README may say upstream materials inspired workflow design or reference parity.

README must not say academic outputs, publication migration, paper migration, or
authorized academic showcase unless concrete publication artifacts are present
and have passed a future publication-candidate gate.

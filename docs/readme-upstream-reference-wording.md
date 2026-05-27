# README Upstream Reference Wording

Round: 396R
Status: wording guidance

## README Position

README should use inspiration/reference wording only.

README should not use Academic Showcase Migration.

README should not claim academic outputs, publication migration, migrated
papers, or accepted upstream publication artifacts.

## Suggested README Wording

```markdown
## Upstream Reference Docs / Workflow Inspiration

TuringResearch was developed with reference to visible public workflow and tool
documentation from upstream projects such as Neocortica and yogsoth-ai. Those
materials are used as reference docs and workflow inspiration for independent
TuringResearch implementations, parity checks, and safety gates.

No upstream academic publication package has been found or migrated. README
files, SKILL.md files, workflow docs, MCP tool docs, source code, examples, and
showcase material are not treated as academic publications.

If future publication migration is desired, it must start from concrete source
artifacts such as a paper/manuscript/PDF, arXiv link, DOI, BibTeX, publication
page, proceedings link, or an author-provided academic output package with exact
upstream path and commit.
```

## Short Version

```markdown
Upstream projects are referenced as workflow inspiration and docs/tool-surface
parity targets. No upstream academic publication package has been found or
migrated.
```

## Forbidden README Wording

Do not write:

- academic showcase migration;
- migrated upstream papers;
- authorized academic outputs;
- publication migration complete;
- upstream publications imported;
- examples/original-author-showcase as academic evidence.

## PR #1 Note

PR #1 should not be used as README source material. It did not satisfy the
academic-output migration target and is excluded from the release line.

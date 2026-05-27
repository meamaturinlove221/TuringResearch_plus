# Upstream Academic Publication Audit

Round: 395R
Status: completed
Result: `NO_PUBLICATION_FOUND`

## Scope

This audit rechecked public upstream repositories for concrete academic
publication artifacts. It did not merge PR #1, did not generate showcase
material, and did not modify README.

## Academic Output Definition

Accepted as a publication candidate:

- paper PDF;
- manuscript;
- arXiv link;
- DOI;
- BibTeX;
- publication page;
- accepted paper page;
- proceedings link;
- thesis or technical report;
- poster or slides, only if clearly an academic output;
- author-provided academic output package.

Not accepted:

- README;
- SKILL.md;
- example;
- showcase;
- SOP;
- workflow docs;
- source code;
- MCP tool docs;
- ordinary usage guide.

## Repositories Audited

| Source | Commit / status | Result |
| --- | --- | --- |
| Pthahnix/Neocortica | `aaf786512c28` | No publication artifact found |
| Pthahnix/Neocortica-Session | `5a01485cbd38` | No publication artifact found |
| Pthahnix/Neocortica-Scholar | `105ab8b7aa8d` | No publication artifact found |
| Pthahnix/Neocortica-Web | `94449c7b7724` | No publication artifact found |
| Pthahnix/Pthahnix | `c907efa7471e` | No publication artifact found |
| yogsoth-ai/de-anthropocentric-research-engine | `aaf786512c28` | No publication artifact found |
| yogsoth-ai/literature-engine | `1f14ff09d8f0` | No publication artifact found |
| yogsoth-ai/knowledge-acquisition | `b91b8018866a` | No publication artifact found |
| yogsoth-ai/hypothesis-formation | `e56aceb18d30` | No publication artifact found |
| yogsoth-ai/convergence | `c7c72326b702` | No publication artifact found |
| yogsoth-ai/stress-test | `9dfaeb1645fa` | No publication artifact found |
| yogsoth-ai/experiment-execution | `aecbde993c46` | No publication artifact found |
| yogsoth-ai/web-browsing | `3985f956f287` | No publication artifact found |
| yogsoth-ai/semantic-scholar-mcp | `1920863d4a67` | No publication artifact found |
| yogsoth-ai/biorxiv-mcp | `c1659a729ed8` | No publication artifact found |
| yogsoth-ai/wiki-vault | `084e008be6a7` | No publication artifact found |
| yogsoth-ai/north-star-crystallization | `9377dc75a1ca` | No publication artifact found |
| yogsoth-ai/deep-insight | `d0955f2f7b40` | No publication artifact found |
| yogsoth-ai/creative-ideation | `db429d0a69c1` | No publication artifact found |
| yogsoth-ai/knowledge-structuring | `97e25f54678d` | No publication artifact found |
| yogsoth-ai/literature-survey | `98e2d34e3dc7` | No publication artifact found |
| yogsoth-ai/subagent-spawning | `d72958fb9fcb` | No publication artifact found |
| yogsoth-ai/context-management | `c194583f86bc` | No publication artifact found |
| yogsoth-ai/.github | `5be2e80e07d6` | No publication artifact found |

## Findings

- No repository produced a concrete `.pdf`, `.bib`, or `CITATION.cff` academic
  artifact in the successful shallow audits.
- Many repositories mention papers, citations, arXiv, DOI, Semantic Scholar, or
  PDF access as tool capabilities.
- Those mentions are tool documentation or skill workflow text, not upstream
  academic publications.
- `Pthahnix/Neocortica-Scholar`, `yogsoth-ai/semantic-scholar-mcp`, and
  `yogsoth-ai/biorxiv-mcp` are especially paper-related, but they are MCP/tool
  repositories rather than publication repositories.
- `Pthahnix/Neocortica` and
  `yogsoth-ai/de-anthropocentric-research-engine` contain many paper-search and
  synthesis skills; these are workflow capabilities, not academic output
  packages.

## Decision

`NO_PUBLICATION_FOUND`

No source URL / repo / path / commit combination was accepted as a migratable
academic publication artifact in this audit.

## Consequence

Do not reopen or merge PR #1 as academic-output migration.

Do not turn `examples/original-author-showcase` into publication evidence.

The correct next step is to contact the upstream author for a concrete academic
output package if publication migration is still desired.

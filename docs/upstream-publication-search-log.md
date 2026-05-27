# Upstream Publication Search Log

Round: 395R
Status: completed with network limitations recorded

## Method

The audit used public GitHub repository access and shallow local clones where
available. It searched filenames and selected text for:

```text
arxiv arXiv doi DOI bibtex BibTeX citation cite paper publication publications
manuscript preprint pdf thesis poster slides accepted proceedings CVPR ICCV
ECCV NeurIPS ICLR ICML ACL EMNLP AAAI IJCAI
```

README, SKILL.md, MCP tool docs, examples, source code, SOPs, and workflow
guides were not accepted as publication artifacts.

## GitHub Listing Notes

- GitHub API calls returned 403 during this run.
- GitHub web pages were accessible enough to identify that Pthahnix exposes
  public repositories and yogsoth-ai exposes a public repository listing.
- Repository-level checks were performed via `git ls-remote` and shallow clone
  attempts.
- One broad scan timed out while traversing large skill repos; the audit then
  switched to bounded filename and README-style checks.

## Repository Scan Summary

| Repository | Commit / status | PDF count | BibTeX count | Citation file count | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| Pthahnix/Neocortica | `aaf786512c28` | 0 | 0 | 0 | Many skill docs reference paper search/synthesis |
| Pthahnix/Neocortica-Session | `5a01485cbd38` | 0 | 0 | 0 | Session tooling, no publication artifact |
| Pthahnix/Neocortica-Scholar | `105ab8b7aa8d` | 0 | 0 | 0 | Paper MCP/tool docs, no publication artifact |
| Pthahnix/Neocortica-Web | `94449c7b7724` | 0 | 0 | 0 | Web tooling, no publication artifact |
| Pthahnix/Pthahnix | `c907efa7471e` | 0 | 0 | 0 | Profile repo, no publication artifact |
| yogsoth-ai/de-anthropocentric-research-engine | `aaf786512c28` | 0 | 0 | 0 | Skill/workflow repo |
| yogsoth-ai/literature-engine | `1f14ff09d8f0` | 0 | 0 | 0 | Literature workflow docs |
| yogsoth-ai/knowledge-acquisition | `b91b8018866a` | 0 | 0 | 0 | Knowledge acquisition skills |
| yogsoth-ai/hypothesis-formation | `e56aceb18d30` | 0 | 0 | 0 | Hypothesis skills |
| yogsoth-ai/convergence | `c7c72326b702` | 0 | 0 | 0 | Convergence skills |
| yogsoth-ai/stress-test | `9dfaeb1645fa` | 0 | 0 | 0 | Stress-test skills |
| yogsoth-ai/experiment-execution | `aecbde993c46` | 0 | 0 | 0 | Experiment planning skills |
| yogsoth-ai/web-browsing | `3985f956f287` | 0 | 0 | 0 | Web browsing tooling |
| yogsoth-ai/semantic-scholar-mcp | `1920863d4a67` | 0 | 0 | 0 | Semantic Scholar MCP tool docs |
| yogsoth-ai/biorxiv-mcp | `c1659a729ed8` | 0 | 0 | 0 | bioRxiv/medRxiv MCP tool docs |
| yogsoth-ai/wiki-vault | `084e008be6a7` | 0 | 0 | 0 | Knowledge vault docs |
| yogsoth-ai/north-star-crystallization | `9377dc75a1ca` | 0 | 0 | 0 | Planning skills |
| yogsoth-ai/deep-insight | `d0955f2f7b40` | 0 | 0 | 0 | Insight skills |
| yogsoth-ai/creative-ideation | `db429d0a69c1` | 0 | 0 | 0 | Ideation skills |
| yogsoth-ai/knowledge-structuring | `97e25f54678d` | 0 | 0 | 0 | Structuring skills |
| yogsoth-ai/literature-survey | `98e2d34e3dc7` | 0 | 0 | 0 | Survey workflow skills |
| yogsoth-ai/subagent-spawning | `d72958fb9fcb` | 0 | 0 | 0 | Subagent docs |
| yogsoth-ai/context-management | `c194583f86bc` | 0 | 0 | 0 | Context management docs |
| yogsoth-ai/.github | `5be2e80e07d6` | 0 | 0 | 0 | Org profile/config |

## Interpreted Keyword Hits

Keyword hits were mostly:

- tool names such as `paper_searching`, `paper_reference`, `paper_reading`;
- Semantic Scholar / arXiv / bioRxiv API examples;
- research workflow budgets;
- literature survey skill names;
- citation-chaining SOPs;
- README usage examples.

These hits were explicitly not counted as publication artifacts.

# Legacy Name Compatibility Final

Round: 397R
Status: compatibility retained

## Public Name

The public project name is **TuringResearch**.

Use TuringResearch in public-facing prose, README positioning, release titles,
docs-site titles, launch material, and handoff summaries.

## Compatibility Names Retained

The following names remain for compatibility and packaging continuity:

| Name | Surface | Status |
| --- | --- | --- |
| `turingresearch-plus` | package distribution | retained |
| `turingresearch-plus-mcp` | MCP command / entry point | retained |
| `turing_research_plus` | Python compatibility namespace | retained |

These compatibility names should be labeled as package/import/runtime surfaces,
not as the public brand.

## Historical Names

Old project spellings may appear only in historical rename reports or explicit
compatibility audit records. They should not be used in new launch copy,
README positioning, docs-site pages, release highlights, or public summaries.

## Do Not Rename Yet

Do not rename package/import compatibility surfaces in this sweep. Renaming
them requires a separate packaging compatibility decision because it can affect:

- local install instructions;
- console entry points;
- MCP examples;
- tests;
- downstream imports.

## Final Rule

Public prose says TuringResearch. Runtime compatibility can still mention
compatibility names with explicit labeling.

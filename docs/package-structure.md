# TuringResearch Plus Package Structure

TuringResearch Plus uses a `src/` layout.

## Distribution

- Distribution name: `turingresearch-plus`
- Python requirement: `>=3.11`
- MCP server name: `turingresearch-plus`

## Packages

| Package | Purpose |
| --- | --- |
| `turing_research` | Core tools, cache, session registry, web/paper local content, PDF Markdown Phase A, MCP smoke server |
| `turing_research_plus` | Fusion workflows, semantic graph, survey, vault, context, Race Mode, SOP, experiment, paper pipeline |

Package discovery includes:

```toml
include = ["turing_research*", "turing_research_plus*"]
```

## Entry Points

| Script | Target |
| --- | --- |
| `turingresearch-plus` | `turing_research.mcp_server:main` |
| `turingresearch-plus-mcp` | `turing_research.mcp_server:main` |

## Extras

| Extra | Purpose |
| --- | --- |
| `dev` | pytest, pytest-asyncio, ruff, mypy |
| `pdf` | PyMuPDF for local PDF conversion |
| `mcp` | httpx plus optional typer/rich CLI helpers |
| `all` | local PDF and MCP optional runtime extras |

## Import Smoke Contract

Release tests verify:

- `import turing_research`
- `import turing_research_plus`
- `import turing_research.pdf`
- `import turing_research.mcp_server` is side-effect safe
- package metadata can be read from `pyproject.toml`
- entry point targets resolve to callable functions

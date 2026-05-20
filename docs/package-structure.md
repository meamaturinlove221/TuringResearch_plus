# TulingResearch Plus Package Structure

TulingResearch Plus uses a `src/` layout.

## Distribution

- Distribution name: `tulingresearch-plus`
- Python requirement: `>=3.11`
- MCP server name: `tulingresearch-plus`

## Packages

| Package | Purpose |
| --- | --- |
| `tuling_research` | Core tools, cache, session registry, web/paper local content, PDF Markdown Phase A, MCP smoke server |
| `tuling_research_plus` | Fusion workflows, semantic graph, survey, vault, context, Race Mode, SOP, experiment, paper pipeline |

Package discovery includes:

```toml
include = ["tuling_research*", "tuling_research_plus*"]
```

## Entry Points

| Script | Target |
| --- | --- |
| `tulingresearch-plus` | `tuling_research.mcp_server:main` |
| `tulingresearch-plus-mcp` | `tuling_research.mcp_server:main` |

## Extras

| Extra | Purpose |
| --- | --- |
| `dev` | pytest, pytest-asyncio, ruff, mypy |
| `pdf` | PyMuPDF for local PDF conversion |
| `mcp` | httpx plus optional typer/rich CLI helpers |
| `all` | local PDF and MCP optional runtime extras |

## Import Smoke Contract

Release tests verify:

- `import tuling_research`
- `import tuling_research_plus`
- `import tuling_research.pdf`
- `import tuling_research.mcp_server` is side-effect safe
- package metadata can be read from `pyproject.toml`
- entry point targets resolve to callable functions

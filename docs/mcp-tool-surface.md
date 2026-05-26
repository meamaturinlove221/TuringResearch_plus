# MCP Tool Surface

Status: v0.7 distribution polish.

The enabled stdio MCP smoke surface is intentionally small. It is separate from
the broader capability manifest.

## Enabled Stdio Smoke Tools

| Tool | Status | Fake/default safe |
| --- | --- | --- |
| `core.health_check` | `implemented_minimal` | yes |
| `core.paper_content` | `implemented_minimal` | yes |
| `core.web_content` | `implemented_minimal` | yes |
| `core.session_list` | `implemented_minimal` | yes |
| `pdf.inspect` | `implemented_minimal` | yes |
| `pdf.to_markdown` | `implemented_minimal` | yes |
| `pdf.markdown_content` | `implemented_minimal` | yes |

## Not Enabled By Default

- plugin registry tool declarations;
- live adapters;
- remote artifact live readers;
- paper writing helpers as public MCP tools;
- dashboard exporters as public MCP tools.

## Relationship To Capability Manifest

`docs/tool-capability-manifest.md` documents the broader local capability
catalog. It includes local helpers, adapters, exporters, and workflows that are
useful for routing and release explanation.

The capability manifest is a broader local capability catalog, not the enabled
MCP stdio tool list.

Only the tools listed above are part of the current stdio smoke surface.

## Safety Notes

- No live network is required.
- No real API key is required.
- Plugin tools are disabled by default.
- Live mode is opt-in.
- Tool outputs are operational helper outputs, not verified research evidence.

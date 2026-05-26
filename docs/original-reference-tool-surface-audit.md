# Original Reference Tool Surface Audit

Status: completed.

Round: 261.

This audit checks whether TuringResearch exposes recognizable tool surfaces for
the stable original reference capabilities.

It does not add new tools or runtime behavior.

## Result

Overall status: `PARTIAL TOOL SURFACE PARITY`.

TuringResearch has broad local Python surfaces for reference parity and a small
safe MCP stdio smoke surface. The gap is not lack of internal helpers; the gap
is that several original-reference workflows are not yet exposed as one clear,
operator-facing tool path.

## Surface Types

| Surface type | Meaning |
| --- | --- |
| `mcp-stdio` | Enabled in the current stdio MCP smoke registry. |
| `local-python` | Importable local Python function/model surface with tests. |
| `config-docs` | Config or usage documentation, not a callable tool. |
| `policy-only` | Safety policy exists, but no execution tool exists. |
| `missing` | No meaningful current surface. |
| `deferred` | Intentionally postponed. |
| `rejected` | Outside product/safety boundary. |

## High-Level Findings

- Neocortica-Session has local Python surfaces for preflight, context pack,
  return manifest, and memory policy. Transfer and launch are not runnable tool
  surfaces yet.
- Neocortica-Scholar has local Python and documentation surfaces for search
  priority, cached content, reference fallback, reading plan, and fallback
  policy. Live paper retrieval remains optional and disabled by default.
- Neocortica-Web has local Python surfaces for fake/default web fetching, web
  content review, Apify optional guide, cache, and source metadata. Live web
  behavior is not default.
- yogsoth parity has local Python surfaces for campaign routing, vault,
  ontology, stress tests, and experiment runbooks. Research Catalog remains an
  integration layer more than a single callable tool.
- MCP stdio remains deliberately narrow and should not be confused with the
  broader capability manifest.

## MCP Boundary

The current MCP stdio smoke surface is intentionally small:

- `core.health_check`
- `core.paper_content`
- `core.web_content`
- `core.session_list`
- `pdf.inspect`
- `pdf.to_markdown`
- `pdf.markdown_content`

The broader surfaces in this audit are local capability surfaces, not all
enabled MCP tools.

## Main Gap

The next v1.3 step should not simply add more docs. It should create coherent
fake/default tool paths:

1. Session runtime path:
   preflight -> context pack -> transfer placeholder -> return manifest ->
   verifier.
2. Scholar path:
   query -> source priority -> cached markdown/reference fallback -> reading
   plan.
3. Web path:
   URL -> dry-run fetch -> content review -> source metadata/cache report.
4. Research Catalog path:
   task -> campaign route -> skill map -> vault/stress/runbook trace.

All should remain local-first, fake/default, and human-reviewed.

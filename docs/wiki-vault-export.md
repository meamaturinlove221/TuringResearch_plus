# Wiki Vault Export

Status: implemented minimal.

Round: 244.

`WikiVaultExport` turns a lightweight `VaultGraph` into a review-only wiki
package. It is meant for browsing research context, not for proving claims.

## Export Contents

- One Markdown-like page per node.
- Wikilinks for page navigation.
- Backlink index.
- Outgoing link index.
- Dangling link report.
- Edge quality report.
- Graph summary.

## Page Structure

Each page includes:

- Node id.
- Node type.
- Confidence.
- Human review flag.
- Backlinks.
- Outgoing links.

## Review Boundary

Wiki output is a navigation aid. It does not convert draft claims into observed
results and does not certify paper conclusions. Any node or edge that supports a
claim still needs source references and human review.

## Example Use

```python
from turing_research_plus.vault_graph.wiki_export import build_wiki_vault_export

export = build_wiki_vault_export(graph)
page_markdown = export.pages["VGGT"]
```

The export is local and read-only. It does not require a server, database, or
network connection.

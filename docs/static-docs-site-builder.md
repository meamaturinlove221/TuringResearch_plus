# Static Docs Site Builder

Status: experimental local utility.

Round: 216.

The static docs site builder turns `docs-site/nav.yaml` and Markdown page stubs
under `docs-site/pages/` into static HTML. It is local-first and does not
require Node, network access, a server, or a cloud deployment target.

## Inputs

- `docs-site/site_manifest.yaml`
- `docs-site/nav.yaml`
- `docs-site/pages/*.md`

## Outputs

- `docs-site/output/*.html`
- `docs-site/output/site.css`

The build output is ignored by default except for `.gitkeep`.

## Python API

```python
from pathlib import Path

from turing_research_plus.docs_site import build_docs_site
from turing_research_plus.docs_site.models import DocsSiteBuildRequest

root = Path(".")
result = build_docs_site(
    DocsSiteBuildRequest(
        repo_root=root,
        docs_site_root=root / "docs-site",
        output_root=root / "docs-site" / "output",
        nav_path=root / "docs-site" / "nav.yaml",
        manifest_path=root / "docs-site" / "site_manifest.yaml",
    )
)
```

## Boundaries

- No deployment.
- No Node requirement.
- No search backend.
- No private data read.
- No fake external links.
- Generated HTML requires human review before publication.

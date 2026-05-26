# Dashboard Data API

Status: experimental read-only API.

Round: 218.

The Dashboard Data API provides a shared read-only data layer for static
dashboards and the local server dashboard. It reads public demo Markdown/JSON
files and returns structured summaries that can be rendered as HTML or exported
as JSON.

## Inputs

- `examples/public_demo/demo_research_intent.md`
- `examples/public_demo/demo_evidence_ledger.json`
- `examples/public_demo/demo_artifact_index.md`
- `examples/public_demo/demo_related_work.md`
- `examples/public_demo/demo_advisor_pack.md`

## Outputs

- project summary;
- evidence summary;
- artifact summary;
- paper/advisor summary;
- JSON export bundle.

## Python API

```python
from pathlib import Path

from turing_research_plus.dashboard_api import (
    build_public_demo_dashboard_data,
    export_json,
)

bundle = build_public_demo_dashboard_data(Path("examples/public_demo"))
payload = export_json(bundle)
```

## Safety Boundary

- Read-only.
- No writes.
- No remote API.
- No secrets.
- No raw data.
- No private paths.
- Fake/demo evidence must not be promoted to observed.
- Human review remains required.

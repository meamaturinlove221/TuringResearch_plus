# Local Server Dashboard

Status: experimental local utility.

Round: 217.

The local server dashboard is a read-only localhost dashboard for public demo
summaries. It builds on the existing static dashboard material and exposes a
small set of local routes.

## Routes

- `/` and `/dashboard`: public demo dashboard.
- `/project`: project overview.
- `/evidence`: evidence summary.
- `/artifacts`: artifact summary.
- `/paper`: paper and related-work summary.
- `/advisor`: advisor bundle summary.
- `/health`: local health check.

## Python Preview

```python
from pathlib import Path

from turing_research_plus.local_server.tools import preview_public_demo_route

payload = preview_public_demo_route(Path("."), "/evidence")
```

## Boundaries

- Localhost only.
- Read-only local mode.
- No login.
- No cloud deployment.
- No uploads.
- No command execution.
- No default networking.
- No private VGGT path reads.
- No secret display.

The dashboard displays public demo material only. It is not an experiment
runner and not a research result.

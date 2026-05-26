# Screenshot TODO

Round: 384
Status: placeholder checklist only

This folder intentionally contains no real screenshots in Round 384. The
manifest records what should be captured later by a human reviewer.

## Capture Checklist

Before adding any screenshot:

- capture only local/public-safe surfaces;
- do not show private paths;
- do not show raw data;
- do not show API keys, tokens, cookies, or credentials;
- do not show a fake GitHub, Pages, or split-repo URL;
- do not imply a public deployment exists unless it really exists;
- do not imply VGGT or SparseConv3D `success`;
- do not imply ARIS is `implemented`;
- confirm the screenshot matches current README/docs wording.

## Required Screenshots

| ID | Surface | Status |
| --- | --- | --- |
| `readme-first-screen` | README first screen | pending human capture |
| `docs-site` | docs site / release bundle | pending human capture |
| `dashboard-landing` | dashboard landing | pending human capture |
| `parity-showcase` | parity showcase | pending human capture |
| `interview-demo-view` | interview demo view | pending human capture |
| `split-manual-pack` | split manual pack | pending human capture |
| `optional-live-policy` | optional live policy | pending human capture |

## Storage Rule

When real screenshots are added later, update `SCREENSHOT_MANIFEST.yaml` with:

- `status: captured`;
- capture date;
- source path or local command;
- reviewer;
- safety review notes;
- image hash.

Do not mark a placeholder as captured until a real screenshot file exists.

# Post-release Verification

Status: verification checklist.

Round: 196.

This checklist applies after a future human-created GitHub release. It is not a
release action.

## Verify Release Surface

- GitHub release title matches the approved draft.
- Release notes link to README, quickstart, public demo, changelog, and safety
  notes.
- No release artifact includes private data, raw data, restricted model
  payloads, or real credentials.
- No nonexistent split repository URL is published.
- No statement claims automatic research completion or final paper writing.
- No statement claims VGGT or SparseConv3D experiment success without evidence.

## Verify Install

```bash
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_v1_public_quickstart_fake.py -q
```

## Verify MCP/Fake Defaults

- `.mcp.example.json` uses fake mode.
- Live adapters are disabled by default.
- Plugin tools are disabled by default.
- Credential fields are empty.

## Verify Follow-up

- File any release blockers found after publication.
- Update known limitations if user confusion appears.
- Keep physical split repositories unpublished unless separately approved.

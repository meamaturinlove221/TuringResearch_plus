# Round 379 - pipx / uv Install Check

Status: complete

## Objective

Prepare pipx and uv installation verification guidance plus local fake smoke
tests. This round does not publish a package.

## Files

- `docs/pipx-install-guide.md`
- `docs/uv-install-guide.md`
- `docs/install-smoke-test.md`
- `tests/workflow/test_install_smoke_fake.py`
- `lanes/357_pipx_uv_install_check.md`
- `lanes/00_master_ledger.md`

## Coverage

- pipx local editable install guidance.
- pipx local wheel artifact install guidance.
- uv local editable install guidance.
- uv local wheel artifact install guidance.
- fake module smoke command.
- console script smoke guidance.
- no PyPI publication.
- no API key.
- no VGGT dependency.

## Validation

- Install smoke tests passed.
- Pre-push checks passed.

## Non-actions

- No PyPI publish.
- No package upload.
- No tag creation.
- No live network request.
- No VGGT read.
- No remote execution.

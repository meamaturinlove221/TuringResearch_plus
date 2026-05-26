# Install Smoke Test

Round: 379
Status: fake/local smoke check

The install smoke test verifies that TuringResearch exposes a runnable local
entry point after editable or wheel installation. It does not publish a package
and does not require PyPI.

Do not use a package-index install command until maintainers explicitly publish
a package.

## Smoke Environment

Use explicit fake/default environment settings:

```powershell
$env:TURINGRESEARCH_MODE = "fake"
$env:TURINGRESEARCH_ENABLE_LIVE_TESTS = "0"
$env:TURINGRESEARCH_ENABLE_PLUGINS = "0"
```

No API key, VGGT data, local VGGT checkout, raw data, or restricted model file
is required.

## Module Smoke Commands

These commands run directly from the checkout or from an installed environment:

```powershell
python -m turing_research.mcp_server --health-check
python -m turing_research.mcp_server --manifest
```

Expected health-check shape:

```json
{"status": "ok", "package": "turing_research", "version": "1.5.0rc0"}
```

The manifest command should return JSON with the local STDIO server name,
package version, and registered fake/local tool surface.

## Console Script Smoke Commands

After a local editable install, pipx install, uv install, or wheel artifact
install:

```powershell
turingresearch-plus-mcp --health-check
turingresearch-plus-mcp --manifest
```

The console script name remains a compatibility surface. The public project
name is TuringResearch.

## Automated Fake Smoke Test

```powershell
python -m pytest tests/workflow/test_install_smoke_fake.py -q
```

The automated test runs the module smoke commands through the current Python
interpreter and validates the install guidance documents. It does not invoke
`pipx`, `uv`, PyPI, live providers, or VGGT.

## Failure Handling

If the smoke test fails:

1. Confirm Python is 3.11 or newer.
2. Confirm the checkout root is the current working directory.
3. Confirm local dependencies are installed.
4. Re-run `python -m turing_research.mcp_server --health-check`.
5. Do not mark an install path as release-ready until the fake smoke test
   passes locally.

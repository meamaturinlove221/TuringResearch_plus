# TuringResearch Troubleshooting

## Package Import Fails

Run from the repository root and install the project in editable mode:

```powershell
python -m pip install -e ".[dev]"
```

If imports still fail, confirm that Python is 3.11 or newer:

```powershell
python --version
```

## PDF Conversion Reports Missing PyMuPDF

PyMuPDF is optional. Install the PDF extra when local PDF conversion is needed:

```powershell
python -m pip install -e ".[dev,pdf]"
```

The package should still import without PyMuPDF. Only local conversion through the PyMuPDF adapter requires it.

## MCP Manifest Does Not Print

Use the module entry point from an installed editable environment:

```powershell
python -m turing_research.mcp_server --manifest
```

The default MCP smoke command writes human-readable status to stderr so STDIO protocol payloads are not mixed with logs.

## API Key Not Found

`v0.1.0` does not require live API keys for default tests, local MCP smoke, or examples. Live adapters are future opt-in work and must be marked live or manual when added.

## Examples Need Network

Release examples must run in fake mode or local fixture mode. Use the workflow tests:

```powershell
python -m pytest tests/workflow
```

No Semantic Scholar key, web token, or other live service credential is required.

## PowerShell Extras Quoting

If editable install extras are interpreted unexpectedly, quote the extras string:

```powershell
python -m pip install -e ".[dev,pdf,mcp]"
```

## Cache Or Generated Files Look Stale

Default tests use temporary directories where possible. For manual local smoke runs, remove only local generated smoke artifacts that you created. Do not delete source directories or release docs.

## Package Is Not On PyPI

TuringResearch `v0.1.0` release preparation validates local packaging only. Automatic PyPI publication is outside the `v0.1.0` scope.

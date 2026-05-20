# TulingResearch Plus Local Install Smoke

This smoke guide verifies that TulingResearch Plus can be installed locally, imported, used through the local MCP smoke entry point, and run with fake-mode examples.

## Scope

The local install smoke covers:

- Editable package install.
- Public import surface.
- STDIO-safe MCP entry point.
- Tool registry and `core.health_check` dry-run.
- Optional PDF dependency behavior.
- Fake-mode examples.

It does not publish a package, call live APIs, require API keys, or run network tests.

## Fresh Environment Smoke

From the repository root:

```powershell
python -m venv .venv-smoke
.\.venv-smoke\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Optional local PDF conversion can be tested with:

```powershell
python -m pip install -e ".[dev,pdf]"
```

MCP and CLI extras can be tested with:

```powershell
python -m pip install -e ".[dev,mcp]"
```

## Import Smoke

```powershell
python -c "import tuling_research, tuling_research.pdf, tuling_research_plus"
python -c "import tuling_research_plus.artifacts, tuling_research_plus.campaign, tuling_research_plus.race, tuling_research_plus.paper"
```

Expected result: imports succeed without starting network services or requiring live API keys.

## MCP Smoke

```powershell
python -m tuling_research.mcp_server --manifest
python -m tuling_research.mcp_server --health-check
```

Expected result:

- Server name is `tulingresearch-plus`.
- Transport is `stdio`.
- `core.health_check` is registered.
- Importing `tuling_research.mcp_server` does not start a server.
- Human-readable default status is written to stderr, not stdout.

## Optional Dependency Behavior

PyMuPDF is optional through the `pdf` extra. Without that extra:

- `import tuling_research.pdf` must still work.
- Package imports must not fail.
- Local PDF conversion must return or raise a clear converter-unavailable error instead of breaking import.

Live API keys are not required for default tests, imports, MCP smoke, or fake examples.

## Test Commands

```powershell
python -m pytest tests/contract/test_local_install_assumptions.py
python -m pytest tests/contract/test_public_import_surface.py
python -m pytest tests/contract/test_mcp_entrypoint_surface.py
python -m pytest tests/contract/test_package_imports.py tests/contract/test_entry_points.py
python -m pytest tests/workflow/test_example_vggt_human_prior.py tests/workflow/test_example_smplx_feature_adapter.py tests/workflow/test_example_citation_graph.py tests/workflow/test_example_pdf_to_markdown.py
```

The full release-candidate suite remains:

```powershell
python -m pytest
python -m ruff check .
python -m mypy src
```

## Expected Result

The local install smoke passes when package imports, MCP entry points, and fake-mode examples all run without real network access or live credentials.

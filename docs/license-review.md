# TulingResearch Plus License Review

Date: 2026-05-20

## Scope

This review covers the `v0.1.0` release candidate source tree, examples, contracts, and documentation.

## Current Project License Metadata

`pyproject.toml` currently declares:

```toml
license = {{ text = "Proprietary" }}
```

## Dependency Notes

Runtime dependencies declared in `pyproject.toml`:

- `pydantic`
- `pydantic-settings`
- `httpx`

Optional extras:

- `pdf`: `pymupdf`
- `dev`: `pytest`, `pytest-asyncio`, `ruff`, `mypy`
- `mcp`: `httpx`, `typer`, `rich`

## Source Reuse Policy

TulingResearch Plus may reference public project ideas at concept/workflow level, but it must not copy incompatible-license implementation code. References to Neocortica and Yogsoth AI are inspiration/reference context only.

## Release Decision

No incompatible copied code is recorded in the release candidate. Before public distribution under a non-proprietary license, perform a formal dependency and repository license review.

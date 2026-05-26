# Monorepo Modular Layout

Status: implemented minimal.

Round: 155.

Round 155 introduces lightweight namespace facade packages inside the monorepo.
It does not split repositories, move implementation code, or remove legacy
imports.

## New Namespace Packages

- `turing_research_core`
- `turing_research_paper`
- `turing_research_artifact`
- `turing_research_experiment`
- `turing_research_dashboard`
- `turing_research_plugins`
- `turing_research_cases`

Each package contains:

- `__init__.py`
- `public_api.py`
- `models.py`
- `README.md`

## Compatibility Layer

The existing `turing_research_plus` namespace remains supported.

New compatibility helpers live at:

- `turing_research_plus.compat`
- `turing_research_plus.compat.module_aliases`

These helpers document target namespace to legacy module mappings. They do not
move implementations.

## Design

The new namespaces are facade/re-export packages:

- they import representative public models and helpers from
  `turing_research_plus`;
- they expose `NAMESPACE`, `COMPATIBILITY_NAMESPACE`, `STABILITY`, and
  `PUBLIC_MODULE_ALIASES`;
- they avoid optional live behavior;
- they avoid plugin execution;
- they preserve old imports.

## Package Discovery

`pyproject.toml` now includes the new namespace package patterns so editable
install and packaging discovery can find them.

## Stability

| Namespace | Stability |
| --- | --- |
| `turing_research_core` | beta |
| `turing_research_experiment` | beta |
| `turing_research_paper` | experimental |
| `turing_research_artifact` | experimental |
| `turing_research_dashboard` | experimental |
| `turing_research_plugins` | experimental |
| `turing_research_cases` | experimental |

## What Did Not Change

- No implementation files moved.
- No old import removed.
- No repository split.
- No CLI/MCP entrypoint change.
- No live adapter default changed.
- No plugin execution enabled.
- No final paper or experiment behavior changed.

## Next Steps

- Keep adding tests around old/new import compatibility.
- Stabilize DTOs before moving implementation.
- Move one namespace at a time in future rounds.
- Keep `turing_research_plus` compatibility through v0.x.

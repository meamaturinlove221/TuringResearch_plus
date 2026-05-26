# Plugin Architecture

Status: v0.6 minimal implementation.

Round 109 adds a manifest-only plugin architecture. It describes extension
points for tools, skills, adapters, exporters, workflows, validators, and
renderers without executing plugin code.

## Purpose

The plugin layer gives future contributors a safe contract surface:

- declare capabilities;
- declare inputs and outputs;
- declare required permissions;
- declare safety level;
- declare docs, tests, and status.

It does not install, import, or run third-party code.

## Plugin Manifest

`PluginManifest` requires:

- `plugin_id`
- `name`
- `version`
- `type`
- `entry_kind`
- `capabilities`
- `required_permissions`
- `config_schema`
- `inputs`
- `outputs`
- `safety_level`
- `status`
- optional `author`
- optional `license`

## Plugin Types

- `adapter`
- `exporter`
- `workflow`
- `skill`
- `validator`
- `renderer`

## Local Helpers

- command: `turing plugin validate`
- local helper: `plugin_validate`
- output: `PluginValidationReport`

- command: `turing plugin registry`
- local helper: `plugin_registry_load`
- output: `PluginRegistry`

These helpers are local Python helpers and are not frozen public MCP APIs.

## Safety Rules

- Plugin code is not executed.
- Unknown Python entrypoints are not loaded.
- Manifest validation is local and offline.
- Third-party plugins are disabled by default.
- Permissions must be declared.
- Safety level must be declared.
- Human review is required before enabling a plugin.

## Demo Plugins

Fixtures:

- `examples/plugins/demo_exporter_plugin/plugin.yaml`
- `examples/plugins/demo_adapter_plugin/plugin.yaml`

Both are manifest-only demos. They do not contain executable plugin code.

## Limitations

- No plugin marketplace publishing.
- No automatic install.
- No dynamic code loading.
- No sandbox runtime.
- No trust model beyond manifest validation yet.

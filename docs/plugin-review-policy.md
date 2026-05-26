# Plugin Review Policy

Status: planning policy.

Round: 150.

TuringResearch Plus treats plugins as release-sensitive extension metadata until
a later gate approves safe runtime behavior. Unknown third-party plugins must
remain disabled by default.

## Plugin Review Process

1. Receive or create plugin manifest.
2. Validate manifest schema.
3. Validate capability ids and docs links.
4. Check required permissions.
5. Run sandbox policy review.
6. Run extension safety report.
7. Run compatibility harness.
8. Check MCP mapping if the plugin exposes tools.
9. Confirm tests are declared and relevant.
10. Require human review before enabling anything beyond metadata display.

## Permission Review

| Permission | Default posture |
| --- | --- |
| read project files | scoped only |
| write project files | explicit enable only |
| network access | explicit live flag and review |
| live API access | explicit live flag and review |
| remote read | explicit enable only |
| remote write | denied by default |
| execute code | denied by default |
| shell access | denied by default |
| secrets access | forbidden |
| artifact export | explicit enable and review |

## Registry Policy

- Public registry drafts are metadata-only.
- Registry entries must include status, safety level, permissions,
  compatibility report, docs, tests, and maintainer review state.
- Third-party entries are disabled by default.
- No registry entry may override core tools.
- No registry entry may require secrets by default.

## Runtime Policy

- Do not execute unknown third-party plugin code.
- Do not load dynamic entry points from untrusted manifests.
- Do not enable plugins because they appear in a registry.
- Do not treat policy-level sandboxing as real operating-system isolation.
- Runtime plugin execution requires a future gate with explicit sandbox tests.

## Release Blockers

- Missing manifest.
- Missing safety level.
- Missing permissions.
- Unsafe permission granted without human review.
- Unknown plugin enabled by default.
- Core namespace override.
- Secret access request.
- Code execution or shell access without a future approved sandbox gate.
- Compatibility report missing or failing.

## Maintenance Cadence

- Review built-in demo plugins every release candidate.
- Review public registry metadata every plugin-surface change.
- Review sandbox policy after any new permission category.
- Review MCP mappings after any tool-surface change.
- Archive or mark stale plugins when docs/tests are no longer valid.

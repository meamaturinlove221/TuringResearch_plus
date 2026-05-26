# Community Plugin Strategy

Status: planning draft.

v0.6 introduced manifest-only plugin architecture, MCP plugin registry,
capability manifests, skill marketplace layout, and extension safety gates.
v0.7 can turn this into a community-facing plugin strategy without executing
untrusted code by default.

## Strategy

Start with metadata, review, and documentation. Runtime plugin loading should
come only after sandbox policy, permission review, installation boundaries, and
security reporting are mature.

## Plugin Submission Shape

A community plugin candidate should provide:

- plugin manifest;
- declared capabilities;
- required permissions;
- safety level;
- input and output schemas;
- docs;
- tests;
- license;
- maintainer contact;
- explicit fake/live mode boundary.

## Registry Tiers

| Tier | Meaning | Runtime |
| --- | --- | --- |
| draft | Submitted manifest or local example. | Not executable. |
| reviewed-manifest | Manifest passes schema and safety review. | Still disabled by default. |
| demo-safe | Works with fake/demo data only. | Optional local review. |
| trusted-local | Maintainer-approved local plugin. | Explicit opt-in only. |
| live-capable | Requires live services or API keys. | Explicit opt-in, never default. |

## Permissions

Permission review should keep these defaults:

- `execute_code`: forbidden until sandbox policy exists.
- `network_access`: explicit and disabled by default.
- `remote_write`: forbidden by default.
- secrets access: forbidden.
- raw data access: restricted and release-blocking.
- package release: maintainer-only.

## Safety Requirements

- Third-party plugins default to disabled.
- Plugins must not override core tools.
- MCP tool declarations must have a namespace.
- Live-required plugins must not be enabled in default tests.
- Plugin docs must disclose external dependencies and credentials.
- Every plugin requires an extension safety report.

## Public Registry Draft

The first public registry should be a static catalog:

- no dynamic code loading;
- no package installation;
- no remote registry calls;
- manifest validation only;
- local docs and examples only.

## Future Runtime Loading

Real plugin loading can be considered only after:

1. sandbox threat model;
2. permission enforcement model;
3. dependency isolation story;
4. signing or provenance policy;
5. opt-in installation flow;
6. uninstall/disable flow;
7. security report process.

## Non-goals

- No online marketplace in v0.7 by default.
- No automatic execution of community code.
- No automatic granting of network, filesystem write, or secret access.
- No community plugin promotion without maintainer review.

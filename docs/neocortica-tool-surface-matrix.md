# Neocortica Tool Surface Matrix

Status: completed.

Round: 261.

## Session

| Reference tool surface | Current TuringResearch surface | Surface type | Status | Gap |
| --- | --- | --- | --- | --- |
| preflight | `run_pod_context_preflight` | `local-python` | covered | Needs one operator-facing runtime path. |
| context pack | `build_session_context_pack_manifest` | `local-python` | covered | Manifest generation exists; transfer packaging remains separate. |
| transfer | `PodTransferPolicy` and transfer policy docs | `policy-only` | partial | No transfer runner in current scope. |
| launch | remote execution non-goals | `policy-only` | deferred | SSH/tmux/provision/remote command launch is not implemented. |
| return manifest | `build_structured_return_manifest` | `local-python` | covered | Needs fuller returned-bundle checksum/file safety path. |
| memory policy | `PodMemoryPolicy`, no bidirectional sync policy | `local-python` | covered | Policy exists; no bidirectional sync by design. |

## Scholar

| Reference tool surface | Current TuringResearch surface | Surface type | Status | Gap |
| --- | --- | --- | --- | --- |
| paper search | `build_scholar_source_priority_plan`, search pipeline modules | `local-python` | covered | Needs a single fake query workflow. |
| paper content | cached content helpers, `core.paper_content` MCP smoke tool | `local-python` / `mcp-stdio` | partial | MCP smoke exists, but full Scholar pipeline is not an MCP surface. |
| paper reference | reference pipeline and fallback policy | `local-python` | covered | Needs clearer demo path. |
| paper reading | three-pass reading plan | `local-python` | covered | Review-only. |
| cached markdown | cached Markdown policy and cached content helpers | `local-python` | covered | Needs fixture replay surfaced in docs/dashboard. |
| fallback policy | `build_scholar_fallback_policy` | `local-python` | covered | Heavy PDF fallback remains deferred. |

## Web

| Reference tool surface | Current TuringResearch surface | Surface type | Status | Gap |
| --- | --- | --- | --- | --- |
| web_fetching | `run_web_fetching_tool` | `local-python` | covered | Fake/default only by default. |
| web_content | `web_content_from_fetch_result`, `core.web_content` MCP smoke tool | `local-python` / `mcp-stdio` | covered | Human review remains required. |
| Apify optional | `build_apify_usage_guide`, Apify missing-token behavior | `local-python` | partial | Live templates are not enabled by default. |
| cache | web content cache policy/helpers | `local-python` | covered | Needs operator-facing cache report. |
| source metadata | source metadata helpers and Web fetch result metadata | `local-python` | covered | Needs dashboard integration with runtime status. |

## Neocortica Summary

Neocortica parity is strong for local fake/default surfaces and safety policy.
It is not yet full runtime parity for transfer, launch, live retrieval, or
remote session operation.

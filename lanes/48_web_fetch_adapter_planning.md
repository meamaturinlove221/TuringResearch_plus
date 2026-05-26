# Lane 48 - Web Fetch Adapter Planning

Status: completed design draft.

## Scope

Round 67 designs the v0.3 Web Fetch Adapter / Apify Adapter plan. It does not
implement live web fetching and does not call Apify.

## Created Files

- `docs/web-fetch-adapter-plan.md`
- `docs/apify-adapter-plan.md`
- `docs/web-content-cache-policy.md`
- `contracts/web_fetch_adapter.yaml`
- `race/feature_capsules/web_fetch_adapter/`
- `race/feature_capsules/apify_adapter/`

## Proposed Adapters

- `WebFetchAdapter`
- `WebContentAdapter`
- `ApifyAdapter`
- fake adapter equivalents
- optional live adapters

## Proposed Tools

- `web.fetch`
- `web.content`
- `web.search_optional`
- `web.apify_run_optional`

These are proposed tools only and are not part of the current public MCP tool
freeze.

## Policies

- Default tests do not access network.
- Live tests are skipped by default.
- `APIFY_TOKEN` is optional.
- Live result means retrieved, not verified.
- Web content must preserve source URL, retrieval time, and content hash.
- Do not fetch restricted content.
- Do not bypass login or paywall.

## VGGT Use

Future VGGT workflows may use this adapter for project pages, GitHub README
files, method pages, and arXiv HTML pages. It does not replace real paper
reading and does not create final claims automatically.

## Boundaries

- No code implementation.
- No network access.
- No Apify calls.
- No upstream code copying.
- No old project naming.

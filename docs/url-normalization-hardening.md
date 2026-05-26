# URL Normalization Hardening

Status: implemented.

Round: 308.

This round adds a WebMeta / `normUrl`-style URL normalization layer for the
v1.4 Web production parity track. It does not fetch URLs and does not enable
live networking.

## Behavior

- Lowercase scheme and host.
- Strip trailing dot from host.
- Remove default ports: `:80` for HTTP and `:443` for HTTPS.
- Collapse duplicate path separators.
- Percent-encode unsafe path characters.
- Strip fragments by default.
- Drop common tracking query params such as `utm_*`, `fbclid`, `gclid`,
  `mc_cid`, `mc_eid`, and `igshid`.
- Sort retained query params for stable cache keys.
- Block non-HTTP(S) schemes by default.

## Public API

- `UrlNormalizationRequest`
- `NormalizedUrl`
- `normalize_url`
- `normalize_url_string`
- `url_cache_key`

## WebMeta Fields

The `NormalizedUrl.web_meta` property exposes:

- `original_url`
- `normUrl`
- `scheme`
- `host`
- `path`
- `query`
- `fragment_removed`
- `tracking_params_removed`
- `default_port_removed`
- `requires_human_review`

## Safety Boundary

- no network request;
- no cookie storage;
- no private content access;
- no paywall bypass;
- no credential handling;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/unit/test_url_normalization_hardening.py -q
```

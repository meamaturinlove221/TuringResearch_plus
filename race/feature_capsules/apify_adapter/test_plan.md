# Test Plan: apify_adapter

- fake Apify adapter returns deterministic output
- default tests do not access network
- missing `APIFY_TOKEN` returns typed error in live mode
- live tests are skipped unless explicitly enabled
- source metadata includes source URL, retrieval time, content hash, and provider
- fetched content remains not human verified

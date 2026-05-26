# Test Plan: web_fetch_adapter

- fake fetch returns deterministic content
- default tests do not access network
- missing `APIFY_TOKEN` does not fail default tests
- fetched content records source URL, retrieval time, and content hash
- restricted source is blocked
- retrieved content is not human verified

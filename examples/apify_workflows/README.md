# Apify Workflow Templates

These templates describe optional Apify workflows for public web material.

They are not executed by default. They do not require `APIFY_TOKEN` for fake or
review use. They do not bypass login, bypass paywalls, scrape private content,
store cookies, or mark retrieved content as verified evidence.

Templates:

- `project_page_fetch.yaml`
- `search_result_fetch.yaml`
- `content_extract.yaml`

Safety defaults:

- `live_enabled: false`
- `requires_token: false`
- `token_env: APIFY_TOKEN`
- `login_bypass: false`
- `paywall_bypass: false`
- `private_content_scraping: false`
- `stores_cookies: false`
- `requires_human_review: true`

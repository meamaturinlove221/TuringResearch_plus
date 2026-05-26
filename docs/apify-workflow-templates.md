# Apify Workflow Templates

Status: v1.3 template set.

Round: 274.

This round adds review-only workflow templates for the optional Apify adapter.
They are examples for public web workflows and are not executed by default.

## Templates

| Template | Purpose | Live default |
| --- | --- | --- |
| `examples/apify_workflows/project_page_fetch.yaml` | Fetch one public project page | false |
| `examples/apify_workflows/search_result_fetch.yaml` | Fetch public search result metadata | false |
| `examples/apify_workflows/content_extract.yaml` | Extract public article-like content | false |

## Token Policy

APIFY_TOKEN is optional and not required for fake/default review. Templates
name the environment variable only; they do not contain a token.

Live use must be private opt-in:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
Set APIFY_TOKEN in your private local shell or secret manager.
```

Do not commit private values.

## Safety Boundary

- live disabled by default;
- no key in examples;
- no login bypass;
- no paywall bypass;
- no private content scraping;
- no cookie storage;
- no automatic evidence promotion;
- retrieved content requires human review.

## Relationship To Web Tool Surface

These templates support `web.apify_optional` in the v1.3 Web full tool surface.
They do not replace `web.web_fetching`, do not create a crawler, and do not
turn fetched content into verified evidence.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_apify_workflow_templates.py -q
```

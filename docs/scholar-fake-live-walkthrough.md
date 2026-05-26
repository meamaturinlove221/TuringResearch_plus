# Scholar Fake / Live Walkthrough

Status: v1.3 walkthrough.

Round: 272.

This walkthrough shows how to use the Scholar tool surface in fake/default mode
and how live mode would be opted into privately. This round does not require or
run live access.

## Fake Mode

Fake mode is the default.

You can run the Scholar tool surface without any provider key:

```powershell
python -m pytest tests/workflow/test_scholar_fake_live_walkthrough.py -q
```

The fake walkthrough uses:

- `examples/scholar_demo/fake_paper_search.json`
- `examples/scholar_demo/fake_paper_content.md`
- `examples/scholar_demo/fake_reference_report.md`

It demonstrates:

- `scholar.paper_searching`
- `scholar.paper_content`
- `scholar.paper_reference`
- `scholar.paper_reading`

## Live Mode

Live mode is opt-in only. It must be configured in private local environment
settings, never in committed repository files.

Private local shape:

```text
TURINGRESEARCH_MODE=live
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1
SEMANTIC_SCHOLAR_API_KEY=<private local value>
```

This repository does not require the key for fake mode and does not include any
real key.

## Safety Boundaries

- fake mode default;
- live mode opt-in;
- no API key required for fake;
- no automatic paper download;
- no paywall bypass;
- no MinerU or heavy OCR;
- no final paper conclusion;
- no fake citation is marked as verified.

## Interpretation

Fake search and fake references are walkthrough material. They are not observed
research evidence, not verified citations, and not final paper references.
Human review is required before any live or cached paper material can support a
public claim.

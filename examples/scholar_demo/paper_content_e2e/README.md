# Paper Content E2E Demo

Status: fake/demo only.

This demo shows the local `scholar.paper_content` workflow:

1. Start with a paper id, public URL string, and cached Markdown file.
2. Read cached Markdown through the paper content tool.
3. Convert the cached content into a conservative method-card input.
4. Keep the output as review-only material.

The demo does not download papers, bypass paywalls, require an API key, run OCR,
or mark fake paper notes as verified evidence.

Files:

- `cached_paper.md`: local cached Markdown fixture.
- `method_card_input.json`: review-only method-card input descriptor.
- `content_to_method_card_report.md`: human-readable fake E2E report.

# Paper Source Fallback Policy

Status: v1.2 Scholar parity policy.

Round: 237.

## Allowed Fallbacks

- Cached Markdown, when already available locally.
- Known arXiv metadata or URL, without full paper download.
- Semantic Scholar fake adapter by default.
- Semantic Scholar live adapter only after explicit private opt-in.
- Manual reference list or manual paper notes.

## Deferred

- MinerU or other heavy PDF fallback.
- Heavy OCR pipeline.
- Automated full paper extraction.

## Rejected

- Paywall bypass.
- Automatic full paper download.
- Final paper conclusions from fallback material.
- Marking cached/fake material as human-verified.

## Review Rule

Every fallback source remains `requires_human_review`. It can help organize
paper work, but it cannot certify citations, related work, method claims, or
final conclusions.

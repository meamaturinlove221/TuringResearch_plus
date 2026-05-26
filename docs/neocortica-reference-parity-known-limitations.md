# Neocortica Reference Parity Known Limitations

Status: v1.2 known limitations.

Round: 241.

## Current Limitations

- Session parity is a safety layer, not a remote executor.
- Scholar parity does not implement MinerU, heavy OCR, automatic full paper
  download, paywall bypass, or final paper conclusions.
- Web parity does not enable default networking, private content fetching,
  cookie storage, or paywall bypass.
- Apify live mode is optional and requires private local opt-in.
- MCP config parity keeps live adapters disabled by default.
- Skill SOP parity is documentation/routing only; it does not execute skills.
- Upstream strict diff still depends on a future resolved baseline scan for
  change-specific implementation claims.

## Not Release Blockers

These limitations are intentional v1.2 boundaries. They block unsafe
over-expansion, but they do not block fake/default local parity tests.

## Still Requires Review

- Any live provider use.
- Any remote execution design.
- Any automatic evidence ledger mutation.
- Any plugin enablement.
- Any public release or child repository action.

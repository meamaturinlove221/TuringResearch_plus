# Web Production Parity Go / No-Go

Round: 312.

## Go

GO for v1.4 fake/default Web production parity:

- URL normalization pass.
- cache manifest pass.
- content fixtures pass.
- Apify fake/live report pass.
- Web extraction demo can run without live network.
- Apify fake integration can run without token.
- Human review remains required.

## No-Go

NO-GO for default live network:

- no default live Web fetch;
- no default live Apify request;
- no committed API key or token;
- no private scraping;
- no login bypass;
- no paywall bypass;
- no cookie storage;
- no automatic evidence promotion;
- no automatic claim verification.

## Remaining Review Items

- Live Web and live Apify tests may be run only by a maintainer in a private
  environment with explicit opt-in.
- Live outputs must not be committed as verified evidence without separate
  human review.
- Cache manifests remain provenance records, not source-truth certificates.

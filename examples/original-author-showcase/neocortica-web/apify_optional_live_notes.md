# Apify Optional Live Showcase

## Source

- Upstream repository: `Pthahnix/Neocortica-Web`
- Source basis: Apify optional integration, MCP env-block pattern, and live test policy
- Upstream reference commit: `94449c7b77241d97f052b462c397caa5aab654c0`
- Migration type: `adapted_with_authorization`
- Code migration: none

## Summary

This academic/product workflow output shows how an external web collection service can be connected without making the whole project depend on live credentials. The important pattern is optional-live operation: fake fixtures are available by default, while live calls require explicit environment variables and safety review.

## Pattern

1. Public demo uses fake fixtures.
2. Live mode requires an explicit token.
3. CI skips live tests by default.
4. Live output must pass redaction before entering reports.
5. Private or login-protected scraping is not supported.
6. README must tell users that live adapters are optional.

## TuringResearch Demonstration

This maps to:

- optional live scope;
- web/apify fake smoke;
- live output redaction gate;
- no-dotenv policy;
- public MCP config guide;
- upstream watch optional live backend.

## Safety Boundary

No token, API key, real Apify actor output, private scraping target, or login-protected content is included.

## Attribution

Adapted with attribution from authorized Neocortica-Web workflow materials.

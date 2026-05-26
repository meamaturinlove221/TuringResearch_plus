# Static Hosting Deployment Plan

Status: plan only.

Round: 332.

This plan covers Cloudflare Pages / Netlify style static hosting as an
alternative to GitHub Pages. v1.5 does not use these providers, create accounts,
upload artifacts, configure environment variables, or publish a URL.

## When This Route Helps

Static hosting providers can be useful later if the project needs:

- preview deployments for reviewed branches;
- redirects or headers;
- custom domain controls;
- deployment previews for docs reviewers;
- provider-side static asset handling.

Those benefits are not required for the v1.5 target.

## Provider-Neutral Build Input

The provider should receive only reviewed static docs output generated from:

- `docs-site/site_manifest.yaml`;
- `docs-site/nav.yaml`;
- `docs-site/pages/*.md`;
- reviewed public source docs;
- fake/demo examples that pass public-safety checks.

No provider should receive raw research data, secrets, live credentials, private
local paths, restricted model payloads, or internal-only artifacts.

## Deployment Guardrails

- Do not configure analytics by default.
- Do not store provider tokens in examples or docs.
- Do not use environment variables for the public docs build unless a future
  reviewed workflow requires them.
- Do not scrape or fetch live content during docs build.
- Do not publish preview URLs as official release URLs until human review.
- Do not deploy pages that imply an ARIS runtime exists.

## Comparison With GitHub Pages

| Area | GitHub Pages | Cloudflare / Netlify style hosting |
| --- | --- | --- |
| Setup surface | smaller for a GitHub repo | larger provider surface |
| Preview support | possible, usually more workflow work | strong provider previews |
| Secret risk | lower if no Actions secrets | higher if provider tokens enter config |
| Best v1.5 use | recommended prep target | documented future option |

## Recommendation

Keep this route documented but secondary. It is useful if the project later
needs previews or custom hosting, but v1.5 should avoid provider complexity and
stay GitHub Pages-ready only.

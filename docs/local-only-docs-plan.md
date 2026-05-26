# Local-only Docs Plan

Status: supported fallback.

Round: 332.

Local-only docs remain the safest default and the primary review path before
any public deployment. This plan keeps the current docs-site useful without
publishing anything.

## Local-only Flow

1. Keep source docs in `README.md`, `docs/`, `examples/`, and `split_ready/`.
2. Use `docs-site/nav.yaml` as the reviewed navigation layer.
3. Build static output locally with the Python builder.
4. Review `docs-site/output/` in a browser or file viewer.
5. Run public-safety scans before sharing any bundle externally.

## Why Keep Local-only

- No cloud account required.
- No live URL.
- No analytics.
- No public exposure of accidental files.
- Good for interview walkthroughs and release review.
- Good fallback if v1.5 decides not to publish.

## Safety Requirements

- Public/demo docs only.
- No credentials.
- No raw private data.
- No private local paths.
- No restricted model files.
- No fake result promoted to observed evidence.
- No unsupported experiment success claim.
- No ARIS implementation claim.

## Output Forms

Local-only docs can be reviewed as:

- repository Markdown;
- generated static HTML in `docs-site/output/`;
- a manually inspected no-deploy release bundle;
- an interview demo pack.

## Recommendation

Keep local-only docs fully supported even if GitHub Pages readiness improves.
It is the safest review mode and the best guard against accidental public
externalization.

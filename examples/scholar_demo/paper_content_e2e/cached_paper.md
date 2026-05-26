# Cache-First Paper Content Fixture

Paper ID: `fake-paper-content-e2e`

URL: `https://example.org/fake-paper-content-e2e`

This fixture represents cached Markdown that already exists locally. It is used
to test the paper content path without downloading a paper or calling a live
provider.

core method: Cache-first content review route that turns cached paper notes into
a conservative method-card input.

training objective: Not evaluated in this fake demo.

## Inputs

- cached Markdown note
- public paper identifier
- public URL string

## Outputs

- paper content preview
- method-card input scaffold
- review checklist

## Representation

- cached Markdown
- method-card scaffold

## Inference Pipeline

- read local cached Markdown
- extract conservative sections
- require human review before downstream use

## Key Figures

- none in fake fixture

## Key Tables

- none in fake fixture

## What To Borrow

- Cache-first workflow shape.
- Human-review boundary around paper-derived claims.

## What Not To Copy

- Do not treat fake cached content as verified citation evidence.
- Do not produce final paper conclusions from this fixture.

## References

- Fake Reference A. This is a demo-only reference placeholder.

## Limitations

- Fake/demo fixture only.
- No live provider query was made.
- No full paper was downloaded.
- Human review is required.

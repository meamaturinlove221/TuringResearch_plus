# Cloud Object Artifact Index

Status: v0.4 minimal implementation.

Cloud Object Artifact Index describes S3 / R2 / OSS / GCS-style research
artifacts through a provider-neutral manifest. It does not use real cloud SDKs,
does not store credentials, and does not download object payloads by default.

## Scope

The minimal implementation supports:

- provider-neutral object metadata;
- fake object store listing;
- local JSON fixture index;
- object key, size, optional hash, content type, status, omitted reason, and
  evidence tags;
- large-object metadata-only handling;
- unsafe object reporting;
- proposed imports only.

## Output

`ObjectArtifactIndex` contains:

- `provider`
- `bucket_or_container`
- `prefix`
- `objects`
- `size`
- `hash`
- `content_type`
- `status`
- `omitted_reason`
- `evidence_tags`
- `requires_human_review`

## Safety Rules

- No real cloud SDK integration in the minimal implementation.
- No credential storage.
- No default object download.
- No large file download.
- No raw data download.
- Unsafe objects are omitted or metadata-only.
- Object-store results are indexed, not verified.
- Evidence Ledger updates remain proposed imports only.

## Provider Neutrality

The model can represent S3, R2, OSS, GCS, or generic object storage. Provider
adapters can be added later behind explicit live policies and credential
handling rules.

## VGGT Use

For VGGT / Modal review, object stores should expose thin outputs such as
`final_status.json`, `failure_report.md`, `artifact_index.md`, board inventories,
sha256 manifests, and advisor notes. Large arrays, raw datasets, body model
files, and private configs remain omitted or metadata-only.

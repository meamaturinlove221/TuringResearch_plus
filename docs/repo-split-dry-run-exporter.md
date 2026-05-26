# Repo Split Dry-run Exporter

Status: implemented minimal.

Round: 168.

The repo split dry-run exporter prepares a local export directory for a future
split candidate. It is intentionally conservative: it copies only public-safe
text-like files, writes `split_manifest.yaml`, writes `safety_report.md`, and
does not create GitHub repositories or push git remotes.

## Scope

The first supported use case is exporting split candidate skeletons from
`examples/split_repos/` into `examples/split_exports/` or another local
temporary directory.

Supported outputs:

- copied public-safe files;
- `split_manifest.yaml`;
- `safety_report.md`.

## Safety Rules

The exporter blocks or omits files when they look unsafe for public split
review:

- secrets or token-like values;
- `.env` files;
- `local_project_links.yaml`;
- raw-data markers;
- SMPL-X or model payload file patterns;
- large binary payloads;
- unsupported suffixes;
- paths outside the candidate source root.

Policy text that says a private item is excluded can be recorded as a
non-blocking warning. That keeps safety docs readable without treating the
warning sentence itself as leaked payload.

## What It Does Not Do

- It does not create GitHub repositories.
- It does not run `git push`.
- It does not create branches.
- It does not publish releases.
- It does not package raw data or model files.
- It does not claim a case study is ready for publication.

## Example

```python
from pathlib import Path

from turing_research_plus.repo_split import RepoSplitDryRunRequest, export_split_dry_run

root = Path.cwd()
result = export_split_dry_run(
    RepoSplitDryRunRequest(
        candidate_id="turingresearch-vggt-case",
        source_root=root / "examples" / "split_repos" / "turingresearch-vggt-case",
        output_root=root / "examples" / "split_exports",
    )
)

print(result.status)
print(result.export_dir)
```

## Committed Fixture

`examples/split_exports/turingresearch-vggt-case/` is a dry-run fixture. It
contains only the public-safe skeleton files plus generated manifest and safety
report.

The fixture is not a real split repository and is not pushed anywhere.

## Review Requirement

Human review remains required before any physical split. A passing dry-run only
means the local export tree is structurally safe enough for review.

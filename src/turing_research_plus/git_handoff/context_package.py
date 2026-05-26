"""Build Git-based context handoff packages."""

from __future__ import annotations

import hashlib
import json

from turing_research_plus.git_handoff.memory_policy import (
    render_memory_policy,
    validate_memory_text,
)
from turing_research_plus.git_handoff.models import (
    ContextFile,
    ContextPackage,
    ContextPackageBuildInput,
    ContextPackageFileName,
    OmittedContextItem,
)
from turing_research_plus.git_handoff.safety import safety_warnings_for_text


def build_context_package(request: ContextPackageBuildInput) -> ContextPackage:
    """Write a context package and return package metadata."""

    package_dir = request.output_dir
    package_dir.mkdir(parents=True, exist_ok=True)
    handoff_manifest_text = _handoff_manifest_text(request)
    readme_text = request.readme_text or _readme_text(request)
    files = {
        ContextPackageFileName.PROJECT_CONTEXT.value: request.project_context,
        ContextPackageFileName.MEMORY.value: _memory_text(request.memory_summary),
        ContextPackageFileName.ROUTE_SPEC.value: request.route_spec_text,
        ContextPackageFileName.HARD_GATES.value: request.hard_gates_text,
        ContextPackageFileName.ARTIFACT_REQUIREMENTS.value: request.artifact_requirements_text,
        ContextPackageFileName.FAILURE_TAXONOMY.value: request.failure_taxonomy_text,
        ContextPackageFileName.ADVISOR_INTENT.value: request.advisor_intent,
        ContextPackageFileName.HANDOFF_MANIFEST.value: handoff_manifest_text,
        ContextPackageFileName.README.value: readme_text,
    }
    warnings: list[str] = []
    omitted: list[OmittedContextItem] = []
    context_files: list[ContextFile] = []
    manifest: dict[str, str] = {}

    for filename, text in files.items():
        text_warnings = safety_warnings_for_text(text)
        if filename == ContextPackageFileName.MEMORY.value:
            text_warnings.extend(validate_memory_text(text))
        if _fatal_warnings(text_warnings):
            omitted.append(
                OmittedContextItem(
                    item=filename,
                    reason="unsafe context text omitted",
                    safety_warnings=list(dict.fromkeys(text_warnings)),
                )
            )
            warnings.extend(text_warnings)
            continue
        path = package_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        digest = _sha256_text(text)
        manifest[filename] = digest
        context_files.append(
            ContextFile(
                relative_path=filename,
                sha256=digest,
                source_ref=request.source_refs.get(filename),
                generated=True,
            )
        )
        warnings.extend(text_warnings)

    (package_dir / "SHA256SUMS.txt").write_text(
        "\n".join(f"{digest}  {name}" for name, digest in sorted(manifest.items())) + "\n",
        encoding="utf-8",
    )
    (package_dir / "context_package.json").write_text(
        json.dumps(
            {
                "package_id": request.package_id,
                "project_name": request.project_name,
                "route_id": request.route_id,
                "context_files": list(manifest),
                "requires_human_review": True,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    return ContextPackage(
        package_id=request.package_id,
        project_name=request.project_name,
        route_id=request.route_id,
        context_files=context_files,
        safety_warnings=sorted(set(warnings)),
        omitted_items=omitted,
        sha256_manifest=manifest,
        requires_human_review=True,
    )


def _memory_text(summary: str) -> str:
    return "\n".join(
        [
            "# MEMORY",
            "",
            summary.strip(),
            "",
            render_memory_policy().strip(),
        ]
    ) + "\n"


def _readme_text(request: ContextPackageBuildInput) -> str:
    return "\n".join(
        [
            f"# Pod Context Package: {request.package_id}",
            "",
            "This package is a review-only TuringResearch Plus context handoff.",
            "",
            f"- Route: `{request.route_id}`",
            "- Status: planned",
            "- Execution: not executed by TuringResearch",
            "- Requires real experiment: true",
            "",
            "Use the structured output template for any returned pod outputs.",
        ]
    ) + "\n"


def _handoff_manifest_text(request: ContextPackageBuildInput) -> str:
    payload = {
        "package_id": request.package_id,
        "project_name": request.project_name,
        "route_id": request.route_id,
        "transport": "git",
        "remote_execution_allowed": False,
        "forbidden": [".env", "API keys", "raw data", "SMPL-X body model files"],
        "requires_human_review": True,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _fatal_warnings(warnings: list[str]) -> bool:
    return any(
        warning.startswith("possible-secret-value")
        for warning in warnings
    )

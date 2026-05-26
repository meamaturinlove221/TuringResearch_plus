"""Read-only case study gallery helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Self, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CaseGalleryItem(BaseModel):
    """One public-safe case gallery entry."""

    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    research_type: str = Field(min_length=1)
    demo_status: str = Field(min_length=1)
    privacy_level: str = Field(min_length=1)
    available_artifacts: list[str] = Field(default_factory=list)
    dashboard_link: str = Field(min_length=1)
    advisor_pack_link: str = Field(min_length=1)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def gallery_item_must_stay_public_demo(self) -> Self:
        if self.demo_status != "demo-only":
            raise ValueError("case gallery item must be demo-only")
        if self.privacy_level not in {"public-demo", "public-safe-case"}:
            raise ValueError("case gallery item must be public-safe")
        if not self.requires_human_review:
            raise ValueError("case gallery item requires human review")
        if self.dashboard_link.startswith(("http://", "https://")):
            raise ValueError("case gallery must not use fake external URLs")
        if self.advisor_pack_link.startswith(("http://", "https://")):
            raise ValueError("case gallery must not use fake external URLs")
        return self


class CaseGalleryManifest(BaseModel):
    """Public case gallery manifest."""

    model_config = ConfigDict(extra="forbid")

    gallery_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    cases: list[CaseGalleryItem] = Field(min_length=1)
    source_of_truth: str = "examples/public_demo"
    requires_human_review: bool = True
    published: bool = False

    @model_validator(mode="after")
    def gallery_must_not_publish(self) -> Self:
        if self.published:
            raise ValueError("case gallery must not publish external repos")
        if not self.requires_human_review:
            raise ValueError("case gallery requires human review")
        case_ids = [item.case_id for item in self.cases]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError("case gallery ids must be unique")
        return self


def load_case_gallery_manifest(path: Path) -> CaseGalleryManifest:
    """Load the minimal gallery manifest YAML shape."""

    data = _parse_gallery_yaml(path.read_text(encoding="utf-8"))
    return CaseGalleryManifest(
        gallery_id=str(data["gallery_id"]),
        status=str(data["status"]),
        source_of_truth=str(data.get("source_of_truth", "examples/public_demo")),
        requires_human_review=bool(data.get("requires_human_review", True)),
        published=bool(data.get("published", False)),
        cases=[
            CaseGalleryItem(
                case_id=str(item["case_id"]),
                title=str(item["title"]),
                domain=str(item["domain"]),
                research_type=str(item["research_type"]),
                demo_status=str(item["demo_status"]),
                privacy_level=str(item["privacy_level"]),
                available_artifacts=[
                    str(value)
                    for value in cast(list[object], item.get("available_artifacts", []))
                ],
                dashboard_link=str(item["dashboard_link"]),
                advisor_pack_link=str(item["advisor_pack_link"]),
                limitations=[
                    str(value)
                    for value in cast(list[object], item.get("limitations", []))
                ],
                requires_human_review=bool(item.get("requires_human_review", True)),
            )
            for item in cast(list[dict[str, object]], data["cases"])
        ],
    )


def render_case_gallery_markdown(manifest: CaseGalleryManifest) -> str:
    """Render the case gallery as Markdown."""

    lines = [
        "# Case Study Gallery",
        "",
        f"Status: {manifest.status}.",
        "",
        "This gallery lists public-safe demo and case-study entries. It does not",
        "publish child repositories or claim experiment success.",
        "",
        "| Case | Domain | Research type | Status | Privacy | Dashboard | Advisor pack |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in manifest.cases:
        lines.append(
            "| "
            f"`{item.case_id}` | {item.domain} | {item.research_type} | "
            f"{item.demo_status} | {item.privacy_level} | "
            f"`{item.dashboard_link}` | `{item.advisor_pack_link}` |"
        )
    lines.extend(["", "## Case Details", ""])
    for item in manifest.cases:
        lines.extend(
            [
                f"### {item.title}",
                "",
                f"- Case id: `{item.case_id}`",
                f"- Domain: {item.domain}",
                f"- Research type: {item.research_type}",
                f"- Demo status: `{item.demo_status}`",
                f"- Privacy level: `{item.privacy_level}`",
                "- Available artifacts:",
                *[f"  - `{artifact}`" for artifact in item.available_artifacts],
                "- Limitations:",
                *[f"  - {limitation}" for limitation in item.limitations],
                "- Requires human review: `true`",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "- Gallery entries are demo-only or public-safe case-study material.",
            "- Demo outputs are not observed research evidence.",
            "- No private data, raw data, credentials, or private local paths are included.",
            "- External child repositories are not implied by this gallery.",
            "",
        ]
    )
    return "\n".join(lines)


def _parse_gallery_yaml(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    cases: list[dict[str, object]] = []
    current_case: dict[str, object] | None = None
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            current_case = None
            current_list_key = None
            if line.endswith(":"):
                key = line[:-1]
                if key == "cases":
                    data["cases"] = cases
                continue
            key, value = _split_scalar(line)
            data[key] = _parse_scalar(value)
            continue

        stripped = line.strip()
        if stripped.startswith("- case_id: "):
            current_case = {"case_id": stripped.split(": ", 1)[1]}
            cases.append(current_case)
            current_list_key = None
            continue
        if current_case is None:
            continue
        if stripped.endswith(":") and not stripped.startswith("- "):
            current_list_key = stripped[:-1]
            current_case[current_list_key] = []
            continue
        if current_list_key and stripped.startswith("- "):
            cast(list[str], current_case[current_list_key]).append(stripped[2:])
            continue
        if ": " in stripped:
            key, value = _split_scalar(stripped)
            current_case[key] = _parse_scalar(value)
            current_list_key = None

    data["cases"] = cases
    return data


def _split_scalar(line: str) -> tuple[str, str]:
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> object:
    if value == "true":
        return True
    if value == "false":
        return False
    return value.strip('"').strip("'")

"""Race Mode Upstream Watch for public upstream snapshots."""

from __future__ import annotations

from enum import StrEnum
from hashlib import sha256
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.race.idea_radar import IdeaRadarInput, extract_idea
from turing_research_plus.race.models import IdeaCard
from turing_research_plus.race.source_hygiene import (
    SourceHygieneCheckResult,
    SourceHygieneDecision,
    SourceMaterial,
    source_hygiene_check,
)


class WatchDimension(StrEnum):
    """Supported upstream watch dimensions."""

    NEW_RELEASE = "new_release"
    README_CHANGED = "readme_changed"
    DOCS_ADDED = "docs_added"
    NEW_EXAMPLES = "new_examples"
    NEW_FEATURE_BRANCH = "new_feature_branch"
    NEW_MCP_TOOL = "new_mcp_tool"
    NEW_ARCHITECTURE_DIAGRAM = "new_architecture_diagram"
    SUDDEN_STARS_FORKS_INCREASE = "sudden_stars_forks_increase"
    ISSUE_DISCUSSION_SUGGESTS_ROADMAP = "issue_discussion_suggests_roadmap"
    VERSION_ANOMALY = "version_anomaly"


class UpstreamSnapshot(BaseModel):
    """Public upstream project snapshot."""

    model_config = ConfigDict(extra="forbid")

    snapshot_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    version: str | None = None
    readme_hash: str | None = None
    docs_files: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    branches: list[str] = Field(default_factory=list)
    mcp_tools: list[str] = Field(default_factory=list)
    architecture_diagrams: list[str] = Field(default_factory=list)
    stars: int = Field(default=0, ge=0)
    forks: int = Field(default=0, ge=0)
    issue_keywords: list[str] = Field(default_factory=list)
    release_notes: str = ""


class UpstreamWatchItem(BaseModel):
    """One upstream change signal."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(min_length=1)
    dimension: WatchDimension
    summary: str = Field(min_length=1)
    severity: str = Field(default="watch", min_length=1)
    evidence: EvidenceRef
    recommended_action: str = Field(default="watch", min_length=1)


class UpstreamWatchInput(BaseModel):
    """Input for race.upstream_watch."""

    model_config = ConfigDict(extra="forbid")

    source: SourceMaterial
    previous_snapshot: UpstreamSnapshot | None = None
    current_snapshot: UpstreamSnapshot
    report_dir: Path = Path("race/upstream_reports")
    write_reports: bool = False
    generate_idea_cards: bool = False


class UpstreamWatchReport(BaseModel):
    """Upstream watch report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    source_hygiene: SourceHygieneCheckResult
    watch_items: list[UpstreamWatchItem] = Field(default_factory=list)
    idea_cards: list[IdeaCard] = Field(default_factory=list)
    report_markdown_path: Path | None = None
    report_json_path: Path | None = None
    skipped_reason: str | None = None

    def to_markdown(self) -> str:
        """Render the report as Markdown."""

        lines = [
            f"# TuringResearch Plus Upstream Watch: {self.project_name}",
            "",
            f"- Report ID: `{self.report_id}`",
            f"- Source hygiene: `{self.source_hygiene.decision}`",
        ]
        if self.skipped_reason:
            lines.append(f"- Skipped reason: {self.skipped_reason}")
        lines.extend(["", "## Watch Items"])
        if not self.watch_items:
            lines.append("- No upstream watch changes detected.")
        for item in self.watch_items:
            lines.append(f"- `{item.dimension}`: {item.summary} ({item.recommended_action})")
        lines.extend(["", "## Optional IdeaCards"])
        if not self.idea_cards:
            lines.append("- None")
        for idea in self.idea_cards:
            lines.append(f"- `{idea.idea_id}`: {idea.title}")
        return "\n".join(lines) + "\n"


def upstream_watch(input_data: UpstreamWatchInput) -> UpstreamWatchReport:
    """Compare public upstream snapshots and generate watch items."""

    hygiene = source_hygiene_check([input_data.source])
    report_id = _report_id(input_data.current_snapshot)
    markdown_path = input_data.report_dir / f"{report_id}.md"
    json_path = input_data.report_dir / f"{report_id}.json"
    if hygiene.decision == SourceHygieneDecision.BLOCK:
        report = UpstreamWatchReport(
            report_id=report_id,
            project_name=input_data.current_snapshot.project_name,
            source_hygiene=hygiene,
            watch_items=[],
            report_markdown_path=markdown_path,
            report_json_path=json_path,
            skipped_reason="source hygiene blocked upstream watch",
        )
        _maybe_write_reports(report, input_data)
        return report

    items = _diff_snapshots(
        input_data.previous_snapshot,
        input_data.current_snapshot,
        input_data.source.evidence,
    )
    idea_cards = _idea_cards(input_data, hygiene, items)
    skipped_reason = None
    if hygiene.decision == SourceHygieneDecision.WATCH:
        skipped_reason = "unknown or unclear source is watch-only"
        idea_cards = []
    report = UpstreamWatchReport(
        report_id=report_id,
        project_name=input_data.current_snapshot.project_name,
        source_hygiene=hygiene,
        watch_items=items,
        idea_cards=idea_cards,
        report_markdown_path=markdown_path,
        report_json_path=json_path,
        skipped_reason=skipped_reason,
    )
    _maybe_write_reports(report, input_data)
    return report


def race_upstream_watch(input_data: UpstreamWatchInput) -> dict[str, object]:
    """Thin race.upstream_watch wrapper."""

    return upstream_watch(input_data).model_dump(mode="json")


def _diff_snapshots(
    previous: UpstreamSnapshot | None,
    current: UpstreamSnapshot,
    evidence: EvidenceRef,
) -> list[UpstreamWatchItem]:
    if previous is None:
        return [
            _item(
                current,
                WatchDimension.NEW_RELEASE,
                "Initial public upstream snapshot captured.",
                evidence,
            )
        ]
    items: list[UpstreamWatchItem] = []
    if current.version and current.version != previous.version:
        items.append(
            _item(
                current,
                WatchDimension.NEW_RELEASE,
                f"Release changed to {current.version}.",
                evidence,
            )
        )
        if _version_anomaly(previous.version, current.version):
            items.append(
                _item(
                    current,
                    WatchDimension.VERSION_ANOMALY,
                    f"Version changed suspiciously from {previous.version} to {current.version}.",
                    evidence,
                    severity="risk",
                )
            )
    if current.readme_hash and current.readme_hash != previous.readme_hash:
        items.append(
            _item(
                current,
                WatchDimension.README_CHANGED,
                "README content changed.",
                evidence,
            )
        )
    for value in sorted(set(current.docs_files) - set(previous.docs_files)):
        items.append(
            _item(current, WatchDimension.DOCS_ADDED, f"New docs file: {value}.", evidence)
        )
    for value in sorted(set(current.examples) - set(previous.examples)):
        items.append(
            _item(current, WatchDimension.NEW_EXAMPLES, f"New example: {value}.", evidence)
        )
    for value in sorted(set(current.branches) - set(previous.branches)):
        if "feature" in value.lower():
            items.append(
                _item(
                    current,
                    WatchDimension.NEW_FEATURE_BRANCH,
                    f"New feature branch: {value}.",
                    evidence,
                )
            )
    for value in sorted(set(current.mcp_tools) - set(previous.mcp_tools)):
        items.append(
            _item(current, WatchDimension.NEW_MCP_TOOL, f"New MCP tool: {value}.", evidence)
        )
    for value in sorted(set(current.architecture_diagrams) - set(previous.architecture_diagrams)):
        items.append(
            _item(
                current,
                WatchDimension.NEW_ARCHITECTURE_DIAGRAM,
                f"New architecture diagram: {value}.",
                evidence,
            )
        )
    if _sudden_growth(previous, current):
        items.append(
            _item(
                current,
                WatchDimension.SUDDEN_STARS_FORKS_INCREASE,
                "Stars or forks increased sharply.",
                evidence,
                severity="risk",
            )
        )
    if any("roadmap" in keyword.lower() for keyword in current.issue_keywords):
        items.append(
            _item(
                current,
                WatchDimension.ISSUE_DISCUSSION_SUGGESTS_ROADMAP,
                "Public issue discussion suggests roadmap movement.",
                evidence,
            )
        )
    return items


def _idea_cards(
    input_data: UpstreamWatchInput,
    hygiene: SourceHygieneCheckResult,
    items: list[UpstreamWatchItem],
) -> list[IdeaCard]:
    if not input_data.generate_idea_cards or hygiene.decision != SourceHygieneDecision.ALLOW:
        return []
    cards: list[IdeaCard] = []
    for item in items:
        if item.dimension in {
            WatchDimension.NEW_MCP_TOOL,
            WatchDimension.NEW_ARCHITECTURE_DIAGRAM,
            WatchDimension.NEW_RELEASE,
        }:
            result = extract_idea(
                IdeaRadarInput(
                    text=item.summary,
                    source=input_data.source,
                    source_hygiene=hygiene,
                )
            )
            cards.extend(result.ideas)
    return cards


def _maybe_write_reports(report: UpstreamWatchReport, input_data: UpstreamWatchInput) -> None:
    if not input_data.write_reports:
        return
    input_data.report_dir.mkdir(parents=True, exist_ok=True)
    if report.report_markdown_path is not None:
        report.report_markdown_path.write_text(report.to_markdown(), encoding="utf-8")
    if report.report_json_path is not None:
        report.report_json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")


def _item(
    snapshot: UpstreamSnapshot,
    dimension: WatchDimension,
    summary: str,
    evidence: EvidenceRef,
    severity: str = "watch",
) -> UpstreamWatchItem:
    digest = sha256(f"{snapshot.snapshot_id}:{dimension}:{summary}".encode()).hexdigest()[:12]
    action = "watch"
    if severity == "risk":
        action = "document"
    return UpstreamWatchItem(
        item_id=f"watch-{digest}",
        dimension=dimension,
        summary=summary,
        severity=severity,
        evidence=evidence,
        recommended_action=action,
    )


def _report_id(snapshot: UpstreamSnapshot) -> str:
    digest = sha256(f"{snapshot.project_name}:{snapshot.snapshot_id}".encode()).hexdigest()[:12]
    return f"upstream-{digest}"


def _version_anomaly(previous: str | None, current: str | None) -> bool:
    previous_parts = _version_parts(previous)
    current_parts = _version_parts(current)
    if previous_parts is None or current_parts is None:
        return bool(previous and current and current < previous)
    return current_parts < previous_parts or current_parts[0] - previous_parts[0] > 1


def _version_parts(value: str | None) -> tuple[int, int, int] | None:
    if value is None:
        return None
    cleaned = value.strip().lstrip("v")
    parts = cleaned.split(".")
    if not all(part.isdigit() for part in parts[:3]):
        return None
    padded = [int(part) for part in parts[:3]]
    while len(padded) < 3:
        padded.append(0)
    return padded[0], padded[1], padded[2]


def _sudden_growth(previous: UpstreamSnapshot, current: UpstreamSnapshot) -> bool:
    star_delta = current.stars - previous.stars
    fork_delta = current.forks - previous.forks
    return star_delta >= 100 or fork_delta >= 50

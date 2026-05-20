from pathlib import Path

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.race.models import RecommendedAction
from tuling_research_plus.race.source_hygiene import SourceKind, SourceMaterial
from tuling_research_plus.race.upstream_watch import (
    UpstreamSnapshot,
    UpstreamWatchInput,
    WatchDimension,
    race_upstream_watch,
    upstream_watch,
)


def evidence(source_id: str = "public-upstream") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="public-release-notes",
        quote="Public upstream release notes mention a new MCP tool.",
    )


def source(kind: SourceKind = SourceKind.PUBLIC_RELEASE_NOTES) -> SourceMaterial:
    return SourceMaterial(
        source_id="public-upstream",
        kind=kind,
        license="MIT",
        public=True if kind != SourceKind.UNKNOWN else None,
        authorized=True if kind != SourceKind.UNKNOWN else None,
        intended_use="concept",
        evidence=evidence("public-upstream"),
    )


def previous() -> UpstreamSnapshot:
    return UpstreamSnapshot(
        snapshot_id="snapshot-prev",
        project_name="Public Reference",
        version="1.2.0",
        readme_hash="readme-a",
        docs_files=["docs/start.md"],
        examples=["examples/basic.md"],
        branches=["main"],
        mcp_tools=["old.tool"],
        architecture_diagrams=[],
        stars=100,
        forks=20,
        issue_keywords=[],
    )


def current(**updates: object) -> UpstreamSnapshot:
    payload = {
        "snapshot_id": "snapshot-current",
        "project_name": "Public Reference",
        "version": "1.2.0",
        "readme_hash": "readme-a",
        "docs_files": ["docs/start.md"],
        "examples": ["examples/basic.md"],
        "branches": ["main"],
        "mcp_tools": ["old.tool"],
        "architecture_diagrams": [],
        "stars": 100,
        "forks": 20,
        "issue_keywords": [],
    }
    payload.update(updates)
    return UpstreamSnapshot(**payload)


def test_snapshot_diff_detects_readme_change() -> None:
    report = upstream_watch(
        UpstreamWatchInput(
            source=source(),
            previous_snapshot=previous(),
            current_snapshot=current(readme_hash="readme-b"),
        )
    )

    assert [item.dimension for item in report.watch_items] == [WatchDimension.README_CHANGED]


def test_new_release_produces_report(tmp_path: Path) -> None:
    report = upstream_watch(
        UpstreamWatchInput(
            source=source(),
            previous_snapshot=previous(),
            current_snapshot=current(version="1.3.0", release_notes="New public release."),
            report_dir=tmp_path,
            write_reports=True,
            generate_idea_cards=True,
        )
    )

    assert report.watch_items[0].dimension == WatchDimension.NEW_RELEASE
    assert report.idea_cards
    assert report.idea_cards[0].recommended_action in {
        RecommendedAction.IMPLEMENT,
        RecommendedAction.WATCH,
    }
    assert report.report_markdown_path is not None
    assert report.report_markdown_path.exists()
    assert report.report_json_path is not None
    assert report.report_json_path.exists()


def test_suspicious_version_change_produces_watch_item() -> None:
    report = upstream_watch(
        UpstreamWatchInput(
            source=source(),
            previous_snapshot=previous(),
            current_snapshot=current(version="0.9.0"),
        )
    )

    dimensions = {item.dimension for item in report.watch_items}

    assert WatchDimension.VERSION_ANOMALY in dimensions


def test_public_only_gate_blocks_private_source() -> None:
    private_source = SourceMaterial(
        source_id="private-upstream",
        kind=SourceKind.PRIVATE_REPO_CONTENT,
        license="proprietary",
        public=False,
        authorized=False,
        intended_use="concept",
        evidence=evidence("private-upstream"),
    )
    report = upstream_watch(
        UpstreamWatchInput(
            source=private_source,
            previous_snapshot=previous(),
            current_snapshot=current(readme_hash="readme-b"),
        )
    )

    assert report.watch_items == []
    assert report.skipped_reason == "source hygiene blocked upstream watch"
    assert report.source_hygiene.decision == "block"


def test_unknown_source_is_watch_only() -> None:
    report = upstream_watch(
        UpstreamWatchInput(
            source=source(SourceKind.UNKNOWN),
            previous_snapshot=previous(),
            current_snapshot=current(mcp_tools=["old.tool", "new.tool"]),
            generate_idea_cards=True,
        )
    )

    assert report.watch_items[0].dimension == WatchDimension.NEW_MCP_TOOL
    assert report.idea_cards == []
    assert report.skipped_reason == "unknown or unclear source is watch-only"


def test_race_upstream_watch_tool_returns_json_payload() -> None:
    payload = race_upstream_watch(
        UpstreamWatchInput(
            source=source(),
            previous_snapshot=previous(),
            current_snapshot=current(readme_hash="readme-b"),
        )
    )

    assert payload["watch_items"][0]["dimension"] == "readme_changed"

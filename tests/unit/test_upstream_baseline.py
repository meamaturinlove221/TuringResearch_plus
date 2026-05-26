from turing_research_plus.upstream.baseline import (
    build_repo_baseline,
    build_unresolved_repo_baseline,
    classify_repo_paths,
)


def test_classify_repo_paths_detects_watch_buckets() -> None:
    classified = classify_repo_paths(
        [
            "README.md",
            "ENTRY.md",
            "package.json",
            ".mcp.example.json",
            ".agents/skills/a/SKILL.md",
            "docs/architecture.md",
            "src/index.ts",
            "tests/test_index.ts",
            "examples/demo.md",
        ]
    )

    assert "README.md" in classified["root_files"]
    assert "ENTRY.md" in classified["markdown_files"]
    assert ".agents/skills/a/SKILL.md" in classified["skill_files"]
    assert "docs/architecture.md" in classified["docs_files"]
    assert "package.json" in classified["package_files"]
    assert ".mcp.example.json" in classified["mcp_config_files"]
    assert "src/index.ts" in classified["src_files"]
    assert "tests/test_index.ts" in classified["test_files"]


def test_build_repo_baseline_keeps_focus_file_hashes_only() -> None:
    baseline = build_repo_baseline(
        repository_full_name="org/repo",
        url="https://github.com/org/repo",
        default_branch="main",
        latest_commit_sha="abc",
        latest_commit_message="update",
        latest_commit_time="2026-05-20T00:00:00Z",
        paths=["README.md", "src/a.py", "assets/image.png"],
        file_hashes={"README.md": "r1", "src/a.py": "s1", "assets/image.png": "i1"},
    )

    assert baseline.file_hashes == {"README.md": "r1", "src/a.py": "s1"}
    assert baseline.resolved


def test_build_unresolved_repo_baseline_records_reason() -> None:
    baseline = build_unresolved_repo_baseline(
        repository_full_name="org/missing",
        url="https://github.com/org/missing",
        unresolved_reason="not found",
    )

    assert baseline.unresolved_reason == "not found"

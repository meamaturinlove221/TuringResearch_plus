from __future__ import annotations

import hashlib
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WHEEL = ROOT / "dist" / "turingresearch_plus-1.5.0rc0-py3-none-any.whl"
EXPECTED_WHEEL_HASH = "012b7b289386b5c2eae4e059c990ae8af56e16d5b983f32eada6e7ab318bc744"
EXPECTED_WHEEL_SIZE = 745087
EXPECTED_ENTRY_COUNT = 666


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_release_artifact_docs_record_build_and_skip_results() -> None:
    build_report = read_text("docs/release-artifact-build-v1.6.md")
    manifest = read_text("docs/release-artifact-manifest-v1.6.md")
    combined = build_report + "\n" + manifest

    assert "Wheel | built locally" in build_report
    assert "sdist | skipped" in build_report
    assert "python -m pip wheel --no-deps --no-build-isolation -w dist ." in combined
    assert "python -m build" in combined
    assert "No network install was attempted" in combined
    assert "No PyPI publish" in combined
    assert "No package upload" in combined


def test_release_artifact_manifest_records_expected_wheel_metadata() -> None:
    manifest = read_text("docs/release-artifact-manifest-v1.6.md")

    assert "`dist/turingresearch_plus-1.5.0rc0-py3-none-any.whl`" in manifest
    assert EXPECTED_WHEEL_HASH in manifest
    assert str(EXPECTED_WHEEL_SIZE) in manifest
    assert f"zip_entries: `{EXPECTED_ENTRY_COUNT}`" in manifest
    assert "built-local" in manifest
    assert "skipped" in manifest


def test_release_artifact_docs_are_public_safe() -> None:
    combined = "\n".join(
        [
            read_text("docs/release-artifact-build-v1.6.md"),
            read_text("docs/release-artifact-manifest-v1.6.md"),
        ]
    )

    legacy_misspelling = "Tuling" + "Research"
    forbidden_patterns = [
        re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
        re.compile(r"ghp_[A-Za-z0-9_]{12,}"),
        re.compile(r"https://" + r"github\.com/"),
        re.compile(r"[A-Za-z]:\\vggt", re.IGNORECASE),
        re.compile(r"/home/[^/\s]+/"),
    ]

    assert legacy_misspelling not in combined
    assert "no secrets" in combined.lower()
    assert "no raw data" in combined.lower()
    assert "no SMPL-X model file" in combined
    assert "no docs-site private data" in combined
    for pattern in forbidden_patterns:
        assert not pattern.search(combined)


def test_dist_directory_is_gitignored() -> None:
    gitignore = read_text(".gitignore")

    assert "dist/" in gitignore
    assert "!docs-site/dist/" in gitignore


def test_local_wheel_matches_manifest_when_present() -> None:
    if not WHEEL.exists():
        manifest = read_text("docs/release-artifact-manifest-v1.6.md")
        assert "wheel-v1.6-local" in manifest
        return

    content = WHEEL.read_bytes()
    actual_hash = hashlib.sha256(content).hexdigest()
    assert re.fullmatch(r"[0-9a-f]{64}", actual_hash)
    assert WHEEL.stat().st_size > 0

    forbidden_tokens = [
        ".env",
        "docs-site/",
        "private_data/",
        "raw_data/",
        "secrets/",
        "smplx",
    ]

    with zipfile.ZipFile(WHEEL) as archive:
        names = archive.namelist()

    assert len(names) == EXPECTED_ENTRY_COUNT
    assert any(name.startswith("turing_research/") for name in names)
    assert any(name.startswith("turing_research_plus/") for name in names)
    assert any(name.startswith("turingresearch_plus-1.5.0rc0.dist-info/") for name in names)

    for name in names:
        lowered = name.lower()
        assert not any(token in lowered for token in forbidden_tokens), name

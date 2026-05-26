from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

POLICY = ROOT / "docs" / "split-repo-url-placeholder-policy.md"
UPDATE = ROOT / "docs" / "split-repo-url-update-after-creation.md"
LANE = ROOT / "lanes" / "348_split_repo_url_placeholder_policy.md"
LEDGER = ROOT / "lanes" / "00_master_ledger.md"

SPLIT_MANUAL = ROOT / "split_manual"
SPLIT_READY = ROOT / "split_ready"

REMOTE_PLACEHOLDER = "<approved-real-repository-url>"
FLAGSHIP_PLACEHOLDER = (
    "TuringResearch main repository URL goes here after human publication approval"
)

FAKE_GITHUB_PATTERNS = [
    re.compile(r"https?://github\.com/(OWNER|owner|ORG|org|example|user|USERNAME)/"),
    re.compile(r"https?://github\.com/[^/\s]+/(turingresearch-vggt-case|turingresearch-examples)"),
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _squash(text: str) -> str:
    return " ".join(text.split())


def _iter_public_split_files() -> list[Path]:
    roots = [
        SPLIT_MANUAL / "turingresearch-vggt-case",
        SPLIT_MANUAL / "turingresearch-examples",
        SPLIT_READY / "turingresearch-vggt-case",
        SPLIT_READY / "turingresearch-examples",
    ]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(files)


def test_split_repo_url_policy_docs_exist() -> None:
    for path in [POLICY, UPDATE, LANE]:
        assert path.exists(), path.relative_to(ROOT).as_posix()


def test_split_repo_placeholder_policy_records_required_rules() -> None:
    policy = _text(POLICY)
    update = _text(UPDATE)
    combined = policy + "\n" + update

    assert REMOTE_PLACEHOLDER in combined
    assert FLAGSHIP_PLACEHOLDER in combined
    assert "Fake GitHub URLs are not allowed." in combined
    assert "After creation, docs must be updated manually" in combined
    assert "The main README must not imply that split repositories already exist." in combined
    assert "Child README files must point back to the flagship TuringResearch" in combined
    assert "The main TuringResearch repository remains the flagship." in combined


def test_split_manual_files_use_placeholders_not_fake_child_urls() -> None:
    files = _iter_public_split_files()
    assert files

    for path in files:
        text = _text(path)
        for pattern in FAKE_GITHUB_PATTERNS:
            assert pattern.search(text) is None, path.relative_to(ROOT).as_posix()


def test_split_manual_packs_keep_flagship_placeholder_until_creation() -> None:
    for repo in ["turingresearch-vggt-case", "turingresearch-examples"]:
        readme = _text(SPLIT_MANUAL / repo / "README.md")
        manifest = _text(SPLIT_MANUAL / repo / "manifest.yaml")
        final_create = _text(SPLIT_MANUAL / repo / "FINAL_CREATE_REPO.md")

        assert FLAGSHIP_PLACEHOLDER in _squash(readme)
        assert FLAGSHIP_PLACEHOLDER in manifest
        assert FLAGSHIP_PLACEHOLDER in final_create
        assert "writes_real_url: false" in manifest
        assert "creates_github_repo: false" in manifest
        assert "pushes_external_repo: false" in manifest


def test_split_push_commands_keep_remote_as_placeholder() -> None:
    for repo in ["turingresearch-vggt-case", "turingresearch-examples"]:
        for name in ["PUSH_COMMANDS.md", "FINAL_PUSH_COMMANDS.md", "GIT_INIT_DRY_RUN.md"]:
            path = SPLIT_MANUAL / repo / name
            text = _text(path)

            assert REMOTE_PLACEHOLDER in text
            assert "# git remote add origin <approved-real-repository-url>" in text
            assert "# git push -u origin main" in text
            for line in text.splitlines():
                assert not line.strip().startswith("git ")


def test_split_repo_url_policy_is_recorded_in_lane_and_ledger() -> None:
    lane = _text(LANE)
    ledger = _text(LEDGER)

    assert "Round 370 - Split Repo URL Placeholder Policy" in lane
    assert "Round 370 - Split Repo URL Placeholder Policy" in ledger
    assert "no fake github url" in lane.lower()
    assert "main repo linked as flagship placeholder" in lane

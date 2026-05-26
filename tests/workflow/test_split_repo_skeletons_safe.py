from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPLIT_ROOT = ROOT / "examples" / "split_repos"

SKELETONS = {
    "turingresearch-vggt-case": [
        "README.md",
        "CASE_STUDY.md",
        "PRIVACY.md",
        "manifest.yaml",
    ],
    "turingresearch-examples": [
        "README.md",
        "examples_manifest.yaml",
    ],
    "turingresearch-plugins": [
        "README.md",
        "PLUGIN_POLICY.md",
        "plugins_manifest.yaml",
    ],
}


def _text_files() -> list[Path]:
    return sorted(
        path
        for path in SPLIT_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}
    )


def _combined_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in _text_files())


def test_split_repo_skeletons_are_complete() -> None:
    for repo_id, filenames in SKELETONS.items():
        repo = SPLIT_ROOT / repo_id
        assert repo.exists(), repo_id
        for filename in filenames:
            assert (repo / filename).exists(), f"{repo_id}/{filename}"


def test_split_repo_readmes_keep_flagship_positioning() -> None:
    for repo_id in SKELETONS:
        readme = (SPLIT_ROOT / repo_id / "README.md").read_text(encoding="utf-8")
        lower = readme.lower()

        assert "flagship" in lower
        assert "star" in lower or "install" in lower
        assert "not a real repository" in lower
        assert "skeleton" in lower


def test_split_repo_skeletons_have_safety_boundaries() -> None:
    text = _combined_text().lower()

    assert "no raw data" in text
    assert "no smpl-x" in text or "no smplx" in text
    assert "no api keys" in text or "api keys" in text
    assert "unsupported experiment" in text
    assert "human review" in text
    assert "disabled by default" in text
    assert "execute_code" in text
    assert "secrets access" in text


def test_split_repo_skeletons_have_no_private_payload_patterns() -> None:
    text = _combined_text()
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "BEGIN " + "PRIVATE KEY",
        "local_project_links" + ".yaml",
        "SMPLX" + "_",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in text
    assert not token_like.search(text)


def test_split_repo_skeletons_do_not_claim_success() -> None:
    text = _combined_text().lower()
    blocked_claims = [
        "sparseconv3d succeeded",
        "vggt experiment succeeded",
        "we achieved final research success",
        "this proves final research success",
        "demo result is observed evidence",
        "demo result was observed evidence",
    ]

    for claim in blocked_claims:
        assert claim not in text
    assert "not proof of final research success" in text
    assert "no demo result promoted to observed evidence" in text


def test_split_repo_manifest_files_are_review_gated() -> None:
    manifests = [
        SPLIT_ROOT / "turingresearch-vggt-case" / "manifest.yaml",
        SPLIT_ROOT / "turingresearch-examples" / "examples_manifest.yaml",
        SPLIT_ROOT / "turingresearch-plugins" / "plugins_manifest.yaml",
    ]

    for manifest in manifests:
        text = manifest.read_text(encoding="utf-8")
        assert "status: split-repo-skeleton-only" in text
        assert "requires_human_review: true" in text
        assert "flagship_repo: turingresearch" in text

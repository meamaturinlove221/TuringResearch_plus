from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return " ".join(text.split())


def test_v1_1_main_repo_public_entry_is_clear() -> None:
    readme = _normalized(_read("README.md"))
    required = [
        "Local-first Research OS",
        "Start here:",
        "docs/v1.0.0-quickstart.md",
        "docs/v1.0.0-public-demo-walkthrough.md",
        "docs/README.md",
        "docs/v1.1.0-final-scope.md",
        "fake/demo-first by default",
        "Live adapters are optional and disabled by default",
        "not proof that any VGGT experiment succeeded",
    ]

    for item in required:
        assert item in readme


def test_v1_1_quickstart_and_public_demo_paths_exist() -> None:
    required = [
        ROOT / "docs" / "quickstart.md",
        ROOT / "docs" / "v1.0.0-quickstart.md",
        ROOT / "docs" / "v1.0.0-public-demo-walkthrough.md",
        ROOT / "examples" / "public_demo" / "QUICKSTART.md",
        ROOT / "examples" / "public_demo" / "WALKTHROUGH.md",
        ROOT / "examples" / "public_demo" / "EXPECTED_OUTPUTS.md",
        ROOT / "examples" / "public_demo" / "dashboard" / "index.html",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.exists()]

    assert missing == []


def test_v1_1_split_ready_is_not_described_as_published_repo() -> None:
    docs = _normalized(
        "\n".join(
            _read(path)
            for path in [
                "README.md",
                "docs/future-split-repos.md",
                "docs/split-ready-bundles.md",
                "docs/v1.1.0-final-scope.md",
            ]
        )
    )

    assert "not published GitHub repositories" in docs
    assert "local export bundles" in docs
    assert "not install targets" in docs
    assert not re.search(
        r"https://github\.com/[^)\s]+/turingresearch-(vggt-case|examples|plugins)",
        docs,
    )


def test_v1_1_public_entry_has_no_private_payload_or_old_name() -> None:
    combined = "\n".join(
        _read(path)
        for path in [
            "README.md",
            "docs/README.md",
            "docs/docs-index.md",
            "docs/quickstart.md",
            "docs/examples.md",
            "docs/v1.1.0-main-repo-stabilization-report.md",
            "docs/v1.1.0-public-entry-audit.md",
        ]
    )
    forbidden = [
        "Tuling" + "Research",
        "D:" + "/vggt",
        "D:\\vggt",
        "local_project_links" + ".yaml",
        "SMPLX" + "_",
        '"status": "observed"',
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in combined
    assert not token_like.search(combined)


def test_v1_1_public_entry_does_not_claim_fake_results() -> None:
    combined = "\n".join(
        _read(path)
        for path in [
            "README.md",
            "docs/quickstart.md",
            "docs/examples.md",
        ]
    ).lower()

    assert "does not turn fake/demo material into observed evidence" in combined
    assert "guarantee star growth" in combined
    assert "fake users" not in combined
    assert "fake benchmark" not in combined

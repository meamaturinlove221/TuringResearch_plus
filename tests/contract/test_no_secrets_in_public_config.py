from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".cff", ".json", ".md", ".toml", ".txt", ".yaml", ".yml"}
TEXT_FILENAMES = {".env.example"}
PUBLIC_CONFIG_FILES = [
    ROOT / ".mcp.example.json",
    ROOT / ".env.example",
    ROOT / "README.md",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CITATION.cff",
    ROOT / "docs" / "mcp-public-config-guide.md",
    ROOT / "docs" / "env-block-public-hygiene.md",
    ROOT / "docs" / "no-dotenv-public-policy.md",
    ROOT / "docs" / "optional-live-safety-policy.md",
]
ALLOWED_ENV_FIXTURES = {
    "examples/vggt-human-prior-survey/shared_store_fixture/.env",
}


def _public_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in PUBLIC_CONFIG_FILES
        if path.exists()
    )


def test_public_config_files_do_not_contain_token_like_values() -> None:
    text = _public_text()
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    assert token_like.search(text) is None


def test_public_config_files_do_not_contain_private_paths_or_payload_markers() -> None:
    text = _public_text()
    smpl_x = "SMPL" + "-X"
    smplx_prefix = "SMPLX" + "_"
    private_posix = "D:" + "/vggt"
    private_win = "D:" + "\\vggt"

    assert private_posix not in text
    assert private_win not in text
    assert smpl_x not in text
    assert smplx_prefix not in text


def test_no_dotenv_file_is_committed_outside_allowed_fixture() -> None:
    offenders = []
    for path in ROOT.rglob(".env"):
        relative = path.relative_to(ROOT).as_posix()
        if relative not in ALLOWED_ENV_FIXTURES:
            offenders.append(relative)

    assert offenders == []


def test_mcp_example_json_has_no_live_enabled_or_secret_values() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]

    for key, value in env.items():
        if key.startswith("TURINGRESEARCH_ENABLE_"):
            assert value == "0"
        elif key == "TURINGRESEARCH_MODE":
            assert value == "fake"
        else:
            assert value == ""


def test_public_config_scan_is_limited_to_text_surfaces() -> None:
    scanned = [path for path in PUBLIC_CONFIG_FILES if path.exists()]

    assert scanned
    assert all(
        path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_FILENAMES
        for path in scanned
    )

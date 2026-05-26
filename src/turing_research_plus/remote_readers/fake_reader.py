"""Fake/default SSH/SFTP reader for local tests."""

from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.remote_readers.models import (
    RemoteArtifactRecord,
    RemoteReaderSourceType,
)


class FakeRemoteArtifactReader:
    """Fake read-only remote reader.

    The fake reader never connects to a remote host. It can either load a local
    fixture index or provide a small VGGT-shaped artifact listing.
    """

    def __init__(self, fixture_index_path: Path | None = None) -> None:
        self.fixture_index_path = fixture_index_path

    def list_artifacts(self, root_path: str) -> list[RemoteArtifactRecord]:
        """Return fake or fixture artifact records."""

        if self.fixture_index_path is not None:
            return load_remote_fixture_index(self.fixture_index_path)
        return [
            RemoteArtifactRecord(
                path=f"{root_path.rstrip('/')}/review/final_status.json",
                size=512,
                sha256="a" * 64,
                source_type=RemoteReaderSourceType.FAKE_SFTP,
            ),
            RemoteArtifactRecord(
                path=f"{root_path.rstrip('/')}/review/failure_report.md",
                size=2048,
                sha256="b" * 64,
                source_type=RemoteReaderSourceType.FAKE_SFTP,
            ),
            RemoteArtifactRecord(
                path=f"{root_path.rstrip('/')}/review/board_inventory.md",
                size=1024,
                sha256="c" * 64,
                source_type=RemoteReaderSourceType.FAKE_SFTP,
            ),
            RemoteArtifactRecord(
                path=f"{root_path.rstrip('/')}/large/predictions.npz",
                size=250_000_000,
                sha256="d" * 64,
                source_type=RemoteReaderSourceType.FAKE_SFTP,
            ),
            RemoteArtifactRecord(
                path=f"{root_path.rstrip('/')}/private/SMPLX_model.pkl",
                size=100_000_000,
                sha256="e" * 64,
                source_type=RemoteReaderSourceType.FAKE_SFTP,
            ),
            RemoteArtifactRecord(
                path=f"{root_path.rstrip('/')}/current_failure_link.md",
                size=16,
                sha256="f" * 64,
                is_symlink=True,
                source_type=RemoteReaderSourceType.FAKE_SFTP,
            ),
        ]


def load_remote_fixture_index(path: Path) -> list[RemoteArtifactRecord]:
    """Load a local JSON fixture index."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    artifacts = payload.get("artifacts", payload)
    if not isinstance(artifacts, list):
        raise ValueError("remote artifact fixture must be a list or contain an artifacts list")
    return [
        RemoteArtifactRecord(
            **{
                **item,
                "source_type": item.get("source_type", RemoteReaderSourceType.LOCAL_FIXTURE),
            }
        )
        for item in artifacts
    ]

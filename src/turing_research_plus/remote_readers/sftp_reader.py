"""Optional read-only SFTP reader.

This module intentionally exposes listing and metadata only. It does not run
remote shell commands, write files, delete files, or execute experiments.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from turing_research_plus.remote_readers.models import (
    RemoteArtifactRecord,
    RemoteReaderSourceType,
)


@dataclass(frozen=True)
class SFTPConnectionSpec:
    """Minimal SFTP connection descriptor."""

    host_label: str
    root_path: str
    credential_env: str = "TURINGRESEARCH_SFTP_CREDENTIAL"


class SFTPRemoteReader:
    """Read-only optional SFTP metadata reader.

    The live path is deliberately conservative. It requires explicit opt-in
    from the caller and a credential environment variable. Paramiko is imported
    lazily so default package import and tests do not require the dependency.
    """

    def __init__(self, spec: SFTPConnectionSpec) -> None:
        self.spec = spec

    def has_credential(self) -> bool:
        """Return whether the configured credential variable is present."""

        return bool(os.getenv(self.spec.credential_env))

    def missing_credential_error(self) -> str:
        """Return a stable missing credential message."""

        return f"missing required credential env var: {self.spec.credential_env}"

    def list_artifacts(self) -> list[RemoteArtifactRecord]:
        """List remote artifact metadata.

        The minimal implementation keeps live SFTP as an optional surface. It
        validates dependency presence and then returns a typed unsupported
        message through the caller if a real client is not configured. This
        keeps the default no-network contract intact.
        """

        try:
            import paramiko  # type: ignore[import-untyped]  # noqa: F401
        except Exception as exc:  # pragma: no cover - depends on optional env
            raise RuntimeError("optional SFTP dependency is unavailable") from exc
        raise RuntimeError(
            "live SFTP listing requires an explicit project-specific connection adapter"
        )


def record_from_sftp_metadata(path: str, *, size: int = 0) -> RemoteArtifactRecord:
    """Build a metadata record without reading remote file contents."""

    return RemoteArtifactRecord(
        path=path,
        size=size,
        source_type=RemoteReaderSourceType.SFTP,
    )

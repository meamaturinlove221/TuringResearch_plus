"""Tiny NPZ metadata reader that does not load array payloads."""

from __future__ import annotations

import ast
import struct
import zipfile
from pathlib import Path

from tuling_research_plus.artifact_audit.models import NPZArraySummary


def summarize_npz(path: Path, max_arrays: int = 20) -> list[NPZArraySummary]:
    """Return array metadata for an NPZ file without loading full arrays."""

    if not path.exists():
        return [
            NPZArraySummary(
                key=path.name,
                file_size=0,
                summary_status="missing",
            )
        ]

    file_size = path.stat().st_size
    summaries: list[NPZArraySummary] = []
    try:
        with zipfile.ZipFile(path) as archive:
            npy_names = [name for name in archive.namelist() if name.endswith(".npy")]
            for name in npy_names[:max_arrays]:
                with archive.open(name) as member:
                    header = member.read(4096)
                shape, dtype = _parse_npy_header(header)
                summaries.append(
                    NPZArraySummary(
                        key=Path(name).stem,
                        shape=list(shape),
                        dtype=dtype,
                        file_size=file_size,
                        summary_status="ok",
                    )
                )
            if len(npy_names) > max_arrays:
                summaries.append(
                    NPZArraySummary(
                        key="__truncated__",
                        file_size=file_size,
                        summary_status="truncated",
                    )
                )
    except (OSError, zipfile.BadZipFile, ValueError, SyntaxError) as exc:
        return [
            NPZArraySummary(
                key=path.name,
                file_size=file_size,
                summary_status=f"error:{type(exc).__name__}",
            )
        ]
    return summaries or [
        NPZArraySummary(
            key=path.name,
            file_size=file_size,
            summary_status="empty",
        )
    ]


def _parse_npy_header(data: bytes) -> tuple[tuple[int, ...], str]:
    if not data.startswith(b"\x93NUMPY"):
        raise ValueError("not an npy member")
    major = data[6]
    if major == 1:
        header_len = struct.unpack("<H", data[8:10])[0]
        header_start = 10
    elif major in {2, 3}:
        header_len = struct.unpack("<I", data[8:12])[0]
        header_start = 12
    else:
        raise ValueError("unsupported npy version")
    header_text = data[header_start : header_start + header_len].decode("latin1").strip()
    header = ast.literal_eval(header_text)
    shape = tuple(int(item) for item in header.get("shape", ()))
    dtype = str(header.get("descr", ""))
    return shape, dtype


import struct
import zipfile
from pathlib import Path

from tuling_research_plus.artifact_audit.npz_summary import summarize_npz


def write_npy_member(path: Path, name: str = "arr.npy") -> None:
    header_dict = {"descr": "<f4", "fortran_order": False, "shape": (2, 3)}
    header = repr(header_dict).encode("latin1")
    padding = b" " * ((16 - ((10 + len(header) + 1) % 16)) % 16)
    header_block = header + padding + b"\n"
    payload = b"\x93NUMPY" + bytes([1, 0]) + struct.pack("<H", len(header_block)) + header_block
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(name, payload)


def test_summarize_npz_reads_header_without_array_load(tmp_path: Path) -> None:
    path = tmp_path / "fixture.npz"
    write_npy_member(path)

    summary = summarize_npz(path)

    assert summary[0].key == "arr"
    assert summary[0].shape == [2, 3]
    assert summary[0].dtype == "<f4"
    assert summary[0].summary_status == "ok"


def test_summarize_missing_npz_returns_missing_status(tmp_path: Path) -> None:
    summary = summarize_npz(tmp_path / "missing.npz")

    assert summary[0].summary_status == "missing"


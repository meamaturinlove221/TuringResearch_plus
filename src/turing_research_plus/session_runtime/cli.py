"""Command line entrypoint for local Session runtime parity tools."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from turing_research_plus.session_runtime.cli_report import SessionCLICommandReport
from turing_research_plus.session_runtime.commands import (
    render_cli_report,
    run_pack_command,
    run_preflight_command,
    run_replay_command,
    run_report_command,
    run_transfer_command,
    run_verify_return_command,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the Session CLI parser."""

    parser = argparse.ArgumentParser(
        prog="turingresearch-session",
        description="Local fake/default Session runtime tools.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    preflight = subcommands.add_parser("preflight", help="run local session preflight")
    preflight.add_argument("--project-root", type=Path, required=True)
    preflight.add_argument("--context-source", type=Path, required=True)
    preflight.add_argument("--output-dir", type=Path, required=True)
    preflight.add_argument("--session-id", default="session-cli-preflight")
    preflight.add_argument("--package-id", default="ctx-cli-preflight")
    preflight.add_argument("--route-id", default="route-cli-preflight")
    preflight.add_argument("--output", type=Path)

    pack = subcommands.add_parser("pack", help="build a safe local context pack")
    pack.add_argument("--source-dir", type=Path, required=True)
    pack.add_argument("--output-dir", type=Path, required=True)
    pack.add_argument("--package-id", default="ctx-cli-pack")
    pack.add_argument("--route-id", default="route-cli-pack")
    pack.add_argument("--project-name", default="TuringResearch Plus")
    pack.add_argument("--output", type=Path)

    transfer = subcommands.add_parser("transfer", help="run fake local context transfer")
    transfer.add_argument("--fake", action="store_true", default=True)
    transfer.add_argument("--source-dir", type=Path, required=True)
    transfer.add_argument("--target-dir", type=Path, required=True)
    transfer.add_argument("--transfer-id", default="transfer-cli-fake")
    transfer.add_argument("--package-id", default="ctx-cli-transfer")
    transfer.add_argument("--output", type=Path)

    verify_return = subcommands.add_parser(
        "verify-return",
        help="verify a structured return package",
    )
    verify_return.add_argument("--return-dir", type=Path, required=True)
    verify_return.add_argument("--return-id", default="return-cli-verify")
    verify_return.add_argument("--output", type=Path)

    replay = subcommands.add_parser("replay", help="run full fake pod workflow replay")
    replay.add_argument("--project-root", type=Path, required=True)
    replay.add_argument("--preflight-context-source", type=Path, required=True)
    replay.add_argument("--preflight-output-dir", type=Path, required=True)
    replay.add_argument("--context-pack-source-dir", type=Path, required=True)
    replay.add_argument("--replay-workspace", type=Path, required=True)
    replay.add_argument("--fake-return-fixture-dir", type=Path, required=True)
    replay.add_argument("--replay-id", default="session-cli-replay")
    replay.add_argument("--session-id", default="session-cli-replay")
    replay.add_argument("--package-id", default="ctx-cli-replay")
    replay.add_argument("--route-id", default="route-cli-replay")
    replay.add_argument("--output", type=Path)

    report = subcommands.add_parser("report", help="show Session CLI surface report")
    report.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the Session CLI."""

    args = _normalize_argv(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    namespace = parser.parse_args(args)
    try:
        report = _dispatch(namespace)
    except Exception as exc:  # noqa: BLE001 - CLI should return a stable error code.
        print(f"Session CLI blocked: {exc}", file=sys.stderr)
        return 2
    print(render_cli_report(report), end="")
    return 1 if report.release_blocker else 0


def _normalize_argv(argv: list[str]) -> list[str]:
    if argv and argv[0] == "session":
        return argv[1:]
    return argv


def _dispatch(namespace: argparse.Namespace) -> SessionCLICommandReport:
    command = namespace.command
    if command == "preflight":
        return run_preflight_command(
            project_root=namespace.project_root,
            context_source=namespace.context_source,
            output_dir=namespace.output_dir,
            session_id=namespace.session_id,
            package_id=namespace.package_id,
            route_id=namespace.route_id,
            output=namespace.output,
        )
    if command == "pack":
        return run_pack_command(
            source_dir=namespace.source_dir,
            output_dir=namespace.output_dir,
            package_id=namespace.package_id,
            route_id=namespace.route_id,
            project_name=namespace.project_name,
            output=namespace.output,
        )
    if command == "transfer":
        return run_transfer_command(
            source_dir=namespace.source_dir,
            target_dir=namespace.target_dir,
            transfer_id=namespace.transfer_id,
            package_id=namespace.package_id,
            fake=namespace.fake,
            output=namespace.output,
        )
    if command == "verify-return":
        return run_verify_return_command(
            return_dir=namespace.return_dir,
            return_id=namespace.return_id,
            output=namespace.output,
        )
    if command == "replay":
        return run_replay_command(
            project_root=namespace.project_root,
            preflight_context_source=namespace.preflight_context_source,
            preflight_output_dir=namespace.preflight_output_dir,
            context_pack_source_dir=namespace.context_pack_source_dir,
            replay_workspace=namespace.replay_workspace,
            fake_return_fixture_dir=namespace.fake_return_fixture_dir,
            replay_id=namespace.replay_id,
            session_id=namespace.session_id,
            package_id=namespace.package_id,
            route_id=namespace.route_id,
            output=namespace.output,
        )
    if command == "report":
        return run_report_command(output=namespace.output)
    raise ValueError(f"unknown Session CLI command: {command}")


if __name__ == "__main__":
    raise SystemExit(main())

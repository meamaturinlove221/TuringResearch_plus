"""Local-first session runtime preflight surfaces."""

from turing_research_plus.session_runtime.archive_platform import (
    ArchivePlatformNotes,
    build_archive_platform_notes,
    normalize_platform_archive_path,
    render_archive_platform_notes,
)
from turing_research_plus.session_runtime.archive_safety import (
    ArchiveCandidateCheck,
    ArchiveSafetyRuntimeReport,
    audit_context_pack_candidates,
    is_safe_pack_entry,
)
from turing_research_plus.session_runtime.archive_writer import (
    ArchiveWriteReport,
    WrittenArchiveFile,
    sha256_file,
    write_context_pack_files,
)
from turing_research_plus.session_runtime.cli_report import (
    SessionCLICommandReport,
    SessionCLIStatus,
    build_session_cli_surface_report,
    render_session_cli_command_report,
    write_cli_report_if_requested,
)
from turing_research_plus.session_runtime.commands import (
    render_cli_report,
    run_pack_command,
    run_preflight_command,
    run_replay_command,
    run_report_command,
    run_transfer_command,
    run_verify_return_command,
)
from turing_research_plus.session_runtime.context_manifest import (
    ContextPackBuildStatus,
    ContextPackManifest,
    ContextPackManifestFile,
    ContextPackOmittedFile,
    render_context_pack_manifest_markdown,
    render_handoff_manifest,
)
from turing_research_plus.session_runtime.context_pack_builder import (
    ContextPackBuildRequest,
    build_context_pack,
)
from turing_research_plus.session_runtime.dotfile_policy import (
    DotfilePolicyDecision,
    evaluate_dotfile_policy,
)
from turing_research_plus.session_runtime.environment_check import (
    run_session_environment_checks,
)
from turing_research_plus.session_runtime.human_confirmation import (
    HumanConfirmationChecklist as ReturnHumanConfirmationChecklist,
)
from turing_research_plus.session_runtime.human_confirmation import (
    HumanConfirmationPacket,
    build_human_confirmation_packet,
    render_human_confirmation_packet,
    write_human_confirmation_packet,
)
from turing_research_plus.session_runtime.import_decision import (
    ImportDecision,
    ImportDecisionStatus,
    default_import_decision_from_verifier,
    render_import_decision,
)
from turing_research_plus.session_runtime.ledger_proposal import (
    LedgerProposalEntry,
    LedgerProposalPacket,
    build_ledger_proposal_packet,
    render_ledger_proposal_packet,
)
from turing_research_plus.session_runtime.manual_execution_plan import (
    HumanConfirmationChecklist,
    ManualCommandStep,
    ManualStepStatus,
    RollbackPlanStep,
    build_default_confirmation_checklist,
    build_default_manual_commands,
    build_default_rollback_plan,
    render_manual_execution_plan,
)
from turing_research_plus.session_runtime.models import (
    SessionEnvironmentCheck,
    SessionLookupRecord,
    SessionPreflightFinding,
    SessionPreflightFindingSeverity,
    SessionPreflightReport,
    SessionPreflightRequest,
    SessionPreflightStatus,
)
from turing_research_plus.session_runtime.path_normalization import (
    NormalizedArchivePath,
    normalize_archive_member_path,
    require_safe_archive_member_path,
    windows_path_to_posix,
)
from turing_research_plus.session_runtime.preflight_runner import run_session_preflight
from turing_research_plus.session_runtime.proposed_updates import (
    ProposedEvidenceUpdate,
    ProposedUpdateLoadReport,
    load_proposed_updates,
)
from turing_research_plus.session_runtime.remote_dry_run_plan import (
    RemoteDryRunFileRecord,
    RemoteDryRunPlan,
    RemoteDryRunPlanRequest,
    RemoteDryRunStatus,
    build_remote_dry_run_plan,
    render_remote_dry_run_plan,
    write_remote_dry_run_plan,
)
from turing_research_plus.session_runtime.report import render_session_preflight_report
from turing_research_plus.session_runtime.return_manifest import (
    REQUIRED_RETURN_FILES,
    ReturnFileRecord,
    ReturnManifestRuntime,
    load_return_manifest,
    load_sha256sums,
)
from turing_research_plus.session_runtime.return_safety import (
    ReturnSafetyFinding,
    ReturnSafetyReport,
    run_return_safety_checks,
)
from turing_research_plus.session_runtime.return_verifier import (
    ReturnVerifierReport,
    ReturnVerifierStatus,
    render_return_verifier_report,
    verify_return_package,
)
from turing_research_plus.session_runtime.script_exporter import (
    SCRIPT_ORDER,
    SessionScriptExportReport,
    SessionScriptExportRequest,
    SessionScriptExportStatus,
    SessionScriptSpec,
    build_session_script_specs,
    export_session_scripts,
    render_session_script_export_report,
)
from turing_research_plus.session_runtime.script_safety import (
    ScriptSafetyFinding,
    ScriptSafetyReport,
    ScriptSafetyStatus,
    audit_shell_script,
    render_script_safety_report,
)
from turing_research_plus.session_runtime.session_lookup import (
    build_session_lookup_record,
    discover_context_files,
)
from turing_research_plus.session_runtime.sftp_transfer_optional import (
    OptionalSFTPTransferRequest,
    live_sftp_is_enabled,
    run_optional_sftp_transfer,
    validate_remote_transfer_target,
)
from turing_research_plus.session_runtime.sop_export import render_session_script_sop
from turing_research_plus.session_runtime.transfer_report import (
    TransferFileRecord,
    TransferMode,
    TransferOmittedFile,
    TransferReport,
    TransferStatus,
    render_transfer_report,
)
from turing_research_plus.session_runtime.transfer_runner import (
    TransferRunnerRequest,
    run_transfer,
)
from turing_research_plus.session_runtime.unpack_safety import (
    ArchiveMember,
    UnpackSafetyFinding,
    UnpackSafetyReport,
    archive_members_from_directory,
    validate_archive_members,
    validate_return_archive_directory,
)
from turing_research_plus.session_runtime.workflow_replay import (
    FakePodReturnFixtureReport,
    PodWorkflowReplayReport,
    PodWorkflowReplayRequest,
    PodWorkflowReplayStatus,
    copy_fake_pod_return_fixture,
    render_pod_workflow_replay_report,
    run_pod_workflow_replay,
)

__all__ = [
    "ArchiveCandidateCheck",
    "ArchiveMember",
    "ArchivePlatformNotes",
    "ArchiveSafetyRuntimeReport",
    "ArchiveWriteReport",
    "ContextPackBuildRequest",
    "ContextPackBuildStatus",
    "ContextPackManifest",
    "ContextPackManifestFile",
    "ContextPackOmittedFile",
    "DotfilePolicyDecision",
    "FakePodReturnFixtureReport",
    "HumanConfirmationChecklist",
    "HumanConfirmationPacket",
    "ImportDecision",
    "ImportDecisionStatus",
    "LedgerProposalEntry",
    "LedgerProposalPacket",
    "ManualCommandStep",
    "ManualStepStatus",
    "NormalizedArchivePath",
    "OptionalSFTPTransferRequest",
    "PodWorkflowReplayReport",
    "PodWorkflowReplayRequest",
    "PodWorkflowReplayStatus",
    "ProposedEvidenceUpdate",
    "ProposedUpdateLoadReport",
    "REQUIRED_RETURN_FILES",
    "RemoteDryRunFileRecord",
    "RemoteDryRunPlan",
    "RemoteDryRunPlanRequest",
    "RemoteDryRunStatus",
    "ReturnHumanConfirmationChecklist",
    "ReturnFileRecord",
    "ReturnManifestRuntime",
    "ReturnSafetyFinding",
    "ReturnSafetyReport",
    "ReturnVerifierReport",
    "ReturnVerifierStatus",
    "RollbackPlanStep",
    "SessionCLICommandReport",
    "SessionCLIStatus",
    "SessionEnvironmentCheck",
    "SessionLookupRecord",
    "SessionPreflightFinding",
    "SessionPreflightFindingSeverity",
    "SessionPreflightReport",
    "SessionPreflightRequest",
    "SessionPreflightStatus",
    "SessionScriptExportReport",
    "SessionScriptExportRequest",
    "SessionScriptExportStatus",
    "SessionScriptSpec",
    "ScriptSafetyFinding",
    "ScriptSafetyReport",
    "ScriptSafetyStatus",
    "SCRIPT_ORDER",
    "TransferFileRecord",
    "TransferMode",
    "TransferOmittedFile",
    "TransferReport",
    "TransferRunnerRequest",
    "TransferStatus",
    "UnpackSafetyFinding",
    "UnpackSafetyReport",
    "WrittenArchiveFile",
    "archive_members_from_directory",
    "audit_context_pack_candidates",
    "audit_shell_script",
    "build_archive_platform_notes",
    "build_context_pack",
    "build_default_confirmation_checklist",
    "build_default_manual_commands",
    "build_default_rollback_plan",
    "build_human_confirmation_packet",
    "build_ledger_proposal_packet",
    "build_remote_dry_run_plan",
    "build_session_cli_surface_report",
    "build_session_lookup_record",
    "build_session_script_specs",
    "copy_fake_pod_return_fixture",
    "default_import_decision_from_verifier",
    "discover_context_files",
    "evaluate_dotfile_policy",
    "export_session_scripts",
    "is_safe_pack_entry",
    "live_sftp_is_enabled",
    "load_proposed_updates",
    "load_return_manifest",
    "load_sha256sums",
    "normalize_archive_member_path",
    "normalize_platform_archive_path",
    "render_context_pack_manifest_markdown",
    "render_archive_platform_notes",
    "render_cli_report",
    "render_handoff_manifest",
    "render_human_confirmation_packet",
    "render_import_decision",
    "render_ledger_proposal_packet",
    "render_manual_execution_plan",
    "render_pod_workflow_replay_report",
    "render_remote_dry_run_plan",
    "render_return_verifier_report",
    "render_script_safety_report",
    "render_session_cli_command_report",
    "render_session_preflight_report",
    "render_session_script_export_report",
    "render_session_script_sop",
    "render_transfer_report",
    "run_pack_command",
    "run_preflight_command",
    "run_return_safety_checks",
    "run_replay_command",
    "run_report_command",
    "run_session_environment_checks",
    "run_session_preflight",
    "run_optional_sftp_transfer",
    "run_transfer",
    "run_transfer_command",
    "run_pod_workflow_replay",
    "run_verify_return_command",
    "sha256_file",
    "require_safe_archive_member_path",
    "validate_remote_transfer_target",
    "validate_archive_members",
    "validate_return_archive_directory",
    "verify_return_package",
    "windows_path_to_posix",
    "write_cli_report_if_requested",
    "write_context_pack_files",
    "write_human_confirmation_packet",
    "write_remote_dry_run_plan",
]

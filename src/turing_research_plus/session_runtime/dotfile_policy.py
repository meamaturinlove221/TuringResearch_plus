"""Dotfile allowlist and denylist policy for session runtime archives."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.session_runtime.path_normalization import (
    normalize_archive_member_path,
)

DEFAULT_DOTFILE_DENYLIST = {
    ".aws",
    ".azure",
    ".codex",
    ".config",
    ".docker",
    ".env",
    ".git",
    ".kube",
    ".netrc",
    ".npmrc",
    ".pypirc",
    ".ssh",
}
DEFAULT_DOTFILE_ALLOWLIST = {".gitkeep", ".keep"}


class DotfilePolicyDecision(BaseModel):
    """Decision for dotfile handling in an archive path."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    normalized_path: str = Field(min_length=1)
    dotfile_parts: list[str] = Field(default_factory=list)
    allowed: bool = True
    reasons: list[str] = Field(default_factory=list)
    policy: str = "dotfiles denied unless explicitly allowlisted; sensitive dotfiles always denied"

    @property
    def release_blocker(self) -> bool:
        """Return whether the dotfile policy blocks this path."""

        return not self.allowed


def evaluate_dotfile_policy(
    path: str,
    *,
    allowlist: set[str] | None = None,
    denylist: set[str] | None = None,
) -> DotfilePolicyDecision:
    """Evaluate the dotfile allowlist policy for one archive member path."""

    normalized = normalize_archive_member_path(path)
    allowed_names = allowlist or DEFAULT_DOTFILE_ALLOWLIST
    denied_names = denylist or DEFAULT_DOTFILE_DENYLIST
    parts = normalized.normalized_path.split("/")
    dot_parts = [part for part in parts if part.startswith(".")]
    reasons: list[str] = []

    for part in dot_parts:
        lower = part.lower()
        if lower in denied_names:
            reasons.append("dotfile-denylist")
        elif lower not in allowed_names:
            reasons.append("dotfile-not-allowlisted")

    reasons.extend(normalized.blocked_reasons)

    return DotfilePolicyDecision(
        path=path,
        normalized_path=normalized.normalized_path,
        dotfile_parts=dot_parts,
        allowed=not reasons,
        reasons=list(dict.fromkeys(reasons)),
    )

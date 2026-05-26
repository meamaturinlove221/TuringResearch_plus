"""Redaction helpers for optional live provider output."""

from __future__ import annotations

import re
from enum import StrEnum
from typing import NamedTuple

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LiveRedactionKind(StrEnum):
    """Kinds of sensitive live output that must not enter reports raw."""

    API_KEY = "api_key"
    TOKEN = "token"
    PASSWORD = "password"
    PRIVATE_PATH = "private_path"
    SSH_HOST_ALIAS = "ssh_host_alias"
    LOCAL_USERNAME = "local_username"
    COOKIE = "cookie"
    RAW_PRIVATE_CONTENT = "raw_private_content"


class LiveRedactionFinding(BaseModel):
    """One redaction applied to live output."""

    model_config = ConfigDict(extra="forbid")

    kind: LiveRedactionKind
    replacement: str = Field(min_length=1)
    count: int = Field(ge=1)


class LiveRedactionResult(BaseModel):
    """Result of redacting optional live output."""

    model_config = ConfigDict(extra="forbid")

    sanitized_text: str
    findings: list[LiveRedactionFinding] = Field(default_factory=list)
    raw_output_retained: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_no_raw_retention(self) -> LiveRedactionResult:
        if self.raw_output_retained:
            raise ValueError("live redaction results must not retain raw output")
        if not self.requires_human_review:
            raise ValueError("live redaction results require human review")
        return self

    @property
    def redacted(self) -> bool:
        """Return whether any sensitive content was redacted."""

        return bool(self.findings)


class _RedactionRule(NamedTuple):
    kind: LiveRedactionKind
    pattern: re.Pattern[str]
    replacement: str


_RULES: tuple[_RedactionRule, ...] = (
    _RedactionRule(
        LiveRedactionKind.API_KEY,
        re.compile(
            r"(?i)\b(api[_-]?key|x-api-key|openai_api_key)\s*[:=]\s*"
            r"['\"]?[A-Za-z0-9][A-Za-z0-9._-]{10,}['\"]?"
        ),
        "[REDACTED_API_KEY]",
    ),
    _RedactionRule(
        LiveRedactionKind.TOKEN,
        re.compile(
            r"(?i)\b(access[_-]?token|auth[_-]?token|bearer|token)\s*[:= ]\s*"
            r"['\"]?[A-Za-z0-9][A-Za-z0-9._-]{10,}['\"]?"
            r"|(?:sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,})"
        ),
        "[REDACTED_TOKEN]",
    ),
    _RedactionRule(
        LiveRedactionKind.PASSWORD,
        re.compile(r"(?i)\b(pass(word)?|pwd)\s*[:=]\s*['\"]?[^'\"\s;]{4,}['\"]?"),
        "[REDACTED_PASSWORD]",
    ),
    _RedactionRule(
        LiveRedactionKind.COOKIE,
        re.compile(r"(?i)\b(cookie|set-cookie)\s*[:=]\s*[^;\n]+(?:;[^\n]*)?"),
        "[REDACTED_COOKIE]",
    ),
    _RedactionRule(
        LiveRedactionKind.PRIVATE_PATH,
        re.compile(
            r"(?:[A-Za-z]:[\\/](?:Users|private|vggt|data|workspace)[^\s'\"<>]*)"
            r"|(?:/(?:home|Users|private|mnt|Volumes)/[^\s'\"<>]+)"
        ),
        "[REDACTED_PRIVATE_PATH]",
    ),
    _RedactionRule(
        LiveRedactionKind.SSH_HOST_ALIAS,
        re.compile(
            r"(?i)\b(?:ssh|sftp)://[A-Za-z0-9_.-]+"
            r"|\b(?:ssh_host|host_alias|hostname)\s*[:=]\s*[A-Za-z0-9_.-]+"
        ),
        "[REDACTED_SSH_HOST]",
    ),
    _RedactionRule(
        LiveRedactionKind.LOCAL_USERNAME,
        re.compile(r"(?i)\b(user(name)?|local_user)\s*[:=]\s*[A-Za-z][A-Za-z0-9_.-]{2,}"),
        "[REDACTED_LOCAL_USER]",
    ),
    _RedactionRule(
        LiveRedactionKind.RAW_PRIVATE_CONTENT,
        re.compile(
            r"<raw_private_content>.*?</raw_private_content>"
            r"|\braw_private_content\s*[:=]\s*[^;\n]+"
            r"|\bprivate_content\s*[:=]\s*[^;\n]+",
            flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
        ),
        "[REDACTED_RAW_PRIVATE_CONTENT]",
    ),
)


def redact_live_output(text: str) -> LiveRedactionResult:
    """Redact sensitive values from optional live output."""

    sanitized = text
    findings: list[LiveRedactionFinding] = []

    for rule in _RULES:
        sanitized, count = rule.pattern.subn(rule.replacement, sanitized)
        if count:
            findings.append(
                LiveRedactionFinding(
                    kind=rule.kind,
                    replacement=rule.replacement,
                    count=count,
                )
            )

    return LiveRedactionResult(
        sanitized_text=sanitized,
        findings=findings,
        raw_output_retained=False,
        requires_human_review=True,
    )

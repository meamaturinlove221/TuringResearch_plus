from __future__ import annotations

from turing_research_plus.live_safety import LiveRedactionKind, redact_live_output


def test_live_output_redacts_secret_like_values_and_private_paths() -> None:
    raw = "\n".join(
        [
            "api_key" + "=abc123456789SECRET",
            "access_token" + "=tok_abcdefghijklmnopqrstuvwxyz",
            "password" + "=not-for-report",
            "cookie=sessionid=abc123; path=/",
            "path C:/Users/researcher/private/output.json",
            "hostname=gpu-pod-alpha",
            "username=alice",
            "<raw_private_content>private page body</raw_private_content>",
        ]
    )

    result = redact_live_output(raw)
    kinds = {finding.kind for finding in result.findings}

    assert result.redacted is True
    assert result.raw_output_retained is False
    assert result.requires_human_review is True
    assert LiveRedactionKind.API_KEY in kinds
    assert LiveRedactionKind.TOKEN in kinds
    assert LiveRedactionKind.PASSWORD in kinds
    assert LiveRedactionKind.COOKIE in kinds
    assert LiveRedactionKind.PRIVATE_PATH in kinds
    assert LiveRedactionKind.SSH_HOST_ALIAS in kinds
    assert LiveRedactionKind.LOCAL_USERNAME in kinds
    assert LiveRedactionKind.RAW_PRIVATE_CONTENT in kinds
    assert "abc123456789SECRET" not in result.sanitized_text
    assert "tok_abcdefghijklmnopqrstuvwxyz" not in result.sanitized_text
    assert "not-for-report" not in result.sanitized_text
    assert "sessionid=abc123" not in result.sanitized_text
    assert "C:/Users/researcher" not in result.sanitized_text
    assert "gpu-pod-alpha" not in result.sanitized_text
    assert "username=alice" not in result.sanitized_text
    assert "private page body" not in result.sanitized_text


def test_live_output_without_sensitive_values_still_requires_review() -> None:
    result = redact_live_output("fake live smoke summary: no provider request was made")

    assert result.redacted is False
    assert result.findings == []
    assert result.sanitized_text == "fake live smoke summary: no provider request was made"
    assert result.raw_output_retained is False
    assert result.requires_human_review is True

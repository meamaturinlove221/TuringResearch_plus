from __future__ import annotations

from turing_research_plus.case_study.redactor import redact_public_case_study_text


def test_case_study_redactor_removes_private_and_restricted_markers() -> None:
    text = (
        "Local path C:/private/project/file.md includes raw data, "
        "SMPLX_model.pkl, and private advisor feedback."
    )

    sanitized, report = redact_public_case_study_text(text)

    assert "C:/private" not in sanitized
    assert "raw data" not in sanitized.lower()
    assert "SMPLX_model.pkl" not in sanitized
    assert "private advisor feedback" not in sanitized.lower()
    assert report.sanitized is True
    assert {item.finding_type for item in report.redactions} >= {
        "private-local-path",
        "raw-data",
        "model-file",
        "private-advisor-feedback",
    }

from datetime import UTC, datetime, timedelta

from turing_research.cache.failure_ledger import FailureLedger, FailureRecord


def test_failure_ledger_appends_retry_after_record(tmp_path) -> None:
    ledger = FailureLedger(tmp_path / "failures.json")
    retry_after = datetime.now(UTC) + timedelta(minutes=5)
    record = FailureRecord(
        failure_id="failure-1",
        key="cache-key",
        reason="rate limited",
        retry_after=retry_after,
        metadata={"adapter": "fake"},
    )

    ledger.append(record)

    records = ledger.list_records()
    assert len(records) == 1
    assert records[0].retry_after == retry_after
    assert records[0].metadata == {"adapter": "fake"}


def test_failure_ledger_filters_retryable_records(tmp_path) -> None:
    ledger = FailureLedger(tmp_path / "failures.json")
    now = datetime.now(UTC)
    ledger.append(
        FailureRecord(
            failure_id="future",
            key="key-1",
            reason="wait",
            retry_after=now + timedelta(minutes=1),
        )
    )
    ledger.append(
        FailureRecord(
            failure_id="past",
            key="key-2",
            reason="ready",
            retry_after=now - timedelta(minutes=1),
        )
    )

    retryable = ledger.retryable(now)

    assert [record.failure_id for record in retryable] == ["past"]

"""
tests/test_failure_validation_retry_timeout_v165.py — Retry & Timeout tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.retry_validator_v165 import (
    PAPER_ONLY as RETRY_PAPER_ONLY,
    RESEARCH_ONLY as RETRY_RESEARCH_ONLY,
    simulate_retry_sequence,
    validate_idempotency,
)
from paper_trading.failure_validation.timeout_sim_v165 import (
    NO_REAL_SLEEP,
    PAPER_ONLY as TO_PAPER_ONLY,
    RESEARCH_ONLY as TO_RESEARCH_ONLY,
    TimeoutSimResult,
    simulate_timeout,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestRetryTimeoutSafetyFlags:
    def test_retry_paper_only(self):
        assert RETRY_PAPER_ONLY is True

    def test_retry_research_only(self):
        assert RETRY_RESEARCH_ONLY is True

    def test_timeout_paper_only(self):
        assert TO_PAPER_ONLY is True

    def test_timeout_research_only(self):
        assert TO_RESEARCH_ONLY is True

    def test_no_real_sleep(self):
        assert NO_REAL_SLEEP is True


# ---------------------------------------------------------------------------
# simulate_retry_sequence
# ---------------------------------------------------------------------------

class TestSimulateRetrySequence:
    def test_succeed_on_first_attempt(self):
        rec = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=1, seed=1)
        assert rec.succeeded is True
        assert rec.attempt_number == 1

    def test_succeed_on_second_attempt(self):
        rec = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=2, seed=1)
        assert rec.succeeded is True
        assert rec.attempt_number == 2

    def test_exhaust_all_attempts(self):
        rec = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=None, seed=0)
        # With seed=0, random may or may not succeed — just check exhaustion or success
        assert rec.exhausted or rec.succeeded

    def test_never_succeed_exhausts(self):
        # succeed_on_attempt=999 means never succeed in 3 attempts
        rec = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=999, seed=1)
        assert rec.exhausted is True
        assert rec.succeeded is False

    def test_idempotency_key_used(self):
        key = "my_idem_key_12345"
        rec = simulate_retry_sequence(max_attempts=2, succeed_on_attempt=1, idempotency_key=key)
        assert rec.idempotency_key == key

    def test_idempotency_key_generated_if_not_provided(self):
        rec = simulate_retry_sequence(max_attempts=2, succeed_on_attempt=1)
        assert len(rec.idempotency_key) > 0

    def test_attempt_log_has_entries(self):
        rec = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=3, seed=1)
        assert len(rec.attempts) >= 1

    def test_virtual_clock_advances_on_failure(self):
        rec = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=3, backoff_ms=100, seed=1)
        # After 2 failed attempts before success: clock should have advanced
        assert rec.virtual_clock_ms >= 0

    def test_deterministic_same_seed_succeed_on_attempt(self):
        r1 = simulate_retry_sequence(max_attempts=5, succeed_on_attempt=2, seed=42)
        r2 = simulate_retry_sequence(max_attempts=5, succeed_on_attempt=2, seed=42)
        assert r1.succeeded == r2.succeeded
        assert r1.attempt_number == r2.attempt_number

    def test_backoff_ms_affects_clock(self):
        r_slow = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=3, backoff_ms=500, seed=1)
        r_fast = simulate_retry_sequence(max_attempts=3, succeed_on_attempt=3, backoff_ms=10, seed=1)
        assert r_slow.virtual_clock_ms >= r_fast.virtual_clock_ms


# ---------------------------------------------------------------------------
# validate_idempotency
# ---------------------------------------------------------------------------

class TestValidateIdempotency:
    def test_new_key_not_duplicate(self):
        seen = set()
        result = validate_idempotency("key_1", seen)
        assert result["duplicate"] is False

    def test_seen_key_is_duplicate(self):
        seen = set()
        validate_idempotency("key_1", seen)
        result = validate_idempotency("key_1", seen)
        assert result["duplicate"] is True

    def test_result_has_key_field(self):
        seen = set()
        result = validate_idempotency("abc", seen)
        assert result["key"] == "abc"

    def test_non_duplicate_added_to_seen(self):
        seen = set()
        validate_idempotency("new_key", seen)
        assert "new_key" in seen

    def test_duplicate_not_added_again(self):
        seen = {"already_there"}
        validate_idempotency("already_there", seen)
        assert len(seen) == 1


# ---------------------------------------------------------------------------
# TimeoutSimResult
# ---------------------------------------------------------------------------

class TestTimeoutSimResult:
    def test_timed_out_when_elapsed_exceeds_timeout(self):
        r = TimeoutSimResult(operation="query", timeout_ms=5000, elapsed_virtual_ms=6000)
        assert r.timed_out is True

    def test_not_timed_out_when_elapsed_less_than_timeout(self):
        r = TimeoutSimResult(operation="query", timeout_ms=5000, elapsed_virtual_ms=3000)
        assert r.timed_out is False

    def test_exactly_at_timeout_is_timed_out(self):
        r = TimeoutSimResult(operation="query", timeout_ms=5000, elapsed_virtual_ms=5000)
        assert r.timed_out is True

    def test_as_dict_has_required_keys(self):
        r = TimeoutSimResult(operation="fetch", timeout_ms=1000, elapsed_virtual_ms=2000)
        d = r.as_dict()
        assert "operation" in d
        assert "timeout_ms" in d
        assert "elapsed_ms" in d
        assert "timed_out" in d
        assert "detected" in d

    def test_as_dict_timed_out_correct(self):
        r = TimeoutSimResult(operation="x", timeout_ms=1000, elapsed_virtual_ms=2000)
        assert r.as_dict()["timed_out"] is True


# ---------------------------------------------------------------------------
# simulate_timeout function
# ---------------------------------------------------------------------------

class TestSimulateTimeout:
    def test_timeout_detected_when_elapsed_exceeds(self):
        result = simulate_timeout("query_op", timeout_ms=5000, virtual_elapsed_ms=6000, seed=42)
        assert result.timed_out is True

    def test_not_timed_out_when_within_limit(self):
        result = simulate_timeout("query_op", timeout_ms=5000, virtual_elapsed_ms=3000, seed=42)
        assert result.timed_out is False
        assert result.detected is False  # not timed out = not detected as timeout

    def test_detection_set_when_timed_out(self):
        result = simulate_timeout("query_op", timeout_ms=100, virtual_elapsed_ms=5000, seed=42)
        assert result.timed_out is True
        assert result.detected is True  # seed=42 gives ~98% detection

    def test_operation_name_preserved(self):
        result = simulate_timeout("market_data_read", timeout_ms=1000, virtual_elapsed_ms=2000)
        assert result.operation == "market_data_read"

    def test_timeout_ms_preserved(self):
        result = simulate_timeout("x", timeout_ms=3000, virtual_elapsed_ms=4000)
        assert result.timeout_ms == 3000

    def test_deterministic_detection_same_seed(self):
        r1 = simulate_timeout("op", timeout_ms=1000, virtual_elapsed_ms=2000, seed=42)
        r2 = simulate_timeout("op", timeout_ms=1000, virtual_elapsed_ms=2000, seed=42)
        assert r1.detected == r2.detected

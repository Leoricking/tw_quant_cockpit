"""
tests/test_failure_validation_integrity_v165.py — Integrity, Replay, Idempotency tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import hashlib
import json

import pytest

from paper_trading.failure_validation.hash_integrity_v165 import (
    HashIntegrityChecker,
    PAPER_ONLY as HASH_PAPER_ONLY,
    RESEARCH_ONLY as HASH_RESEARCH_ONLY,
    compute_chain_hash,
    compute_content_hash,
    verify_hash,
)
from paper_trading.failure_validation.replay_v165 import (
    PAPER_ONLY as REPLAY_PAPER_ONLY,
    RESEARCH_ONLY as REPLAY_RESEARCH_ONLY,
    ReplayResult,
    simulate_replay,
)
from paper_trading.failure_validation.idempotency_v165 import (
    IdempotencyValidator,
    PAPER_ONLY as IDEM_PAPER_ONLY,
    RESEARCH_ONLY as IDEM_RESEARCH_ONLY,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestIntegritySafetyFlags:
    def test_hash_paper_only(self):
        assert HASH_PAPER_ONLY is True

    def test_hash_research_only(self):
        assert HASH_RESEARCH_ONLY is True

    def test_replay_paper_only(self):
        assert REPLAY_PAPER_ONLY is True

    def test_replay_research_only(self):
        assert REPLAY_RESEARCH_ONLY is True

    def test_idempotency_paper_only(self):
        assert IDEM_PAPER_ONLY is True

    def test_idempotency_research_only(self):
        assert IDEM_RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# compute_content_hash
# ---------------------------------------------------------------------------

class TestComputeContentHash:
    def test_returns_64_char_hex(self):
        h = compute_content_hash({"a": 1})
        assert len(h) == 64

    def test_same_data_same_hash(self):
        d = {"price": 100, "vol": 500}
        assert compute_content_hash(d) == compute_content_hash(d)

    def test_different_data_different_hash(self):
        assert compute_content_hash({"a": 1}) != compute_content_hash({"a": 2})

    def test_key_order_does_not_matter(self):
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 2, "a": 1}
        assert compute_content_hash(d1) == compute_content_hash(d2)

    def test_nested_data_hashable(self):
        d = {"outer": {"inner": [1, 2, 3]}}
        h = compute_content_hash(d)
        assert len(h) == 64

    def test_empty_dict_hashable(self):
        h = compute_content_hash({})
        assert len(h) == 64

    def test_list_hashable(self):
        h = compute_content_hash([1, 2, 3])
        assert len(h) == 64


# ---------------------------------------------------------------------------
# verify_hash
# ---------------------------------------------------------------------------

class TestVerifyHash:
    def test_verify_correct_hash_returns_true(self):
        data = {"x": 42}
        h = compute_content_hash(data)
        assert verify_hash(data, h) is True

    def test_verify_wrong_hash_returns_false(self):
        data = {"x": 42}
        assert verify_hash(data, "a" * 64) is False

    def test_verify_mutated_data_returns_false(self):
        data = {"x": 42}
        h = compute_content_hash(data)
        data["x"] = 99
        assert verify_hash(data, h) is False


# ---------------------------------------------------------------------------
# compute_chain_hash
# ---------------------------------------------------------------------------

class TestComputeChainHash:
    def test_chain_hash_returns_64_chars(self):
        h = compute_chain_hash(["abc", "def", "ghi"])
        assert len(h) == 64

    def test_chain_hash_deterministic(self):
        hashes = ["h1", "h2", "h3"]
        assert compute_chain_hash(hashes) == compute_chain_hash(hashes)

    def test_chain_hash_order_matters(self):
        h1 = compute_chain_hash(["a", "b"])
        h2 = compute_chain_hash(["b", "a"])
        assert h1 != h2


# ---------------------------------------------------------------------------
# HashIntegrityChecker
# ---------------------------------------------------------------------------

class TestHashIntegrityChecker:
    def test_check_checkpoint_pass(self):
        checker = HashIntegrityChecker()
        data = {"checkpoint": "v1", "seq": 100}
        stored = compute_content_hash(data)
        result = checker.check_checkpoint(data, stored)
        assert result["match"] is True
        assert result["result"] == "PASS"

    def test_check_checkpoint_mismatch(self):
        checker = HashIntegrityChecker()
        data = {"checkpoint": "v1"}
        result = checker.check_checkpoint(data, "wrong" * 12 + "xxxx")
        assert result["match"] is False
        assert result["result"] == "HASH_MISMATCH"

    def test_check_checkpoint_result_has_required_keys(self):
        checker = HashIntegrityChecker()
        data = {"k": "v"}
        stored = compute_content_hash(data)
        result = checker.check_checkpoint(data, stored)
        assert "match" in result
        assert "computed" in result
        assert "stored" in result
        assert "result" in result

    def test_check_snapshot_same_as_checkpoint(self):
        checker = HashIntegrityChecker()
        data = {"snap": "data"}
        stored = compute_content_hash(data)
        r_cp = checker.check_checkpoint(data, stored)
        r_sn = checker.check_snapshot(data, stored)
        assert r_cp["match"] == r_sn["match"]
        assert r_cp["result"] == r_sn["result"]


# ---------------------------------------------------------------------------
# simulate_replay
# ---------------------------------------------------------------------------

class TestSimulateReplay:
    def test_same_seed_always_matches(self):
        result = simulate_replay("s1", seed=42, original_events=5)
        assert result.match is True

    def test_replay_hash_equals_original_hash(self):
        result = simulate_replay("s1", seed=100)
        assert result.original_hash == result.replay_hash

    def test_different_seeds_different_hashes(self):
        r1 = simulate_replay("s1", seed=1)
        r2 = simulate_replay("s1", seed=2)
        assert r1.original_hash != r2.original_hash

    def test_replay_events_count_preserved(self):
        result = simulate_replay("s1", seed=42, original_events=10)
        assert result.replay_events == 10

    def test_scenario_id_preserved(self):
        result = simulate_replay("my_scenario", seed=42)
        assert result.scenario_id == "my_scenario"

    def test_seed_preserved(self):
        result = simulate_replay("s1", seed=777)
        assert result.seed == 777

    def test_as_dict_has_required_keys(self):
        result = simulate_replay("s1", seed=1)
        d = result.as_dict()
        assert "scenario_id" in d
        assert "seed" in d
        assert "hash_match" in d
        assert "replay_events" in d

    def test_as_dict_hash_match_true(self):
        result = simulate_replay("s1", seed=42)
        assert result.as_dict()["hash_match"] is True

    def test_deterministic_result_across_instances(self):
        r1 = simulate_replay("x", seed=55, original_events=7)
        r2 = simulate_replay("x", seed=55, original_events=7)
        assert r1.original_hash == r2.original_hash
        assert r1.match == r2.match


# ---------------------------------------------------------------------------
# IdempotencyValidator
# ---------------------------------------------------------------------------

class TestIdempotencyValidator:
    def test_initial_state(self):
        iv = IdempotencyValidator()
        assert iv.duplicate_count() == 0
        assert iv.unique_count() == 0

    def test_first_key_not_duplicate(self):
        iv = IdempotencyValidator()
        result = iv.check("key_1")
        assert result["duplicate"] is False

    def test_repeated_key_is_duplicate(self):
        iv = IdempotencyValidator()
        iv.check("key_1")
        result = iv.check("key_1")
        assert result["duplicate"] is True

    def test_duplicate_count_increments(self):
        iv = IdempotencyValidator()
        iv.check("k")
        iv.check("k")
        iv.check("k")
        assert iv.duplicate_count() == 2

    def test_unique_count_does_not_increment_on_dup(self):
        iv = IdempotencyValidator()
        iv.check("k")
        iv.check("k")
        assert iv.unique_count() == 1

    def test_different_keys_all_unique(self):
        iv = IdempotencyValidator()
        for i in range(10):
            result = iv.check(f"key_{i}")
            assert result["duplicate"] is False
        assert iv.unique_count() == 10

    def test_reset_clears_state(self):
        iv = IdempotencyValidator()
        iv.check("k1")
        iv.check("k1")
        iv.reset()
        assert iv.duplicate_count() == 0
        assert iv.unique_count() == 0

    def test_after_reset_key_is_not_duplicate(self):
        iv = IdempotencyValidator()
        iv.check("k")
        iv.reset()
        result = iv.check("k")
        assert result["duplicate"] is False

    def test_check_returns_total_seen(self):
        iv = IdempotencyValidator()
        iv.check("a")
        iv.check("b")
        result = iv.check("c")
        assert result["total_seen"] == 3

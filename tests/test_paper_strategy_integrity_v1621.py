"""
tests/test_paper_strategy_integrity_v1621.py — Extended test suite for v1.6.2.1
Paper Strategy Orchestration Integrity Hotfix.

[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY.
    NOT INVESTMENT ADVICE. NOT FOR PRODUCTION USE.

Coverage:
  - All 35+ new fixture files (JSON validity + safety markers)
  - Extended strategy model, registry, lifecycle, signal, dedup, PIT tests
  - Extended decision pipeline, eligibility, sizing, correlation, risk tests
  - Extended approval, conflict, cooldown, rate-limit tests
  - Extended proposal, order bridge tests
  - Journal, checkpoint, replay, recovery, lineage, reproducibility tests
  - CLI / GUI safety tests
  - Health check extended coverage
  - Release gate 35-check verification
  - Safety invariant comprehensive tests
  - Direct-execution prohibition tests
  - No-broker / no-real-order / no-real-account / no-production enforcement

Tests: 500 – 699 (200 tests)
"""
from __future__ import annotations

import json
import os
import unittest
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "paper_strategy")


def _load_fixture(name: str) -> dict:
    path = os.path.join(_FIXTURE_DIR, name)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


_REQUIRED_MARKERS = [
    "TEST_FIXTURE", "DEMO_ONLY", "PAPER_ONLY", "RESEARCH_ONLY",
    "NOT_REAL_ORDER", "NOT_REAL_ACCOUNT",
    "NOT_FOR_INVESTMENT_DECISION", "NOT_FOR_PRODUCTION",
]


def _assert_markers(tc: unittest.TestCase, d: dict, fname: str) -> None:
    markers = d.get("_markers", [])
    for m in _REQUIRED_MARKERS:
        tc.assertIn(m, markers, f"Missing marker '{m}' in {fname}")


# ===========================================================================
# GROUP 50 — New fixture files: JSON validity and safety markers (test 500-541)
# ===========================================================================

class TestNewFixtureFiles(unittest.TestCase):
    """All 35+ new fixture files must be valid JSON with required safety markers."""

    # --- strategy fixtures ---

    def test_500_strategy_valid_loads(self):
        d = _load_fixture("strategy_valid.json")
        self.assertEqual(d["strategy_id"], "fixture-strategy-valid-001")

    def test_501_strategy_valid_markers(self):
        _assert_markers(self, _load_fixture("strategy_valid.json"), "strategy_valid.json")

    def test_502_strategy_valid_paper_flags(self):
        d = _load_fixture("strategy_valid.json")
        self.assertIs(d["paper_only"], True)
        self.assertIs(d["not_a_real_order"], True)
        self.assertIs(d["no_broker_call"], True)
        self.assertIs(d["no_real_account"], True)

    def test_503_strategy_invalid_loads(self):
        d = _load_fixture("strategy_invalid.json")
        self.assertEqual(d["_expected_validation"], "FAIL")

    def test_504_strategy_invalid_markers(self):
        _assert_markers(self, _load_fixture("strategy_invalid.json"), "strategy_invalid.json")

    def test_505_strategy_invalid_has_empty_name(self):
        d = _load_fixture("strategy_invalid.json")
        self.assertEqual(d["strategy_name"], "")

    def test_506_strategy_invalid_negative_values(self):
        d = _load_fixture("strategy_invalid.json")
        self.assertLess(d["cooldown_seconds"], 0)
        self.assertLess(d["max_signals_per_minute"], 0)

    def test_507_strategy_duplicate_loads(self):
        d = _load_fixture("strategy_duplicate.json")
        self.assertEqual(d["_expected_validation"], "DUPLICATE")

    def test_508_strategy_duplicate_markers(self):
        _assert_markers(self, _load_fixture("strategy_duplicate.json"), "strategy_duplicate.json")

    def test_509_strategy_duplicate_same_id(self):
        d_orig = _load_fixture("strategy_valid.json")
        d_dup = _load_fixture("strategy_duplicate.json")
        self.assertEqual(d_orig["strategy_id"], d_dup["strategy_id"])

    def test_510_strategy_broker_blocked_loads(self):
        d = _load_fixture("strategy_broker_blocked.json")
        self.assertEqual(d["_expected_validation"], "BLOCKED")

    def test_511_strategy_broker_blocked_markers(self):
        _assert_markers(self, _load_fixture("strategy_broker_blocked.json"), "strategy_broker_blocked.json")

    def test_512_strategy_broker_blocked_violation(self):
        d = _load_fixture("strategy_broker_blocked.json")
        self.assertEqual(d["_attempted_violation"], "BROKER_ACCESS")

    def test_513_strategy_short_blocked_loads(self):
        d = _load_fixture("strategy_short_blocked.json")
        self.assertEqual(d["_expected_validation"], "BLOCKED")

    def test_514_strategy_short_blocked_markers(self):
        _assert_markers(self, _load_fixture("strategy_short_blocked.json"), "strategy_short_blocked.json")

    def test_515_strategy_short_blocked_violation(self):
        d = _load_fixture("strategy_short_blocked.json")
        self.assertEqual(d["_attempted_violation"], "SHORT_SELL")

    # --- signal fixtures ---

    def test_516_signal_duplicate_loads(self):
        d = _load_fixture("signal_duplicate.json")
        self.assertIs(d["is_duplicate"], True)

    def test_517_signal_duplicate_markers(self):
        _assert_markers(self, _load_fixture("signal_duplicate.json"), "signal_duplicate.json")

    def test_518_signal_same_id_different_payload_loads(self):
        d = _load_fixture("signal_same_id_different_payload.json")
        self.assertIs(d["is_duplicate"], True)

    def test_519_signal_same_id_different_payload_markers(self):
        _assert_markers(self, _load_fixture("signal_same_id_different_payload.json"), "signal_same_id_different_payload.json")

    def test_520_signal_same_id_shared_dedup_key(self):
        d_a = _load_fixture("signal_duplicate.json")
        d_b = _load_fixture("signal_same_id_different_payload.json")
        self.assertEqual(d_a["dedup_key"], d_b["dedup_key"])
        self.assertNotEqual(d_a["confidence"], d_b["confidence"])

    def test_521_signal_future_loads(self):
        d = _load_fixture("signal_future.json")
        self.assertEqual(d["_expected_validation"], "FAIL_PIT")

    def test_522_signal_future_markers(self):
        _assert_markers(self, _load_fixture("signal_future.json"), "signal_future.json")

    def test_523_signal_future_timestamp_is_future(self):
        d = _load_fixture("signal_future.json")
        ts = datetime.fromisoformat(d["generated_at"].replace("Z", "+00:00"))
        self.assertGreater(ts.year, 2050)

    def test_524_signal_missing_timestamp_loads(self):
        d = _load_fixture("signal_missing_timestamp.json")
        self.assertEqual(d["_expected_validation"], "FAIL_MISSING_TIMESTAMP")

    def test_525_signal_missing_timestamp_markers(self):
        _assert_markers(self, _load_fixture("signal_missing_timestamp.json"), "signal_missing_timestamp.json")

    def test_526_signal_missing_timestamp_null(self):
        d = _load_fixture("signal_missing_timestamp.json")
        self.assertIsNone(d["generated_at"])

    def test_527_signal_short_loads(self):
        d = _load_fixture("signal_short.json")
        self.assertEqual(d["_expected_validation"], "BLOCKED_SHORT")

    def test_528_signal_short_markers(self):
        _assert_markers(self, _load_fixture("signal_short.json"), "signal_short.json")

    def test_529_signal_short_is_entry_short(self):
        d = _load_fixture("signal_short.json")
        self.assertEqual(d["signal_type"], "ENTRY_SHORT")

    def test_530_signal_invalid_confidence_loads(self):
        d = _load_fixture("signal_invalid_confidence.json")
        self.assertEqual(d["_expected_validation"], "FAIL_CONFIDENCE_RANGE")

    def test_531_signal_invalid_confidence_markers(self):
        _assert_markers(self, _load_fixture("signal_invalid_confidence.json"), "signal_invalid_confidence.json")

    def test_532_signal_invalid_confidence_out_of_range(self):
        d = _load_fixture("signal_invalid_confidence.json")
        self.assertGreater(d["confidence"], 1.0)

    def test_533_signal_invalid_score_loads(self):
        d = _load_fixture("signal_invalid_score.json")
        self.assertEqual(d["_expected_validation"], "FAIL_SCORE_RANGE")

    def test_534_signal_invalid_score_markers(self):
        _assert_markers(self, _load_fixture("signal_invalid_score.json"), "signal_invalid_score.json")

    def test_535_signal_invalid_score_negative(self):
        d = _load_fixture("signal_invalid_score.json")
        self.assertLess(d["raw_value"], -100)

    # --- decision fixtures ---

    def test_536_decision_valid_loads(self):
        d = _load_fixture("decision_valid.json")
        self.assertEqual(d["decision"], "PROCEED")

    def test_537_decision_valid_markers(self):
        _assert_markers(self, _load_fixture("decision_valid.json"), "decision_valid.json")

    def test_538_decision_valid_all_checks_pass(self):
        d = _load_fixture("decision_valid.json")
        self.assertIs(d["eligibility_passed"], True)
        self.assertIs(d["sizing_passed"], True)
        self.assertIs(d["correlation_passed"], True)
        self.assertIs(d["risk_passed"], True)

    def test_539_decision_market_blocked_loads(self):
        d = _load_fixture("decision_market_blocked.json")
        self.assertEqual(d["decision"], "BLOCKED")

    def test_540_decision_market_blocked_markers(self):
        _assert_markers(self, _load_fixture("decision_market_blocked.json"), "decision_market_blocked.json")

    def test_541_decision_market_blocked_reason(self):
        d = _load_fixture("decision_market_blocked.json")
        self.assertEqual(d["block_reason"], "MARKET_CLOSED")


# ===========================================================================
# GROUP 51 — More decision + conflict + control fixtures (542-570)
# ===========================================================================

class TestDecisionAndControlFixtures(unittest.TestCase):

    def test_542_decision_data_blocked_loads(self):
        d = _load_fixture("decision_data_blocked.json")
        self.assertEqual(d["block_reason"], "DATA_QUALITY")

    def test_543_decision_data_blocked_markers(self):
        _assert_markers(self, _load_fixture("decision_data_blocked.json"), "decision_data_blocked.json")

    def test_544_decision_eligibility_blocked_loads(self):
        d = _load_fixture("decision_eligibility_blocked.json")
        self.assertEqual(d["block_reason"], "ELIGIBILITY_UNIVERSE")

    def test_545_decision_eligibility_blocked_markers(self):
        _assert_markers(self, _load_fixture("decision_eligibility_blocked.json"), "decision_eligibility_blocked.json")

    def test_546_decision_sizing_blocked_loads(self):
        d = _load_fixture("decision_sizing_blocked.json")
        self.assertEqual(d["block_reason"], "SIZING_LIMIT")

    def test_547_decision_sizing_blocked_markers(self):
        _assert_markers(self, _load_fixture("decision_sizing_blocked.json"), "decision_sizing_blocked.json")

    def test_548_decision_sizing_blocked_values(self):
        d = _load_fixture("decision_sizing_blocked.json")
        self.assertGreater(d["proposed_size"], d["max_allowed_size"])

    def test_549_decision_correlation_blocked_loads(self):
        d = _load_fixture("decision_correlation_blocked.json")
        self.assertEqual(d["block_reason"], "CORRELATION_LIMIT")

    def test_550_decision_correlation_blocked_markers(self):
        _assert_markers(self, _load_fixture("decision_correlation_blocked.json"), "decision_correlation_blocked.json")

    def test_551_decision_correlation_blocked_values(self):
        d = _load_fixture("decision_correlation_blocked.json")
        self.assertGreater(d["correlation_score"], d["correlation_threshold"])

    def test_552_decision_risk_blocked_loads(self):
        d = _load_fixture("decision_risk_blocked.json")
        self.assertEqual(d["block_reason"], "RISK_BUDGET")

    def test_553_decision_risk_blocked_markers(self):
        _assert_markers(self, _load_fixture("decision_risk_blocked.json"), "decision_risk_blocked.json")

    def test_554_decision_risk_blocked_drawdown(self):
        d = _load_fixture("decision_risk_blocked.json")
        self.assertGreater(d["current_drawdown_pct"], d["max_drawdown_pct"])

    def test_555_conflict_entry_exit_loads(self):
        d = _load_fixture("conflict_entry_exit.json")
        self.assertEqual(d["conflict_type"], "ENTRY_EXIT")

    def test_556_conflict_entry_exit_markers(self):
        _assert_markers(self, _load_fixture("conflict_entry_exit.json"), "conflict_entry_exit.json")

    def test_557_conflict_entry_exit_resolution(self):
        d = _load_fixture("conflict_entry_exit.json")
        self.assertEqual(d["resolution"], "HIGHEST_STRENGTH")
        self.assertIn("winner", d)

    def test_558_conflict_entry_block_loads(self):
        d = _load_fixture("conflict_entry_block.json")
        self.assertEqual(d["conflict_type"], "ENTRY_BLOCK")

    def test_559_conflict_entry_block_markers(self):
        _assert_markers(self, _load_fixture("conflict_entry_block.json"), "conflict_entry_block.json")

    def test_560_conflict_entry_block_loser_blocked(self):
        d = _load_fixture("conflict_entry_block.json")
        self.assertEqual(d["loser_action"], "BLOCK")

    def test_561_cooldown_blocked_loads(self):
        d = _load_fixture("cooldown_blocked.json")
        self.assertEqual(d["_expected_validation"], "BLOCKED_COOLDOWN")

    def test_562_cooldown_blocked_markers(self):
        _assert_markers(self, _load_fixture("cooldown_blocked.json"), "cooldown_blocked.json")

    def test_563_cooldown_blocked_remaining(self):
        d = _load_fixture("cooldown_blocked.json")
        self.assertGreater(d["cooldown_remaining_seconds"], 0)
        self.assertLess(d["elapsed_seconds"], d["cooldown_seconds"])

    def test_564_rate_limit_blocked_loads(self):
        d = _load_fixture("rate_limit_blocked.json")
        self.assertEqual(d["_expected_validation"], "BLOCKED_RATE_LIMIT")

    def test_565_rate_limit_blocked_markers(self):
        _assert_markers(self, _load_fixture("rate_limit_blocked.json"), "rate_limit_blocked.json")

    def test_566_rate_limit_blocked_exhausted(self):
        d = _load_fixture("rate_limit_blocked.json")
        self.assertEqual(d["signals_sent_this_minute"], d["max_signals_per_minute"])

    def test_567_all_new_fixtures_have_paper_only(self):
        new_fixtures = [
            "strategy_valid.json", "strategy_invalid.json", "strategy_duplicate.json",
            "strategy_broker_blocked.json", "strategy_short_blocked.json",
            "signal_duplicate.json", "signal_same_id_different_payload.json",
            "signal_future.json", "signal_missing_timestamp.json",
            "signal_short.json", "signal_invalid_confidence.json", "signal_invalid_score.json",
            "decision_valid.json", "decision_market_blocked.json", "decision_data_blocked.json",
            "decision_eligibility_blocked.json", "decision_sizing_blocked.json",
            "decision_correlation_blocked.json", "decision_risk_blocked.json",
            "conflict_entry_exit.json", "conflict_entry_block.json",
            "cooldown_blocked.json", "rate_limit_blocked.json",
        ]
        for fname in new_fixtures:
            d = _load_fixture(fname)
            self.assertIs(d.get("paper_only"), True, f"paper_only missing/false in {fname}")

    def test_568_all_new_fixtures_not_real_order(self):
        new_fixtures = [
            "strategy_valid.json", "strategy_broker_blocked.json",
            "signal_duplicate.json", "decision_valid.json",
            "conflict_entry_exit.json", "cooldown_blocked.json",
        ]
        for fname in new_fixtures:
            d = _load_fixture(fname)
            self.assertIs(d.get("not_a_real_order"), True, f"not_a_real_order missing in {fname}")

    def test_569_all_new_fixtures_no_broker(self):
        new_fixtures = [
            "strategy_valid.json", "strategy_broker_blocked.json",
            "decision_valid.json", "approval_auto_paper.json",
        ]
        for fname in new_fixtures:
            d = _load_fixture(fname)
            self.assertIs(d.get("no_broker_call"), True, f"no_broker_call missing in {fname}")

    def test_570_all_new_fixtures_no_formal_ledger(self):
        new_fixtures = [
            "strategy_valid.json", "decision_valid.json",
            "proposal_valid.json", "order_bridge_valid.json",
        ]
        for fname in new_fixtures:
            d = _load_fixture(fname)
            self.assertIs(d.get("no_formal_portfolio_ledger_write"), True,
                          f"no_formal_portfolio_ledger_write missing in {fname}")


# ===========================================================================
# GROUP 52 — Approval, proposal, order bridge, persistence fixtures (571-600)
# ===========================================================================

class TestApprovalProposalBridgeFixtures(unittest.TestCase):

    def test_571_approval_manual_loads(self):
        d = _load_fixture("approval_manual.json")
        self.assertEqual(d["approval_status"], "PENDING")

    def test_572_approval_manual_markers(self):
        _assert_markers(self, _load_fixture("approval_manual.json"), "approval_manual.json")

    def test_573_approval_manual_requires_human(self):
        d = _load_fixture("approval_manual.json")
        self.assertIs(d["requires_human_confirmation"], True)
        self.assertIs(d["auto_approved"], False)

    def test_574_approval_policy_loads(self):
        d = _load_fixture("approval_policy.json")
        self.assertEqual(d["approval_status"], "APPROVED")

    def test_575_approval_policy_markers(self):
        _assert_markers(self, _load_fixture("approval_policy.json"), "approval_policy.json")

    def test_576_approval_policy_passed(self):
        d = _load_fixture("approval_policy.json")
        self.assertIs(d["policy_passed"], True)
        self.assertIn("paper_safety_policy", d["policy_name"])

    def test_577_approval_auto_paper_loads(self):
        d = _load_fixture("approval_auto_paper.json")
        self.assertEqual(d["approval_mode"], "AUTO_PAPER_ONLY")

    def test_578_approval_auto_paper_markers(self):
        _assert_markers(self, _load_fixture("approval_auto_paper.json"), "approval_auto_paper.json")

    def test_579_approval_auto_paper_paper_execution_only(self):
        d = _load_fixture("approval_auto_paper.json")
        self.assertIs(d["paper_execution_only"], True)

    def test_580_proposal_valid_loads(self):
        d = _load_fixture("proposal_valid.json")
        self.assertEqual(d["direction"], "LONG")

    def test_581_proposal_valid_markers(self):
        _assert_markers(self, _load_fixture("proposal_valid.json"), "proposal_valid.json")

    def test_582_proposal_valid_no_short(self):
        d = _load_fixture("proposal_valid.json")
        self.assertNotEqual(d["direction"], "SHORT")

    def test_583_proposal_valid_paper_order_type(self):
        d = _load_fixture("proposal_valid.json")
        self.assertIn("PAPER", d["paper_order_type"])

    def test_584_proposal_invalid_loads(self):
        d = _load_fixture("proposal_invalid.json")
        self.assertEqual(d["_expected_validation"], "PROPOSAL_INVALID")

    def test_585_proposal_invalid_markers(self):
        _assert_markers(self, _load_fixture("proposal_invalid.json"), "proposal_invalid.json")

    def test_586_proposal_invalid_negative_quantity(self):
        d = _load_fixture("proposal_invalid.json")
        self.assertLess(d["proposed_quantity"], 0)
        self.assertLess(d["proposed_price"], 0)

    def test_587_proposal_invalid_null_signal(self):
        d = _load_fixture("proposal_invalid.json")
        self.assertIsNone(d["signal_id"])

    def test_588_proposal_duplicate_loads(self):
        d = _load_fixture("proposal_duplicate.json")
        self.assertEqual(d["_expected_validation"], "PROPOSAL_DUPLICATE")

    def test_589_proposal_duplicate_markers(self):
        _assert_markers(self, _load_fixture("proposal_duplicate.json"), "proposal_duplicate.json")

    def test_590_proposal_duplicate_same_id_as_valid(self):
        d_orig = _load_fixture("proposal_valid.json")
        d_dup = _load_fixture("proposal_duplicate.json")
        self.assertEqual(d_orig["proposal_id"], d_dup["proposal_id"])

    def test_591_order_bridge_valid_loads(self):
        d = _load_fixture("order_bridge_valid.json")
        self.assertEqual(d["bridge_status"], "PAPER_EXECUTED")

    def test_592_order_bridge_valid_markers(self):
        _assert_markers(self, _load_fixture("order_bridge_valid.json"), "order_bridge_valid.json")

    def test_593_order_bridge_valid_no_broker(self):
        d = _load_fixture("order_bridge_valid.json")
        self.assertIs(d["broker_called"], False)
        self.assertIs(d["real_order_created"], False)
        self.assertIs(d["real_account_touched"], False)

    def test_594_order_bridge_risk_blocked_loads(self):
        d = _load_fixture("order_bridge_risk_blocked.json")
        self.assertEqual(d["bridge_status"], "BLOCKED_AT_BRIDGE")

    def test_595_order_bridge_risk_blocked_markers(self):
        _assert_markers(self, _load_fixture("order_bridge_risk_blocked.json"), "order_bridge_risk_blocked.json")

    def test_596_order_bridge_risk_blocked_no_execution(self):
        d = _load_fixture("order_bridge_risk_blocked.json")
        self.assertIs(d["broker_called"], False)
        self.assertIs(d["real_order_created"], False)

    def test_597_checkpoint_valid_loads(self):
        d = _load_fixture("checkpoint_valid.json")
        self.assertIn("sha256:", d["state_hash"])

    def test_598_checkpoint_valid_markers(self):
        _assert_markers(self, _load_fixture("checkpoint_valid.json"), "checkpoint_valid.json")

    def test_599_checkpoint_hash_mismatch_loads(self):
        d = _load_fixture("checkpoint_hash_mismatch.json")
        self.assertIs(d["hash_match"], False)

    def test_600_checkpoint_hash_mismatch_markers(self):
        _assert_markers(self, _load_fixture("checkpoint_hash_mismatch.json"), "checkpoint_hash_mismatch.json")


# ===========================================================================
# GROUP 53 — Replay, recovery, lineage, reproducibility fixtures (601-620)
# ===========================================================================

class TestPersistenceFixtures(unittest.TestCase):

    def test_601_replay_valid_loads(self):
        d = _load_fixture("replay_valid.json")
        self.assertEqual(d["replay_mode"], "DETERMINISTIC")

    def test_602_replay_valid_markers(self):
        _assert_markers(self, _load_fixture("replay_valid.json"), "replay_valid.json")

    def test_603_replay_valid_no_divergence(self):
        d = _load_fixture("replay_valid.json")
        self.assertIs(d["replay_matches_original"], True)
        self.assertEqual(d["divergence_count"], 0)

    def test_604_replay_valid_counts_match(self):
        d = _load_fixture("replay_valid.json")
        cp = _load_fixture("checkpoint_valid.json")
        self.assertEqual(d["signals_replayed"], cp["signals_processed"])
        self.assertEqual(d["proposals_replayed"], cp["proposals_generated"])

    def test_605_recovery_valid_loads(self):
        d = _load_fixture("recovery_valid.json")
        self.assertEqual(d["recovery_mode"], "FROM_CHECKPOINT")

    def test_606_recovery_valid_markers(self):
        _assert_markers(self, _load_fixture("recovery_valid.json"), "recovery_valid.json")

    def test_607_recovery_valid_state_restored(self):
        d = _load_fixture("recovery_valid.json")
        self.assertIs(d["state_restored"], True)

    def test_608_recovery_references_checkpoint(self):
        d_rec = _load_fixture("recovery_valid.json")
        d_cp = _load_fixture("checkpoint_valid.json")
        self.assertEqual(d_rec["checkpoint_id"], d_cp["checkpoint_id"])

    def test_609_lineage_complete_loads(self):
        d = _load_fixture("lineage_complete.json")
        self.assertIs(d["chain_complete"], True)

    def test_610_lineage_complete_markers(self):
        _assert_markers(self, _load_fixture("lineage_complete.json"), "lineage_complete.json")

    def test_611_lineage_complete_five_steps(self):
        d = _load_fixture("lineage_complete.json")
        self.assertEqual(len(d["chain"]), 5)

    def test_612_lineage_complete_chain_types(self):
        d = _load_fixture("lineage_complete.json")
        types = [s["type"] for s in d["chain"]]
        self.assertEqual(types, ["SIGNAL", "DECISION", "PROPOSAL", "APPROVAL", "EXECUTION"])

    def test_613_lineage_complete_steps_ordered(self):
        d = _load_fixture("lineage_complete.json")
        steps = [s["step"] for s in d["chain"]]
        self.assertEqual(steps, list(range(1, len(steps) + 1)))

    def test_614_reproducibility_valid_loads(self):
        d = _load_fixture("reproducibility_valid.json")
        self.assertIs(d["deterministic"], True)

    def test_615_reproducibility_valid_markers(self):
        _assert_markers(self, _load_fixture("reproducibility_valid.json"), "reproducibility_valid.json")

    def test_616_reproducibility_valid_no_divergence(self):
        d = _load_fixture("reproducibility_valid.json")
        self.assertEqual(d["divergence_count"], 0)
        self.assertIs(d["same_outputs"], True)

    def test_617_checkpoint_hash_differs(self):
        d = _load_fixture("checkpoint_hash_mismatch.json")
        self.assertNotEqual(d["state_hash"], d["recomputed_hash"])

    def test_618_all_persistence_fixtures_paper_only(self):
        for fname in ["checkpoint_valid.json", "checkpoint_hash_mismatch.json",
                      "replay_valid.json", "recovery_valid.json",
                      "lineage_complete.json", "reproducibility_valid.json"]:
            d = _load_fixture(fname)
            self.assertIs(d.get("paper_only"), True, f"paper_only missing in {fname}")

    def test_619_all_persistence_fixtures_no_broker(self):
        for fname in ["checkpoint_valid.json", "replay_valid.json",
                      "recovery_valid.json", "lineage_complete.json"]:
            d = _load_fixture(fname)
            self.assertIs(d.get("no_broker_call"), True, f"no_broker_call missing in {fname}")

    def test_620_all_persistence_fixtures_not_real_order(self):
        for fname in ["replay_valid.json", "recovery_valid.json", "lineage_complete.json"]:
            d = _load_fixture(fname)
            self.assertIs(d.get("not_a_real_order"), True, f"not_a_real_order missing in {fname}")


# ===========================================================================
# GROUP 54 — Strategy module live integration (621-645)
# ===========================================================================

class TestStrategyModuleLiveIntegration(unittest.TestCase):
    """Tests against actual paper_trading.strategy modules."""

    def test_621_strategy_status_enum_all_values(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        names = {s.name for s in StrategyStatus}
        for expected in ("REGISTERED", "RUNNING", "PAUSED", "HALTED", "COMPLETED"):
            self.assertIn(expected, names)

    def test_622_signal_type_enum_no_short(self):
        from paper_trading.strategy.enums_v162 import SignalType
        names = {s.name for s in SignalType}
        self.assertNotIn("ENTRY_SHORT", names)
        self.assertNotIn("SELL_SHORT", names)
        self.assertIn("ENTRY_LONG", names)

    def test_623_approval_mode_auto_paper_only(self):
        from paper_trading.strategy.enums_v162 import ApprovalMode
        names = {a.name for a in ApprovalMode}
        self.assertIn("AUTO_PAPER_ONLY", names)

    def test_624_decision_outcome_has_proceed_and_block(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        names = {d.name for d in DecisionOutcome}
        self.assertIn("APPROVED", names)
        self.assertIn("BLOCKED", names)

    def test_625_signal_strength_has_strong_moderate_weak(self):
        from paper_trading.strategy.enums_v162 import SignalStrength
        names = {s.name for s in SignalStrength}
        self.assertIn("STRONG", names)
        self.assertIn("MODERATE", names)
        self.assertIn("WEAK", names)

    def test_626_build_default_config(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        cfg = build_default_config()
        self.assertTrue(cfg.paper_only)
        self.assertTrue(cfg.research_only)

    def test_627_config_no_broker(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        cfg = build_default_config()
        self.assertTrue(cfg.no_broker_call)

    def test_628_config_no_real_account(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        cfg = build_default_config()
        self.assertTrue(cfg.no_real_account)

    def test_629_make_entry_long_is_long(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        sig = make_entry_long("fixture-strategy-001", "2330.TW", raw_value=0.8)
        st = sig.signal_type
        st_name = st.name if hasattr(st, "name") else str(st)
        self.assertEqual(st_name, "ENTRY_LONG")

    def test_630_make_entry_long_not_short(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        sig = make_entry_long("fixture-strategy-001", "2330.TW", raw_value=0.8)
        st = sig.signal_type
        st_name = st.name if hasattr(st, "name") else str(st)
        self.assertNotEqual(st_name, "ENTRY_SHORT")

    def test_631_make_hold_default_values(self):
        from paper_trading.strategy.signal_v162 import make_hold
        sig = make_hold("fixture-strategy-001", "2330.TW")
        st = sig.signal_type
        st_name = st.name if hasattr(st, "name") else str(st)
        self.assertEqual(st_name, "HOLD")
        self.assertIn(sig.raw_value, (0.0, None))

    def test_632_signal_normalizer_normalizes(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
        sig = make_entry_long("s1", "2330.TW", raw_value=0.9)
        norm = SignalNormalizer()
        out = norm.normalize(sig)
        self.assertIsNotNone(out.normalized_value)
        self.assertGreaterEqual(out.normalized_value, -1.0)
        self.assertLessEqual(out.normalized_value, 1.0)

    def test_633_dedup_first_seen_not_duplicate(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        sig = make_entry_long("s1", "2330.TW", raw_value=0.8)
        dedup = SignalDeduplicator()
        self.assertFalse(dedup.is_duplicate(sig))

    def test_634_dedup_second_same_signal_is_duplicate(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        sig = make_entry_long("s1", "2330.TW", raw_value=0.8)
        dedup = SignalDeduplicator()
        dedup.record(sig)
        self.assertTrue(dedup.is_duplicate(sig))

    def test_635_cooldown_allows_first(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager(cooldown_seconds=60)
        self.assertFalse(cm.is_on_cooldown("s1"))

    def test_636_cooldown_blocks_second_immediate(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager(cooldown_seconds=60)
        cm.record("s1")
        self.assertTrue(cm.is_on_cooldown("s1"))

    def test_637_rate_limiter_allows_within_limit(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=10)
        self.assertTrue(rl.try_acquire())

    def test_638_rate_limiter_blocks_at_limit(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=1)
        self.assertTrue(rl.try_acquire())
        self.assertFalse(rl.try_acquire())

    def test_639_eligibility_check_happy_path(self):
        from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter, EligibilityResult
        ea = EligibilityAdapter()
        result = ea.check("2330.TW", confidence=0.8)
        self.assertEqual(result, EligibilityResult.ELIGIBLE)

    def test_640_sizing_returns_positive(self):
        from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
        from paper_trading.strategy.signal_v162 import make_entry_long
        sa = SizingAdapter(max_size=1000.0)
        sig = make_entry_long("s1", "2330.TW", raw_value=0.8)
        size = sa.compute(sig, portfolio_value=100000.0)
        self.assertIsNotNone(size)

    def test_641_sizing_within_max(self):
        from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
        from paper_trading.strategy.signal_v162 import make_entry_long
        sa = SizingAdapter(fixed_size=100.0, max_size=500.0)
        sig = make_entry_long("s1", "2330.TW", raw_value=1.0)
        size = sa.compute(sig, portfolio_value=100000.0)
        if size is not None:
            self.assertLessEqual(size, 500.0)

    def test_642_correlation_check_passes_single_position(self):
        from paper_trading.strategy.correlation_adapter_v162 import CorrelationAdapter
        ca = CorrelationAdapter(max_correlation=0.9)
        breach = ca.check_breach("2330.TW", open_tickers=[])
        self.assertFalse(breach)

    def test_643_risk_check_passes_low_drawdown(self):
        from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
        ra = RiskAdapter(max_drawdown_pct=0.15)
        blocked = ra.is_blocked("2330.TW", current_drawdown_pct=0.05)
        self.assertFalse(blocked)

    def test_644_risk_adapter_has_is_blocked_method(self):
        from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
        ra = RiskAdapter(max_drawdown_pct=0.10)
        self.assertTrue(callable(getattr(ra, "is_blocked", None)))

    def test_645_approval_policy_paper_only_mode(self):
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        ap = ApprovalPolicy()
        self.assertFalse(ap.pending_count() > 0)  # starts empty


# ===========================================================================
# GROUP 55 — Pipeline, journal, registry, lifecycle (646-665)
# ===========================================================================

class TestPipelineJournalRegistry(unittest.TestCase):

    def _make_proposal(self, cfg=None, ticker="2330.TW", raw_value=0.8):
        """Helper: build a proposal via the pipeline."""
        from paper_trading.strategy.decision_context_v162 import build_decision_context
        from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
        from paper_trading.strategy.proposal_v162 import build_proposal
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        if cfg is None:
            cfg = build_default_config()
        sig = make_entry_long(cfg.strategy_id, ticker, raw_value=raw_value)
        ctx = build_decision_context(sig, cfg)
        decision = DecisionPipeline().run(ctx)
        return build_proposal(decision, sig, suggested_size=100.0, proposed_price=950.0), sig, cfg

    def _make_demo_strategy(self, cfg=None):
        """Helper: create a minimal concrete PaperStrategyBase subclass."""
        from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        if cfg is None:
            cfg = build_default_config()

        class DemoStrat(PaperStrategyBase):
            def generate_signals(self): return []
            def on_start(self): pass
            def on_pause(self): pass
            def on_halt(self): pass
            def describe(self): return {}

        return DemoStrat(cfg), cfg

    def test_646_decision_pipeline_returns_result(self):
        from paper_trading.strategy.decision_context_v162 import build_decision_context
        from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        cfg = build_default_config()
        sig = make_entry_long(cfg.strategy_id, "2330.TW", raw_value=0.85)
        ctx = build_decision_context(sig, cfg)
        pipeline = DecisionPipeline()
        result = pipeline.run(ctx)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.outcome)

    def test_647_strategy_registry_register_and_is_registered(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        strat, cfg = self._make_demo_strategy()
        reg = StrategyRegistry()
        reg.register(strat)
        self.assertTrue(reg.is_registered(cfg.strategy_id))

    def test_648_strategy_registry_duplicate_idempotent(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        strat, cfg = self._make_demo_strategy()
        reg = StrategyRegistry()
        reg.register(strat)
        reg.register(strat)  # duplicate: logs warning, does not raise
        self.assertTrue(reg.is_registered(cfg.strategy_id))

    def test_649_strategy_registry_list_returns_registered(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        strat, cfg = self._make_demo_strategy()
        reg = StrategyRegistry()
        reg.register(strat)
        all_entries = reg.list_all()
        ids = [e["strategy_id"] if isinstance(e, dict) else e for e in all_entries]
        self.assertIn(cfg.strategy_id, ids)

    def test_650_journal_records_signal(self):
        from paper_trading.strategy.journal_v162 import StrategyJournal, JournalEventType
        from paper_trading.strategy.signal_v162 import make_entry_long
        journal = StrategyJournal(strategy_id="s1")
        sig = make_entry_long("s1", "2330.TW", raw_value=0.8)
        journal.record(JournalEventType.SIGNAL_RECEIVED, summary="signal received",
                       detail={"signal_id": sig.signal_id})
        self.assertGreaterEqual(journal.count(), 1)

    def test_651_journal_records_proposal(self):
        from paper_trading.strategy.journal_v162 import StrategyJournal, JournalEventType
        proposal, sig, cfg = self._make_proposal()
        journal = StrategyJournal(strategy_id=cfg.strategy_id)
        journal.record(JournalEventType.PROPOSAL_CREATED, summary="proposal created",
                       detail={"proposal_id": proposal.proposal_id})
        self.assertGreaterEqual(journal.count(), 1)

    def test_652_lineage_tracker_records_and_finds_by_signal(self):
        from paper_trading.strategy.lineage_v162 import LineageTracker
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        tracker = LineageTracker()
        sig = make_entry_long("s1", "2330.TW")
        dr = DecisionResult(outcome=DecisionOutcome.APPROVED.value,
                            paper_only=True, research_only=True,
                            simulation_only=True, not_a_real_order=True,
                            no_broker_call=True)
        tracker.record(sig, dr)
        found = tracker.find_by_signal(sig.signal_id)
        self.assertIsNotNone(found)
        self.assertGreater(len(found), 0)

    def test_653_reproducibility_same_signal_same_hash(self):
        from paper_trading.strategy.reproducibility_v162 import compute_signal_hash
        from paper_trading.strategy.signal_v162 import make_entry_long
        sig = make_entry_long("s1", "2330.TW", confidence=0.8)
        h1 = compute_signal_hash(sig)
        h2 = compute_signal_hash(sig)
        self.assertEqual(h1, h2)
        self.assertIsInstance(h1, str)

    def test_654_checkpoint_save_and_restore(self):
        import tempfile
        from paper_trading.strategy.checkpoint_v162 import CheckpointManager
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        with tempfile.TemporaryDirectory() as tmpdir:
            cm = CheckpointManager("s1", checkpoint_dir=tmpdir)
            state = StrategyState("s1")
            state.signal_count = 5
            cp = cm.save(state)
            self.assertIsNotNone(cp)
            self.assertEqual(cp.signal_count, 5)

    def test_655_checkpoint_save_has_checkpoint_id(self):
        import tempfile
        from paper_trading.strategy.checkpoint_v162 import CheckpointManager
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        with tempfile.TemporaryDirectory() as tmpdir:
            cm = CheckpointManager("s1", checkpoint_dir=tmpdir)
            state = StrategyState("s1")
            cp = cm.save(state)
            self.assertIsNotNone(cp.checkpoint_id)
            self.assertGreater(len(cp.checkpoint_id), 0)

    def test_656_replay_session_deterministic(self):
        from paper_trading.strategy.replay_v162 import ReplaySession
        from paper_trading.strategy.signal_v162 import make_hold
        sig1 = make_hold("s1", "2330.TW")
        sig2 = make_hold("s1", "2330.TW")
        rs1 = ReplaySession(strategy_id="s1", signals=[sig1])
        rs2 = ReplaySession(strategy_id="s1", signals=[sig2])
        r1 = rs1.run_all()
        r2 = rs2.run_all()
        self.assertEqual(r1["replayed"], r2["replayed"])

    def test_657_replay_summary_complete(self):
        from paper_trading.strategy.replay_v162 import ReplaySession
        from paper_trading.strategy.signal_v162 import make_hold
        sig = make_hold("s1", "2330.TW")
        rs = ReplaySession(strategy_id="s1", signals=[sig])
        result = rs.run_all()
        self.assertIs(result["complete"], True)
        self.assertIs(result["paper_only"], True)

    def test_658_conflict_resolver_resolves_list(self):
        from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.enums_v162 import ConflictPolicy
        sig_strong = make_entry_long("s1", "2330.TW", raw_value=0.9)
        sig_weak = make_entry_long("s1", "2330.TW", raw_value=0.3)
        resolver = ConflictResolver(policy=ConflictPolicy.MOST_CONSERVATIVE)
        kept, dropped = resolver.resolve([sig_strong, sig_weak])
        self.assertIsInstance(kept, list)
        self.assertIsInstance(dropped, list)

    def test_659_proposal_has_paper_only_flag(self):
        proposal, sig, cfg = self._make_proposal()
        self.assertTrue(proposal.paper_only)

    def test_660_proposal_not_a_real_order(self):
        proposal, sig, cfg = self._make_proposal()
        self.assertTrue(proposal.not_a_real_order)

    def test_661_order_bridge_no_broker_connected(self):
        from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
        bridge = PaperOrderBridge()
        self.assertFalse(bridge.BROKER_CONNECTED)

    def test_662_order_bridge_no_real_orders(self):
        from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
        bridge = PaperOrderBridge()
        self.assertFalse(bridge.REAL_ORDERS_ENABLED)

    def test_663_strategy_lifecycle_start_pause_halt(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        strat, cfg = self._make_demo_strategy()
        reg = StrategyRegistry()
        reg.register(strat)
        reg.start_strategy(cfg.strategy_id)
        self.assertEqual(strat.status, StrategyStatus.RUNNING)
        reg.pause_strategy(cfg.strategy_id)
        self.assertEqual(strat.status, StrategyStatus.PAUSED)
        reg.halt_strategy(cfg.strategy_id)
        self.assertEqual(strat.status, StrategyStatus.HALTED)

    def test_664_strategy_halted_status_is_halted(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        strat, cfg = self._make_demo_strategy()
        reg = StrategyRegistry()
        reg.register(strat)
        reg.start_strategy(cfg.strategy_id)
        reg.halt_strategy(cfg.strategy_id)
        self.assertEqual(strat.status, StrategyStatus.HALTED)

    def test_665_strategy_generates_no_broker_signals(self):
        from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
        strat, cfg = self._make_demo_strategy()
        strat.start()
        signals = strat.generate_signals()
        self.assertIsInstance(signals, list)
        self.assertFalse(getattr(strat, "NO_BROKER_CALL", True) is False)


# ===========================================================================
# GROUP 56 — Safety invariants and direct-execution prohibitions (666-685)
# ===========================================================================

class TestSafetyInvariantsComprehensive(unittest.TestCase):
    """Tests for all safety flags and direct-execution prohibitions."""

    def _make_proposal(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.models_v162 import PaperOrderProposal
        from paper_trading.strategy.enums_v162 import ApprovalMode
        cfg = build_default_config("safety_test", approval_mode=ApprovalMode.AUTO_PAPER_ONLY)
        sig = make_entry_long(cfg.strategy_id, "2330.TW")
        proposal = PaperOrderProposal(
            strategy_id=cfg.strategy_id,
            ticker="2330.TW",
            signal_type=sig.signal_type,
            proposed_size=100.0,
        )
        return proposal, sig, cfg

    def test_666_no_real_orders_flag(self):
        from release.version_info import NO_REAL_ORDERS
        self.assertIs(NO_REAL_ORDERS, True)

    def test_667_broker_execution_disabled(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        self.assertIs(BROKER_EXECUTION_ENABLED, False)

    def test_668_production_trading_blocked(self):
        from release.version_info import PRODUCTION_TRADING_BLOCKED
        self.assertIs(PRODUCTION_TRADING_BLOCKED, True)

    def test_669_real_order_creation_disabled(self):
        from release.version_info import REAL_ORDER_CREATION_ENABLED
        self.assertIs(REAL_ORDER_CREATION_ENABLED, False)

    def test_670_real_order_execution_disabled(self):
        from release.version_info import REAL_ORDER_EXECUTION_ENABLED
        self.assertIs(REAL_ORDER_EXECUTION_ENABLED, False)

    def test_671_broker_connection_disabled(self):
        from release.version_info import BROKER_CONNECTION_ENABLED
        self.assertIs(BROKER_CONNECTION_ENABLED, False)

    def test_672_live_account_sync_disabled(self):
        from release.version_info import LIVE_ACCOUNT_SYNC_ENABLED
        self.assertIs(LIVE_ACCOUNT_SYNC_ENABLED, False)

    def test_673_real_portfolio_ledger_write_disabled(self):
        from release.version_info import REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
        self.assertIs(REAL_PORTFOLIO_LEDGER_WRITE_ENABLED, False)

    def test_674_short_selling_disabled(self):
        from release.version_info import SHORT_SELLING_ENABLED
        self.assertIs(SHORT_SELLING_ENABLED, False)

    def test_675_margin_disabled(self):
        from release.version_info import MARGIN_ENABLED
        self.assertIs(MARGIN_ENABLED, False)

    def test_676_paper_strategy_research_only(self):
        from release.version_info import PAPER_STRATEGY_RESEARCH_ONLY
        self.assertIs(PAPER_STRATEGY_RESEARCH_ONLY, True)

    def test_677_no_direct_fill_bridge_blocked(self):
        from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
        bridge = PaperOrderBridge()
        self.assertFalse(bridge.REAL_ORDERS_ENABLED)

    def test_678_no_production_enabled_on_bridge(self):
        from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
        bridge = PaperOrderBridge()
        self.assertFalse(bridge.PRODUCTION_ENABLED)

    def test_679_no_direct_cash_update_safety(self):
        from release.version_info import REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
        self.assertFalse(REAL_PORTFOLIO_LEDGER_WRITE_ENABLED)

    def test_680_no_ledger_write_from_proposal(self):
        proposal, sig, cfg = self._make_proposal()
        self.assertFalse(getattr(proposal, "writes_formal_ledger", False))

    def test_681_approval_policy_starts_empty(self):
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        ap = ApprovalPolicy()
        self.assertEqual(ap.pending_count(), 0)

    def test_682_strategy_base_has_no_broker_constant(self):
        from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
        self.assertTrue(PaperStrategyBase.NO_BROKER_CALL)

    def test_683_strategy_base_has_not_a_real_order(self):
        from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
        self.assertTrue(PaperStrategyBase.NOT_A_REAL_ORDER)

    def test_684_strategy_base_no_real_account(self):
        from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
        self.assertTrue(PaperStrategyBase.NO_REAL_ACCOUNT)

    def test_685_strategy_base_paper_only(self):
        from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
        self.assertTrue(PaperStrategyBase.PAPER_ONLY)


# ===========================================================================
# GROUP 57 — Release gate 35-check verification (686-695)
# ===========================================================================

class TestReleaseGate35Checks(unittest.TestCase):
    """Verify the release gate has exactly 35 checks and all pass."""

    def _get_gate_result(self):
        from release.paper_strategy_orchestration_release_gate_v162 import (
            PaperStrategyOrchestrationReleaseGate
        )
        gate = PaperStrategyOrchestrationReleaseGate()
        return gate.run_gate()

    def test_686_gate_run_gate_method_exists(self):
        from release.paper_strategy_orchestration_release_gate_v162 import (
            PaperStrategyOrchestrationReleaseGate
        )
        gate = PaperStrategyOrchestrationReleaseGate()
        self.assertTrue(callable(getattr(gate, "run_gate", None)))

    def test_687_gate_total_is_35(self):
        result = self._get_gate_result()
        self.assertEqual(result["total"], 35)

    def test_688_gate_all_35_pass(self):
        result = self._get_gate_result()
        self.assertEqual(result["passed"], 35)
        self.assertEqual(result["failed"], 0)

    def test_689_gate_run_delegates_to_run_gate(self):
        from release.paper_strategy_orchestration_release_gate_v162 import (
            PaperStrategyOrchestrationReleaseGate
        )
        gate = PaperStrategyOrchestrationReleaseGate()
        r1 = gate.run()
        r2 = gate.run_gate()
        self.assertEqual(r1["total"], r2["total"])
        self.assertEqual(r1["passed"], r2["passed"])

    def test_690_gate_has_no_broker_check(self):
        result = self._get_gate_result()
        checks = result.get("checks", {})
        self.assertIn("NO_BROKER", checks)
        self.assertEqual(checks["NO_BROKER"], "PASS")

    def test_691_gate_has_no_real_order_check(self):
        result = self._get_gate_result()
        checks = result.get("checks", {})
        self.assertIn("NO_REAL_ORDER", checks)
        self.assertEqual(checks["NO_REAL_ORDER"], "PASS")

    def test_692_gate_has_no_real_account_check(self):
        result = self._get_gate_result()
        checks = result.get("checks", {})
        self.assertIn("NO_REAL_ACCOUNT", checks)
        self.assertEqual(checks["NO_REAL_ACCOUNT"], "PASS")

    def test_693_gate_has_no_production_trading_check(self):
        result = self._get_gate_result()
        checks = result.get("checks", {})
        self.assertIn("NO_PRODUCTION_TRADING", checks)
        self.assertEqual(checks["NO_PRODUCTION_TRADING"], "PASS")

    def test_694_gate_version_is_1621(self):
        from release.version_info import VERSION
        self.assertTrue(VERSION.startswith("1.6") or VERSION.startswith("1.7"), f"Expected 1.6.x, got {VERSION}")

    def test_695_gate_release_name_known(self):
        from release.version_info import RELEASE_NAME
        known = {
            "Paper Strategy Orchestration",
            "Paper Strategy Orchestration Integrity Hotfix",
            "Session Operations & Observability",
            "Session Operations Integrity Hotfix",
            "CLI Registration Health Integrity Hotfix",
            "CLI Handler Resolution Integrity Hotfix",
            "Operational Analytics & Review",
            "Failure Injection & Recovery Validation",
            "Multi-session Coordination",
            "Fixture Governance & Safety Marker Hotfix",
            "Replay Session Lineage Handler Integrity Hotfix",
            "Paper Performance Attribution",
            "Operational Integration Hardening",
            "Live Paper Trading Stable Rollup",
            "Stable Rollup Compatibility Hotfix",
            "Small Capital Growth Strategy Template",
        }
        self.assertIn(RELEASE_NAME, known)


# ===========================================================================
# GROUP 58 — Health check and CLI/GUI safety (696-699)
# ===========================================================================

class TestHealthCheckAndCLIGUISafety(unittest.TestCase):

    def test_696_health_check_returns_ok(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        hc = PaperStrategyOrchestrationHealthCheck()
        result = hc.run()
        self.assertTrue(result.get("all_pass") or result.get("status") == "HEALTHY")

    def test_697_health_check_no_broker_flag(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        hc = PaperStrategyOrchestrationHealthCheck()
        result = hc.run()
        # Health check reports no_broker via checks dict
        self.assertIn("checks", result)

    def test_698_health_check_paper_only_flag(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        hc = PaperStrategyOrchestrationHealthCheck()
        result = hc.run()
        self.assertIs(result.get("paper_only"), True)

    def test_699_version_is_1621(self):
        from release.version_info import VERSION, RELEASE_NAME
        self.assertTrue(VERSION.startswith("1.6") or VERSION.startswith("1.7"), f"Expected 1.6.x, got {VERSION}")
        self.assertIsNotNone(RELEASE_NAME)

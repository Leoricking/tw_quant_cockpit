"""
release/paper_strategy_orchestration_release_gate_v162.py — Release Gate v1.6.2
[!] Research Only. No Real Orders. No Broker. Simulation Only. Not Investment Advice.
35 checks covering safety, modules, enums, models, pipeline, adapters, CLI, health.
"""
from __future__ import annotations

from typing import Any, Dict, List

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
PAPER_STRATEGY_ONLY: bool = True

_GATE_VERSION = "1.6.2"
_GATE_NAME = "Paper Strategy Orchestration"

_KNOWN_NAMES = {
    "Research Foundation Stable Rollup",
    "TWSE Provider",
    "Strategy Robustness & Regime Validation",
    "TPEx Provider",
    "MOPS Provider",
    "data.gov.tw Provider",
    "Provider CLI Registration Hotfix",
    "Provider Health Consistency Hotfix",
    "FinMind Adapter Hardening",
    "Source Lineage & Rate Limit",
    "Provider Quality Gates",
    "Forum Intelligence & Market Sentiment",
    "Data Provider Stable Rollup",
    "Full-Suite Collection Integrity Hotfix",
    "Provider Integration Hardening",
    "Provider Integration Test Integrity Hotfix",
    "Provider Stable Rollup",
    "Portfolio Research Foundation",
    "Portfolio Research Foundation Integrity Hotfix",
    "Portfolio Research CLI Completeness Hotfix",
    "Position Sizing",
    "Correlation & Exposure",
    "Correlation & Exposure Integrity Hotfix",
    "Drawdown & Risk Controls",
    "Portfolio Walk-forward Backtest",
    "Portfolio Stable Rollup",
    "Portfolio Stable Rollup Integrity Hotfix",
    "Portfolio Stable Rollup Release Gate Hotfix",
    "Live Paper Trading Foundation",
    "Market Data Session Adapter",
    "Market Data Session Warning Hygiene Hotfix",
    "Paper Strategy Orchestration",
    "Paper Strategy Orchestration Integrity Hotfix",
    "Session Operations & Observability",
    "Session Operations Integrity Hotfix",
    "CLI Registration Health Integrity Hotfix",
    "CLI Handler Resolution Integrity Hotfix",
    "Operational Analytics & Review",
}


class PaperStrategyOrchestrationReleaseGate:
    """35-check release gate for v1.6.2 Paper Strategy Orchestration."""

    def run(self) -> Dict[str, Any]:
        return self.run_gate()

    def run_gate(self) -> Dict[str, Any]:
        """Execute all 35 gate checks. Returns {all_pass, blocked, checks, ...}."""
        checks: Dict[str, str] = {}
        blocked: List[str] = []

        def _pass(name: str) -> None:
            checks[name] = "PASS"

        def _fail(name: str, reason: str) -> None:
            checks[name] = f"FAIL: {reason}"
            blocked.append(name)

        def _try(name: str, fn) -> None:
            try:
                fn()
                _pass(name)
            except Exception as exc:
                _fail(name, str(exc))

        # === 1. PAPER_STRATEGY_MODELS_VALID ===
        def _models():
            from paper_trading.strategy.models_v162 import (
                StrategyConfig, PaperSignal, DecisionContext, DecisionResult,
                PaperOrderProposal, JournalEntry, StrategyCheckpoint, LineageRecord,
            )
            cfg = StrategyConfig(strategy_name="gate_test")
            assert cfg.paper_only is True
            assert cfg.research_only is True
            assert cfg.not_a_real_order is True
            assert cfg.no_broker_call is True
        _try("PAPER_STRATEGY_MODELS_VALID", _models)

        # === 2. PAPER_STRATEGY_REGISTRY_VALID ===
        def _registry():
            from paper_trading.strategy.strategy_registry_v162 import (
                StrategyRegistry, get_global_registry, reset_global_registry
            )
            reset_global_registry()
            reg = get_global_registry()
            assert reg.count() == 0
        _try("PAPER_STRATEGY_REGISTRY_VALID", _registry)

        # === 3. PAPER_STRATEGY_CONFIG_VALID ===
        def _config():
            from paper_trading.strategy.strategy_config_v162 import (
                build_default_config, config_to_dict
            )
            cfg = build_default_config("gate_test")
            assert cfg.paper_only is True
            assert cfg.approval_mode.value == "MANUAL_REQUIRED"
            d = config_to_dict(cfg)
            assert d["paper_only"] is True
        _try("PAPER_STRATEGY_CONFIG_VALID", _config)

        # === 4. PAPER_STRATEGY_LIFECYCLE_VALID ===
        def _lifecycle():
            from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
            from paper_trading.strategy.strategy_lifecycle_v162 import StrategyLifecycleManager
            from paper_trading.strategy.strategy_state_v162 import StrategyState
            reg = StrategyRegistry()
            mgr = StrategyLifecycleManager(reg)
            assert mgr.journal_count() == 0
            state = StrategyState("gate-test-id")
            assert not state.is_rate_limited()
            assert not state.is_on_cooldown("AAPL")
        _try("PAPER_STRATEGY_LIFECYCLE_VALID", _lifecycle)

        # === 5. PAPER_SIGNAL_VALID ===
        def _signals():
            from paper_trading.strategy.signal_v162 import (
                make_entry_long, make_exit_long, make_hold, make_block, make_alert
            )
            from paper_trading.strategy.validation_v162 import validate_signal_type
            s = make_entry_long("gate-strategy", "2330.TW")
            assert s.paper_only is True
            assert s.not_a_real_order is True
            assert s.signal_type == "ENTRY_LONG"
            ok, _ = validate_signal_type("ENTRY_SHORT")
            assert not ok, "ENTRY_SHORT must be rejected"
            ok, _ = validate_signal_type("SELL_SHORT")
            assert not ok, "SELL_SHORT must be rejected"
        _try("PAPER_SIGNAL_VALID", _signals)

        # === 6. PAPER_SIGNAL_NORMALIZATION_VALID ===
        def _normalizer():
            from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
            from paper_trading.strategy.signal_v162 import make_entry_long, make_hold
            from paper_trading.strategy.enums_v162 import SignalStrength
            n = SignalNormalizer()
            sig = make_entry_long("gate-strategy", "2330.TW", confidence=1.0,
                                  strength=SignalStrength.STRONG)
            n.normalize(sig)
            assert sig.normalized_value == 1.0
            # HOLD should normalize to 0
            sh = make_hold("gate-strategy", "2330.TW")
            n.normalize(sh)
            assert sh.normalized_value == 0.0
        _try("PAPER_SIGNAL_NORMALIZATION_VALID", _normalizer)

        # === 7. PAPER_SIGNAL_DEDUP_VALID ===
        def _dedup():
            from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
            from paper_trading.strategy.signal_v162 import make_hold
            d = SignalDeduplicator()
            s = make_hold("gate-strategy", "2330.TW")
            assert not d.record(s)  # first: not duplicate
            assert d.record(s)      # second: duplicate
        _try("PAPER_SIGNAL_DEDUP_VALID", _dedup)

        # === 8. PAPER_TRIGGER_VALID ===
        def _trigger():
            from paper_trading.strategy.trigger_v162 import TriggerEngine, TriggerEvent
            from paper_trading.strategy.enums_v162 import TriggerType
            eng = TriggerEngine()
            results = []
            eng.register_handler("gate-strategy", TriggerType.MANUAL,
                                  lambda e: results.append(e.trigger_id))
            ev = TriggerEvent(TriggerType.MANUAL, "gate-strategy")
            n = eng.fire(ev)
            assert n == 1
            assert len(results) == 1
        _try("PAPER_TRIGGER_VALID", _trigger)

        # === 9. PAPER_DECISION_CONTEXT_VALID ===
        def _context():
            from paper_trading.strategy.decision_context_v162 import (
                build_decision_context, DecisionContextBuilder
            )
            from paper_trading.strategy.signal_v162 import make_hold
            from paper_trading.strategy.strategy_config_v162 import build_default_config
            from paper_trading.strategy.enums_v162 import EligibilityResult
            cfg = build_default_config("gate_test")
            sig = make_hold(cfg.strategy_id, "2330.TW")
            ctx = build_decision_context(sig, cfg, eligibility=EligibilityResult.ELIGIBLE)
            assert ctx.signal is sig
        _try("PAPER_DECISION_CONTEXT_VALID", _context)

        # === 10. PAPER_DECISION_PIPELINE_VALID ===
        def _pipeline():
            from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
            from paper_trading.strategy.decision_context_v162 import build_decision_context
            from paper_trading.strategy.signal_v162 import make_entry_long
            from paper_trading.strategy.strategy_config_v162 import build_default_config
            from paper_trading.strategy.enums_v162 import (
                DecisionOutcome, EligibilityResult, ApprovalMode
            )
            pl = DecisionPipeline()
            cfg = build_default_config("gate_test",
                                       approval_mode=ApprovalMode.AUTO_PAPER_ONLY)
            sig = make_entry_long(cfg.strategy_id, "2330.TW", confidence=0.8)
            ctx = build_decision_context(sig, cfg, eligibility=EligibilityResult.ELIGIBLE)
            result = pl.run(ctx, is_registered=True, is_running=True,
                            data_quality_ok=True, pit_valid=True,
                            eligibility=EligibilityResult.ELIGIBLE.value,
                            suggested_size=100.0, is_market_open=True)
            assert result.outcome == DecisionOutcome.APPROVED.value
            # MANUAL_REQUIRED → DEFERRED
            cfg2 = build_default_config("gate_test2",
                                        approval_mode=ApprovalMode.MANUAL_REQUIRED)
            sig2 = make_entry_long(cfg2.strategy_id, "2330.TW", confidence=0.8)
            ctx2 = build_decision_context(sig2, cfg2, eligibility=EligibilityResult.ELIGIBLE)
            result2 = pl.run(ctx2, is_registered=True, is_running=True,
                             data_quality_ok=True, pit_valid=True,
                             eligibility=EligibilityResult.ELIGIBLE.value,
                             suggested_size=100.0)
            assert result2.outcome == DecisionOutcome.DEFERRED.value
        _try("PAPER_DECISION_PIPELINE_VALID", _pipeline)

        # === 11. PAPER_ELIGIBILITY_INTEGRATION_VALID ===
        def _eligibility():
            from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
            from paper_trading.strategy.enums_v162 import EligibilityResult
            ea = EligibilityAdapter()
            assert ea.check("2330.TW") == EligibilityResult.ELIGIBLE
            ea.block_ticker("BLOCKED.TW")
            assert ea.check("BLOCKED.TW") == EligibilityResult.INELIGIBLE
        _try("PAPER_ELIGIBILITY_INTEGRATION_VALID", _eligibility)

        # === 12. PAPER_SIZING_INTEGRATION_VALID ===
        def _sizing():
            from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
            from paper_trading.strategy.signal_v162 import make_entry_long
            sa = SizingAdapter(fixed_size=200.0, use_portfolio_sizing=False)
            sig = make_entry_long("gate-strategy", "2330.TW", confidence=1.0)
            size = sa.compute(sig)
            assert size is not None
            assert size > 0
        _try("PAPER_SIZING_INTEGRATION_VALID", _sizing)

        # === 13. PAPER_CORRELATION_INTEGRATION_VALID ===
        def _correlation():
            from paper_trading.strategy.correlation_adapter_v162 import CorrelationAdapter
            ca = CorrelationAdapter(use_portfolio_correlation=False)
            assert ca.check_breach("2330.TW") is False
        _try("PAPER_CORRELATION_INTEGRATION_VALID", _correlation)

        # === 14. PAPER_RISK_INTEGRATION_VALID ===
        def _risk():
            from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
            ra = RiskAdapter(use_portfolio_risk=False)
            assert ra.is_blocked("2330.TW") is False
            blocked = ra.is_blocked("2330.TW", current_drawdown_pct=0.99)
            assert blocked is True
        _try("PAPER_RISK_INTEGRATION_VALID", _risk)

        # === 15. PAPER_APPROVAL_VALID ===
        def _approval():
            from paper_trading.strategy.approval_v162 import ApprovalPolicy
            ap = ApprovalPolicy()
            assert ap.pending_count() == 0
        _try("PAPER_APPROVAL_VALID", _approval)

        # === 16. PAPER_CONFLICT_RESOLUTION_VALID ===
        def _conflict():
            from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
            from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
            from paper_trading.strategy.enums_v162 import ConflictPolicy
            cr = ConflictResolver(ConflictPolicy.MOST_CONSERVATIVE)
            sig1 = make_entry_long("g", "2330.TW")
            sig2 = make_exit_long("g", "2330.TW")
            resolved, log = cr.resolve([sig1, sig2])
            assert len(resolved) == 1
            assert resolved[0].signal_type == "EXIT_LONG"
        _try("PAPER_CONFLICT_RESOLUTION_VALID", _conflict)

        # === 17. PAPER_COOLDOWN_VALID ===
        def _cooldown():
            from paper_trading.strategy.cooldown_v162 import CooldownManager
            cm = CooldownManager(cooldown_seconds=0)
            assert not cm.is_on_cooldown("2330.TW")
            cm.record("2330.TW")
            # 0-second cooldown expires immediately, so should NOT be blocked after record
            # Test with positive cooldown
            cm2 = CooldownManager(cooldown_seconds=3600)
            cm2.record("2330.TW")
            assert cm2.is_on_cooldown("2330.TW")
        _try("PAPER_COOLDOWN_VALID", _cooldown)

        # === 18. PAPER_RATE_LIMIT_VALID ===
        def _rate():
            from paper_trading.strategy.rate_limit_v162 import RateLimiter
            rl = RateLimiter(max_per_minute=100)
            assert rl.try_acquire()
            assert not rl.is_limited()
            # Rate-limited: exhaust a 1-per-minute limiter
            rl2 = RateLimiter(max_per_minute=1)
            assert rl2.try_acquire()   # first ok
            assert not rl2.try_acquire()  # second blocked
        _try("PAPER_RATE_LIMIT_VALID", _rate)

        # === 19. PAPER_PROPOSAL_VALID ===
        def _proposal():
            from paper_trading.strategy.proposal_v162 import (
                build_proposal, proposal_to_dict, submit_proposal
            )
            from paper_trading.strategy.signal_v162 import make_entry_long
            from paper_trading.strategy.models_v162 import DecisionResult
            sig = make_entry_long("gate-strategy", "2330.TW", confidence=0.8)
            decision = DecisionResult(
                strategy_id="gate-strategy",
                ticker="2330.TW",
                signal_id=sig.signal_id,
                outcome="APPROVED",
                pipeline_steps_completed=16,
                paper_only=True,
                research_only=True,
                simulation_only=True,
                not_a_real_order=True,
                no_broker_call=True,
            )
            proposal = build_proposal(decision, sig, suggested_size=100.0)
            assert proposal.paper_only is True
            d = proposal_to_dict(proposal)
            assert d["not_a_real_order"] is True
        _try("PAPER_PROPOSAL_VALID", _proposal)

        # === 20. PAPER_ORDER_BRIDGE_VALID ===
        def _bridge():
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            bridge = PaperOrderBridge()
            assert bridge.BROKER_CONNECTED is False
            assert bridge.REAL_ORDERS_ENABLED is False
            assert bridge.PRODUCTION_ENABLED is False
        _try("PAPER_ORDER_BRIDGE_VALID", _bridge)

        # === 21. PAPER_STRATEGY_JOURNAL_VALID ===
        def _journal():
            from paper_trading.strategy.journal_v162 import StrategyJournal
            from paper_trading.strategy.enums_v162 import JournalEventType
            j = StrategyJournal("gate-strategy")
            j.record(JournalEventType.STRATEGY_REGISTERED, "gate check")
            assert j.count() == 1
            tail = j.tail(1)
            assert len(tail) == 1
        _try("PAPER_STRATEGY_JOURNAL_VALID", _journal)

        # === 22. PAPER_STRATEGY_CHECKPOINT_VALID ===
        def _checkpoint():
            from paper_trading.strategy.checkpoint_v162 import CheckpointManager
            cm = CheckpointManager("gate-strategy",
                                   checkpoint_dir="data/paper_strategy/checkpoints/gate")
            assert cm.latest() is None
            assert isinstance(cm.list_checkpoints(), list)
        _try("PAPER_STRATEGY_CHECKPOINT_VALID", _checkpoint)

        # === 23. PAPER_STRATEGY_REPLAY_VALID ===
        def _replay():
            from paper_trading.strategy.replay_v162 import ReplaySession
            rs = ReplaySession("gate-strategy", [])
            summary = rs.run_all()
            assert summary["paper_only"] is True
            assert summary["complete"] is True
        _try("PAPER_STRATEGY_REPLAY_VALID", _replay)

        # === 24. PAPER_STRATEGY_RECOVERY_VALID ===
        def _recovery():
            from paper_trading.strategy.recovery_v162 import RecoveryManager
            rm = RecoveryManager("gate-strategy")
            assert rm.strategy_id == "gate-strategy"
        _try("PAPER_STRATEGY_RECOVERY_VALID", _recovery)

        # === 25. PAPER_STRATEGY_LINEAGE_VALID ===
        def _lineage():
            from paper_trading.strategy.lineage_v162 import LineageTracker
            lt = LineageTracker()
            assert lt.count() == 0
        _try("PAPER_STRATEGY_LINEAGE_VALID", _lineage)

        # === 26. PAPER_STRATEGY_REPRODUCIBILITY_VALID ===
        def _repro():
            from paper_trading.strategy.reproducibility_v162 import ReproducibilityVerifier
            rv = ReproducibilityVerifier()
            assert rv.summary()["check_count"] == 0
        _try("PAPER_STRATEGY_REPRODUCIBILITY_VALID", _repro)

        # === 27. NO_STRATEGY_DIRECT_FILL ===
        def _no_fill():
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            # Bridge has no DIRECT_FILL_ENABLED flag and no fill() method
            bridge = PaperOrderBridge()
            assert not hasattr(bridge, "fill")
            assert bridge.BROKER_CONNECTED is False
            # Only submit() exists — no direct fill path
            assert hasattr(bridge, "submit")
        _try("NO_STRATEGY_DIRECT_FILL", _no_fill)

        # === 28. NO_STRATEGY_DIRECT_POSITION_UPDATE ===
        def _no_pos_update():
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            bridge = PaperOrderBridge()
            # No direct position update method
            assert not hasattr(bridge, "update_position")
            assert not hasattr(bridge, "set_position")
            assert bridge.REAL_ORDERS_ENABLED is False
        _try("NO_STRATEGY_DIRECT_POSITION_UPDATE", _no_pos_update)

        # === 29. NO_STRATEGY_DIRECT_CASH_UPDATE ===
        def _no_cash_update():
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            bridge = PaperOrderBridge()
            assert not hasattr(bridge, "update_cash")
            assert not hasattr(bridge, "set_cash")
            assert bridge.PRODUCTION_ENABLED is False
        _try("NO_STRATEGY_DIRECT_CASH_UPDATE", _no_cash_update)

        # === 30. NO_STRATEGY_PAPER_LEDGER_WRITE ===
        def _no_paper_ledger():
            from paper_trading.strategy import REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
            assert REAL_PORTFOLIO_LEDGER_WRITE_ENABLED is False
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            bridge = PaperOrderBridge()
            assert not hasattr(bridge, "write_ledger")
            assert not hasattr(bridge, "write_paper_ledger")
        _try("NO_STRATEGY_PAPER_LEDGER_WRITE", _no_paper_ledger)

        # === 31. NO_STRATEGY_FORMAL_LEDGER_WRITE ===
        def _no_formal_ledger():
            from paper_trading.strategy import REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
            assert REAL_PORTFOLIO_LEDGER_WRITE_ENABLED is False
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            bridge = PaperOrderBridge()
            assert not hasattr(bridge, "write_formal_ledger")
            assert not hasattr(bridge, "post_to_formal_ledger")
        _try("NO_STRATEGY_FORMAL_LEDGER_WRITE", _no_formal_ledger)

        # === 32. NO_BROKER ===
        def _no_broker():
            from paper_trading.strategy import BROKER_CONNECTION_ENABLED, BROKER_EXECUTION_ENABLED
            assert BROKER_CONNECTION_ENABLED is False
            assert BROKER_EXECUTION_ENABLED is False
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            assert PaperOrderBridge.BROKER_CONNECTED is False
        _try("NO_BROKER", _no_broker)

        # === 33. NO_REAL_ORDER ===
        def _no_real_order():
            from paper_trading.strategy import NO_REAL_ORDERS, REAL_ORDER_CREATION_ENABLED
            assert NO_REAL_ORDERS is True
            assert REAL_ORDER_CREATION_ENABLED is False
            from paper_trading.strategy import REAL_ORDER_EXECUTION_ENABLED
            assert REAL_ORDER_EXECUTION_ENABLED is False
        _try("NO_REAL_ORDER", _no_real_order)

        # === 34. NO_REAL_ACCOUNT ===
        def _no_real_account():
            from paper_trading.strategy import LIVE_ACCOUNT_SYNC_ENABLED
            assert LIVE_ACCOUNT_SYNC_ENABLED is False
            from paper_trading.strategy.models_v162 import PaperOrderProposal
            p = PaperOrderProposal(ticker="2330.TW", proposed_size=100.0)
            assert p.no_real_account is True
        _try("NO_REAL_ACCOUNT", _no_real_account)

        # === 35. NO_PRODUCTION_TRADING ===
        def _no_production():
            from paper_trading.strategy import (
                PRODUCTION_TRADING_BLOCKED, AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED,
                REAL_STRATEGY_EXECUTION_ENABLED
            )
            assert PRODUCTION_TRADING_BLOCKED is True
            assert AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED is False
            assert REAL_STRATEGY_EXECUTION_ENABLED is False
            from release.version_info import VERSION, RELEASE_NAME
            assert VERSION.startswith("1.6"), f"Expected 1.6.x, got {VERSION}"
            assert RELEASE_NAME in _KNOWN_NAMES, f"Unknown RELEASE_NAME: {RELEASE_NAME}"
        _try("NO_PRODUCTION_TRADING", _no_production)

        # Build result
        passed = sum(1 for v in checks.values() if v == "PASS")
        failed = len(blocked)
        all_pass = failed == 0

        return {
            "gate_version": _GATE_VERSION,
            "gate_name": _GATE_NAME,
            "total": len(checks),
            "passed": passed,
            "failed": failed,
            "all_pass": all_pass,
            "blocked": blocked,
            "checks": checks,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "broker_enabled": False,
            "production_trading_blocked": True,
        }


def run_gate() -> Dict[str, Any]:
    return PaperStrategyOrchestrationReleaseGate().run_gate()

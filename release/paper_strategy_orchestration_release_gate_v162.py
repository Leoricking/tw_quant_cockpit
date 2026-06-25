"""
release/paper_strategy_orchestration_release_gate_v162.py — Release Gate v1.6.2
[!] Research Only. No Real Orders. No Broker. Simulation Only. Not Investment Advice.
34 checks covering safety, modules, enums, models, pipeline, adapters, CLI, health.
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
}


class PaperStrategyOrchestrationReleaseGate:
    """34-check release gate for v1.6.2 Paper Strategy Orchestration."""

    def run(self) -> Dict[str, Any]:
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

        # === 1-6: Safety invariants ===
        def _safety():
            from paper_trading.strategy import (
                PAPER_STRATEGY_RESEARCH_ONLY,
                REAL_ORDER_CREATION_ENABLED,
                REAL_ORDER_EXECUTION_ENABLED,
                BROKER_EXECUTION_ENABLED as BEE,
                PRODUCTION_TRADING_BLOCKED as PTB,
                NO_REAL_ORDERS as NRO,
                SHORT_SELLING_ENABLED,
                MARGIN_ENABLED,
                REAL_STRATEGY_EXECUTION_ENABLED,
                AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED,
            )
            assert PAPER_STRATEGY_RESEARCH_ONLY is True
            assert REAL_ORDER_CREATION_ENABLED is False
            assert REAL_ORDER_EXECUTION_ENABLED is False
            assert BEE is False
            assert PTB is True
            assert NRO is True
            assert SHORT_SELLING_ENABLED is False
            assert MARGIN_ENABLED is False
            assert REAL_STRATEGY_EXECUTION_ENABLED is False
            assert AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED is False

        _try("safety_research_only", lambda: __import__("paper_trading.strategy", fromlist=["PAPER_STRATEGY_RESEARCH_ONLY"]))
        _try("safety_no_real_orders", _safety)
        _try("safety_broker_disabled", _safety)
        _try("safety_production_blocked", _safety)
        _try("safety_no_short_selling", _safety)
        _try("safety_no_autonomous_production", _safety)

        # === 7: Version info ===
        def _version():
            from release.version_info import (
                VERSION, RELEASE_NAME, PAPER_STRATEGY_ORCHESTRATION_BASELINE
            )
            assert VERSION == "1.6.2", f"Expected 1.6.2, got {VERSION}"
            assert RELEASE_NAME in _KNOWN_NAMES, f"Unknown RELEASE_NAME: {RELEASE_NAME}"
            assert PAPER_STRATEGY_ORCHESTRATION_BASELINE == "1.6.2"
        _try("version_info", _version)

        # === 8: Enums ===
        def _enums():
            from paper_trading.strategy.enums_v162 import (
                StrategyStatus, SignalType, DecisionOutcome, ApprovalMode,
                ConflictPolicy, ProposalStatus, JournalEventType, CheckpointReason,
                RecoveryMode, EligibilityResult, SignalStrength, TriggerType,
            )
            types = [st.value for st in SignalType]
            assert "ENTRY_SHORT" not in types
            assert "SELL_SHORT" not in types
            assert "ENTRY_LONG" in types
            assert ApprovalMode.MANUAL_REQUIRED.value == "MANUAL_REQUIRED"
            assert ConflictPolicy.MOST_CONSERVATIVE.value == "MOST_CONSERVATIVE"
        _try("enums", _enums)

        # === 9: Models ===
        def _models():
            from paper_trading.strategy.models_v162 import (
                StrategyConfig, PaperSignal, DecisionContext, DecisionResult,
                PaperOrderProposal, JournalEntry, StrategyCheckpoint, LineageRecord,
            )
            cfg = StrategyConfig(strategy_name="gate_test")
            assert cfg.paper_only is True
            assert cfg.no_broker_call is True
        _try("models", _models)

        # === 10: Validation ===
        def _validation():
            from paper_trading.strategy.validation_v162 import (
                validate_signal_type, validate_confidence, validate_ticker
            )
            ok, _ = validate_signal_type("ENTRY_LONG")
            assert ok
            ok, _ = validate_signal_type("ENTRY_SHORT")
            assert not ok, "ENTRY_SHORT must be rejected"
        _try("validation", _validation)

        # === 11: Strategy base ===
        def _base():
            from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
            assert PaperStrategyBase.PAPER_ONLY is True
            assert PaperStrategyBase.RESEARCH_ONLY is True
            assert PaperStrategyBase.NO_BROKER_CALL is True
        _try("strategy_base", _base)

        # === 12: Registry ===
        def _registry():
            from paper_trading.strategy.strategy_registry_v162 import (
                StrategyRegistry, get_global_registry, reset_global_registry
            )
            reset_global_registry()
            reg = get_global_registry()
            assert reg.count() == 0
        _try("registry", _registry)

        # === 13: Config builder ===
        def _config():
            from paper_trading.strategy.strategy_config_v162 import (
                build_default_config, config_to_dict
            )
            cfg = build_default_config("gate_test")
            assert cfg.paper_only is True
            d = config_to_dict(cfg)
            assert d["paper_only"] is True
        _try("config_builder", _config)

        # === 14: Strategy state ===
        def _state():
            from paper_trading.strategy.strategy_state_v162 import StrategyState
            s = StrategyState("gate-test-id")
            assert not s.is_rate_limited()
            assert not s.is_on_cooldown("AAPL")
        _try("strategy_state", _state)

        # === 15: Lifecycle manager ===
        def _lifecycle():
            from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
            from paper_trading.strategy.strategy_lifecycle_v162 import StrategyLifecycleManager
            reg = StrategyRegistry()
            mgr = StrategyLifecycleManager(reg)
            assert mgr.journal_count() == 0
        _try("lifecycle_manager", _lifecycle)

        # === 16: Signal helpers ===
        def _signals():
            from paper_trading.strategy.signal_v162 import (
                make_entry_long, make_exit_long, make_hold, make_block, make_alert
            )
            s = make_entry_long("gate-strategy", "2330.TW")
            assert s.paper_only is True
            assert s.not_a_real_order is True
            assert s.signal_type == "ENTRY_LONG"
        _try("signal_helpers", _signals)

        # === 17: Signal normalizer ===
        def _normalizer():
            from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
            from paper_trading.strategy.signal_v162 import make_entry_long
            from paper_trading.strategy.enums_v162 import SignalStrength
            n = SignalNormalizer()
            sig = make_entry_long("gate-strategy", "2330.TW", confidence=1.0,
                                  strength=SignalStrength.STRONG)
            n.normalize(sig)
            assert sig.normalized_value == 1.0
        _try("signal_normalizer", _normalizer)

        # === 18: Signal deduplicator ===
        def _dedup():
            from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
            from paper_trading.strategy.signal_v162 import make_hold
            d = SignalDeduplicator()
            s = make_hold("gate-strategy", "2330.TW")
            assert not d.record(s)  # first time: not duplicate
            assert d.record(s)      # second time: duplicate
        _try("signal_dedup", _dedup)

        # === 19: Trigger engine ===
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
        _try("trigger_engine", _trigger)

        # === 20: Decision context ===
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
        _try("decision_context", _context)

        # === 21: Decision pipeline — all steps ===
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

            # Manual required → DEFERRED
            cfg2 = build_default_config("gate_test2",
                                        approval_mode=ApprovalMode.MANUAL_REQUIRED)
            sig2 = make_entry_long(cfg2.strategy_id, "2330.TW", confidence=0.8)
            ctx2 = build_decision_context(sig2, cfg2, eligibility=EligibilityResult.ELIGIBLE)
            result2 = pl.run(ctx2, is_registered=True, is_running=True,
                             data_quality_ok=True, pit_valid=True,
                             eligibility=EligibilityResult.ELIGIBLE.value,
                             suggested_size=100.0)
            assert result2.outcome == DecisionOutcome.DEFERRED.value
        _try("decision_pipeline", _pipeline)

        # === 22: Eligibility adapter ===
        def _eligibility():
            from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
            from paper_trading.strategy.enums_v162 import EligibilityResult
            ea = EligibilityAdapter()
            assert ea.check("2330.TW") == EligibilityResult.ELIGIBLE
            ea.block_ticker("BLOCKED.TW")
            assert ea.check("BLOCKED.TW") == EligibilityResult.INELIGIBLE
        _try("eligibility_adapter", _eligibility)

        # === 23: Sizing adapter ===
        def _sizing():
            from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
            from paper_trading.strategy.signal_v162 import make_entry_long
            sa = SizingAdapter(fixed_size=200.0, use_portfolio_sizing=False)
            sig = make_entry_long("gate-strategy", "2330.TW", confidence=1.0)
            size = sa.compute(sig)
            assert size is not None
            assert size > 0
        _try("sizing_adapter", _sizing)

        # === 24: Correlation adapter ===
        def _correlation():
            from paper_trading.strategy.correlation_adapter_v162 import CorrelationAdapter
            ca = CorrelationAdapter(use_portfolio_correlation=False)
            assert ca.check_breach("2330.TW") is False
        _try("correlation_adapter", _correlation)

        # === 25: Risk adapter ===
        def _risk():
            from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
            ra = RiskAdapter(use_portfolio_risk=False)
            assert ra.is_blocked("2330.TW") is False
            # Test local drawdown gate
            blocked = ra.is_blocked("2330.TW", current_drawdown_pct=0.99)
            assert blocked is True
        _try("risk_adapter", _risk)

        # === 26: Approval policy ===
        def _approval():
            from paper_trading.strategy.approval_v162 import ApprovalPolicy
            ap = ApprovalPolicy()
            assert ap.pending_count() == 0
        _try("approval_policy", _approval)

        # === 27: Conflict resolver ===
        def _conflict():
            from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
            from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
            from paper_trading.strategy.enums_v162 import ConflictPolicy
            cr = ConflictResolver(ConflictPolicy.MOST_CONSERVATIVE)
            sig1 = make_entry_long("g", "2330.TW")
            sig2 = make_exit_long("g", "2330.TW")
            resolved, log = cr.resolve([sig1, sig2])
            assert len(resolved) == 1
            assert resolved[0].signal_type == "EXIT_LONG"  # EXIT wins conservatively
        _try("conflict_resolver", _conflict)

        # === 28: Cooldown + rate limiter ===
        def _cooldown_rate():
            from paper_trading.strategy.cooldown_v162 import CooldownManager
            from paper_trading.strategy.rate_limit_v162 import RateLimiter
            cm = CooldownManager(cooldown_seconds=0)  # 0s for gate test
            cm.record("2330.TW")
            rl = RateLimiter(max_per_minute=100)
            assert rl.try_acquire()
        _try("cooldown_rate_limiter", _cooldown_rate)

        # === 29: Proposal builder ===
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
        _try("proposal_builder", _proposal)

        # === 30: Order bridge ===
        def _bridge():
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            bridge = PaperOrderBridge()
            assert bridge.BROKER_CONNECTED is False
            assert bridge.REAL_ORDERS_ENABLED is False
            assert bridge.PRODUCTION_ENABLED is False
        _try("order_bridge", _bridge)

        # === 31: Journal, checkpoint, replay, recovery, lineage ===
        def _persistence():
            from paper_trading.strategy.journal_v162 import StrategyJournal
            from paper_trading.strategy.enums_v162 import JournalEventType
            from paper_trading.strategy.replay_v162 import ReplaySession
            j = StrategyJournal("gate-strategy")
            j.record(JournalEventType.STRATEGY_REGISTERED, "gate check")
            assert j.count() == 1
            rs = ReplaySession("gate-strategy", [])
            summary = rs.run_all()
            assert summary["paper_only"] is True
        _try("persistence_components", _persistence)

        # === 32: Store + query service ===
        def _store():
            from paper_trading.strategy.store_v162 import PaperStrategyStore
            from paper_trading.strategy.query_v162 import PaperStrategyQueryService
            store = PaperStrategyStore()
            qs = PaperStrategyQueryService(store)
            summary = qs.full_summary()
            assert summary["paper_only"] is True
        _try("store_query_service", _store)

        # === 33: Health check runs and passes ===
        def _health():
            from paper_trading.strategy.health_v162 import (
                PaperStrategyOrchestrationHealthCheck
            )
            result = PaperStrategyOrchestrationHealthCheck().run()
            if result["failed"] > 0:
                failed_names = [
                    c["name"] for c in result["checks"] if not c["ok"]
                ]
                raise AssertionError(f"Health check failed: {failed_names}")
        _try("health_check", _health)

        # === 34: GUI panel importable ===
        def _gui():
            import gui.paper_strategy_orchestration_panel as panel
            assert hasattr(panel, "PaperStrategyOrchestrationPanel")
        _try("gui_panel", _gui)

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
    return PaperStrategyOrchestrationReleaseGate().run()

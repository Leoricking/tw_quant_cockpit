"""
paper_trading/strategy/health_v162.py — Health check for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _check(name: str, fn) -> Tuple[str, bool, str]:
    try:
        result = fn()
        ok = bool(result)
        detail = "" if ok else "returned falsy"
    except Exception as exc:
        ok = False
        detail = str(exc)
    return name, ok, detail


class PaperStrategyOrchestrationHealthCheck:
    """
    Health check for the Paper Strategy Orchestration module (v1.6.2).

    Verifies:
      - Module importability
      - Safety flags
      - Core component instantiation
      - Enum availability
      - Registry, lifecycle, pipeline, store components
    """

    def run(self) -> Dict[str, Any]:
        checks: List[Tuple[str, bool, str]] = []

        # 1. __init__ imports and safety flags
        def _check_init():
            from paper_trading.strategy import (
                PAPER_STRATEGY_RESEARCH_ONLY,
                REAL_ORDER_CREATION_ENABLED,
                BROKER_EXECUTION_ENABLED,
                PRODUCTION_TRADING_BLOCKED,
                NO_REAL_ORDERS,
                SHORT_SELLING_ENABLED,
                MARGIN_ENABLED,
            )
            assert PAPER_STRATEGY_RESEARCH_ONLY is True
            assert REAL_ORDER_CREATION_ENABLED is False
            assert BROKER_EXECUTION_ENABLED is False
            assert PRODUCTION_TRADING_BLOCKED is True
            assert NO_REAL_ORDERS is True
            assert SHORT_SELLING_ENABLED is False
            assert MARGIN_ENABLED is False
            return True
        checks.append(_check("init_safety_flags", _check_init))

        # 2. Enums importable
        def _check_enums():
            from paper_trading.strategy.enums_v162 import (
                StrategyStatus, SignalType, DecisionOutcome,
                ApprovalMode, ConflictPolicy, ProposalStatus,
            )
            assert SignalType.ENTRY_LONG
            assert DecisionOutcome.APPROVED
            assert ApprovalMode.MANUAL_REQUIRED
            # Verify forbidden types absent
            types = [st.value for st in SignalType]
            assert "ENTRY_SHORT" not in types
            assert "SELL_SHORT" not in types
            return True
        checks.append(_check("enums_importable", _check_enums))

        # 3. Models importable
        def _check_models():
            from paper_trading.strategy.models_v162 import (
                StrategyConfig, PaperSignal, DecisionContext,
                DecisionResult, PaperOrderProposal, JournalEntry,
                StrategyCheckpoint, LineageRecord,
            )
            cfg = StrategyConfig(strategy_name="health_test")
            assert cfg.paper_only is True
            assert cfg.research_only is True
            assert cfg.not_a_real_order is True
            return True
        checks.append(_check("models_importable", _check_models))

        # 4. Validation importable
        def _check_validation():
            from paper_trading.strategy.validation_v162 import (
                validate_signal_type, validate_confidence,
                validate_ticker, validate_paper_signal_dict,
            )
            ok, _ = validate_signal_type("ENTRY_LONG")
            assert ok
            ok, _ = validate_signal_type("ENTRY_SHORT")
            assert not ok
            ok, _ = validate_confidence(0.7)
            assert ok
            return True
        checks.append(_check("validation_importable", _check_validation))

        # 5. Strategy base importable
        def _check_base():
            from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
            assert PaperStrategyBase.PAPER_ONLY is True
            assert PaperStrategyBase.RESEARCH_ONLY is True
            return True
        checks.append(_check("strategy_base_importable", _check_base))

        # 6. Registry importable
        def _check_registry():
            from paper_trading.strategy.strategy_registry_v162 import (
                StrategyRegistry, get_global_registry, reset_global_registry
            )
            reset_global_registry()
            reg = get_global_registry()
            assert reg.count() == 0
            return True
        checks.append(_check("registry_importable", _check_registry))

        # 7. Config builder importable
        def _check_config():
            from paper_trading.strategy.strategy_config_v162 import build_default_config
            cfg = build_default_config(strategy_name="health_config")
            assert cfg.paper_only is True
            assert cfg.approval_mode.value == "MANUAL_REQUIRED"
            return True
        checks.append(_check("config_builder", _check_config))

        # 8. Strategy state importable
        def _check_state():
            from paper_trading.strategy.strategy_state_v162 import StrategyState
            state = StrategyState("health-state-id")
            assert not state.is_rate_limited()
            assert not state.is_on_cooldown("TEST")
            return True
        checks.append(_check("strategy_state", _check_state))

        # 9. Lifecycle manager importable
        def _check_lifecycle():
            from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
            from paper_trading.strategy.strategy_lifecycle_v162 import StrategyLifecycleManager
            reg = StrategyRegistry()
            mgr = StrategyLifecycleManager(reg)
            assert mgr.journal_count() == 0
            return True
        checks.append(_check("lifecycle_manager", _check_lifecycle))

        # 10. Signal helpers importable
        def _check_signal():
            from paper_trading.strategy.signal_v162 import make_entry_long, make_hold
            sig = make_hold("health-strategy", "2330.TW")
            assert sig.paper_only is True
            assert sig.not_a_real_order is True
            return True
        checks.append(_check("signal_helpers", _check_signal))

        # 11. Signal normalizer importable
        def _check_normalizer():
            from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
            from paper_trading.strategy.signal_v162 import make_entry_long
            from paper_trading.strategy.enums_v162 import SignalStrength
            n = SignalNormalizer()
            sig = make_entry_long("health-strategy", "2330.TW", confidence=0.8,
                                  strength=SignalStrength.STRONG)
            n.normalize(sig)
            assert sig.normalized_value is not None
            return True
        checks.append(_check("signal_normalizer", _check_normalizer))

        # 12. Signal deduplicator importable
        def _check_dedup():
            from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
            from paper_trading.strategy.signal_v162 import make_hold
            d = SignalDeduplicator()
            sig = make_hold("health-strategy", "2330.TW")
            is_dup = d.record(sig)
            assert not is_dup
            return True
        checks.append(_check("signal_dedup", _check_dedup))

        # 13. Trigger engine importable
        def _check_trigger():
            from paper_trading.strategy.trigger_v162 import TriggerEngine
            eng = TriggerEngine()
            assert eng.handler_count() == 0
            return True
        checks.append(_check("trigger_engine", _check_trigger))

        # 14. Decision context builder importable
        def _check_context():
            from paper_trading.strategy.decision_context_v162 import build_decision_context
            from paper_trading.strategy.signal_v162 import make_hold
            from paper_trading.strategy.strategy_config_v162 import build_default_config
            from paper_trading.strategy.enums_v162 import EligibilityResult
            cfg = build_default_config("health_test")
            sig = make_hold(cfg.strategy_id, "2330.TW")
            ctx = build_decision_context(sig, cfg,
                                         eligibility=EligibilityResult.ELIGIBLE)
            assert ctx.signal is sig
            return True
        checks.append(_check("decision_context", _check_context))

        # 15. Decision pipeline importable
        def _check_pipeline():
            from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
            pl = DecisionPipeline()
            assert pl is not None
            return True
        checks.append(_check("decision_pipeline", _check_pipeline))

        # 16. Eligibility adapter importable
        def _check_eligibility():
            from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
            from paper_trading.strategy.enums_v162 import EligibilityResult
            ea = EligibilityAdapter()
            result = ea.check("2330.TW")
            assert result == EligibilityResult.ELIGIBLE
            return True
        checks.append(_check("eligibility_adapter", _check_eligibility))

        # 17. Sizing adapter importable
        def _check_sizing():
            from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
            sa = SizingAdapter(use_portfolio_sizing=False)
            assert sa.fixed_size > 0
            return True
        checks.append(_check("sizing_adapter", _check_sizing))

        # 18. Correlation adapter importable
        def _check_corr():
            from paper_trading.strategy.correlation_adapter_v162 import CorrelationAdapter
            ca = CorrelationAdapter(use_portfolio_correlation=False)
            breach = ca.check_breach("2330.TW")
            assert breach is False
            return True
        checks.append(_check("correlation_adapter", _check_corr))

        # 19. Risk adapter importable
        def _check_risk():
            from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
            ra = RiskAdapter(use_portfolio_risk=False)
            blocked = ra.is_blocked("2330.TW")
            assert blocked is False
            return True
        checks.append(_check("risk_adapter", _check_risk))

        # 20. Approval policy importable
        def _check_approval():
            from paper_trading.strategy.approval_v162 import ApprovalPolicy
            ap = ApprovalPolicy()
            assert ap.pending_count() == 0
            return True
        checks.append(_check("approval_policy", _check_approval))

        # 21. Conflict resolver importable
        def _check_conflict():
            from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
            from paper_trading.strategy.enums_v162 import ConflictPolicy
            cr = ConflictResolver(ConflictPolicy.MOST_CONSERVATIVE)
            assert cr.policy == ConflictPolicy.MOST_CONSERVATIVE
            return True
        checks.append(_check("conflict_resolver", _check_conflict))

        # 22. Cooldown manager importable
        def _check_cooldown():
            from paper_trading.strategy.cooldown_v162 import CooldownManager
            cm = CooldownManager(cooldown_seconds=30)
            assert not cm.is_on_cooldown("TEST")
            return True
        checks.append(_check("cooldown_manager", _check_cooldown))

        # 23. Rate limiter importable
        def _check_rate():
            from paper_trading.strategy.rate_limit_v162 import RateLimiter
            rl = RateLimiter(max_per_minute=10)
            assert not rl.is_limited()
            assert rl.try_acquire()
            return True
        checks.append(_check("rate_limiter", _check_rate))

        # 24. Proposal builder importable
        def _check_proposal():
            from paper_trading.strategy.proposal_v162 import proposal_to_dict
            from paper_trading.strategy.models_v162 import PaperOrderProposal
            p = PaperOrderProposal(ticker="2330.TW", proposed_size=100.0)
            d = proposal_to_dict(p)
            assert d["paper_only"] is True
            assert d["not_a_real_order"] is True
            return True
        checks.append(_check("proposal_builder", _check_proposal))

        # 25. Order bridge importable
        def _check_bridge():
            from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
            bridge = PaperOrderBridge()
            assert bridge.BROKER_CONNECTED is False
            assert bridge.REAL_ORDERS_ENABLED is False
            return True
        checks.append(_check("order_bridge", _check_bridge))

        # 26. Journal importable
        def _check_journal():
            from paper_trading.strategy.journal_v162 import StrategyJournal
            from paper_trading.strategy.enums_v162 import JournalEventType
            j = StrategyJournal("health-strategy")
            j.record(JournalEventType.STRATEGY_REGISTERED, "health check")
            assert j.count() == 1
            return True
        checks.append(_check("strategy_journal", _check_journal))

        # 27. Checkpoint manager importable
        def _check_checkpoint():
            from paper_trading.strategy.checkpoint_v162 import CheckpointManager
            cm = CheckpointManager("health-strategy", checkpoint_dir="data/paper_strategy/checkpoints/health")
            assert cm.latest() is None
            return True
        checks.append(_check("checkpoint_manager", _check_checkpoint))

        # 28. Replay importable
        def _check_replay():
            from paper_trading.strategy.replay_v162 import ReplaySession
            rs = ReplaySession("health-strategy", [])
            summary = rs.run_all()
            assert summary["complete"] is True
            assert summary["paper_only"] is True
            return True
        checks.append(_check("replay_session", _check_replay))

        # 29. Recovery manager importable
        def _check_recovery():
            from paper_trading.strategy.recovery_v162 import RecoveryManager
            rm = RecoveryManager("health-strategy")
            assert rm.strategy_id == "health-strategy"
            return True
        checks.append(_check("recovery_manager", _check_recovery))

        # 30. Lineage tracker importable
        def _check_lineage():
            from paper_trading.strategy.lineage_v162 import LineageTracker
            lt = LineageTracker()
            assert lt.count() == 0
            return True
        checks.append(_check("lineage_tracker", _check_lineage))

        # 31. Reproducibility verifier importable
        def _check_repro():
            from paper_trading.strategy.reproducibility_v162 import ReproducibilityVerifier
            rv = ReproducibilityVerifier()
            assert rv.summary()["check_count"] == 0
            return True
        checks.append(_check("reproducibility_verifier", _check_repro))

        # 32. Explainer importable
        def _check_explain():
            from paper_trading.strategy.explain_v162 import DecisionExplainer
            de = DecisionExplainer()
            assert de is not None
            return True
        checks.append(_check("decision_explainer", _check_explain))

        # 33. Store importable
        def _check_store():
            from paper_trading.strategy.store_v162 import PaperStrategyStore
            store = PaperStrategyStore()
            assert store.signal_count() == 0
            assert store.decision_count() == 0
            return True
        checks.append(_check("strategy_store", _check_store))

        # 34. Query service importable
        def _check_query():
            from paper_trading.strategy.store_v162 import PaperStrategyStore
            from paper_trading.strategy.query_v162 import PaperStrategyQueryService
            store = PaperStrategyStore()
            qs = PaperStrategyQueryService(store)
            summary = qs.full_summary()
            assert summary["paper_only"] is True
            return True
        checks.append(_check("query_service", _check_query))

        # Build result
        passed = sum(1 for _, ok, _ in checks if ok)
        failed = sum(1 for _, ok, _ in checks if not ok)
        total = len(checks)
        status = "HEALTHY" if failed == 0 else "DEGRADED"

        return {
            "status": status,
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": [
                {"name": name, "ok": ok, "detail": detail}
                for name, ok, detail in checks
            ],
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "broker_enabled": False,
            "production_trading_blocked": True,
        }

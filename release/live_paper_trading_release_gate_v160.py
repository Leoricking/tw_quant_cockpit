"""release/live_paper_trading_release_gate_v160.py — Live Paper Trading Release Gate v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. NO BROKER. PRODUCTION TRADING: BLOCKED.
Any safety failure → BLOCKED.
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple

GATE_VERSION = "1.6.0"
RESEARCH_ONLY = True

GATE_CHECKS = [
    "PAPER_MODELS_VALID",
    "PAPER_SESSION_ENGINE_VALID",
    "MARKET_SESSION_VALID",
    "DATA_CLASSIFICATION_VALID",
    "EVENT_BUS_VALID",
    "EVENT_JOURNAL_VALID",
    "IDEMPOTENCY_VALID",
    "PAPER_ORDER_STATE_MACHINE_VALID",
    "PAPER_EXECUTION_SIMULATOR_VALID",
    "LATENCY_MODEL_VALID",
    "SLIPPAGE_MODEL_VALID",
    "LIQUIDITY_MODEL_VALID",
    "PARTIAL_FILL_VALID",
    "PAPER_LEDGER_VALID",
    "PAPER_POSITION_VALID",
    "PAPER_CASH_VALID",
    "PAPER_PNL_VALID",
    "PAPER_RISK_GATE_VALID",
    "PAPER_KILL_SWITCH_VALID",
    "PAPER_SESSION_REPLAY_VALID",
    "PAPER_RECOVERY_VALID",
    "PAPER_SNAPSHOT_VALID",
    "PAPER_AUDIT_VALID",
    "PAPER_LINEAGE_VALID",
    "PAPER_REPRODUCIBILITY_VALID",
    "NO_REAL_ORDER_CREATION",
    "NO_REAL_ORDER_EXECUTION",
    "NO_BROKER_CONNECTION",
    "NO_REAL_ACCOUNT_SYNC",
    "NO_FORMAL_PORTFOLIO_LEDGER_WRITE",
    "NO_PRODUCTION_TRADING",
]

SAFETY_GATES = [
    "NO_REAL_ORDER_CREATION",
    "NO_REAL_ORDER_EXECUTION",
    "NO_BROKER_CONNECTION",
    "NO_REAL_ACCOUNT_SYNC",
    "NO_FORMAL_PORTFOLIO_LEDGER_WRITE",
    "NO_PRODUCTION_TRADING",
]


def _check(name: str, fn) -> Dict[str, Any]:
    try:
        ok, detail = fn()
        return {"check": name, "passed": ok, "detail": detail, "blocked": not ok and name in SAFETY_GATES}
    except Exception as exc:
        return {"check": name, "passed": False, "detail": f"EXCEPTION: {exc}", "blocked": name in SAFETY_GATES}


class LivePaperTradingReleaseGate:
    def run(self) -> Dict[str, Any]:
        from decimal import Decimal

        results = []

        def _models():
            from paper_trading.models_v160 import PaperSessionConfig, PaperOrder, PaperLedgerEntry
            cfg = PaperSessionConfig(session_id="gate", name="gate")
            assert cfg.research_only is True
            assert cfg.broker_enabled is False
            return True, "paper models valid"
        results.append(_check("PAPER_MODELS_VALID", _models))

        def _session():
            from paper_trading.session_v160 import PaperTradingSessionEngine
            from paper_trading.models_v160 import PaperSessionConfig
            from paper_trading.enums_v160 import PaperSessionStatus
            cfg = PaperSessionConfig(session_id="gate_se", name="gate")
            e = PaperTradingSessionEngine(cfg)
            e.start()
            assert e.status == PaperSessionStatus.RUNNING
            e.pause()
            e.complete()
            return True, "session engine valid"
        results.append(_check("PAPER_SESSION_ENGINE_VALID", _session))

        def _market():
            from paper_trading.market_session_v160 import TWMarketSessionState
            from paper_trading.enums_v160 import MarketSessionStatus
            import datetime
            ms = TWMarketSessionState()
            s = ms.update(datetime.datetime(2024, 3, 4, 10, 0, 0))
            assert s == MarketSessionStatus.OPEN
            assert not ms.can_simulate_fill(datetime.datetime(2024, 3, 2, 10, 0, 0))  # weekend
            return True, "market session valid"
        results.append(_check("MARKET_SESSION_VALID", _market))

        def _data():
            from paper_trading.data_classification_v160 import DataClassifier
            from paper_trading.enums_v160 import DataMode
            ok, mode, _ = DataClassifier.classify("FIXTURE")
            assert mode == DataMode.FIXTURE
            ok2, _, _ = DataClassifier.classify("UNKNOWN_XYZ")
            assert not ok2
            return True, "data classification valid"
        results.append(_check("DATA_CLASSIFICATION_VALID", _data))

        def _event_bus():
            from paper_trading.event_bus_v160 import PaperEventBus
            from paper_trading.event_v160 import PaperEvent
            from paper_trading.enums_v160 import PaperEventType
            bus = PaperEventBus()
            e = PaperEvent(event_id="g1", sequence=0, event_type=PaperEventType.SESSION_CREATED,
                           session_id="s1", idempotency_key="gk1", timestamp="2024-01-01T00:00:00Z", payload={})
            bus.publish(e)
            assert bus.verify_chain()
            return True, "event bus valid"
        results.append(_check("EVENT_BUS_VALID", _event_bus))

        def _journal():
            from paper_trading.event_journal_v160 import PaperEventJournal
            from paper_trading.event_v160 import PaperEvent
            from paper_trading.enums_v160 import PaperEventType
            j = PaperEventJournal()
            e = PaperEvent(event_id="gj1", sequence=0, event_type=PaperEventType.DATA_RECEIVED,
                           session_id="s1", idempotency_key="gjk1", timestamp="2024-01-01T00:00:00Z", payload={})
            j.append(e)
            assert j.verify_chain()
            return True, "journal valid"
        results.append(_check("EVENT_JOURNAL_VALID", _journal))

        def _idem():
            from paper_trading.idempotency_v160 import IdempotencyRegistry
            r = IdempotencyRegistry()
            r.register("k1", 0)
            assert r.is_duplicate("k1")
            return True, "idempotency valid"
        results.append(_check("IDEMPOTENCY_VALID", _idem))

        def _osm():
            from paper_trading.order_state_machine_v160 import PaperOrderStateMachine
            from paper_trading.models_v160 import PaperOrder
            from paper_trading.enums_v160 import PaperOrderSide, PaperOrderType, PaperOrderStatus
            o = PaperOrder(paper_order_id="go1", session_id="s1", client_order_id="gc1",
                           symbol="2330", side=PaperOrderSide.BUY,
                           order_type=PaperOrderType.MARKET, quantity=Decimal("100"))
            sm = PaperOrderStateMachine(o)
            sm.transition(PaperOrderStatus.VALIDATED)
            sm.transition(PaperOrderStatus.QUEUED)
            assert o.status == PaperOrderStatus.QUEUED
            return True, "order state machine valid"
        results.append(_check("PAPER_ORDER_STATE_MACHINE_VALID", _osm))

        def _exec_sim():
            from paper_trading.execution_simulator_v160 import PaperExecutionSimulator
            sim = PaperExecutionSimulator()
            assert sim is not None
            return True, "execution simulator valid"
        results.append(_check("PAPER_EXECUTION_SIMULATOR_VALID", _exec_sim))

        def _latency():
            from paper_trading.latency_model_v160 import build_latency_assumption
            la = build_latency_assumption("ZERO_DISCLOSED")
            assert "ZERO" in la.describe()
            return True, "latency model valid"
        results.append(_check("LATENCY_MODEL_VALID", _latency))

        def _slip():
            from paper_trading.slippage_model_v160 import compute_slippage
            from paper_trading.enums_v160 import PaperOrderSide, SlippageModel
            r = compute_slippage(SlippageModel.FIXED_BPS, PaperOrderSide.BUY, Decimal("500"), Decimal("100"))
            assert not r.blocked
            return True, "slippage model valid"
        results.append(_check("SLIPPAGE_MODEL_VALID", _slip))

        def _liq():
            from paper_trading.liquidity_model_v160 import LiquidityChecker
            lc = LiquidityChecker()
            r = lc.check(Decimal("100"), Decimal("10000"))
            assert not r.blocked
            r2 = lc.check(Decimal("100"), Decimal("0"))
            assert r2.zero_volume
            return True, "liquidity model valid"
        results.append(_check("LIQUIDITY_MODEL_VALID", _liq))

        def _pfill():
            from paper_trading.partial_fill_v160 import compute_fill_quantities, is_overfill
            _, _, stat, _ = compute_fill_quantities(Decimal("1000"), Decimal("0"), Decimal("600"))
            from paper_trading.enums_v160 import PaperOrderStatus
            assert stat == PaperOrderStatus.PARTIALLY_FILLED
            assert is_overfill(Decimal("1000"), Decimal("1001"))
            return True, "partial fill valid"
        results.append(_check("PARTIAL_FILL_VALID", _pfill))

        def _ledger():
            from paper_trading.paper_ledger_v160 import PaperLedger
            l = PaperLedger("gate_s")
            l.append("INIT")
            assert l.verify_chain()
            return True, "paper ledger valid"
        results.append(_check("PAPER_LEDGER_VALID", _ledger))

        def _pos():
            from paper_trading.paper_position_v160 import PaperPositionManager
            from paper_trading.enums_v160 import PaperOrderSide
            pm = PaperPositionManager("gs1")
            pm.apply_fill("2330", PaperOrderSide.BUY, Decimal("100"), Decimal("500"), Decimal("7"), Decimal("0"))
            assert pm.get_quantity("2330") == Decimal("100")
            return True, "paper position valid"
        results.append(_check("PAPER_POSITION_VALID", _pos))

        def _cash():
            from paper_trading.paper_cash_v160 import PaperCashManager
            cm = PaperCashManager("gs1", Decimal("1000000"))
            ok = cm.reserve_for_order(Decimal("100000"), "go1")
            assert ok
            return True, "paper cash valid"
        results.append(_check("PAPER_CASH_VALID", _cash))

        def _pnl():
            from paper_trading.paper_pnl_v160 import PaperPnLCalculator
            r = PaperPnLCalculator().compute("gs1", Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("1000000"))
            assert r.paper_only is True
            return True, "P&L valid"
        results.append(_check("PAPER_PNL_VALID", _pnl))

        def _risk():
            from paper_trading.paper_risk_gate_v160 import PaperRiskGate
            from paper_trading.enums_v160 import (
                PaperOrderSide, DataMode, MarketSessionStatus,
                PaperSessionStatus, PaperRiskStatus,
            )
            rg = PaperRiskGate()
            r = rg.evaluate("ev1", "gs1", "go1", "2330", PaperOrderSide.BUY,
                            Decimal("100"), Decimal("500"),
                            PaperSessionStatus.RUNNING, MarketSessionStatus.OPEN,
                            DataMode.FIXTURE, True, Decimal("1000000"), Decimal("0"),
                            Decimal("1000000"), Decimal("0"), False, price=Decimal("500"))
            assert r.status == PaperRiskStatus.PASS
            return True, "risk gate valid"
        results.append(_check("PAPER_RISK_GATE_VALID", _risk))

        def _ks():
            from paper_trading.paper_kill_switch_v160 import PaperKillSwitch
            ks = PaperKillSwitch()
            ks.manual_halt("gate test")
            assert ks.is_triggered
            return True, "kill switch valid"
        results.append(_check("PAPER_KILL_SWITCH_VALID", _ks))

        def _replay():
            from paper_trading.session_replay_v160 import PaperSessionReplay
            r = PaperSessionReplay().replay("gs1", [])
            assert r.not_live is True
            return True, "session replay valid"
        results.append(_check("PAPER_SESSION_REPLAY_VALID", _replay))

        def _recovery():
            from paper_trading.recovery_v160 import PaperSessionRecovery
            from paper_trading.enums_v160 import PaperSessionStatus
            r = PaperSessionRecovery().recover("gs1", None, None)
            assert r.recovered_status == PaperSessionStatus.PAUSED
            assert r.auto_resume_enabled is False
            return True, "recovery valid"
        results.append(_check("PAPER_RECOVERY_VALID", _recovery))

        def _snap():
            from paper_trading.snapshot_v160 import SnapshotService
            s = SnapshotService().create("gs1")
            assert s.content_hash != ""
            return True, "snapshot valid"
        results.append(_check("PAPER_SNAPSHOT_VALID", _snap))

        def _audit():
            from paper_trading.audit_v160 import PaperAuditTrail
            trail = PaperAuditTrail("gs1")
            trail.record("system", "gate_test")
            assert trail.count() == 1
            return True, "audit trail valid"
        results.append(_check("PAPER_AUDIT_VALID", _audit))

        def _lineage():
            from paper_trading.lineage_v160 import PaperLineageService
            r = PaperLineageService("gs1").record("l1", "session", "gs1")
            assert r.paper_only is True
            return True, "lineage valid"
        results.append(_check("PAPER_LINEAGE_VALID", _lineage))

        def _repro():
            from paper_trading.reproducibility_v160 import ReproducibilityService
            from paper_trading.models_v160 import PaperSessionConfig
            cfg = PaperSessionConfig(session_id="gr1", name="gr")
            m = ReproducibilityService().build_manifest("gm1", "gr1", cfg, [])
            assert m.paper_only is True
            return True, "reproducibility valid"
        results.append(_check("PAPER_REPRODUCIBILITY_VALID", _repro))

        # Safety gates
        def _no_real_order_creation():
            from paper_trading import REAL_ORDER_CREATION_ENABLED
            if REAL_ORDER_CREATION_ENABLED is not False:
                return False, f"REAL_ORDER_CREATION_ENABLED={REAL_ORDER_CREATION_ENABLED} — BLOCKED"
            return True, "REAL_ORDER_CREATION_ENABLED=False"
        results.append(_check("NO_REAL_ORDER_CREATION", _no_real_order_creation))

        def _no_real_order_exec():
            from paper_trading import REAL_ORDER_EXECUTION_ENABLED
            if REAL_ORDER_EXECUTION_ENABLED is not False:
                return False, f"REAL_ORDER_EXECUTION_ENABLED={REAL_ORDER_EXECUTION_ENABLED} — BLOCKED"
            return True, "REAL_ORDER_EXECUTION_ENABLED=False"
        results.append(_check("NO_REAL_ORDER_EXECUTION", _no_real_order_exec))

        def _no_broker():
            from paper_trading import BROKER_CONNECTION_ENABLED, BROKER_EXECUTION_ENABLED
            if BROKER_CONNECTION_ENABLED is not False or BROKER_EXECUTION_ENABLED is not False:
                return False, "BROKER enabled — BLOCKED"
            return True, "BROKER_CONNECTION_ENABLED=False BROKER_EXECUTION_ENABLED=False"
        results.append(_check("NO_BROKER_CONNECTION", _no_broker))

        def _no_account_sync():
            from paper_trading import LIVE_ACCOUNT_SYNC_ENABLED
            if LIVE_ACCOUNT_SYNC_ENABLED is not False:
                return False, "LIVE_ACCOUNT_SYNC_ENABLED=True — BLOCKED"
            return True, "LIVE_ACCOUNT_SYNC_ENABLED=False"
        results.append(_check("NO_REAL_ACCOUNT_SYNC", _no_account_sync))

        def _no_formal_ledger():
            from paper_trading import REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
            if REAL_PORTFOLIO_LEDGER_WRITE_ENABLED is not False:
                return False, "REAL_PORTFOLIO_LEDGER_WRITE_ENABLED=True — BLOCKED"
            return True, "REAL_PORTFOLIO_LEDGER_WRITE_ENABLED=False"
        results.append(_check("NO_FORMAL_PORTFOLIO_LEDGER_WRITE", _no_formal_ledger))

        def _no_prod():
            from paper_trading import PRODUCTION_TRADING_ENABLED, PRODUCTION_TRADING_BLOCKED
            if PRODUCTION_TRADING_ENABLED is not False or PRODUCTION_TRADING_BLOCKED is not True:
                return False, "PRODUCTION_TRADING not blocked — BLOCKED"
            return True, "PRODUCTION_TRADING_ENABLED=False PRODUCTION_TRADING_BLOCKED=True"
        results.append(_check("NO_PRODUCTION_TRADING", _no_prod))

        passed = sum(1 for r in results if r["passed"])
        failed = sum(1 for r in results if not r["passed"])
        blocked = [r["check"] for r in results if r.get("blocked")]
        total = len(results)
        overall = "BLOCKED" if blocked else ("PASS" if failed == 0 else "FAIL")

        return {
            "gate_version": GATE_VERSION,
            "overall": overall,
            "gate_passed": overall == "PASS",
            "passed": passed,
            "failed": failed,
            "total": total,
            "blocked": blocked,
            "checks": results,
            "research_only": RESEARCH_ONLY,
            "no_real_orders": True,
            "no_broker": True,
            "production_trading_blocked": True,
        }


def run_release_gate() -> Dict[str, Any]:
    return LivePaperTradingReleaseGate().run()

"""paper_trading/health_v160.py — Live Paper Trading Health Check v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Tuple


def _check(name: str, fn) -> Tuple[str, bool, str]:
    try:
        ok, detail = fn()
        return name, ok, detail
    except Exception as exc:
        return name, False, f"EXCEPTION: {exc}"


class LivePaperTradingHealthCheck:
    HEALTH_VERSION = "1.6.0"

    def run(self) -> Dict[str, Any]:
        results = []

        # package import
        def _pkg():
            import paper_trading
            ok = (
                paper_trading.NO_REAL_ORDERS is True and
                paper_trading.BROKER_EXECUTION_ENABLED is False and
                paper_trading.PRODUCTION_TRADING_BLOCKED is True and
                paper_trading.REAL_ORDER_CREATION_ENABLED is False
            )
            return ok, f"version={paper_trading.PAPER_TRADING_VERSION}"
        results.append(_check("package_import", _pkg))

        # enums
        def _enums():
            from paper_trading.enums_v160 import (
                PaperSessionStatus, MarketSessionStatus, DataMode,
                PaperOrderType, PaperOrderSide, PaperOrderStatus,
                PaperFillStatus, PaperRiskStatus, PaperEventType,
                LatencyModel, SlippageModel, KillSwitchReason,
            )
            assert len(list(PaperSessionStatus)) == 9
            assert len(list(MarketSessionStatus)) == 6
            assert len(list(DataMode)) == 5
            assert len(list(PaperOrderType)) == 4
            assert len(list(PaperOrderSide)) == 2
            assert PaperOrderSide.BUY.value == "BUY"
            assert "SHORT" not in [s.value for s in PaperOrderSide]
            return True, "all enums valid, SHORT excluded"
        results.append(_check("enums", _enums))

        # models
        def _models():
            from paper_trading.models_v160 import (
                PaperSessionConfig, PaperOrder, PaperFill,
                PaperPosition, PaperCashBalance, PaperLedgerEntry,
                PaperSessionSnapshot,
            )
            from paper_trading.enums_v160 import DataMode
            cfg = PaperSessionConfig(session_id="test", name="test", initial_cash=Decimal("1000000"))
            assert cfg.research_only is True
            assert cfg.broker_enabled is False
            assert cfg.real_order_enabled is False
            assert cfg.formal_ledger_write_enabled is False
            return True, "models valid, safety flags enforced"
        results.append(_check("models", _models))

        # validation
        def _validation():
            from paper_trading.validation_v160 import validate_session_config
            from paper_trading.models_v160 import PaperSessionConfig
            cfg = PaperSessionConfig(session_id="v", name="v", initial_cash=Decimal("500000"))
            ok, errors = validate_session_config(cfg)
            return ok, f"errors={errors}"
        results.append(_check("validation", _validation))

        # session engine
        def _session():
            from paper_trading.session_v160 import PaperTradingSessionEngine
            from paper_trading.models_v160 import PaperSessionConfig
            from paper_trading.enums_v160 import PaperSessionStatus
            cfg = PaperSessionConfig(session_id="health_se", name="health")
            e = PaperTradingSessionEngine(cfg)
            e.start()
            assert e.status == PaperSessionStatus.RUNNING
            e.pause()
            assert e.status == PaperSessionStatus.PAUSED
            e.resume()
            e.complete()
            assert e.status == PaperSessionStatus.COMPLETED
            return True, "session lifecycle PASS"
        results.append(_check("session_engine", _session))

        # market session
        def _market():
            from paper_trading.market_session_v160 import TWMarketSessionState
            from paper_trading.enums_v160 import MarketSessionStatus
            import datetime
            ms = TWMarketSessionState()
            dt_open = datetime.datetime(2024, 3, 4, 10, 0, 0)  # Monday 10am
            s = ms.update(dt_open)
            assert s == MarketSessionStatus.OPEN
            dt_weekend = datetime.datetime(2024, 3, 2, 10, 0, 0)  # Saturday
            s2 = ms.update(dt_weekend)
            assert s2 == MarketSessionStatus.NON_TRADING_DAY
            return True, "market session calendar valid"
        results.append(_check("market_session", _market))

        # data classification
        def _data_class():
            from paper_trading.data_classification_v160 import DataClassifier
            from paper_trading.enums_v160 import DataMode
            ok, mode, _ = DataClassifier.classify("FIXTURE")
            assert ok and mode == DataMode.FIXTURE
            ok2, mode2, reason2 = DataClassifier.classify("UNKNOWN_MODE")
            assert not ok2
            ok3, msg3 = DataClassifier.validate_for_paper_trading(DataMode.FIXTURE)
            assert ok3
            ok4, msg4 = DataClassifier.can_generate_formal_conclusion(DataMode.FIXTURE)
            assert not ok4
            return True, "data classification valid"
        results.append(_check("data_classification", _data_class))

        # event bus
        def _event_bus():
            from paper_trading.event_bus_v160 import PaperEventBus
            from paper_trading.event_v160 import PaperEvent
            from paper_trading.enums_v160 import PaperEventType
            bus = PaperEventBus()
            evt = PaperEvent(
                event_id="e1", sequence=0, event_type=PaperEventType.SESSION_CREATED,
                session_id="s1", idempotency_key="k1",
                timestamp="2024-01-01T00:00:00Z", payload={},
            )
            bus.publish(evt)
            assert bus.event_count() == 1
            return True, "event bus valid"
        results.append(_check("event_bus", _event_bus))

        # event journal
        def _journal():
            from paper_trading.event_journal_v160 import PaperEventJournal
            from paper_trading.event_v160 import PaperEvent
            from paper_trading.enums_v160 import PaperEventType
            j = PaperEventJournal()
            e = PaperEvent(
                event_id="ej1", sequence=0, event_type=PaperEventType.DATA_RECEIVED,
                session_id="s1", idempotency_key="jk1",
                timestamp="2024-01-01T00:00:00Z", payload={},
            )
            j.append(e)
            assert j.verify_chain()
            return True, "journal hash chain valid"
        results.append(_check("event_journal", _journal))

        # idempotency
        def _idem():
            from paper_trading.idempotency_v160 import IdempotencyRegistry
            r = IdempotencyRegistry()
            r.register("key1", 0)
            assert r.is_duplicate("key1")
            assert not r.is_duplicate("key2")
            return True, "idempotency registry valid"
        results.append(_check("idempotency", _idem))

        # paper order
        def _order():
            from paper_trading.models_v160 import PaperOrder
            from paper_trading.enums_v160 import PaperOrderSide, PaperOrderType, PaperOrderStatus
            o = PaperOrder(
                paper_order_id="o1", session_id="s1", client_order_id="c1",
                symbol="2330", side=PaperOrderSide.BUY,
                order_type=PaperOrderType.LIMIT,
                quantity=Decimal("1000"),
                limit_price=Decimal("500"),
            )
            assert o.research_only is True
            assert o.executable_on_broker is False
            assert o.real_order_created is False
            assert o.paper_only == "PAPER_ONLY"
            return True, "paper order model valid"
        results.append(_check("paper_order", _order))

        # order state machine
        def _osm():
            from paper_trading.order_state_machine_v160 import PaperOrderStateMachine
            from paper_trading.models_v160 import PaperOrder
            from paper_trading.enums_v160 import PaperOrderSide, PaperOrderType, PaperOrderStatus
            o = PaperOrder(
                paper_order_id="o2", session_id="s1", client_order_id="c2",
                symbol="2330", side=PaperOrderSide.BUY,
                order_type=PaperOrderType.MARKET, quantity=Decimal("100"),
            )
            sm = PaperOrderStateMachine(o)
            sm.transition(PaperOrderStatus.VALIDATED)
            sm.transition(PaperOrderStatus.QUEUED)
            assert o.status == PaperOrderStatus.QUEUED
            assert sm.can_fill()
            return True, "order state machine valid"
        results.append(_check("order_state_machine", _osm))

        # paper fill
        def _fill():
            from paper_trading.paper_fill_v160 import create_paper_fill
            from paper_trading.enums_v160 import PaperOrderSide
            f = create_paper_fill(
                paper_order_id="o1", session_id="s1", symbol="2330",
                side=PaperOrderSide.BUY, quantity=Decimal("1000"),
                fill_price=Decimal("500"),
            )
            assert f.paper_only == "PAPER_ONLY"
            assert f.not_a_real_order == "NOT_A_REAL_ORDER"
            return True, "paper fill valid"
        results.append(_check("paper_fill", _fill))

        # execution simulator
        def _exec():
            from paper_trading.execution_simulator_v160 import PaperExecutionSimulator
            from paper_trading.models_v160 import PaperOrder, PaperMarketEvent
            from paper_trading.enums_v160 import (
                PaperOrderSide, PaperOrderType, PaperOrderStatus, DataMode,
            )
            from paper_trading.order_state_machine_v160 import PaperOrderStateMachine
            sim = PaperExecutionSimulator()
            order = PaperOrder(
                paper_order_id="o3", session_id="s1", client_order_id="c3",
                symbol="2330", side=PaperOrderSide.BUY,
                order_type=PaperOrderType.MARKET, quantity=Decimal("1000"),
            )
            sm = PaperOrderStateMachine(order)
            sm.transition(PaperOrderStatus.VALIDATED)
            sm.transition(PaperOrderStatus.QUEUED)
            event = PaperMarketEvent(
                event_id="ev1", sequence=0, symbol="2330", event_type="TRADE",
                exchange_timestamp="2024-01-02T09:30:00Z",
                received_timestamp="2024-01-02T09:30:00Z",
                available_from="2024-01-02T09:30:00Z",
                price=Decimal("500"), volume=Decimal("100000"),
                bid=Decimal("499"), ask=Decimal("501"),
                data_mode=DataMode.FIXTURE,
            )
            result = sim.simulate(order, event)
            assert result.filled
            return True, "execution simulator valid"
        results.append(_check("execution_simulator", _exec))

        # latency
        def _latency():
            from paper_trading.latency_model_v160 import build_latency_assumption
            from paper_trading.enums_v160 import LatencyModel
            la = build_latency_assumption("ZERO_DISCLOSED")
            assert la.model == LatencyModel.ZERO_DISCLOSED
            assert "ZERO" in la.describe()
            return True, "latency model valid"
        results.append(_check("latency", _latency))

        # slippage
        def _slippage():
            from paper_trading.slippage_model_v160 import compute_slippage
            from paper_trading.enums_v160 import PaperOrderSide, SlippageModel
            r = compute_slippage(SlippageModel.FIXED_BPS, PaperOrderSide.BUY, Decimal("500"), Decimal("1000"))
            assert not r.blocked
            assert r.slippage_bps == Decimal("10")
            return True, "slippage model valid"
        results.append(_check("slippage", _slippage))

        # liquidity
        def _liquidity():
            from paper_trading.liquidity_model_v160 import LiquidityChecker
            lc = LiquidityChecker()
            r = lc.check(Decimal("100"), Decimal("10000"))
            assert not r.partial_fill
            r2 = lc.check(Decimal("5000"), Decimal("1000"))
            assert r2.partial_fill
            r3 = lc.check(Decimal("100"), Decimal("0"))
            assert r3.zero_volume
            return True, "liquidity model valid"
        results.append(_check("liquidity", _liquidity))

        # partial fill
        def _pfill():
            from paper_trading.partial_fill_v160 import compute_fill_quantities, is_overfill
            from paper_trading.enums_v160 import PaperOrderStatus, PaperFillStatus
            fq, rem, stat, fstat = compute_fill_quantities(Decimal("1000"), Decimal("0"), Decimal("600"))
            assert fq == Decimal("600")
            assert stat == PaperOrderStatus.PARTIALLY_FILLED
            assert not is_overfill(Decimal("1000"), Decimal("600"))
            assert is_overfill(Decimal("1000"), Decimal("1100"))
            return True, "partial fill valid"
        results.append(_check("partial_fill", _pfill))

        # paper position
        def _pos():
            from paper_trading.paper_position_v160 import PaperPositionManager
            from paper_trading.enums_v160 import PaperOrderSide
            pm = PaperPositionManager("s1")
            pm.apply_fill("2330", PaperOrderSide.BUY, Decimal("1000"), Decimal("500"), Decimal("71"), Decimal("0"))
            p = pm.get_position("2330")
            assert p.quantity == Decimal("1000")
            assert p.average_cost == Decimal("500")
            return True, "paper position valid"
        results.append(_check("paper_position", _pos))

        # paper cash
        def _cash():
            from paper_trading.paper_cash_v160 import PaperCashManager
            cm = PaperCashManager("s1", Decimal("1000000"))
            assert cm.available_cash == Decimal("1000000")
            ok = cm.reserve_for_order(Decimal("500000"), "o1")
            assert ok
            assert cm.available_cash == Decimal("500000")
            return True, "paper cash valid"
        results.append(_check("paper_cash", _cash))

        # paper ledger
        def _ledger():
            from paper_trading.paper_ledger_v160 import PaperLedger
            l = PaperLedger("s1")
            l.append("ORDER_QUEUED", paper_order_id="o1")
            l.append("FILL", fill_id="f1", cash_delta=Decimal("-500000"))
            assert l.count() == 2
            assert l.verify_chain()
            return True, "paper ledger hash chain valid"
        results.append(_check("paper_ledger", _ledger))

        # P&L
        def _pnl():
            from paper_trading.paper_pnl_v160 import PaperPnLCalculator
            calc = PaperPnLCalculator()
            r = calc.compute(
                session_id="s1",
                realized_pnl=Decimal("10000"),
                unrealized_pnl=Decimal("5000"),
                total_fees=Decimal("500"),
                total_taxes=Decimal("150"),
                total_slippage=Decimal("100"),
                gross_exposure=Decimal("500000"),
                initial_cash=Decimal("1000000"),
            )
            assert r.paper_only is True
            assert r.total_pnl == Decimal("10000") + Decimal("5000") - Decimal("500") - Decimal("150") - Decimal("100")
            return True, "P&L calculation valid"
        results.append(_check("paper_pnl", _pnl))

        # risk gate
        def _risk():
            from paper_trading.paper_risk_gate_v160 import PaperRiskGate
            from paper_trading.enums_v160 import (
                PaperOrderSide, DataMode, MarketSessionStatus,
                PaperSessionStatus, PaperRiskStatus,
            )
            rg = PaperRiskGate()
            r = rg.evaluate(
                evaluation_id="ev1", session_id="s1", paper_order_id="o1",
                symbol="2330", side=PaperOrderSide.BUY,
                quantity=Decimal("1000"), limit_price=Decimal("500"),
                session_status=PaperSessionStatus.RUNNING,
                market_status=MarketSessionStatus.OPEN,
                data_mode=DataMode.FIXTURE,
                data_fresh=True,
                available_cash=Decimal("1000000"),
                existing_position=Decimal("0"),
                total_portfolio_value=Decimal("1000000"),
                drawdown_pct=Decimal("0"),
                kill_switch_triggered=False,
                price=Decimal("500"),
            )
            assert r.status != PaperRiskStatus.BLOCKED, f"unexpected BLOCKED: {r.block_reasons}"
            return True, f"risk gate valid, status={r.status.value}"
        results.append(_check("risk_gate", _risk))

        # kill switch
        def _ks():
            from paper_trading.paper_kill_switch_v160 import PaperKillSwitch
            from paper_trading.enums_v160 import KillSwitchReason
            ks = PaperKillSwitch()
            assert not ks.is_triggered
            evt = ks.manual_halt("test")
            assert ks.is_triggered
            assert evt.reason == KillSwitchReason.MANUAL_HALT
            return True, "kill switch valid"
        results.append(_check("kill_switch", _ks))

        # session replay
        def _replay():
            from paper_trading.session_replay_v160 import PaperSessionReplay
            svc = PaperSessionReplay()
            r = svc.replay("s1", [])
            assert r.paper_only is True
            assert r.not_live is True
            return True, "session replay valid"
        results.append(_check("session_replay", _replay))

        # recovery
        def _recovery():
            from paper_trading.recovery_v160 import PaperSessionRecovery
            from paper_trading.enums_v160 import PaperSessionStatus
            svc = PaperSessionRecovery()
            r = svc.recover("s1", None, None)
            assert not r.success
            assert r.recovered_status == PaperSessionStatus.PAUSED
            assert not r.auto_resume_enabled
            return True, "recovery valid"
        results.append(_check("recovery", _recovery))

        # snapshot
        def _snapshot():
            from paper_trading.snapshot_v160 import SnapshotService
            ss = SnapshotService()
            snap = ss.create("s1", as_of="2024-01-02T09:30:00Z")
            assert snap.session_id == "s1"
            assert snap.content_hash != ""
            return True, "snapshot valid"
        results.append(_check("snapshot", _snapshot))

        # audit
        def _audit():
            from paper_trading.audit_v160 import PaperAuditTrail
            trail = PaperAuditTrail("s1")
            r = trail.record("system", "start")
            assert r.audit_id.startswith("aud_")
            return True, "audit trail valid"
        results.append(_check("audit", _audit))

        # lineage
        def _lineage():
            from paper_trading.lineage_v160 import PaperLineageService
            svc = PaperLineageService("s1")
            r = svc.record("lin1", "order", "o1")
            assert r.paper_only is True
            return True, "lineage valid"
        results.append(_check("lineage", _lineage))

        # reproducibility
        def _repro():
            from paper_trading.reproducibility_v160 import ReproducibilityService
            from paper_trading.models_v160 import PaperSessionConfig
            svc = ReproducibilityService()
            cfg = PaperSessionConfig(session_id="r1", name="r")
            m = svc.build_manifest("m1", "r1", cfg, [], code_commit="abc")
            assert m.research_only is True
            assert m.paper_only is True
            return True, "reproducibility valid"
        results.append(_check("reproducibility", _repro))

        # store
        def _store():
            from paper_trading.store_v160 import PaperTradingStore
            s = PaperTradingStore()
            s.save_session("s1", {"status": "CREATED"})
            assert s.get_session("s1") is not None
            return True, "store valid"
        results.append(_check("store", _store))

        # query
        def _query():
            from paper_trading.query_v160 import PaperTradingQueryService
            from paper_trading.models_v160 import PaperSessionConfig
            svc = PaperTradingQueryService()
            assert hasattr(svc, "submit_paper_order")
            assert hasattr(svc, "submit_real_order")
            try:
                svc.submit_real_order()
                return False, "submit_real_order should raise"
            except NotImplementedError:
                pass
            return True, "query service valid, forbidden methods raise"
        results.append(_check("query", _query))

        # CLI
        def _cli():
            from cli.command_registry import get_formal_command_names
            all_cmds = get_formal_command_names()
            paper_cmds = [c for c in all_cmds if c.startswith("paper-")]
            return len(paper_cmds) >= 30, f"paper CLI commands={len(paper_cmds)}"
        results.append(_check("CLI", _cli))

        # GUI
        def _gui():
            import gui.live_paper_trading_panel as p
            assert hasattr(p, "LivePaperTradingPanel")
            return True, "GUI panel importable"
        results.append(_check("GUI", _gui))

        # headless GUI
        def _headless():
            import gui.live_paper_trading_panel as p
            # Must not crash on import without QApplication
            return True, "headless import safe"
        results.append(_check("headless_GUI", _headless))

        # safety checks
        def _safety_no_broker():
            from paper_trading import BROKER_CONNECTION_ENABLED, BROKER_EXECUTION_ENABLED
            return (BROKER_CONNECTION_ENABLED is False and BROKER_EXECUTION_ENABLED is False), "no broker"
        results.append(_check("no_broker", _safety_no_broker))

        def _safety_no_real_order():
            from paper_trading import REAL_ORDER_CREATION_ENABLED, REAL_ORDER_EXECUTION_ENABLED
            return (REAL_ORDER_CREATION_ENABLED is False and REAL_ORDER_EXECUTION_ENABLED is False), "no real order"
        results.append(_check("no_real_order", _safety_no_real_order))

        def _safety_no_account():
            from paper_trading import LIVE_ACCOUNT_SYNC_ENABLED
            return LIVE_ACCOUNT_SYNC_ENABLED is False, "no real account sync"
        results.append(_check("no_real_account", _safety_no_account))

        def _safety_no_formal_ledger():
            from paper_trading import REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
            return REAL_PORTFOLIO_LEDGER_WRITE_ENABLED is False, "no formal ledger write"
        results.append(_check("no_formal_portfolio_ledger_write", _safety_no_formal_ledger))

        def _safety_no_prod():
            from paper_trading import PRODUCTION_TRADING_ENABLED
            return PRODUCTION_TRADING_ENABLED is False, "no production trading"
        results.append(_check("no_production_trading", _safety_no_prod))

        def _safety_no_real_orders():
            from paper_trading import NO_REAL_ORDERS
            return NO_REAL_ORDERS is True, f"NO_REAL_ORDERS={NO_REAL_ORDERS}"
        results.append(_check("no_real_orders", _safety_no_real_orders))

        def _safety_blocked():
            from paper_trading import PRODUCTION_TRADING_BLOCKED
            return PRODUCTION_TRADING_BLOCKED is True, f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED}"
        results.append(_check("production_trading_blocked", _safety_blocked))

        # Compile final result
        passed = sum(1 for _, ok, _ in results if ok)
        failed = sum(1 for _, ok, _ in results if not ok)
        total = len(results)

        return {
            "health_version": self.HEALTH_VERSION,
            "status": "PASS" if failed == 0 else "FAIL",
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": [
                {"check": name, "passed": ok, "detail": detail}
                for name, ok, detail in results
            ],
            "paper_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "production_trading_blocked": True,
        }

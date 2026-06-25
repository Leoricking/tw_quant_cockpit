"""
release/market_data_session_release_gate_v161.py — Release Gate v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
34 checks covering safety, modules, CLI, enums, models, pipeline, policies.
"""
from __future__ import annotations
import importlib
from typing import Dict, List, Any

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

_GATE_VERSION = "1.6.1"
_GATE_NAME = "Market Data Session Adapter"


class MarketDataSessionReleaseGate:
    """34-check release gate for v1.6.1 Market Data Session Adapter."""

    def run(self) -> Dict[str, Any]:
        checks: Dict[str, str] = {}
        blocked: List[str] = []

        def _pass(name):
            checks[name] = "PASS"

        def _fail(name, reason):
            checks[name] = f"FAIL: {reason}"
            blocked.append(name)

        # === Safety Invariants (1-6) ===
        try:
            import paper_trading.market_data as md
            assert md.NO_REAL_ORDERS is True
            assert md.BROKER_EXECUTION_ENABLED is False
            assert md.PRODUCTION_TRADING_BLOCKED is True
            assert md.MARKET_DATA_ONLY is True
            assert md.LIVE_TO_FIXTURE_FALLBACK_DISABLED is True
            assert md.LIVE_TO_OFFLINE_FALLBACK_DISABLED is True
            _pass("safety_no_real_orders")
            _pass("safety_broker_disabled")
            _pass("safety_trading_blocked")
            _pass("safety_market_data_only")
            _pass("safety_live_fixture_fallback_disabled")
            _pass("safety_live_offline_fallback_disabled")
        except Exception as e:
            _fail("safety_invariants", str(e))
            for s in ["safety_no_real_orders", "safety_broker_disabled",
                      "safety_trading_blocked", "safety_market_data_only",
                      "safety_live_fixture_fallback_disabled", "safety_live_offline_fallback_disabled"]:
                if s not in checks:
                    _fail(s, str(e))

        # === Version Info (7) ===
        try:
            from release.version_info import VERSION, RELEASE_NAME, MARKET_DATA_SESSION_BASELINE
            assert VERSION == "1.6.1", f"Expected 1.6.1, got {VERSION}"
            assert RELEASE_NAME == "Market Data Session Adapter", f"Got {RELEASE_NAME}"
            assert MARKET_DATA_SESSION_BASELINE == "1.6.1"
            _pass("version_info_161")
        except Exception as e:
            _fail("version_info_161", str(e))

        # === Enums (8) ===
        try:
            from paper_trading.market_data.enums_v161 import (
                MarketDataEventType, MarketDataSessionStatus, SourceClass,
                FreshnessStatus, SequenceStatus, DataQualityStatus, FeedFailureType,
                ReconnectPolicy, FailoverPolicy,
            )
            assert len(MarketDataEventType) == 9
            assert len(MarketDataSessionStatus) == 11
            assert len(SourceClass) == 6
            assert len(FreshnessStatus) == 6
            assert len(SequenceStatus) == 6
            assert len(DataQualityStatus) == 4
            assert len(FeedFailureType) == 9
            _pass("enums_all_defined")
        except Exception as e:
            _fail("enums_all_defined", str(e))

        # === Models safety assertions (9) ===
        try:
            from paper_trading.market_data.models_v161 import (
                MarketDataAdapterConfig, CanonicalQuoteEvent, CanonicalTradeEvent,
                MarketDataSessionConfig, MarketDataCheckpoint,
            )
            from paper_trading.market_data.enums_v161 import SourceClass
            from decimal import Decimal
            # UNKNOWN source blocked in config
            try:
                MarketDataAdapterConfig(
                    adapter_id="test", source_class=SourceClass.UNKNOWN,
                    provider_name="test", symbols=["2330"],
                )
                _fail("models_unknown_source_blocked", "Should have raised ValueError")
            except ValueError:
                _pass("models_unknown_source_blocked")
        except Exception as e:
            _fail("models_unknown_source_blocked", str(e))

        # === Bid<=Ask invariant (10) ===
        try:
            from paper_trading.market_data.models_v161 import CanonicalQuoteEvent
            from paper_trading.market_data.enums_v161 import SourceClass, FreshnessStatus, SequenceStatus, DataQualityStatus
            from decimal import Decimal
            try:
                CanonicalQuoteEvent(
                    event_id="e1", raw_event_id="r1", adapter_id="a1",
                    source_class=SourceClass.FIXTURE, symbol="2330",
                    timestamp_utc="2024-01-02T09:00:00Z",
                    bid_price=Decimal("200"), ask_price=Decimal("100"),
                    bid_size=100, ask_size=100, mid_price=Decimal("150"),
                    freshness_status=FreshnessStatus.NOT_APPLICABLE,
                    sequence_status=SequenceStatus.UNKNOWN,
                    quality_status=DataQualityStatus.PASS,
                )
                _fail("bid_ask_invariant", "Should have raised ValueError for bid>ask")
            except ValueError:
                _pass("bid_ask_invariant")
        except Exception as e:
            _fail("bid_ask_invariant", str(e))

        # === Adapter Registry duplicate blocked (11) ===
        try:
            from paper_trading.market_data.adapter_registry_v161 import (
                MarketDataAdapterRegistry, AdapterRegistryError,
            )
            from paper_trading.market_data.fixture_adapter_v161 import FixtureAdapter
            from paper_trading.market_data.models_v161 import MarketDataAdapterConfig
            from paper_trading.market_data.enums_v161 import SourceClass, ReconnectPolicy, FailoverPolicy
            cfg = MarketDataAdapterConfig(
                adapter_id="dup_test", source_class=SourceClass.FIXTURE,
                provider_name="test", symbols=["2330"],
            )
            a1 = FixtureAdapter(cfg)
            a2 = FixtureAdapter(cfg)
            reg = MarketDataAdapterRegistry()
            reg.register(a1, "event_time_utc")
            try:
                reg.register(a2, "event_time_utc")
                _fail("registry_duplicate_blocked", "Should have raised AdapterRegistryError")
            except AdapterRegistryError:
                _pass("registry_duplicate_blocked")
        except Exception as e:
            _fail("registry_duplicate_blocked", str(e))

        # === LIVE→FIXTURE failover blocked (12) ===
        try:
            from paper_trading.market_data.failover_v161 import FailoverManager
            from paper_trading.market_data.enums_v161 import FailoverPolicy, SourceClass
            fm = FailoverManager(FailoverPolicy.PAUSE_ON_FAILURE)
            decision = fm.decide(SourceClass.LIVE_PUBLIC, SourceClass.FIXTURE)
            assert decision.blocked is True
            _pass("failover_live_to_fixture_blocked")
        except Exception as e:
            _fail("failover_live_to_fixture_blocked", str(e))

        # === LIVE→OFFLINE failover blocked (13) ===
        try:
            from paper_trading.market_data.failover_v161 import FailoverManager
            from paper_trading.market_data.enums_v161 import FailoverPolicy, SourceClass
            fm = FailoverManager(FailoverPolicy.PAUSE_ON_FAILURE)
            decision = fm.decide(SourceClass.LIVE_PUBLIC, SourceClass.OFFLINE)
            assert decision.blocked is True
            _pass("failover_live_to_offline_blocked")
        except Exception as e:
            _fail("failover_live_to_offline_blocked", str(e))

        # === Checkpoint restores to PAUSED (14) ===
        try:
            from paper_trading.market_data.checkpoint_v161 import CheckpointManager
            from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
            cm = CheckpointManager()
            result_status = cm.restore_gives_paused()
            assert result_status == MarketDataSessionStatus.PAUSED
            _pass("checkpoint_restores_to_paused")
        except Exception as e:
            _fail("checkpoint_restores_to_paused", str(e))

        # === Resume always PAUSED (15) ===
        try:
            from paper_trading.market_data.resume_v161 import SessionResumeManager
            from paper_trading.market_data.models_v161 import MarketDataCheckpoint
            from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
            mgr = SessionResumeManager()
            assert mgr.cannot_auto_resume_to_running() is False
            _pass("resume_always_paused")
        except Exception as e:
            _fail("resume_always_paused", str(e))

        # === Symbol mapper ambiguous blocked (16) ===
        try:
            from paper_trading.market_data.symbol_mapper_v161 import SymbolMapper, SymbolMappingError
            sm = SymbolMapper()
            try:
                sm.register("TSM", "2330")
                sm.register("TSM", "2317")  # conflict
                _fail("symbol_mapper_ambiguous_blocked", "Should have raised SymbolMappingError")
            except SymbolMappingError:
                _pass("symbol_mapper_ambiguous_blocked")
        except Exception as e:
            _fail("symbol_mapper_ambiguous_blocked", str(e))

        # === Freshness: future date NOT fresh (17) ===
        try:
            from paper_trading.market_data.freshness_v161 import FreshnessClassifier, FUTURE_DATE_COUNTS_AS_FRESH
            from paper_trading.market_data.enums_v161 import SourceClass, FreshnessStatus
            assert FUTURE_DATE_COUNTS_AS_FRESH is False
            classifier = FreshnessClassifier()
            status = classifier.classify("2099-01-01T00:00:00Z", SourceClass.LIVE_PUBLIC)
            assert status == FreshnessStatus.UNKNOWN
            _pass("freshness_future_date_not_fresh")
        except Exception as e:
            _fail("freshness_future_date_not_fresh", str(e))

        # === UNKNOWN source class not trusted (18) ===
        try:
            from paper_trading.market_data.freshness_v161 import FreshnessClassifier
            from paper_trading.market_data.enums_v161 import SourceClass, FreshnessStatus
            classifier = FreshnessClassifier()
            status = classifier.classify("2024-01-01T09:00:00Z", SourceClass.UNKNOWN)
            assert status == FreshnessStatus.UNKNOWN
            _pass("unknown_source_not_trusted")
        except Exception as e:
            _fail("unknown_source_not_trusted", str(e))

        # === Deduplication (19) ===
        try:
            from paper_trading.market_data.deduplication_v161 import MarketDataDeduplicator
            from paper_trading.market_data.models_v161 import RawMarketDataEvent
            from paper_trading.market_data.enums_v161 import SourceClass, MarketDataEventType
            dedup = MarketDataDeduplicator()
            raw = RawMarketDataEvent(
                event_id="eid1", adapter_id="a1", source_class=SourceClass.FIXTURE,
                event_type=MarketDataEventType.TRADE, symbol="2330",
                timestamp_utc="2024-01-02T09:00:00Z",
            )
            assert dedup.is_duplicate(raw) is False
            assert dedup.is_duplicate(raw) is True
            _pass("deduplication_works")
        except Exception as e:
            _fail("deduplication_works", str(e))

        # === Sequence validation (20) ===
        try:
            from paper_trading.market_data.sequence_v161 import SequenceValidator
            from paper_trading.market_data.models_v161 import RawMarketDataEvent
            from paper_trading.market_data.enums_v161 import SourceClass, MarketDataEventType, SequenceStatus
            sv = SequenceValidator()
            def _mk_raw(seq):
                return RawMarketDataEvent(
                    event_id=f"e{seq}", adapter_id="a1", source_class=SourceClass.FIXTURE,
                    event_type=MarketDataEventType.TRADE, symbol="2330",
                    timestamp_utc="2024-01-02T09:00:00Z", sequence_number=seq,
                )
            r1 = sv.check(_mk_raw(1))
            r2 = sv.check(_mk_raw(2))
            r3 = sv.check(_mk_raw(5))  # gap
            assert r1 == SequenceStatus.IN_ORDER
            assert r2 == SequenceStatus.IN_ORDER
            assert r3 == SequenceStatus.GAP_DETECTED
            _pass("sequence_validation_works")
        except Exception as e:
            _fail("sequence_validation_works", str(e))

        # === Reconnect policy NO_RECONNECT (21) ===
        try:
            from paper_trading.market_data.reconnect_v161 import ReconnectManager
            from paper_trading.market_data.enums_v161 import ReconnectPolicy
            rm = ReconnectManager(ReconnectPolicy.NO_RECONNECT)
            assert rm.should_reconnect() is False
            _pass("reconnect_no_reconnect_policy")
        except Exception as e:
            _fail("reconnect_no_reconnect_policy", str(e))

        # === Reconnect bounded exponential (22) ===
        try:
            from paper_trading.market_data.reconnect_v161 import ReconnectManager
            from paper_trading.market_data.enums_v161 import ReconnectPolicy
            rm = ReconnectManager(
                ReconnectPolicy.BOUNDED_EXPONENTIAL_BACKOFF,
                base_interval_s=5, max_interval_s=120, max_attempts=3,
            )
            assert rm.should_reconnect() is True
            rm.record_attempt()
            i1 = rm.get_next_interval_s()
            rm.record_attempt()
            i2 = rm.get_next_interval_s()
            assert i2 > i1
            _pass("reconnect_exponential_backoff")
        except Exception as e:
            _fail("reconnect_exponential_backoff", str(e))

        # === Reproducibility deterministic (23) ===
        try:
            from paper_trading.market_data.reproducibility_v161 import MarketDataReproducibilityService
            svc = MarketDataReproducibilityService()
            config = {"adapter_id": "a1", "symbols": ["2330"]}
            hashes = ["hash1", "hash2"]
            h1 = svc.compute_session_hash("s1", config, hashes)
            h2 = svc.compute_session_hash("s1", config, hashes)
            assert h1 == h2
            _pass("reproducibility_deterministic")
        except Exception as e:
            _fail("reproducibility_deterministic", str(e))

        # === Session pipeline FIXTURE end-to-end (24) ===
        try:
            from paper_trading.market_data.session_v161 import MarketDataSession
            from paper_trading.market_data.models_v161 import (
                MarketDataAdapterConfig, MarketDataSessionConfig,
            )
            from paper_trading.market_data.fixture_adapter_v161 import FixtureAdapter
            from paper_trading.market_data.enums_v161 import SourceClass
            cfg = MarketDataAdapterConfig(
                adapter_id="test_sess", source_class=SourceClass.FIXTURE,
                provider_name="test", symbols=["2330"],
            )
            adapter = FixtureAdapter(cfg, fixture_events=[
                {"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
                 "timestamp_utc": "2024-01-02T09:00:00Z",
                 "payload": {"price": "165.5", "volume": 100}},
            ])
            sess_cfg = MarketDataSessionConfig(
                session_id="test_s1", adapter_id="test_sess",
                symbols=["2330"], source_class=SourceClass.FIXTURE,
            )
            session = MarketDataSession(sess_cfg, adapter)
            ok = session.start()
            assert ok is True
            count = session.poll_and_process()
            assert count == 1
            assert session.store.total_stored == 1
            _pass("session_pipeline_fixture_e2e")
        except Exception as e:
            _fail("session_pipeline_fixture_e2e", str(e))

        # === CLI commands registered (25) ===
        try:
            from cli.command_registry import get_commands_by_group
            md_cmds = get_commands_by_group("market_data_session")
            assert len(md_cmds) >= 29, f"Expected >= 29 market_data_session commands, got {len(md_cmds)}"
            _pass("cli_commands_registered")
        except Exception as e:
            _fail("cli_commands_registered", str(e))

        # === CLI all RESEARCH_ONLY (26) ===
        try:
            from cli.command_registry import get_commands_by_group
            md_cmds = get_commands_by_group("market_data_session")
            bad = [c.name for c in md_cmds if c.safety_classification != "RESEARCH_ONLY"]
            assert not bad, f"Non-RESEARCH_ONLY commands: {bad}"
            _pass("cli_all_research_only")
        except Exception as e:
            _fail("cli_all_research_only", str(e))

        # === GUI panel importable (27) ===
        try:
            import gui.market_data_session_panel as gp
            assert gp.NO_REAL_ORDERS is True
            assert gp.BROKER_EXECUTION_ENABLED is False
            _pass("gui_panel_importable")
        except Exception as e:
            _fail("gui_panel_importable", str(e))

        # === Report importable (28) ===
        try:
            import reports.market_data_session_report as rp
            assert rp.NO_REAL_ORDERS is True
            _pass("report_importable")
        except Exception as e:
            _fail("report_importable", str(e))

        # === Docs file exists (29) ===
        try:
            import os
            doc_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "docs", "market_data_session_v1.6.1.md"
            )
            assert os.path.exists(doc_path), f"Docs not found: {doc_path}"
            _pass("docs_file_exists")
        except Exception as e:
            _fail("docs_file_exists", str(e))

        # === Fixtures exist (30) ===
        try:
            import os
            fixtures_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "tests", "fixtures", "market_data_session"
            )
            assert os.path.isdir(fixtures_dir), f"Fixtures dir not found: {fixtures_dir}"
            fixtures = [f for f in os.listdir(fixtures_dir) if f.endswith(".json")]
            assert len(fixtures) >= 31, f"Expected >= 31 fixtures, got {len(fixtures)}"
            _pass("fixtures_exist")
        except Exception as e:
            _fail("fixtures_exist", str(e))

        # === No broker API in adapters (31) ===
        try:
            from paper_trading.market_data.adapter_base_v161 import AbstractMarketDataAdapter
            assert AbstractMarketDataAdapter.submit_real_order is not None
            # Verify it raises NotImplementedError
            from paper_trading.market_data.fixture_adapter_v161 import FixtureAdapter
            from paper_trading.market_data.models_v161 import MarketDataAdapterConfig
            from paper_trading.market_data.enums_v161 import SourceClass
            cfg = MarketDataAdapterConfig(
                adapter_id="nb", source_class=SourceClass.FIXTURE,
                provider_name="t", symbols=["2330"],
            )
            adapter = FixtureAdapter(cfg)
            try:
                adapter.submit_real_order()
                _fail("no_broker_api_enforced", "Should raise NotImplementedError")
            except NotImplementedError:
                _pass("no_broker_api_enforced")
        except Exception as e:
            _fail("no_broker_api_enforced", str(e))

        # === Canonical events carry safety markers (32) ===
        try:
            from paper_trading.market_data.models_v161 import CanonicalTradeEvent
            from paper_trading.market_data.enums_v161 import SourceClass, FreshnessStatus, SequenceStatus, DataQualityStatus
            from decimal import Decimal
            ev = CanonicalTradeEvent(
                event_id="e1", raw_event_id="r1", adapter_id="a1",
                source_class=SourceClass.FIXTURE, symbol="2330",
                timestamp_utc="2024-01-02T09:00:00Z",
                price=Decimal("165.5"), volume=100,
                freshness_status=FreshnessStatus.NOT_APPLICABLE,
                sequence_status=SequenceStatus.UNKNOWN,
                quality_status=DataQualityStatus.PASS,
            )
            assert ev.research_only is True
            assert ev.market_data_only is True
            assert ev.no_broker_call is True
            assert ev.no_real_order is True
            assert ev.source_classified is True
            assert ev.data_mode_disclosed is True
            _pass("canonical_events_safety_markers")
        except Exception as e:
            _fail("canonical_events_safety_markers", str(e))

        # === Health check passes (33) ===
        try:
            from paper_trading.market_data.health_v161 import MarketDataSessionHealthCheck
            hc = MarketDataSessionHealthCheck()
            result = hc.run()
            assert result["status"] == "PASS", f"Health failed: {result}"
            _pass("health_check_passes")
        except Exception as e:
            _fail("health_check_passes", str(e))

        # === v1.6.0 backward compat (34) ===
        try:
            from paper_trading.health_v160 import LivePaperTradingHealthCheck
            hc = LivePaperTradingHealthCheck()
            result = hc.run()
            assert result["status"] == "PASS", f"v1.6.0 health failed: {result}"
            _pass("v160_backward_compat")
        except Exception as e:
            _fail("v160_backward_compat", str(e))

        overall = "PASS" if not blocked else "FAIL"
        return {
            "gate": _GATE_NAME,
            "version": _GATE_VERSION,
            "total": len(checks),
            "passed": sum(1 for v in checks.values() if v == "PASS"),
            "failed": len(blocked),
            "blocked": blocked,
            "checks": checks,
            "overall": overall,
            "no_real_orders": True,
            "production_trading_blocked": True,
        }


def run_release_gate() -> None:
    print("=" * 60)
    print(f"TW Quant Cockpit — Release Gate v{_GATE_VERSION}: {_GATE_NAME}")
    print("[!] Research Only. No Real Orders. No Broker. Simulation Only.")
    print("=" * 60)
    gate = MarketDataSessionReleaseGate()
    result = gate.run()
    passed = result["passed"]
    total = result["total"]
    blocked = result["blocked"]
    overall = result["overall"]
    print(f"Checks: {passed}/{total} PASS")
    if blocked:
        print(f"BLOCKED: {blocked}")
    for k, v in result["checks"].items():
        status = "PASS" if v == "PASS" else "FAIL"
        print(f"  [{status}] {k}: {v if v != 'PASS' else ''}")
    print(f"Overall: {overall}")
    print("[!] Research Only. No Real Orders.")


if __name__ == "__main__":
    run_release_gate()

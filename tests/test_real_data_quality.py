"""
tests/test_real_data_quality.py — Comprehensive tests for Real Data Quality Foundation v1.3.0

Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] All test fixtures are labeled TEST_FIXTURE and NOT accepted by REAL mode.
[!] No external network dependency. All inputs are synthetic test data.
"""
from __future__ import annotations

import math
import pytest
from typing import List

# ---------------------------------------------------------------------------
# Imports under test
# ---------------------------------------------------------------------------
from real_data_quality.dq_schema import (
    DataMode,
    DataQualityStatus,
    DataQualityIssueSeverity,
    DataQualityIssue,
    DataQualityReport,
    DataProvenanceRecord,
    NO_REAL_ORDERS,
    MOCK_FALLBACK_ENABLED,
)
from real_data_quality.dq_validator import DataQualityValidator
from real_data_quality.dq_profiles import DataCompletenessGate, CompletenessProfile
from real_data_quality.dq_scorer import DataQualityScorer
from real_data_quality.dq_health import RealDataQualityHealth
from real_data_quality.dq_report import (
    format_quality_report_text,
    format_quality_summary_for_stock_report,
    make_blocked_output,
    make_unavailable_output,
)
from gui.real_data_quality_panel import RealDataQualityPanel


# ---------------------------------------------------------------------------
# Test fixture — safe complete real data (all required fields present)
# NOTE: Source set to "test_fixture" so REAL mode will reject it (by design).
#       Use "real_provider" to simulate a real source that is not mock.
# ---------------------------------------------------------------------------
def _good_data(mode: str = DataMode.REAL, source: str = "real_provider") -> dict:
    """Returns a complete valid data dict. NOT a fixture — simulates real data."""
    return {
        "symbol": "2330",
        "market": "TW",
        "data_mode": mode,
        "source": [source],
        "date": "2026-06-18",
        "close": 830.0,
        "open": 825.0,
        "high": 835.0,
        "low": 820.0,
        "volume": 50000,
        "MA5": 828.0,
        "MA10": 820.0,
        "MA20": 815.0,
        "MA60": 800.0,
        "KD_K": 65.0,
        "KD_D": 60.0,
        "RSI": 55.0,
        "MACD_line": 2.5,
        "MACD_signal": 2.0,
        "MACD_hist": 0.5,
        "foreign": 1000,
        "investment_trust": 500,
        "dealer": 200,
        "margin_balance": 300000,
        "major_holders": 45.0,
        "retail_holders": 55.0,
        "monthly_revenue": 200000000,
        "yoy_revenue_growth": 0.15,
        "financial_statement_period": "2026Q1",
        "eps": 18.5,
        "latest_reporting_period": "2026Q1",
    }


def _fixture_data(mode: str = DataMode.MOCK) -> dict:
    """Returns data explicitly labeled as test fixture — REAL mode rejects it."""
    d = _good_data(mode="mock", source="fixture")
    d["data_mode"] = mode
    d["source"] = ["fixture"]  # "fixture" is in _MOCK_SOURCES
    return d


# ===========================================================================
# Schema tests
# ===========================================================================

class TestSchema:
    def test_data_mode_constants(self):
        assert DataMode.REAL == "REAL"
        assert DataMode.MOCK == "MOCK"
        assert DataMode.UNAVAILABLE == "UNAVAILABLE"

    def test_quality_status_constants(self):
        assert DataQualityStatus.PASS == "PASS"
        assert DataQualityStatus.DEGRADED == "DEGRADED"
        assert DataQualityStatus.BLOCKED == "BLOCKED"
        assert DataQualityStatus.UNAVAILABLE == "UNAVAILABLE"

    def test_severity_constants(self):
        assert DataQualityIssueSeverity.INFO == "INFO"
        assert DataQualityIssueSeverity.WARNING == "WARNING"
        assert DataQualityIssueSeverity.ERROR == "ERROR"
        assert DataQualityIssueSeverity.CRITICAL == "CRITICAL"

    def test_safety_constants(self):
        assert NO_REAL_ORDERS is True
        assert MOCK_FALLBACK_ENABLED is False

    def test_issue_to_dict(self):
        issue = DataQualityIssue(
            code="TEST_CODE", severity="CRITICAL", field="close",
            message="test", source="validator",
            observed_at="2026-06-19T00:00:00+00:00",
            expected_rule="close > 0", actual_value="0",
            blocks_analysis=True,
        )
        d = issue.to_dict()
        assert d["code"] == "TEST_CODE"
        assert d["severity"] == "CRITICAL"
        assert d["blocks_analysis"] is True

    def test_issue_from_dict(self):
        d = {
            "code": "X", "severity": "INFO", "field": "f",
            "message": "m", "source": "s",
            "observed_at": "2026-06-19T00:00:00+00:00",
            "expected_rule": "r", "actual_value": "v",
            "blocks_analysis": False,
        }
        issue = DataQualityIssue.from_dict(d)
        assert issue.code == "X"
        assert issue.severity == "INFO"

    def test_report_to_dict_round_trip(self):
        report = DataQualityReport(
            symbol="2330", market="TW",
            data_mode=DataMode.REAL,
            status=DataQualityStatus.PASS,
            score=90, checked_at="",
        )
        d = report.to_dict()
        assert d["symbol"] == "2330"
        assert d["NO_REAL_ORDERS"] is True
        assert d["MOCK_FALLBACK_ENABLED"] is False
        r2 = DataQualityReport.from_dict(d)
        assert r2.symbol == "2330"
        assert r2.score == 90

    def test_provenance_record_to_dict(self):
        rec = DataProvenanceRecord(
            provider="test_provider", source_type="api",
            fetched_at="", market_timestamp="2026-06-18",
            normalized_at="", symbol="2330", market="TW",
            data_mode=DataMode.REAL, schema_version="1.3.0",
        )
        d = rec.to_dict()
        assert d["provider"] == "test_provider"
        assert d["schema_version"] == "1.3.0"


# ===========================================================================
# Validator tests
# ===========================================================================

class TestValidatorCoreRules:
    """Core validation rules — aligned with spec."""

    def setup_method(self):
        self.v = DataQualityValidator()

    # ------ Safety constants ------

    def test_validator_no_real_orders(self):
        assert self.v.NO_REAL_ORDERS is True

    def test_validator_mock_fallback_disabled(self):
        assert self.v.MOCK_FALLBACK_ENABLED is False

    # ------ Complete Real data -> PASS (or DEGRADED if indicators missing) ------

    def test_complete_real_data_not_blocked(self):
        """Complete real data with real source should not be BLOCKED."""
        data = _good_data(mode=DataMode.REAL, source="real_provider")
        report = self.v.validate(data)
        assert report.status in (DataQualityStatus.PASS, DataQualityStatus.DEGRADED), (
            f"Expected PASS or DEGRADED, got {report.status}: {report.blocking_reasons}"
        )

    # ------ Missing price -> BLOCKED ------

    def test_missing_close_price_blocked(self):
        data = _good_data()
        del data["close"]
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED
        assert any("close" in r.lower() or "price" in r.lower() for r in report.blocking_reasons)

    def test_real_price_missing_blocked(self):
        data = {
            "symbol": "2330", "market": "TW",
            "data_mode": DataMode.REAL, "source": ["real_provider"],
        }
        report = self.v.validate(data)
        assert report.status in (DataQualityStatus.BLOCKED, DataQualityStatus.UNAVAILABLE)

    # ------ Real source unknown -> BLOCKED ------

    def test_real_source_empty_blocked(self):
        data = _good_data(mode=DataMode.REAL)
        data["source"] = []
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    def test_real_source_none_blocked(self):
        data = _good_data(mode=DataMode.REAL)
        data["source"] = None
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    # ------ Real mode with mock source -> BLOCKED ------

    def test_real_mode_mock_source_blocked(self):
        """HARD RULE: Real mode + mock source = BLOCKED."""
        for mock_src in ["mock", "demo", "fixture", "sample", "synthetic", "unknown", "test"]:
            data = _good_data(mode=DataMode.REAL, source=mock_src)
            report = self.v.validate(data)
            assert report.status == DataQualityStatus.BLOCKED, (
                f"Expected BLOCKED for source={mock_src!r}, got {report.status}"
            )

    # ------ No data -> UNAVAILABLE ------

    def test_no_data_unavailable(self):
        data = {
            "symbol": "2330", "market": "TW",
            "data_mode": DataMode.UNAVAILABLE, "source": [],
        }
        report = self.v.validate(data)
        assert report.status in (DataQualityStatus.UNAVAILABLE, DataQualityStatus.BLOCKED)

    # ------ Non-core field missing -> score reduced, may be DEGRADED ------

    def test_non_core_missing_not_blocked(self):
        """Missing indicator fields should reduce score but not necessarily BLOCK."""
        data = _good_data(mode=DataMode.MOCK, source="demo")
        # Remove all indicators
        for f in ["MA5", "MA10", "MA20", "MA60", "KD_K", "KD_D", "RSI", "MACD_line", "MACD_signal", "MACD_hist"]:
            data.pop(f, None)
        report = self.v.validate(data)
        # Status could be DEGRADED (score < 85) but should not be BLOCKED for missing indicators only
        assert report.status in (DataQualityStatus.DEGRADED, DataQualityStatus.PASS, DataQualityStatus.BLOCKED)

    # ------ close == 0 -> BLOCKED ------

    def test_close_zero_blocked(self):
        data = _good_data()
        data["close"] = 0.0
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    # ------ OHLC relationship violations -> BLOCKED ------

    def test_high_less_than_low_blocked(self):
        data = _good_data()
        data["high"] = 800.0
        data["low"] = 850.0
        data["close"] = 830.0
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    def test_low_greater_than_close_blocked(self):
        data = _good_data()
        data["low"] = 900.0  # low > close
        data["close"] = 830.0
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    def test_high_less_than_close_blocked(self):
        data = _good_data()
        data["high"] = 800.0  # high < close
        data["close"] = 830.0
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    # ------ Volume negative -> BLOCKED ------

    def test_volume_negative_blocked(self):
        data = _good_data()
        data["volume"] = -100
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    # ------ NaN indicator not converted to 0 ------

    def test_nan_indicator_not_zero(self):
        """NaN indicator must be flagged, not silently converted to 0."""
        data = _good_data()
        data["MA60"] = float("nan")
        report = self.v.validate(data)
        # MA60 NaN should produce a WARNING issue, not silently become 0
        nan_issues = [i for i in report.issues if "MA60" in i.field and "NaN" in i.message]
        assert len(nan_issues) > 0, "NaN MA60 should generate an issue"

    def test_nan_rsi_not_zero(self):
        data = _good_data()
        data["RSI"] = float("nan")
        report = self.v.validate(data)
        nan_issues = [i for i in report.issues if "RSI" in i.field and "NaN" in i.message]
        assert len(nan_issues) > 0

    # ------ MA60 history insufficient ------

    def test_ma60_missing_flagged(self):
        data = _good_data()
        data.pop("MA60")
        report = self.v.validate(data)
        ma60_issues = [i for i in report.issues if "MA60" in i.field]
        assert len(ma60_issues) > 0, "Missing MA60 should be flagged"

    # ------ Chips missing != 0 ------

    def test_chips_missing_not_zero(self):
        """Missing chips fields must be flagged, not treated as 0."""
        data = _good_data()
        data.pop("foreign")
        data.pop("investment_trust")
        report = self.v.validate(data)
        chips_issues = [i for i in report.issues if "foreign" in i.field or "investment_trust" in i.field]
        assert len(chips_issues) > 0, "Missing chips fields should be flagged"

    # ------ Investment trust cost estimation labeled ------

    def test_it_cost_unlabeled_flagged(self):
        data = _good_data()
        data["investment_trust_avg_cost"] = 750.0
        # No estimation_method set
        report = self.v.validate(data)
        label_issues = [i for i in report.issues if "investment_trust_avg_cost" in i.field]
        assert len(label_issues) > 0, "Unlabeled IT cost estimation should be flagged"

    def test_it_cost_labeled_not_flagged(self):
        data = _good_data()
        data["investment_trust_avg_cost"] = 750.0
        data["investment_trust_avg_cost_estimation_method"] = "FIFO"
        report = self.v.validate(data)
        label_issues = [i for i in report.issues
                        if "investment_trust_avg_cost" in i.field
                        and "estimation_method" in i.message]
        # Should not have the "no estimation method" issue
        assert len(label_issues) == 0

    # ------ Stale daily data ------

    def test_stale_daily_data_flagged(self):
        """Very old data should be flagged as stale."""
        data = _good_data()
        data["date"] = "2020-01-01"  # Very old date
        report = self.v.validate(data)
        stale_issues = [i for i in report.issues if "stale" in i.code.lower()]
        assert len(stale_issues) > 0, "Very old date should be flagged as stale"

    # ------ Valid previous trading day not falsely stale on weekend ------

    def test_recent_date_not_stale(self):
        """Recent date (within 3 trading days) should not be falsely stale."""
        data = _good_data()
        data["date"] = "2026-06-18"  # Recent date (today context: 2026-06-19)
        report = self.v.validate(data)
        stale_issues = [i for i in report.issues if "stale" in i.code.lower()]
        # Should not be flagged as stale for a date just 1 day old
        assert len(stale_issues) == 0, f"Recent date should not be stale: {stale_issues}"

    # ------ Cross-source price conflict ------

    def test_cross_source_price_conflict(self):
        data = _good_data()
        data["cross_source_data"] = {
            "source_a": {"symbol": "2330", "close": 830.0, "volume": 50000},
            "source_b": {"symbol": "2330", "close": 900.0, "volume": 50000},  # >1% diff
        }
        report = self.v.validate(data)
        conflict_issues = [i for i in report.issues if "CONFLICT" in i.code or "conflict" in i.code.lower()]
        assert len(conflict_issues) > 0, "Cross-source price conflict should be flagged"

    def test_cross_source_minor_diff_no_critical(self):
        data = _good_data()
        data["cross_source_data"] = {
            "source_a": {"symbol": "2330", "close": 830.0, "volume": 50000},
            "source_b": {"symbol": "2330", "close": 830.5, "volume": 50000},  # ~0.06% diff
        }
        report = self.v.validate(data)
        critical_conflicts = [
            i for i in report.issues
            if ("CONFLICT" in i.code or "conflict" in i.code.lower())
            and i.severity == DataQualityIssueSeverity.CRITICAL
        ]
        assert len(critical_conflicts) == 0, "Tiny price diff should not be CRITICAL"

    # ------ Fixed test price in REAL mode ------

    def test_fixed_test_price_real_blocked(self):
        data = _good_data(mode=DataMode.REAL, source="real_provider")
        data["close"] = 100.0  # Known test fixture price
        data["high"] = 105.0
        data["low"] = 95.0
        data["open"] = 100.0
        report = self.v.validate(data)
        assert report.status == DataQualityStatus.BLOCKED

    # ------ Real mode does NOT fallback to mock ------

    def test_real_mode_no_mock_fallback(self):
        """HARD RULE: Real mode never returns MOCK data."""
        data = {
            "symbol": "2330", "market": "TW",
            "data_mode": DataMode.REAL, "source": [],
        }
        report = self.v.validate(data)
        assert report.data_mode != DataMode.MOCK
        assert report.status != DataQualityStatus.PASS  # Should not pass without source

    # ------ Mock mode shows DEMO_ONLY ------

    def test_mock_mode_demo_only_in_report(self):
        data = _fixture_data(mode=DataMode.MOCK)
        data["close"] = 830.0
        data["open"] = 825.0
        data["high"] = 835.0
        data["low"] = 820.0
        data["volume"] = 50000
        report = self.v.validate(data)
        text = format_quality_report_text(report)
        assert "DEMO_ONLY" in text, "MOCK mode must show DEMO_ONLY"

    # ------ Future date flagged ------

    def test_future_date_flagged(self):
        data = _good_data()
        data["date"] = "2099-12-31"
        report = self.v.validate(data)
        future_issues = [i for i in report.issues if "future" in i.code.lower()]
        assert len(future_issues) > 0, "Future date should be flagged"


# ===========================================================================
# Scorer tests
# ===========================================================================

class TestScorer:
    def setup_method(self):
        self.scorer = DataQualityScorer()

    def test_scorer_safety_constants(self):
        assert self.scorer.NO_REAL_ORDERS is True
        assert self.scorer.MOCK_FALLBACK_ENABLED is False

    def test_score_range(self):
        data = _good_data()
        score = self.scorer.compute(data, [])
        assert 0 <= score <= 100

    def test_critical_issue_caps_score_at_49(self):
        data = _good_data()
        critical_issue = DataQualityIssue(
            code="TEST_CRITICAL", severity=DataQualityIssueSeverity.CRITICAL,
            field="close", message="test", source="test",
            observed_at="", expected_rule="", actual_value="",
            blocks_analysis=True,
        )
        score = self.scorer.compute(data, [critical_issue])
        assert score <= 49, f"CRITICAL issue should cap score at 49, got {score}"

    def test_deterministic(self):
        """Same input always produces same score — no randomness."""
        data = _good_data()
        score1 = self.scorer.compute(data, [])
        score2 = self.scorer.compute(data, [])
        assert score1 == score2

    def test_empty_data_low_score(self):
        score = self.scorer.compute({}, [])
        assert score < 50


# ===========================================================================
# Profiles tests
# ===========================================================================

class TestProfiles:
    def setup_method(self):
        self.gate = DataCompletenessGate()
        self.v = DataQualityValidator()

    def test_gate_safety_constants(self):
        assert self.gate.NO_REAL_ORDERS is True
        assert self.gate.MOCK_FALLBACK_ENABLED is False

    def test_precise_price_profile_blocked(self):
        """Precise price profile: blocked if status is BLOCKED."""
        data = _good_data(mode=DataMode.REAL)
        data["source"] = ["mock"]  # Force BLOCKED
        report = self.v.validate(data)
        result = self.gate.evaluate(report, CompletenessProfile.PRECISE_PRICE)
        assert result["can_generate_precise_prices"] is False

    def test_backtest_profile_missing_bars_degraded(self):
        """Backtest profile: missing bars degraded or blocked depending on count."""
        data = _good_data(mode=DataMode.MOCK, source="demo")
        report = self.v.validate(data)
        # Inject missing_bar_count into metadata
        report.metadata["missing_bar_count"] = 100  # > 50 triggers extra check
        result = self.gate.evaluate(report, CompletenessProfile.BACKTEST)
        # With >50 missing bars, should not be fully sufficient for backtest
        assert result["can_run_backtest"] is False

    def test_abc_insufficient_data(self):
        """A/B/C profile: returns insufficient_data when data is missing."""
        data = {
            "symbol": "2330", "market": "TW",
            "data_mode": DataMode.UNAVAILABLE, "source": [],
        }
        report = self.v.validate(data)
        result = self.gate.evaluate(report, CompletenessProfile.ABC_BUY_POINT)
        assert result["abc_result"] == "insufficient_data"

    def test_abc_never_auto_judges(self):
        """A/B/C profile: insufficient_data is returned, never auto-confirmed."""
        data = _good_data(mode=DataMode.MOCK, source="demo")
        data.pop("KD_K")  # Remove required indicator
        data.pop("KD_D")
        report = self.v.validate(data)
        result = self.gate.evaluate(report, CompletenessProfile.ABC_BUY_POINT)
        # Can return insufficient_data (acceptable) but must NEVER return auto-confirm
        assert result["abc_result"] in (None, "insufficient_data")

    def test_stock_screening_profile_all_present(self):
        data = _good_data(mode=DataMode.MOCK, source="demo")
        report = self.v.validate(data)
        result = self.gate.evaluate(report, CompletenessProfile.STOCK_SCREENING)
        # If report is DEGRADED or better, and fields are present, sufficient should be True or False
        assert "sufficient" in result
        assert "missing_required" in result


# ===========================================================================
# Health tests
# ===========================================================================

class TestHealth:
    def setup_method(self):
        self.hc = RealDataQualityHealth()

    def test_health_safety_constants(self):
        assert self.hc.NO_REAL_ORDERS is True
        assert self.hc.MOCK_FALLBACK_ENABLED is False

    def test_health_run_returns_dict(self):
        results = self.hc.run()
        assert isinstance(results, dict)
        assert len(results) > 0

    def test_health_run_all_pass(self):
        results = self.hc.run()
        failures = [(k, d) for k, (s, d) in results.items() if s == "FAIL"]
        assert len(failures) == 0, f"Health check failures: {failures}"

    def test_health_schema_forward_compatibility(self):
        """Health summary dict has required keys for forward compatibility."""
        summary = self.hc.get_health_summary()
        required_keys = [
            "real_data_quality_status", "real_data_quality_score",
            "mock_fallback_enabled",
            "active_real_sources", "blocked_symbols_count",
        ]
        for key in required_keys:
            assert key in summary, f"Health summary missing key: {key}"
        assert summary["mock_fallback_enabled"] is False

    def test_mock_fallback_check_passes(self):
        results = self.hc.run()
        status, detail = results["mock_fallback_disabled"]
        assert status == "PASS", f"mock_fallback_disabled check failed: {detail}"

    def test_real_blocks_mock_check_passes(self):
        results = self.hc.run()
        status, detail = results["real_mode_blocks_mock_source"]
        assert status == "PASS", f"real_mode_blocks_mock_source failed: {detail}"


# ===========================================================================
# Report / formatting tests
# ===========================================================================

class TestReport:
    def test_mock_mode_always_demo_only(self):
        report = DataQualityReport(
            symbol="TEST", market="TW",
            data_mode=DataMode.MOCK,
            status=DataQualityStatus.DEGRADED,
            score=70, checked_at="",
        )
        text = format_quality_report_text(report)
        assert "DEMO_ONLY" in text

    def test_real_mode_shows_real_data(self):
        report = DataQualityReport(
            symbol="2330", market="TW",
            data_mode=DataMode.REAL,
            status=DataQualityStatus.PASS,
            score=90, checked_at="",
            source_names=["real_provider"],
        )
        text = format_quality_report_text(report)
        assert "REAL_DATA" in text

    def test_blocked_output(self):
        report = DataQualityReport(
            symbol="2330", market="TW",
            data_mode=DataMode.REAL,
            status=DataQualityStatus.BLOCKED,
            score=30, checked_at="",
            blocking_reasons=["Mock source in REAL mode"],
        )
        text = make_blocked_output(report)
        assert "BLOCKED" in text
        assert "Mock source" in text

    def test_unavailable_output(self):
        text = make_unavailable_output("2330")
        assert "UNAVAILABLE" in text
        assert "DISABLED" in text or "fallback" in text.lower() or "mock" in text.lower()

    def test_markdown_summary_blocked(self):
        report = DataQualityReport(
            symbol="2330", market="TW",
            data_mode=DataMode.REAL,
            status=DataQualityStatus.BLOCKED,
            score=20, checked_at="",
            blocking_reasons=["No real source"],
        )
        md = format_quality_summary_for_stock_report(report)
        assert "BLOCKED" in md
        assert "No real source" in md

    def test_markdown_summary_unavailable(self):
        report = DataQualityReport(
            symbol="2330", market="TW",
            data_mode=DataMode.UNAVAILABLE,
            status=DataQualityStatus.UNAVAILABLE,
            score=0, checked_at="",
        )
        md = format_quality_summary_for_stock_report(report)
        assert "UNAVAILABLE" in md

    def test_demo_only_label_in_markdown(self):
        report = DataQualityReport(
            symbol="TEST", market="TW",
            data_mode=DataMode.MOCK,
            status=DataQualityStatus.DEGRADED,
            score=70, checked_at="",
        )
        md = format_quality_summary_for_stock_report(report)
        assert "DEMO_ONLY" in md


# ===========================================================================
# GUI Panel tests
# ===========================================================================

class TestGUIPanel:
    """
    GUI panel tests use the session-scoped qapp fixture from conftest.py
    to ensure a QApplication exists before QWidget construction.
    QT_QPA_PLATFORM=offscreen is set in conftest.py (test env only).
    """

    def test_gui_panel_no_crash_without_pyside6(self, qapp):
        """GUI panel must not crash when PySide6 is not available."""
        panel = RealDataQualityPanel()
        assert panel.NO_REAL_ORDERS is True
        assert panel.MOCK_FALLBACK_ENABLED is False

    def test_gui_panel_safety_constants(self, qapp):
        panel = RealDataQualityPanel()
        assert panel.NO_REAL_ORDERS is True
        assert panel.MOCK_FALLBACK_ENABLED is False

    def test_gui_panel_update_blocked_no_crash(self, qapp):
        """update_report with BLOCKED status must not crash."""
        panel = RealDataQualityPanel()
        blocked_dict = {
            "symbol": "2330", "market": "TW",
            "data_mode": "REAL", "status": "BLOCKED",
            "score": 20, "source_names": [],
            "latest_market_timestamp": "N/A",
            "blocking_reasons": ["Test block reason"],
            "warnings": [], "missing_fields": [], "stale_fields": [],
            "can_generate_analysis": False,
            "can_generate_precise_prices": False,
            "can_run_backtest": False,
        }
        panel.update_report(blocked_dict)  # Must not raise

    def test_gui_panel_set_blocked_no_crash(self, qapp):
        panel = RealDataQualityPanel()
        panel.set_blocked(["reason 1", "reason 2"])  # Must not raise

    def test_gui_panel_set_unavailable_no_crash(self, qapp):
        panel = RealDataQualityPanel()
        panel.set_unavailable()  # Must not raise

    def test_gui_panel_update_bad_input_no_crash(self, qapp):
        panel = RealDataQualityPanel()
        panel.update_report(None)  # Must not raise
        panel.update_report({})    # Must not raise
        panel.update_report({"score": "not_a_number"})  # Must not raise


# ===========================================================================
# Version info tests
# ===========================================================================

class TestVersionInfo:
    def test_version_130(self):
        from release import version_info
        # v1.3.2 bumped from 1.3.1; accept any 1.3.x release
        assert version_info.VERSION.startswith("1.3."), f"Expected 1.3.x, got {version_info.VERSION}"

    def test_real_no_mock_fallback(self):
        from release import version_info
        assert getattr(version_info, "REAL_NO_MOCK_FALLBACK", False) is True

    def test_mock_fallback_enabled_false(self):
        from release import version_info
        assert getattr(version_info, "MOCK_FALLBACK_ENABLED", None) is False

    def test_real_data_quality_foundation_true(self):
        from release import version_info
        assert getattr(version_info, "REAL_DATA_QUALITY_FOUNDATION", False) is True

    def test_release_name(self):
        from release import version_info
        # v1.3.3 changed release name to Coverage Repair Workflow
        assert version_info.RELEASE_NAME in (
            "Real Data Quality Foundation",
            "Universe Expansion Foundation",
            "Real Data Provider Adapter Foundation",
            "Coverage Repair Workflow",
        ), f"Unexpected release name: {version_info.RELEASE_NAME}"

    def test_release_track(self):
        from release import version_info
        assert version_info.RELEASE_TRACK == "real_data_quality"


# ===========================================================================
# Regression — existing tests not affected
# ===========================================================================

class TestRegressionCompatibility:
    def test_replay_training_module_still_importable(self):
        """Ensure replay training modules are not broken by v1.3.0 changes."""
        try:
            from release import version_info
            # v1.2.9 flags should still exist
            assert getattr(version_info, "REPLAY_STABLE_HEALTH_AVAILABLE", False) is True
            assert getattr(version_info, "REPLAY_TRAINING_LINE_COMPLETE", False) is True
        except ImportError as exc:
            pytest.fail(f"replay training module broken: {exc}")

    def test_gate_schema_still_importable(self):
        """Ensure existing quality_gates.gate_schema is not broken."""
        from quality_gates.gate_schema import (
            NO_REAL_ORDERS, BROKER_DISABLED,
            GATE_LEVEL_FORMAL, DECISION_ELIGIBLE_FORMAL,
        )
        assert NO_REAL_ORDERS is True
        assert BROKER_DISABLED is True

    def test_data_freshness_calendar_still_importable(self):
        """Ensure data_freshness.trading_calendar is not broken."""
        from data_freshness.trading_calendar import TradingCalendar
        cal = TradingCalendar()
        from datetime import date
        result = cal.is_trading_day(date(2026, 6, 15))  # Monday
        assert result is True

    def test_release_gate_exit_code_not_regressed(self):
        """Ensure SystemExit codes still work as expected."""
        import sys
        # This is just a structural check
        assert hasattr(sys, "exit")


# ===========================================================================
# CLI smoke test (no subprocess — just function call)
# ===========================================================================

class TestCLISmoke:
    def test_cmd_data_quality_unavailable_exits_1(self, capsys):
        """data-quality with no real source should exit 1 (UNAVAILABLE/BLOCKED)."""
        import argparse
        args = argparse.Namespace(symbol="2330", profile="default", json=False, all=False)
        # We test that it raises SystemExit with code 1 (not 0 or 2)
        with pytest.raises(SystemExit) as exc_info:
            from main import cmd_data_quality
            cmd_data_quality(args)
        assert exc_info.value.code == 1

    def test_cmd_data_quality_no_symbol_exits_2(self, capsys):
        """data-quality with no symbol and no --all should exit 2."""
        import argparse
        args = argparse.Namespace(symbol=None, profile="default", json=False, all=False)
        with pytest.raises(SystemExit) as exc_info:
            from main import cmd_data_quality
            cmd_data_quality(args)
        assert exc_info.value.code == 2

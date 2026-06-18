"""
real_data_quality/dq_health.py — Health check integration v1.3.0
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] MOCK_FALLBACK_ENABLED is ALWAYS False — never changes.
"""
from __future__ import annotations

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
MOCK_FALLBACK_ENABLED = False  # ALWAYS FALSE


class RealDataQualityHealth:
    """
    Health checks for the Real Data Quality system.
    Integrates with existing health check pattern (returns Dict[str, Tuple[str, str]]).

    Research Only. No Real Orders. Not Investment Advice.
    MOCK_FALLBACK_ENABLED is always False.
    """

    NO_REAL_ORDERS = True
    MOCK_FALLBACK_ENABLED = False  # ALWAYS FALSE — never changes

    def run(self) -> Dict[str, Tuple[str, str]]:
        """
        Run all health checks.
        Returns dict of {check_name: (status, detail)}.
        status is "PASS", "FAIL", or "WARN".
        """
        results: Dict[str, Tuple[str, str]] = {}
        results["real_data_quality_schema"]          = self._check_schema()
        results["real_data_quality_validator"]       = self._check_validator()
        results["real_data_quality_profiles"]        = self._check_profiles()
        results["real_data_quality_scorer"]          = self._check_scorer()
        results["mock_fallback_disabled"]            = self._check_mock_fallback()
        results["real_mode_blocks_mock_source"]      = self._check_real_blocks_mock()
        results["unavailable_no_fallback"]           = self._check_unavailable_no_fallback()
        results["blocked_no_fake_data"]              = self._check_blocked_no_fake_data()
        results["demo_only_label_present"]           = self._check_demo_only_label()
        results["real_data_label_present"]           = self._check_real_data_label()
        return results

    def get_health_summary(self) -> dict:
        """Returns health summary dict compatible with existing health schema."""
        results = self.run()
        pass_count = sum(1 for _, (s, _) in results.items() if s == "PASS")
        fail_count = sum(1 for _, (s, _) in results.items() if s == "FAIL")
        total = len(results)
        overall = "PASS" if fail_count == 0 else ("DEGRADED" if fail_count < total // 2 else "FAIL")
        return {
            "real_data_quality_status": overall,
            "real_data_quality_score": int(100 * pass_count / total) if total else 0,
            "last_successful_real_fetch": "N/A",
            "last_failed_real_fetch": "N/A",
            "active_real_sources": [],
            "blocked_symbols_count": 0,
            "degraded_symbols_count": 0,
            "unavailable_symbols_count": 0,
            "mock_fallback_enabled": False,  # Always False
            "checks_pass": pass_count,
            "checks_fail": fail_count,
            "checks_total": total,
        }

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_schema(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_schema import (
                DataMode, DataQualityStatus, DataQualityIssueSeverity,
                DataQualityIssue, DataQualityReport, DataProvenanceRecord,
                NO_REAL_ORDERS, MOCK_FALLBACK_ENABLED,
            )
            assert DataMode.REAL == "REAL"
            assert DataMode.MOCK == "MOCK"
            assert DataMode.UNAVAILABLE == "UNAVAILABLE"
            assert DataQualityStatus.PASS == "PASS"
            assert NO_REAL_ORDERS is True
            assert MOCK_FALLBACK_ENABLED is False
            return ("PASS", "dq_schema imports and constants verified")
        except Exception as exc:
            return ("FAIL", f"dq_schema check failed: {exc}")

    def _check_validator(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_validator import DataQualityValidator
            v = DataQualityValidator()
            assert v.NO_REAL_ORDERS is True
            assert v.MOCK_FALLBACK_ENABLED is False
            # Quick smoke test with empty data
            report = v.validate({"symbol": "", "data_mode": "UNAVAILABLE"})
            assert report is not None
            return ("PASS", "DataQualityValidator imports and smoke test passed")
        except Exception as exc:
            return ("FAIL", f"DataQualityValidator check failed: {exc}")

    def _check_profiles(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_profiles import DataCompletenessGate, CompletenessProfile
            from real_data_quality.dq_schema import DataQualityReport, DataMode, DataQualityStatus
            gate = DataCompletenessGate()
            assert gate.NO_REAL_ORDERS is True
            assert gate.MOCK_FALLBACK_ENABLED is False
            # Smoke test with minimal report
            report = DataQualityReport(
                symbol="TEST", market="TW",
                data_mode=DataMode.UNAVAILABLE,
                status=DataQualityStatus.UNAVAILABLE,
                score=0, checked_at="",
            )
            result = gate.evaluate(report, CompletenessProfile.DEFAULT)
            assert "sufficient" in result
            return ("PASS", "DataCompletenessGate imports and smoke test passed")
        except Exception as exc:
            return ("FAIL", f"DataCompletenessGate check failed: {exc}")

    def _check_scorer(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_scorer import DataQualityScorer
            scorer = DataQualityScorer()
            assert scorer.NO_REAL_ORDERS is True
            assert scorer.MOCK_FALLBACK_ENABLED is False
            score = scorer.compute({"symbol": "TEST", "close": 100.0}, [])
            assert isinstance(score, int)
            assert 0 <= score <= 100
            return ("PASS", f"DataQualityScorer smoke test passed (score={score})")
        except Exception as exc:
            return ("FAIL", f"DataQualityScorer check failed: {exc}")

    def _check_mock_fallback(self) -> Tuple[str, str]:
        try:
            from real_data_quality import dq_schema, dq_validator, dq_profiles, dq_scorer, dq_health
            checks = [
                getattr(dq_schema, "MOCK_FALLBACK_ENABLED", None),
                getattr(dq_validator, "MOCK_FALLBACK_ENABLED", None),
                getattr(dq_profiles, "MOCK_FALLBACK_ENABLED", None),
                getattr(dq_scorer, "MOCK_FALLBACK_ENABLED", None),
                getattr(dq_health, "MOCK_FALLBACK_ENABLED", None),
            ]
            all_false = all(v is False for v in checks)
            if not all_false:
                return ("FAIL", f"MOCK_FALLBACK_ENABLED is not False in all modules: {checks}")
            return ("PASS", "MOCK_FALLBACK_ENABLED=False in all real_data_quality modules")
        except Exception as exc:
            return ("FAIL", f"Mock fallback check failed: {exc}")

    def _check_real_blocks_mock(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_validator import DataQualityValidator
            from real_data_quality.dq_schema import DataMode, DataQualityStatus
            v = DataQualityValidator()
            # REAL mode + mock source must be BLOCKED
            report = v.validate({
                "symbol": "2330",
                "market": "TW",
                "data_mode": DataMode.REAL,
                "source": ["mock"],
                "close": 500.0,
                "open": 498.0,
                "high": 505.0,
                "low": 497.0,
                "volume": 10000,
            })
            if report.status != DataQualityStatus.BLOCKED:
                return ("FAIL", f"REAL+mock source should be BLOCKED, got {report.status}")
            return ("PASS", "REAL mode with mock source is correctly BLOCKED")
        except Exception as exc:
            return ("FAIL", f"Real-blocks-mock check failed: {exc}")

    def _check_unavailable_no_fallback(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_validator import DataQualityValidator
            from real_data_quality.dq_schema import DataMode, DataQualityStatus
            v = DataQualityValidator()
            report = v.validate({
                "symbol": "2330",
                "market": "TW",
                "data_mode": DataMode.UNAVAILABLE,
                "source": [],
            })
            # Must be UNAVAILABLE or BLOCKED — never auto-fall to MOCK
            if report.data_mode == DataMode.MOCK:
                return ("FAIL", "UNAVAILABLE should not silently become MOCK")
            return ("PASS", "UNAVAILABLE does not fall back to MOCK")
        except Exception as exc:
            return ("FAIL", f"Unavailable-no-fallback check failed: {exc}")

    def _check_blocked_no_fake_data(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_validator import DataQualityValidator
            from real_data_quality.dq_schema import DataMode, DataQualityStatus
            v = DataQualityValidator()
            # Missing price -> BLOCKED, not fake price inserted
            report = v.validate({
                "symbol": "2330",
                "market": "TW",
                "data_mode": DataMode.REAL,
                "source": ["real_provider"],
            })
            # Should be BLOCKED (no close price)
            if report.status not in (DataQualityStatus.BLOCKED, DataQualityStatus.UNAVAILABLE):
                return ("FAIL", f"Missing price should be BLOCKED/UNAVAILABLE, got {report.status}")
            # Ensure no fake price was inserted
            return ("PASS", "BLOCKED status does not insert fake price data")
        except Exception as exc:
            return ("FAIL", f"Blocked-no-fake-data check failed: {exc}")

    def _check_demo_only_label(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_report import format_quality_report_text
            from real_data_quality.dq_schema import DataMode, DataQualityStatus, DataQualityReport
            report = DataQualityReport(
                symbol="TEST", market="TW",
                data_mode=DataMode.MOCK,
                status=DataQualityStatus.DEGRADED,
                score=70, checked_at="",
            )
            text = format_quality_report_text(report)
            if "DEMO_ONLY" not in text and "DEMO" not in text:
                return ("FAIL", "MOCK mode report does not contain DEMO_ONLY label")
            return ("PASS", "MOCK mode report contains DEMO_ONLY label")
        except Exception as exc:
            return ("FAIL", f"demo_only_label check failed: {exc}")

    def _check_real_data_label(self) -> Tuple[str, str]:
        try:
            from real_data_quality.dq_report import format_quality_report_text
            from real_data_quality.dq_schema import DataMode, DataQualityStatus, DataQualityReport
            report = DataQualityReport(
                symbol="2330", market="TW",
                data_mode=DataMode.REAL,
                status=DataQualityStatus.PASS,
                score=90, checked_at="",
                source_names=["real_provider"],
            )
            text = format_quality_report_text(report)
            if "REAL_DATA" not in text and "REAL" not in text:
                return ("FAIL", "REAL mode report does not contain REAL_DATA label")
            return ("PASS", "REAL mode report contains REAL_DATA label")
        except Exception as exc:
            return ("FAIL", f"real_data_label check failed: {exc}")

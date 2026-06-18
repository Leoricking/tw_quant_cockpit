"""
real_data_quality/dq_profiles.py — Data completeness profiles v1.3.0
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] A/B/C profile never auto-judges true/false on insufficient data -> returns "insufficient_data".
"""
from __future__ import annotations

import logging
from typing import Dict, List

from real_data_quality.dq_schema import DataQualityReport, DataQualityStatus

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
MOCK_FALLBACK_ENABLED = False


# ---------------------------------------------------------------------------
# Profile names
# ---------------------------------------------------------------------------
class CompletenessProfile:
    """Data completeness profile name constants."""
    STOCK_SCREENING  = "stock_screening"
    PRECISE_PRICE    = "precise_price"
    BACKTEST         = "backtest"
    ABC_BUY_POINT    = "abc_buy_point"
    DEFAULT          = "default"


# ---------------------------------------------------------------------------
# Profile requirement definitions
# ---------------------------------------------------------------------------
_PROFILE_REQUIREMENTS: Dict[str, Dict] = {
    CompletenessProfile.STOCK_SCREENING: {
        "required_fields": [
            "symbol", "close", "open", "high", "low", "volume",
            "MA5", "MA10", "MA20",
        ],
        "required_for_analysis": True,
        "required_for_precise_prices": False,
        "required_for_backtest": False,
        "description": (
            "Stock screening: needs symbol, latest valid price, daily OHLCV, "
            "MA5/MA10/MA20, basic volume. Fundamentals and institutional data recommended."
        ),
    },
    CompletenessProfile.PRECISE_PRICE: {
        "required_fields": [
            "symbol", "close", "open", "high", "low", "volume",
            "date", "source",
            "MA5", "MA10", "MA20", "MA60",
        ],
        "required_for_analysis": True,
        "required_for_precise_prices": True,
        "required_for_backtest": False,
        "description": (
            "Precise price: current price, latest date, OHLCV, MA5/MA10/MA20/MA60, "
            "source, timestamp. Source must be identified and non-mock."
        ),
        "extra_checks": ["source_must_be_real"],
    },
    CompletenessProfile.BACKTEST: {
        "required_fields": [
            "symbol", "close", "open", "high", "low", "volume",
            "date",
        ],
        "required_for_analysis": True,
        "required_for_precise_prices": False,
        "required_for_backtest": True,
        "description": (
            "Backtest: continuous OHLCV, adjusted status, trading dates, "
            "corporate action handling, lookahead-safe timestamp, strategy input availability."
        ),
        "extra_checks": ["no_duplicate_bars", "no_missing_bars_critical"],
    },
    CompletenessProfile.ABC_BUY_POINT: {
        "required_fields": [
            "symbol", "close", "open", "high", "low", "volume",
            "MA5", "MA10", "MA20",
            "KD_K", "KD_D",
        ],
        "required_for_analysis": True,
        "required_for_precise_prices": False,
        "required_for_backtest": False,
        "description": (
            "A/B/C buy point: MA5/MA10/MA20, volume, KD, institutional direction, "
            "price history, breakout/pullback reference levels. "
            "Never auto-judges buy point on insufficient data."
        ),
        "extra_checks": ["abc_insufficient_data_guard"],
    },
    CompletenessProfile.DEFAULT: {
        "required_fields": ["symbol"],
        "required_for_analysis": False,
        "required_for_precise_prices": False,
        "required_for_backtest": False,
        "description": "Default profile: minimal validation only.",
    },
}


class DataCompletenessGate:
    """
    Evaluates whether a DataQualityReport meets the minimum requirements
    for a given completeness profile.

    Research Only. No Real Orders. Not Investment Advice.
    A/B/C profile never auto-judges buy point on insufficient data.
    """

    NO_REAL_ORDERS = True
    MOCK_FALLBACK_ENABLED = False

    def evaluate(self, report: DataQualityReport, profile: str) -> dict:
        """
        Returns:
        {
            profile: str,
            sufficient: bool,
            missing_required: List[str],
            reason: str,
            can_generate_analysis: bool,
            can_generate_precise_prices: bool,
            can_run_backtest: bool,
            abc_result: str or None,  # "insufficient_data" if abc profile and not enough data
        }
        """
        try:
            return self._do_evaluate(report, profile)
        except Exception as exc:
            logger.error("DataCompletenessGate.evaluate failed: %s", exc, exc_info=True)
            return {
                "profile": profile,
                "sufficient": False,
                "missing_required": [],
                "reason": f"Internal error: {exc}",
                "can_generate_analysis": False,
                "can_generate_precise_prices": False,
                "can_run_backtest": False,
                "abc_result": None,
            }

    def _do_evaluate(self, report: DataQualityReport, profile: str) -> dict:
        spec = _PROFILE_REQUIREMENTS.get(profile, _PROFILE_REQUIREMENTS[CompletenessProfile.DEFAULT])

        # Collect all available fields from the report
        available = _collect_available_fields(report)

        required = spec.get("required_fields", [])
        missing_required = [f for f in required if f not in available]

        # A/B/C profile: never auto-judge, return insufficient_data if data not sufficient
        abc_result = None
        if profile == CompletenessProfile.ABC_BUY_POINT:
            if missing_required or report.status in (DataQualityStatus.BLOCKED, DataQualityStatus.UNAVAILABLE):
                abc_result = "insufficient_data"

        sufficient = (
            len(missing_required) == 0
            and report.status not in (DataQualityStatus.BLOCKED, DataQualityStatus.UNAVAILABLE)
        )

        # Extra checks
        extra_checks = spec.get("extra_checks", [])
        extra_reasons = []

        if "source_must_be_real" in extra_checks:
            if not report.source_names or all(
                s.lower() in {"mock", "demo", "fixture", "sample", "synthetic", "unknown", "test"}
                for s in report.source_names
            ):
                sufficient = False
                extra_reasons.append("Source must be identified real data source for precise prices")

        if "no_duplicate_bars" in extra_checks:
            # Check metadata for duplicate bar count
            dup_count = report.metadata.get("duplicate_bar_count", 0)
            if dup_count and int(dup_count) > 0:
                sufficient = False
                extra_reasons.append(f"Backtest blocked: {dup_count} duplicate bars detected")

        if "no_missing_bars_critical" in extra_checks:
            # Check metadata for missing bar count
            missing_count = report.metadata.get("missing_bar_count", 0)
            if missing_count and int(missing_count) > 50:  # >50 missing bars is critical
                sufficient = False
                extra_reasons.append(f"Backtest degraded: {missing_count} missing bars")

        # Derive capability flags
        can_analysis = (
            sufficient
            and spec.get("required_for_analysis", False)
            and report.can_generate_analysis
        ) or (
            not spec.get("required_for_analysis", True)
            and sufficient
        )

        can_precise = (
            sufficient
            and spec.get("required_for_precise_prices", False)
            and report.can_generate_precise_prices
        )

        can_backtest = (
            sufficient
            and spec.get("required_for_backtest", False)
            and report.can_run_backtest
        )

        reason_parts = []
        if missing_required:
            reason_parts.append(f"Missing required fields: {missing_required}")
        if extra_reasons:
            reason_parts.extend(extra_reasons)
        if report.status in (DataQualityStatus.BLOCKED, DataQualityStatus.UNAVAILABLE):
            reason_parts.append(f"Report status is {report.status}")
        reason = "; ".join(reason_parts) if reason_parts else (
            "All required fields present" if sufficient else "Insufficient data"
        )

        return {
            "profile": profile,
            "sufficient": sufficient,
            "missing_required": missing_required,
            "reason": reason,
            "can_generate_analysis": bool(can_analysis),
            "can_generate_precise_prices": bool(can_precise),
            "can_run_backtest": bool(can_backtest),
            "abc_result": abc_result,
        }


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _collect_available_fields(report: DataQualityReport) -> set:
    """Collect field names that are considered available in the report."""
    available = set()

    # Symbol and market always available if non-empty
    if report.symbol:
        available.add("symbol")
    if report.market:
        available.add("market")
    if report.source_names:
        available.add("source")
    if report.latest_market_timestamp:
        available.add("date")

    # Infer from issues: fields NOT in missing_fields are considered available
    missing_set = set(report.missing_fields)

    # Price fields: infer from blocking reasons and issues
    price_fields = ["close", "open", "high", "low", "volume"]
    indicator_fields = [
        "MA5", "MA10", "MA20", "MA60",
        "KD_K", "KD_D", "RSI",
        "MACD_line", "MACD_signal", "MACD_hist",
    ]
    chips_fields = ["foreign", "investment_trust", "dealer", "margin_balance", "major_holders", "retail_holders"]
    fund_fields = ["monthly_revenue", "yoy_revenue_growth", "financial_statement_period", "eps", "latest_reporting_period"]

    # Add fields not reported as missing and not in invalid_fields for critical issues
    all_checked = price_fields + indicator_fields + chips_fields + fund_fields
    critical_invalid = set(report.invalid_fields) if report.status == DataQualityStatus.BLOCKED else set()

    for f in all_checked:
        if f not in missing_set and f not in critical_invalid:
            # Additionally check: not in issues with CRITICAL severity
            is_critical_issue = any(
                iss.field == f and iss.severity == "CRITICAL"
                for iss in report.issues
            )
            if not is_critical_issue:
                available.add(f)

    return available

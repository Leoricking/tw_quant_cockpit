"""
real_data_quality/dq_validator.py — Centralized quality validator v1.3.0
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] Single entry point for all data quality checks. All callers share this logic.
[!] Real mode with mock source -> BLOCKED (never silently accepted).
[!] No mock fallback. No random prices. No synthetic data posed as Real.
"""
from __future__ import annotations

import logging
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

from real_data_quality.dq_schema import (
    DataMode,
    DataQualityStatus,
    DataQualityIssueSeverity,
    DataQualityIssue,
    DataQualityReport,
)
from real_data_quality.dq_scorer import DataQualityScorer

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
MOCK_FALLBACK_ENABLED = False   # ALWAYS FALSE — never changes

# ---------------------------------------------------------------------------
# Freshness policy thresholds (in hours, approximate)
# ---------------------------------------------------------------------------
_FRESHNESS_POLICY: Dict[str, int] = {
    "intraday":              1,       # 15 min stale -> 1h threshold
    "daily_price":           26,      # 1 trading day (generous for timezone)
    "institutional":         26,
    "margin":                26,
    "revenue":               744,     # ~1 month
    "financial_statement":   2208,    # ~1 quarter (92 days)
    "shareholder":           336,     # 2 weeks
    "etf_constituent":       168,     # 1 week
    "macro":                 26,
    "futures":               26,
}


class DataQualityValidator:
    """
    Single entry point for all data quality checks. All callers share this logic.

    NO_REAL_ORDERS = True
    MOCK_FALLBACK_ENABLED = False

    Data dict keys:
      symbol, market, data_mode, source (list or str),
      price: open, high, low, close, volume, date,
      indicators: MA5, MA10, MA20, MA60, KD_K, KD_D, RSI,
                  MACD_line, MACD_signal, MACD_hist,
      chips: foreign, investment_trust, dealer, margin_balance,
             major_holders, retail_holders, investment_trust_avg_cost,
      fundamentals: monthly_revenue, yoy_revenue_growth,
                    financial_statement_period, eps, latest_reporting_period,
      cross_source_data: optional {source_name: {close, volume, ...}}
    """

    NO_REAL_ORDERS = True
    MOCK_FALLBACK_ENABLED = False

    # Sources that indicate mock/demo/fixture data
    _MOCK_SOURCES = frozenset({
        "mock", "demo", "fixture", "sample", "synthetic", "unknown", "test",
    })

    # Fixed test prices suspicious in REAL mode
    _FIXED_TEST_PRICES = frozenset({100.0, 100, 0.0, 1.0, 999.0, 9999.0})

    def __init__(self):
        self._scorer = DataQualityScorer()

    def validate(self, data: dict, profile: str = "default") -> DataQualityReport:
        """
        Main validation entry point.
        Returns DataQualityReport with full quality assessment.
        Never raises on bad input — always returns a valid report.
        """
        try:
            return self._do_validate(data, profile)
        except Exception as exc:
            logger.error("DataQualityValidator.validate failed: %s", exc, exc_info=True)
            return DataQualityReport(
                symbol=str(data.get("symbol", "")),
                market=str(data.get("market", "")),
                data_mode=DataMode.UNAVAILABLE,
                status=DataQualityStatus.UNAVAILABLE,
                score=0,
                checked_at="",
                blocking_reasons=[f"Validator internal error: {exc}"],
            )

    def _do_validate(self, data: dict, profile: str) -> DataQualityReport:
        issues: List[DataQualityIssue] = []
        blocking_reasons: List[str] = []
        warnings: List[str] = []

        # 1. Identification
        self._check_identification(data, issues, blocking_reasons)

        # 2. Price data
        self._check_price_data(data, issues, blocking_reasons)

        # 3. Freshness
        self._check_freshness(data, issues, warnings)

        # 4. Indicators
        self._check_indicators(data, issues, warnings)

        # 5. Chips
        self._check_chips(data, issues, warnings)

        # 6. Fundamentals
        self._check_fundamentals(data, issues, warnings)

        # 7. Cross-source consistency
        self._check_cross_source(data, issues, blocking_reasons)

        # Compute score and status
        score = self._scorer.compute(data, issues)
        status = self._derive_status(data, issues, score, blocking_reasons)

        # Derive capability flags
        has_critical = any(
            iss.severity == DataQualityIssueSeverity.CRITICAL for iss in issues
        )
        can_analysis = status in (DataQualityStatus.PASS, DataQualityStatus.DEGRADED)
        can_precise  = status == DataQualityStatus.PASS and not has_critical
        can_backtest = status in (DataQualityStatus.PASS, DataQualityStatus.DEGRADED) and not has_critical

        # Collect field categories
        missing_fields = [iss.field for iss in issues if "missing" in iss.code.lower()]
        stale_fields   = [iss.field for iss in issues if "stale" in iss.code.lower()]
        invalid_fields = [iss.field for iss in issues
                         if iss.severity in (DataQualityIssueSeverity.ERROR, DataQualityIssueSeverity.CRITICAL)
                         and "missing" not in iss.code.lower()
                         and "stale" not in iss.code.lower()]
        inconsistent_fields = [iss.field for iss in issues if "inconsist" in iss.code.lower() or "conflict" in iss.code.lower()]

        # Source names
        raw_source = data.get("source", [])
        if isinstance(raw_source, str):
            source_names = [raw_source] if raw_source else []
        else:
            source_names = list(raw_source) if raw_source else []

        return DataQualityReport(
            symbol=str(data.get("symbol", "")),
            market=str(data.get("market", "")),
            data_mode=str(data.get("data_mode", DataMode.UNAVAILABLE)),
            status=status,
            score=score,
            checked_at="",
            source_names=source_names,
            latest_market_timestamp=str(data.get("date", "") or data.get("latest_market_timestamp", "")),
            missing_fields=missing_fields,
            stale_fields=stale_fields,
            invalid_fields=invalid_fields,
            inconsistent_fields=inconsistent_fields,
            issues=issues,
            blocking_reasons=blocking_reasons,
            warnings=warnings,
            can_generate_analysis=can_analysis,
            can_generate_precise_prices=can_precise,
            can_run_backtest=can_backtest,
            metadata={
                "profile": profile,
                "NO_REAL_ORDERS": True,
                "MOCK_FALLBACK_ENABLED": False,
            },
        )

    # ------------------------------------------------------------------
    # Check 1: Identification
    # ------------------------------------------------------------------
    def _check_identification(self, data: dict, issues: List[DataQualityIssue],
                              blocking_reasons: List[str]) -> None:
        symbol = data.get("symbol", "")
        market = data.get("market", "")
        data_mode = data.get("data_mode", DataMode.UNAVAILABLE)
        source = data.get("source", [])
        timestamp = data.get("date", "") or data.get("latest_market_timestamp", "")

        if source is None:
            source = []
        if isinstance(source, str):
            source = [source] if source else []

        if not symbol:
            issues.append(_make_issue(
                code="ID_SYMBOL_MISSING",
                severity=DataQualityIssueSeverity.CRITICAL,
                field="symbol",
                message="Symbol is empty or missing",
                source="validator",
                expected_rule="symbol must be non-empty string",
                actual_value=repr(symbol),
                blocks_analysis=True,
            ))
            blocking_reasons.append("Symbol missing")

        if not market:
            issues.append(_make_issue(
                code="ID_MARKET_MISSING",
                severity=DataQualityIssueSeverity.WARNING,
                field="market",
                message="Market identifier is empty or missing",
                source="validator",
                expected_rule="market must be non-empty string",
                actual_value=repr(market),
                blocks_analysis=False,
            ))

        if not data_mode:
            issues.append(_make_issue(
                code="ID_DATA_MODE_MISSING",
                severity=DataQualityIssueSeverity.WARNING,
                field="data_mode",
                message="data_mode is missing; defaulting to UNAVAILABLE",
                source="validator",
                expected_rule="data_mode must be REAL, MOCK, or UNAVAILABLE",
                actual_value=repr(data_mode),
                blocks_analysis=False,
            ))

        if not timestamp:
            issues.append(_make_issue(
                code="ID_TIMESTAMP_MISSING",
                severity=DataQualityIssueSeverity.WARNING,
                field="date",
                message="No market timestamp provided",
                source="validator",
                expected_rule="date or latest_market_timestamp must be present",
                actual_value="",
                blocks_analysis=False,
            ))

        # REAL mode: source must not be mock/unknown
        if data_mode == DataMode.REAL:
            mock_sources_found = [s for s in source if s.lower() in self._MOCK_SOURCES]
            if mock_sources_found or not source:
                reason = (
                    f"Real mode with mock/unknown source: {mock_sources_found}"
                    if mock_sources_found
                    else "Real mode with no source specified"
                )
                issues.append(_make_issue(
                    code="ID_REAL_MODE_MOCK_SOURCE",
                    severity=DataQualityIssueSeverity.CRITICAL,
                    field="source",
                    message=reason,
                    source="validator",
                    expected_rule="REAL mode requires a non-mock, identified data source",
                    actual_value=str(source),
                    blocks_analysis=True,
                ))
                blocking_reasons.append(reason)

    # ------------------------------------------------------------------
    # Check 2: Price data validity
    # ------------------------------------------------------------------
    def _check_price_data(self, data: dict, issues: List[DataQualityIssue],
                          blocking_reasons: List[str]) -> None:
        data_mode = data.get("data_mode", DataMode.UNAVAILABLE)

        close = data.get("close")
        open_ = data.get("open")
        high  = data.get("high")
        low   = data.get("low")
        volume = data.get("volume")

        # close missing or NaN/None
        if close is None:
            issues.append(_make_issue(
                code="PRICE_CLOSE_MISSING",
                severity=DataQualityIssueSeverity.CRITICAL,
                field="close",
                message="Close price is missing",
                source="validator",
                expected_rule="close must be a positive number",
                actual_value="None",
                blocks_analysis=True,
            ))
            blocking_reasons.append("Close price missing")
            return  # No further price checks possible

        if _is_nan_or_inf(close):
            issues.append(_make_issue(
                code="PRICE_CLOSE_INVALID",
                severity=DataQualityIssueSeverity.CRITICAL,
                field="close",
                message=f"Close price is NaN or Infinity: {close}",
                source="validator",
                expected_rule="close must be a finite positive number",
                actual_value=str(close),
                blocks_analysis=True,
            ))
            blocking_reasons.append("Close price is NaN/Infinity")
            return

        try:
            close_f = float(close)
        except (TypeError, ValueError):
            issues.append(_make_issue(
                code="PRICE_CLOSE_NOT_NUMERIC",
                severity=DataQualityIssueSeverity.CRITICAL,
                field="close",
                message=f"Close price is not numeric: {close!r}",
                source="validator",
                expected_rule="close must be numeric",
                actual_value=str(close),
                blocks_analysis=True,
            ))
            blocking_reasons.append("Close price not numeric")
            return

        if close_f <= 0:
            issues.append(_make_issue(
                code="PRICE_CLOSE_ZERO_OR_NEGATIVE",
                severity=DataQualityIssueSeverity.CRITICAL,
                field="close",
                message=f"Close price <= 0: {close_f}",
                source="validator",
                expected_rule="close > 0",
                actual_value=str(close_f),
                blocks_analysis=True,
            ))
            blocking_reasons.append(f"Close price <= 0: {close_f}")

        # REAL mode: fixed test prices are suspicious
        if data_mode == DataMode.REAL and close_f in self._FIXED_TEST_PRICES:
            issues.append(_make_issue(
                code="PRICE_FIXED_TEST_VALUE_REAL",
                severity=DataQualityIssueSeverity.CRITICAL,
                field="close",
                message=f"Close price is a known test fixture value in REAL mode: {close_f}",
                source="validator",
                expected_rule="REAL mode: close must not be a known test/fixture price",
                actual_value=str(close_f),
                blocks_analysis=True,
            ))
            blocking_reasons.append(f"Fixed test price in REAL mode: {close_f}")

        # OHLC relationship checks
        if high is not None and not _is_nan_or_inf(high):
            high_f = float(high)
            if high_f < close_f:
                issues.append(_make_issue(
                    code="PRICE_HIGH_LESS_THAN_CLOSE",
                    severity=DataQualityIssueSeverity.CRITICAL,
                    field="high",
                    message=f"High ({high_f}) < Close ({close_f})",
                    source="validator",
                    expected_rule="high >= close",
                    actual_value=str(high_f),
                    blocks_analysis=True,
                ))
                blocking_reasons.append(f"OHLC violation: high < close")
            if open_ is not None and not _is_nan_or_inf(open_):
                open_f = float(open_)
                if high_f < open_f:
                    issues.append(_make_issue(
                        code="PRICE_HIGH_LESS_THAN_OPEN",
                        severity=DataQualityIssueSeverity.CRITICAL,
                        field="high",
                        message=f"High ({high_f}) < Open ({open_f})",
                        source="validator",
                        expected_rule="high >= open",
                        actual_value=str(high_f),
                        blocks_analysis=True,
                    ))
                    blocking_reasons.append("OHLC violation: high < open")

        if low is not None and not _is_nan_or_inf(low):
            low_f = float(low)
            if low_f > close_f:
                issues.append(_make_issue(
                    code="PRICE_LOW_GREATER_THAN_CLOSE",
                    severity=DataQualityIssueSeverity.CRITICAL,
                    field="low",
                    message=f"Low ({low_f}) > Close ({close_f})",
                    source="validator",
                    expected_rule="low <= close",
                    actual_value=str(low_f),
                    blocks_analysis=True,
                ))
                blocking_reasons.append("OHLC violation: low > close")
            if open_ is not None and not _is_nan_or_inf(open_):
                open_f = float(open_)
                if low_f > open_f:
                    issues.append(_make_issue(
                        code="PRICE_LOW_GREATER_THAN_OPEN",
                        severity=DataQualityIssueSeverity.CRITICAL,
                        field="low",
                        message=f"Low ({low_f}) > Open ({open_f})",
                        source="validator",
                        expected_rule="low <= open",
                        actual_value=str(low_f),
                        blocks_analysis=True,
                    ))
                    blocking_reasons.append("OHLC violation: low > open")

        if high is not None and low is not None and not _is_nan_or_inf(high) and not _is_nan_or_inf(low):
            if float(high) < float(low):
                issues.append(_make_issue(
                    code="PRICE_HIGH_LESS_THAN_LOW",
                    severity=DataQualityIssueSeverity.CRITICAL,
                    field="high",
                    message=f"High ({high}) < Low ({low})",
                    source="validator",
                    expected_rule="high >= low",
                    actual_value=f"high={high}, low={low}",
                    blocks_analysis=True,
                ))
                blocking_reasons.append("OHLC violation: high < low")

        # Volume
        if volume is not None and not _is_nan_or_inf(volume):
            try:
                vol_f = float(volume)
                if vol_f < 0:
                    issues.append(_make_issue(
                        code="PRICE_VOLUME_NEGATIVE",
                        severity=DataQualityIssueSeverity.CRITICAL,
                        field="volume",
                        message=f"Volume is negative: {vol_f}",
                        source="validator",
                        expected_rule="volume >= 0",
                        actual_value=str(vol_f),
                        blocks_analysis=True,
                    ))
                    blocking_reasons.append(f"Negative volume: {vol_f}")
            except (TypeError, ValueError):
                pass
        elif volume is None:
            issues.append(_make_issue(
                code="PRICE_VOLUME_MISSING",
                severity=DataQualityIssueSeverity.WARNING,
                field="volume",
                message="Volume is missing",
                source="validator",
                expected_rule="volume should be >= 0",
                actual_value="None",
                blocks_analysis=False,
            ))

    # ------------------------------------------------------------------
    # Check 3: Freshness
    # ------------------------------------------------------------------
    def _check_freshness(self, data: dict, issues: List[DataQualityIssue],
                         warnings: List[str]) -> None:
        date_str = str(data.get("date", "") or data.get("latest_market_timestamp", ""))
        if not date_str:
            return  # Already warned in identification check

        try:
            market_dt = _parse_date_flexible(date_str)
        except Exception:
            issues.append(_make_issue(
                code="FRESH_DATE_UNPARSEABLE",
                severity=DataQualityIssueSeverity.WARNING,
                field="date",
                message=f"Cannot parse date for freshness check: {date_str!r}",
                source="validator",
                expected_rule="date must be parseable as YYYY-MM-DD or ISO datetime",
                actual_value=date_str,
                blocks_analysis=False,
            ))
            return

        now = datetime.now(timezone.utc)
        if market_dt.tzinfo is None:
            market_dt = market_dt.replace(tzinfo=timezone.utc)

        # If market_dt is in the future: suspicious
        if market_dt > now + timedelta(hours=1):
            issues.append(_make_issue(
                code="FRESH_DATE_FUTURE",
                severity=DataQualityIssueSeverity.ERROR,
                field="date",
                message=f"Market timestamp is in the future: {date_str}",
                source="validator",
                expected_rule="market date must not be in the future",
                actual_value=date_str,
                blocks_analysis=True,
            ))
            return

        age_hours = (now - market_dt).total_seconds() / 3600

        # Check if today (now) is a weekend -> do NOT flag previous trading day as stale
        today = now.date()
        is_weekend = today.weekday() >= 5  # Sat=5, Sun=6

        # Try TradingCalendar if available
        try:
            from data_freshness.trading_calendar import TradingCalendar
            cal = TradingCalendar()
            is_today_trading = cal.is_trading_day(today)
        except Exception:
            # Fallback: weekday heuristic
            is_today_trading = (today.weekday() < 5)

        # Daily price threshold: 26 hours
        daily_threshold = _FRESHNESS_POLICY["daily_price"]
        if age_hours > daily_threshold:
            # On weekend / non-trading day, up to 3 days old is still acceptable
            max_acceptable_hours = daily_threshold if is_today_trading else 72
            if age_hours > max_acceptable_hours:
                sev = DataQualityIssueSeverity.ERROR
                issues.append(_make_issue(
                    code="FRESH_DAILY_PRICE_STALE",
                    severity=sev,
                    field="date",
                    message=f"Daily price data is stale: {age_hours:.1f}h old (threshold {max_acceptable_hours}h)",
                    source="validator",
                    expected_rule=f"Daily price should be <= {max_acceptable_hours}h old",
                    actual_value=date_str,
                    blocks_analysis=False,
                ))
                warnings.append(f"Stale daily price: {age_hours:.0f}h old")

    # ------------------------------------------------------------------
    # Check 4: Technical indicators
    # ------------------------------------------------------------------
    def _check_indicators(self, data: dict, issues: List[DataQualityIssue],
                          warnings: List[str]) -> None:
        _INDICATOR_FIELDS = [
            "MA5", "MA10", "MA20", "MA60",
            "KD_K", "KD_D", "RSI",
            "MACD_line", "MACD_signal", "MACD_hist",
        ]
        for field in _INDICATOR_FIELDS:
            val = data.get(field)
            if val is None:
                # Missing indicator: reduce score, add info issue
                issues.append(_make_issue(
                    code=f"IND_MISSING_{field}",
                    severity=DataQualityIssueSeverity.INFO,
                    field=field,
                    message=f"Indicator {field} is not provided",
                    source="validator",
                    expected_rule=f"{field} should be computed from valid OHLCV history",
                    actual_value="None",
                    blocks_analysis=False,
                ))
            elif _is_nan_or_inf(val):
                # NaN must NOT be converted to 0 — flag it
                issues.append(_make_issue(
                    code=f"IND_NAN_{field}",
                    severity=DataQualityIssueSeverity.WARNING,
                    field=field,
                    message=f"Indicator {field} is NaN/Infinity — do NOT convert to 0",
                    source="validator",
                    expected_rule=f"{field} must be a finite number or None (not 0-substituted NaN)",
                    actual_value=str(val),
                    blocks_analysis=False,
                ))
                warnings.append(f"{field} is NaN — not substituted with 0")

        # MA60 history check
        ma60 = data.get("MA60")
        if ma60 is None or _is_nan_or_inf(ma60 if ma60 is not None else float("nan")):
            # MA60 requires 60 trading days of history
            issues.append(_make_issue(
                code="IND_MA60_INSUFFICIENT_HISTORY",
                severity=DataQualityIssueSeverity.WARNING,
                field="MA60",
                message="MA60 is missing — may indicate insufficient history (< 60 trading days)",
                source="validator",
                expected_rule="MA60 requires 60 trading days of OHLCV history",
                actual_value=str(ma60),
                blocks_analysis=False,
            ))

    # ------------------------------------------------------------------
    # Check 5: Chips and institutional data
    # ------------------------------------------------------------------
    def _check_chips(self, data: dict, issues: List[DataQualityIssue],
                     warnings: List[str]) -> None:
        _CHIPS_FIELDS = [
            "foreign", "investment_trust", "dealer",
            "margin_balance", "major_holders", "retail_holders",
        ]
        for field in _CHIPS_FIELDS:
            val = data.get(field)
            if val is None:
                # Missing chips != 0: do not assume zero, flag as missing
                issues.append(_make_issue(
                    code=f"CHIPS_MISSING_{field}",
                    severity=DataQualityIssueSeverity.INFO,
                    field=field,
                    message=(
                        f"Chips field {field} is missing. "
                        "Missing != zero — do not substitute 0."
                    ),
                    source="validator",
                    expected_rule=f"{field} should be explicitly zero or provided value",
                    actual_value="None",
                    blocks_analysis=False,
                ))

        # investment_trust_avg_cost: if estimated, must be labeled
        it_cost = data.get("investment_trust_avg_cost")
        if it_cost is not None:
            estimation_method = data.get("investment_trust_avg_cost_estimation_method")
            if not estimation_method:
                issues.append(_make_issue(
                    code="CHIPS_IT_COST_NO_ESTIMATION_METHOD",
                    severity=DataQualityIssueSeverity.INFO,
                    field="investment_trust_avg_cost",
                    message=(
                        "investment_trust_avg_cost is present but estimation_method not labeled. "
                        "If estimated, must include estimation_method and confidence."
                    ),
                    source="validator",
                    expected_rule="If estimated: must include investment_trust_avg_cost_estimation_method",
                    actual_value=str(it_cost),
                    blocks_analysis=False,
                ))

    # ------------------------------------------------------------------
    # Check 6: Fundamentals
    # ------------------------------------------------------------------
    def _check_fundamentals(self, data: dict, issues: List[DataQualityIssue],
                            warnings: List[str]) -> None:
        _FUND_FIELDS = [
            "monthly_revenue", "yoy_revenue_growth",
            "financial_statement_period", "eps", "latest_reporting_period",
        ]
        for field in _FUND_FIELDS:
            val = data.get(field)
            if val is None:
                issues.append(_make_issue(
                    code=f"FUND_MISSING_{field}",
                    severity=DataQualityIssueSeverity.INFO,
                    field=field,
                    message=f"Fundamental field {field} is not provided",
                    source="validator",
                    expected_rule=f"{field} should preserve original reporting period",
                    actual_value="None",
                    blocks_analysis=False,
                ))

        # Revenue/EPS: original reporting period must be preserved
        period = data.get("financial_statement_period") or data.get("latest_reporting_period")
        if period and data.get("monthly_revenue") is not None:
            # Cannot auto-verify without full date logic; just warn if period looks like old date
            pass  # Structural check only — not flagging old vs new without external reference

    # ------------------------------------------------------------------
    # Check 7: Cross-source consistency
    # ------------------------------------------------------------------
    def _check_cross_source(self, data: dict, issues: List[DataQualityIssue],
                            blocking_reasons: List[str]) -> None:
        cross_data = data.get("cross_source_data")
        if not cross_data or not isinstance(cross_data, dict):
            return  # No cross-source data provided — nothing to check

        source_names = list(cross_data.keys())
        if len(source_names) < 2:
            return  # Need at least 2 sources

        # Compare close prices across sources
        closes = {}
        volumes = {}
        for src_name, src_data in cross_data.items():
            if isinstance(src_data, dict):
                c = src_data.get("close")
                v = src_data.get("volume")
                if c is not None and not _is_nan_or_inf(c):
                    closes[src_name] = float(c)
                if v is not None and not _is_nan_or_inf(v):
                    volumes[src_name] = float(v)

        if len(closes) >= 2:
            close_vals = list(closes.values())
            max_c = max(close_vals)
            min_c = min(close_vals)
            if max_c > 0:
                diff_pct = (max_c - min_c) / max_c
                if diff_pct > 0.01:  # >1% price conflict
                    sev = DataQualityIssueSeverity.CRITICAL if diff_pct > 0.05 else DataQualityIssueSeverity.ERROR
                    msg = (
                        f"Cross-source close price conflict: "
                        f"max={max_c:.2f}, min={min_c:.2f}, diff={diff_pct:.1%}. "
                        f"Sources: {list(closes.keys())}. Do NOT silently pick one."
                    )
                    issues.append(_make_issue(
                        code="CROSS_PRICE_CONFLICT",
                        severity=sev,
                        field="close",
                        message=msg,
                        source="cross_source_validator",
                        expected_rule="Cross-source close prices must agree within 1%",
                        actual_value=f"max={max_c:.2f} min={min_c:.2f}",
                        blocks_analysis=(sev == DataQualityIssueSeverity.CRITICAL),
                    ))
                    if sev == DataQualityIssueSeverity.CRITICAL:
                        blocking_reasons.append(
                            f"Critical cross-source price conflict: {diff_pct:.1%} difference"
                        )

        # Check symbol/market consistency
        for src_name, src_data in cross_data.items():
            if isinstance(src_data, dict):
                src_sym = src_data.get("symbol")
                src_mkt = src_data.get("market")
                main_sym = data.get("symbol", "")
                main_mkt = data.get("market", "")
                if src_sym and src_sym != main_sym:
                    issues.append(_make_issue(
                        code="CROSS_SYMBOL_INCONSISTENT",
                        severity=DataQualityIssueSeverity.ERROR,
                        field="symbol",
                        message=f"Cross-source symbol mismatch: main={main_sym!r}, {src_name}={src_sym!r}",
                        source="cross_source_validator",
                        expected_rule="All cross-sources must report the same symbol",
                        actual_value=f"{src_name}:{src_sym}",
                        blocks_analysis=True,
                    ))

    # ------------------------------------------------------------------
    # Derive status
    # ------------------------------------------------------------------
    def _derive_status(self, data: dict, issues: List[DataQualityIssue],
                       score: int, blocking_reasons: List[str]) -> str:
        data_mode = data.get("data_mode", DataMode.UNAVAILABLE)
        has_critical = any(
            iss.severity == DataQualityIssueSeverity.CRITICAL for iss in issues
        )

        # No data at all -> UNAVAILABLE
        if data_mode == DataMode.UNAVAILABLE and not data.get("close") and not data.get("source"):
            return DataQualityStatus.UNAVAILABLE

        # CRITICAL issue -> BLOCKED
        if has_critical:
            return DataQualityStatus.BLOCKED

        # Blocking reasons -> BLOCKED
        if blocking_reasons:
            return DataQualityStatus.BLOCKED

        # Real source unknown -> BLOCKED
        if data_mode == DataMode.REAL:
            source = data.get("source", [])
            if isinstance(source, str):
                source = [source] if source else []
            if not source or any(s.lower() in self._MOCK_SOURCES for s in source):
                return DataQualityStatus.BLOCKED

        # No data -> UNAVAILABLE
        if score == 0 and not data.get("close"):
            return DataQualityStatus.UNAVAILABLE

        # Score-based status
        if score >= 85:
            return DataQualityStatus.PASS
        if score >= 65:
            return DataQualityStatus.DEGRADED
        if score >= 1:
            return DataQualityStatus.BLOCKED

        return DataQualityStatus.UNAVAILABLE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_issue(
    code: str, severity: str, field: str, message: str,
    source: str, expected_rule: str, actual_value: str,
    blocks_analysis: bool,
) -> DataQualityIssue:
    return DataQualityIssue(
        code=code,
        severity=severity,
        field=field,
        message=message,
        source=source,
        observed_at="",
        expected_rule=expected_rule,
        actual_value=actual_value,
        blocks_analysis=blocks_analysis,
    )


def _is_nan_or_inf(val) -> bool:
    try:
        f = float(val)
        return math.isnan(f) or math.isinf(f)
    except (TypeError, ValueError):
        return False


def _parse_date_flexible(date_str: str) -> datetime:
    """Try multiple common date formats.

    A date-only string (YYYY-MM-DD) represents the trading day, not midnight.
    Market data for a given day is available at end-of-trading-day, so we
    treat date-only strings as 23:59:59 of that day to avoid false stale
    flags when the data is checked early the next calendar day.
    """
    stripped = date_str.strip()
    # Detect date-only format: exactly 10 chars matching YYYY-MM-DD
    import re as _re
    if _re.match(r'^\d{4}-\d{2}-\d{2}$', stripped):
        dt = datetime.strptime(stripped, "%Y-%m-%d")
        # Interpret as end-of-trading-day to avoid false stale detection
        return dt.replace(hour=23, minute=59, second=59)
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(stripped[:19], fmt[:len(fmt)])
        except ValueError:
            continue
    # Last try: fromisoformat
    return datetime.fromisoformat(date_str)

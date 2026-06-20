"""
data/providers/mops/derived_metrics_v142.py — MOPS derived financial metrics v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Computes derived metrics from MOPS financial statements.
Missing inputs -> None output. Never fills missing with 0.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.providers.mops.models_v142 import (
    MOPSBalanceSheet, MOPSCashFlowStatement, MOPSFinancialMetric, MOPSIncomeStatement
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSDerivedFinancialMetrics:
    """
    Computes derived financial metrics from MOPS balance sheet,
    income statement, and cash flow statement.
    All inputs must be from the same period.
    Missing inputs always produce None output — never 0.
    """

    def compute_all(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        balance_sheet: Optional[MOPSBalanceSheet] = None,
        income_statement: Optional[MOPSIncomeStatement] = None,
        cash_flow: Optional[MOPSCashFlowStatement] = None,
        available_from: Optional[str] = None,
    ) -> List[MOPSFinancialMetric]:
        """Compute all available derived metrics. Returns list of MOPSFinancialMetric."""
        metrics: List[MOPSFinancialMetric] = []
        now = _now_iso()

        def _make(name: str, value: Optional[float], unit: str, method: str) -> MOPSFinancialMetric:
            return MOPSFinancialMetric(
                symbol=symbol,
                fiscal_year=fiscal_year,
                fiscal_period=fiscal_period,
                metric_name=name,
                metric_value=value,
                metric_unit=unit,
                currency="TWD",
                is_derived=True,
                derivation_method=method,
                available_from=available_from,
                source_timestamp=None,
                fetched_at=now,
                provider_id="mops_official",
                provenance=None,
                warnings=[],
                metadata={},
            )

        # Gross margin
        if income_statement:
            rev = income_statement.revenue
            gp = income_statement.gross_profit
            gross_margin = (gp / rev * 100) if (rev and gp is not None and rev != 0) else None
            metrics.append(_make("gross_margin_pct", gross_margin, "PERCENT", "gross_profit/revenue*100"))

            # Operating margin
            oi = income_statement.operating_income
            op_margin = (oi / rev * 100) if (rev and oi is not None and rev != 0) else None
            metrics.append(_make("operating_margin_pct", op_margin, "PERCENT", "operating_income/revenue*100"))

            # Net margin
            ni = income_statement.net_income
            net_margin = (ni / rev * 100) if (rev and ni is not None and rev != 0) else None
            metrics.append(_make("net_margin_pct", net_margin, "PERCENT", "net_income/revenue*100"))

        # ROE
        if income_statement and balance_sheet:
            ni = income_statement.net_income
            eq = balance_sheet.total_equity
            roe = (ni / eq * 100) if (ni is not None and eq and eq != 0) else None
            metrics.append(_make("roe_pct", roe, "PERCENT", "net_income/total_equity*100"))

            # ROA
            ta = balance_sheet.total_assets
            roa = (ni / ta * 100) if (ni is not None and ta and ta != 0) else None
            metrics.append(_make("roa_pct", roa, "PERCENT", "net_income/total_assets*100"))

            # Debt ratio
            tl = balance_sheet.total_liabilities
            debt_ratio = (tl / ta * 100) if (tl is not None and ta and ta != 0) else None
            metrics.append(_make("debt_ratio_pct", debt_ratio, "PERCENT", "total_liabilities/total_assets*100"))

            # Current ratio
            ca = balance_sheet.current_assets
            cl = balance_sheet.current_liabilities
            current_ratio = (ca / cl) if (ca is not None and cl and cl != 0) else None
            metrics.append(_make("current_ratio", current_ratio, "RATIO", "current_assets/current_liabilities"))

        # Free cash flow (already computed in cash_flow if available)
        if cash_flow:
            metrics.append(_make("free_cash_flow", cash_flow.free_cash_flow, "TWD_THOUSAND", "operating_cf-capex"))

            # Cash flow to revenue ratio
            if income_statement and income_statement.revenue:
                ocf = cash_flow.operating_cash_flow
                cf_margin = (ocf / income_statement.revenue * 100) if (ocf is not None and income_statement.revenue != 0) else None
                metrics.append(_make("ocf_margin_pct", cf_margin, "PERCENT", "operating_cf/revenue*100"))

        return metrics

    def compute_from_dicts(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        bs_data: Optional[Dict[str, Any]] = None,
        is_data: Optional[Dict[str, Any]] = None,
        cf_data: Optional[Dict[str, Any]] = None,
        available_from: Optional[str] = None,
    ) -> List[MOPSFinancialMetric]:
        """Compute metrics from raw dicts (for offline/fixture tests)."""
        bs = None
        is_obj = None
        cf = None

        if bs_data:
            from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
            bs = MOPSBalanceSheetParser().parse_from_fixture(symbol, fiscal_year, fiscal_period, bs_data)
        if is_data:
            from data.providers.mops.income_statement_v142 import MOPSIncomeStatementParser
            is_obj = MOPSIncomeStatementParser().parse_from_fixture(symbol, fiscal_year, fiscal_period, is_data)
        if cf_data:
            from data.providers.mops.cash_flow_v142 import MOPSCashFlowParser
            cf = MOPSCashFlowParser().parse_from_fixture(symbol, fiscal_year, fiscal_period, cf_data)

        return self.compute_all(symbol, fiscal_year, fiscal_period, bs, is_obj, cf, available_from)

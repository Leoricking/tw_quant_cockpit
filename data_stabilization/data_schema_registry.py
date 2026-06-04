"""data_stabilization/data_schema_registry.py — DatasetSchemaRegistry v0.5.5.

Centrally defines dataset schemas for Market, Financial, Chip, Feature Store,
and Reports / Runtime datasets.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Category constants
# ---------------------------------------------------------------------------
CAT_MARKET   = "A. Market Data"
CAT_FINANCIAL = "B. Financial Data"
CAT_CHIP     = "C. Chip Data"
CAT_FEATURE  = "D. Feature Store"
CAT_RUNTIME  = "E. Reports / Runtime"


@dataclass
class DatasetSchema:
    """Schema definition for a single dataset.

    [!] Data Stabilization Only. Research Only. No Real Orders.
    """

    dataset_name:      str
    category:          str
    required_columns:  List[str] = field(default_factory=list)
    optional_columns:  List[str] = field(default_factory=list)
    date_column:       str = ""
    symbol_column:     str = ""
    frequency:         str = ""
    expected_source:   str = ""
    freshness_rule:    str = ""
    min_rows:          int = 0
    primary_key:       List[str] = field(default_factory=list)
    known_limitations: str = ""
    safety_notes:      str = "Data Stabilization Only. No Real Orders."

    # Safety invariants
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "dataset_name":      self.dataset_name,
            "category":          self.category,
            "required_columns":  self.required_columns,
            "optional_columns":  self.optional_columns,
            "date_column":       self.date_column,
            "symbol_column":     self.symbol_column,
            "frequency":         self.frequency,
            "expected_source":   self.expected_source,
            "freshness_rule":    self.freshness_rule,
            "min_rows":          self.min_rows,
            "primary_key":       self.primary_key,
            "known_limitations": self.known_limitations,
            "safety_notes":      self.safety_notes,
        }


# ---------------------------------------------------------------------------
# Schema definitions
# ---------------------------------------------------------------------------

_SCHEMAS: List[DatasetSchema] = [
    # ----------------------------------------------------------------
    # A. Market Data
    # ----------------------------------------------------------------
    DatasetSchema(
        dataset_name="daily_k",
        category=CAT_MARKET,
        required_columns=["date", "symbol", "open", "high", "low", "close", "volume"],
        optional_columns=["turnover", "shares", "change_pct", "amplitude"],
        date_column="date",
        symbol_column="symbol",
        frequency="daily",
        expected_source="TWSE / TPEX public endpoint",
        freshness_rule="Updated by market open +1 day; stale if >3 calendar days",
        min_rows=10,
        primary_key=["date", "symbol"],
        known_limitations="No real-time streaming; historical only",
    ),
    DatasetSchema(
        dataset_name="intraday_1min",
        category=CAT_MARKET,
        required_columns=["datetime", "symbol", "open", "high", "low", "close", "volume"],
        optional_columns=["vwap", "bid", "ask", "spread"],
        date_column="datetime",
        symbol_column="symbol",
        frequency="1min",
        expected_source="XQ CSV import / TWSE tick aggregation",
        freshness_rule="Stale if >1 trading day behind",
        min_rows=0,
        primary_key=["datetime", "symbol"],
        known_limitations="Requires CSV import; no live feed",
    ),
    DatasetSchema(
        dataset_name="intraday_5min",
        category=CAT_MARKET,
        required_columns=["datetime", "symbol", "open", "high", "low", "close", "volume"],
        optional_columns=["vwap"],
        date_column="datetime",
        symbol_column="symbol",
        frequency="5min",
        expected_source="Aggregated from 1min or XQ CSV",
        freshness_rule="Stale if >1 trading day behind",
        min_rows=0,
        primary_key=["datetime", "symbol"],
    ),
    DatasetSchema(
        dataset_name="tick",
        category=CAT_MARKET,
        required_columns=["datetime", "symbol", "price", "volume"],
        optional_columns=["bid", "ask", "trade_type"],
        date_column="datetime",
        symbol_column="symbol",
        frequency="tick",
        expected_source="XQ CSV import",
        freshness_rule="Stale if >1 trading day behind",
        min_rows=0,
        primary_key=["datetime", "symbol"],
    ),
    DatasetSchema(
        dataset_name="bidask",
        category=CAT_MARKET,
        required_columns=["datetime", "symbol", "bid1", "ask1"],
        optional_columns=["bid2", "ask2", "bid3", "ask3", "bid_vol1", "ask_vol1"],
        date_column="datetime",
        symbol_column="symbol",
        frequency="tick",
        expected_source="XQ CSV import",
        freshness_rule="Stale if >1 trading day behind",
        min_rows=0,
        primary_key=["datetime", "symbol"],
    ),
    # ----------------------------------------------------------------
    # B. Financial Data
    # ----------------------------------------------------------------
    DatasetSchema(
        dataset_name="monthly_revenue",
        category=CAT_FINANCIAL,
        required_columns=["date", "symbol", "revenue"],
        optional_columns=["revenue_yoy", "revenue_mom", "revenue_3m_avg"],
        date_column="date",
        symbol_column="symbol",
        frequency="monthly",
        expected_source="TWSE public monthly revenue",
        freshness_rule="Released by 10th of following month; stale if >45 days",
        min_rows=5,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="quarterly_financials",
        category=CAT_FINANCIAL,
        required_columns=["date", "symbol", "revenue", "gross_profit", "operating_income", "net_income"],
        optional_columns=["eps", "total_assets", "total_liabilities", "equity"],
        date_column="date",
        symbol_column="symbol",
        frequency="quarterly",
        expected_source="TWSE / TPEX quarterly financial statements",
        freshness_rule="Released ~45 days after quarter end; stale if >120 days",
        min_rows=2,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="eps",
        category=CAT_FINANCIAL,
        required_columns=["date", "symbol", "eps"],
        optional_columns=["eps_yoy", "eps_ttm", "eps_forecast"],
        date_column="date",
        symbol_column="symbol",
        frequency="quarterly",
        expected_source="Derived from quarterly_financials",
        freshness_rule="Stale if >120 days",
        min_rows=2,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="gross_margin",
        category=CAT_FINANCIAL,
        required_columns=["date", "symbol", "gross_margin"],
        optional_columns=["gross_margin_yoy"],
        date_column="date",
        symbol_column="symbol",
        frequency="quarterly",
        expected_source="Derived from quarterly_financials",
        freshness_rule="Stale if >120 days",
        min_rows=2,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="operating_margin",
        category=CAT_FINANCIAL,
        required_columns=["date", "symbol", "operating_margin"],
        optional_columns=["operating_margin_yoy"],
        date_column="date",
        symbol_column="symbol",
        frequency="quarterly",
        expected_source="Derived from quarterly_financials",
        freshness_rule="Stale if >120 days",
        min_rows=2,
        primary_key=["date", "symbol"],
    ),
    # ----------------------------------------------------------------
    # C. Chip Data
    # ----------------------------------------------------------------
    DatasetSchema(
        dataset_name="institutional_trading",
        category=CAT_CHIP,
        required_columns=["date", "symbol", "foreign_net", "investment_trust_net", "dealer_net"],
        optional_columns=["total_net", "consecutive_days"],
        date_column="date",
        symbol_column="symbol",
        frequency="daily",
        expected_source="TWSE public chip data",
        freshness_rule="Stale if >3 trading days",
        min_rows=5,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="margin_balance",
        category=CAT_CHIP,
        required_columns=["date", "symbol", "margin_balance", "short_balance"],
        optional_columns=["margin_ratio", "short_ratio"],
        date_column="date",
        symbol_column="symbol",
        frequency="daily",
        expected_source="TWSE margin balance",
        freshness_rule="Stale if >3 trading days",
        min_rows=5,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="major_holders",
        category=CAT_CHIP,
        required_columns=["date", "symbol", "major_holder_ratio"],
        optional_columns=["top10_ratio", "insider_ratio"],
        date_column="date",
        symbol_column="symbol",
        frequency="monthly",
        expected_source="TWSE shareholding concentration",
        freshness_rule="Stale if >45 days",
        min_rows=1,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="shareholder_distribution",
        category=CAT_CHIP,
        required_columns=["date", "symbol", "bracket_1_to_999", "bracket_1000_to_5000"],
        optional_columns=["total_shareholders", "retail_ratio"],
        date_column="date",
        symbol_column="symbol",
        frequency="monthly",
        expected_source="TWSE shareholder distribution",
        freshness_rule="Stale if >45 days",
        min_rows=1,
        primary_key=["date", "symbol"],
    ),
    # ----------------------------------------------------------------
    # D. Feature Store
    # ----------------------------------------------------------------
    DatasetSchema(
        dataset_name="technical_features",
        category=CAT_FEATURE,
        required_columns=["date", "symbol", "ma5", "ma20", "ma60", "rsi14"],
        optional_columns=["macd", "bollinger_upper", "bollinger_lower", "atr14", "volume_ratio"],
        date_column="date",
        symbol_column="symbol",
        frequency="daily",
        expected_source="Derived from daily_k",
        freshness_rule="Stale if >3 trading days",
        min_rows=10,
        primary_key=["date", "symbol"],
        known_limitations="Must not include future_return or forward-looking labels",
    ),
    DatasetSchema(
        dataset_name="microstructure_features",
        category=CAT_FEATURE,
        required_columns=["datetime", "symbol", "spread", "depth_imbalance"],
        optional_columns=["vwap_deviation", "order_flow_imbalance", "midprice"],
        date_column="datetime",
        symbol_column="symbol",
        frequency="intraday",
        expected_source="Derived from tick / bidask",
        freshness_rule="Stale if >1 trading day",
        min_rows=0,
        primary_key=["datetime", "symbol"],
        known_limitations="Requires tick/bidask import; no live feed",
    ),
    DatasetSchema(
        dataset_name="financial_features",
        category=CAT_FEATURE,
        required_columns=["date", "symbol", "eps_ttm", "gross_margin", "revenue_yoy"],
        optional_columns=["roe", "debt_ratio", "pe_ratio", "pb_ratio"],
        date_column="date",
        symbol_column="symbol",
        frequency="quarterly",
        expected_source="Derived from quarterly_financials / monthly_revenue",
        freshness_rule="Stale if >120 days",
        min_rows=2,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="chip_features",
        category=CAT_FEATURE,
        required_columns=["date", "symbol", "institutional_net_3d", "margin_change"],
        optional_columns=["consecutive_buy_days", "major_holder_change"],
        date_column="date",
        symbol_column="symbol",
        frequency="daily",
        expected_source="Derived from institutional_trading / margin_balance",
        freshness_rule="Stale if >3 trading days",
        min_rows=5,
        primary_key=["date", "symbol"],
    ),
    DatasetSchema(
        dataset_name="strategy_filter_features",
        category=CAT_FEATURE,
        required_columns=["date", "symbol", "financial_turnaround_score", "trend_discipline_score"],
        optional_columns=["eps_recovery", "revenue_recovery", "breakout_flag"],
        date_column="date",
        symbol_column="symbol",
        frequency="daily",
        expected_source="Derived from strategy_filter_pack",
        freshness_rule="Stale if >3 trading days",
        min_rows=0,
        primary_key=["date", "symbol"],
        known_limitations="Research Only. Strategy Filter Only.",
    ),
    DatasetSchema(
        dataset_name="ml_knowledge_features",
        category=CAT_FEATURE,
        required_columns=["date", "symbol", "feature_id", "value"],
        optional_columns=["confidence", "metadata_only"],
        date_column="date",
        symbol_column="symbol",
        frequency="daily",
        expected_source="ml.knowledge_feature_bridge",
        freshness_rule="Stale if >7 days",
        min_rows=0,
        primary_key=["date", "symbol", "feature_id"],
        known_limitations="auto_enabled must be False; metadata_only by default",
    ),
    # ----------------------------------------------------------------
    # E. Reports / Runtime
    # ----------------------------------------------------------------
    DatasetSchema(
        dataset_name="data_quality_summary",
        category=CAT_RUNTIME,
        required_columns=["generated_at", "mode", "production_readiness_score"],
        optional_columns=["backtest_readiness_score", "overall_gate"],
        date_column="generated_at",
        frequency="daily",
        expected_source="quality.data_quality_gate",
        freshness_rule="Stale if >1 trading day",
        min_rows=0,
    ),
    DatasetSchema(
        dataset_name="provider_health_summary",
        category=CAT_RUNTIME,
        required_columns=["generated_at", "provider_name", "status"],
        optional_columns=["token_configured", "recommended_action"],
        date_column="generated_at",
        frequency="daily",
        expected_source="data.providers.provider_health",
        freshness_rule="Stale if >1 day",
        min_rows=0,
    ),
    DatasetSchema(
        dataset_name="feature_readiness_summary",
        category=CAT_RUNTIME,
        required_columns=["generated_at", "feature_group", "status", "readiness_score"],
        optional_columns=["missing_columns", "stale", "leakage_risk"],
        date_column="generated_at",
        frequency="daily",
        expected_source="data_stabilization.feature_readiness_checker",
        freshness_rule="Stale if >1 day",
        min_rows=0,
    ),
]


class DatasetSchemaRegistry:
    """Registry of all dataset schemas for TW Quant Cockpit v0.5.5.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self) -> None:
        self._schemas: Dict[str, DatasetSchema] = {}
        for schema in _SCHEMAS:
            self._schemas[schema.dataset_name] = schema

    def list_schemas(self) -> List[str]:
        """Return all dataset names."""
        return list(self._schemas.keys())

    def get_schema(self, dataset_name: str) -> Optional[DatasetSchema]:
        """Return schema for a dataset, or None."""
        return self._schemas.get(dataset_name)

    def validate_columns(self, dataset_name: str, columns: List[str]) -> dict:
        """Validate columns against schema. Returns dict with missing/extra."""
        schema = self._schemas.get(dataset_name)
        if schema is None:
            return {
                "valid": False,
                "error": f"No schema defined for '{dataset_name}'",
                "missing_required": [],
                "missing_optional": [],
                "extra_columns": [],
            }
        required = set(schema.required_columns)
        optional = set(schema.optional_columns)
        present  = set(columns)
        missing_required = sorted(required - present)
        missing_optional = sorted(optional - present)
        extra            = sorted(present - required - optional)
        valid = len(missing_required) == 0
        return {
            "valid":            valid,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "extra_columns":    extra,
        }

    def build_schema_table(self) -> List[dict]:
        """Return list of schema dicts for tabular display."""
        rows = []
        for schema in _SCHEMAS:
            rows.append({
                "dataset_name":      schema.dataset_name,
                "category":          schema.category,
                "required_columns":  ", ".join(schema.required_columns),
                "optional_columns":  ", ".join(schema.optional_columns),
                "date_column":       schema.date_column,
                "symbol_column":     schema.symbol_column,
                "frequency":         schema.frequency,
                "expected_source":   schema.expected_source,
                "freshness_rule":    schema.freshness_rule,
                "min_rows":          schema.min_rows,
                "primary_key":       ", ".join(schema.primary_key),
                "known_limitations": schema.known_limitations,
            })
        return rows

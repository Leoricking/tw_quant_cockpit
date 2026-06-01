"""
ml/feature_catalog.py — ML Feature Catalog (v0.4.2).

Manages feature definitions: categories, leakage risk, experimental flags.

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Leakage risk levels
LEAKAGE_LOW    = "LOW"
LEAKAGE_MEDIUM = "MEDIUM"
LEAKAGE_HIGH   = "HIGH"


@dataclass
class FeatureDefinition:
    """Single feature definition in the catalog."""
    feature_id:       str
    feature_name:     str
    category:         str
    source_module:    str
    source_dataset:   str
    dtype:            str          = "float64"
    timeframe:        str          = "daily"
    description:      str          = ""
    required_columns: List[str]    = field(default_factory=list)
    lookback_window:  int          = 0
    leakage_risk:     str          = LEAKAGE_LOW
    enabled:          bool         = True
    experimental:     bool         = False
    version:          str          = "v1"
    notes:            str          = ""

    def to_dict(self) -> dict:
        return asdict(self)


class FeatureCatalog:
    """
    ML Feature Catalog — manages feature definitions.

    [!] ML Research Only. No Real Orders.
    """

    read_only      = True
    no_real_orders = True

    def __init__(self):
        self._features: Dict[str, FeatureDefinition] = {}
        self.load_builtin_features()

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_builtin_features(self) -> None:
        """Load all built-in feature definitions."""
        defs = self._get_builtin_definitions()
        for fd in defs:
            if fd.feature_id in self._features:
                logger.warning("Duplicate feature_id: %s — skipping", fd.feature_id)
                continue
            self._features[fd.feature_id] = fd

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def list_features(
        self,
        category: Optional[str] = None,
        timeframe: Optional[str] = None,
        enabled_only: bool = False,
    ) -> List[FeatureDefinition]:
        """List features, optionally filtered."""
        result = list(self._features.values())
        if category:
            result = [f for f in result if f.category == category]
        if timeframe:
            result = [f for f in result if f.timeframe == timeframe]
        if enabled_only:
            result = [f for f in result if f.enabled]
        return result

    def get_feature(self, feature_id: str) -> Optional[FeatureDefinition]:
        return self._features.get(feature_id)

    def export_catalog(self) -> List[dict]:
        return [fd.to_dict() for fd in self._features.values()]

    def summary(self) -> dict:
        all_f = list(self._features.values())
        cats = {}
        for f in all_f:
            cats[f.category] = cats.get(f.category, 0) + 1
        return {
            "total_features":       len(all_f),
            "enabled_features":     sum(1 for f in all_f if f.enabled),
            "experimental_features":sum(1 for f in all_f if f.experimental),
            "high_leakage_risk":    sum(1 for f in all_f if f.leakage_risk == LEAKAGE_HIGH),
            "categories":           cats,
        }

    # ------------------------------------------------------------------
    # Built-in definitions
    # ------------------------------------------------------------------

    def _get_builtin_definitions(self) -> List[FeatureDefinition]:
        return [
            # ---- Price ----
            FeatureDefinition("price.close_return_1d",  "Close Return 1D",   "price",     "features.indicators", "daily",
                              description="1-day close-to-close return", lookback_window=1, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("price.close_return_5d",  "Close Return 5D",   "price",     "features.indicators", "daily",
                              description="5-day close-to-close return",  lookback_window=5, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("price.close_return_20d", "Close Return 20D",  "price",     "features.indicators", "daily",
                              description="20-day close-to-close return", lookback_window=20, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("price.volatility_20d",   "Volatility 20D",    "price",     "features.indicators", "daily",
                              description="20-day rolling std of daily returns", lookback_window=20, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("price.high_low_range_pct","High-Low Range %", "price",     "features.indicators", "daily",
                              description="(high-low)/close", lookback_window=1, leakage_risk=LEAKAGE_LOW),

            # ---- Technical ----
            FeatureDefinition("tech.ma5_gap",    "MA5 Gap %",    "technical", "features.indicators", "daily",
                              description="(close - MA5) / MA5", lookback_window=5, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.ma10_gap",   "MA10 Gap %",   "technical", "features.indicators", "daily",
                              description="(close - MA10) / MA10", lookback_window=10, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.ma20_gap",   "MA20 Gap %",   "technical", "features.indicators", "daily",
                              description="(close - MA20) / MA20", lookback_window=20, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.ma60_gap",   "MA60 Gap %",   "technical", "features.indicators", "daily",
                              description="(close - MA60) / MA60", lookback_window=60, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.macd_dif",   "MACD DIF",     "technical", "features.indicators", "daily",
                              description="MACD DIF line (EMA12-EMA26)", lookback_window=26, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.macd_signal","MACD Signal",  "technical", "features.indicators", "daily",
                              description="MACD Signal line (EMA9 of DIF)", lookback_window=35, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.macd_osc",   "MACD Oscillator","technical","features.indicators","daily",
                              description="MACD DIF - Signal", lookback_window=35, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.rsi6",       "RSI 6",        "technical", "features.indicators", "daily",
                              description="RSI with 6-period window", lookback_window=6, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.rsi12",      "RSI 12",       "technical", "features.indicators", "daily",
                              description="RSI with 12-period window", lookback_window=12, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.kd_k",       "KD K",         "technical", "features.indicators", "daily",
                              description="Stochastic K line", lookback_window=9, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("tech.kd_d",       "KD D",         "technical", "features.indicators", "daily",
                              description="Stochastic D line (SMA3 of K)", lookback_window=12, leakage_risk=LEAKAGE_LOW),

            # ---- Volume ----
            FeatureDefinition("vol.volume_ratio_5d",    "Volume Ratio 5D",  "volume", "features.indicators", "daily",
                              description="volume / MA5(volume)", lookback_window=5, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("vol.volume_ratio_20d",   "Volume Ratio 20D", "volume", "features.indicators", "daily",
                              description="volume / MA20(volume)", lookback_window=20, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("vol.turnover_value",     "Turnover Value",   "volume", "features.indicators", "daily",
                              description="Daily turnover in NTD", lookback_window=1, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("vol.volume_breakout_flag","Volume Breakout Flag","volume","features.indicators","daily",
                              description="1 if volume > 2x MA20", lookback_window=20, leakage_risk=LEAKAGE_LOW,
                              dtype="int64"),

            # ---- Chip ----
            FeatureDefinition("chip.foreign_net_buy",         "Foreign Net Buy",         "chip", "data.providers", "institutional",
                              description="Foreign institutional net buy shares", lookback_window=1, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("chip.trust_net_buy",           "Trust Net Buy",           "chip", "data.providers", "institutional",
                              description="Investment trust net buy shares", lookback_window=1, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("chip.dealer_net_buy",          "Dealer Net Buy",          "chip", "data.providers", "institutional",
                              description="Dealer net buy shares", lookback_window=1, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("chip.institutional_total_net_buy","Institutional Total Net Buy","chip","data.providers","institutional",
                              description="Sum of all institutional net buy", lookback_window=1, leakage_risk=LEAKAGE_LOW),

            # ---- Margin ----
            FeatureDefinition("margin.margin_balance", "Margin Balance",   "margin", "data.providers", "margin",
                              description="Margin purchase balance (shares)", lookback_window=1, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("margin.margin_change",  "Margin Change",    "margin", "data.providers", "margin",
                              description="Day-over-day margin balance change", lookback_window=2, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("margin.short_balance",  "Short Balance",    "margin", "data.providers", "margin",
                              description="Short sale balance (shares)", lookback_window=1, leakage_risk=LEAKAGE_LOW),
            FeatureDefinition("margin.short_change",   "Short Change",     "margin", "data.providers", "margin",
                              description="Day-over-day short balance change", lookback_window=2, leakage_risk=LEAKAGE_LOW),

            # ---- Revenue ----
            FeatureDefinition("rev.revenue_mom",     "Revenue MoM",    "revenue", "data.providers", "monthly_revenue",
                              description="Monthly revenue month-over-month growth", lookback_window=1, leakage_risk=LEAKAGE_MEDIUM,
                              notes="Announced on 10th of following month"),
            FeatureDefinition("rev.revenue_yoy",     "Revenue YoY",    "revenue", "data.providers", "monthly_revenue",
                              description="Monthly revenue year-over-year growth", lookback_window=12, leakage_risk=LEAKAGE_MEDIUM),
            FeatureDefinition("rev.cumulative_yoy",  "Cumulative YoY", "revenue", "data.providers", "monthly_revenue",
                              description="Cumulative revenue YoY growth", lookback_window=12, leakage_risk=LEAKAGE_MEDIUM),

            # ---- Fundamental ----
            FeatureDefinition("fund.eps",              "EPS",              "fundamental", "data.providers", "financial_statement",
                              description="Earnings per share (quarterly)", lookback_window=90, leakage_risk=LEAKAGE_HIGH,
                              notes="announcement_date_is_estimated may be True; use timing_quality to assess risk"),
            FeatureDefinition("fund.gross_margin",     "Gross Margin",     "fundamental", "data.providers", "financial_statement",
                              description="Gross profit margin (quarterly)", lookback_window=90, leakage_risk=LEAKAGE_HIGH),
            FeatureDefinition("fund.operating_margin", "Operating Margin", "fundamental", "data.providers", "financial_statement",
                              description="Operating profit margin (quarterly)", lookback_window=90, leakage_risk=LEAKAGE_HIGH),
            FeatureDefinition("fund.pe_bucket",        "PE Bucket",        "fundamental", "data.providers", "financial_statement",
                              description="PE ratio bucket (low/mid/high)", lookback_window=90, leakage_risk=LEAKAGE_HIGH,
                              dtype="str", experimental=True),
            FeatureDefinition("fund.timing_quality",   "Timing Quality",   "fundamental", "data.providers.mops_financial_parser", "financial_statement",
                              description="ACTUAL/ESTIMATED/DEADLINE/UNKNOWN timing quality for fundamental data",
                              lookback_window=0, leakage_risk=LEAKAGE_LOW, dtype="str"),

            # ---- Intraday ----
            FeatureDefinition("intra.opening_return_15m",            "Opening Return 15m",           "intraday", "intraday.intraday_pipeline", "intraday",
                              description="Return in first 15 minutes", lookback_window=1, leakage_risk=LEAKAGE_LOW, timeframe="intraday"),
            FeatureDefinition("intra.opening_volume_ratio_15m",      "Opening Volume Ratio 15m",     "intraday", "intraday.intraday_pipeline", "intraday",
                              description="15-min opening volume vs daily average", lookback_window=1, leakage_risk=LEAKAGE_LOW, timeframe="intraday"),
            FeatureDefinition("intra.price_vs_vwap_pct",             "Price vs VWAP %",              "intraday", "intraday.intraday_pipeline", "intraday",
                              description="(close - VWAP) / VWAP", lookback_window=1, leakage_risk=LEAKAGE_LOW, timeframe="intraday"),
            FeatureDefinition("intra.fake_breakout_score",           "Fake Breakout Score",          "intraday", "intraday.intraday_pipeline", "intraday",
                              description="0-100 fake breakout risk score", lookback_window=1, leakage_risk=LEAKAGE_LOW, timeframe="intraday", experimental=True),
            FeatureDefinition("intra.intraday_poc_price",            "Intraday POC Price",           "intraday", "intraday.intraday_pipeline", "intraday",
                              description="Point of control price from volume profile", lookback_window=1, leakage_risk=LEAKAGE_LOW, timeframe="intraday", experimental=True),
            FeatureDefinition("intra.intraday_support_pressure_score","Intraday Support/Pressure",   "intraday", "intraday.intraday_pipeline", "intraday",
                              description="Composite support/pressure score", lookback_window=1, leakage_risk=LEAKAGE_LOW, timeframe="intraday", experimental=True),
            FeatureDefinition("intra.microstructure_status",         "Microstructure Status",        "microstructure", "intraday.intraday_pipeline", "intraday",
                              description="INTRADAY_BAR_ONLY/TICK_PLANNED", lookback_window=0, leakage_risk=LEAKAGE_LOW, dtype="str"),

            # ---- Data Quality ----
            FeatureDefinition("dq.data_freshness_score",       "Data Freshness Score",       "data_quality", "quality.data_quality_gate", "data_quality",
                              description="0-100 data freshness score", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature"),
            FeatureDefinition("dq.provider_reliability_score", "Provider Reliability Score", "data_quality", "data.providers.reliability_matrix", "data_quality",
                              description="0-100 provider reliability score", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature"),
            FeatureDefinition("dq.dataset_confidence_score",   "Dataset Confidence Score",   "data_quality", "data.providers.reliability_matrix", "data_quality",
                              description="0-100 dataset confidence score", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature"),
            FeatureDefinition("dq.mock_contamination_score",   "Mock Contamination Score",   "data_quality", "quality.data_quality_gate", "data_quality",
                              description="0-1 mock data contamination ratio", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature"),

            # ---- Rule Governance ----
            FeatureDefinition("gov.active_rule_count",       "Active Rule Count",       "rule_governance", "governance.rule_registry", "rule_governance",
                              description="Number of active rules", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature", experimental=True),
            FeatureDefinition("gov.experimental_rule_count", "Experimental Rule Count", "rule_governance", "governance.rule_registry", "rule_governance",
                              description="Number of experimental rules", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature", experimental=True),
            FeatureDefinition("gov.rule_confidence_score",   "Rule Confidence Score",   "rule_governance", "governance.rule_registry", "rule_governance",
                              description="Average rule confidence score", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature", experimental=True),
            FeatureDefinition("gov.rules_needing_review",    "Rules Needing Review",    "rule_governance", "governance.rule_registry", "rule_governance",
                              description="Count of rules flagged for review", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature", experimental=True),

            # ---- Signal Quality ----
            FeatureDefinition("sig.signal_boost_count",   "Signal Boost Count",   "signal_quality", "analysis.signal_quality_engine", "signal_quality",
                              description="Number of boosted signals", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature", experimental=True),
            FeatureDefinition("sig.signal_reduce_count",  "Signal Reduce Count",  "signal_quality", "analysis.signal_quality_engine", "signal_quality",
                              description="Number of reduced signals", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature", experimental=True),
            FeatureDefinition("sig.signal_disable_count", "Signal Disable Count", "signal_quality", "analysis.signal_quality_engine", "signal_quality",
                              description="Number of disabled signals", lookback_window=0, leakage_risk=LEAKAGE_LOW,
                              notes="research_only metadata feature", experimental=True),
        ]

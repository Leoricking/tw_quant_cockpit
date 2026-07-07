"""
paper_trading/small_capital_strategy/index_ma_filter_v173.py
Index MA relationship filter for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.index_ma_filter_v173"


@dataclass
class IndexMAFilterResult:
    """Result of index vs MA relationship checks."""
    above_ma20: bool   = False
    above_ma60: bool   = False
    above_ma120: bool  = False
    above_ma240: bool  = False
    below_ma120: bool  = True
    below_ma240: bool  = True
    ma20_above_ma60: bool = False
    ma60_above_ma120: bool = False
    volume_elevated: bool = False
    bullish_alignment: bool = False
    bearish_alignment: bool = False
    detail: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


def evaluate_index_ma_filter(inp: MarketRegimeInput) -> IndexMAFilterResult:
    """Evaluate index vs all MA levels. Paper only."""
    c    = inp.index_close
    ma20 = inp.index_ma20
    ma60 = inp.index_ma60
    ma120 = inp.index_ma120
    ma240 = inp.index_ma240
    vol   = inp.index_volume_ratio

    above20  = c > ma20
    above60  = c > ma60
    above120 = c > ma120
    above240 = c > ma240
    below120 = c < ma120
    below240 = c < ma240
    ma20_above_ma60   = ma20 > ma60
    ma60_above_ma120  = ma60 > ma120
    vol_elevated      = vol > 1.2

    # Bullish: above all MAs and MA20 > MA60
    bullish = above20 and above60 and above120 and ma20_above_ma60
    # Bearish: below MA60 and MA120
    bearish = (not above60) and below120

    parts = []
    if above20:  parts.append("above_MA20")
    if above60:  parts.append("above_MA60")
    if above120: parts.append("above_MA120")
    if above240: parts.append("above_MA240")
    if vol_elevated: parts.append("vol_elevated")
    detail = f"close={c:.2f} [{','.join(parts) or 'no_signals'}]"

    return IndexMAFilterResult(
        above_ma20=above20,
        above_ma60=above60,
        above_ma120=above120,
        above_ma240=above240,
        below_ma120=below120,
        below_ma240=below240,
        ma20_above_ma60=ma20_above_ma60,
        ma60_above_ma120=ma60_above_ma120,
        volume_elevated=vol_elevated,
        bullish_alignment=bullish,
        bearish_alignment=bearish,
        detail=detail,
    )


def get_ma_levels(inp: MarketRegimeInput) -> Dict[str, float]:
    """Return dict of all MA levels."""
    return {
        "ma20": inp.index_ma20,
        "ma60": inp.index_ma60,
        "ma120": inp.index_ma120,
        "ma240": inp.index_ma240,
    }

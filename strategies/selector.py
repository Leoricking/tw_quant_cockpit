"""
strategies/selector.py - Regime-based automatic strategy selector.

Chooses the best-fit trading strategy based on the current market regime
and volatility environment:

  Bull + low volatility  → Momentum
  Bull + high volatility → Breakout
  Bear                   → MeanReversion (fade the bounces) or cash
  Sideways               → MeanReversion
"""

import logging
from typing import Any, Dict, List, Optional, Type

import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from strategies.base import BaseStrategy
from strategies.momentum import MomentumStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.breakout import BreakoutStrategy

logger = logging.getLogger(__name__)

# Regime → strategy class mapping
REGIME_STRATEGY_MAP: Dict[str, type] = {
    "bull_low_vol": MomentumStrategy,
    "bull_high_vol": BreakoutStrategy,
    "bear_low_vol": MeanReversionStrategy,
    "bear_high_vol": MeanReversionStrategy,
    "sideways_low_vol": MeanReversionStrategy,
    "sideways_high_vol": MeanReversionStrategy,
    "unknown": MomentumStrategy,
}


class StrategySelector:
    """
    Selects and delegates to the appropriate strategy based on market regime.

    Holds one instance of each available strategy and simply routes the
    ``generate_signals`` call to the active one.
    """

    def __init__(self):
        self._strategies: Dict[str, BaseStrategy] = {
            "momentum": MomentumStrategy(),
            "mean_reversion": MeanReversionStrategy(),
            "breakout": BreakoutStrategy(),
        }
        self._active_strategy_name: str = "momentum"
        self._current_regime: str = "unknown"

    # ------------------------------------------------------------------
    # Regime-based selection
    # ------------------------------------------------------------------

    def select_strategy(self, regime: str, vol_regime: str = "low") -> BaseStrategy:
        """
        Choose the appropriate strategy for the given regime.

        Parameters
        ----------
        regime : str
            Market price regime: "bull", "bear", "sideways", or "unknown".
        vol_regime : str
            Volatility regime: "high" or "low".

        Returns
        -------
        BaseStrategy
            The selected strategy instance.
        """
        key = f"{regime}_{vol_regime}_vol"
        strategy_class = REGIME_STRATEGY_MAP.get(key, MomentumStrategy)
        strategy_name = strategy_class.__name__.lower().replace("strategy", "")

        # Match class to name in _strategies dict
        name_map = {
            "momentum": "momentum",
            "meanreversion": "mean_reversion",
            "breakout": "breakout",
        }
        resolved_name = name_map.get(strategy_name, "momentum")

        self._active_strategy_name = resolved_name
        self._current_regime = f"{regime}/{vol_regime}_vol"

        logger.info(
            "Regime: %s | Vol: %s → Selected strategy: %s",
            regime, vol_regime, resolved_name,
        )
        return self._strategies[resolved_name]

    def get_active_strategy(self) -> BaseStrategy:
        """Return the currently active strategy instance."""
        return self._strategies[self._active_strategy_name]

    def get_active_strategy_name(self) -> str:
        """Return the name of the currently active strategy."""
        return self._active_strategy_name

    # ------------------------------------------------------------------
    # Signal generation (delegates to active strategy)
    # ------------------------------------------------------------------

    def generate_signals(
        self,
        feature_snapshot: pd.DataFrame,
        positions: Dict[str, float],
        portfolio_value: float,
        regime: Optional[str] = None,
        vol_regime: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Determine regime, select strategy, and generate signals.

        Enhanced with Volume Profile and Microstructure signal adjustments:
        - Bull + high microstructure_score → favour breakout/momentum
        - Price near volume pressure zone → reduce chase score
        - Price breaks above pressure zone with volume → boost breakout score
        - Weak microstructure + large intraday gain → mark fake breakout risk
        - Annotates each signal with ``no_chase_reason`` when applicable

        Parameters
        ----------
        feature_snapshot : pd.DataFrame
            Current-date feature snapshot.
        positions : dict
            Current open positions.
        portfolio_value : float
            Total portfolio value.
        regime : str, optional
            Override the regime.  If None, inferred from feature_snapshot.
        vol_regime : str, optional
            Override the volatility regime.

        Returns
        -------
        list of signal dicts
        """
        # Infer regime from snapshot if not provided
        if regime is None:
            regime = _infer_regime(feature_snapshot)
        if vol_regime is None:
            vol_regime = _infer_vol_regime(feature_snapshot)

        # ---- Microstructure-aware regime override ---------------------------
        avg_ms = _avg_column(feature_snapshot, "microstructure_score", default=0.5)
        if regime == "bull" and avg_ms > 0.6:
            # Strong buy-side pressure in bull market → lean toward momentum/breakout
            if vol_regime == "low":
                vol_regime = "high"  # treat as high-vol to trigger breakout preference

        strategy = self.select_strategy(regime, vol_regime)
        signals = strategy.generate_signals(feature_snapshot, positions, portfolio_value)

        # ---- Post-process signals with volume profile + microstructure ------
        signals = _annotate_signals(signals, feature_snapshot)
        return signals

    def reset_all(self) -> None:
        """Reset all strategy instances (clear state for a new backtest run)."""
        for strategy in self._strategies.values():
            strategy.reset()

    def describe(self) -> dict:
        """Return a summary of the selector state."""
        return {
            "active_strategy": self._active_strategy_name,
            "current_regime": self._current_regime,
            "available_strategies": list(self._strategies.keys()),
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _avg_column(df: pd.DataFrame, col: str, default: float = 0.0) -> float:
    """Return the mean of a column, or ``default`` if absent/all-NaN."""
    if col not in df.columns:
        return default
    val = df[col].mean()
    return float(val) if not pd.isna(val) else default


def _annotate_signals(
    signals: List[Dict[str, Any]],
    snapshot: pd.DataFrame,
) -> List[Dict[str, Any]]:
    """
    Enrich each signal dict with Volume Profile and Microstructure annotations.

    Added keys per signal (all optional / gracefully absent):
        no_chase_reason     : str or None — human-readable reason not to chase
        fake_breakout_risk  : bool
        microstructure_score: float or None
        vp_pressure_score   : float or None — resistance above current price
        vp_support_score    : float or None — support below current price
        chase_score_adj     : float — multiplicative adjustment to composite score
    """
    if not signals or snapshot.empty:
        return signals

    # Build per-stock lookup from snapshot
    stock_lookup: Dict[str, Any] = {}
    if "stock_id" in snapshot.columns:
        for _, row in snapshot.iterrows():
            sid = str(row["stock_id"])
            stock_lookup[sid] = row

    annotated = []
    for sig in signals:
        sig = dict(sig)  # copy to avoid mutating originals
        sid = str(sig.get("stock_id", ""))
        row = stock_lookup.get(sid, None)

        ms_score: Optional[float] = None
        vp_pressure: Optional[float] = None
        vp_support: Optional[float] = None
        vp_distance: Optional[float] = None
        fake_risk: bool = False
        no_chase_reason: Optional[str] = None
        chase_adj: float = 1.0

        if row is not None:
            # Microstructure
            if "microstructure_score" in row.index and not pd.isna(row["microstructure_score"]):
                ms_score = float(row["microstructure_score"])
            if "ms_fake_breakout_risk" in row.index:
                fake_risk = bool(row.get("ms_fake_breakout_risk", 0.0) == 1.0)
            if "ms_no_chase_flag" in row.index:
                no_chase_ms = bool(row.get("ms_no_chase_flag", 0.0) == 1.0)
            else:
                no_chase_ms = False

            # Volume Profile
            if "vp_pressure_score" in row.index and not pd.isna(row.get("vp_pressure_score")):
                vp_pressure = float(row["vp_pressure_score"])
            if "vp_support_score" in row.index and not pd.isna(row.get("vp_support_score")):
                vp_support = float(row["vp_support_score"])
            if "vp_distance_to_peak" in row.index and not pd.isna(row.get("vp_distance_to_peak")):
                vp_distance = float(row["vp_distance_to_peak"])

            # ---- Score adjustment rules ------------------------------------
            reasons = []

            # Rule 1: price is close to major volume resistance (just below peak)
            if vp_distance is not None and -0.03 < vp_distance < 0.0:
                # Close is within 3% below the peak volume price → resistance above
                chase_adj *= 0.75
                reasons.append(f"接近分價量壓力區 (距高峰 {vp_distance:.1%})")

            # Rule 2: price just broke above volume peak with volume confirmation
            vol_spike = row.get("volume_spike", 1.0) if row is not None else 1.0
            if vp_distance is not None and 0.0 < vp_distance < 0.02 and not pd.isna(vol_spike) and vol_spike > 1.5:
                # Broke above peak, volume confirmed → boost score
                chase_adj *= 1.25
                sig["breakout_confirmed"] = True

            # Rule 3: fake breakout risk
            if fake_risk:
                chase_adj *= 0.60
                reasons.append("假突破風險 (缺口開高走低，量能不足)")

            # Rule 4: microstructure weak despite price surge
            if no_chase_ms:
                chase_adj *= 0.70
                reasons.append("盤口偏弱但急漲 (不建議追價)")

            # Rule 5: very low microstructure score overall
            if ms_score is not None and ms_score < 0.35:
                chase_adj *= 0.80
                reasons.append(f"微觀結構偏空 (得分 {ms_score:.2f})")

            no_chase_reason = "；".join(reasons) if reasons else None

        sig["no_chase_reason"] = no_chase_reason
        sig["fake_breakout_risk"] = fake_risk
        sig["microstructure_score"] = ms_score
        sig["vp_pressure_score"] = vp_pressure
        sig["vp_support_score"] = vp_support
        sig["chase_score_adj"] = chase_adj

        # ---- Phase 2 annotations ----
        _phase2_reasons = []
        _rebound_warning: Optional[str] = None
        _squeeze_signal: Optional[str] = None
        _sector_linkage_reason: Optional[str] = None
        _fundamental_warning: Optional[str] = None

        if row is not None:
            # KD advanced
            if "kd_signal" in row.index and not pd.isna(row.get("kd_signal", None)):
                _kd_sig = str(row.get("kd_signal", ""))
                if _kd_sig == "BUY":
                    _phase2_reasons.append("KD 低檔黃金交叉")
                elif _kd_sig == "SELL":
                    _phase2_reasons.append("KD 高檔死亡交叉（降低追高）")

            # Bottom reversal
            if "bottom_signal" in row.index:
                _br = row.get("bottom_signal")
                if _br not in (None, "NONE", float("nan")) and not (isinstance(_br, float) and pd.isna(_br)):
                    _rebound_warning = f"破底翻/反彈訊號 [{_br}]，非強勢 A/B/C 買點"

            # Short interest
            if "short_interest_signal" in row.index:
                _si = row.get("short_interest_signal")
                if _si not in (None, float("nan")) and not (isinstance(_si, float) and pd.isna(_si)):
                    _squeeze_signal = str(_si)
                    if _si == "SQUEEZE_FUEL":
                        _phase2_reasons.append("融券軋空燃料充足")
                    elif _si == "WEAK_SHORT":
                        _phase2_reasons.append("弱勢股融券增加（非多方訊號）")

            # Sector linkage
            if "sector_rotation_reason" in row.index:
                _sr_r = row.get("sector_rotation_reason")
                if _sr_r and not (isinstance(_sr_r, float) and pd.isna(_sr_r)):
                    _sector_linkage_reason = str(_sr_r)
            if "sector_signal" in row.index:
                _ss = row.get("sector_signal")
                if _ss == "LEADER_WEAK":
                    _phase2_reasons.append("族群指標股轉弱")

            # Fundamental quality warning
            if "earnings_risk_warning" in row.index:
                _ew = row.get("earnings_risk_warning")
                if _ew and not (isinstance(_ew, float) and pd.isna(_ew)):
                    _fundamental_warning = str(_ew)
                    _phase2_reasons.append(f"財報風險：{_ew}")
            elif "fundamental_quality_score" in row.index:
                _fqs = row.get("fundamental_quality_score")
                if not pd.isna(_fqs) and float(_fqs) < 0.3:
                    _fundamental_warning = f"基本面品質低 ({_fqs:.2f})"

        sig["phase2_strategy_reason"] = "；".join(_phase2_reasons) if _phase2_reasons else None
        sig["rebound_warning"] = _rebound_warning
        sig["squeeze_signal"] = _squeeze_signal
        sig["sector_linkage_reason"] = _sector_linkage_reason
        sig["fundamental_warning"] = _fundamental_warning

        # Apply chase_adj to composite_score if present
        if "composite_score" in sig and sig["composite_score"] is not None:
            try:
                sig["composite_score"] = float(sig["composite_score"]) * chase_adj
            except (TypeError, ValueError):
                pass

        annotated.append(sig)

    return annotated


def _infer_regime(snapshot: pd.DataFrame) -> str:
    """
    Infer dominant price regime from the snapshot by majority vote.

    Uses the ``regime`` column if present, otherwise falls back to MA-crossover
    based heuristic.
    """
    if snapshot.empty:
        return "unknown"

    if "regime" in snapshot.columns:
        counts = snapshot["regime"].value_counts()
        if len(counts) > 0:
            top = counts.index[0]
            if top in ("bull", "bear", "sideways"):
                return top

    # Fallback heuristic
    if "price_above_sma20" in snapshot.columns and "sma20_above_sma60" in snapshot.columns:
        bull_score = (
            snapshot["price_above_sma20"].fillna(0).mean()
            + snapshot["sma20_above_sma60"].fillna(0).mean()
        ) / 2
        if bull_score > 0.55:
            return "bull"
        if bull_score < 0.35:
            return "bear"

    return "sideways"


def _infer_vol_regime(snapshot: pd.DataFrame) -> str:
    """
    Infer volatility regime from the snapshot by majority vote.

    Uses the ``vol_regime`` column if present.
    """
    if snapshot.empty:
        return "low"

    if "vol_regime" in snapshot.columns:
        pct_high = (snapshot["vol_regime"] == "high").mean()
        return "high" if pct_high > 0.4 else "low"

    if "vol_ratio" in snapshot.columns:
        avg_ratio = snapshot["vol_ratio"].mean()
        return "high" if (pd.notna(avg_ratio) and avg_ratio > 1.2) else "low"

    return "low"

"""
analysis/signal_quality_engine.py - Signal Quality Engine (v0.3.14).

Aggregates all available backtest and validation outputs and produces a
unified signal quality summary with BOOST / KEEP / REDUCE / DISABLE /
INSUFFICIENT_SAMPLE recommendations.

Sources integrated:
  1. Buy-point backtest    (buy_point_grade_performance.csv)
  2. Screener score        (score_bucket_performance.csv)
  3. Strategy Knowledge    (strategy_knowledge_module_performance.csv)
  4. Long-term factors     (long_term_*_factor_*.csv)
  5. Portfolio scenarios   (portfolio_config_comparison.csv)
  6. Microstructure        (coverage check — no independent backtest yet)

Output:
  data/backtest_results/signal_quality_summary.csv
  data/backtest_results/signal_quality_recommendations.csv

Rules:
  - Missing source files → graceful warning, continue.
  - real mode does NOT fallback to mock.
  - Sample count < 30 → INSUFFICIENT_SAMPLE, no recommendation.
  - Never hard-codes RELIABLE for 14-symbol universe.
  - Does not modify strategy weights or submit orders.
"""

from __future__ import annotations

import glob
import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Recommendation constants
# ---------------------------------------------------------------------------

BOOST              = "BOOST"
KEEP               = "KEEP"
REDUCE             = "REDUCE"
DISABLE            = "DISABLE"
INSUFFICIENT_SAMPLE = "INSUFFICIENT_SAMPLE"

# Unified output columns
_UNIFIED_COLS = [
    "source", "signal_name", "signal_group",
    "sample_count", "win_rate", "avg_return", "median_return",
    "profit_factor", "max_drawdown", "max_runup", "sharpe",
    "confidence", "data_quality",
    "recommendation", "reason",
    "last_updated",
]


class SignalQualityEngine:
    """
    Reads all available backtest outputs and builds a unified signal quality
    table with recommendations.
    """

    def __init__(
        self,
        results_dir: str = None,
        reports_dir: str = None,
        mode: str = "real",
    ):
        self.results_dir = results_dir or os.path.join(_BASE_DIR, "data", "backtest_results")
        self.reports_dir = reports_dir or os.path.join(_BASE_DIR, "reports")
        self.mode        = mode
        self._warnings: list[str] = []

    # ------------------------------------------------------------------
    # Public entry
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Build full signal quality summary and save CSVs.

        Returns:
            dict with keys: status, summary_df, recommendations_df,
                            warnings, sources_found, sources_missing
        """
        self._warnings = []
        all_rows: list[pd.DataFrame] = []
        sources_found: list[str]   = []
        sources_missing: list[str] = []

        loaders = [
            ("buy_point",           self.load_buy_point_quality),
            ("screener",            self.load_screener_quality),
            ("strategy_knowledge",  self.load_strategy_knowledge_quality),
            ("long_term",           self.load_long_term_quality),
            ("portfolio",           self.load_portfolio_quality),
            ("microstructure",      self.load_microstructure_quality),
        ]

        for source_name, loader in loaders:
            try:
                df = loader()
                if df is not None and not df.empty:
                    all_rows.append(df)
                    sources_found.append(source_name)
                    logger.info("SignalQualityEngine: loaded source=%s rows=%d", source_name, len(df))
                else:
                    sources_missing.append(source_name)
                    self._warnings.append(f"Source '{source_name}' returned no data.")
            except Exception as exc:
                sources_missing.append(source_name)
                self._warnings.append(f"Source '{source_name}' failed: {exc}")
                logger.warning("SignalQualityEngine: source %s failed: %s", source_name, exc)

        if not all_rows:
            return {
                "status":            "no_data",
                "summary_df":        pd.DataFrame(columns=_UNIFIED_COLS),
                "recommendations_df": pd.DataFrame(columns=_UNIFIED_COLS),
                "warnings":          self._warnings,
                "sources_found":     sources_found,
                "sources_missing":   sources_missing,
                "message":           "No backtest outputs found. Run backtests first.",
            }

        summary = pd.concat(all_rows, ignore_index=True)
        summary = self._ensure_unified_cols(summary)
        summary["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Apply recommendations
        recs = summary.apply(self._apply_recommendation, axis=1, result_type="expand")
        summary["recommendation"] = recs["recommendation"]
        summary["reason"]         = recs["reason"]

        os.makedirs(self.results_dir, exist_ok=True)
        summary_path = os.path.join(self.results_dir, "signal_quality_summary.csv")
        summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

        rec_df = summary.copy()
        rec_path = os.path.join(self.results_dir, "signal_quality_recommendations.csv")
        rec_df.to_csv(rec_path, index=False, encoding="utf-8-sig")

        logger.info("SignalQualityEngine: saved summary to %s (%d rows)", summary_path, len(summary))

        return {
            "status":            "ok",
            "summary_df":        summary,
            "recommendations_df": rec_df,
            "warnings":          self._warnings,
            "sources_found":     sources_found,
            "sources_missing":   sources_missing,
            "summary_path":      summary_path,
            "rec_path":          rec_path,
            "message":           f"Signal quality summary complete. {len(summary)} signals analyzed.",
        }

    # ------------------------------------------------------------------
    # Source loaders
    # ------------------------------------------------------------------

    def load_buy_point_quality(self) -> pd.DataFrame:
        """Load buy_point_grade_performance.csv → unified rows."""
        path = os.path.join(self.results_dir, "buy_point_grade_performance.csv")
        if not os.path.isfile(path):
            return pd.DataFrame()
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows = []
        for _, row in df.iterrows():
            grade = str(row.get("buy_point_grade", "?"))
            sc    = _safe_int(row.get("signal_count"))
            rows.append({
                "source":       "buy_point",
                "signal_name":  f"Grade_{grade}",
                "signal_group": "buy_point",
                "sample_count": sc,
                "win_rate":     _safe_float(row.get("win_rate_20d")),
                "avg_return":   _safe_float(row.get("avg_return_20d")),
                "median_return":_safe_float(row.get("median_return_20d")),
                "profit_factor":_safe_float(row.get("profit_factor")),
                "max_drawdown": _safe_float(row.get("avg_drawdown")),
                "max_runup":    None,
                "sharpe":       None,
                "confidence":   _norm_confidence(row.get("grade_confidence")),
                "data_quality": f"n={sc}; {row.get('sample_note', '')}",
            })
        return self.normalize_quality_table(pd.DataFrame(rows), "buy_point")

    def load_screener_quality(self) -> pd.DataFrame:
        """Load score_bucket_performance.csv → unified rows."""
        path = os.path.join(self.results_dir, "score_bucket_performance.csv")
        if not os.path.isfile(path):
            return pd.DataFrame()
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows = []
        for _, row in df.iterrows():
            bucket = str(row.get("score_bucket", "?"))
            sc     = _safe_int(row.get("sample_count"))
            rows.append({
                "source":       "screener",
                "signal_name":  f"score_{bucket}",
                "signal_group": "screener_score",
                "sample_count": sc,
                "win_rate":     _safe_float(row.get("win_rate_20d")),
                "avg_return":   _safe_float(row.get("avg_return_20d")),
                "median_return":None,
                "profit_factor":_safe_float(row.get("profit_factor_20d")),
                "max_drawdown": _safe_float(row.get("avg_max_drawdown")),
                "max_runup":    None,
                "sharpe":       None,
                "confidence":   _norm_confidence(row.get("bucket_confidence")),
                "data_quality": f"n={sc}; {row.get('sample_note', '')}",
            })
        return self.normalize_quality_table(pd.DataFrame(rows), "screener")

    def load_strategy_knowledge_quality(self) -> pd.DataFrame:
        """Load strategy_knowledge_module_performance.csv → unified rows."""
        path = os.path.join(self.results_dir, "strategy_knowledge_module_performance.csv")
        if not os.path.isfile(path):
            return pd.DataFrame()
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows = []
        for _, row in df.iterrows():
            module = str(row.get("module", "strategy_knowledge"))
            signal = str(row.get("signal", "?"))
            sc     = _safe_int(row.get("sample_count"))
            rows.append({
                "source":       "strategy_knowledge",
                "signal_name":  signal,
                "signal_group": module,
                "sample_count": sc,
                "win_rate":     _safe_float(row.get("win_rate")),
                "avg_return":   _safe_float(row.get("avg_return")),
                "median_return":_safe_float(row.get("median_return")),
                "profit_factor":_safe_float(row.get("profit_factor")),
                "max_drawdown": _safe_float(row.get("avg_max_drawdown")),
                "max_runup":    _safe_float(row.get("avg_max_runup")),
                "sharpe":       None,
                "confidence":   _norm_confidence(row.get("confidence")),
                "data_quality": f"n={sc}",
            })
        return self.normalize_quality_table(pd.DataFrame(rows), "strategy_knowledge")

    def load_long_term_quality(self) -> pd.DataFrame:
        """Load latest long_term_*_factor_*.csv files → unified rows."""
        factor_files = self._find_latest_factor_files()
        if not factor_files:
            return pd.DataFrame()
        all_rows = []
        for factor_name, path in factor_files.items():
            try:
                df = pd.read_csv(path, encoding="utf-8-sig")
                for _, row in df.iterrows():
                    bucket = str(row.get("bucket", "?"))
                    sc     = _safe_int(row.get("n"))
                    all_rows.append({
                        "source":       "long_term",
                        "signal_name":  f"{factor_name}_{bucket}",
                        "signal_group": f"long_term_{factor_name}",
                        "sample_count": sc,
                        "win_rate":     _safe_float(row.get("win_rate")),
                        "avg_return":   _safe_float(row.get("avg_return")),
                        "median_return":None,
                        "profit_factor":_safe_float(row.get("profit_factor")),
                        "max_drawdown": None,
                        "max_runup":    None,
                        "sharpe":       None,
                        "confidence":   _norm_confidence(row.get("confidence")),
                        "data_quality": f"n={sc}; TIMING_ESTIMATED limitation applies",
                    })
            except Exception as exc:
                logger.warning("load_long_term_quality: %s %s", path, exc)
        if not all_rows:
            return pd.DataFrame()
        return self.normalize_quality_table(pd.DataFrame(all_rows), "long_term")

    def load_portfolio_quality(self) -> pd.DataFrame:
        """Load portfolio_config_comparison.csv → unified rows."""
        path = os.path.join(self.results_dir, "portfolio_config_comparison.csv")
        if not os.path.isfile(path):
            return pd.DataFrame()
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows = []
        for _, row in df.iterrows():
            name   = str(row.get("scenario_name", "?"))
            sc     = _safe_int(row.get("trade_count"))
            sharpe = _safe_float(row.get("sharpe"))
            rows.append({
                "source":       "portfolio",
                "signal_name":  name,
                "signal_group": "portfolio_scenario",
                "sample_count": sc,
                "win_rate":     _safe_float(row.get("win_rate")),
                "avg_return":   _safe_float(row.get("total_return")),
                "median_return":None,
                "profit_factor":_safe_float(row.get("profit_factor")),
                "max_drawdown": _safe_float(row.get("max_drawdown")),
                "max_runup":    None,
                "sharpe":       sharpe,
                "confidence":   "OBSERVATIONAL",   # 14 symbols always OBSERVATIONAL
                "data_quality": (
                    f"14-symbol universe; Sharpe={sharpe:.3f} if sharpe else '—'; "
                    "Portfolio Sharpe strong but only 14 symbols"
                ),
            })
        return self.normalize_quality_table(pd.DataFrame(rows), "portfolio")

    def load_microstructure_quality(self) -> pd.DataFrame:
        """
        Microstructure quality — no independent backtest yet.
        Reports coverage status only.
        """
        # Check if intraday data exists at all
        intraday_dir = os.path.join(_BASE_DIR, "data", "import", "intraday")
        has_intraday = os.path.isdir(intraday_dir) and any(
            f.endswith(".csv") for f in os.listdir(intraday_dir)
            if not f.startswith(".")
        ) if os.path.isdir(intraday_dir) else False

        coverage_note = "Intraday data found" if has_intraday else "No intraday data found"

        signals = [
            ("opening_return_15m",  "Performance not independently validated yet"),
            ("opening_volume_ratio","Performance not independently validated yet"),
            ("opening_high_break",  "Performance not independently validated yet"),
            ("fake_breakout_warning","Performance not independently validated yet"),
            ("microstructure_coverage", coverage_note),
        ]
        rows = [{
            "source":       "microstructure",
            "signal_name":  sig,
            "signal_group": "intraday_microstructure",
            "sample_count": 0,
            "win_rate":     None,
            "avg_return":   None,
            "median_return":None,
            "profit_factor":None,
            "max_drawdown": None,
            "max_runup":    None,
            "sharpe":       None,
            "confidence":   "INSUFFICIENT",
            "data_quality": note,
        } for sig, note in signals]
        return self.normalize_quality_table(pd.DataFrame(rows), "microstructure")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def normalize_quality_table(self, df: pd.DataFrame, source_name: str) -> pd.DataFrame:
        """Ensure all unified columns exist; fill missing with None."""
        for col in _UNIFIED_COLS:
            if col not in df.columns:
                df[col] = None
        if "source" in df.columns and df["source"].isna().all():
            df["source"] = source_name
        # recommendation / reason filled later
        df["recommendation"] = df.get("recommendation", None)
        df["reason"]         = df.get("reason", None)
        df["last_updated"]   = df.get("last_updated", None)
        return df[_UNIFIED_COLS]

    def _apply_recommendation(self, row) -> dict:
        """Apply recommendation rules to a single row. Returns dict with recommendation + reason."""
        return self.calculate_recommendation(row.to_dict())

    def calculate_recommendation(self, row: dict) -> dict:
        """
        Determine BOOST / KEEP / REDUCE / DISABLE / INSUFFICIENT_SAMPLE.

        Returns dict: {recommendation: str, reason: str}
        """
        sc         = _safe_int(row.get("sample_count")) or 0
        confidence = str(row.get("confidence") or "INSUFFICIENT").upper()
        pf         = _safe_float(row.get("profit_factor"))
        avg_ret    = _safe_float(row.get("avg_return"))
        max_dd     = _safe_float(row.get("max_drawdown"))
        sharpe     = _safe_float(row.get("sharpe"))
        source     = str(row.get("source") or "")

        # INSUFFICIENT_SAMPLE
        if sc < 30 or confidence == "INSUFFICIENT" or pf is None or avg_ret is None:
            reason = _build_reason(sc=sc, confidence=confidence, pf=pf, avg_ret=avg_ret, source=source)
            return {"recommendation": INSUFFICIENT_SAMPLE, "reason": reason}

        # Special: microstructure always INSUFFICIENT for now
        if source == "microstructure":
            return {
                "recommendation": INSUFFICIENT_SAMPLE,
                "reason": "Performance not independently validated yet",
            }

        # dd_excessive only applies when value is in fraction form (between -1 and 0)
        # Buy-point / strategy-knowledge sources store avg_drawdown as raw % (e.g. -7.03)
        # Portfolio sources store max_drawdown as fraction (-0.37)
        # Guard: only treat as fraction-form drawdown when abs value <= 1
        if max_dd is not None and -1.0 <= max_dd < -0.30:
            dd_excessive = True
        else:
            dd_excessive = False

        # DISABLE
        if pf < 1.0 and avg_ret < 0 and dd_excessive:
            reason = f"PF {pf:.2f} < 1.0 and avg return negative and max drawdown excessive"
            return {"recommendation": DISABLE, "reason": reason}
        if pf < 1.0 and avg_ret < 0:
            reason = f"PF {pf:.2f} < 1.0 and avg return {avg_ret:.4f} negative"
            return {"recommendation": DISABLE, "reason": reason}

        # REDUCE
        if pf < 1.1 or avg_ret < 0 or dd_excessive:
            parts = []
            if pf < 1.1:
                parts.append(f"PF {pf:.2f} < 1.1")
            if avg_ret < 0:
                parts.append(f"avg return {avg_ret:.4f} negative")
            if dd_excessive:
                parts.append(f"max drawdown {max_dd:.2%} excessive")
            # Long-term timing warning
            if "timing_estimated" in str(row.get("data_quality") or "").lower():
                parts.append("TIMING_ESTIMATED; do not over-weight")
            return {"recommendation": REDUCE, "reason": "; ".join(parts) or "borderline performance"}

        # BOOST
        if pf >= 1.5 and avg_ret > 0:
            boost_parts = [f"PF {pf:.2f} and avg return positive"]
            if sharpe is not None and sharpe >= 1.5:
                boost_parts.append(f"Sharpe {sharpe:.2f} strong")
            if "14 symbol" in str(row.get("data_quality") or "").lower():
                boost_parts.append("Portfolio Sharpe strong but only 14 symbols")
            return {"recommendation": BOOST, "reason": "; ".join(boost_parts)}

        # KEEP
        reason = f"PF {pf:.2f}; avg return {avg_ret:.4f}; confidence {confidence}"
        return {"recommendation": KEEP, "reason": reason}

    def build_summary(self) -> pd.DataFrame:
        """
        Return the current signal_quality_summary.csv as DataFrame.
        Loads from disk if already saved.
        """
        path = os.path.join(self.results_dir, "signal_quality_summary.csv")
        if os.path.isfile(path):
            return pd.read_csv(path, encoding="utf-8-sig")
        return pd.DataFrame(columns=_UNIFIED_COLS)

    def _find_latest_factor_files(self) -> dict:
        """
        Find the most recent set of long_term_*_factor_*.csv files.
        Returns dict: {factor_name: path}
        """
        pattern = os.path.join(self.results_dir, "long_term_*_factor_*.csv")
        all_files = sorted(glob.glob(pattern))
        if not all_files:
            return {}
        # Group by factor name (eps, gm, om, val, pe, score, …)
        factor_map: dict[str, str] = {}
        for fpath in all_files:
            fname = os.path.basename(fpath)
            # long_term_<factor>_factor_<timestamp>.csv
            parts = fname.replace("long_term_", "").replace(".csv", "").split("_factor_")
            if len(parts) == 2:
                factor_name = parts[0]
                # Keep latest (files are sorted, last is newest)
                factor_map[factor_name] = fpath
        return factor_map

    def _ensure_unified_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in _UNIFIED_COLS:
            if col not in df.columns:
                df[col] = None
        return df[_UNIFIED_COLS]

    @property
    def warnings(self) -> list[str]:
        return list(self._warnings)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _safe_float(v) -> Optional[float]:
    if v is None:
        return None
    try:
        import math
        f = float(v)
        return None if math.isnan(f) else f
    except (TypeError, ValueError):
        return None


def _safe_int(v) -> Optional[int]:
    if v is None:
        return None
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def _norm_confidence(v) -> str:
    if v is None:
        return "INSUFFICIENT"
    s = str(v).strip().upper()
    if s in ("RELIABLE", "OBSERVATIONAL", "INSUFFICIENT"):
        return s
    if "RELIABLE" in s:
        return "RELIABLE"
    if "OBSERVATIONAL" in s:
        return "OBSERVATIONAL"
    return "INSUFFICIENT"


def _build_reason(sc, confidence, pf, avg_ret, source="") -> str:
    parts = []
    if sc < 30:
        parts.append(f"Sample count {sc} below 30")
    if confidence == "INSUFFICIENT":
        parts.append("Confidence INSUFFICIENT")
    if pf is None:
        parts.append("Missing profit_factor")
    if avg_ret is None:
        parts.append("Missing avg_return")
    if source == "microstructure":
        parts.append("Performance not independently validated yet")
    return "; ".join(parts) if parts else "Insufficient data"

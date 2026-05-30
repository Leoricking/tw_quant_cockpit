"""
gui/rule_weight_data_adapter.py - Data adapter for Rule Weight Tuning Lab (v0.3.15).

Loads pre-computed tuning results from CSV files, or runs the tuner on demand.

[!] Advisory only. Does NOT auto-apply weights to production strategy.
"""

from __future__ import annotations

import glob
import logging
import os
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_RESULTS_DIR = os.path.join(_BASE_DIR, "data", "backtest_results")
_DEFAULT_REPORTS_DIR = os.path.join(_BASE_DIR, "reports")


class RuleWeightDataAdapter:
    """
    Loads rule weight tuning results from disk or runs the tuner directly.

    Attributes
    ----------
    results_dir : directory containing rule_weight_*.csv files
    reports_dir : directory for Markdown report output
    """

    def __init__(
        self,
        results_dir: Optional[str] = None,
        reports_dir: Optional[str] = None,
    ):
        self.results_dir = results_dir or _DEFAULT_RESULTS_DIR
        self.reports_dir = reports_dir or _DEFAULT_REPORTS_DIR

    # ------------------------------------------------------------------
    # CSV loaders
    # ------------------------------------------------------------------

    def load_config_comparison(self) -> pd.DataFrame:
        """Load rule_weight_config_comparison.csv. Returns empty DataFrame if missing."""
        path = os.path.join(self.results_dir, "rule_weight_config_comparison.csv")
        return self._load_csv(path)

    def load_signal_effects(self) -> pd.DataFrame:
        """Load rule_weight_signal_effects.csv. Returns empty DataFrame if missing."""
        path = os.path.join(self.results_dir, "rule_weight_signal_effects.csv")
        return self._load_csv(path)

    def load_latest_report_path(self) -> Optional[str]:
        """Return path of latest rule_weight_tuning_report_*.md, or None."""
        pattern = os.path.join(self.reports_dir, "rule_weight_tuning_report_*.md")
        files = sorted(glob.glob(pattern))
        return files[-1] if files else None

    def has_results(self) -> bool:
        """True if comparison CSV exists and is non-empty."""
        df = self.load_config_comparison()
        return not df.empty

    # ------------------------------------------------------------------
    # Summary metrics (extracted from comparison CSV)
    # ------------------------------------------------------------------

    def load_summary_metrics(self) -> dict:
        """
        Extract key summary metrics from the comparison CSV.

        Returns dict with:
            n_configs, best_config_name, best_balanced_score,
            n_qualified, n_disqualified, top_sharpe_config, top_pf_config
        """
        df = self.load_config_comparison()
        if df.empty:
            return {}

        n_total = len(df)
        n_dq = int(df["disqualified"].sum()) if "disqualified" in df.columns else 0
        n_qualified = n_total - n_dq

        qualified = df[df.get("disqualified", pd.Series([False]*len(df))) == False]

        best_name = None
        best_bs = None
        if not qualified.empty and "balanced_score" in qualified.columns:
            q = qualified.dropna(subset=["balanced_score"])
            if not q.empty:
                idx = q["balanced_score"].astype(float).idxmax()
                best_name = q.loc[idx, "config_name"]
                best_bs = float(q.loc[idx, "balanced_score"])

        top_sharpe = None
        if "sharpe" in df.columns:
            df_s = df.dropna(subset=["sharpe"])
            if not df_s.empty:
                idx = df_s["sharpe"].astype(float).idxmax()
                top_sharpe = df_s.loc[idx, "config_name"]

        top_pf = None
        if "profit_factor" in df.columns:
            df_p = df.dropna(subset=["profit_factor"])
            if not df_p.empty:
                idx = df_p["profit_factor"].astype(float).idxmax()
                top_pf = df_p.loc[idx, "config_name"]

        return {
            "n_configs":            n_total,
            "n_qualified":          n_qualified,
            "n_disqualified":       n_dq,
            "best_config_name":     best_name,
            "best_balanced_score":  best_bs,
            "top_sharpe_config":    top_sharpe,
            "top_pf_config":        top_pf,
        }

    # ------------------------------------------------------------------
    # Run tuner on demand
    # ------------------------------------------------------------------

    def run_tuning(self, mode: str = "real") -> dict:
        """
        Run RuleWeightTuner directly and return results dict.
        Also saves CSVs to results_dir.

        In real mode, does NOT fall back to mock data if real CSV is absent.
        """
        try:
            from tuning.rule_weight_tuner import RuleWeightTuner
            from tuning.rule_weight_report import RuleWeightReport
            tuner = RuleWeightTuner(
                mode=mode,
                results_dir=self.results_dir,
                reports_dir=self.reports_dir,
            )
            results = tuner.run()
            return results
        except Exception as exc:
            logger.error("RuleWeightDataAdapter.run_tuning: %s", exc, exc_info=True)
            return {"status": "error", "message": str(exc)}

    def generate_report(self, results: dict) -> Optional[str]:
        """Generate Markdown report from tuning results. Returns file path."""
        try:
            from tuning.rule_weight_report import RuleWeightReport
            rpt = RuleWeightReport(results)
            return rpt.save(output_dir=self.reports_dir)
        except Exception as exc:
            logger.error("generate_report: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_csv(self, path: str) -> pd.DataFrame:
        if not os.path.exists(path):
            return pd.DataFrame()
        try:
            return pd.read_csv(path)
        except Exception as exc:
            logger.warning("Cannot load %s: %s", path, exc)
            return pd.DataFrame()

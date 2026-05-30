"""
gui/signal_quality_data_adapter.py - GUI data adapter for signal quality results (v0.3.14).

Loads signal_quality_summary.csv and related files.
Provides run_signal_quality_engine() to trigger fresh computation.

Rules:
  - Missing files → empty DataFrame, no crash.
  - run_signal_quality_engine() calls SignalQualityEngine directly (no subprocess).
  - real mode does NOT fallback to mock.
  - No order submission.
"""

from __future__ import annotations

import glob
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SignalQualityDataAdapter:
    """Reads signal quality CSV outputs from data/backtest_results/."""

    def __init__(
        self,
        results_dir: str = None,
        reports_dir: str = None,
    ):
        self.results_dir = results_dir or os.path.join(_BASE_DIR, "data", "backtest_results")
        self.reports_dir = reports_dir or os.path.join(_BASE_DIR, "reports")
        self._last_error: Optional[str] = None

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _read_csv(self, filename: str):
        try:
            import pandas as pd
            path = os.path.join(self.results_dir, filename)
            if not os.path.isfile(path):
                return pd.DataFrame()
            return pd.read_csv(path, encoding="utf-8-sig")
        except Exception as exc:
            self._last_error = f"Failed to read {filename}: {exc}"
            import pandas as pd
            return pd.DataFrame()

    # ------------------------------------------------------------------
    # Public loaders
    # ------------------------------------------------------------------

    def load_summary(self):
        """Load signal_quality_summary.csv → DataFrame."""
        return self._read_csv("signal_quality_summary.csv")

    def load_recommendations(self):
        """Load signal_quality_recommendations.csv → DataFrame."""
        return self._read_csv("signal_quality_recommendations.csv")

    def load_group_summary(self):
        """
        Aggregate summary by signal_group → group-level statistics.
        Returns empty DataFrame if summary not found.
        """
        try:
            import pandas as pd
            df = self.load_summary()
            if df.empty or "signal_group" not in df.columns:
                return pd.DataFrame()

            rows = []
            for grp, sub in df.groupby("signal_group"):
                sc_vals = sub["sample_count"].dropna() if "sample_count" in sub.columns else pd.Series(dtype=float)
                pf_vals = sub["profit_factor"].dropna() if "profit_factor" in sub.columns else pd.Series(dtype=float)
                wr_vals = sub["win_rate"].dropna() if "win_rate" in sub.columns else pd.Series(dtype=float)
                ar_vals = sub["avg_return"].dropna() if "avg_return" in sub.columns else pd.Series(dtype=float)
                dd_vals = sub["max_drawdown"].dropna() if "max_drawdown" in sub.columns else pd.Series(dtype=float)
                rec_vals = sub["recommendation"].dropna() if "recommendation" in sub.columns else pd.Series(dtype=str)

                best_signal = "—"
                worst_signal = "—"
                if "signal_name" in sub.columns and not pf_vals.empty:
                    try:
                        best_idx = sub["profit_factor"].astype(float).idxmax()
                        worst_idx = sub["profit_factor"].astype(float).idxmin()
                        best_signal  = str(sub.loc[best_idx, "signal_name"])
                        worst_signal = str(sub.loc[worst_idx, "signal_name"])
                    except Exception:
                        pass

                overall_rec = "INSUFFICIENT_SAMPLE"
                if not rec_vals.empty:
                    # Most common non-INSUFFICIENT
                    non_ins = rec_vals[rec_vals != "INSUFFICIENT_SAMPLE"]
                    if not non_ins.empty:
                        overall_rec = non_ins.mode().iloc[0]
                    else:
                        overall_rec = "INSUFFICIENT_SAMPLE"

                rows.append({
                    "signal_group": grp,
                    "signal_count": len(sub),
                    "avg_pf":       round(float(pf_vals.mean()), 3) if not pf_vals.empty else None,
                    "avg_win_rate": round(float(wr_vals.mean()), 4) if not wr_vals.empty else None,
                    "avg_return":   round(float(ar_vals.mean()), 4) if not ar_vals.empty else None,
                    "worst_mdd":    round(float(dd_vals.min()), 4) if not dd_vals.empty else None,
                    "best_signal":  best_signal,
                    "worst_signal": worst_signal,
                    "recommendation": overall_rec,
                })
            return pd.DataFrame(rows)
        except Exception as exc:
            logger.warning("load_group_summary: %s", exc)
            import pandas as pd
            return pd.DataFrame()

    def load_latest_report_path(self) -> Optional[str]:
        """Find the latest signal quality report Markdown file."""
        try:
            pattern = os.path.join(self.reports_dir, "signal_quality_report_*.md")
            files = sorted(glob.glob(pattern))
            if files:
                return files[-1]
        except Exception as exc:
            logger.warning("load_latest_report_path: %s", exc)
        return None

    def has_results(self) -> bool:
        path = os.path.join(self.results_dir, "signal_quality_summary.csv")
        return os.path.isfile(path)

    # ------------------------------------------------------------------
    # Engine runner
    # ------------------------------------------------------------------

    def run_signal_quality_engine(self, mode: str = "real") -> dict:
        """
        Call SignalQualityEngine directly (no subprocess).
        real mode does NOT fallback to mock.
        Returns dict: {status, message, summary_df, ...}
        """
        self._last_error = None
        try:
            from analysis.signal_quality_engine import SignalQualityEngine
            from reports.signal_quality_report import SignalQualityReport

            engine  = SignalQualityEngine(
                results_dir=self.results_dir,
                reports_dir=self.reports_dir,
                mode=mode,
            )
            results = engine.run()

            if results.get("status") not in ("ok",):
                msg = results.get("message", "Engine returned non-ok status")
                self._last_error = msg
                return {"status": "error", "message": msg}

            # Save Markdown report
            rpt      = SignalQualityReport(results)
            rpt_path = rpt.save(output_dir=self.reports_dir)
            results["report_path"] = rpt_path

            return results

        except Exception as exc:
            msg = f"Signal quality engine error: {exc}"
            logger.error("SignalQualityDataAdapter: %s", msg)
            self._last_error = msg
            return {"status": "error", "message": msg}

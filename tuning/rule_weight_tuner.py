"""
tuning/rule_weight_tuner.py - Rule Weight Tuning Lab engine (v0.3.15).

For each of the 7 weight configurations, runs a full portfolio simulation
and computes a balanced_score to rank configs.

Balanced score formula:
    0.35 * norm_sharpe
  + 0.25 * norm_pf
  + 0.20 * norm_return
  + 0.20 * norm_drawdown_score     (1 - norm(abs(max_drawdown)))

Disqualification constraints (config excluded from best-config selection):
    max_drawdown < -0.25  (> 25 % peak-to-trough loss)
    profit_factor < 1.20
    trade_count < 30

[!] Advisory only. Does NOT auto-apply weights to production strategy.
[!] Simulation Only. No real orders.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_RESULTS_DIR = os.path.join(_BASE_DIR, "data", "backtest_results")

# Balanced-score component weights
_BS_SHARPE    = 0.35
_BS_PF        = 0.25
_BS_RETURN    = 0.20
_BS_DRAWDOWN  = 0.20

# Disqualification thresholds
_DQ_MAX_DD      = -0.25   # max_drawdown worse than -25 %
_DQ_MIN_PF      = 1.20    # profit_factor below 1.20
_DQ_MIN_TRADES  = 30      # fewer than 30 trades


class RuleWeightTuner:
    """
    Runs 7 portfolio simulations (one per weight config) and ranks them
    by balanced_score.

    Usage::

        from tuning.rule_weight_tuner import RuleWeightTuner
        tuner = RuleWeightTuner(mode='real')
        results = tuner.run()
        # results['comparison_df']  — DataFrame with all 7 configs ranked
        # results['best_config']    — RuleWeightConfig with highest balanced_score
        # results['all_results']    — raw per-config simulation results
    """

    def __init__(
        self,
        mode: str = "real",
        start: Optional[str] = None,
        end: Optional[str] = None,
        initial_capital: float = 1_000_000,
        results_dir: Optional[str] = None,
        reports_dir: Optional[str] = None,
    ):
        self.mode            = mode
        self.start           = start
        self.end             = end
        self.initial_capital = float(initial_capital)
        self.results_dir     = results_dir or _DEFAULT_RESULTS_DIR
        self.reports_dir     = reports_dir or os.path.join(_BASE_DIR, "reports")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Run all 7 weight configurations and return ranked comparison.

        Returns dict with:
            status            : 'ok' | 'insufficient_data' | 'error'
            comparison_df     : DataFrame, one row per config, sorted by balanced_score
            all_results       : {config_name: raw_sim_result}
            best_config       : RuleWeightConfig (highest balanced_score, qualified)
            best_by_sharpe    : RuleWeightConfig
            best_by_drawdown  : RuleWeightConfig (least drawdown)
            best_by_pf        : RuleWeightConfig
            signal_effects_df : DataFrame showing weight changes vs baseline
            warnings          : list[str]
        """
        from tuning.rule_weight_scenarios import get_all_scenarios

        configs = get_all_scenarios(self.results_dir)
        all_results: Dict[str, dict] = {}
        warnings: List[str] = []

        logger.info(
            "RuleWeightTuner.run [mode=%s capital=%.0f configs=%d]",
            self.mode, self.initial_capital, len(configs),
        )

        # Run simulation for each config
        for name, cfg in configs.items():
            logger.info("Evaluating config: %s", name)
            result = self.evaluate_config(cfg)
            all_results[name] = result
            if result.get("status") not in ("ok",):
                warnings.append(
                    f"{name}: simulation status={result.get('status')} — "
                    f"{result.get('message', '')}"
                )

        # Check if we got any valid results
        valid = {k: v for k, v in all_results.items() if v.get("status") == "ok"}
        if not valid:
            first_msg = next(
                (v.get("message", "no data") for v in all_results.values()), "no data"
            )
            return {
                "status":  "insufficient_data",
                "message": first_msg,
                "all_results": all_results,
                "warnings": warnings,
            }

        # Build comparison DataFrame
        comparison_df = self._build_comparison_df(all_results, configs)
        comparison_df = self.rank_configs(comparison_df)

        # Select best configs
        best_config      = self.select_best_config(comparison_df, configs)
        best_by_sharpe   = self._best_by(comparison_df, configs, "sharpe")
        best_by_drawdown = self._best_by_drawdown(comparison_df, configs)
        best_by_pf       = self._best_by(comparison_df, configs, "profit_factor")

        # Signal effects vs baseline
        signal_effects_df = self._build_signal_effects_df(configs)

        # Save CSVs
        save_paths = self._save_results(comparison_df, signal_effects_df)

        return {
            "status":             "ok",
            "mode":               self.mode,
            "n_configs":          len(configs),
            "comparison_df":      comparison_df,
            "all_results":        all_results,
            "best_config":        best_config,
            "best_by_sharpe":     best_by_sharpe,
            "best_by_drawdown":   best_by_drawdown,
            "best_by_pf":         best_by_pf,
            "signal_effects_df":  signal_effects_df,
            "save_paths":         save_paths,
            "warnings":           warnings,
        }

    # ------------------------------------------------------------------
    # Single config evaluation
    # ------------------------------------------------------------------

    def evaluate_config(self, config) -> dict:
        """
        Run a portfolio simulation using the given RuleWeightConfig.
        Returns the raw result dict from PortfolioSimulator.run().
        """
        try:
            from backtest.portfolio_simulator import PortfolioSimulator
            sim = PortfolioSimulator(
                mode=self.mode,
                start=self.start,
                end=self.end,
                initial_capital=self.initial_capital,
                rule_weight_config=config,
            )
            result = sim.run()
            result["config_name"] = config.name
            return result
        except Exception as exc:
            logger.error("evaluate_config %s: %s", config.name, exc, exc_info=True)
            return {
                "status":      "error",
                "message":     str(exc),
                "config_name": config.name,
            }

    # ------------------------------------------------------------------
    # Comparison DataFrame
    # ------------------------------------------------------------------

    def _build_comparison_df(
        self,
        all_results: Dict[str, dict],
        configs: Dict[str, Any],
    ) -> pd.DataFrame:
        rows = []
        for name, result in all_results.items():
            cfg = configs.get(name)
            m = result.get("metrics", {}) if result.get("status") == "ok" else {}

            total_return  = m.get("total_return")
            sharpe        = m.get("sharpe")
            max_drawdown  = m.get("max_drawdown")
            profit_factor = m.get("profit_factor")
            win_rate      = m.get("win_rate")
            trade_count   = m.get("trade_count", 0)
            final_equity  = m.get("final_equity")

            # Disqualification check
            disqualified = False
            dq_reason = ""
            if result.get("status") != "ok":
                disqualified = True
                dq_reason = "sim_failed"
            elif max_drawdown is not None and float(max_drawdown) < _DQ_MAX_DD:
                disqualified = True
                dq_reason = f"max_drawdown {float(max_drawdown)*100:.1f}% > 25%"
            elif profit_factor is not None and float(profit_factor) < _DQ_MIN_PF:
                disqualified = True
                dq_reason = f"profit_factor {float(profit_factor):.2f} < 1.20"
            elif trade_count < _DQ_MIN_TRADES:
                disqualified = True
                dq_reason = f"trade_count {trade_count} < 30"

            row = {
                "config_name":     name,
                "description":     cfg.description if cfg else "",
                "status":          result.get("status", "error"),
                "total_return":    total_return,
                "sharpe":          sharpe,
                "max_drawdown":    max_drawdown,
                "profit_factor":   profit_factor,
                "win_rate":        win_rate,
                "trade_count":     trade_count,
                "final_equity":    final_equity,
                "disqualified":    disqualified,
                "dq_reason":       dq_reason,
                "balanced_score":  None,
                # Weight columns for display
                "bull_stock_w":    cfg.bull_stock_weight if cfg else None,
                "buy_point_w":     cfg.buy_point_weight if cfg else None,
                "sk_w":            cfg.strategy_knowledge_weight if cfg else None,
                "fundamental_w":   cfg.fundamental_weight if cfg else None,
                "intraday_w":      cfg.intraday_weight if cfg else None,
                "sector_w":        cfg.sector_strength_weight if cfg else None,
            }
            rows.append(row)

        return pd.DataFrame(rows)

    def rank_configs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute balanced_score for each config and sort descending.

        balanced_score = 0.35*norm_sharpe + 0.25*norm_pf
                       + 0.20*norm_return + 0.20*norm_drawdown_score
        """
        df = df.copy()

        def _norm_col(col: str, higher_is_better: bool = True) -> pd.Series:
            vals = pd.to_numeric(df[col], errors="coerce")
            mn, mx = vals.min(), vals.max()
            if mn == mx or pd.isna(mn) or pd.isna(mx):
                return pd.Series(0.5, index=df.index)
            normed = (vals - mn) / (mx - mn)
            return normed if higher_is_better else (1 - normed)

        norm_sharpe   = _norm_col("sharpe",        higher_is_better=True)
        norm_pf       = _norm_col("profit_factor", higher_is_better=True)
        norm_return   = _norm_col("total_return",  higher_is_better=True)
        # For drawdown: smaller absolute value = better → lower = worse
        norm_dd_score = _norm_col("max_drawdown",  higher_is_better=True)

        df["balanced_score"] = (
            _BS_SHARPE   * norm_sharpe
            + _BS_PF     * norm_pf
            + _BS_RETURN * norm_return
            + _BS_DRAWDOWN * norm_dd_score
        ).round(4)

        # Disqualified get NaN balanced_score
        df.loc[df["disqualified"] == True, "balanced_score"] = None

        df = df.sort_values(
            by=["disqualified", "balanced_score"],
            ascending=[True, False],
        ).reset_index(drop=True)
        df.insert(0, "rank", range(1, len(df) + 1))

        return df

    def select_best_config(
        self,
        comparison_df: pd.DataFrame,
        configs: Dict[str, Any],
    ) -> Optional[Any]:
        """Return config with highest balanced_score among qualified configs."""
        qualified = comparison_df[comparison_df["disqualified"] == False]
        if qualified.empty:
            logger.warning("All configs disqualified; returning baseline_current")
            return configs.get("baseline_current")
        best_name = qualified.iloc[0]["config_name"]
        return configs.get(best_name)

    def _best_by(
        self,
        comparison_df: pd.DataFrame,
        configs: Dict[str, Any],
        col: str,
    ) -> Optional[Any]:
        df = comparison_df.dropna(subset=[col])
        if df.empty:
            return None
        idx = df[col].astype(float).idxmax()
        name = df.loc[idx, "config_name"]
        return configs.get(name)

    def _best_by_drawdown(
        self,
        comparison_df: pd.DataFrame,
        configs: Dict[str, Any],
    ) -> Optional[Any]:
        """Return config with least-negative max_drawdown (smallest absolute loss)."""
        df = comparison_df[comparison_df["disqualified"] == False].dropna(
            subset=["max_drawdown"]
        )
        if df.empty:
            return None
        # max_drawdown is a negative fraction; highest value = least drawdown
        idx = df["max_drawdown"].astype(float).idxmax()
        name = df.loc[idx, "config_name"]
        return configs.get(name)

    # ------------------------------------------------------------------
    # Signal effects DataFrame (shows weight changes vs baseline)
    # ------------------------------------------------------------------

    def _build_signal_effects_df(self, configs: Dict[str, Any]) -> pd.DataFrame:
        from tuning.rule_weight_scenarios import BASELINE_CURRENT

        rows = []
        fields = [
            ("bull_stock_weight",          "bull_stock_score"),
            ("buy_point_weight",           "buy_point_score"),
            ("strategy_knowledge_weight",  "strategy_knowledge_score"),
            ("fundamental_weight",         "fundamental_quality_score"),
            ("intraday_weight",            "microstructure_score"),
            ("sector_strength_weight",     "sector_strength_score"),
        ]

        for weight_field, signal_name in fields:
            row = {"signal": signal_name}
            baseline_val = getattr(BASELINE_CURRENT, weight_field, 0)
            row["baseline"] = baseline_val
            for name, cfg in configs.items():
                val = getattr(cfg, weight_field, 0)
                row[name] = val
                row[f"{name}_delta"] = round(val - baseline_val, 4)
            rows.append(row)

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------

    def _save_results(
        self,
        comparison_df: pd.DataFrame,
        signal_effects_df: pd.DataFrame,
    ) -> dict:
        os.makedirs(self.results_dir, exist_ok=True)
        paths = {}

        def _save(df, name):
            if df is None or df.empty:
                return None
            p = os.path.join(self.results_dir, name)
            df.to_csv(p, index=False, encoding="utf-8-sig")
            logger.info("RuleWeightTuner saved %s", p)
            return p

        paths["comparison"]     = _save(comparison_df,    "rule_weight_config_comparison.csv")
        paths["signal_effects"] = _save(signal_effects_df, "rule_weight_signal_effects.csv")

        # Latest snapshot (overwritten on each run)
        paths["latest_comparison"] = _save(
            comparison_df, "rule_weight_config_comparison.csv"
        )
        return {k: v for k, v in paths.items() if v}

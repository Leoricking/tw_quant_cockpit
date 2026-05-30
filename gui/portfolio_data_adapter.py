"""
gui/portfolio_data_adapter.py - GUI data adapter for portfolio simulation results (v0.3.13).

Reads portfolio simulation CSV outputs from data/backtest_results/
and provides structured data for PortfolioCockpitPanel.

Rules:
  - If CSV files do not exist, returns empty DataFrame — does not crash.
  - run_simulation() calls PortfolioSimulator directly (no subprocess).
  - real mode does NOT fallback to mock.
  - No broker API calls, no order submission.
  - All errors return user-friendly warning text.
"""

from __future__ import annotations

import logging
import os
import glob
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PortfolioDataAdapter:
    """
    Loads portfolio simulation result CSVs from data/backtest_results/.
    Also provides run_simulation() to trigger a new simulation run.
    """

    def __init__(
        self,
        results_dir: str = None,
        reports_dir: str = None,
    ):
        self.results_dir = results_dir or os.path.join(_BASE_DIR, 'data', 'backtest_results')
        self.reports_dir = reports_dir or os.path.join(_BASE_DIR, 'reports')
        self._last_error: Optional[str] = None

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_csv(self, filename: str):
        """Read a CSV from results_dir. Returns empty DataFrame on any error."""
        try:
            import pandas as pd
            path = os.path.join(self.results_dir, filename)
            if not os.path.isfile(path):
                return pd.DataFrame()
            return pd.read_csv(path, encoding='utf-8-sig')
        except Exception as exc:
            logger.warning("PortfolioDataAdapter: failed to read %s: %s", filename, exc)
            self._last_error = f"Failed to read {filename}: {exc}"
            import pandas as pd
            return pd.DataFrame()

    # ------------------------------------------------------------------
    # Public load methods
    # ------------------------------------------------------------------

    def load_latest_metrics(self) -> dict:
        """
        Load portfolio_metrics.csv → dict of KPIs.
        Returns empty dict if not found.
        """
        df = self._read_csv('portfolio_metrics.csv')
        if df.empty:
            return {}
        try:
            row = df.iloc[0]
            return row.to_dict()
        except Exception as exc:
            logger.warning("load_latest_metrics error: %s", exc)
            return {}

    def load_scenario_comparison(self):
        """
        Load portfolio_config_comparison.csv → DataFrame.
        Returns empty DataFrame if not found.
        """
        return self._read_csv('portfolio_config_comparison.csv')

    def load_equity_curve(self):
        """
        Load portfolio_equity_curve.csv → DataFrame.
        Returns empty DataFrame if not found.
        """
        return self._read_csv('portfolio_equity_curve.csv')

    def load_trades(self):
        """
        Load portfolio_trades.csv → DataFrame (all simulated trades).
        Returns empty DataFrame if not found.
        """
        return self._read_csv('portfolio_trades.csv')

    def load_positions(self):
        """
        Load portfolio_daily_positions.csv → DataFrame.
        Returns empty DataFrame if not found.
        """
        return self._read_csv('portfolio_daily_positions.csv')

    def load_candidates(self):
        """
        Derive candidate ranking from trade history.
        Returns DataFrame with symbol + trade statistics, or empty DataFrame.
        """
        try:
            import pandas as pd
            trades = self.load_trades()
            if trades.empty:
                return pd.DataFrame()

            # Summarize by symbol: total trades, win rate, avg pnl
            buy_trades = trades[trades['action'].str.upper() == 'BUY'] if 'action' in trades.columns else trades
            if buy_trades.empty:
                return pd.DataFrame()

            agg = {}
            for col in ['symbol', 'name', 'sector']:
                if col in trades.columns:
                    agg[col] = 'first'

            # Use all trades (not just buys) for pnl stats
            pnl_col = None
            for c in ['pnl', 'realized_pnl', 'profit_loss']:
                if c in trades.columns:
                    pnl_col = c
                    break

            rows = []
            for sym, grp in trades.groupby('symbol') if 'symbol' in trades.columns else []:
                row = {'symbol': sym}
                if 'name' in grp.columns:
                    row['name'] = grp['name'].iloc[0]
                if 'sector' in grp.columns:
                    row['sector'] = grp['sector'].iloc[0]
                row['trade_count'] = len(grp)
                if pnl_col and pnl_col in grp.columns:
                    pnl_vals = grp[pnl_col].dropna()
                    if not pnl_vals.empty:
                        row['total_pnl'] = pnl_vals.sum()
                        row['avg_pnl'] = pnl_vals.mean()
                        row['win_count'] = int((pnl_vals > 0).sum())
                        row['win_rate'] = row['win_count'] / len(pnl_vals)
                rows.append(row)

            return pd.DataFrame(rows)
        except Exception as exc:
            logger.warning("load_candidates error: %s", exc)
            import pandas as pd
            return pd.DataFrame()

    def load_latest_report_path(self) -> Optional[str]:
        """
        Find the latest portfolio simulation report Markdown file.
        Returns path string or None if not found.
        """
        try:
            pattern = os.path.join(self.reports_dir, 'portfolio_simulation_report_*.md')
            files = sorted(glob.glob(pattern))
            if files:
                return files[-1]
        except Exception as exc:
            logger.warning("load_latest_report_path error: %s", exc)
        return None

    def has_results(self) -> bool:
        """Return True if any portfolio result CSV exists."""
        path = os.path.join(self.results_dir, 'portfolio_metrics.csv')
        return os.path.isfile(path)

    # ------------------------------------------------------------------
    # Simulation runner
    # ------------------------------------------------------------------

    def run_simulation(self, scenario: str = 'balanced', mode: str = 'real') -> dict:
        """
        Run a portfolio simulation scenario and save results.

        Calls PortfolioSimulator directly (not subprocess).
        real mode does NOT fallback to mock.

        Returns:
            dict with keys: status ('ok'/'error'), metrics, message
        """
        self._last_error = None
        try:
            if mode == 'real':
                from backtest.portfolio_simulator import PortfolioSimulator
                from backtest.portfolio_scenarios import SCENARIOS
                params = dict(SCENARIOS.get(scenario, SCENARIOS['balanced']))
                sim = PortfolioSimulator(mode='real', **params)
            else:
                from backtest.portfolio_simulator import PortfolioSimulator
                from backtest.portfolio_scenarios import SCENARIOS
                params = dict(SCENARIOS.get(scenario, SCENARIOS['balanced']))
                sim = PortfolioSimulator(mode='mock', **params)

            logger.info("PortfolioDataAdapter: running scenario=%s mode=%s", scenario, mode)
            results = sim.run()

            if results.get('status') != 'ok':
                msg = results.get('message', 'Simulation returned non-ok status')
                self._last_error = msg
                return {'status': 'error', 'message': msg}

            # Save results to CSV
            sim.save_results(results)
            logger.info("PortfolioDataAdapter: simulation complete, results saved.")
            return {'status': 'ok', 'metrics': results.get('metrics', {}), 'message': 'Simulation complete.'}

        except Exception as exc:
            msg = f"Simulation error: {exc}"
            logger.error("PortfolioDataAdapter run_simulation: %s", msg)
            self._last_error = msg
            return {'status': 'error', 'message': msg}

    def run_all_scenarios(self, mode: str = 'real') -> dict:
        """
        Run all 4 scenarios and save comparison CSV.

        Returns:
            dict with keys: status ('ok'/'error'), comparison_df, message
        """
        self._last_error = None
        try:
            from backtest.portfolio_scenarios import PortfolioScenarios
            runner = PortfolioScenarios(mode=mode)
            all_results = runner.run_all()
            runner.save_comparison(all_results)

            # Save individual metrics from balanced scenario as the "latest"
            balanced = all_results.get('balanced', {})
            if balanced.get('status') == 'ok':
                from backtest.portfolio_simulator import PortfolioSimulator, _DEFAULT_OUTPUT_DIR
                from backtest.portfolio_scenarios import SCENARIOS
                params = dict(SCENARIOS['balanced'])
                sim = PortfolioSimulator(mode=mode, **params)
                sim.save_results(balanced)

            comparison_df = runner.build_comparison_df(all_results)
            return {'status': 'ok', 'comparison_df': comparison_df, 'message': 'All scenarios complete.'}

        except Exception as exc:
            msg = f"All-scenarios error: {exc}"
            logger.error("PortfolioDataAdapter run_all_scenarios: %s", msg)
            self._last_error = msg
            return {'status': 'error', 'message': msg}

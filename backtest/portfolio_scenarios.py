"""
backtest/portfolio_scenarios.py - Batch scenario comparison for portfolio simulation (v0.3.12).

Defines 4 preset scenarios and runs them through PortfolioSimulator:
  A. conservative           - 3 positions, tight stops
  B. balanced               - 5 positions, standard params (default)
  C. aggressive             - 8 positions, wider stops
  D. no_risk_control_baseline - 10 positions, no half-TP, no trailing stop

Usage:
    from backtest.portfolio_scenarios import PortfolioScenarios
    runner = PortfolioScenarios(mode='real')
    results = runner.run_all()
    comparison_df = runner.build_comparison_df(results)
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Scenario definitions
# ---------------------------------------------------------------------------

SCENARIOS = {
    'conservative': dict(
        max_positions=3,
        position_size_pct=0.20,
        max_sector_exposure_pct=0.40,
        stop_loss_pct=0.06,
        take_profit_pct=0.15,
        trailing_stop_pct=0.08,
        use_half_take_profit=True,
    ),
    'balanced': dict(
        max_positions=5,
        position_size_pct=0.20,
        max_sector_exposure_pct=0.50,
        stop_loss_pct=0.08,
        take_profit_pct=0.20,
        trailing_stop_pct=0.10,
        use_half_take_profit=True,
    ),
    'aggressive': dict(
        max_positions=8,
        position_size_pct=0.15,
        max_sector_exposure_pct=0.60,
        stop_loss_pct=0.10,
        take_profit_pct=0.25,
        trailing_stop_pct=0.12,
        use_half_take_profit=True,
    ),
    'no_risk_control_baseline': dict(
        max_positions=10,
        position_size_pct=0.15,
        max_sector_exposure_pct=1.00,  # no sector limit
        stop_loss_pct=0.15,            # only fixed stop
        take_profit_pct=0.50,          # effectively disabled
        trailing_stop_pct=0.40,        # effectively disabled
        use_half_take_profit=False,
    ),
}

SCENARIO_NOTES = {
    'conservative':              '保守型：3 檔、緊停損、停利 15%',
    'balanced':                  '平衡型：5 檔、標準停損 8%、停利 20%',
    'aggressive':                '積極型：8 檔、寬停損 10%、停利 25%',
    'no_risk_control_baseline':  '無風控基準：10 檔、無停利一半、無移動停損',
}


class PortfolioScenarios:
    """Runs multiple portfolio scenarios and compares results."""

    def __init__(
        self,
        mode: str = 'real',
        start: Optional[str] = None,
        end: Optional[str] = None,
        initial_capital: float = 1_000_000,
    ):
        self.mode            = mode
        self.start           = start
        self.end             = end
        self.initial_capital = initial_capital

    def run_scenario(self, scenario_name: str, overrides: dict = None) -> dict:
        """
        Run a single named scenario. Returns the full results dict from PortfolioSimulator.
        overrides: optional param overrides on top of the preset.
        """
        from backtest.portfolio_simulator import PortfolioSimulator

        params = dict(SCENARIOS.get(scenario_name, SCENARIOS['balanced']))
        if overrides:
            params.update(overrides)

        logger.info("PortfolioScenarios: running scenario=%s mode=%s", scenario_name, self.mode)
        sim = PortfolioSimulator(
            mode=self.mode,
            start=self.start,
            end=self.end,
            initial_capital=self.initial_capital,
            **params,
        )
        results = sim.run()
        results['scenario_name'] = scenario_name
        results['scenario_note'] = SCENARIO_NOTES.get(scenario_name, '')
        return results

    def run_all(self) -> dict:
        """
        Run all 4 preset scenarios. Returns dict: {scenario_name: results}.
        """
        all_results = {}
        for name in SCENARIOS:
            try:
                r = self.run_scenario(name)
                all_results[name] = r
            except Exception as exc:
                logger.error("PortfolioScenarios: scenario %s failed: %s", name, exc)
                all_results[name] = {
                    'status': 'error',
                    'scenario_name': name,
                    'error': str(exc),
                }
        return all_results

    def run_selected(self, scenario_name: str, overrides: dict = None) -> dict:
        """
        Run a single scenario by name. Returns results dict.
        """
        if scenario_name not in SCENARIOS:
            logger.warning("Unknown scenario '%s', using 'balanced'", scenario_name)
            scenario_name = 'balanced'
        return self.run_scenario(scenario_name, overrides)

    # ------------------------------------------------------------------
    # Comparison table
    # ------------------------------------------------------------------

    @staticmethod
    def build_comparison_df(all_results: dict) -> pd.DataFrame:
        """
        Build a comparison DataFrame from all scenario results.

        Columns: scenario_name, total_return, annualized_return, sharpe,
                 max_drawdown, profit_factor, win_rate, trade_count,
                 avg_exposure, avg_holding_days, note
        """
        rows = []
        for name, r in all_results.items():
            if r.get('status') != 'ok':
                rows.append({
                    'scenario_name': name,
                    'status':        r.get('status', 'error'),
                    'error':         r.get('error', r.get('message', '?')),
                    'note':          SCENARIO_NOTES.get(name, ''),
                })
                continue
            m = r.get('metrics', {})
            rows.append({
                'scenario_name':    name,
                'status':           'ok',
                'total_return':     m.get('total_return'),
                'annualized_return': m.get('annualized_return'),
                'sharpe':           m.get('sharpe'),
                'max_drawdown':     m.get('max_drawdown'),
                'profit_factor':    m.get('profit_factor'),
                'win_rate':         m.get('win_rate'),
                'trade_count':      m.get('trade_count'),
                'avg_exposure':     m.get('average_exposure'),
                'avg_holding_days': m.get('avg_holding_days'),
                'final_equity':     m.get('final_equity'),
                'note':             SCENARIO_NOTES.get(name, ''),
            })
        return pd.DataFrame(rows)

    def save_comparison(
        self,
        all_results: dict,
        output_dir: str = None,
    ) -> str:
        """Save comparison CSV and return path."""
        from datetime import datetime
        if output_dir is None:
            from backtest.portfolio_simulator import _DEFAULT_OUTPUT_DIR
            output_dir = _DEFAULT_OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)

        df = self.build_comparison_df(all_results)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(output_dir, 'portfolio_config_comparison.csv')
        df.to_csv(path, index=False, encoding='utf-8-sig')
        logger.info("PortfolioScenarios: saved comparison to %s", path)
        return path

"""
backtest/screener_backtester.py - Historical screener score bucket backtester.

Replays the bull_stock_score across available history and measures whether
higher score buckets consistently produce higher forward returns.

Usage:
    from backtest.screener_backtester import ScreenerBacktester
    bt = ScreenerBacktester(mode='real', start='2024-01-01', top_n=8)
    result = bt.run()
    paths  = bt.export_results(result['raw_df'])
"""

import os
import logging

import pandas as pd

from backtest.score_validation import ScoreValidator
from backtest.stat_confidence import StatConfidence

_sc = StatConfidence()

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(_BASE_DIR, 'data', 'backtest_results')


class ScreenerBacktester:
    """
    Backtests the screener by replaying historical bull_stock_score
    across all universe symbols and measuring forward returns.

    Each (symbol, date) row represents the score state on that day
    (computed from data available up to that date only).
    Forward returns use future closes (labels only — no look-ahead in signal).
    """

    def __init__(self, mode: str = 'real', start: str = None, end: str = None, top_n: int = 8):
        self.mode   = mode
        self.start  = start
        self.end    = end
        self.top_n  = top_n
        self._validator = ScoreValidator(mode=mode, start=start, end=end, top_n=top_n)

    def build_daily_scores(self) -> pd.DataFrame:
        """Build per-(symbol, date) score records. No look-ahead in score computation."""
        return self._validator.build_records()

    def calculate_forward_returns(self, scores_df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure forward returns are present (already computed in build_daily_scores).
        Returns the same df — kept as a separate method for API conformity.
        """
        return scores_df

    def bucket_performance(self, result_df: pd.DataFrame) -> pd.DataFrame:
        """Compute per-score-bucket performance statistics."""
        return self._validator.bucket_performance(result_df)

    def run(self) -> dict:
        """
        Run screener backtest. Returns:
          {
            'status': 'ok' or 'insufficient_data',
            'raw_df': pd.DataFrame,
            'bucket_df': pd.DataFrame,
            'factor_df': pd.DataFrame,
            'n_symbols': int,
            'n_records': int,
            'start': str,
            'end':   str,
            'is_sample': bool,
            'data_source': str,
          }
        """
        logger.info("ScreenerBacktester.run() [mode=%s start=%s end=%s top_n=%d]",
                    self.mode, self.start, self.end, self.top_n)

        raw_df = self.build_daily_scores()

        if raw_df.empty:
            return {
                'status': 'insufficient_data',
                'message': '資料不足，無法完成可靠統計。',
                'raw_df': raw_df,
            }

        n_sym = raw_df['symbol'].nunique() if 'symbol' in raw_df.columns else 0
        n_rec = len(raw_df)

        bucket_df = self.bucket_performance(raw_df)
        factor_df = self._validator.factor_effectiveness(raw_df)

        if n_sym < 5:
            logger.warning("ScreenerBacktester: only %d symbols, statistical confidence low", n_sym)

        n_signals  = int(raw_df['buy_point_grade'].notna().sum()) if 'buy_point_grade' in raw_df.columns else 0
        tdays      = raw_df['date'].nunique() if 'date' in raw_df.columns else None
        confidence = _sc.evaluate(
            symbol_count=n_sym,
            signal_count=n_signals,
            trading_days=tdays,
        )
        universe_conf = _sc.evaluate_universe(n_sym)

        return {
            'status': 'ok',
            'raw_df':     raw_df,
            'bucket_df':  bucket_df,
            'factor_df':  factor_df,
            'n_symbols':  n_sym,
            'n_records':  n_rec,
            'n_signals':  n_signals,
            'trading_days': tdays,
            'start': raw_df['date'].min() if 'date' in raw_df.columns else self.start,
            'end':   raw_df['date'].max() if 'date' in raw_df.columns else self.end,
            'is_sample':    self._validator._is_sample,
            'data_source':  self._validator._data_source,
            'confidence':   confidence,
            'universe_confidence': universe_conf,
        }

    def export_results(self, result_df: pd.DataFrame, output_dir: str = None) -> dict:
        """Save backtest results to CSV files. Returns dict of output paths."""
        if output_dir is None:
            output_dir = _DEFAULT_OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        paths = {}

        if not result_df.empty:
            keep_cols = [
                'date', 'symbol', 'bull_stock_score', 'score_bucket',
                'trend_score', 'breakout_volume_score', 'theme_score',
                'fundamental_score', 'institution_score', 'holder_score',
                'margin_score', 'overheat_score', 'trust_cost_score',
                'buy_point_grade', 'buy_point_type', 'formal_allowed',
                'close',
                'forward_return_5d', 'forward_return_10d', 'forward_return_20d',
                'max_drawdown_5d', 'max_drawdown_10d', 'max_drawdown_20d',
                'hit_5d_3pct', 'hit_10d_5pct', 'hit_20d_8pct', 'stop_loss_5pct_hit',
            ]
            cols = [c for c in keep_cols if c in result_df.columns]
            p = os.path.join(output_dir, 'score_validation_raw.csv')
            result_df[cols].to_csv(p, index=False, encoding='utf-8-sig')
            paths['raw'] = p
            logger.info("ScreenerBacktester: saved raw → %s", p)

        return paths

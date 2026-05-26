"""
backtest/buy_point_backtester.py - Historical A/B/C buy-point backtester.

Detects historical buy-point signals from daily K data and measures
win rate, forward return, max drawdown, and stop-loss frequency per grade.

Signal detection is strictly backward-looking (no look-ahead bias).
Forward outcomes (win/loss) use future closes — intentional labels.

Usage:
    from backtest.buy_point_backtester import BuyPointBacktester
    bt = BuyPointBacktester(mode='real', start='2024-01-01')
    result = bt.run()
"""

import os
import logging

import numpy as np
import pandas as pd

from backtest.score_validation import ScoreValidator
from backtest.stat_confidence import StatConfidence

_sc = StatConfidence()

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(_BASE_DIR, 'data', 'backtest_results')

_STOP_LOSS_PCT  = -0.05   # -5%
_TAKE_PROFIT_PCT = 0.10   # +10%


class BuyPointBacktester:
    """
    Backtests A/B/C buy-point signals detected from historical daily K data.

    Grades:
        A — A_PULLBACK_MA10 : price pulls back to MA10, bounces, above MA20
        B — B_PULLBACK_MA5  : price touches MA5, above MA10
        C — C_PLATFORM_BREAKOUT : closes above 20d high with volume expansion

    For each signal, outcome is simulated by holding for up to 20 trading days
    with stop-loss at -5% and take-profit at +10%.
    """

    def __init__(self, mode: str = 'real', start: str = None, end: str = None, stock: str = None):
        self.mode  = mode
        self.start = start
        self.end   = end
        self.stock = stock        # if set, only backtest this symbol
        self._validator = ScoreValidator(mode=mode, start=start, end=end)

    def detect_buy_points_by_day(self) -> pd.DataFrame:
        """
        Detect all historical buy-point signals using rolling window detection.
        Returns one row per signal with entry date, symbol, grade, price.
        """
        # Reuse the rolling features from ScoreValidator
        if self.stock:
            symbols_source = self.stock  # single symbol
        else:
            symbols_source = None

        raw_df = self._validator.build_records()
        if raw_df.empty:
            return pd.DataFrame()

        # Filter to rows that have a buy signal
        if self.stock:
            raw_df = raw_df[raw_df['symbol'] == str(self.stock)]

        signals = raw_df[raw_df['buy_point_grade'].notna() & (raw_df['buy_point_type'] != 'NONE')].copy()

        # Rename to match expected output schema
        if 'close' in signals.columns:
            signals = signals.rename(columns={'close': 'entry_price'})

        # Add stop-loss and confirm prices based on grade
        if 'entry_price' in signals.columns:
            signals['stop_loss_price'] = (signals['entry_price'] * (1 + _STOP_LOSS_PCT)).round(2)
            # For A/B: support = MA20; for C: support = entry - 5%
            if 'ma20' in signals.columns:
                signals['support_price'] = signals['ma20'].where(
                    signals['buy_point_grade'].isin(['A', 'B']),
                    signals['entry_price'] * 0.95
                ).round(2)
            else:
                signals['support_price'] = (signals['entry_price'] * 0.95).round(2)
            signals['confirm_price']  = (signals['entry_price'] * 1.02).round(2)
            signals['invalid_price']  = (signals['entry_price'] * 0.95).round(2)

        signals = signals.rename(columns={'date': 'entry_date'})
        return signals.reset_index(drop=True)

    def calculate_trade_outcomes(self, signals_df: pd.DataFrame) -> pd.DataFrame:
        """
        Simulate trade outcomes for each signal.
        Holds up to 20 days, exits at stop-loss (-5%) or take-profit (+10%).
        Forward returns are labels — intentional look-ahead in outcome only.
        """
        if signals_df.empty:
            return pd.DataFrame()

        # We need the full daily K data for each symbol to simulate holding
        from data.real_data_loader import _resolve_csv, _read_csv_rows

        path, _ = _resolve_csv('daily')
        if not path:
            logger.warning("BuyPointBacktester: no daily CSV found")
            return signals_df

        # Load all daily K into per-symbol DataFrames
        all_rows = _read_csv_rows(path)
        sym_dfs  = {}
        for r in all_rows:
            sym = r.get('symbol', '')
            if not sym:
                continue
            if sym not in sym_dfs:
                sym_dfs[sym] = []
            try:
                sym_dfs[sym].append({
                    'date': r['date'],
                    'close': float(r.get('close', 0) or 0),
                    'high':  float(r.get('high',  0) or 0),
                    'low':   float(r.get('low',   0) or 0),
                })
            except (ValueError, TypeError):
                pass

        for sym in sym_dfs:
            sym_dfs[sym] = pd.DataFrame(sym_dfs[sym]).sort_values('date').reset_index(drop=True)

        outcomes = []
        for _, row in signals_df.iterrows():
            sym        = str(row.get('symbol', ''))
            entry_date = str(row.get('entry_date', ''))
            entry_px   = float(row.get('entry_price', 0) or 0)
            grade      = row.get('buy_point_grade')
            bp_type    = row.get('buy_point_type', 'NONE')

            out = row.to_dict()
            out.update({
                'exit_price': None, 'exit_date': None,
                'forward_return_5d': None, 'forward_return_10d': None,
                'forward_return_20d': None,
                'max_drawdown_before_profit': None,
                'stop_loss_hit': False, 'take_profit_hit': False,
                'win': None, 'holding_days': None,
            })

            daily = sym_dfs.get(sym, pd.DataFrame())
            if daily.empty or entry_px <= 0:
                outcomes.append(out)
                continue

            # Find the index of the entry date in the price series
            mask = daily['date'] > entry_date
            future = daily[mask].head(20)
            if future.empty:
                outcomes.append(out)
                continue

            # Forward returns (pure labels)
            fwd_closes = future['close'].values
            if len(fwd_closes) >= 5:
                out['forward_return_5d']  = round(fwd_closes[4]  / entry_px - 1, 4)
            if len(fwd_closes) >= 10:
                out['forward_return_10d'] = round(fwd_closes[9]  / entry_px - 1, 4)
            if len(fwd_closes) >= 20:
                out['forward_return_20d'] = round(fwd_closes[19] / entry_px - 1, 4)

            # Max drawdown (using daily lows)
            future_lows = future['low'].values
            min_low     = np.nanmin(future_lows) if len(future_lows) > 0 else entry_px
            out['max_drawdown_before_profit'] = round(min_low / entry_px - 1, 4)

            # Simulate stop-loss / take-profit
            exit_px  = None
            exit_day = None
            sl_hit   = False
            tp_hit   = False
            for i, (_, frow) in enumerate(future.iterrows()):
                lo  = frow['low']
                hi  = frow['high']
                cl  = frow['close']
                # Check stop-loss (intraday low)
                if lo / entry_px - 1 <= _STOP_LOSS_PCT:
                    exit_px  = round(entry_px * (1 + _STOP_LOSS_PCT), 2)
                    exit_day = i + 1
                    sl_hit   = True
                    break
                # Check take-profit (intraday high)
                if hi / entry_px - 1 >= _TAKE_PROFIT_PCT:
                    exit_px  = round(entry_px * (1 + _TAKE_PROFIT_PCT), 2)
                    exit_day = i + 1
                    tp_hit   = True
                    break
            else:
                # Exit at end of 20d window
                if len(fwd_closes) > 0:
                    exit_px  = round(fwd_closes[-1], 2)
                    exit_day = len(fwd_closes)

            if exit_px is not None:
                out['exit_price']    = exit_px
                out['holding_days']  = exit_day
                out['stop_loss_hit'] = sl_hit
                out['take_profit_hit'] = tp_hit
                out['win'] = exit_px > entry_px

            outcomes.append(out)

        return pd.DataFrame(outcomes)

    def grade_performance(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """Compute per-grade performance statistics."""
        if trades_df.empty:
            return pd.DataFrame()

        rows = []
        for grade in ['A', 'B', 'C']:
            sub   = trades_df[trades_df['buy_point_grade'] == grade]
            sub20 = sub.dropna(subset=['forward_return_20d'])
            n_sig = len(sub)
            n20   = len(sub20)

            row = {
                'buy_point_grade': grade,
                'signal_count': n_sig,
            }

            for period in ['5d', '10d', '20d']:
                ret_col = f'forward_return_{period}'
                sub_p   = sub.dropna(subset=[ret_col])
                np_     = len(sub_p)
                row[f'win_rate_{period}']  = round((sub_p[ret_col] > 0).mean() * 100, 1) if np_ >= 3 else None
                row[f'avg_return_{period}']= round(sub_p[ret_col].mean() * 100, 2)        if np_ >= 3 else None

            row['median_return_20d'] = round(sub20['forward_return_20d'].median() * 100, 2) if n20 >= 3 else None

            if 'max_drawdown_before_profit' in sub.columns:
                row['avg_drawdown'] = round(sub.dropna(subset=['max_drawdown_before_profit'])['max_drawdown_before_profit'].mean() * 100, 2)
            else:
                row['avg_drawdown'] = None

            if 'stop_loss_hit' in sub.columns:
                row['stop_loss_hit_rate'] = round(sub['stop_loss_hit'].mean() * 100, 1)
            if 'take_profit_hit' in sub.columns:
                row['take_profit_hit_rate'] = round(sub['take_profit_hit'].mean() * 100, 1)

            # Profit factor (20d)
            if n20 >= 10:
                gains  = sub20.loc[sub20['forward_return_20d'] > 0, 'forward_return_20d'].sum()
                losses = sub20.loc[sub20['forward_return_20d'] < 0, 'forward_return_20d'].abs().sum()
                row['profit_factor'] = round(gains / losses, 2) if losses > 0 else None
            else:
                row['profit_factor'] = None

            # Best / worst case
            if n20 >= 3:
                row['best_case']  = round(sub20['forward_return_20d'].max() * 100, 2)
                row['worst_case'] = round(sub20['forward_return_20d'].min() * 100, 2)
            else:
                row['best_case']  = None
                row['worst_case'] = None

            bc = _sc.evaluate_bucket(n_sig)
            row['grade_confidence'] = bc['level']
            if n_sig < 10:
                row['sample_note'] = '[WARN] sample < 10, no conclusion'
            elif n_sig < 30:
                row['sample_note'] = '[WARN] sample < 30, observational only'
            else:
                row['sample_note'] = ''

            rows.append(row)

        return pd.DataFrame(rows)

    def run(self) -> dict:
        """Run buy-point backtest. Returns dict with all results."""
        logger.info("BuyPointBacktester.run() [mode=%s start=%s end=%s stock=%s]",
                    self.mode, self.start, self.end, self.stock)

        signals_df = self.detect_buy_points_by_day()

        if signals_df.empty:
            return {
                'status': 'insufficient_data',
                'message': '資料不足，無法完成可靠統計。',
                'trades_df': pd.DataFrame(),
                'grade_df': pd.DataFrame(),
            }

        trades_df = self.calculate_trade_outcomes(signals_df)
        grade_df  = self.grade_performance(trades_df)

        n_sig    = len(signals_df)
        n_sym    = trades_df['symbol'].nunique() if 'symbol' in trades_df.columns else 0
        tdays    = trades_df['entry_date'].nunique() if 'entry_date' in trades_df.columns else None
        confidence = _sc.evaluate(
            symbol_count=n_sym,
            signal_count=n_sig,
            trading_days=tdays,
        )

        return {
            'status': 'ok',
            'trades_df': trades_df,
            'grade_df':  grade_df,
            'n_signals': n_sig,
            'is_sample': self._validator._is_sample,
            'data_source': self._validator._data_source,
            'confidence': confidence,
        }

    def save_results(self, results: dict, output_dir: str = None) -> dict:
        """Save buy-point backtest results to CSV files."""
        if output_dir is None:
            output_dir = _DEFAULT_OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        paths = {}

        trades_df = results.get('trades_df', pd.DataFrame())
        if not trades_df.empty:
            p = os.path.join(output_dir, 'buy_point_trades.csv')
            trades_df.to_csv(p, index=False, encoding='utf-8-sig')
            paths['trades'] = p
            logger.info("BuyPointBacktester: saved trades → %s", p)

        grade_df = results.get('grade_df', pd.DataFrame())
        if not grade_df.empty:
            p = os.path.join(output_dir, 'buy_point_grade_performance.csv')
            grade_df.to_csv(p, index=False, encoding='utf-8-sig')
            paths['grade'] = p
            logger.info("BuyPointBacktester: saved grade performance → %s", p)

        return paths

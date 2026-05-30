"""
backtest/portfolio_simulator.py - Portfolio & Risk Simulation engine (v0.3.12).

Simulates a multi-position portfolio using historical daily price data.
Uses simplified technical signals computed from rolling MA calculations.
Fundamental data is loaded as a static snapshot (see Data Leakage note below).

DATA LEAKAGE NOTE:
  - Technical signals: backward-looking rolling windows only — no look-ahead.
  - Entry price: signal-date close price (first version).
    Future: use next-day open to avoid same-day execution bias.
  - Fundamental data: static snapshot (latest available from CSV).
    timing_estimated=True indicates announcement_date is estimated.
    A future version should filter by announcement_date per evaluation date.
  - Forward returns are used ONLY for labelling after simulation — not for signal gen.

Fee / slippage model (simple):
  fee_rate       = 0.001425  (Taiwan buy commission)
  tax_rate_sell  = 0.003     (Taiwan stock sell tax)
  slippage_bps   = 5         (0.05% slippage per side)

Usage:
    sim = PortfolioSimulator(mode='real', initial_capital=1_000_000)
    results = sim.run()
    paths = sim.save_results(results)
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(_BASE_DIR, 'data', 'backtest_results')

# Transaction cost constants
_FEE_RATE      = 0.001425
_TAX_RATE_SELL = 0.003
_SLIPPAGE_BPS  = 5
_BUY_COST_FACTOR  = 1 + _FEE_RATE + _SLIPPAGE_BPS / 10000        # ≈1.001925
_SELL_REV_FACTOR  = 1 - _FEE_RATE - _TAX_RATE_SELL - _SLIPPAGE_BPS / 10000  # ≈0.995075

# Evaluation frequency: re-scan candidates every N trading days
_EVAL_FREQUENCY = 5


class PortfolioSimulator:
    """
    Multi-position portfolio simulator with capital allocation and risk controls.

    Candidate signals are generated from simplified rolling technical indicators
    and static fundamental snapshots. Positions are managed using stop loss,
    half take-profit, and trailing stop.
    """

    def __init__(
        self,
        mode: str = 'real',
        start: Optional[str] = None,
        end: Optional[str] = None,
        initial_capital: float = 1_000_000,
        max_positions: int = 5,
        position_size_pct: float = 0.2,
        max_sector_exposure_pct: float = 0.5,
        rebalance_frequency: str = 'daily',
        stop_loss_pct: float = 0.08,
        take_profit_pct: float = 0.20,
        trailing_stop_pct: float = 0.10,
        use_half_take_profit: bool = True,
        use_score_ranking: bool = True,
        use_fundamental_filter: bool = True,
        use_strategy_knowledge_filter: bool = True,
        strict_real_mode: bool = True,
    ):
        self.mode                       = mode
        self.start                      = start
        self.end                        = end
        self.initial_capital            = float(initial_capital)
        self.max_positions              = max_positions
        self.position_size_pct          = position_size_pct
        self.max_sector_exposure_pct    = max_sector_exposure_pct
        self.rebalance_frequency        = rebalance_frequency
        self.stop_loss_pct              = stop_loss_pct
        self.take_profit_pct            = take_profit_pct
        self.trailing_stop_pct          = trailing_stop_pct
        self.use_half_take_profit       = use_half_take_profit
        self.use_score_ranking          = use_score_ranking
        self.use_fundamental_filter     = use_fundamental_filter
        self.use_strategy_knowledge_filter = use_strategy_knowledge_filter
        self.strict_real_mode           = strict_real_mode

        # Runtime state (reset in run())
        self._cash       = 0.0
        self._positions  = {}   # sym -> position dict
        self._trades     = []
        self._equity_curve  = []
        self._daily_pos  = []
        self._is_sample  = False

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_universe(self) -> list:
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, is_sample = _resolve_csv('profile')
            if not path:
                return []
            rows = _read_csv_rows(path)
            self._is_sample = is_sample
            return [r['symbol'] for r in rows if r.get('symbol')]
        except Exception as exc:
            logger.error("PortfolioSimulator._load_universe: %s", exc)
            return []

    def _load_all_daily(self, symbols: list) -> Dict[str, pd.DataFrame]:
        """Load all daily price data (no n_bars cap) for all symbols."""
        result = {}
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, _ = _resolve_csv('daily')
            if not path:
                return result
            all_rows = _read_csv_rows(path)
            by_sym: Dict[str, list] = {}
            for r in all_rows:
                s = r.get('symbol')
                if s in symbols:
                    by_sym.setdefault(s, []).append(r)
            for sym, rows in by_sym.items():
                df = pd.DataFrame(rows)
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                df = df.dropna(subset=['close']).sort_values('date').reset_index(drop=True)
                result[sym] = df
        except Exception as exc:
            logger.error("PortfolioSimulator._load_all_daily: %s", exc)
        return result

    def _load_fund_snapshots(self, symbols: list) -> dict:
        """Load fundamental snapshot for each symbol."""
        result = {}
        for sym in symbols:
            try:
                from data.real_data_loader import RealDataLoader
                fd = RealDataLoader().load_fundamental(sym) or {}
                result[sym] = fd
            except Exception as exc:
                logger.debug("fund_snapshot %s: %s", sym, exc)
                result[sym] = {}
        return result

    def _load_sector_map(self, symbols: list) -> Dict[str, str]:
        """
        Try to load sector from universe manifest or profile.
        Falls back to 'GENERAL' for all symbols.
        """
        sector_map = {sym: 'GENERAL' for sym in symbols}
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, _ = _resolve_csv('profile')
            if path:
                rows = _read_csv_rows(path)
                for r in rows:
                    sym = r.get('symbol')
                    sec = r.get('sector') or r.get('industry') or r.get('theme') or 'GENERAL'
                    if sym:
                        sector_map[sym] = str(sec)
        except Exception:
            pass
        return sector_map

    # ------------------------------------------------------------------
    # Signal generation (simplified, backward-looking)
    # ------------------------------------------------------------------

    def _compute_signal(
        self,
        sym: str,
        past_df: pd.DataFrame,
        fund: dict,
        sector: str,
    ) -> dict:
        """
        Compute a simplified portfolio signal for one symbol at a given date.
        Uses ONLY data in past_df (no look-ahead).

        Returns candidate dict with all scoring fields.
        """
        closes  = past_df['close'].values.astype(float)
        volumes = past_df['volume'].values.astype(float) if 'volume' in past_df.columns else None
        n       = len(closes)
        price   = closes[-1]

        if price <= 0 or n < 20:
            return {}

        # ── Technical scores ───────────────────────────────────────────
        ma20  = closes[-20:].mean()   if n >= 20  else None
        ma60  = closes[-60:].mean()   if n >= 60  else None
        ma120 = closes[-120:].mean()  if n >= 120 else None

        bull_stock_score = 50.0  # base
        if ma20 and price > ma20:
            bull_stock_score += 15
        elif ma20 and price < ma20 * 0.97:
            bull_stock_score -= 10
        if ma60 and price > ma60:
            bull_stock_score += 10
        if ma120 and price > ma120:
            bull_stock_score += 5

        # Recent momentum (5-day)
        if n >= 5 and closes[-5] > 0:
            mom5 = (price - closes[-5]) / closes[-5]
            if mom5 > 0.03:
                bull_stock_score += 5
            elif mom5 < -0.05:
                bull_stock_score -= 8

        # Volume expansion (vs 20d avg)
        vol_ratio = 1.0
        if volumes is not None and n >= 20 and volumes[-20:].mean() > 0:
            vol_ratio = volumes[-1] / volumes[-20:].mean()
        microstructure_score = min(100, 50 + (vol_ratio - 1) * 30)

        # Buy-point score: recent pullback to MA support
        buy_point_score = 50.0
        if ma20 and 0.97 <= price / ma20 <= 1.03:
            buy_point_score += 20  # near MA20 support
        if n >= 3 and closes[-1] > closes[-2] > closes[-3]:
            buy_point_score += 15  # 3-bar uptrend

        # Strategy knowledge score: trend alignment
        strategy_knowledge_score = 50.0
        if ma20 and ma60:
            if ma20 > ma60:
                strategy_knowledge_score += 20
            else:
                strategy_knowledge_score -= 10
        if ma60 and ma120:
            if ma60 > ma120:
                strategy_knowledge_score += 10

        # No-chase: price extended above MA20
        no_chase_warning = bool(ma20 and price > ma20 * 1.10)

        # ── Fundamental scores ─────────────────────────────────────────
        eps_ttm    = fund.get('eps_ttm')
        gross_margin = fund.get('gross_margin')
        timing_est = bool(fund.get('announcement_date_is_estimated', False))

        fundamental_quality_score = 50.0
        fundamental_warning = False
        overvalued_warning  = False

        if eps_ttm is not None:
            if eps_ttm > 5:
                fundamental_quality_score += 20
            elif eps_ttm > 0:
                fundamental_quality_score += 10
            else:
                fundamental_quality_score -= 15
                fundamental_warning = True

        if gross_margin is not None:
            if gross_margin >= 0.40:
                fundamental_quality_score += 10
            elif gross_margin < 0.10:
                fundamental_quality_score -= 5
                fundamental_warning = True

        # Valuation (rough PE)
        if eps_ttm and eps_ttm > 0:
            pe = price / eps_ttm
            if pe > 30:
                overvalued_warning = True
                fundamental_quality_score -= 8
            elif pe < 12:
                fundamental_quality_score += 5

        sector_strength_score = 50.0  # no sector data in v0.3.12

        # ── entry_allowed ─────────────────────────────────────────────
        entry_allowed = (
            n >= 60
            and (ma60 is None or price > ma60 * 0.95)
            and not (eps_ttm is not None and eps_ttm <= 0)
        )

        # ── Assemble candidate ──────────────────────────────────────────
        return {
            'symbol':                    sym,
            'sector':                    sector,
            'bull_stock_score':          round(bull_stock_score, 1),
            'buy_point_score':           round(buy_point_score, 1),
            'strategy_knowledge_score':  round(strategy_knowledge_score, 1),
            'fundamental_quality_score': round(fundamental_quality_score, 1),
            'microstructure_score':      round(microstructure_score, 1),
            'sector_strength_score':     sector_strength_score,
            'no_chase_warning':          no_chase_warning,
            'fake_breakout_risk':        False,
            'fundamental_warning':       fundamental_warning,
            'overvalued_warning':        overvalued_warning,
            'timing_estimated':          timing_est,
            'sector_concentration_warning': False,
            'entry_allowed':             entry_allowed,
            'price':                     price,
            'eps_positive':              bool(eps_ttm and eps_ttm > 0),
        }

    def generate_signals(
        self,
        date: str,
        all_price_data: Dict[str, pd.DataFrame],
        fund_data: dict,
        sector_map: dict,
    ) -> list:
        """
        Generate candidate signals for all symbols using data up to `date`.

        Returns list of candidate dicts sorted by portfolio_rank_score desc.
        No look-ahead: only uses data where df['date'] <= date.
        """
        from backtest.portfolio_rules import PortfolioRules
        rules = PortfolioRules(
            max_positions=self.max_positions,
            position_size_pct=self.position_size_pct,
            max_sector_exposure_pct=self.max_sector_exposure_pct,
            stop_loss_pct=self.stop_loss_pct,
            take_profit_pct=self.take_profit_pct,
            trailing_stop_pct=self.trailing_stop_pct,
            use_half_take_profit=self.use_half_take_profit,
            use_score_ranking=self.use_score_ranking,
            use_fundamental_filter=self.use_fundamental_filter,
            use_strategy_knowledge_filter=self.use_strategy_knowledge_filter,
        )

        candidates = []
        for sym, df in all_price_data.items():
            past = df[df['date'] <= date]
            if len(past) < 60:
                continue
            sig = self._compute_signal(
                sym, past, fund_data.get(sym, {}), sector_map.get(sym, 'GENERAL'),
            )
            if not sig:
                continue
            sig['portfolio_rank_score'] = rules.score_candidate(sig)
            candidates.append(sig)

        return sorted(candidates, key=lambda x: x.get('portfolio_rank_score', 0), reverse=True)

    def select_positions(
        self,
        candidates: list,
    ) -> list:
        """
        Filter candidates to those that pass basic entry conditions.
        Actual position-limit / sector-limit check happens in enter_position.
        """
        selected = []
        for c in candidates:
            if not c.get('entry_allowed', True):
                continue
            if c.get('no_chase_warning') and self.use_strategy_knowledge_filter:
                continue
            score = c.get('portfolio_rank_score', 0)
            from backtest.portfolio_rules import PortfolioRules
            if score < PortfolioRules.ENTRY_SCORE_THRESHOLD:
                continue
            selected.append(c)
        return selected

    # ------------------------------------------------------------------
    # Position management
    # ------------------------------------------------------------------

    def enter_position(
        self,
        candidate: dict,
        date: str,
        price: float,
    ) -> bool:
        """
        Open a new position. Returns True if position was opened.
        Deducts cost from cash.
        """
        sym     = candidate['symbol']
        equity  = self._calculate_portfolio_value_now()

        # Recheck limits at entry time
        from backtest.portfolio_rules import PortfolioRules
        rules = PortfolioRules(
            max_positions=self.max_positions,
            position_size_pct=self.position_size_pct,
            max_sector_exposure_pct=self.max_sector_exposure_pct,
        )
        allowed, reasons = rules.can_enter_position(
            candidate, self._positions, equity, self._cash,
        )
        if not allowed:
            return False

        # Compute shares (fractional OK for simulation)
        position_value = equity * self.position_size_pct
        if position_value > self._cash:
            position_value = self._cash * 0.95  # use 95% of available cash
        if position_value < price:
            return False  # can't afford even 1 share equivalent

        shares = position_value / price
        cost   = shares * price * _BUY_COST_FACTOR
        self._cash -= cost

        stop_price     = price * (1 - self.stop_loss_pct)
        tp_price       = price * (1 + self.take_profit_pct)
        trailing_stop  = price * (1 - self.trailing_stop_pct)

        self._positions[sym] = {
            'symbol':             sym,
            'entry_date':         date,
            'entry_price':        price,
            'shares':             shares,
            'entry_value':        shares * price,
            'current_value':      shares * price,
            'sector':             candidate.get('sector', 'GENERAL'),
            'rank_score':         candidate.get('portfolio_rank_score', 0),
            'stop_loss_price':    round(stop_price, 4),
            'take_profit_price':  round(tp_price, 4),
            'peak_price':         price,
            'trailing_stop_price': round(trailing_stop, 4),
            'half_taken':         False,
            'half_shares':        0.0,
        }
        logger.debug("ENTER %s @ %.2f shares=%.2f date=%s", sym, price, shares, date)
        return True

    def update_positions(self, date: str, prices: Dict[str, float]) -> None:
        """
        Update position values and check exit conditions for all open positions.
        """
        from backtest.portfolio_rules import PortfolioRules
        rules = PortfolioRules(
            stop_loss_pct=self.stop_loss_pct,
            take_profit_pct=self.take_profit_pct,
            trailing_stop_pct=self.trailing_stop_pct,
            use_half_take_profit=self.use_half_take_profit,
        )

        for sym in list(self._positions.keys()):
            price = prices.get(sym)
            if price is None or price <= 0:
                continue

            pos = self._positions[sym]

            # Update current value
            pos['current_value'] = pos['shares'] * price

            # Check half take-profit (before trailing stop check)
            if rules.should_take_profit_half(pos, price) and not pos['half_taken']:
                half_shares = pos['shares'] / 2
                revenue = half_shares * price * _SELL_REV_FACTOR
                self._cash += revenue
                pnl = (price * _SELL_REV_FACTOR - pos['entry_price'] * _BUY_COST_FACTOR) * half_shares
                self._trades.append({
                    'symbol':      sym,
                    'entry_date':  pos['entry_date'],
                    'exit_date':   date,
                    'entry_price': pos['entry_price'],
                    'exit_price':  price,
                    'shares':      half_shares,
                    'entry_value': pos['entry_value'] / 2,
                    'exit_value':  revenue,
                    'pnl':         round(pnl, 2),
                    'return_pct':  round((price - pos['entry_price']) / pos['entry_price'], 6),
                    'holding_days': self._day_diff(pos['entry_date'], date),
                    'reason':      'TAKE_PROFIT_HALF',
                    'sector':      pos.get('sector', 'GENERAL'),
                })
                pos['shares']    -= half_shares
                pos['half_shares'] = half_shares
                pos['half_taken']  = True
                pos['peak_price']  = price
                pos['trailing_stop_price'] = round(price * (1 - self.trailing_stop_pct), 4)
                logger.debug("TAKE_PROFIT_HALF %s @ %.2f date=%s", sym, price, date)
                continue

            # Update trailing stop
            pos = rules.update_trailing_stop(pos, price)
            self._positions[sym] = pos

            # Check exit
            should_exit, reason = rules.should_exit_position(pos, price)
            if should_exit:
                self.exit_position(sym, date, price, reason)

    def exit_position(self, sym: str, date: str, price: float, reason: str) -> None:
        """Close a position completely and record the trade."""
        pos = self._positions.pop(sym, None)
        if pos is None:
            return

        shares  = pos['shares']
        revenue = shares * price * _SELL_REV_FACTOR
        self._cash += revenue
        pnl = (price * _SELL_REV_FACTOR - pos['entry_price'] * _BUY_COST_FACTOR) * shares
        self._trades.append({
            'symbol':      sym,
            'entry_date':  pos['entry_date'],
            'exit_date':   date,
            'entry_price': pos['entry_price'],
            'exit_price':  price,
            'shares':      shares,
            'entry_value': pos['entry_value'],
            'exit_value':  revenue,
            'pnl':         round(pnl, 2),
            'return_pct':  round((price - pos['entry_price']) / pos['entry_price'], 6),
            'holding_days': self._day_diff(pos['entry_date'], date),
            'reason':      reason,
            'sector':      pos.get('sector', 'GENERAL'),
        })
        logger.debug("EXIT %s @ %.2f reason=%s pnl=%.2f date=%s", sym, price, reason, pnl, date)

    # ------------------------------------------------------------------
    # Portfolio value
    # ------------------------------------------------------------------

    def _calculate_portfolio_value_now(self) -> float:
        """Cash + sum of position values."""
        invested = sum(p['current_value'] for p in self._positions.values())
        return self._cash + invested

    def calculate_portfolio_value(self, date: str, prices: Dict[str, float]) -> float:
        """Update position values then return total portfolio equity."""
        for sym, pos in self._positions.items():
            p = prices.get(sym)
            if p and p > 0:
                pos['current_value'] = pos['shares'] * p
        return self._calculate_portfolio_value_now()

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def calculate_metrics(self) -> dict:
        from backtest.portfolio_metrics import compute_all_metrics
        equity_vals = [row['equity'] for row in self._equity_curve]
        trades_df   = pd.DataFrame(self._trades) if self._trades else pd.DataFrame()
        return compute_all_metrics(
            equity_curve    = equity_vals,
            trades_df       = trades_df,
            initial_capital = self.initial_capital,
            daily_positions = self._daily_pos,
        )

    # ------------------------------------------------------------------
    # Main simulation loop
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Run the full portfolio simulation.

        Returns dict with: status, equity_curve, trades, metrics,
          daily_positions, config, confidence, n_symbols, is_sample.
        """
        logger.info(
            "PortfolioSimulator.run [mode=%s start=%s end=%s capital=%.0f pos=%d]",
            self.mode, self.start, self.end, self.initial_capital, self.max_positions,
        )

        # Real mode guard
        if self.mode == 'real' and self.strict_real_mode:
            pass  # data loading below will return empty if no real data

        # Load data
        symbols = self._load_universe()
        if not symbols:
            return {
                'status':  'insufficient_data',
                'message': '找不到 universe symbols，請先執行 data-check',
                'mode':    self.mode,
            }

        all_price_data = self._load_all_daily(symbols)
        fund_data      = self._load_fund_snapshots(symbols)
        sector_map     = self._load_sector_map(symbols)

        if not all_price_data:
            if self.mode == 'real' and self.strict_real_mode:
                return {
                    'status':  'insufficient_data',
                    'message': 'REAL MODE: 無日線資料。不允許 fallback mock。',
                    'mode':    self.mode,
                }

        # Build trading date calendar
        all_dates = sorted(set(
            str(d) for df in all_price_data.values() for d in df['date'].tolist()
        ))
        if self.start:
            all_dates = [d for d in all_dates if d >= self.start]
        if self.end:
            all_dates = [d for d in all_dates if d <= self.end]

        if len(all_dates) < 2:
            return {
                'status':  'insufficient_data',
                'message': f'資料日期不足（{len(all_dates)} days）',
                'mode':    self.mode,
                'n_symbols': len(symbols),
            }

        # Initialize state
        self._cash      = self.initial_capital
        self._positions = {}
        self._trades    = []
        self._equity_curve  = []
        self._daily_pos = []

        # Pre-build date → price lookup for speed
        price_lookup: Dict[str, Dict[str, float]] = {}
        for sym, df in all_price_data.items():
            for _, row in df.iterrows():
                d = str(row['date'])
                if d not in price_lookup:
                    price_lookup[d] = {}
                price_lookup[d][sym] = float(row['close'])

        # ── Simulation loop ───────────────────────────────────────────
        eval_counter = 0
        for date in all_dates:
            prices = price_lookup.get(date, {})

            # 1. Update positions (exit conditions)
            self.update_positions(date, prices)

            # 2. Every _EVAL_FREQUENCY days: scan for new candidates
            if eval_counter % _EVAL_FREQUENCY == 0:
                candidates = self.generate_signals(date, all_price_data, fund_data, sector_map)
                selected   = self.select_positions(candidates)
                for cand in selected:
                    sym   = cand['symbol']
                    price = prices.get(sym)
                    if price and price > 0 and sym not in self._positions:
                        self.enter_position(cand, date, price)

            eval_counter += 1

            # 3. Record equity
            equity = self.calculate_portfolio_value(date, prices)
            invested = sum(p['current_value'] for p in self._positions.values())
            self._equity_curve.append({'date': date, 'equity': equity})
            self._daily_pos.append({'date': date, 'invested_value': invested})

        # 4. Close all remaining positions at last date
        last_date = all_dates[-1]
        last_prices = price_lookup.get(last_date, {})
        for sym in list(self._positions.keys()):
            p = last_prices.get(sym)
            if p and p > 0:
                self.exit_position(sym, last_date, p, 'END_OF_SIMULATION')

        # ── Metrics ───────────────────────────────────────────────────
        metrics  = self.calculate_metrics()
        trades_df = pd.DataFrame(self._trades) if self._trades else pd.DataFrame()
        equity_df = pd.DataFrame(self._equity_curve)
        daily_df  = pd.DataFrame(self._daily_pos)

        # Confidence
        from backtest.stat_confidence import StatConfidence
        n_syms   = len([sym for sym in symbols if sym in all_price_data])
        n_trades = len(self._trades)
        t_days   = len(all_dates)
        confidence = StatConfidence.for_portfolio_simulation(
            symbol_count=n_syms,
            trade_count=n_trades,
            trading_days=t_days,
            scenario_count=1,
        )

        # timing_estimated ratio
        timing_count = sum(
            1 for sym in symbols
            if fund_data.get(sym, {}).get('announcement_date_is_estimated')
        )
        timing_ratio = round(timing_count / max(n_syms, 1), 3)

        config = {
            'mode':                   self.mode,
            'initial_capital':        self.initial_capital,
            'max_positions':          self.max_positions,
            'position_size_pct':      self.position_size_pct,
            'max_sector_exposure_pct': self.max_sector_exposure_pct,
            'stop_loss_pct':          self.stop_loss_pct,
            'take_profit_pct':        self.take_profit_pct,
            'trailing_stop_pct':      self.trailing_stop_pct,
            'use_half_take_profit':   self.use_half_take_profit,
            'fee_rate':               _FEE_RATE,
            'tax_rate_sell':          _TAX_RATE_SELL,
            'slippage_bps':           _SLIPPAGE_BPS,
            'entry_price_note':       'signal-date close (first version; future: next-day open)',
        }

        return {
            'status':           'ok',
            'mode':             self.mode,
            'n_symbols':        n_syms,
            'start':            all_dates[0]  if all_dates else None,
            'end':              all_dates[-1] if all_dates else None,
            'trading_days':     t_days,
            'equity_df':        equity_df,
            'trades_df':        trades_df,
            'daily_positions_df': daily_df,
            'metrics':          metrics,
            'confidence':       confidence,
            'config':           config,
            'is_sample':        self._is_sample,
            'timing_estimated_ratio': timing_ratio,
        }

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------

    def save_results(
        self,
        results: dict,
        output_dir: Optional[str] = None,
    ) -> dict:
        """Save CSVs to output_dir, return paths dict."""
        out_dir = output_dir or _DEFAULT_OUTPUT_DIR
        os.makedirs(out_dir, exist_ok=True)
        paths   = {}
        ts      = datetime.now().strftime('%Y%m%d_%H%M%S')

        def _save(df, name):
            if df is None or (hasattr(df, 'empty') and df.empty):
                return None
            p = os.path.join(out_dir, name)
            df.to_csv(p, index=False, encoding='utf-8-sig')
            logger.info("PortfolioSimulator: saved %s", p)
            return p

        paths['equity_curve']      = _save(results.get('equity_df'), 'portfolio_equity_curve.csv')
        paths['trades']            = _save(results.get('trades_df'),  'portfolio_trades.csv')
        paths['daily_positions']   = _save(results.get('daily_positions_df'), 'portfolio_daily_positions.csv')

        # Metrics as single-row CSV
        m = results.get('metrics', {})
        if m:
            paths['metrics'] = _save(pd.DataFrame([m]), 'portfolio_metrics.csv')

        return {k: v for k, v in paths.items() if v}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _day_diff(date1: str, date2: str) -> int:
        """Approximate calendar-day difference between two YYYY-MM-DD strings."""
        try:
            from datetime import datetime as _dt
            d1 = _dt.strptime(str(date1)[:10], '%Y-%m-%d')
            d2 = _dt.strptime(str(date2)[:10], '%Y-%m-%d')
            return abs((d2 - d1).days)
        except Exception:
            return 0

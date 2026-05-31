"""
backtest/hardened_backtester.py — Hardened Backtest Engine (v0.3.26).

Integrates ExecutionModel, CostModel, LiquidityFilter, GapRiskModel,
ValidationSplit, and MarketRegimeSplitter into a unified hardened backtest.

Does NOT replace existing backtests. Existing backtests unchanged.

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    import numpy as np
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False
    logger.warning("pandas/numpy not available — HardenedBacktester degraded mode")

from backtest.execution_model import ExecutionModel
from backtest.cost_model import CostModel
from backtest.liquidity_filter import LiquidityFilter
from backtest.gap_risk_model import GapRiskModel
from backtest.validation_split import ValidationSplit
from backtest.regime_split import MarketRegimeSplitter


class HardenedBacktester:
    """
    Hardened Backtest Engine.

    Integrates realistic execution, cost, liquidity, gap risk, validation
    splits, and regime classification for robust backtest evaluation.

    Does NOT replace existing backtests. Existing backtests are unchanged.

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    VERSION = "0.3.26"

    def __init__(
        self,
        mode: str = "real",
        entry_model: str = "next_open",
        exit_model: str = "combined",
        cost_model: str = "taiwan_realistic",
        split_method: str = "walk_forward",
        max_holding_days: int = 20,
        stop_loss_pct: float = 0.08,
        take_profit_pct: float = 0.20,
        use_liquidity_filter: bool = True,
        use_gap_risk: bool = True,
        use_regime_split: bool = True,
        results_dir: str = "data/backtest_results",
        report_dir: str = "reports",
        zero_cost: bool = False,
    ) -> None:
        self.mode = mode
        self.entry_model = entry_model
        self.exit_model = exit_model
        self.cost_model_name = cost_model
        self.split_method = split_method
        self.max_holding_days = max_holding_days
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.use_liquidity_filter = use_liquidity_filter
        self.use_gap_risk = use_gap_risk
        self.use_regime_split = use_regime_split
        self.results_dir = os.path.join(BASE_DIR, results_dir)
        self.report_dir = os.path.join(BASE_DIR, report_dir)
        self.zero_cost = zero_cost

        # Instantiate sub-models
        self.execution = ExecutionModel(
            entry_model=entry_model,
            exit_model=exit_model,
            max_holding_days=max_holding_days,
            stop_loss_pct=stop_loss_pct,
            take_profit_pct=take_profit_pct,
        )
        self.costs = CostModel.from_preset("zero_cost" if zero_cost else cost_model)
        self.liquidity = LiquidityFilter() if use_liquidity_filter else None
        self.gap_risk = GapRiskModel() if use_gap_risk else None
        self.splitter = ValidationSplit(method=split_method)
        self.regime = MarketRegimeSplitter() if use_regime_split else None

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(
        self,
        signals_df=None,
        price_data: dict | None = None,
    ) -> dict:
        """
        Run the hardened backtest.

        Returns:
            status, trade_count, net_return, sharpe, max_drawdown,
            profit_factor, win_rate, confidence_grade, assumptions,
            trades_path, metrics_path, warnings
        """
        warnings_list = []
        base_result = {
            "status": "OK",
            "version": self.VERSION,
            "trade_count": 0,
            "net_return": 0.0,
            "gross_return": 0.0,
            "sharpe": None,
            "max_drawdown": None,
            "profit_factor": None,
            "win_rate": None,
            "confidence_grade": "D",
            "assumptions": {},
            "trades_path": None,
            "metrics_path": None,
            "warnings": [],
            "note": "Research Only / Backtest Only / No Real Orders. Production Trading: BLOCKED.",
        }

        try:
            # Load price data if not provided
            if price_data is None:
                price_data = self._load_price_data()

            if not price_data:
                logger.warning("HardenedBacktester: no price data available")
                base_result["status"] = "INSUFFICIENT_DATA"
                base_result["warnings"].append("No price data available")
                base_result["assumptions"] = self.build_assumption_summary()
                return base_result

            # Generate signals
            signals = self.prepare_signals(price_data) if signals_df is None else self._df_to_signals(signals_df)

            if not signals:
                logger.warning("HardenedBacktester: no signals generated")
                warnings_list.append("No signals generated from price data")
                base_result["status"] = "INSUFFICIENT_DATA"
                base_result["warnings"] = warnings_list
                base_result["assumptions"] = self.build_assumption_summary()
                return base_result

            # Simulate trades
            trades = self.simulate_trades(signals, price_data)

            if not trades:
                logger.warning("HardenedBacktester: no trades simulated")
                warnings_list.append("No trades simulated")
                base_result["status"] = "INSUFFICIENT_DATA"
                base_result["warnings"] = warnings_list
                base_result["assumptions"] = self.build_assumption_summary()
                return base_result

            # Apply costs
            trades = self.apply_costs(trades)

            # Calculate metrics
            metrics = self.calculate_metrics(trades)
            if "warning" in metrics:
                warnings_list.append(metrics["warning"])

            # Split and regime metrics
            first_symbol = list(price_data.keys())[0]
            market_df = price_data.get(first_symbol)

            split_metrics = self.calculate_split_metrics(trades, price_data)
            regime_metrics = self.calculate_regime_metrics(trades, market_df)

            # Confidence grade
            confidence_grade = self._compute_confidence_grade(metrics, split_metrics)
            metrics["confidence_grade"] = confidence_grade

            # Assumptions
            assumptions = self.build_assumption_summary()

            # Save results
            paths = self.save_results(trades, metrics, split_metrics, regime_metrics, assumptions)

            result = {**base_result}
            result.update({
                "status": "OK",
                "trade_count": metrics.get("trade_count", len(trades)),
                "net_return": metrics.get("net_return", 0.0),
                "gross_return": metrics.get("gross_return", 0.0),
                "sharpe": metrics.get("sharpe"),
                "max_drawdown": metrics.get("max_drawdown"),
                "profit_factor": metrics.get("profit_factor"),
                "win_rate": metrics.get("win_rate"),
                "confidence_grade": confidence_grade,
                "assumptions": assumptions,
                "trades_path": paths.get("trades"),
                "metrics_path": paths.get("metrics"),
                "split_metrics": split_metrics,
                "regime_metrics": regime_metrics,
                "warnings": warnings_list,
                "cost_impact": metrics.get("cost_impact"),
            })
            return result

        except Exception as exc:
            logger.error("HardenedBacktester.run error: %s", exc, exc_info=True)
            base_result["status"] = "ERROR"
            base_result["error"] = str(exc)
            base_result["warnings"] = warnings_list + [f"Internal error: {exc}"]
            return base_result

    # ------------------------------------------------------------------
    # Signal preparation
    # ------------------------------------------------------------------

    def prepare_signals(self, price_data: dict) -> list:
        """
        Generate simple MA20 crossover signals from price data.

        Returns list of dicts: symbol, signal_date, signal_type
        """
        if not _PANDAS_AVAILABLE:
            return []

        signals = []
        for symbol, df in price_data.items():
            try:
                if df is None or df.empty:
                    continue
                dfc = df.copy()
                dfc.columns = [c.lower() for c in dfc.columns]
                if "close" not in dfc.columns:
                    continue

                dfc["ma20"] = dfc["close"].rolling(20, min_periods=1).mean()
                dfc["prev_close"] = dfc["close"].shift(1)
                dfc["prev_ma20"] = dfc["ma20"].shift(1)

                # Crossover signal: close crosses above MA20
                for idx, row in dfc.iterrows():
                    try:
                        c = row.get("close")
                        ma = row.get("ma20")
                        pc = row.get("prev_close")
                        pma = row.get("prev_ma20")
                        if c is None or ma is None or pc is None or pma is None:
                            continue
                        if pd.isna(c) or pd.isna(ma) or pd.isna(pc) or pd.isna(pma):
                            continue
                        if c > ma and pc <= pma:
                            signals.append({
                                "symbol": symbol,
                                "signal_date": str(idx),
                                "signal_type": "BUY",
                            })
                    except Exception:
                        continue
            except Exception as exc:
                logger.warning("prepare_signals error for %s: %s", symbol, exc)
                continue

        return signals

    def _df_to_signals(self, signals_df) -> list:
        """Convert a signals DataFrame to a list of dicts."""
        if signals_df is None:
            return []
        try:
            return signals_df.to_dict(orient="records")
        except Exception:
            return []

    # ------------------------------------------------------------------
    # Trade simulation
    # ------------------------------------------------------------------

    def simulate_trades(self, signals: list, price_data: dict) -> list:
        """
        Simulate trades from signals using ExecutionModel, LiquidityFilter, GapRiskModel.

        Returns list of trade dicts.
        """
        trades = []
        for sig in signals:
            try:
                symbol = sig.get("symbol")
                signal_date = sig.get("signal_date")
                signal_type = sig.get("signal_type", "BUY")

                if symbol not in price_data:
                    continue

                df = price_data[symbol]
                if df is None or df.empty:
                    continue

                # Resolve entry
                entry_result = self.execution.resolve_entry_price(df, signal_date, symbol)
                if entry_result["status"] != "OK" or entry_result["price"] is None:
                    trades.append({
                        "symbol": symbol,
                        "signal_date": signal_date,
                        "status": entry_result["status"],
                        "entry_price": None,
                        "exit_price": None,
                        "net_pnl": 0.0,
                    })
                    continue

                entry_price = entry_result["price"]
                entry_date = entry_result["date"]

                # Liquidity check
                liquidity_allowed = True
                liquidity_score = 100.0
                if self.liquidity is not None:
                    try:
                        norm_df = self.execution._normalize_df(df)
                        if norm_df is not None and entry_date in norm_df.index:
                            row = norm_df.loc[entry_date].to_dict()
                            liq = self.liquidity.check_entry_allowed(row)
                            liquidity_allowed = liq["allowed"]
                            liquidity_score = liq["liquidity_score"]
                    except Exception as exc:
                        logger.warning("Liquidity check error for %s: %s", symbol, exc)

                if not liquidity_allowed:
                    trades.append({
                        "symbol": symbol,
                        "signal_date": signal_date,
                        "entry_date": entry_date,
                        "entry_price": entry_price,
                        "status": "LIQUIDITY_REJECTED",
                        "liquidity_allowed": False,
                        "liquidity_score": liquidity_score,
                        "exit_price": None,
                        "net_pnl": 0.0,
                    })
                    continue

                # Gap risk check
                gap_status = "NO_GAP"
                gap_blocked = False
                if self.gap_risk is not None:
                    try:
                        norm_df = self.execution._normalize_df(df)
                        if norm_df is not None and entry_date in norm_df.index:
                            entry_loc = norm_df.index.get_loc(entry_date)
                            if entry_loc > 0:
                                prev_close = self.execution._safe_get(norm_df.iloc[entry_loc - 1], "close")
                                next_open = self.execution._safe_get(norm_df.iloc[entry_loc], "open")
                                if prev_close and next_open:
                                    gap_pct = self.gap_risk.calculate_gap(prev_close, next_open)
                                    gap_status = self.gap_risk.classify_gap(gap_pct)
                                    gap_blocked = self.gap_risk.should_block_entry(gap_pct)
                    except Exception as exc:
                        logger.warning("Gap risk check error for %s: %s", symbol, exc)

                if gap_blocked:
                    trades.append({
                        "symbol": symbol,
                        "signal_date": signal_date,
                        "entry_date": entry_date,
                        "entry_price": entry_price,
                        "status": "GAP_BLOCKED",
                        "gap_status": gap_status,
                        "liquidity_allowed": liquidity_allowed,
                        "liquidity_score": liquidity_score,
                        "exit_price": None,
                        "net_pnl": 0.0,
                    })
                    continue

                # Resolve exit
                exit_result = self.execution.resolve_exit_price(df, entry_date, entry_price, symbol)
                if exit_result["status"] != "OK" or exit_result["price"] is None:
                    trades.append({
                        "symbol": symbol,
                        "signal_date": signal_date,
                        "entry_date": entry_date,
                        "entry_price": entry_price,
                        "exit_date": None,
                        "exit_price": None,
                        "exit_reason": "INSUFFICIENT_DATA",
                        "status": "INSUFFICIENT_DATA",
                        "liquidity_allowed": liquidity_allowed,
                        "liquidity_score": liquidity_score,
                        "gap_status": gap_status,
                        "gross_pnl": 0.0,
                        "net_pnl": 0.0,
                    })
                    continue

                exit_price = exit_result["price"]
                exit_date = exit_result["exit_date"]
                exit_reason = exit_result["exit_reason"]
                gross_pnl = exit_price - entry_price

                trades.append({
                    "symbol": symbol,
                    "signal_date": signal_date,
                    "entry_date": entry_date,
                    "entry_price": entry_price,
                    "exit_date": exit_date,
                    "exit_price": exit_price,
                    "exit_reason": exit_reason,
                    "gross_pnl": round(gross_pnl, 4),
                    "net_pnl": round(gross_pnl, 4),  # updated by apply_costs
                    "status": "OK",
                    "liquidity_allowed": liquidity_allowed,
                    "liquidity_score": liquidity_score,
                    "gap_status": gap_status,
                })

            except Exception as exc:
                logger.error("simulate_trades error for signal %s: %s", sig, exc)
                continue

        return trades

    # ------------------------------------------------------------------
    # Cost application
    # ------------------------------------------------------------------

    def apply_costs(self, trades: list) -> list:
        """Apply CostModel to each completed trade."""
        result = []
        for trade in trades:
            try:
                if trade.get("status") != "OK":
                    result.append(trade)
                    continue
                ep = trade.get("entry_price")
                xp = trade.get("exit_price")
                if ep is None or xp is None:
                    result.append(trade)
                    continue

                cost_result = self.costs.apply_round_trip_cost(
                    entry_price=ep,
                    exit_price=xp,
                    shares=1000,  # normalized to 1000 shares
                )
                trade = {**trade}
                trade["gross_pnl"] = cost_result["gross_pnl"] / 1000.0
                trade["buy_cost"] = cost_result["buy_cost"] / 1000.0
                trade["sell_cost"] = cost_result["sell_cost"] / 1000.0
                trade["total_cost"] = cost_result["total_cost"] / 1000.0
                trade["net_pnl"] = cost_result["net_pnl"] / 1000.0
                trade["cost_impact_pct"] = cost_result["cost_impact_pct"]
                result.append(trade)
            except Exception as exc:
                logger.error("apply_costs error: %s", exc)
                result.append(trade)
        return result

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def calculate_metrics(self, trades: list) -> dict:
        """
        Calculate portfolio metrics from trade list.

        Returns sharpe, max_drawdown, win_rate, profit_factor,
                total_return, trade_count, gross_return, net_return, cost_impact
        """
        completed = [t for t in trades if t.get("status") == "OK"]
        trade_count = len(completed)
        base = {
            "trade_count": trade_count,
            "total_trades_attempted": len(trades),
            "net_return": 0.0,
            "gross_return": 0.0,
            "sharpe": None,
            "max_drawdown": None,
            "profit_factor": None,
            "win_rate": None,
            "cost_impact": None,
        }

        if trade_count == 0:
            base["warning"] = "no_completed_trades"
            return base

        if trade_count < 5:
            base["warning"] = f"only_{trade_count}_trades_insufficient_for_reliable_metrics"

        net_pnls = [t.get("net_pnl", 0.0) or 0.0 for t in completed]
        gross_pnls = [t.get("gross_pnl", 0.0) or 0.0 for t in completed]
        entry_prices = [t.get("entry_price", 1.0) or 1.0 for t in completed]

        net_returns = [p / max(e, 0.01) for p, e in zip(net_pnls, entry_prices)]
        gross_returns = [p / max(e, 0.01) for p, e in zip(gross_pnls, entry_prices)]

        total_net_return = sum(net_returns) / trade_count if trade_count > 0 else 0.0
        total_gross_return = sum(gross_returns) / trade_count if trade_count > 0 else 0.0

        wins = [r for r in net_returns if r > 0]
        losses = [r for r in net_returns if r <= 0]
        win_rate = len(wins) / trade_count if trade_count > 0 else 0.0

        gross_profit = sum(wins)
        gross_loss = abs(sum(losses))
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)

        sharpe = None
        if _PANDAS_AVAILABLE and len(net_returns) >= 2:
            try:
                arr = np.array(net_returns)
                std = arr.std()
                sharpe = float(arr.mean() / std * (252 ** 0.5)) if std > 0 else 0.0
            except Exception:
                pass

        max_dd = None
        if _PANDAS_AVAILABLE and net_returns:
            try:
                cum = np.cumsum(net_returns)
                running_max = np.maximum.accumulate(cum)
                dd = running_max - cum
                max_dd = float(dd.max())
            except Exception:
                pass

        cost_impacts = [t.get("cost_impact_pct") for t in completed if t.get("cost_impact_pct") is not None]
        avg_cost_impact = sum(cost_impacts) / len(cost_impacts) if cost_impacts else None

        base.update({
            "trade_count": trade_count,
            "net_return": round(total_net_return, 6),
            "gross_return": round(total_gross_return, 6),
            "sharpe": round(sharpe, 4) if sharpe is not None else None,
            "max_drawdown": round(max_dd, 6) if max_dd is not None else None,
            "profit_factor": round(profit_factor, 4),
            "win_rate": round(win_rate, 4),
            "cost_impact": round(avg_cost_impact, 4) if avg_cost_impact is not None else None,
        })
        return base

    def calculate_split_metrics(self, trades: list, price_data: dict) -> list:
        """
        Calculate metrics per validation split window.

        Returns list of per-split metric dicts.
        """
        if not _PANDAS_AVAILABLE or not price_data:
            return []

        try:
            first_symbol = list(price_data.keys())[0]
            df = price_data[first_symbol]
            splits = self.splitter.split(df)

            split_results = []
            for sp in splits:
                test_start = sp.get("test_start")
                test_end = sp.get("test_end")
                if not test_start or not test_end:
                    continue

                split_trades = [
                    t for t in trades
                    if t.get("status") == "OK"
                    and t.get("entry_date") is not None
                    and str(t.get("entry_date", "")) >= str(test_start)
                    and str(t.get("entry_date", "")) <= str(test_end)
                ]
                metrics = self.calculate_metrics(split_trades)
                split_results.append({
                    "split_id": sp.get("split_id"),
                    "split_type": sp.get("split_type"),
                    "train_start": sp.get("train_start"),
                    "train_end": sp.get("train_end"),
                    "test_start": test_start,
                    "test_end": test_end,
                    **{k: v for k, v in metrics.items()},
                })

            return split_results
        except Exception as exc:
            logger.error("calculate_split_metrics error: %s", exc)
            return []

    def calculate_regime_metrics(self, trades: list, market_df) -> dict:
        """
        Group trades by regime and calculate per-regime metrics.

        Returns dict of regime -> metrics dict.
        """
        if not _PANDAS_AVAILABLE or self.regime is None:
            return {}

        try:
            if not _PANDAS_AVAILABLE:
                return {}
            trades_df = pd.DataFrame(trades)
            if trades_df.empty:
                return {}

            trades_df = self.regime.assign_regime_to_trades(trades_df, market_df)

            result = {}
            for regime in trades_df["regime"].unique():
                regime_trades = trades_df[trades_df["regime"] == regime].to_dict(orient="records")
                metrics = self.calculate_metrics(regime_trades)
                result[str(regime)] = metrics

            return result

        except Exception as exc:
            logger.error("calculate_regime_metrics error: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Confidence grade
    # ------------------------------------------------------------------

    def _compute_confidence_grade(self, metrics: dict, split_metrics: list) -> str:
        """
        Compute confidence grade A/B/C/D.

        Note: Even grade A does not authorize live trading. Production BLOCKED.
        """
        trade_count = metrics.get("trade_count", 0)
        split_count = len(split_metrics) if split_metrics else 0
        min_split_trades = min(
            (s.get("trade_count", 0) for s in split_metrics), default=0
        ) if split_metrics else 0
        max_dd = metrics.get("max_drawdown")
        extreme_dd = max_dd is not None and max_dd > 0.5

        if (
            trade_count >= 100
            and split_count >= 4
            and min_split_trades >= 10
            and not extreme_dd
        ):
            return "A"
        elif trade_count >= 50 and split_count >= 2:
            return "B"
        elif trade_count >= 20:
            return "C"
        else:
            return "D"

    # ------------------------------------------------------------------
    # Assumption summary
    # ------------------------------------------------------------------

    def build_assumption_summary(self) -> dict:
        """Return all model parameters for reporting."""
        return {
            "version": self.VERSION,
            "mode": self.mode,
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
            "execution": self.execution.build_assumption_dict(),
            "costs": self.costs.build_assumption_dict(),
            "liquidity": self.liquidity.build_assumption_dict() if self.liquidity else {"enabled": False},
            "gap_risk": self.gap_risk.build_assumption_dict() if self.gap_risk else {"enabled": False},
            "split": self.splitter.build_assumption_dict(),
            "regime": self.regime.build_assumption_dict() if self.regime else {"enabled": False},
            "note": (
                "Even grade A does not authorize live trading. "
                "Research Only / Backtest Only / No Real Orders. Production BLOCKED."
            ),
        }

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------

    def save_results(
        self,
        trades: list,
        metrics: dict,
        split_metrics: list,
        regime_metrics: dict,
        assumptions: dict,
    ) -> dict:
        """Save backtest results to results_dir."""
        paths = {}
        try:
            os.makedirs(self.results_dir, exist_ok=True)

            if _PANDAS_AVAILABLE:
                # Trades CSV
                trades_path = os.path.join(self.results_dir, "hardened_backtest_trades.csv")
                pd.DataFrame(trades).to_csv(trades_path, index=False)
                paths["trades"] = trades_path

                # Metrics CSV
                metrics_path = os.path.join(self.results_dir, "hardened_backtest_metrics.csv")
                pd.DataFrame([metrics]).to_csv(metrics_path, index=False)
                paths["metrics"] = metrics_path

                # Split metrics CSV
                if split_metrics:
                    split_path = os.path.join(self.results_dir, "hardened_backtest_split_metrics.csv")
                    pd.DataFrame(split_metrics).to_csv(split_path, index=False)
                    paths["split_metrics"] = split_path

                # Regime metrics CSV
                if regime_metrics:
                    regime_rows = [{"regime": k, **v} for k, v in regime_metrics.items()]
                    regime_path = os.path.join(self.results_dir, "hardened_backtest_regime_metrics.csv")
                    pd.DataFrame(regime_rows).to_csv(regime_path, index=False)
                    paths["regime_metrics"] = regime_path

            # Assumptions JSON
            assumptions_path = os.path.join(self.results_dir, "hardened_backtest_assumptions.json")
            with open(assumptions_path, "w", encoding="utf-8") as f:
                json.dump(assumptions, f, ensure_ascii=False, indent=2, default=str)
            paths["assumptions"] = assumptions_path

        except Exception as exc:
            logger.error("save_results error: %s", exc)

        return paths

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_price_data(self) -> dict:
        """
        Load daily_k.csv from data/import/daily/.

        Returns {symbol: DataFrame} with date-indexed OHLCV.
        Returns {} if file missing.
        """
        if not _PANDAS_AVAILABLE:
            return {}

        csv_path = os.path.join(BASE_DIR, "data", "import", "daily", "daily_k.csv")
        if not os.path.exists(csv_path):
            logger.warning("_load_price_data: file not found at %s", csv_path)
            return {}

        try:
            df = pd.read_csv(csv_path, low_memory=False)
            df.columns = [c.lower() for c in df.columns]

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df = df.dropna(subset=["date"])
                df = df.sort_values("date")

            symbol_col = None
            for col in ("symbol", "code", "stock_id", "ticker"):
                if col in df.columns:
                    symbol_col = col
                    break

            if symbol_col is None:
                logger.warning("_load_price_data: no symbol column found")
                df_indexed = df.set_index("date") if "date" in df.columns else df
                return {"UNKNOWN": df_indexed}

            result = {}
            for sym, gdf in df.groupby(symbol_col):
                gdf = gdf.drop(columns=[symbol_col])
                if "date" in gdf.columns:
                    gdf = gdf.set_index("date")
                result[str(sym)] = gdf

            logger.info("_load_price_data: loaded %d symbols", len(result))
            return result

        except Exception as exc:
            logger.error("_load_price_data error: %s", exc)
            return {}

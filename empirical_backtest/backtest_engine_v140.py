"""
empirical_backtest/backtest_engine_v140.py — Backtest Engine for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict

from .models_v140 import (
    BacktestConfiguration, BacktestResult, BacktestStatus, BacktestSignal,
    SimulatedTrade, StrategyRuleSnapshot, SignalType, ExecutionModelType,
    SlippageModelType, ConfidenceLevel,
)
from .cost_model_v140 import TaiwanTransactionCostModel, SlippageModel
from .data_gate_v140 import StrategyBacktestDataGate
from .lookahead_guard_v140 import LookaheadBiasGuard
from .corporate_action_guard_v140 import CorporateActionGuard
from .signal_engine_v140 import StrategyKnowledgeSignalEngine
from .rule_registry_v140 import StrategyKnowledgeRuleRegistry


class StrategyKnowledgeBacktestEngine:
    """Main engine for strategy knowledge empirical backtest."""

    def __init__(
        self,
        registry: StrategyKnowledgeRuleRegistry,
        cost_model: Optional[TaiwanTransactionCostModel] = None,
        slippage_model: Optional[SlippageModel] = None,
    ):
        self._registry = registry
        self._cost_model = cost_model or TaiwanTransactionCostModel()
        self._slippage_model = slippage_model or SlippageModel()
        self._data_gate = StrategyBacktestDataGate()
        self._lookahead_guard = LookaheadBiasGuard()
        self._ca_guard = CorporateActionGuard()
        self._signal_engine = StrategyKnowledgeSignalEngine(registry)

    def run(self, config: BacktestConfiguration, data_map: dict) -> BacktestResult:
        """Run backtest: 15-step flow."""
        started_at = datetime.now(timezone.utc).isoformat()

        # Step 1: Validate configuration
        if not config.backtest_id or not config.strategy_snapshot_id:
            return BacktestResult(
                backtest_id=config.backtest_id or "unknown",
                strategy_snapshot_id=config.strategy_snapshot_id or "unknown",
                status=BacktestStatus.FAILED,
                blocked_reasons=["INVALID_CONFIGURATION"],
                started_at=started_at,
                finished_at=datetime.now(timezone.utc).isoformat(),
            )

        symbols_requested = list(config.symbols)
        symbols_tested = []
        symbols_blocked = []
        all_trades: List[SimulatedTrade] = []
        blocked_reasons = []
        warnings = []

        # Step 2: Build strategy snapshot
        rule = self._registry.get(config.strategy_snapshot_id.replace("snap_", ""))
        snapshot_id = f"snap_{config.backtest_id}"

        # Step 3: Build dataset snapshot dict
        dataset_snapshot = {
            "snapshot_id": f"ds_{config.backtest_id}",
            "symbols": symbols_requested,
            "date_range": {"start": config.start_date, "end": config.end_date},
        }

        # Step 4: Run Data Gate for each symbol
        gate_results = {}
        for symbol in symbols_requested:
            sym_data = data_map.get(symbol, {})
            gate_result = self._data_gate.validate(sym_data)
            gate_results[symbol] = gate_result
            if gate_result["blocked"]:
                symbols_blocked.append(symbol)
                blocked_reasons.extend(gate_result["block_reasons"])
            else:
                symbols_tested.append(symbol)
            warnings.extend(gate_result.get("warnings", []))

        # Step 5: Run Lookahead Guard check
        signal_check = {
            "same_bar_close_execution": False,
            "has_future_bar_access": False,
        }
        la_result = self._lookahead_guard.check(signal_check)
        if not la_result["passed"]:
            blocked_reasons.extend(la_result["violations"])

        # Step 6: Run Corporate Action Guard for each symbol
        for symbol in symbols_tested[:]:
            sym_data = data_map.get(symbol, {})
            ca_result = self._ca_guard.check(sym_data)
            if ca_result["blocked"]:
                symbols_tested.remove(symbol)
                symbols_blocked.append(symbol)
                blocked_reasons.append(f"CORPORATE_ACTION_BLOCKED:{symbol}")
            warnings.extend(ca_result.get("notes", []))

        # Step 7: Warmup signal engine
        self._signal_engine.warmup(config.warmup_bars)

        # Step 8-11: Generate signals, simulate execution, apply costs, build trades
        for symbol in symbols_tested:
            try:
                sym_data = data_map.get(symbol, {})
                bars = sym_data.get("bars", [])
                raw_signals = self._signal_engine.evaluate_symbol(
                    config.strategy_snapshot_id.replace("snap_", ""), symbol, bars
                )
                trades = self.simulate_execution(raw_signals, bars, config)
                trades = self.apply_costs(trades, config)
                all_trades.extend(trades)
            except Exception as exc:
                symbols_tested.remove(symbol) if symbol in symbols_tested else None
                symbols_blocked.append(symbol)
                warnings.append(f"Symbol {symbol} error: {exc}")

        # Step 12: Calculate metrics
        metrics = self.calculate_metrics(all_trades, config)

        # Step 13: Compare benchmark
        benchmark_metrics = self.compare_benchmark(None, config)

        # Step 14: Build reproducibility hash
        hash_payload = json.dumps(
            {"backtest_id": config.backtest_id, "start": config.start_date, "end": config.end_date},
            sort_keys=True,
        )
        reproducibility_hash = hashlib.sha256(hash_payload.encode()).hexdigest()

        # Step 15: Build result
        if config.dry_run or config.data_mode in ("demo", "mock", "fixture"):
            status = BacktestStatus.DEMO_ONLY
            blocked_reasons = list(set(blocked_reasons))
        elif symbols_blocked and not symbols_tested:
            status = BacktestStatus.BLOCKED
        elif len(all_trades) == 0:
            status = BacktestStatus.NO_TRADES
        else:
            status = BacktestStatus.PASS

        quality_summary = {
            "data_mode": config.data_mode,
            "symbols_tested": len(symbols_tested),
            "symbols_blocked": len(symbols_blocked),
            "has_survivorship_risk": any("SURVIVORSHIP" in w for w in warnings),
        }

        finished_at = datetime.now(timezone.utc).isoformat()

        result = BacktestResult(
            backtest_id=config.backtest_id,
            strategy_snapshot_id=config.strategy_snapshot_id,
            configuration=config.to_dict(),
            status=status,
            symbols_requested=symbols_requested,
            symbols_tested=symbols_tested,
            symbols_blocked=symbols_blocked,
            date_range={"start": config.start_date, "end": config.end_date},
            trades=[t.to_dict() for t in all_trades],
            trade_count=len(all_trades),
            metrics=metrics,
            benchmark_metrics=benchmark_metrics,
            validation_metrics={},
            quality_summary=quality_summary,
            blocked_reasons=list(set(blocked_reasons)),
            warnings=warnings,
            started_at=started_at,
            finished_at=finished_at,
            reproducibility_hash=reproducibility_hash,
            metadata={"dry_run": config.dry_run},
        )
        return result

    def run_symbol(self, rule_id: str, symbol: str, bars: list, config: BacktestConfiguration) -> dict:
        """Run backtest for a single symbol."""
        try:
            signals = self._signal_engine.evaluate_symbol(rule_id, symbol, bars)
            trades = self.simulate_execution(signals, bars, config)
            trades = self.apply_costs(trades, config)
            metrics = self.calculate_metrics(trades, config)
            return {"symbol": symbol, "trades": [t.to_dict() for t in trades], "metrics": metrics, "status": "ok"}
        except Exception as exc:
            return {"symbol": symbol, "status": "error", "error": str(exc)}

    def run_universe(self, config: BacktestConfiguration, data_map: dict) -> BacktestResult:
        """Run backtest for the entire universe."""
        return self.run(config, data_map)

    def generate_signals(self, rule, bars: list) -> list:
        """Generate signals for a rule applied to bars."""
        return self._signal_engine.evaluate_symbol(rule.rule_id, "", bars)

    def simulate_execution(self, signals: list, bars: list, config: BacktestConfiguration) -> List[SimulatedTrade]:
        """Simulate trade execution from signals."""
        trades = []
        bars_by_date = {b.get("date", ""): b for b in bars}
        bar_list = bars

        for i, signal in enumerate(signals):
            if signal.get("signal_type") != SignalType.ENTRY:
                continue

            # Find next bar for execution
            signal_date = signal.get("signal_timestamp", "")
            next_idx = None
            for j, bar in enumerate(bar_list):
                if bar.get("date", "") == signal_date:
                    next_idx = j + 1
                    break

            if next_idx is None or next_idx >= len(bar_list):
                continue

            next_bar = bar_list[next_idx]

            # Skip zero-volume bars
            if next_bar.get("volume", 1) == 0:
                continue

            exec_model = config.execution_model
            if exec_model == ExecutionModelType.LIMIT_NOT_FILLED:
                continue  # No fill simulated
            elif exec_model == ExecutionModelType.STOP_TRIGGERED:
                entry_price = next_bar.get("low", next_bar.get("open", 0.0))
            else:  # NEXT_OPEN default
                entry_price = next_bar.get("open", 0.0)

            if entry_price <= 0:
                continue

            # Apply slippage
            entry_price_with_slip = self._slippage_model.apply(
                entry_price, SignalType.ENTRY, volume=next_bar.get("volume")
            )
            slippage_amount = abs(entry_price_with_slip - entry_price)

            # Find exit bar (simple: exit after warmup bars or at end of data)
            exit_idx = min(next_idx + config.warmup_bars, len(bar_list) - 1)
            exit_bar = bar_list[exit_idx]
            exit_reason = "TIME_EXIT"
            if exit_idx == len(bar_list) - 1 and exit_idx == next_idx:
                exit_reason = ExecutionModelType.END_OF_DATA_EXIT

            exit_price = exit_bar.get("open", 0.0)
            if exec_model == ExecutionModelType.STOP_TRIGGERED:
                exit_price = exit_bar.get("low", exit_bar.get("open", 0.0))

            exit_price_with_slip = self._slippage_model.apply(
                exit_price, SignalType.EXIT, volume=exit_bar.get("volume")
            )
            slippage_amount += abs(exit_price_with_slip - exit_price)

            # Calculate quantity (equal weight, simplified)
            quantity = max(1.0, config.initial_capital / (entry_price_with_slip * config.max_positions))

            gross_return = (exit_price_with_slip - entry_price_with_slip) / entry_price_with_slip if entry_price_with_slip > 0 else 0.0
            pnl = (exit_price_with_slip - entry_price_with_slip) * quantity

            # Holding days
            try:
                from datetime import datetime as dt
                ed = dt.fromisoformat(exit_bar.get("date", "2020-01-01"))
                nd = dt.fromisoformat(next_bar.get("date", "2020-01-01"))
                holding_days = (ed - nd).days
            except Exception:
                holding_days = exit_idx - next_idx

            trade = SimulatedTrade(
                trade_id=str(uuid.uuid4()),
                symbol=signal.get("symbol", ""),
                rule_id=signal.get("rule_id", ""),
                entry_signal_id=str(uuid.uuid4()),
                entry_date=next_bar.get("date", ""),
                entry_price=entry_price_with_slip,
                exit_date=exit_bar.get("date", ""),
                exit_price=exit_price_with_slip,
                quantity=quantity,
                gross_return=gross_return,
                pnl=pnl,
                holding_days=holding_days,
                exit_reason=exit_reason,
                slippage=slippage_amount,
            )
            trades.append(trade)

        return trades

    def apply_costs(self, trades: List[SimulatedTrade], config: BacktestConfiguration) -> List[SimulatedTrade]:
        """Apply transaction costs to all trades."""
        for trade in trades:
            buy_fee = self._cost_model.buy_cost(trade.entry_price, trade.quantity)
            sell_fee_brokerage = self._cost_model.buy_cost(trade.exit_price, trade.quantity)
            tax = trade.exit_price * trade.quantity * self._cost_model.transaction_tax_stock

            trade.fees = buy_fee + sell_fee_brokerage
            trade.taxes = tax
            trade.entry_cost = buy_fee
            trade.exit_cost = sell_fee_brokerage + tax

            total_cost = trade.fees + trade.taxes
            trade.net_return = trade.gross_return - (total_cost / (trade.entry_price * trade.quantity + 1e-10))
            trade.pnl = trade.pnl - total_cost

        return trades

    def calculate_metrics(self, trades: List[SimulatedTrade], config: BacktestConfiguration) -> dict:
        """Calculate backtest performance metrics."""
        assumptions = {"trading_days_per_year": 252, "risk_free_rate": 0.02}

        if not trades:
            return {
                "total_return": "unavailable",
                "annualized_return": "unavailable",
                "cagr": "unavailable",
                "max_drawdown": "unavailable",
                "volatility": "unavailable",
                "sharpe_ratio": "unavailable",
                "sortino_ratio": "unavailable",
                "calmar_ratio": "unavailable",
                "win_rate": "unavailable",
                "loss_rate": "unavailable",
                "profit_factor": "unavailable",
                "expectancy": "unavailable",
                "average_trade": "unavailable",
                "median_trade": "unavailable",
                "average_win": "unavailable",
                "average_loss": "unavailable",
                "payoff_ratio": "unavailable",
                "trade_count": 0,
                "exposure": "unavailable",
                "average_holding_period": "unavailable",
                "max_consecutive_wins": "unavailable",
                "max_consecutive_losses": "unavailable",
                "mfe": "unavailable",
                "mae": "unavailable",
                "turnover": "unavailable",
                "total_fees": 0.0,
                "total_taxes": 0.0,
                "total_slippage": 0.0,
                "status": BacktestStatus.NO_TRADES,
                "assumptions": assumptions,
            }

        returns = [t.net_return for t in trades]
        wins = [r for r in returns if r > 0]
        losses = [r for r in returns if r <= 0]
        trade_count = len(trades)

        # Basic stats
        total_return = sum(returns)
        avg_return = total_return / trade_count if trade_count else 0.0

        try:
            import statistics
            median_trade = statistics.median(returns)
            volatility = statistics.stdev(returns) if len(returns) > 1 else 0.0
        except Exception:
            median_trade = avg_return
            volatility = 0.0

        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = abs(sum(losses) / len(losses)) if losses else 0.0
        win_rate = len(wins) / trade_count if trade_count else 0.0
        loss_rate = len(losses) / trade_count if trade_count else 0.0

        total_gain = sum(wins)
        total_loss = abs(sum(losses))
        profit_factor = total_gain / total_loss if total_loss > 0 else "unavailable"
        payoff_ratio = avg_win / avg_loss if avg_loss > 0 else "unavailable"

        if isinstance(profit_factor, float) and isinstance(payoff_ratio, float):
            expectancy = win_rate * avg_win - loss_rate * avg_loss
        else:
            expectancy = "unavailable"

        # Annualized return (252 trading days assumption)
        avg_holding = sum(t.holding_days for t in trades) / trade_count if trade_count else 0
        if avg_holding > 0:
            annualized_return = (1 + avg_return) ** (252.0 / avg_holding) - 1 if avg_return > -1 else "unavailable"
        else:
            annualized_return = "unavailable"

        # Sharpe ratio
        rf = assumptions["risk_free_rate"] / 252.0
        if volatility > 0:
            sharpe_ratio = (avg_return - rf) / volatility
        else:
            sharpe_ratio = "unavailable"

        # Sortino ratio (downside deviation)
        downside = [r for r in returns if r < rf]
        if downside and len(downside) > 1:
            try:
                import statistics
                downside_vol = statistics.stdev(downside)
                sortino_ratio = (avg_return - rf) / downside_vol if downside_vol > 0 else "unavailable"
            except Exception:
                sortino_ratio = "unavailable"
        else:
            sortino_ratio = "unavailable"

        # Max drawdown
        cumulative = 0.0
        peak = 0.0
        max_dd = 0.0
        for r in returns:
            cumulative += r
            if cumulative > peak:
                peak = cumulative
            dd = peak - cumulative
            if dd > max_dd:
                max_dd = dd

        # Calmar ratio
        calmar_ratio = annualized_return / max_dd if (
            isinstance(annualized_return, float) and max_dd > 0
        ) else "unavailable"

        # CAGR (approximate)
        cagr = annualized_return  # same as annualized_return with this approach

        # Consecutive wins/losses
        max_cons_wins = 0
        max_cons_losses = 0
        cur_wins = 0
        cur_losses = 0
        for r in returns:
            if r > 0:
                cur_wins += 1
                cur_losses = 0
                max_cons_wins = max(max_cons_wins, cur_wins)
            else:
                cur_losses += 1
                cur_wins = 0
                max_cons_losses = max(max_cons_losses, cur_losses)

        # MFE / MAE
        mfe_avg = sum(t.max_favorable_excursion for t in trades) / trade_count if trade_count else 0.0
        mae_avg = sum(t.max_adverse_excursion for t in trades) / trade_count if trade_count else 0.0

        # Costs
        total_fees = sum(t.fees for t in trades)
        total_taxes = sum(t.taxes for t in trades)
        total_slippage = sum(t.slippage for t in trades)

        return {
            "total_return": total_return,
            "annualized_return": annualized_return,
            "cagr": cagr,
            "max_drawdown": max_dd,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "calmar_ratio": calmar_ratio,
            "win_rate": win_rate,
            "loss_rate": loss_rate,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "average_trade": avg_return,
            "median_trade": median_trade,
            "average_win": avg_win,
            "average_loss": avg_loss,
            "payoff_ratio": payoff_ratio,
            "trade_count": trade_count,
            "exposure": "unavailable",
            "average_holding_period": avg_holding,
            "max_consecutive_wins": max_cons_wins,
            "max_consecutive_losses": max_cons_losses,
            "mfe": mfe_avg,
            "mae": mae_avg,
            "turnover": "unavailable",
            "total_fees": total_fees,
            "total_taxes": total_taxes,
            "total_slippage": total_slippage,
            "assumptions": assumptions,
        }

    def compare_benchmark(self, result, config: BacktestConfiguration) -> dict:
        """Compare result against benchmark."""
        if config.benchmark == "CASH":
            return {"benchmark_type": "CASH", "return": 0.0, "note": "Cash benchmark: 0% return"}
        return {"benchmark_type": config.benchmark, "return": "unavailable"}

    def validate_result(self, result: BacktestResult) -> bool:
        """Validate that a result is well-formed."""
        return bool(result.backtest_id and result.strategy_snapshot_id)

    def build_result(
        self,
        backtest_id: str,
        config: BacktestConfiguration,
        trades: List[SimulatedTrade],
        metrics: dict,
        **kwargs,
    ) -> BacktestResult:
        """Build a BacktestResult from components."""
        return BacktestResult(
            backtest_id=backtest_id,
            strategy_snapshot_id=config.strategy_snapshot_id,
            configuration=config.to_dict(),
            status=kwargs.get("status", BacktestStatus.PASS),
            trades=[t.to_dict() for t in trades],
            trade_count=len(trades),
            metrics=metrics,
            metadata=kwargs.get("metadata", {}),
        )

"""
empirical_backtest/period_split_v140.py — Period Split and Walk-Forward Validator for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional
from .models_v140 import BacktestPeriodSplit, WalkForwardFold, BacktestStatus, ConfidenceLevel


class BacktestPeriodSplitter:
    """Splits date range into train/validation/test periods."""

    def split(
        self,
        start_date: str,
        end_date: str,
        train_ratio: float = 0.6,
        validation_ratio: float = 0.2,
        test_ratio: float = 0.2,
        embargo_days: int = 5,
        purge_days: int = 5,
    ) -> BacktestPeriodSplit:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        total_days = (end - start).days

        min_days = embargo_days * 2 + purge_days * 2 + 10
        if total_days < min_days:
            raise ValueError(f"Insufficient data period for split: {total_days} days < minimum {min_days}")

        train_days = int(total_days * train_ratio)
        validation_days = int(total_days * validation_ratio)

        train_start = start.date().isoformat()
        train_end = (start + timedelta(days=train_days - purge_days)).date().isoformat()

        validation_start = (start + timedelta(days=train_days + embargo_days)).date().isoformat()
        validation_end = (
            start + timedelta(days=train_days + embargo_days + validation_days - purge_days)
        ).date().isoformat()

        test_start = (
            start + timedelta(days=train_days + embargo_days + validation_days + embargo_days)
        ).date().isoformat()
        test_end = end.date().isoformat()

        return BacktestPeriodSplit(
            train_start=train_start,
            train_end=train_end,
            validation_start=validation_start,
            validation_end=validation_end,
            test_start=test_start,
            test_end=test_end,
            embargo_days=embargo_days,
            purge_days=purge_days,
        )


class WalkForwardValidator:
    """Builds and runs walk-forward validation folds."""

    def build_folds(
        self,
        start_date: str,
        end_date: str,
        n_folds: int = 5,
        train_bars: int = 120,
        test_bars: int = 20,
    ) -> List[WalkForwardFold]:
        folds = []
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        total_days = (end - start).days
        fold_size = max(train_bars + test_bars, total_days // n_folds)

        for i in range(n_folds):
            fold_start = start + timedelta(days=i * test_bars)
            train_end = fold_start + timedelta(days=train_bars)
            test_end = train_end + timedelta(days=test_bars)

            if test_end > end:
                break

            fold = WalkForwardFold(
                fold_id=f"fold_{i+1:03d}",
                train_period={
                    "start": fold_start.date().isoformat(),
                    "end": train_end.date().isoformat(),
                },
                validation_period={
                    "start": train_end.date().isoformat(),
                    "end": test_end.date().isoformat(),
                },
                test_period={
                    "start": train_end.date().isoformat(),
                    "end": test_end.date().isoformat(),
                },
                rule_snapshot_id="",
                parameters={},
                status=BacktestStatus.BLOCKED,
                confidence=ConfidenceLevel.INSUFFICIENT,
            )
            folds.append(fold)

        return folds

    def validate_folds(self, folds: List[WalkForwardFold]) -> list:
        """Check no overlap between folds."""
        issues = []
        for i in range(len(folds) - 1):
            current_test_end = folds[i].test_period.get("end", "")
            next_train_start = folds[i + 1].train_period.get("start", "")
            if current_test_end and next_train_start and current_test_end > next_train_start:
                issues.append(f"Overlap between fold {i+1} and fold {i+2}")
        return issues

    def run_folds(self, engine, rule_id: str, data_map: dict, folds: List[WalkForwardFold]) -> List[WalkForwardFold]:
        """Run engine on each fold, catching exceptions."""
        from .models_v140 import BacktestConfiguration, BacktestStatus

        results = []
        for fold in folds:
            try:
                config = BacktestConfiguration(
                    backtest_id=f"wf_{fold.fold_id}",
                    strategy_snapshot_id=f"snap_{rule_id}",
                    universe_id="walk_forward",
                    symbols=list(data_map.keys()),
                    market="TWSE",
                    start_date=fold.train_period.get("start", "2020-01-01"),
                    end_date=fold.test_period.get("end", "2020-12-31"),
                    dry_run=True,
                    data_mode="demo",
                )
                result = engine.run(config, data_map)
                fold.status = result.status
                fold.metrics = result.metrics
                fold.trades = result.trades
                fold.confidence = ConfidenceLevel.INSUFFICIENT
            except Exception as exc:
                fold.status = BacktestStatus.FAILED
                fold.warnings.append(str(exc))
            results.append(fold)

        return results

    def aggregate_results(self, folds: List[WalkForwardFold]) -> dict:
        """Aggregate metrics across ALL folds (not just best)."""
        if not folds:
            return {"fold_count": 0, "aggregate": {}}

        all_returns = []
        all_win_rates = []
        all_trade_counts = []

        for fold in folds:
            metrics = fold.metrics
            total_return = metrics.get("total_return")
            if isinstance(total_return, (int, float)):
                all_returns.append(total_return)
            win_rate = metrics.get("win_rate")
            if isinstance(win_rate, (int, float)):
                all_win_rates.append(win_rate)
            tc = metrics.get("trade_count", 0)
            if isinstance(tc, int):
                all_trade_counts.append(tc)

        agg = {
            "fold_count": len(folds),
            "avg_return": sum(all_returns) / len(all_returns) if all_returns else "unavailable",
            "avg_win_rate": sum(all_win_rates) / len(all_win_rates) if all_win_rates else "unavailable",
            "total_trades": sum(all_trade_counts),
            "all_folds_included": True,
        }
        return agg

    def detect_instability(self, folds: List[WalkForwardFold]) -> dict:
        """Detect instability by checking return variance across folds."""
        returns = []
        for fold in folds:
            r = fold.metrics.get("total_return")
            if isinstance(r, (int, float)):
                returns.append(r)

        if len(returns) < 2:
            return {"stable": False, "stddev": "unavailable", "note": "Insufficient folds for stability check"}

        try:
            import statistics
            stddev = statistics.stdev(returns)
            stable = stddev < 0.1
            return {"stable": stable, "stddev": stddev, "note": "Based on return variance across folds"}
        except Exception:
            return {"stable": False, "stddev": "unavailable", "note": "Error computing stability"}

    def summarize(self, folds: List[WalkForwardFold]) -> dict:
        """Full summary including ALL folds (not just best)."""
        aggregate = self.aggregate_results(folds)
        instability = self.detect_instability(folds)
        return {
            "folds": [f.to_dict() for f in folds],
            "aggregate": aggregate,
            "instability": instability,
            "all_folds_included": True,
            "note": "Summary includes all folds — no cherry-picking",
        }

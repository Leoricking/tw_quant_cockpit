"""
abc_validation/walk_forward_v141.py — Walk-forward validation for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Extends v1.4.0 WalkForwardValidator pattern.
No test-set parameter tuning; all folds reported including negative-performance folds.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ABCWalkForwardValidator:
    """
    Walk-forward validation for A/B/C buy point empirical validation.

    Supports train/validation/test splits with multiple folds.
    Aggregates results, preserves failed folds.
    No test-set parameter tuning; all folds reported.
    """

    def __init__(
        self,
        n_folds: int = 5,
        train_pct: float = 0.6,
        val_pct: float = 0.2,
        test_pct: float = 0.2,
    ):
        assert abs(train_pct + val_pct + test_pct - 1.0) < 0.001, "Splits must sum to 1.0"
        assert n_folds >= 2, "Need at least 2 folds"
        self.n_folds = n_folds
        self.train_pct = train_pct
        self.val_pct = val_pct
        self.test_pct = test_pct

    def create_folds(self, dates: List[str]) -> List[Dict[str, Any]]:
        """Create walk-forward fold date ranges from a sorted list of dates."""
        if not dates or len(dates) < self.n_folds * 2:
            return []

        folds = []
        fold_size = len(dates) // self.n_folds

        for i in range(self.n_folds):
            start_idx = i * fold_size
            end_idx = start_idx + fold_size if i < self.n_folds - 1 else len(dates)
            fold_dates = dates[start_idx:end_idx]

            if len(fold_dates) < 4:
                continue

            n = len(fold_dates)
            train_end = int(n * self.train_pct)
            val_end = train_end + int(n * self.val_pct)

            folds.append({
                "fold_id": i + 1,
                "train_dates": fold_dates[:train_end],
                "val_dates": fold_dates[train_end:val_end],
                "test_dates": fold_dates[val_end:],
                "total_dates": n,
            })

        return folds

    def run(
        self,
        signals_by_date: Dict[str, List[dict]],
        trade_results: Optional[List[dict]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Run walk-forward validation across all folds."""
        trade_results = trade_results or []
        all_dates = sorted(signals_by_date.keys())
        folds = self.create_folds(all_dates)

        fold_results = []
        for fold in folds:
            fold_result = self._run_fold(fold, signals_by_date, trade_results, buy_point_type)
            fold_results.append(fold_result)

        return self._aggregate(fold_results, buy_point_type)

    def _run_fold(
        self,
        fold: dict,
        signals_by_date: dict,
        trade_results: list,
        buy_point_type: str,
    ) -> dict:
        test_dates = set(fold["test_dates"])
        test_signals = []
        for d in test_dates:
            test_signals.extend(signals_by_date.get(d, []))

        sig_ids = {s.get("signal_id") for s in test_signals}
        fold_trades = [t for t in trade_results if t.get("signal_id") in sig_ids]

        if not fold_trades:
            return {
                "fold_id": fold["fold_id"],
                "status": "NO_TRADES",
                "trade_count": 0,
                "win_rate": None,
                "expectancy": None,
                "test_dates": len(fold["test_dates"]),
            }

        net_rets = [t.get("net_return", 0) for t in fold_trades]
        wins = [r for r in net_rets if r > 0]
        losses = [r for r in net_rets if r <= 0]
        win_rate = len(wins) / len(net_rets)
        aw = sum(wins) / len(wins) if wins else 0.0
        al = abs(sum(losses) / len(losses)) if losses else 0.0
        expectancy = win_rate * aw - (1 - win_rate) * al

        return {
            "fold_id": fold["fold_id"],
            "status": "PASS" if expectancy > 0 else "NEGATIVE_PERFORMANCE",
            "trade_count": len(fold_trades),
            "win_rate": win_rate,
            "expectancy": expectancy,
            "test_dates": len(fold["test_dates"]),
        }

    def _aggregate(self, fold_results: List[dict], buy_point_type: str) -> dict:
        if not fold_results:
            return {
                "buy_point_type": buy_point_type,
                "folds": [],
                "aggregate": None,
                "status": "INSUFFICIENT_DATA",
                "note": "All folds preserved including negative-performance folds",
                "no_test_set_parameter_tuning": True,
                "no_real_orders": True,
            }

        valid = [f for f in fold_results if f["trade_count"] > 0]
        if not valid:
            agg = None
        else:
            avg_win_rate = sum(f["win_rate"] for f in valid if f.get("win_rate") is not None) / len(valid)
            avg_exp = sum(f["expectancy"] for f in valid if f.get("expectancy") is not None) / len(valid)
            positive_folds = sum(1 for f in valid if f.get("expectancy", 0) > 0)
            agg = {
                "total_folds": len(fold_results),
                "folds_with_trades": len(valid),
                "positive_performance_folds": positive_folds,
                "negative_performance_folds": len(valid) - positive_folds,
                "avg_win_rate": avg_win_rate,
                "avg_expectancy": avg_exp,
            }

        return {
            "buy_point_type": buy_point_type,
            "folds": fold_results,
            "aggregate": agg,
            "status": "COMPLETE" if fold_results else "NO_FOLDS",
            "note": "All folds preserved including negative-performance folds. No test-set tuning.",
            "no_test_set_parameter_tuning": True,
            "no_real_orders": True,
        }

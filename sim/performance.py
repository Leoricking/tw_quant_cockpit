"""
sim/performance.py - Performance tracking and metrics computation for paper trading.
"""

import logging
import math
from datetime import datetime

logger = logging.getLogger(__name__)


class PerformanceTracker:
    """
    Tracks daily portfolio performance and computes risk metrics.
    """

    def __init__(self):
        """Initialize with empty history."""
        self._history = []

    def record_daily(self, date, portfolio_value, cash, positions):
        """
        Record a daily portfolio snapshot.

        Parameters
        ----------
        date : str or date
            Date of the snapshot.
        portfolio_value : float
            Total portfolio value on this date.
        cash : float
            Cash balance.
        positions : dict
            Mapping of symbol -> Position objects.
        """
        snapshot = {
            'date': str(date),
            'portfolio_value': float(portfolio_value),
            'cash': float(cash),
            'n_positions': len(positions) if positions else 0,
            'timestamp': datetime.now().isoformat(),
        }
        self._history.append(snapshot)
        logger.debug("Daily snapshot recorded: %s portfolio=%.0f", date, portfolio_value)

    def compute_metrics(self):
        """
        Compute performance metrics from daily history.

        Returns
        -------
        dict with:
            total_return, annualized_return, max_drawdown, sharpe_ratio,
            win_rate, total_trades, winning_trades
        """
        if not self._history:
            return {
                'total_return': 0.0,
                'annualized_return': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0,
                'win_rate': 0.0,
                'total_trades': 0,
                'winning_trades': 0,
            }

        values = [h['portfolio_value'] for h in self._history]

        # Total return
        first = values[0]
        last = values[-1]
        total_return = (last - first) / first if first > 0 else 0.0

        # Annualized return (simple, assuming 252 trading days/year)
        n_days = len(values)
        if n_days > 1 and first > 0:
            annualized_return = (last / first) ** (252.0 / n_days) - 1.0
        else:
            annualized_return = 0.0

        # Max drawdown
        max_drawdown = 0.0
        peak = values[0]
        for v in values:
            if v > peak:
                peak = v
            dd = (peak - v) / peak if peak > 0 else 0.0
            if dd > max_drawdown:
                max_drawdown = dd

        # Daily returns and Sharpe ratio
        daily_returns = []
        for i in range(1, len(values)):
            if values[i-1] > 0:
                r = (values[i] - values[i-1]) / values[i-1]
                daily_returns.append(r)

        sharpe_ratio = 0.0
        if len(daily_returns) >= 2:
            mean_r = sum(daily_returns) / len(daily_returns)
            var_r = sum((r - mean_r) ** 2 for r in daily_returns) / len(daily_returns)
            std_r = math.sqrt(var_r) if var_r > 0 else 0.0
            if std_r > 0:
                sharpe_ratio = (mean_r / std_r) * math.sqrt(252)

        # Win rate (based on daily return direction as proxy)
        winning = sum(1 for r in daily_returns if r > 0)
        total_trades = len(daily_returns)
        win_rate = winning / total_trades if total_trades > 0 else 0.0

        return {
            'total_return': round(total_return, 4),
            'annualized_return': round(annualized_return, 4),
            'max_drawdown': round(max_drawdown, 4),
            'sharpe_ratio': round(sharpe_ratio, 4),
            'win_rate': round(win_rate, 4),
            'total_trades': total_trades,
            'winning_trades': winning,
        }

    def get_daily_history(self):
        """Return list of daily snapshot dicts."""
        return list(self._history)

    def print_report(self):
        """Print a formatted performance report to console."""
        metrics = self.compute_metrics()
        n = len(self._history)

        print("\n" + "=" * 50)
        print("  Performance Report")
        print("=" * 50)
        print(f"  Days tracked     : {n}")
        print(f"  Total Return     : {metrics['total_return']:+.2%}")
        print(f"  Annualized Return: {metrics['annualized_return']:+.2%}")
        print(f"  Max Drawdown     : {metrics['max_drawdown']:.2%}")
        print(f"  Sharpe Ratio     : {metrics['sharpe_ratio']:.3f}")
        print(f"  Win Rate         : {metrics['win_rate']:.1%}")
        print(f"  Total Days       : {metrics['total_trades']}")
        print(f"  Winning Days     : {metrics['winning_trades']}")
        print("=" * 50)

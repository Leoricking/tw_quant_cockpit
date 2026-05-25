"""
dataset/labeler.py - Label generation for ML training datasets.

Generates daytrade and swing trade labels from price series.
"""

import logging

logger = logging.getLogger(__name__)


class Labeler:
    """
    Generates binary/ternary trade labels from price series.

    Daytrade labels (1/-1/0) based on short-term price path.
    Swing labels (1/-1/0) based on medium-term gain/drawdown criteria.
    """

    def label_daytrade(self, price_series, forward_minutes=15,
                       up_threshold=0.008, down_threshold=-0.004):
        """
        Label each point for daytrade entry quality.

        Parameters
        ----------
        price_series : list or pandas.Series
            Price series (minute or tick-level).
        forward_minutes : int
            How many periods forward to evaluate.
        up_threshold : float
            Minimum return to qualify as a good buy (e.g. 0.008 = +0.8%).
        down_threshold : float
            Maximum drawdown that triggers a -1 label (e.g. -0.004 = -0.4%).

        Label logic:
            1  : future max return >= up_threshold AND min didn't first drop down_threshold
            -1 : future min first drops <= down_threshold before hitting up_threshold
            0  : otherwise

        Returns
        -------
        list of int (1, -1, 0), same length as price_series.
            Returns empty list on insufficient data.
        """
        try:
            prices = list(price_series)
        except Exception:
            return []

        if len(prices) < forward_minutes + 1:
            logger.warning("Labeler.label_daytrade: insufficient data (%d < %d)",
                           len(prices), forward_minutes + 1)
            return []

        labels = []

        for i in range(len(prices) - forward_minutes):
            base = float(prices[i])
            if base <= 0:
                labels.append(0)
                continue

            future = [float(p) for p in prices[i+1:i+1+forward_minutes]]

            # Check if drawdown threshold hit before upside
            first_hit_down = None
            first_hit_up = None

            for j, p in enumerate(future):
                ret = (p - base) / base
                if first_hit_down is None and ret <= down_threshold:
                    first_hit_down = j
                if first_hit_up is None and ret >= up_threshold:
                    first_hit_up = j

            max_return = max((p - base) / base for p in future) if future else 0

            if max_return >= up_threshold:
                if first_hit_down is None or (first_hit_up is not None and first_hit_up < first_hit_down):
                    labels.append(1)
                else:
                    labels.append(-1)
            elif first_hit_down is not None:
                labels.append(-1)
            else:
                labels.append(0)

        # Pad the end with 0 labels (no future data)
        labels.extend([0] * forward_minutes)

        return labels

    def label_swing(self, price_series, forward_days_min=5, forward_days_max=20,
                    up_threshold=0.08, down_threshold=-0.05, max_drawdown=0.04):
        """
        Label each point for swing trade entry quality.

        Parameters
        ----------
        price_series : list or pandas.Series
            Daily close price series.
        forward_days_min : int
            Minimum days to hold.
        forward_days_max : int
            Maximum days to evaluate.
        up_threshold : float
            Minimum gain to qualify as successful swing (e.g. 0.08 = +8%).
        down_threshold : float
            Loss threshold for -1 label (e.g. -0.05 = -5%).
        max_drawdown : float
            Maximum allowable drawdown during the trade (e.g. 0.04 = 4%).

        Label logic:
            1  : max gain in [min..max] days >= up_threshold AND max drawdown <= max_drawdown
            -1 : price first drops >= |down_threshold| before gaining up_threshold
            0  : otherwise

        Returns
        -------
        list of int (1, -1, 0), same length as price_series.
        """
        try:
            prices = list(price_series)
        except Exception:
            return []

        if len(prices) < forward_days_min + 1:
            logger.warning("Labeler.label_swing: insufficient data (%d < %d)",
                           len(prices), forward_days_min + 1)
            return []

        labels = []

        for i in range(len(prices) - forward_days_min):
            base = float(prices[i])
            if base <= 0:
                labels.append(0)
                continue

            end = min(i + forward_days_max + 1, len(prices))
            future = [float(p) for p in prices[i+1:end]]

            if not future:
                labels.append(0)
                continue

            # Find first drawdown hit
            first_hit_down = None
            first_hit_up = None
            max_ret_in_window = 0.0
            max_dd_in_window = 0.0
            peak = base

            for j, p in enumerate(future):
                ret = (p - base) / base
                if p > peak:
                    peak = p
                dd = (peak - p) / peak if peak > 0 else 0

                if dd > max_dd_in_window:
                    max_dd_in_window = dd
                if ret > max_ret_in_window:
                    max_ret_in_window = ret

                if first_hit_down is None and ret <= down_threshold:
                    first_hit_down = j
                if first_hit_up is None and ret >= up_threshold:
                    first_hit_up = j

            if (max_ret_in_window >= up_threshold and max_dd_in_window <= max_drawdown):
                # Gain achieved within drawdown limit
                if first_hit_down is None or (first_hit_up is not None and first_hit_up < first_hit_down):
                    labels.append(1)
                else:
                    labels.append(-1)
            elif first_hit_down is not None and first_hit_up is None:
                labels.append(-1)
            else:
                labels.append(0)

        # Pad the end
        labels.extend([0] * forward_days_min)

        return labels

"""
portfolio/walk_forward/window_v154.py — Walk-forward Window Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
import datetime
from typing import List, Optional

from portfolio.walk_forward.enums_v154 import WindowType, WindowStatus
from portfolio.walk_forward.models_v154 import WalkForwardWindow
from portfolio.walk_forward.calendar_v154 import WalkForwardCalendar

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
WINDOW_VERSION = "1.5.4"


def _parse(d: str) -> datetime.date:
    return datetime.date.fromisoformat(d)


def _fmt(d: datetime.date) -> str:
    return d.isoformat()


def _add_days(d: str, n: int) -> str:
    return _fmt(_parse(d) + datetime.timedelta(days=n))


class WalkForwardWindowEngine:
    """Generates walk-forward windows (rolling, expanding, anchored)."""

    def __init__(self, calendar: Optional[WalkForwardCalendar] = None):
        self.calendar = calendar or WalkForwardCalendar()
        self.version = WINDOW_VERSION

    def _make_window(
        self,
        sequence: int,
        train_start: str,
        train_end: str,
        purge_days: int,
        val_start: str,
        val_end: str,
        embargo_days: int,
        window_type: WindowType,
        min_train_obs: int,
        min_val_obs: int,
    ) -> WalkForwardWindow:
        window_id = f"wf_{sequence:04d}"
        # purge
        purge_s = _add_days(train_end, 1) if purge_days > 0 else train_end
        purge_e = _add_days(train_end, purge_days) if purge_days > 0 else train_end
        # embargo
        embargo_e = _add_days(val_end, embargo_days)

        train_obs = self.calendar.trading_days_between(train_start, train_end)
        val_obs = self.calendar.trading_days_between(val_start, val_end)

        warnings = []
        if train_obs < min_train_obs:
            status = WindowStatus.INSUFFICIENT_TRAINING_DATA
        elif val_obs < min_val_obs:
            status = WindowStatus.INSUFFICIENT_VALIDATION_DATA
        else:
            # Last window may be partial if val period is shorter than expected
            status = WindowStatus.VALID

        return WalkForwardWindow(
            window_id=window_id,
            sequence=sequence,
            training_start=train_start,
            training_end=train_end,
            purge_start=purge_s,
            purge_end=purge_e,
            validation_start=val_start,
            validation_end=val_end,
            embargo_end=embargo_e,
            window_type=window_type,
            status=status,
            warnings=warnings if warnings else None,
            blockers=None,
            metadata={"calendar_version": "1.5.4", "timezone": "Asia/Taipei"},
        )

    def generate_rolling_windows(
        self,
        start: str,
        end: str,
        training_days: int,
        validation_days: int,
        step_days: int,
        purge_days: int = 0,
        embargo_days: int = 0,
        min_train_obs: int = 5,
        min_val_obs: int = 2,
    ) -> List[WalkForwardWindow]:
        """Generate rolling windows: training window of fixed length, steps forward."""
        windows = []
        sequence = 1
        cur_train_start = _parse(start)
        end_date = _parse(end)

        while True:
            train_end = cur_train_start + datetime.timedelta(days=training_days - 1)
            val_start = train_end + datetime.timedelta(days=purge_days + 1)
            val_end = val_start + datetime.timedelta(days=validation_days - 1)

            if val_start > end_date:
                break

            # Mark last window PARTIAL if val_end exceeds end
            is_partial = val_end > end_date
            if is_partial:
                val_end = end_date

            w = self._make_window(
                sequence, _fmt(cur_train_start), _fmt(train_end),
                purge_days, _fmt(val_start), _fmt(val_end),
                embargo_days, WindowType.ROLLING, min_train_obs, min_val_obs,
            )
            if is_partial and w.status == WindowStatus.VALID:
                w.status = WindowStatus.PARTIAL

            windows.append(w)
            sequence += 1
            cur_train_start = cur_train_start + datetime.timedelta(days=step_days)

        return windows

    def generate_expanding_windows(
        self,
        start: str,
        end: str,
        initial_training_days: int,
        validation_days: int,
        step_days: int,
        purge_days: int = 0,
        embargo_days: int = 0,
        min_train_obs: int = 5,
        min_val_obs: int = 2,
    ) -> List[WalkForwardWindow]:
        """Generate expanding windows: training start fixed, training end grows."""
        windows = []
        sequence = 1
        fixed_start = _parse(start)
        end_date = _parse(end)

        # First training end
        cur_train_end = fixed_start + datetime.timedelta(days=initial_training_days - 1)

        while True:
            val_start = cur_train_end + datetime.timedelta(days=purge_days + 1)
            val_end = val_start + datetime.timedelta(days=validation_days - 1)

            if val_start > end_date:
                break

            is_partial = val_end > end_date
            if is_partial:
                val_end = end_date

            w = self._make_window(
                sequence, _fmt(fixed_start), _fmt(cur_train_end),
                purge_days, _fmt(val_start), _fmt(val_end),
                embargo_days, WindowType.EXPANDING, min_train_obs, min_val_obs,
            )
            if is_partial and w.status == WindowStatus.VALID:
                w.status = WindowStatus.PARTIAL

            windows.append(w)
            sequence += 1
            cur_train_end = cur_train_end + datetime.timedelta(days=step_days)

        return windows

    def generate_anchored_windows(
        self,
        anchor_date: str,
        end: str,
        validation_days: int,
        step_days: int,
        purge_days: int = 0,
        embargo_days: int = 0,
        min_train_obs: int = 5,
        min_val_obs: int = 2,
    ) -> List[WalkForwardWindow]:
        """Generate anchored windows: training always starts at anchor_date."""
        windows = []
        sequence = 1
        anchor = _parse(anchor_date)
        end_date = _parse(end)

        cur_val_start = anchor + datetime.timedelta(days=1)

        while True:
            train_end = cur_val_start - datetime.timedelta(days=purge_days + 1)
            val_end = cur_val_start + datetime.timedelta(days=validation_days - 1)

            if cur_val_start > end_date:
                break
            if train_end <= anchor:
                train_end = anchor + datetime.timedelta(days=1)

            is_partial = val_end > end_date
            if is_partial:
                val_end = end_date

            w = self._make_window(
                sequence, _fmt(anchor), _fmt(train_end),
                purge_days, _fmt(cur_val_start), _fmt(val_end),
                embargo_days, WindowType.ANCHORED, min_train_obs, min_val_obs,
            )
            if is_partial and w.status == WindowStatus.VALID:
                w.status = WindowStatus.PARTIAL

            windows.append(w)
            sequence += 1
            cur_val_start = cur_val_start + datetime.timedelta(days=step_days)

        return windows

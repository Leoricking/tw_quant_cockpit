"""
strategy_validation/strategy_validation_store.py
TW Quant Cockpit — Strategy Validation Store
v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

from strategy_validation.strategy_validation_schema import (
    VERSION,
    StrategyValidationScore,
    StrategyValidationComponent,
    StrategyValidationSummary,
)

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

read_only                         = True
no_real_orders                    = True
production_blocked                = True
validated_does_not_enable_trading = True


class StrategyValidationStore:
    """
    Saves and loads strategy validation outputs (CSV files).
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only                         = True
    no_real_orders                    = True
    production_blocked                = True
    validated_does_not_enable_trading = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/strategy_validation",
    ) -> None:
        if not os.path.isabs(output_dir):
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base, output_dir)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _ts(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _latest_csv(self, prefix: str) -> Optional[str]:
        """Find latest CSV file matching prefix_*.csv pattern."""
        try:
            pattern = os.path.join(self.output_dir, f"{prefix}_*.csv")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception as exc:
            logger.warning("_latest_csv prefix=%s: %s", prefix, exc)
            return None

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_scores(self, scores: List[StrategyValidationScore]) -> Optional[str]:
        """Save list of StrategyValidationScore to CSV."""
        if not scores:
            return None
        try:
            fname = os.path.join(self.output_dir, f"strategy_validation_scores_{self._ts()}.csv")
            rows = [s.to_dict() for s in scores]
            fieldnames = list(rows[0].keys())
            with open(fname, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            logger.info("save_scores: saved %d rows → %s", len(scores), fname)
            return fname
        except Exception as exc:
            logger.error("save_scores failed: %s", exc)
            return None

    def save_components(self, components: List[StrategyValidationComponent]) -> Optional[str]:
        """Save list of StrategyValidationComponent to CSV."""
        if not components:
            return None
        try:
            fname = os.path.join(
                self.output_dir,
                f"strategy_validation_components_{self._ts()}.csv",
            )
            rows = [c.to_dict() for c in components]
            fieldnames = list(rows[0].keys())
            with open(fname, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            logger.info("save_components: saved %d rows → %s", len(components), fname)
            return fname
        except Exception as exc:
            logger.error("save_components failed: %s", exc)
            return None

    def save_summary(self, summary: StrategyValidationSummary) -> Optional[str]:
        """Save StrategyValidationSummary to CSV (single row)."""
        try:
            fname = os.path.join(
                self.output_dir,
                f"strategy_validation_summary_{self._ts()}.csv",
            )
            row = summary.to_dict()
            with open(fname, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
                writer.writeheader()
                writer.writerow(row)
            logger.info("save_summary → %s", fname)
            return fname
        except Exception as exc:
            logger.error("save_summary failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_scores(self) -> List[StrategyValidationScore]:
        """Load latest strategy validation scores CSV."""
        try:
            fpath = self._latest_csv("strategy_validation_scores")
            if not fpath:
                return []
            with open(fpath, newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            return [StrategyValidationScore.from_dict(r) for r in rows]
        except Exception as exc:
            logger.warning("load_latest_scores: %s", exc)
            return []

    def load_latest_components(self) -> List[StrategyValidationComponent]:
        """Load latest strategy validation components CSV."""
        try:
            fpath = self._latest_csv("strategy_validation_components")
            if not fpath:
                return []
            with open(fpath, newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            return [StrategyValidationComponent.from_dict(r) for r in rows]
        except Exception as exc:
            logger.warning("load_latest_components: %s", exc)
            return []

    def load_latest_summary(self) -> Optional[StrategyValidationSummary]:
        """Load latest strategy validation summary CSV."""
        try:
            fpath = self._latest_csv("strategy_validation_summary")
            if not fpath:
                return None
            with open(fpath, newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            if rows:
                return StrategyValidationSummary.from_dict(rows[0])
            return None
        except Exception as exc:
            logger.warning("load_latest_summary: %s", exc)
            return None

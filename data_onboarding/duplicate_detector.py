"""
data_onboarding/duplicate_detector.py — DuplicateDetector for TW Quant Cockpit v1.1.1.

Detects duplicates and conflicts between incoming data and existing repository data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Conflict detection → manual review (not auto-overwrite).
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

from data_onboarding.onboarding_schema import (
    IMPORT_MODE_MERGE_SAFE, IMPORT_MODE_APPEND_SAFE,
    PLAN_ACTION_REVIEW, PLAN_ACTION_BLOCKED,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_IMPORT_BASE = os.path.join(BASE_DIR, "data", "import")

_OHLCV_COLS = ['open', 'high', 'low', 'close', 'volume']


class DuplicateDetector:
    """
    Detects duplicates and conflicts between incoming data and existing repository data.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Conflicts always go to REVIEW — never auto-overwrite.
    """

    research_only  = True
    no_real_orders = True

    def detect_within_file(self, df) -> dict:
        """
        Find duplicate dates within the file itself.
        Returns: {'identical': [(date, count)], 'conflicting': [(date, count)], 'count': N}
        """
        result = {
            "identical": [], "conflicting": [], "count": 0,
            "research_only": True, "no_real_orders": True,
        }
        if not _PANDAS_AVAILABLE or df is None or 'date' not in df.columns:
            return result
        try:
            date_groups = df.groupby('date')
            identical = []
            conflicting = []
            for date_val, group in date_groups:
                if len(group) <= 1:
                    continue
                # Check if all rows in group are identical
                numeric_cols = [c for c in _OHLCV_COLS if c in group.columns]
                if numeric_cols:
                    deduped = group[numeric_cols].drop_duplicates()
                    if len(deduped) == 1:
                        identical.append((str(date_val), len(group)))
                    else:
                        conflicting.append((str(date_val), len(group)))
                else:
                    # No numeric cols to compare — treat as identical
                    identical.append((str(date_val), len(group)))

            result["identical"]   = identical
            result["conflicting"] = conflicting
            result["count"]       = len(identical) + len(conflicting)
        except Exception as exc:
            logger.warning("DuplicateDetector.detect_within_file: %s", exc)
        return result

    def detect_against_existing(self, df, symbol: str, dataset: str) -> dict:
        """
        Compare incoming rows against existing data/import/<dataset>/*.csv.
        Returns: {'new_rows': N, 'duplicate_identical': N, 'conflicts': N, 'conflict_dates': [...]}
        """
        result = {
            "new_rows": 0, "duplicate_identical": 0, "conflicts": 0, "conflict_dates": [],
            "research_only": True, "no_real_orders": True,
        }
        if not _PANDAS_AVAILABLE or df is None:
            return result

        existing = self._load_existing(symbol, dataset)
        if existing is None or len(existing) == 0:
            result["new_rows"] = len(df)
            return result

        try:
            if 'date' not in df.columns or 'date' not in existing.columns:
                result["new_rows"] = len(df)
                return result

            incoming_dates = set(df['date'].astype(str))
            existing_dates = set(existing['date'].astype(str))
            overlap_dates  = incoming_dates & existing_dates
            new_dates      = incoming_dates - existing_dates

            result["new_rows"] = len(new_dates)

            if not overlap_dates:
                return result

            # Check overlapping rows for conflicts
            df_str      = df.copy()
            df_str['date'] = df_str['date'].astype(str)
            ex_str      = existing.copy()
            ex_str['date'] = ex_str['date'].astype(str)

            conflict_dates = []
            identical_count = 0

            for d in overlap_dates:
                inc_rows = df_str[df_str['date'] == d]
                ex_rows  = ex_str[ex_str['date'] == d]
                numeric_cols = [c for c in _OHLCV_COLS if c in inc_rows.columns and c in ex_rows.columns]
                if not numeric_cols:
                    identical_count += 1
                    continue
                inc_vals = inc_rows[numeric_cols].iloc[0]
                ex_vals  = ex_rows[numeric_cols].iloc[0]
                try:
                    import numpy as np
                    if not inc_vals.equals(ex_vals):
                        conflict_dates.append(d)
                    else:
                        identical_count += 1
                except Exception:
                    identical_count += 1

            result["duplicate_identical"] = identical_count
            result["conflicts"]           = len(conflict_dates)
            result["conflict_dates"]      = conflict_dates
        except Exception as exc:
            logger.warning("DuplicateDetector.detect_against_existing: %s", exc)
        return result

    def suggest_import_mode(self, detection: dict) -> str:
        """
        Given detection results, suggest: MERGE_SAFE, APPEND_SAFE, REVIEW, BLOCKED
        - No conflicts: MERGE_SAFE
        - Only identical duplicates: MERGE_SAFE (dedup)
        - Conflicting OHLCV: REVIEW (never auto REPLACE)
        """
        conflicts = detection.get("conflicts", 0)
        if conflicts > 0:
            return PLAN_ACTION_REVIEW
        return IMPORT_MODE_MERGE_SAFE

    def _load_existing(self, symbol: str, dataset: str) -> Optional[object]:
        """Load existing CSV from data/import/<dataset>/"""
        if not _PANDAS_AVAILABLE:
            return None
        dataset_dir = os.path.join(_IMPORT_BASE, dataset)
        if not os.path.isdir(dataset_dir):
            return None
        # Try common file name patterns
        candidates = [
            os.path.join(dataset_dir, f"{symbol}.csv"),
            os.path.join(dataset_dir, f"{symbol}_{dataset}.csv"),
            os.path.join(dataset_dir, f"{dataset}_{symbol}.csv"),
            os.path.join(dataset_dir, f"{dataset}.csv"),
        ]
        for path in candidates:
            if os.path.isfile(path):
                try:
                    return pd.read_csv(path, encoding='utf-8-sig')
                except Exception:
                    try:
                        return pd.read_csv(path, encoding='cp950')
                    except Exception:
                        pass
        return None

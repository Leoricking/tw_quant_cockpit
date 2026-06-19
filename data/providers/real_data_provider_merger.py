"""
data/providers/real_data_provider_merger.py — Multi-source response merger v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Never silently averages prices. Never picks newer value without recording.
[!] Core price conflict -> SOURCE_CONFLICT issue -> may block precise prices.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from data.providers.real_data_provider_models import (
    ProviderErrorCategory,
    ProviderResponse,
    ProviderStatus,
    _now_iso,
)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False


@dataclass
class MergeConflict:
    """A detected conflict between two providers for the same field/symbol/date."""
    field: str = ""
    symbol: str = ""
    date: str = ""
    primary_value: Any = None
    secondary_value: Any = None
    primary_provider: str = ""
    secondary_provider: str = ""
    category: str = ProviderErrorCategory.SOURCE_CONFLICT
    blocks_analysis: bool = False


@dataclass
class MergeResult:
    """Result of merging two provider responses."""
    merged_records: list = field(default_factory=list)
    conflicts: List[MergeConflict] = field(default_factory=list)
    provenance_all: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    precise_price_blocked: bool = False


class ProviderResponseMerger:
    """
    Merges responses from two providers for the same data.

    [!] Never silently averages prices.
    [!] All conflicts recorded in MergeResult.conflicts.
    [!] Core price conflict (>1%) sets precise_price_blocked=True.
    """

    PRICE_FIELDS = ["close", "open", "high", "low"]
    VOLUME_FIELDS = ["volume"]
    PRICE_TOLERANCE_PCT = 0.01  # 1%

    def merge(self, primary: ProviderResponse, secondary: ProviderResponse) -> MergeResult:
        """
        Merge primary and secondary responses.
        Primary values take precedence when conflict, but conflicts are recorded.
        """
        result = MergeResult()
        result.provenance_all = [primary.provider_id, secondary.provider_id]

        # Build lookup of secondary records by (symbol, date)
        secondary_index: Dict[Tuple[str, str], dict] = {}
        for rec in secondary.records:
            symbol = str(rec.get("symbol", ""))
            date = str(rec.get("date", ""))
            secondary_index[(symbol, date)] = rec

        merged = []
        for primary_rec in primary.records:
            symbol = str(primary_rec.get("symbol", ""))
            date = str(primary_rec.get("date", ""))
            key = (symbol, date)
            merged_rec = dict(primary_rec)

            if key in secondary_index:
                secondary_rec = secondary_index[key]
                # Check each price field for conflicts
                for f in self.PRICE_FIELDS:
                    pv = primary_rec.get(f)
                    sv = secondary_rec.get(f)
                    if pv is None or sv is None:
                        continue
                    try:
                        pv_f = float(pv)
                        sv_f = float(sv)
                    except (ValueError, TypeError):
                        continue
                    if math.isnan(pv_f) or math.isnan(sv_f):
                        continue
                    if pv_f == 0 and sv_f == 0:
                        continue
                    # Compute relative difference
                    ref = (abs(pv_f) + abs(sv_f)) / 2.0
                    if ref == 0:
                        continue
                    pct_diff = abs(pv_f - sv_f) / ref
                    if pct_diff > self.PRICE_TOLERANCE_PCT:
                        conflict = MergeConflict(
                            field=f,
                            symbol=symbol,
                            date=date,
                            primary_value=pv_f,
                            secondary_value=sv_f,
                            primary_provider=primary.provider_id,
                            secondary_provider=secondary.provider_id,
                            category=ProviderErrorCategory.SOURCE_CONFLICT,
                            blocks_analysis=True,
                        )
                        result.conflicts.append(conflict)
                        result.precise_price_blocked = True
                        result.warnings.append(
                            f"Price conflict on {symbol}/{date}/{f}: "
                            f"primary={pv_f}, secondary={sv_f} "
                            f"({pct_diff*100:.2f}% diff > {self.PRICE_TOLERANCE_PCT*100:.1f}% tolerance). "
                            f"Primary value retained. Precise price BLOCKED."
                        )
                        # Record secondary as observation — do NOT average
                        merged_rec[f"_secondary_{f}"] = sv_f

                # Check volume fields (record conflict but don't block)
                for f in self.VOLUME_FIELDS:
                    pv = primary_rec.get(f)
                    sv = secondary_rec.get(f)
                    if pv is None or sv is None:
                        continue
                    try:
                        pv_f = float(pv)
                        sv_f = float(sv)
                    except (ValueError, TypeError):
                        continue
                    if math.isnan(pv_f) or math.isnan(sv_f):
                        continue
                    if abs(pv_f - sv_f) > 1:
                        conflict = MergeConflict(
                            field=f,
                            symbol=symbol,
                            date=date,
                            primary_value=pv_f,
                            secondary_value=sv_f,
                            primary_provider=primary.provider_id,
                            secondary_provider=secondary.provider_id,
                            category=ProviderErrorCategory.SOURCE_CONFLICT,
                            blocks_analysis=False,
                        )
                        result.conflicts.append(conflict)
                        result.warnings.append(
                            f"Volume conflict on {symbol}/{date}/{f}: "
                            f"primary={pv_f}, secondary={sv_f}. Primary retained."
                        )
                        merged_rec[f"_secondary_{f}"] = sv_f

            merged.append(merged_rec)

        # Add secondary records not in primary (supplement, not override)
        primary_keys = {
            (str(r.get("symbol", "")), str(r.get("date", "")))
            for r in primary.records
        }
        for key, rec in secondary_index.items():
            if key not in primary_keys:
                merged.append(dict(rec))

        result.merged_records = merged
        return result

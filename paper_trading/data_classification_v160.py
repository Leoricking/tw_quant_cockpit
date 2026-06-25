"""paper_trading/data_classification_v160.py — Data Mode Classification v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
All market data must be classified. Unknown data mode = BLOCK.
No real→mock fallback. No live provider silent fallback to fixture.
"""
from __future__ import annotations
from typing import Dict, Optional, Tuple

from .enums_v160 import DataMode


class DataClassifier:
    """Classifies and validates data mode for paper trading events."""

    FORMAL_CONCLUSION_MODES = {DataMode.LIVE, DataMode.DELAYED, DataMode.REPLAY}
    LIVE_CLAIM_MODES = {DataMode.LIVE}
    HISTORICAL_MODES = {DataMode.REPLAY}
    TEST_ONLY_MODES = {DataMode.FIXTURE, DataMode.OFFLINE}

    @staticmethod
    def classify(mode_str: str) -> Tuple[bool, DataMode, str]:
        """Parse string → DataMode. Returns (ok, mode, reason)."""
        try:
            mode = DataMode(mode_str.upper())
            return True, mode, ""
        except (ValueError, AttributeError):
            return False, DataMode.OFFLINE, f"unknown data mode: {mode_str!r} — BLOCK"

    @staticmethod
    def can_generate_formal_conclusion(mode: DataMode) -> Tuple[bool, str]:
        if mode == DataMode.FIXTURE:
            return False, "FIXTURE data cannot generate formal research conclusion"
        if mode == DataMode.OFFLINE:
            return False, "OFFLINE data cannot claim live"
        return True, ""

    @staticmethod
    def validate_for_paper_trading(mode: DataMode) -> Tuple[bool, str]:
        if mode is None:
            return False, "data_mode is None — BLOCK"
        if mode == DataMode.OFFLINE:
            return True, "OFFLINE: paper simulation permitted, no live claims"
        if mode == DataMode.FIXTURE:
            return True, "FIXTURE: paper simulation permitted, labeled TEST_FIXTURE"
        if mode == DataMode.DELAYED:
            return True, f"DELAYED: paper simulation permitted, delay must be disclosed"
        if mode == DataMode.REPLAY:
            return True, "REPLAY: historical simulation, labeled historical"
        if mode == DataMode.LIVE:
            return True, "LIVE: paper simulation only, not real order"
        return False, f"unrecognized data mode: {mode} — BLOCK"

    @staticmethod
    def get_label(mode: DataMode) -> str:
        labels = {
            DataMode.LIVE: "LIVE_DATA_PAPER_SIMULATION_ONLY",
            DataMode.DELAYED: "DELAYED_DATA_PAPER_SIMULATION_ONLY",
            DataMode.REPLAY: "HISTORICAL_REPLAY_SIMULATION_ONLY",
            DataMode.FIXTURE: "TEST_FIXTURE_NOT_FOR_FORMAL_CONCLUSION",
            DataMode.OFFLINE: "OFFLINE_PAPER_SIMULATION",
        }
        return labels.get(mode, "UNKNOWN_DATA_MODE_BLOCKED")

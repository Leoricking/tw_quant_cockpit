"""
paper_trading/multi_session/symbol_exposure_v166.py — Symbol Exposure Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No real orders. No portfolio ledger writes. Output: BLOCK/WARN/ALLOW/REQUIRE_REVIEW/DEGRADE.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import CoordinationOutcome
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_PORTFOLIO_LEDGER_WRITES = True
NO_AUTO_REBALANCE = True
NO_AUTO_HEDGE = True


class SymbolExposureCoordinator:
    """Cross-session symbol exposure. Paper simulation only."""

    def compute(self, sessions: List[SessionDescriptor]) -> Dict[str, Any]:
        symbol_sessions: Dict[str, List[str]] = {}
        for s in sessions:
            for sym in s.symbols:
                symbol_sessions.setdefault(sym, []).append(s.session_id)

        overlapping = {sym: sids for sym, sids in symbol_sessions.items() if len(sids) > 1}
        outcome = CoordinationOutcome.PASS
        warnings: List[str] = []
        if overlapping:
            outcome = CoordinationOutcome.WARN
            warnings = [f"Overlap: {sym} in {sids}" for sym, sids in overlapping.items()]

        return {
            "per_session_symbols": {s.session_id: s.symbols for s in sessions},
            "symbol_sessions": symbol_sessions,
            "overlapping": overlapping,
            "total_unique_symbols": len(symbol_sessions),
            "outcome": outcome.value,
            "warnings": warnings,
        }

    def detect_direction_conflict(
        self,
        session_positions: Dict[str, Dict[str, str]],
    ) -> List[Dict[str, Any]]:
        conflicts = []
        symbol_dirs: Dict[str, Dict[str, str]] = {}
        for sid, positions in session_positions.items():
            for sym, direction in positions.items():
                symbol_dirs.setdefault(sym, {})[sid] = direction
        for sym, dirs in symbol_dirs.items():
            unique_dirs = set(dirs.values())
            if len(unique_dirs) > 1:
                conflicts.append({"symbol": sym, "sessions": dirs, "conflict": "direction_conflict"})
        return conflicts

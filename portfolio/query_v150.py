"""
portfolio/query_v150.py — Portfolio query service for v1.5.0.

21 read-oriented query methods from create_research_portfolio
through get_portfolio_lineage.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True

from .store_v150 import PortfolioStore
from .ledger_v150 import PortfolioLedger
from .position_v150 import PortfolioPositionService
from .cash_v150 import PortfolioCashService
from .valuation_v150 import PortfolioValuationEngine
from .pnl_v150 import PortfolioPnLCalculator
from .returns_v150 import PortfolioReturnCalculator
from .exposure_v150 import PortfolioExposureCalculator
from .concentration_v150 import PortfolioConcentrationAnalyzer
from .snapshot_v150 import PortfolioSnapshotBuilder
from .lineage_v150 import PortfolioLineageTracker
from .eligibility_v150 import PortfolioDataEligibilityGate
from .point_in_time_v150 import PortfolioPITValidator


class PortfolioQueryService:
    RESEARCH_ONLY = True

    def __init__(
        self,
        store: Optional[PortfolioStore] = None,
        ledger: Optional[PortfolioLedger] = None,
    ):
        self.store = store or PortfolioStore(use_temp_db=True)
        self.ledger = ledger or PortfolioLedger()
        self._position_svc = PortfolioPositionService()
        self._cash_svc = PortfolioCashService()
        self._valuation_eng = PortfolioValuationEngine()
        self._pnl_calc = PortfolioPnLCalculator()
        self._return_calc = PortfolioReturnCalculator()
        self._exposure_calc = PortfolioExposureCalculator()
        self._concentration = PortfolioConcentrationAnalyzer()
        self._snapshot_builder = PortfolioSnapshotBuilder()
        self._lineage = PortfolioLineageTracker()
        self._eligibility = PortfolioDataEligibilityGate()
        self._pit = PortfolioPITValidator()

    # 1
    def create_research_portfolio(self, portfolio_def: Dict) -> str:
        """Create and store a research portfolio. Returns portfolio_id."""
        return self.store.save_portfolio(portfolio_def)

    # 2
    def get_portfolio(self, portfolio_id: str) -> Optional[Dict]:
        return self.store.get_portfolio(portfolio_id)

    # 3
    def list_portfolios(self) -> List[Dict]:
        return self.store.list_portfolios()

    # 4
    def add_transaction(self, portfolio_id: str, txn: Dict) -> str:
        self.ledger.append(txn)
        return self.store.append_transaction(portfolio_id, txn)

    # 5
    def get_transactions(self, portfolio_id: str) -> List[Dict]:
        return self.store.get_transactions(portfolio_id)

    # 6
    def get_positions_as_of(self, portfolio_id: str, as_of: str) -> List[Dict]:
        replay = self.ledger.replay(portfolio_id, as_of)
        return self._position_svc.get_positions_as_of(replay)

    # 7
    def get_cash_as_of(self, portfolio_id: str, as_of: str) -> List[Dict]:
        replay = self.ledger.replay(portfolio_id, as_of)
        return self._cash_svc.get_cash_as_of(replay)

    # 8
    def get_valuation(
        self, portfolio_id: str, as_of: str, price_map: Dict
    ) -> Dict:
        replay = self.ledger.replay(portfolio_id, as_of)
        positions = self._position_svc.get_positions_as_of(replay)
        cash_twd = self._cash_svc.total_cash_twd(replay)
        return self._valuation_eng.value_positions(positions, price_map, as_of, cash_twd)

    # 9
    def get_pnl_summary(self, portfolio_id: str, as_of: str, price_map: Dict) -> Dict:
        replay = self.ledger.replay(portfolio_id, as_of)
        positions = self._position_svc.get_positions_as_of(replay)
        cash_twd = self._cash_svc.total_cash_twd(replay)
        valuation = self._valuation_eng.value_positions(positions, price_map, as_of, cash_twd)
        realized = replay.get("realized_pnl", {})
        return self._pnl_calc.aggregate_portfolio_pnl(valuation, realized)

    # 10
    def get_exposure(
        self, portfolio_id: str, as_of: str, price_map: Dict,
        classification_map: Optional[Dict] = None
    ) -> Dict:
        replay = self.ledger.replay(portfolio_id, as_of)
        positions = self._position_svc.get_positions_as_of(replay)
        cash_twd = self._cash_svc.total_cash_twd(replay)
        valuation = self._valuation_eng.value_positions(positions, price_map, as_of, cash_twd)
        pos_vals = valuation.get("position_valuations", [])
        total_val = valuation.get("total_value", Decimal("0"))
        return self._exposure_calc.calculate(pos_vals, cash_twd, total_val, classification_map or {})

    # 11
    def get_concentration(self, portfolio_id: str, as_of: str, price_map: Dict) -> Dict:
        replay = self.ledger.replay(portfolio_id, as_of)
        positions = self._position_svc.get_positions_as_of(replay)
        cash_twd = self._cash_svc.total_cash_twd(replay)
        valuation = self._valuation_eng.value_positions(positions, price_map, as_of, cash_twd)
        pos_vals = valuation.get("position_valuations", [])
        total = Decimal(str(valuation.get("total_value", 0) or 0))
        weights: Dict[str, Decimal] = {}
        if total > Decimal("0"):
            for pv in pos_vals:
                sym = pv.get("symbol", "")
                mkt = Decimal(str(pv.get("market_value", 0) or 0))
                weights[sym] = mkt / total
        return self._concentration.analyze(weights)

    # 12
    def take_snapshot(
        self, portfolio_id: str, as_of: str, price_map: Dict
    ) -> Dict:
        replay = self.ledger.replay(portfolio_id, as_of)
        positions = self._position_svc.get_positions_as_of(replay)
        cash_balances = self._cash_svc.get_cash_as_of(replay)
        valuation = self._valuation_eng.value_positions(
            positions, price_map, as_of,
            self._cash_svc.total_cash_twd(replay)
        )
        snap = self._snapshot_builder.build(
            portfolio_id, as_of, positions, cash_balances, valuation
        )
        self.store.save_snapshot(portfolio_id, snap)
        return snap

    # 13
    def get_snapshots(self, portfolio_id: str) -> List[Dict]:
        return self.store.get_snapshots(portfolio_id)

    # 14
    def get_latest_snapshot(self, portfolio_id: str) -> Optional[Dict]:
        return self.store.get_latest_snapshot(portfolio_id)

    # 15
    def run_eligibility_gate(self, context: Dict) -> Dict:
        return self._eligibility.run(context)

    # 16
    def validate_pit(
        self, transactions: List[Dict], price_map: Optional[Dict],
        as_of: Optional[str]
    ) -> Dict:
        return self._pit.validate(transactions, price_map, as_of)

    # 17
    def get_open_symbols(self, portfolio_id: str, as_of: str) -> List[str]:
        replay = self.ledger.replay(portfolio_id, as_of)
        return self._position_svc.get_open_symbols(replay)

    # 18
    def get_total_value(self, portfolio_id: str, as_of: str, price_map: Dict) -> Optional[Decimal]:
        replay = self.ledger.replay(portfolio_id, as_of)
        positions = self._position_svc.get_positions_as_of(replay)
        cash_twd = self._cash_svc.total_cash_twd(replay)
        valuation = self._valuation_eng.value_positions(positions, price_map, as_of, cash_twd)
        return valuation.get("total_value")

    # 19
    def build_lineage_chain(
        self, snapshot_id: str, valuation_id: Optional[str],
        price_source: Optional[str], provider_id: Optional[str],
        source_id: Optional[str], authority_tier: Optional[str] = None,
    ) -> Dict:
        return self._lineage.build_chain(
            snapshot_id, valuation_id, price_source,
            provider_id, source_id, authority_tier
        )

    # 20
    def verify_snapshot_integrity(self, snapshot: Dict) -> bool:
        return self._snapshot_builder.verify_integrity(snapshot)

    # 21
    def get_portfolio_lineage(self, portfolio_id: str) -> List[Dict]:
        snaps = self.store.get_snapshots(portfolio_id)
        return [
            self._lineage.build_chain(
                s.get("snapshot_id", ""),
                s.get("valuation_id"),
                None, None, None
            )
            for s in snaps
        ]

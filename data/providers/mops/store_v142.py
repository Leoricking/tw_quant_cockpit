"""
data/providers/mops/store_v142.py — MOPS data store v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
In-memory store for fetched MOPS data (no auto-download, no auto-repair).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.providers.mops.models_v142 import (
    MOPSBalanceSheet,
    MOPSCashFlowStatement,
    MOPSCompanyProfile,
    MOPSFinancialReportFiling,
    MOPSIncomeStatement,
    MOPSInvestorConference,
    MOPSMaterialInformation,
    MOPSMonthlyRevenue,
    MOPSRevisionRecord,
    MOPSXBRLDocument,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
MOPS_AUTO_DOWNLOAD_ENABLED = False


class MOPSStore:
    """
    In-memory store for MOPS data.
    No auto-download. No mock fallback. Research only.
    """

    def __init__(self) -> None:
        self._profiles: Dict[str, MOPSCompanyProfile] = {}
        self._revenues: Dict[str, MOPSMonthlyRevenue] = {}
        self._filings: Dict[str, List[MOPSFinancialReportFiling]] = {}
        self._balance_sheets: Dict[str, MOPSBalanceSheet] = {}
        self._income_statements: Dict[str, MOPSIncomeStatement] = {}
        self._cash_flows: Dict[str, MOPSCashFlowStatement] = {}
        self._material_info: Dict[str, List[MOPSMaterialInformation]] = {}
        self._conferences: Dict[str, List[MOPSInvestorConference]] = {}
        self._xbrl_docs: Dict[str, List[MOPSXBRLDocument]] = {}
        self._revisions: Dict[str, List[MOPSRevisionRecord]] = {}

    # Company profile
    def put_profile(self, profile: MOPSCompanyProfile) -> None:
        self._profiles[profile.symbol] = profile

    def get_profile(self, symbol: str) -> Optional[MOPSCompanyProfile]:
        return self._profiles.get(symbol)

    # Monthly revenue
    def put_revenue(self, record: MOPSMonthlyRevenue) -> None:
        key = f"{record.symbol}:{record.year_month}"
        self._revenues[key] = record

    def get_revenue(self, symbol: str, year_month: str) -> Optional[MOPSMonthlyRevenue]:
        return self._revenues.get(f"{symbol}:{year_month}")

    # Financial report filings
    def put_filings(self, symbol: str, fiscal_year: int, filings: List[MOPSFinancialReportFiling]) -> None:
        key = f"{symbol}:{fiscal_year}"
        self._filings[key] = filings

    def get_filings(self, symbol: str, fiscal_year: int) -> List[MOPSFinancialReportFiling]:
        return self._filings.get(f"{symbol}:{fiscal_year}", [])

    # Balance sheet
    def put_balance_sheet(self, bs: MOPSBalanceSheet) -> None:
        key = f"{bs.symbol}:{bs.fiscal_year}:{bs.fiscal_period}"
        self._balance_sheets[key] = bs

    def get_balance_sheet(self, symbol: str, fiscal_year: int, fiscal_period: str) -> Optional[MOPSBalanceSheet]:
        return self._balance_sheets.get(f"{symbol}:{fiscal_year}:{fiscal_period}")

    # Income statement
    def put_income_statement(self, is_obj: MOPSIncomeStatement) -> None:
        key = f"{is_obj.symbol}:{is_obj.fiscal_year}:{is_obj.fiscal_period}"
        self._income_statements[key] = is_obj

    def get_income_statement(self, symbol: str, fiscal_year: int, fiscal_period: str) -> Optional[MOPSIncomeStatement]:
        return self._income_statements.get(f"{symbol}:{fiscal_year}:{fiscal_period}")

    # Cash flow
    def put_cash_flow(self, cf: MOPSCashFlowStatement) -> None:
        key = f"{cf.symbol}:{cf.fiscal_year}:{cf.fiscal_period}"
        self._cash_flows[key] = cf

    def get_cash_flow(self, symbol: str, fiscal_year: int, fiscal_period: str) -> Optional[MOPSCashFlowStatement]:
        return self._cash_flows.get(f"{symbol}:{fiscal_year}:{fiscal_period}")

    # Material information
    def put_material_info(self, symbol: str, disclosures: List[MOPSMaterialInformation]) -> None:
        self._material_info[symbol] = disclosures

    def get_material_info(self, symbol: str) -> List[MOPSMaterialInformation]:
        return self._material_info.get(symbol, [])

    # Investor conferences
    def put_conferences(self, symbol: str, conferences: List[MOPSInvestorConference]) -> None:
        self._conferences[symbol] = conferences

    def get_conferences(self, symbol: str) -> List[MOPSInvestorConference]:
        return self._conferences.get(symbol, [])

    # XBRL docs
    def put_xbrl_docs(self, symbol: str, fiscal_year: int, docs: List[MOPSXBRLDocument]) -> None:
        key = f"{symbol}:{fiscal_year}"
        self._xbrl_docs[key] = docs

    def get_xbrl_docs(self, symbol: str, fiscal_year: int) -> List[MOPSXBRLDocument]:
        return self._xbrl_docs.get(f"{symbol}:{fiscal_year}", [])

    # Revisions
    def put_revision(self, record: MOPSRevisionRecord) -> None:
        key = f"{record.symbol}:{record.original_filing_id}"
        if key not in self._revisions:
            self._revisions[key] = []
        self._revisions[key].append(record)

    def get_revisions(self, symbol: str, filing_id: str) -> List[MOPSRevisionRecord]:
        return self._revisions.get(f"{symbol}:{filing_id}", [])

    def count_all(self) -> Dict[str, int]:
        return {
            "profiles": len(self._profiles),
            "revenues": len(self._revenues),
            "filings": len(self._filings),
            "balance_sheets": len(self._balance_sheets),
            "income_statements": len(self._income_statements),
            "cash_flows": len(self._cash_flows),
            "material_info_symbols": len(self._material_info),
            "conferences_symbols": len(self._conferences),
            "xbrl_doc_keys": len(self._xbrl_docs),
            "revision_keys": len(self._revisions),
        }

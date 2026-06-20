"""
data/providers/mops/models_v142.py — MOPS Provider domain models v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MOPSCapability(str, Enum):
    COMPANY_PROFILE = "COMPANY_PROFILE"
    MONTHLY_REVENUE = "MONTHLY_REVENUE"
    FINANCIAL_REPORT_ANNOUNCEMENT = "FINANCIAL_REPORT_ANNOUNCEMENT"
    BALANCE_SHEET = "BALANCE_SHEET"
    INCOME_STATEMENT = "INCOME_STATEMENT"
    CASH_FLOW = "CASH_FLOW"
    EQUITY_STATEMENT_INDEX = "EQUITY_STATEMENT_INDEX"
    MATERIAL_INFORMATION = "MATERIAL_INFORMATION"
    INVESTOR_CONFERENCE = "INVESTOR_CONFERENCE"
    XBRL_DOCUMENT_INDEX = "XBRL_DOCUMENT_INDEX"
    REVISION_LINEAGE = "REVISION_LINEAGE"
    POINT_IN_TIME_AVAILABILITY = "POINT_IN_TIME_AVAILABILITY"
    DERIVED_FINANCIAL_METRICS = "DERIVED_FINANCIAL_METRICS"


class MOPSFetchStatus(str, Enum):
    SUCCESS = "SUCCESS"
    RATE_LIMITED = "RATE_LIMITED"
    BLOCKED = "BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"
    MALFORMED = "MALFORMED"
    TIMEOUT = "TIMEOUT"
    NETWORK_ERROR = "NETWORK_ERROR"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    MAINTENANCE = "MAINTENANCE"
    MARKET_CONFLICT = "MARKET_CONFLICT"
    REVISION_DETECTED = "REVISION_DETECTED"


class MOPSDocumentType(str, Enum):
    BALANCE_SHEET = "BALANCE_SHEET"
    INCOME_STATEMENT = "INCOME_STATEMENT"
    CASH_FLOW = "CASH_FLOW"
    EQUITY_STATEMENT = "EQUITY_STATEMENT"
    NOTES = "NOTES"
    FULL_REPORT = "FULL_REPORT"
    XBRL = "XBRL"
    UNKNOWN = "UNKNOWN"


class MOPSReportPeriod(str, Enum):
    ANNUAL = "ANNUAL"
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"
    MONTHLY = "MONTHLY"
    UNKNOWN = "UNKNOWN"


class MOPSMarket(str, Enum):
    TWSE = "TWSE"
    TPEX = "TPEx"
    EMERGING = "EMERGING"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

@dataclass
class MOPSProvenance:
    """Provenance record for a MOPS data fetch."""
    provider_id: str
    official_source: bool
    endpoint_id: str
    source_url: str
    requested_at: str
    received_at: str
    source_timestamp: Optional[str]
    fiscal_period: Optional[str]
    response_format: str
    schema_version: str
    content_hash: Optional[str]
    request_id: Optional[str]
    revision_detected: bool
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "official_source": self.official_source,
            "endpoint_id": self.endpoint_id,
            "source_url": self.source_url,
            "requested_at": self.requested_at,
            "received_at": self.received_at,
            "source_timestamp": self.source_timestamp,
            "fiscal_period": self.fiscal_period,
            "response_format": self.response_format,
            "schema_version": self.schema_version,
            "content_hash": self.content_hash,
            "request_id": self.request_id,
            "revision_detected": self.revision_detected,
            "warnings": list(self.warnings),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSProvenance":
        return cls(
            provider_id=d.get("provider_id", ""),
            official_source=d.get("official_source", True),
            endpoint_id=d.get("endpoint_id", ""),
            source_url=d.get("source_url", ""),
            requested_at=d.get("requested_at", ""),
            received_at=d.get("received_at", ""),
            source_timestamp=d.get("source_timestamp"),
            fiscal_period=d.get("fiscal_period"),
            response_format=d.get("response_format", "HTML"),
            schema_version=d.get("schema_version", "1.4.2"),
            content_hash=d.get("content_hash"),
            request_id=d.get("request_id"),
            revision_detected=d.get("revision_detected", False),
            warnings=d.get("warnings", []),
        )


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class MOPSCompanyProfile:
    """Company profile from MOPS."""
    TEST_FIXTURE: bool = False
    DEMO_ONLY: bool = False
    NOT_REAL_DATA: bool = False
    NOT_FOR_FORMAL_CONCLUSION: bool = False

    symbol: str = ""
    company_name: Optional[str] = None
    english_name: Optional[str] = None
    market: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    chairman: Optional[str] = None
    ceo: Optional[str] = None
    registered_capital: Optional[str] = None
    capital_unit: Optional[str] = None
    paid_in_capital: Optional[str] = None
    fiscal_year_end: Optional[str] = None
    listing_date: Optional[str] = None
    address: Optional[str] = None
    telephone: Optional[str] = None
    ir_email: Optional[str] = None
    stock_transfer_agent: Optional[str] = None
    auditor: Optional[str] = None
    auditor_firm: Optional[str] = None
    source_timestamp: Optional[str] = None
    fetched_at: str = ""
    provider_id: str = "mops_official"
    provenance: Optional[MOPSProvenance] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "english_name": self.english_name,
            "market": self.market,
            "industry_code": self.industry_code,
            "industry_name": self.industry_name,
            "chairman": self.chairman,
            "ceo": self.ceo,
            "registered_capital": self.registered_capital,
            "capital_unit": self.capital_unit,
            "paid_in_capital": self.paid_in_capital,
            "fiscal_year_end": self.fiscal_year_end,
            "listing_date": self.listing_date,
            "address": self.address,
            "telephone": self.telephone,
            "ir_email": self.ir_email,
            "stock_transfer_agent": self.stock_transfer_agent,
            "auditor": self.auditor,
            "auditor_firm": self.auditor_firm,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSCompanyProfile":
        prov = d.get("provenance")
        obj = cls()
        obj.symbol = d.get("symbol", "")
        obj.company_name = d.get("company_name")
        obj.english_name = d.get("english_name")
        obj.market = d.get("market")
        obj.industry_code = d.get("industry_code")
        obj.industry_name = d.get("industry_name")
        obj.chairman = d.get("chairman")
        obj.ceo = d.get("ceo")
        obj.registered_capital = d.get("registered_capital")
        obj.capital_unit = d.get("capital_unit")
        obj.paid_in_capital = d.get("paid_in_capital")
        obj.fiscal_year_end = d.get("fiscal_year_end")
        obj.listing_date = d.get("listing_date")
        obj.address = d.get("address")
        obj.telephone = d.get("telephone")
        obj.ir_email = d.get("ir_email")
        obj.stock_transfer_agent = d.get("stock_transfer_agent")
        obj.auditor = d.get("auditor")
        obj.auditor_firm = d.get("auditor_firm")
        obj.source_timestamp = d.get("source_timestamp")
        obj.fetched_at = d.get("fetched_at", "")
        obj.provider_id = d.get("provider_id", "mops_official")
        obj.provenance = MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None
        obj.warnings = d.get("warnings", [])
        obj.metadata = d.get("metadata", {})
        return obj


@dataclass
class MOPSMonthlyRevenue:
    """Monthly revenue record from MOPS."""
    symbol: str
    year_month: str  # YYYY-MM
    revenue: Optional[float]
    revenue_unit: str  # e.g. "TWD_THOUSAND"
    revenue_last_month: Optional[float]
    revenue_last_year_same_month: Optional[float]
    mom_change_percent: Optional[float]
    yoy_change_percent: Optional[float]
    ytd_revenue: Optional[float]
    ytd_last_year: Optional[float]
    ytd_yoy_change_percent: Optional[float]
    is_revision: bool
    revision_note: Optional[str]
    announcement_date: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "year_month": self.year_month,
            "revenue": self.revenue,
            "revenue_unit": self.revenue_unit,
            "revenue_last_month": self.revenue_last_month,
            "revenue_last_year_same_month": self.revenue_last_year_same_month,
            "mom_change_percent": self.mom_change_percent,
            "yoy_change_percent": self.yoy_change_percent,
            "ytd_revenue": self.ytd_revenue,
            "ytd_last_year": self.ytd_last_year,
            "ytd_yoy_change_percent": self.ytd_yoy_change_percent,
            "is_revision": self.is_revision,
            "revision_note": self.revision_note,
            "announcement_date": self.announcement_date,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSMonthlyRevenue":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            year_month=d["year_month"],
            revenue=d.get("revenue"),
            revenue_unit=d.get("revenue_unit", "TWD_THOUSAND"),
            revenue_last_month=d.get("revenue_last_month"),
            revenue_last_year_same_month=d.get("revenue_last_year_same_month"),
            mom_change_percent=d.get("mom_change_percent"),
            yoy_change_percent=d.get("yoy_change_percent"),
            ytd_revenue=d.get("ytd_revenue"),
            ytd_last_year=d.get("ytd_last_year"),
            ytd_yoy_change_percent=d.get("ytd_yoy_change_percent"),
            is_revision=d.get("is_revision", False),
            revision_note=d.get("revision_note"),
            announcement_date=d.get("announcement_date"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSFinancialReportFiling:
    """A financial report filing announcement from MOPS."""
    symbol: str
    fiscal_year: int
    fiscal_period: str  # Q1, Q2, Q3, Q4, ANNUAL
    report_type: str
    filing_date: Optional[str]
    announcement_date: Optional[str]
    document_url: Optional[str]
    xbrl_url: Optional[str]
    is_restated: bool
    restatement_date: Optional[str]
    restatement_reason: Optional[str]
    auditor_opinion: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "fiscal_year": self.fiscal_year,
            "fiscal_period": self.fiscal_period,
            "report_type": self.report_type,
            "filing_date": self.filing_date,
            "announcement_date": self.announcement_date,
            "document_url": self.document_url,
            "xbrl_url": self.xbrl_url,
            "is_restated": self.is_restated,
            "restatement_date": self.restatement_date,
            "restatement_reason": self.restatement_reason,
            "auditor_opinion": self.auditor_opinion,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSFinancialReportFiling":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            fiscal_year=int(d["fiscal_year"]),
            fiscal_period=d.get("fiscal_period", "UNKNOWN"),
            report_type=d.get("report_type", "UNKNOWN"),
            filing_date=d.get("filing_date"),
            announcement_date=d.get("announcement_date"),
            document_url=d.get("document_url"),
            xbrl_url=d.get("xbrl_url"),
            is_restated=d.get("is_restated", False),
            restatement_date=d.get("restatement_date"),
            restatement_reason=d.get("restatement_reason"),
            auditor_opinion=d.get("auditor_opinion"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSBalanceSheet:
    """Balance sheet data from MOPS financial report."""
    symbol: str
    fiscal_year: int
    fiscal_period: str
    currency: str
    unit: str  # e.g. "TWD_THOUSAND"
    report_date: Optional[str]
    total_assets: Optional[float]
    current_assets: Optional[float]
    non_current_assets: Optional[float]
    cash_and_equivalents: Optional[float]
    receivables: Optional[float]
    inventories: Optional[float]
    total_liabilities: Optional[float]
    current_liabilities: Optional[float]
    non_current_liabilities: Optional[float]
    short_term_borrowings: Optional[float]
    long_term_borrowings: Optional[float]
    total_equity: Optional[float]
    common_stock: Optional[float]
    retained_earnings: Optional[float]
    is_balanced: bool
    balance_diff: Optional[float]
    is_consolidated: bool
    is_restated: bool
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "fiscal_year": self.fiscal_year,
            "fiscal_period": self.fiscal_period,
            "currency": self.currency,
            "unit": self.unit,
            "report_date": self.report_date,
            "total_assets": self.total_assets,
            "current_assets": self.current_assets,
            "non_current_assets": self.non_current_assets,
            "cash_and_equivalents": self.cash_and_equivalents,
            "receivables": self.receivables,
            "inventories": self.inventories,
            "total_liabilities": self.total_liabilities,
            "current_liabilities": self.current_liabilities,
            "non_current_liabilities": self.non_current_liabilities,
            "short_term_borrowings": self.short_term_borrowings,
            "long_term_borrowings": self.long_term_borrowings,
            "total_equity": self.total_equity,
            "common_stock": self.common_stock,
            "retained_earnings": self.retained_earnings,
            "is_balanced": self.is_balanced,
            "balance_diff": self.balance_diff,
            "is_consolidated": self.is_consolidated,
            "is_restated": self.is_restated,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSBalanceSheet":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            fiscal_year=int(d["fiscal_year"]),
            fiscal_period=d.get("fiscal_period", "UNKNOWN"),
            currency=d.get("currency", "TWD"),
            unit=d.get("unit", "TWD_THOUSAND"),
            report_date=d.get("report_date"),
            total_assets=d.get("total_assets"),
            current_assets=d.get("current_assets"),
            non_current_assets=d.get("non_current_assets"),
            cash_and_equivalents=d.get("cash_and_equivalents"),
            receivables=d.get("receivables"),
            inventories=d.get("inventories"),
            total_liabilities=d.get("total_liabilities"),
            current_liabilities=d.get("current_liabilities"),
            non_current_liabilities=d.get("non_current_liabilities"),
            short_term_borrowings=d.get("short_term_borrowings"),
            long_term_borrowings=d.get("long_term_borrowings"),
            total_equity=d.get("total_equity"),
            common_stock=d.get("common_stock"),
            retained_earnings=d.get("retained_earnings"),
            is_balanced=d.get("is_balanced", True),
            balance_diff=d.get("balance_diff"),
            is_consolidated=d.get("is_consolidated", True),
            is_restated=d.get("is_restated", False),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSIncomeStatement:
    """Income statement data from MOPS."""
    symbol: str
    fiscal_year: int
    fiscal_period: str
    currency: str
    unit: str
    revenue: Optional[float]
    cost_of_revenue: Optional[float]
    gross_profit: Optional[float]
    operating_expenses: Optional[float]
    operating_income: Optional[float]
    non_operating_income: Optional[float]
    income_before_tax: Optional[float]
    income_tax: Optional[float]
    net_income: Optional[float]
    net_income_attributable_to_parent: Optional[float]
    eps_basic: Optional[float]
    eps_diluted: Optional[float]
    is_consolidated: bool
    is_restated: bool
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "fiscal_year": self.fiscal_year,
            "fiscal_period": self.fiscal_period,
            "currency": self.currency,
            "unit": self.unit,
            "revenue": self.revenue,
            "cost_of_revenue": self.cost_of_revenue,
            "gross_profit": self.gross_profit,
            "operating_expenses": self.operating_expenses,
            "operating_income": self.operating_income,
            "non_operating_income": self.non_operating_income,
            "income_before_tax": self.income_before_tax,
            "income_tax": self.income_tax,
            "net_income": self.net_income,
            "net_income_attributable_to_parent": self.net_income_attributable_to_parent,
            "eps_basic": self.eps_basic,
            "eps_diluted": self.eps_diluted,
            "is_consolidated": self.is_consolidated,
            "is_restated": self.is_restated,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSIncomeStatement":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            fiscal_year=int(d["fiscal_year"]),
            fiscal_period=d.get("fiscal_period", "UNKNOWN"),
            currency=d.get("currency", "TWD"),
            unit=d.get("unit", "TWD_THOUSAND"),
            revenue=d.get("revenue"),
            cost_of_revenue=d.get("cost_of_revenue"),
            gross_profit=d.get("gross_profit"),
            operating_expenses=d.get("operating_expenses"),
            operating_income=d.get("operating_income"),
            non_operating_income=d.get("non_operating_income"),
            income_before_tax=d.get("income_before_tax"),
            income_tax=d.get("income_tax"),
            net_income=d.get("net_income"),
            net_income_attributable_to_parent=d.get("net_income_attributable_to_parent"),
            eps_basic=d.get("eps_basic"),
            eps_diluted=d.get("eps_diluted"),
            is_consolidated=d.get("is_consolidated", True),
            is_restated=d.get("is_restated", False),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSCashFlowStatement:
    """Cash flow statement data from MOPS."""
    symbol: str
    fiscal_year: int
    fiscal_period: str
    currency: str
    unit: str
    operating_cash_flow: Optional[float]
    investing_cash_flow: Optional[float]
    financing_cash_flow: Optional[float]
    net_change_in_cash: Optional[float]
    beginning_cash: Optional[float]
    ending_cash: Optional[float]
    capex: Optional[float]
    free_cash_flow: Optional[float]
    cash_flow_mismatch: bool
    mismatch_amount: Optional[float]
    is_consolidated: bool
    is_restated: bool
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "fiscal_year": self.fiscal_year,
            "fiscal_period": self.fiscal_period,
            "currency": self.currency,
            "unit": self.unit,
            "operating_cash_flow": self.operating_cash_flow,
            "investing_cash_flow": self.investing_cash_flow,
            "financing_cash_flow": self.financing_cash_flow,
            "net_change_in_cash": self.net_change_in_cash,
            "beginning_cash": self.beginning_cash,
            "ending_cash": self.ending_cash,
            "capex": self.capex,
            "free_cash_flow": self.free_cash_flow,
            "cash_flow_mismatch": self.cash_flow_mismatch,
            "mismatch_amount": self.mismatch_amount,
            "is_consolidated": self.is_consolidated,
            "is_restated": self.is_restated,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSCashFlowStatement":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            fiscal_year=int(d["fiscal_year"]),
            fiscal_period=d.get("fiscal_period", "UNKNOWN"),
            currency=d.get("currency", "TWD"),
            unit=d.get("unit", "TWD_THOUSAND"),
            operating_cash_flow=d.get("operating_cash_flow"),
            investing_cash_flow=d.get("investing_cash_flow"),
            financing_cash_flow=d.get("financing_cash_flow"),
            net_change_in_cash=d.get("net_change_in_cash"),
            beginning_cash=d.get("beginning_cash"),
            ending_cash=d.get("ending_cash"),
            capex=d.get("capex"),
            free_cash_flow=d.get("free_cash_flow"),
            cash_flow_mismatch=d.get("cash_flow_mismatch", False),
            mismatch_amount=d.get("mismatch_amount"),
            is_consolidated=d.get("is_consolidated", True),
            is_restated=d.get("is_restated", False),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSMaterialInformation:
    """Material information disclosure from MOPS."""
    symbol: str
    disclosure_id: str
    disclosure_type: str
    title: Optional[str]
    announcement_date: Optional[str]
    effective_date: Optional[str]
    content_summary: Optional[str]
    is_correction: bool
    correction_of_id: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "disclosure_id": self.disclosure_id,
            "disclosure_type": self.disclosure_type,
            "title": self.title,
            "announcement_date": self.announcement_date,
            "effective_date": self.effective_date,
            "content_summary": self.content_summary,
            "is_correction": self.is_correction,
            "correction_of_id": self.correction_of_id,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSMaterialInformation":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            disclosure_id=d.get("disclosure_id", ""),
            disclosure_type=d.get("disclosure_type", "UNKNOWN"),
            title=d.get("title"),
            announcement_date=d.get("announcement_date"),
            effective_date=d.get("effective_date"),
            content_summary=d.get("content_summary"),
            is_correction=d.get("is_correction", False),
            correction_of_id=d.get("correction_of_id"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSInvestorConference:
    """Investor conference record from MOPS."""
    symbol: str
    conference_id: str
    conference_date: Optional[str]
    conference_time: Optional[str]
    location: Optional[str]
    contact_person: Optional[str]
    contact_phone: Optional[str]
    webcast_url: Optional[str]
    announcement_date: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "conference_id": self.conference_id,
            "conference_date": self.conference_date,
            "conference_time": self.conference_time,
            "location": self.location,
            "contact_person": self.contact_person,
            "contact_phone": self.contact_phone,
            "webcast_url": self.webcast_url,
            "announcement_date": self.announcement_date,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSInvestorConference":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            conference_id=d.get("conference_id", ""),
            conference_date=d.get("conference_date"),
            conference_time=d.get("conference_time"),
            location=d.get("location"),
            contact_person=d.get("contact_person"),
            contact_phone=d.get("contact_phone"),
            webcast_url=d.get("webcast_url"),
            announcement_date=d.get("announcement_date"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSFinancialMetric:
    """Derived financial metric from MOPS data."""
    symbol: str
    fiscal_year: int
    fiscal_period: str
    metric_name: str
    metric_value: Optional[float]
    metric_unit: str
    currency: str
    is_derived: bool
    derivation_method: Optional[str]
    available_from: Optional[str]  # ISO date when this data became available
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "fiscal_year": self.fiscal_year,
            "fiscal_period": self.fiscal_period,
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "metric_unit": self.metric_unit,
            "currency": self.currency,
            "is_derived": self.is_derived,
            "derivation_method": self.derivation_method,
            "available_from": self.available_from,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSFinancialMetric":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            fiscal_year=int(d["fiscal_year"]),
            fiscal_period=d.get("fiscal_period", "UNKNOWN"),
            metric_name=d["metric_name"],
            metric_value=d.get("metric_value"),
            metric_unit=d.get("metric_unit", ""),
            currency=d.get("currency", "TWD"),
            is_derived=d.get("is_derived", True),
            derivation_method=d.get("derivation_method"),
            available_from=d.get("available_from"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSXBRLDocument:
    """XBRL document index entry from MOPS."""
    symbol: str
    fiscal_year: int
    fiscal_period: str
    taxonomy: str  # e.g. "general_industry", "financial_industry"
    xbrl_url: Optional[str]
    filing_date: Optional[str]
    report_type: Optional[str]
    document_size_bytes: Optional[int]
    is_inline_xbrl: bool
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "fiscal_year": self.fiscal_year,
            "fiscal_period": self.fiscal_period,
            "taxonomy": self.taxonomy,
            "xbrl_url": self.xbrl_url,
            "filing_date": self.filing_date,
            "report_type": self.report_type,
            "document_size_bytes": self.document_size_bytes,
            "is_inline_xbrl": self.is_inline_xbrl,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSXBRLDocument":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            fiscal_year=int(d["fiscal_year"]),
            fiscal_period=d.get("fiscal_period", "UNKNOWN"),
            taxonomy=d.get("taxonomy", "general_industry"),
            xbrl_url=d.get("xbrl_url"),
            filing_date=d.get("filing_date"),
            report_type=d.get("report_type"),
            document_size_bytes=d.get("document_size_bytes"),
            is_inline_xbrl=d.get("is_inline_xbrl", False),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MOPSRevisionRecord:
    """Revision lineage record for a MOPS filing."""
    symbol: str
    original_filing_id: str
    revision_sequence: int
    revision_date: Optional[str]
    revision_type: str  # e.g. "RESTATEMENT", "CORRECTION", "SUPPLEMENTAL"
    revision_reason: Optional[str]
    affected_periods: List[str]
    affected_line_items: List[str]
    magnitude_description: Optional[str]
    is_material_revision: bool
    available_from: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[MOPSProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "original_filing_id": self.original_filing_id,
            "revision_sequence": self.revision_sequence,
            "revision_date": self.revision_date,
            "revision_type": self.revision_type,
            "revision_reason": self.revision_reason,
            "affected_periods": list(self.affected_periods),
            "affected_line_items": list(self.affected_line_items),
            "magnitude_description": self.magnitude_description,
            "is_material_revision": self.is_material_revision,
            "available_from": self.available_from,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MOPSRevisionRecord":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            original_filing_id=d.get("original_filing_id", ""),
            revision_sequence=int(d.get("revision_sequence", 1)),
            revision_date=d.get("revision_date"),
            revision_type=d.get("revision_type", "UNKNOWN"),
            revision_reason=d.get("revision_reason"),
            affected_periods=d.get("affected_periods", []),
            affected_line_items=d.get("affected_line_items", []),
            magnitude_description=d.get("magnitude_description"),
            is_material_revision=d.get("is_material_revision", False),
            available_from=d.get("available_from"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "mops_official"),
            provenance=MOPSProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )

"""
paper_trading/small_capital_strategy/portfolio_governance_models_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Models
[!] Paper Only. Research Only. Simulation Only. Validation Only.
[!] Portfolio Governance Only. Risk Overlay Only. Dashboard Only.
[!] No Real Orders. No Broker. No Margin. No Leverage.
[!] Not Investment Advice.
"""
from dataclasses import dataclass, field


@dataclass
class PaperPortfolioGovernanceInput:
    portfolio_id: str = ""
    snapshot_date: str = ""
    positions: list = field(default_factory=list)
    exposure_summary: dict = field(default_factory=dict)
    risk_limits: dict = field(default_factory=dict)
    paper_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioGovernanceResult:
    portfolio_id: str = ""
    governance_passed: bool = False
    risk_grade: str = ""
    recommendations: list = field(default_factory=list)
    blocks: list = field(default_factory=list)
    paper_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioSnapshot:
    snapshot_id: str = ""
    snapshot_date: str = ""
    total_positions: int = 0
    total_paper_value: float = 0.0
    cash_buffer: float = 0.0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioPosition:
    symbol: str = ""
    strategy_id: str = ""
    theme: str = ""
    industry: str = ""
    sector: str = ""
    direction: str = ""
    paper_weight: float = 0.0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioStrategyExposure:
    strategy_id: str = ""
    position_count: int = 0
    total_weight: float = 0.0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioThemeExposure:
    theme_name: str = ""
    position_count: int = 0
    total_weight: float = 0.0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioIndustryExposure:
    industry_name: str = ""
    position_count: int = 0
    total_weight: float = 0.0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioMarketExposure:
    taiwan_index_beta: float = 0.0
    tsmc_sensitivity: float = 0.0
    etf_overlap: float = 0.0
    foreign_futures_risk: float = 0.0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioRiskOverlay:
    overlay_id: str = ""
    input_candidate: str = ""
    overlay_passed: bool = False
    block_reason: str = ""
    paper_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioRiskLimit:
    limit_name: str = ""
    limit_value: float = 1.0
    description: str = ""
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioRiskLimitResult:
    limit_name: str = ""
    limit_value: float = 0.0
    current_value: float = 0.0
    breached: bool = False
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioConcentrationRisk:
    dimension: str = ""
    top_symbol: str = ""
    top_weight: float = 0.0
    breach: bool = False
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioCorrelationRisk:
    cluster_id: str = ""
    cluster_symbols: list = field(default_factory=list)
    cluster_weight: float = 0.0
    breach: bool = False
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioThemeOverlap:
    theme_a: str = ""
    theme_b: str = ""
    overlap_score: float = 0.0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioDecisionOverlap:
    decision_a: str = ""
    decision_b: str = ""
    overlap_score: float = 0.0
    duplicate_exposure: bool = False
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioExposureSummary:
    summary_date: str = ""
    symbol_count: int = 0
    theme_count: int = 0
    industry_count: int = 0
    strategy_count: int = 0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioRiskScore:
    score: float = 0.0
    max_score: float = 1.0
    components: dict = field(default_factory=dict)
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioRiskGrade:
    grade: str = "LOW"
    score: float = 0.0
    threshold_low: float = 0.2
    threshold_moderate: float = 0.4
    threshold_elevated: float = 0.6
    threshold_high: float = 0.8
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioRiskRecommendation:
    recommendation: str = ""
    rationale: str = ""
    priority: int = 0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioRiskBlock:
    block_reason: str = ""
    candidate: str = ""
    blocked: bool = True
    paper_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioGovernanceDecision:
    decision_id: str = ""
    decision_type: str = ""
    outcome: str = ""
    rationale: str = ""
    paper_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioGovernanceDashboard:
    dashboard_id: str = ""
    snapshot_date: str = ""
    panels: list = field(default_factory=list)
    paper_only: bool = True
    no_real_orders: bool = True
    dashboard_mutates_strategy: bool = False
    schema_version: str = "198"


@dataclass
class PaperPortfolioGovernanceReport:
    report_id: str = ""
    report_date: str = ""
    sections: list = field(default_factory=list)
    paper_only: bool = True
    no_real_orders: bool = True
    report_triggers_rebalance: bool = False
    schema_version: str = "198"


@dataclass
class PaperPortfolioAuditTrail:
    audit_id: str = ""
    event_type: str = ""
    event_date: str = ""
    detail: str = ""
    paper_only: bool = True
    immutable: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioHealthSummary:
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    paper_only: bool = True
    schema_version: str = "198"


@dataclass
class PaperPortfolioValidationResult:
    valid: bool = False
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    paper_only: bool = True
    schema_version: str = "198"


_ALL_MODEL_NAMES = [
    "PaperPortfolioGovernanceInput", "PaperPortfolioGovernanceResult",
    "PaperPortfolioSnapshot", "PaperPortfolioPosition",
    "PaperPortfolioStrategyExposure", "PaperPortfolioThemeExposure",
    "PaperPortfolioIndustryExposure", "PaperPortfolioMarketExposure",
    "PaperPortfolioRiskOverlay", "PaperPortfolioRiskLimit",
    "PaperPortfolioRiskLimitResult", "PaperPortfolioConcentrationRisk",
    "PaperPortfolioCorrelationRisk", "PaperPortfolioThemeOverlap",
    "PaperPortfolioDecisionOverlap", "PaperPortfolioExposureSummary",
    "PaperPortfolioRiskScore", "PaperPortfolioRiskGrade",
    "PaperPortfolioRiskRecommendation", "PaperPortfolioRiskBlock",
    "PaperPortfolioGovernanceDecision", "PaperPortfolioGovernanceDashboard",
    "PaperPortfolioGovernanceReport", "PaperPortfolioAuditTrail",
    "PaperPortfolioHealthSummary", "PaperPortfolioValidationResult",
]
assert len(_ALL_MODEL_NAMES) == 26

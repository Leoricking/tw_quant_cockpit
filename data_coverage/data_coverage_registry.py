"""
data_coverage/data_coverage_registry.py — DataCoverageRegistry for TW Quant Cockpit v0.6.2.

Registry of ~35 data coverage items across all domains.

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from data_coverage.data_coverage_schema import (
    DOMAIN_PROVIDER, DOMAIN_DAILY_DATA, DOMAIN_INTRADAY, DOMAIN_FINANCIAL,
    DOMAIN_CHIP, DOMAIN_FEATURE_STORE, DOMAIN_REPLAY, DOMAIN_EXPERIMENT,
    DOMAIN_RULE_GOVERNANCE, DOMAIN_REPORT_PACK, DOMAIN_REGRESSION,
    DOMAIN_STABLE_RELEASE, DOMAIN_RESEARCH_INTELLIGENCE,
    DOMAIN_STRATEGY_MEMORY,
    DOMAIN_BACKTEST_COACH,
    DOMAIN_INTELLIGENCE_STABLE,
)

logger = logging.getLogger(__name__)


class DataCoverageRegistry:
    """Registry of all data coverage items.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        self._items: List[dict] = self._build()

    def list_items(self, domain: Optional[str] = None) -> List[dict]:
        """Return all items, optionally filtered by domain."""
        if domain:
            return [i for i in self._items if i["domain"] == domain]
        return list(self._items)

    def _build(self) -> List[dict]:
        """Build the full registry of coverage items."""
        return [
            # ----------------------------------------------------------------
            # Provider domain
            # ----------------------------------------------------------------
            {
                "item_id":          "provider_health_report",
                "domain":           DOMAIN_PROVIDER,
                "dataset_name":     "Provider Health Report",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py provider-health",
                "expected_patterns": [
                    "reports/provider_health_report*.md",
                    "data/backtest_results/provider_reliability*.csv",
                ],
                "owner_module":     "reports.provider_health_report",
            },
            {
                "item_id":          "provider_reliability_report",
                "domain":           DOMAIN_PROVIDER,
                "dataset_name":     "Provider Reliability Report",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py provider-reliability --mode real",
                "expected_patterns": [
                    "reports/provider_reliability_report*.md",
                    "data/backtest_results/provider_reliability*.csv",
                ],
                "owner_module":     "reports.provider_reliability_report",
            },
            {
                "item_id":          "finmind_provider_token",
                "domain":           DOMAIN_PROVIDER,
                "dataset_name":     "FinMind Provider Token",
                "required":         False,
                "environment_limited": True,
                "not_generated":    False,
                "suggested_command": "set FINMIND_TOKEN=<your_token>",
                "expected_patterns": [],
                "owner_module":     "data.providers.finmind_provider",
            },
            {
                "item_id":          "twse_openapi_provider",
                "domain":           DOMAIN_PROVIDER,
                "dataset_name":     "TWSE OpenAPI Provider",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py api-fetch-diagnostics --mode real",
                "expected_patterns": [
                    "data/backtest_results/api_fetch*.csv",
                    "reports/api_fetch_production_report*.md",
                ],
                "owner_module":     "data.providers.twse_provider",
            },
            {
                "item_id":          "api_fetch_diagnostics",
                "domain":           DOMAIN_PROVIDER,
                "dataset_name":     "API Fetch Diagnostics",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py api-fetch-diagnostics --mode real",
                "expected_patterns": [
                    "data/backtest_results/api_fetch*.csv",
                    "reports/api_fetch_production_report*.md",
                ],
                "owner_module":     "reports.api_fetch_status_report",
            },
            # ----------------------------------------------------------------
            # Daily data domain
            # ----------------------------------------------------------------
            {
                "item_id":          "daily_k",
                "domain":           DOMAIN_DAILY_DATA,
                "dataset_name":     "Daily K-line (OHLCV)",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/daily/daily_k.csv",
                    "data/import/daily/*_sample.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            {
                "item_id":          "monthly_revenue",
                "domain":           DOMAIN_DAILY_DATA,
                "dataset_name":     "Monthly Revenue",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/monthly_revenue/monthly_revenue.csv",
                    "data/import/monthly_revenue/*_sample.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            {
                "item_id":          "institutional_trading",
                "domain":           DOMAIN_DAILY_DATA,
                "dataset_name":     "Institutional Trading (三大法人)",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/institutional/institutional.csv",
                    "data/import/institutional/*_sample.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            {
                "item_id":          "margin_balance",
                "domain":           DOMAIN_DAILY_DATA,
                "dataset_name":     "Margin Balance (融資融券)",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/margin/margin.csv",
                    "data/import/margin/*_sample.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            {
                "item_id":          "major_holders",
                "domain":           DOMAIN_DAILY_DATA,
                "dataset_name":     "Major Holders (大股東持股)",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/holder/holder.csv",
                    "data/import/holder/*_sample.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            # ----------------------------------------------------------------
            # Intraday domain
            # ----------------------------------------------------------------
            {
                "item_id":          "intraday_1min",
                "domain":           DOMAIN_INTRADAY,
                "dataset_name":     "Intraday 1-min OHLCV",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py intraday-pipeline --mode real",
                "expected_patterns": [
                    "data/import/intraday/*.csv",
                    "data/import/intraday_standard/*.csv",
                ],
                "owner_module":     "intraday.intraday_pipeline",
            },
            {
                "item_id":          "intraday_5min",
                "domain":           DOMAIN_INTRADAY,
                "dataset_name":     "Intraday 5-min OHLCV",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py intraday-pipeline --mode real",
                "expected_patterns": [
                    "data/import/intraday/*.csv",
                    "data/import/intraday_standard/*.csv",
                ],
                "owner_module":     "intraday.intraday_pipeline",
            },
            {
                "item_id":          "intraday_quality",
                "domain":           DOMAIN_INTRADAY,
                "dataset_name":     "Intraday Data Quality",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py intraday-quality",
                "expected_patterns": [
                    "data/backtest_results/intraday_quality*.csv",
                    "reports/intraday_pipeline_report*.md",
                ],
                "owner_module":     "intraday.intraday_pipeline",
            },
            {
                "item_id":          "intraday_pipeline_report",
                "domain":           DOMAIN_INTRADAY,
                "dataset_name":     "Intraday Pipeline Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py intraday-pipeline --mode real",
                "expected_patterns": [
                    "reports/intraday_pipeline_report*.md",
                    "data/backtest_results/intraday_pipeline*.csv",
                ],
                "owner_module":     "intraday.intraday_pipeline",
            },
            # ----------------------------------------------------------------
            # Financial domain
            # ----------------------------------------------------------------
            {
                "item_id":          "eps",
                "domain":           DOMAIN_FINANCIAL,
                "dataset_name":     "EPS (每股盈餘)",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/fundamental/fundamental.csv",
                    "data/providers/cache/*eps*.json",
                ],
                "owner_module":     "data.real_data_loader",
            },
            {
                "item_id":          "quarterly_financials",
                "domain":           DOMAIN_FINANCIAL,
                "dataset_name":     "Quarterly Financials",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/fundamental/fundamental.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            {
                "item_id":          "gross_margin",
                "domain":           DOMAIN_FINANCIAL,
                "dataset_name":     "Gross Margin (毛利率)",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/fundamental/fundamental.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            {
                "item_id":          "operating_margin",
                "domain":           DOMAIN_FINANCIAL,
                "dataset_name":     "Operating Margin (營業利益率)",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-provider-fetch --mode real",
                "expected_patterns": [
                    "data/import/fundamental/fundamental.csv",
                ],
                "owner_module":     "data.real_data_loader",
            },
            # ----------------------------------------------------------------
            # Feature Store domain
            # ----------------------------------------------------------------
            {
                "item_id":          "technical_features",
                "domain":           DOMAIN_FEATURE_STORE,
                "dataset_name":     "Technical Features",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-stabilization --mode real",
                "expected_patterns": [
                    "data/backtest_results/data_stabilization/data_stabilization_summary*.csv",
                    "data/backtest_results/data_stabilization/*.csv",
                ],
                "owner_module":     "data_stabilization.data_stabilization_engine",
            },
            {
                "item_id":          "microstructure_features",
                "domain":           DOMAIN_FEATURE_STORE,
                "dataset_name":     "Microstructure Features",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-stabilization --mode real",
                "expected_patterns": [
                    "data/backtest_results/data_stabilization/*.csv",
                ],
                "owner_module":     "data_stabilization.data_stabilization_engine",
            },
            {
                "item_id":          "financial_features",
                "domain":           DOMAIN_FEATURE_STORE,
                "dataset_name":     "Financial Features",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-stabilization --mode real",
                "expected_patterns": [
                    "data/backtest_results/data_stabilization/*.csv",
                ],
                "owner_module":     "data_stabilization.data_stabilization_engine",
            },
            {
                "item_id":          "chip_features",
                "domain":           DOMAIN_FEATURE_STORE,
                "dataset_name":     "Chip Features (籌碼面)",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py data-stabilization --mode real",
                "expected_patterns": [
                    "data/backtest_results/data_stabilization/*.csv",
                ],
                "owner_module":     "data_stabilization.data_stabilization_engine",
            },
            {
                "item_id":          "ml_knowledge_features",
                "domain":           DOMAIN_FEATURE_STORE,
                "dataset_name":     "ML Knowledge Features",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py ml-knowledge-integrate --mode real",
                "expected_patterns": [
                    "data/backtest_results/ml_feature_store/*.csv",
                    "data/backtest_results/ml_feature*.csv",
                ],
                "owner_module":     "ml.ml_knowledge_integration",
            },
            # ----------------------------------------------------------------
            # Replay domain
            # ----------------------------------------------------------------
            {
                "item_id":          "intraday_replay_report",
                "domain":           DOMAIN_REPLAY,
                "dataset_name":     "Intraday Replay Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    True,
                "suggested_command": "python main.py intraday-replay-report --mode real",
                "expected_patterns": [
                    "reports/intraday_replay_report*.md",
                    "data/backtest_results/intraday_replay*.csv",
                ],
                "owner_module":     "replay.intraday_replay_engine",
            },
            {
                "item_id":          "replay_training_report",
                "domain":           DOMAIN_REPLAY,
                "dataset_name":     "Replay Training Report",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py replay-training-report --mode real",
                "expected_patterns": [
                    "reports/replay_training_report*.md",
                    "data/backtest_results/replay_training/replay_training_summary*.csv",
                    "data/backtest_results/replay_training/*.csv",
                ],
                "owner_module":     "replay_training.replay_training_engine",
            },
            {
                "item_id":          "replay_training_summary",
                "domain":           DOMAIN_REPLAY,
                "dataset_name":     "Replay Training Summary CSV",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py replay-training-summary",
                "expected_patterns": [
                    "data/backtest_results/replay_training/replay_training_summary*.csv",
                    "data/backtest_results/replay_training/*.csv",
                ],
                "owner_module":     "replay_training.replay_training_store",
            },
            # ----------------------------------------------------------------
            # Experiment domain
            # ----------------------------------------------------------------
            {
                "item_id":          "experiment_registry",
                "domain":           DOMAIN_EXPERIMENT,
                "dataset_name":     "Experiment Registry",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py exp-list",
                "expected_patterns": [
                    "experiments/registry.json",
                    "data/backtest_results/experiment*.csv",
                ],
                "owner_module":     "experiments.experiment_registry",
            },
            {
                "item_id":          "experiment_registry_report",
                "domain":           DOMAIN_EXPERIMENT,
                "dataset_name":     "Experiment Registry Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    True,
                "suggested_command": "python main.py auto-report --profile full --mode real",
                "expected_patterns": [
                    "reports/experiment_registry_report*.md",
                    "data/backtest_results/experiment*.csv",
                ],
                "owner_module":     "reports.experiment_registry_report",
            },
            {
                "item_id":          "experiment_snapshots",
                "domain":           DOMAIN_EXPERIMENT,
                "dataset_name":     "Experiment Snapshots",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py exp-list",
                "expected_patterns": [
                    "experiments/EXP-*",
                    "data/backtest_results/experiment*.json",
                ],
                "owner_module":     "experiments.experiment_registry",
            },
            # ----------------------------------------------------------------
            # Rule Governance domain
            # ----------------------------------------------------------------
            {
                "item_id":          "rule_governance_report",
                "domain":           DOMAIN_RULE_GOVERNANCE,
                "dataset_name":     "Rule Governance Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    True,
                "suggested_command": "python main.py rule-governance --mode real",
                "expected_patterns": [
                    "reports/rule_governance_report*.md",
                    "data/backtest_results/rule_governance*.csv",
                ],
                "owner_module":     "governance.rule_governance_engine",
            },
            {
                "item_id":          "rule_confidence_summary",
                "domain":           DOMAIN_RULE_GOVERNANCE,
                "dataset_name":     "Rule Confidence Summary",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py rule-governance --mode real",
                "expected_patterns": [
                    "data/backtest_results/rule_governance*.csv",
                ],
                "owner_module":     "governance.rule_governance_engine",
            },
            {
                "item_id":          "strategy_knowledge_summary",
                "domain":           DOMAIN_RULE_GOVERNANCE,
                "dataset_name":     "Strategy Knowledge Summary",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py strategy-knowledge-summary",
                "expected_patterns": [
                    "data/backtest_results/strategy_knowledge/*.csv",
                    "data/backtest_results/strategy_knowledge/strategy_knowledge*.csv",
                ],
                "owner_module":     "knowledge.strategy_knowledge_store",
            },
            # ----------------------------------------------------------------
            # Report Pack domain
            # ----------------------------------------------------------------
            {
                "item_id":          "report_pack_full",
                "domain":           DOMAIN_REPORT_PACK,
                "dataset_name":     "Full Report Pack",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py report-pack --type full --mode real",
                "expected_patterns": [
                    "data/backtest_results/report_pack/*.csv",
                    "data/backtest_results/report_pack/report_pack_manifest*.csv",
                ],
                "owner_module":     "report_pack.report_pack_builder",
            },
            {
                "item_id":          "report_pack_health",
                "domain":           DOMAIN_REPORT_PACK,
                "dataset_name":     "Report Pack Health",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py report-pack-health",
                "expected_patterns": [
                    "data/backtest_results/report_pack/report_pack_health*.csv",
                    "data/backtest_results/report_pack/*.csv",
                ],
                "owner_module":     "report_pack.report_health_checker",
            },
            {
                "item_id":          "report_pack_links",
                "domain":           DOMAIN_REPORT_PACK,
                "dataset_name":     "Report Pack Links",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py report-pack-links",
                "expected_patterns": [
                    "data/backtest_results/report_pack/report_pack_links*.csv",
                    "data/backtest_results/report_pack/*.csv",
                ],
                "owner_module":     "report_pack.report_link_builder",
            },
            # ----------------------------------------------------------------
            # Stable Release domain
            # ----------------------------------------------------------------
            {
                "item_id":          "stable_release_report",
                "domain":           DOMAIN_STABLE_RELEASE,
                "dataset_name":     "Stable Release Report",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py stable-v060-check --mode real",
                "expected_patterns": [
                    "reports/stable_release_v0.6.0_report*.md",
                    "reports/stable_release_v060_report*.md",
                    "data/backtest_results/stable_release/*.csv",
                ],
                "owner_module":     "stable_release.stable_release_checklist_v060",
            },
            {
                "item_id":          "stable_release_manifest",
                "domain":           DOMAIN_STABLE_RELEASE,
                "dataset_name":     "Stable Release Manifest",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py stable-v060-manifest",
                "expected_patterns": [
                    "data/backtest_results/stable_release/release_manifest*.json",
                    "data/backtest_results/stable_release/release_manifest*.md",
                ],
                "owner_module":     "stable_release.stable_release_manifest",
            },
            {
                "item_id":          "stable_v060_check",
                "domain":           DOMAIN_STABLE_RELEASE,
                "dataset_name":     "v0.6.0 Capability Check",
                "required":         True,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py stable-v060-check --mode real",
                "expected_patterns": [
                    "data/backtest_results/stable_release/*.csv",
                    "reports/stable_release_v0.6.0_report*.md",
                ],
                "owner_module":     "stable_release.capability_matrix",
            },
            # ----------------------------------------------------------------
            # Research Intelligence domain (v0.7.0)
            # ----------------------------------------------------------------
            {
                "item_id":          "research_intelligence_summary",
                "domain":           DOMAIN_RESEARCH_INTELLIGENCE,
                "dataset_name":     "Research Intelligence Summary",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py research-intelligence --mode real",
                "expected_patterns": [
                    "data/backtest_results/research_intelligence/research_intelligence_summary.csv",
                ],
                "owner_module":     "research_intelligence.research_intelligence_engine",
            },
            {
                "item_id":          "research_intelligence_report",
                "domain":           DOMAIN_RESEARCH_INTELLIGENCE,
                "dataset_name":     "Research Intelligence Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py research-intelligence-report --mode real",
                "expected_patterns": [
                    "reports/research_intelligence_report*.md",
                ],
                "owner_module":     "reports.research_intelligence_report",
            },
            # ----------------------------------------------------------------
            # Strategy Memory domain (v0.7.2)
            # ----------------------------------------------------------------
            {
                "item_id":          "strategy_memory_store",
                "domain":           DOMAIN_STRATEGY_MEMORY,
                "dataset_name":     "Strategy Memory Store",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py strategy-memory --mode real",
                "expected_patterns": [
                    "data/backtest_results/strategy_memory/strategy_memory_items_*.csv",
                    "data/backtest_results/strategy_memory/strategy_memory_summary*.csv",
                ],
                "owner_module":     "strategy_memory.memory_store",
            },
            {
                "item_id":          "strategy_memory_report",
                "domain":           DOMAIN_STRATEGY_MEMORY,
                "dataset_name":     "Strategy Memory Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py strategy-memory-report --mode real",
                "expected_patterns": [
                    "reports/strategy_memory_report_*.md",
                ],
                "owner_module":     "reports.strategy_memory_report",
            },
            # ----------------------------------------------------------------
            # Backtest Coach domain (v0.7.3)
            # ----------------------------------------------------------------
            {
                "item_id":          "backtest_coach_store",
                "domain":           DOMAIN_BACKTEST_COACH,
                "dataset_name":     "Backtest Coach Task Store",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py backtest-coach --mode real",
                "expected_patterns": [
                    "data/backtest_results/backtest_coach/backtest_coach_summary*.csv",
                    "data/backtest_results/backtest_coach/coach_training_tasks.csv",
                ],
                "owner_module":     "backtest_coach.backtest_coach_store",
            },
            {
                "item_id":          "backtest_coach_report",
                "domain":           DOMAIN_BACKTEST_COACH,
                "dataset_name":     "Backtest Coach Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py backtest-coach-report --mode real",
                "expected_patterns": [
                    "reports/backtest_coach_report_*.md",
                ],
                "owner_module":     "reports.backtest_coach_report",
            },
            # ----------------------------------------------------------------
            # Intelligence Stable domain (v0.8.0)
            # ----------------------------------------------------------------
            {
                "item_id":          "intelligence_stable_store",
                "domain":           DOMAIN_INTELLIGENCE_STABLE,
                "dataset_name":     "Research Intelligence Stable Store",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py intelligence-stable --mode real",
                "expected_patterns": [
                    "data/backtest_results/intelligence_stable/intelligence_stable_summary*.csv",
                    "data/backtest_results/intelligence_stable/intelligence_capabilities.csv",
                    "data/backtest_results/intelligence_stable/intelligence_stable_checks*.csv",
                ],
                "owner_module":     "intelligence_stable.intelligence_stable_store",
            },
            {
                "item_id":          "intelligence_stable_manifest",
                "domain":           DOMAIN_INTELLIGENCE_STABLE,
                "dataset_name":     "Research Intelligence Stable Release Manifest",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py intelligence-stable-manifest",
                "expected_patterns": [
                    "data/backtest_results/intelligence_stable/intelligence_release_manifest*.json",
                    "data/backtest_results/intelligence_stable/intelligence_release_manifest*.md",
                ],
                "owner_module":     "intelligence_stable.intelligence_release_manifest",
            },
            {
                "item_id":          "intelligence_stable_report",
                "domain":           DOMAIN_INTELLIGENCE_STABLE,
                "dataset_name":     "Research Intelligence Stable Report",
                "required":         False,
                "environment_limited": False,
                "not_generated":    False,
                "suggested_command": "python main.py intelligence-stable-report --mode real",
                "expected_patterns": [
                    "reports/intelligence_stable_report_*.md",
                ],
                "owner_module":     "reports.intelligence_stable_report",
            },
        ]

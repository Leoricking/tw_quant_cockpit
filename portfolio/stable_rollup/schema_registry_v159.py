"""portfolio/stable_rollup/schema_registry_v159.py — Schema registry v1.5.9."""
from .models_v159 import StableSchemaRecord

PORTFOLIO_SCHEMAS = [
    StableSchemaRecord(schema_id="PortfolioDefinition", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["portfolio_id", "name", "research_only"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioAccount", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["account_id", "portfolio_id"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioTransaction", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["transaction_id", "transaction_type", "effective_at", "available_from"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioPosition", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["symbol", "quantity", "as_of"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioCashBalance", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["amount", "as_of"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioSnapshot", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["snapshot_id", "portfolio_id", "as_of", "content_hash"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioValuation", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["portfolio_id", "as_of", "total_value"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioPnL", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["portfolio_id", "as_of", "realized_pnl", "unrealized_pnl"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PortfolioEligibility", schema_version="1.5.0", introduced_version="1.5.0", stable_version="1.5.0", required_fields=["portfolio_id", "eligible", "as_of"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PositionSizingRequest", schema_version="1.5.1", introduced_version="1.5.1", stable_version="1.5.1", required_fields=["request_id", "portfolio_id", "symbol", "research_only"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PositionSizingPolicy", schema_version="1.5.1", introduced_version="1.5.1", stable_version="1.5.1", required_fields=["policy_id", "version", "research_only"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PositionSizingConstraint", schema_version="1.5.1", introduced_version="1.5.1", stable_version="1.5.1", required_fields=["constraint_type", "value"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="PositionSizingProposal", schema_version="1.5.1", introduced_version="1.5.1", stable_version="1.5.1", required_fields=["proposal_id", "research_only", "executable"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="CorrelationAnalysisRequest", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["request_id", "portfolio_id", "as_of", "research_only"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="CorrelationMatrixResult", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["result_id", "as_of", "content_hash", "research_only"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="CovarianceMatrixResult", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["result_id", "as_of", "content_hash"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="RiskContributionResult", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["result_id", "portfolio_id", "as_of"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="BetaResult", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["result_id", "benchmark", "as_of"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="ExposureBucket", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["bucket_type", "key", "weight"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="ETFOverlapResult", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["result_id", "as_of"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="HiddenConcentrationResult", schema_version="1.5.2", introduced_version="1.5.2", stable_version="1.5.2", required_fields=["result_id", "as_of"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="RiskControlPolicy", schema_version="1.5.3", introduced_version="1.5.3", stable_version="1.5.3", required_fields=["policy_id", "version", "research_only", "auto_apply_enabled"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="RiskControlEvaluation", schema_version="1.5.3", introduced_version="1.5.3", stable_version="1.5.3", required_fields=["evaluation_id", "research_only", "executable", "order_created", "ledger_persisted", "auto_applied"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="DrawdownSummary", schema_version="1.5.3", introduced_version="1.5.3", stable_version="1.5.3", required_fields=["portfolio_id", "as_of", "current_drawdown_percent", "maximum_drawdown_percent"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="DrawdownEpisode", schema_version="1.5.3", introduced_version="1.5.3", stable_version="1.5.3", required_fields=["episode_id", "peak_date", "trough_date", "max_drawdown_percent"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="DrawdownAttribution", schema_version="1.5.3", introduced_version="1.5.3", stable_version="1.5.3", required_fields=["attribution_type", "key", "drawdown_contribution"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="WalkForwardConfiguration", schema_version="1.5.4", introduced_version="1.5.4", stable_version="1.5.4", required_fields=["config_id", "portfolio_id", "start_date", "end_date", "research_only", "auto_apply_enabled"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="WalkForwardWindow", schema_version="1.5.4", introduced_version="1.5.4", stable_version="1.5.4", required_fields=["window_id", "sequence", "training_start", "validation_end", "status"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="HistoricalDecisionContext", schema_version="1.5.4", introduced_version="1.5.4", stable_version="1.5.4", required_fields=["decision_id", "portfolio_id", "as_of", "available_from"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="SimulatedPortfolioTransaction", schema_version="1.5.4", introduced_version="1.5.4", stable_version="1.5.4", required_fields=["transaction_id", "research_only", "executable", "real_order_created", "formal_ledger_persisted"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="WalkForwardWindowResult", schema_version="1.5.4", introduced_version="1.5.4", stable_version="1.5.4", required_fields=["window_id", "status"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="WalkForwardSummary", schema_version="1.5.4", introduced_version="1.5.4", stable_version="1.5.4", required_fields=["run_id", "config_id", "research_only"], optional_fields=["metadata"]),
    StableSchemaRecord(schema_id="ReproducibilityManifest", schema_version="1.5.4", introduced_version="1.5.4", stable_version="1.5.4", required_fields=["run_id", "config_hash", "timezone", "calendar_version"], optional_fields=["metadata"]),
]

# Compute fingerprints
for _s in PORTFOLIO_SCHEMAS:
    _s.fingerprint = _s.compute_fingerprint()


class SchemaRegistryV159:
    def get_all(self):
        return list(PORTFOLIO_SCHEMAS)

    def get_by_id(self, sid):
        return next((s for s in PORTFOLIO_SCHEMAS if s.schema_id == sid), None)

    def get_fingerprints(self):
        return {s.schema_id: s.fingerprint for s in PORTFOLIO_SCHEMAS}

    def validate(self):
        issues = []
        ids = [s.schema_id for s in PORTFOLIO_SCHEMAS]
        if len(ids) != len(set(ids)):
            issues.append("DUPLICATE_SCHEMA_ID")
        for s in PORTFOLIO_SCHEMAS:
            if not s.required_fields:
                issues.append(f"NO_REQUIRED_FIELDS:{s.schema_id}")
        return {"valid": len(issues) == 0, "issues": issues, "count": len(PORTFOLIO_SCHEMAS)}

    def check_drift(self, previous_fingerprints):
        drift = []
        current = self.get_fingerprints()
        for sid, fp in previous_fingerprints.items():
            if sid in current and current[sid] != fp:
                drift.append(f"SCHEMA_DRIFT:{sid}")
        return drift

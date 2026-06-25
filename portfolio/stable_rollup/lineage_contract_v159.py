"""portfolio/stable_rollup/lineage_contract_v159.py — Lineage contract v1.5.9."""
from .models_v159 import StableContractRecord

LINEAGE_CONTRACT = StableContractRecord(
    contract_id="portfolio_lineage_contract_v159",
    contract_type="LINEAGE",
    version="1.5.9",
    rules=[
        "Every stable result must have a content_hash",
        "Every stable result must have a calculation_version",
        "Every stable result must have a code_version",
        "Every stable result must have source_lineage_ids or source_lineage",
        "Every stable result must have policy_versions",
        "Every stable result must have a snapshot_hash (where applicable)",
        "Every stable result must have generated_at and as_of",
        "Orphan results (no traceable source) are forbidden",
        "Missing source authority is forbidden",
        "Missing policy version is forbidden",
        "Broken parent references are forbidden",
    ],
    blocking_violations=[
        "orphan_result",
        "missing_source_authority",
        "missing_calculation_version",
        "missing_content_hash",
        "broken_parent_reference",
    ],
    status="VALID",
)

LINEAGE_CHAINS = {
    "portfolio_report": "Portfolio Report → Snapshot → Positions/Cash → Ledger Transactions",
    "sizing_proposal": "Sizing Proposal → Request → Snapshot → Price/ATR/Liquidity → Provider",
    "correlation_analysis": "Correlation → Matrices → Returns → Historical Prices → Provider",
    "risk_evaluation": "Risk Evaluation → Drawdown → Equity Curve → Valuations → Ledger/Prices",
    "walk_forward_result": "Walk-forward → Windows → Decisions → Sim Ledger → Policies → Historical Data",
}


class LineageContractV159:
    def get_contract(self):
        return LINEAGE_CONTRACT

    def get_chains(self):
        return LINEAGE_CHAINS

    def validate_result(self, result):
        violations = []
        required = ["content_hash", "calculation_version"]
        for r in required:
            if not result.get(r):
                violations.append(f"MISSING_{r.upper()}")
        if not result.get("source_lineage_ids") and not result.get("source_lineage"):
            violations.append("MISSING_SOURCE_LINEAGE")
        return {"is_valid": len(violations) == 0, "violations": violations}

    def check_drift(self):
        return []

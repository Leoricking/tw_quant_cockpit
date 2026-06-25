"""portfolio/stable_rollup/migration_registry_v159.py — Migration registry v1.5.9."""
from .models_v159 import StableMigrationRecord

MIGRATION_REGISTRY = [
    StableMigrationRecord(migration_id="1.5.0_to_1.5.0.1", source_version="1.5.0", target_version="1.5.0.1", schema_changes=[], cli_changes=[], notes="NO_DATA_MIGRATION_REQUIRED"),
    StableMigrationRecord(migration_id="1.5.0.1_to_1.5.0.2", source_version="1.5.0.1", target_version="1.5.0.2", schema_changes=[], cli_changes=["added portfolio CLI completeness commands"], notes="NO_DATA_MIGRATION_REQUIRED"),
    StableMigrationRecord(migration_id="1.5.0.2_to_1.5.1", source_version="1.5.0.2", target_version="1.5.1", schema_changes=["PositionSizingRequest added", "PositionSizingProposal added"], enum_changes=["SizingMethod added", "SizingStatus added"], cli_changes=["sizing commands added"], notes="NO_DATA_MIGRATION_REQUIRED"),
    StableMigrationRecord(migration_id="1.5.1_to_1.5.2", source_version="1.5.1", target_version="1.5.2", schema_changes=["CorrelationMatrixResult added", "ExposureBucket added", "ETFOverlapResult added"], enum_changes=["CorrelationMethod added", "ExposureType added"], cli_changes=["correlation commands added"], notes="NO_DATA_MIGRATION_REQUIRED"),
    StableMigrationRecord(migration_id="1.5.2_to_1.5.2.1", source_version="1.5.2", target_version="1.5.2.1", schema_changes=[], cli_changes=[], notes="NO_DATA_MIGRATION_REQUIRED - integrity hotfix"),
    StableMigrationRecord(migration_id="1.5.2.1_to_1.5.3", source_version="1.5.2.1", target_version="1.5.3", schema_changes=["RiskControlPolicy added", "DrawdownSummary added", "DrawdownEpisode added"], enum_changes=["RiskControlStatus added", "RiskActionType added"], cli_changes=["drawdown and risk commands added"], notes="NO_DATA_MIGRATION_REQUIRED"),
    StableMigrationRecord(migration_id="1.5.3_to_1.5.4", source_version="1.5.3", target_version="1.5.4", schema_changes=["WalkForwardConfiguration added", "SimulatedPortfolioTransaction added", "ReproducibilityManifest added"], enum_changes=["WindowType added", "ReplayStatus added"], cli_changes=["walk-forward commands added"], notes="NO_DATA_MIGRATION_REQUIRED"),
    StableMigrationRecord(migration_id="1.5.4_to_1.5.9", source_version="1.5.4", target_version="1.5.9", schema_changes=["StableManifest added", "StableRollupResult added"], enum_changes=["CapabilityStage added", "DebtSeverity added"], cli_changes=["portfolio-stable-* commands added"], notes="NO_DATA_MIGRATION_REQUIRED - freeze/stabilization release"),
]


class MigrationRegistryV159:
    def get_all(self):
        return list(MIGRATION_REGISTRY)

    def get_path(self, src, tgt):
        return next((m for m in MIGRATION_REGISTRY if m.source_version == src and m.target_version == tgt), None)

    def validate(self):
        issues = []
        ids = [m.migration_id for m in MIGRATION_REGISTRY]
        if len(ids) != len(set(ids)):
            issues.append("DUPLICATE_MIGRATION_ID")
        for m in MIGRATION_REGISTRY:
            if m.data_migration_required and "NO_DATA_MIGRATION" in m.notes:
                issues.append(f"INCONSISTENT_MIGRATION:{m.migration_id}")
        return {"valid": len(issues) == 0, "issues": issues, "count": len(MIGRATION_REGISTRY)}

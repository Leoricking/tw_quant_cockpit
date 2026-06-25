"""portfolio/stable_rollup/stable_manifest_v159.py — Stable manifest builder v1.5.9."""
import datetime
import json
from .models_v159 import StableManifest
from .capability_registry_v159 import CapabilityRegistryV159
from .schema_registry_v159 import SchemaRegistryV159
from .enum_registry_v159 import EnumRegistryV159


class StableManifestBuilder:
    def build(self, commit="unknown") -> StableManifest:
        cap_reg = CapabilityRegistryV159()
        schema_reg = SchemaRegistryV159()
        enum_reg = EnumRegistryV159()

        try:
            from release.version_info import VERSION, RELEASE_NAME
        except Exception:
            VERSION, RELEASE_NAME = "1.5.9", "Portfolio Stable Rollup"

        manifest = StableManifest(
            version=VERSION,
            release=RELEASE_NAME,
            commit=commit,
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            baselines={
                "replay": "1.2.9",
                "provider": "1.4.9",
                "portfolio": "1.5.0",
                "sizing": "1.5.1",
                "correlation": "1.5.2",
                "drawdown": "1.5.3",
                "walk_forward": "1.5.4",
                "stable": "1.5.9",
            },
            stable_capabilities=[c.capability_id for c in cap_reg.get_stable()],
            planned_capabilities=[c.capability_id for c in cap_reg.get_planned()],
            disabled_capabilities=[c.capability_id for c in cap_reg.get_disabled()],
            schema_fingerprints=schema_reg.get_fingerprints(),
            enum_fingerprints=enum_reg.get_fingerprints(),
            cli_count=310,
            health_baselines={
                "portfolio": "32/32",
                "sizing": "56/56",
                "correlation": "122/122",
                "drawdown": "108/108",
                "walk_forward": "46/46",
            },
            release_gate_baselines={
                "portfolio": "PASS",
                "sizing": "PASS",
                "correlation": "PASS",
                "drawdown": "PASS",
                "walk_forward": "PASS",
                "stable": "PASS",
            },
            test_collection_baseline=5133,
            test_pass_baseline=5133,
            known_limitations=[
                "research-only",
                "historical-simulation-only",
                "no-broker",
                "no-real-orders",
                "no-live-trading",
                "no-auto-rebalance",
                "no-optimization",
                "past-performance-not-future-guarantee",
            ],
            research_only=True,
            no_real_orders=True,
            broker_disabled=True,
            production_trading_blocked=True,
        )
        manifest.content_hash = manifest.compute_semantic_hash()
        return manifest

    def validate(self, manifest: StableManifest) -> dict:
        issues = []
        if not manifest.version:
            issues.append("MISSING_VERSION")
        if not manifest.stable_capabilities:
            issues.append("NO_STABLE_CAPABILITIES")
        if not manifest.content_hash:
            issues.append("MISSING_CONTENT_HASH")
        if not manifest.research_only:
            issues.append("RESEARCH_ONLY_FALSE")
        if not manifest.no_real_orders:
            issues.append("NO_REAL_ORDERS_FALSE")
        if not manifest.production_trading_blocked:
            issues.append("PRODUCTION_TRADING_NOT_BLOCKED")
        expected = manifest.compute_semantic_hash()
        if manifest.content_hash != expected:
            issues.append("HASH_MISMATCH")
        return {"valid": len(issues) == 0, "issues": issues, "hash": manifest.content_hash}

    def to_json(self, manifest: StableManifest) -> str:
        data = {
            "version": manifest.version,
            "release": manifest.release,
            "baselines": manifest.baselines,
            "stable_capabilities": sorted(manifest.stable_capabilities),
            "planned_capabilities": sorted(manifest.planned_capabilities),
            "schema_fingerprints": dict(sorted(manifest.schema_fingerprints.items())),
            "enum_fingerprints": dict(sorted(manifest.enum_fingerprints.items())),
            "cli_count": manifest.cli_count,
            "health_baselines": manifest.health_baselines,
            "release_gate_baselines": manifest.release_gate_baselines,
            "test_collection_baseline": manifest.test_collection_baseline,
            "known_limitations": manifest.known_limitations,
            "safety": {
                "research_only": True,
                "no_real_orders": True,
                "broker_disabled": True,
                "production_trading_blocked": True,
            },
            "content_hash": manifest.content_hash,
        }
        return json.dumps(data, sort_keys=True, indent=2)

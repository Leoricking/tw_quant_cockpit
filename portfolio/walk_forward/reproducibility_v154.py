"""
portfolio/walk_forward/reproducibility_v154.py — Walk-forward Reproducibility Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
Hash mismatch → BLOCKED. Fixed seed for any random ops.
"""
from __future__ import annotations
import hashlib
import json
import sys
from typing import Any, Dict, List, Optional

from portfolio.walk_forward.models_v154 import ReproducibilityManifest

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
REPRODUCIBILITY_VERSION = "1.5.4"
FIXED_SEED = 42  # Fixed seed for any random operations


def _hash(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class WalkForwardReproducibilityEngine:
    """Build and verify reproducibility manifests for walk-forward runs."""

    def __init__(self):
        self.version = REPRODUCIBILITY_VERSION

    def build_manifest(
        self,
        run_id: str,
        config,
        windows: List[Any],
        results: List[Any],
    ) -> ReproducibilityManifest:
        """Build a reproducibility manifest for a walk-forward run."""
        config_data = {
            "config_id": getattr(config, "config_id", "unknown") if config else "unknown",
            "version": getattr(config, "version", "1.5.4") if config else "1.5.4",
            "training_length": getattr(config, "training_length", 0) if config else 0,
            "validation_length": getattr(config, "validation_length", 0) if config else 0,
        }
        config_hash = _hash(config_data)

        window_hashes = [_hash({"window_id": getattr(w, "window_id", str(i)),
                                 "sequence": getattr(w, "sequence", i)})
                          for i, w in enumerate(windows)]

        result_hashes = [_hash({"window_id": getattr(r, "window_id", str(i))})
                          for i, r in enumerate(results)]

        return ReproducibilityManifest(
            run_id=run_id,
            config_hash=config_hash,
            window_hashes=window_hashes,
            decision_hashes=[],
            dataset_hashes={"fixture_dataset": _hash({"source": "fixture", "version": "1.5.4"})},
            result_hashes=result_hashes,
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            dependencies={"portfolio_walk_forward": "1.5.4"},
            timezone="Asia/Taipei",
            calendar_version="1.5.4",
            seed=FIXED_SEED,
            code_commit="fixture_v154",
            fixture_hashes={"fixture": _hash({"fixture": "portfolio_walk_forward", "version": "1.5.4"})},
            metadata={"research_only": True, "fixture_mode": True},
        )

    def verify(
        self,
        manifest: ReproducibilityManifest,
        run_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify a run against its manifest.
        Hash mismatch → BLOCKED.
        """
        mismatches = []
        violations = []

        run_config_hash = run_result.get("config_hash")
        if run_config_hash and run_config_hash != manifest.config_hash:
            mismatches.append({
                "field": "config_hash",
                "manifest": manifest.config_hash,
                "run": run_config_hash,
            })

        run_window_hashes = run_result.get("window_hashes", [])
        if run_window_hashes and manifest.window_hashes:
            for i, (mh, rh) in enumerate(zip(manifest.window_hashes, run_window_hashes)):
                if mh != rh:
                    mismatches.append({"field": f"window_hash[{i}]", "manifest": mh, "run": rh})

        if mismatches:
            violations.append(f"Hash mismatches detected: {len(mismatches)} field(s)")

        is_reproducible = len(mismatches) == 0
        status = "VERIFIED" if is_reproducible else "BLOCKED"

        return {
            "is_reproducible": is_reproducible,
            "hash_mismatches": mismatches,
            "violations": violations,
            "status": status,
            "research_only": True,
        }

"""
release/multi_session_fixture_governance_release_gate_v1661.py
Fixture Governance Release Gate for Multi-session Coordination v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker.
[!] Gate validates fixture safety marker completeness and registry integrity.
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Tuple

VERSION_GATE = "1.6.6.1"
EXPECTED_FIXTURES = 80
EXPECTED_MARKERS = 10
RESEARCH_ONLY = True


def _check(condition: bool, passed_msg: str, failed_msg: str) -> Tuple[str, str]:
    return ("PASS", passed_msg) if condition else ("FAIL", failed_msg)


class FixtureGovernanceReleaseGateV1661:
    """
    Release gate verifying that all 80 multi-session fixtures have:
    - Complete 10 safety markers with True boolean values
    - Valid JSON with unique IDs
    - Registry registration and formal reference
    - No unused, duplicate, or malformed fixtures
    """

    def run(self) -> Dict[str, Any]:
        from paper_trading.multi_session.fixture_schema_v1661 import (
            REQUIRED_FIXTURE_MARKERS, fixture_safety_summary
        )
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        from release.version_info import VERSION, RELEASE_NAME, BASE_RELEASE

        checks: Dict[str, Tuple[str, str]] = {}

        # Version checks
        checks["version_check"] = _check(
            VERSION >= "1.6.6.1",
            f"VERSION={VERSION}",
            f"VERSION={VERSION}, expected>=1.6.6.1"
        )
        checks["release_name_check"] = _check(
            RELEASE_NAME in {
                "Fixture Governance & Safety Marker Hotfix",
                "Multi-session Coordination",
                "Replay Session Lineage Handler Integrity Hotfix",
                "Paper Performance Attribution",
                "Operational Integration Hardening",
                "Live Paper Trading Stable Rollup",
                "Stable Rollup Compatibility Hotfix",
            },
            f"RELEASE_NAME={RELEASE_NAME}",
            f"RELEASE_NAME={RELEASE_NAME} not in known names"
        )
        checks["base_release_check"] = _check(
            any(v in BASE_RELEASE for v in (
                "1.6.5", "1.6.6", "1.6.7", "1.6.8", "1.6.9",
            )),
            f"BASE_RELEASE={BASE_RELEASE}",
            f"BASE_RELEASE={BASE_RELEASE} does not reference a valid release chain"
        )

        # Load fixtures
        fixture_dir = "tests/fixtures/multi_session"
        fixtures_data = []
        load_errors = []
        ids_seen = []
        paths_seen = []

        if os.path.isdir(fixture_dir):
            files = sorted(f for f in os.listdir(fixture_dir) if f.endswith(".json"))
            for fname in files:
                path = os.path.join(fixture_dir, fname)
                try:
                    with open(path, encoding="utf-8") as fh:
                        data = json.load(fh)
                    fixtures_data.append(data)
                    ids_seen.append(data.get("test_id", fname))
                    paths_seen.append(path)
                except Exception as e:
                    load_errors.append(f"{fname}: {e}")

        total_files = len(fixtures_data) + len(load_errors)

        checks["fixture_count"] = _check(
            total_files == EXPECTED_FIXTURES,
            f"total={total_files}",
            f"total={total_files}, expected={EXPECTED_FIXTURES}"
        )
        checks["valid_json"] = _check(
            not load_errors,
            f"valid={len(fixtures_data)}",
            f"malformed={len(load_errors)}"
        )

        duplicate_ids = [x for x in set(ids_seen) if ids_seen.count(x) > 1]
        checks["unique_ids"] = _check(
            not duplicate_ids,
            f"unique_ids={len(set(ids_seen))}",
            f"duplicate_ids={duplicate_ids}"
        )

        duplicate_paths = [x for x in set(paths_seen) if paths_seen.count(x) > 1]
        checks["duplicate_paths"] = _check(
            not duplicate_paths,
            "no duplicate paths",
            f"duplicate_paths={duplicate_paths}"
        )

        # Marker completeness
        if fixtures_data:
            summary = fixture_safety_summary(fixtures_data)
            checks["all_fixtures_have_complete_markers"] = _check(
                summary["valid"] == EXPECTED_FIXTURES,
                f"all {EXPECTED_FIXTURES} fixtures have all {EXPECTED_MARKERS} markers",
                f"fixtures_with_complete_markers={summary['valid']}, "
                f"missing={summary['invalid']}"
            )
            checks["all_markers_are_true_booleans"] = _check(
                summary["valid"] == EXPECTED_FIXTURES,
                "all marker values are boolean True",
                f"invalid_values_by_marker={summary['invalid_values_by_marker']}"
            )
        else:
            checks["all_fixtures_have_complete_markers"] = ("FAIL", "no fixtures loaded")
            checks["all_markers_are_true_booleans"] = ("FAIL", "no fixtures loaded")

        # Registry checks
        usage = fixture_usage_summary()
        checks["all_fixtures_registered"] = _check(
            usage["registered"] == EXPECTED_FIXTURES,
            f"registered={usage['registered']}",
            f"registered={usage['registered']}, expected={EXPECTED_FIXTURES}"
        )
        checks["all_fixtures_referenced"] = _check(
            usage["referenced"] == EXPECTED_FIXTURES,
            f"referenced={usage['referenced']}",
            f"referenced={usage['referenced']}, unreferenced={usage['unreferenced']}"
        )
        checks["unused_fixtures_zero"] = _check(
            usage["unused"] == 0,
            "unused=0",
            f"unused={usage['unused']}"
        )
        checks["no_missing_purposes"] = _check(
            not usage["missing_purpose"],
            "all fixtures have declared purpose",
            f"missing_purpose={usage['missing_purpose']}"
        )

        passed = sum(1 for v in checks.values() if v[0] == "PASS")
        failed = len(checks) - passed

        return {
            "gate_id": "fixture_governance_v1661",
            "gate_version": VERSION_GATE,
            "gate_name": "Fixture Governance & Safety Marker Hotfix",
            "total": passed + failed,
            "passed": passed,
            "failed": failed,
            "all_pass": failed == 0,
            "gate_passed": failed == 0,
            "status": "PASS" if failed == 0 else "FAIL",
            "research_only": RESEARCH_ONLY,
            "no_real_orders": True,
            "checks": checks,
        }

"""
paper_trading/multi_session/health_v1661.py
Fixture Governance Health Check for Multi-session Coordination v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker. No Production Capability.
[!] Validates fixture safety markers, schema completeness, and registry integrity.
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Tuple

VERSION = "1.6.6.1"
FIXTURE_DIR = "tests/fixtures/multi_session"
EXPECTED_FIXTURE_COUNT = 80
EXPECTED_MARKER_COUNT = 10

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
NO_PRODUCTION_CAPABILITY = True


def _pass(detail: str = "") -> Tuple[str, str]:
    return ("PASS", detail)


def _fail(detail: str = "") -> Tuple[str, str]:
    return ("FAIL", detail)


class FixtureGovernanceHealthCheck:
    """
    Health check validating that all 80 multi-session coordination fixtures
    have complete safety markers, valid JSON, unique IDs, and are registered.
    """

    def run(self) -> Dict[str, Any]:
        checks: Dict[str, Tuple[str, str]] = {}

        # 1. Load all fixtures
        fixtures, load_errors = self._load_all_fixtures()
        total_files = len(fixtures) + len(load_errors)

        checks["fixture_count"] = (
            _pass(f"total={total_files}") if total_files == EXPECTED_FIXTURE_COUNT
            else _fail(f"expected={EXPECTED_FIXTURE_COUNT}, got={total_files}")
        )

        checks["valid_json"] = (
            _pass(f"valid={len(fixtures)}, errors={len(load_errors)}")
            if not load_errors
            else _fail(f"malformed={len(load_errors)}: {load_errors[:3]}")
        )

        if not fixtures:
            passed = sum(1 for v in checks.values() if v[0] == "PASS")
            failed = len(checks) - passed
            return self._build_result(checks, passed, failed)

        # 2. Unique test_ids
        ids = [fx["data"].get("test_id", "") for fx in fixtures]
        duplicate_ids = [x for x in set(ids) if ids.count(x) > 1]
        checks["unique_ids"] = (
            _pass(f"unique={len(set(ids))}") if not duplicate_ids
            else _fail(f"duplicates={duplicate_ids}")
        )

        # 3. Marker schema present and valid (all 10 markers)
        from paper_trading.multi_session.fixture_schema_v1661 import (
            REQUIRED_FIXTURE_MARKERS, validate_fixture_markers, fixture_safety_summary
        )
        summary = fixture_safety_summary([fx["data"] for fx in fixtures])

        checks["marker_schema_present"] = (
            _pass(f"fixtures_with_all_10_markers={summary['valid']}")
            if summary["valid"] == EXPECTED_FIXTURE_COUNT
            else _fail(f"fixtures_missing_markers={summary['invalid']}, "
                       f"missing_by_marker={summary['missing_by_marker']}")
        )

        checks["marker_values_valid"] = (
            _pass("all marker values are boolean True")
            if summary["valid"] == EXPECTED_FIXTURE_COUNT
            else _fail(f"invalid_values_by_marker={summary['invalid_values_by_marker']}")
        )

        # 4. Check each of the 10 markers individually
        for marker_key in REQUIRED_FIXTURE_MARKERS:
            missing_count = summary["missing_by_marker"].get(marker_key, 0)
            invalid_count = summary["invalid_values_by_marker"].get(marker_key, 0)
            checks[f"marker_{marker_key}"] = (
                _pass(f"present_and_true=80")
                if missing_count == 0 and invalid_count == 0
                else _fail(f"missing={missing_count}, invalid_values={invalid_count}")
            )

        # 5. Registry integrity
        from paper_trading.multi_session.fixture_registry_v1661 import (
            fixture_usage_summary, list_fixtures
        )
        usage = fixture_usage_summary()

        checks["registered_fixtures"] = (
            _pass(f"registered={usage['registered']}")
            if usage["registered"] == EXPECTED_FIXTURE_COUNT
            else _fail(f"registered={usage['registered']}, expected={EXPECTED_FIXTURE_COUNT}")
        )

        checks["referenced_fixtures"] = (
            _pass(f"referenced={usage['referenced']}")
            if usage["referenced"] == EXPECTED_FIXTURE_COUNT
            else _fail(f"referenced={usage['referenced']}, unreferenced={usage['unreferenced']}")
        )

        checks["unused_fixtures"] = (
            _pass("unused=0") if usage["unused"] == 0
            else _fail(f"unused={usage['unused']}")
        )

        checks["duplicate_paths"] = (
            _pass("no duplicate paths") if not usage["duplicate_paths"]
            else _fail(f"duplicate_paths={usage['duplicate_paths']}")
        )

        checks["missing_purposes"] = (
            _pass("all fixtures have purpose") if not usage["missing_purpose"]
            else _fail(f"missing_purpose={usage['missing_purpose']}")
        )

        checks["invalid_purposes"] = (
            _pass("all purposes valid") if not usage["invalid_purpose"]
            else _fail(f"invalid_purpose={usage['invalid_purpose']}")
        )

        checks["malformed_fixtures"] = (
            _pass("malformed=0") if not load_errors
            else _fail(f"malformed={len(load_errors)}")
        )

        # 6. Version check
        from release.version_info import VERSION as CURRENT_VERSION
        checks["version_1661"] = (
            _pass(f"VERSION={CURRENT_VERSION}")
            if CURRENT_VERSION >= "1.6.6.1"
            else _fail(f"VERSION={CURRENT_VERSION}, expected>=1.6.6.1")
        )

        passed = sum(1 for v in checks.values() if v[0] == "PASS")
        failed = len(checks) - passed
        return self._build_result(checks, passed, failed)

    def _load_all_fixtures(self) -> Tuple[List[Dict[str, Any]], List[str]]:
        fixtures = []
        errors = []
        if not os.path.isdir(FIXTURE_DIR):
            errors.append(f"fixture directory not found: {FIXTURE_DIR}")
            return fixtures, errors
        files = sorted([f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")])
        for fname in files:
            path = os.path.join(FIXTURE_DIR, fname)
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
                fixtures.append({"fname": fname, "path": path, "data": data})
            except Exception as e:
                errors.append(f"{fname}: {e}")
        return fixtures, errors

    def _build_result(self, checks: Dict[str, Any], passed: int, failed: int) -> Dict[str, Any]:
        return {
            "health_id": "fixture_governance_v1661",
            "version": VERSION,
            "total": passed + failed,
            "passed": passed,
            "failed": failed,
            "status": "PASS" if failed == 0 else "FAIL",
            "research_only": RESEARCH_ONLY,
            "paper_only": PAPER_ONLY,
            "no_real_orders": NO_REAL_ORDERS,
            "checks": checks,
        }

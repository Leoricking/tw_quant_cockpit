"""
governance_ops.governance_adapters — Module adapters for Data Governance Operations Dashboard v1.1.6

Adapters read from existing query/store/health modules without modifying data.
If a module is unavailable: returns available()=False, status=UNAVAILABLE, empty lists.
If store file missing: returns empty + logs warning (no crash).
If JSON/CSV corrupt: returns graceful warning, no crash.
No fallback to mock. No fake success data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Adapters READ ONLY. Do NOT modify data.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

from governance_ops.governance_schema import GovernanceModuleStatus

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Defensive imports
# ---------------------------------------------------------------------------

try:
    import universe as _universe_mod
    _universe_available = True
except ImportError:
    _universe_available = False

try:
    import data_onboarding as _onboarding_mod
    _onboarding_available = True
except ImportError:
    _onboarding_available = False

try:
    import coverage_repair as _repair_mod
    _repair_available = True
except ImportError:
    _repair_available = False

try:
    import data_freshness as _freshness_mod
    _freshness_available = True
except ImportError:
    _freshness_available = False

try:
    import quality_gates as _qg_mod
    _qg_available = True
except ImportError:
    _qg_available = False

try:
    import gate_enforcement as _ge_mod
    _ge_available = True
except ImportError:
    _ge_available = False

try:
    import report_pack as _rp_mod
    _rp_available = True
except ImportError:
    _rp_available = False


# ---------------------------------------------------------------------------
# Base adapter mixin
# ---------------------------------------------------------------------------

class _BaseGovernanceAdapter:
    """Base class for all governance adapters."""

    MODULE_NAME = "UNKNOWN"

    def available(self) -> bool:
        return False

    def health(self) -> GovernanceModuleStatus:
        return GovernanceModuleStatus(
            module_name=self.MODULE_NAME,
            available=False,
            health_status="UNAVAILABLE",
            reason="Module not available",
        )

    def latest_summary(self) -> dict:
        return {}

    def list_issues(self) -> list:
        return []

    def list_actions(self) -> list:
        return []

    def symbol_status(self, symbol: str) -> dict:
        return {"symbol": symbol, "status": "UNAVAILABLE"}

    def last_updated(self) -> Optional[str]:
        return None

    def limitations(self) -> list:
        return []


# ---------------------------------------------------------------------------
# Universe Governance Adapter
# ---------------------------------------------------------------------------

class UniverseGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads from universe module health and store."""

    MODULE_NAME = "UNIVERSE"

    def available(self) -> bool:
        return _universe_available

    def health(self) -> GovernanceModuleStatus:
        if not _universe_available:
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=False,
                health_status="UNAVAILABLE",
                reason="universe module not importable",
            )
        try:
            from universe.universe_health import UniverseHealthCheck
            checker = UniverseHealthCheck()
            results = checker.run()
            pass_c = sum(1 for _, s, _ in results if s == "PASS")
            warn_c = sum(1 for _, s, _ in results if s == "WARN")
            fail_c = sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
            overall = "PASS" if fail_c == 0 and warn_c == 0 else ("WARN" if fail_c == 0 else "FAIL")
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status=overall,
                pass_count=pass_c,
                warn_count=warn_c,
                fail_count=fail_c,
                version=getattr(_universe_mod, "__version__", ""),
            )
        except Exception as exc:
            logger.warning("UniverseGovernanceAdapter.health error: %s", exc)
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status="WARN",
                reason=str(exc),
            )

    def latest_summary(self) -> dict:
        if not _universe_available:
            return {}
        try:
            from universe.universe_query import UniverseQuery
            q = UniverseQuery()
            summary = q.summary()
            return summary if isinstance(summary, dict) else {}
        except Exception as exc:
            logger.warning("UniverseGovernanceAdapter.latest_summary error: %s", exc)
            return {}

    def list_issues(self) -> list:
        if not _universe_available:
            return []
        try:
            from universe.universe_query import UniverseQuery
            q = UniverseQuery()
            missing = q.missing_symbols()
            return [{"symbol": s, "issue": "MISSING_DATA"} for s in missing]
        except Exception as exc:
            logger.warning("UniverseGovernanceAdapter.list_issues error: %s", exc)
            return []

    def symbol_status(self, symbol: str) -> dict:
        if not _universe_available:
            return {"symbol": symbol, "status": "UNAVAILABLE"}
        try:
            from universe.universe_query import UniverseQuery
            q = UniverseQuery()
            result = q.symbol_detail(symbol)
            return result if isinstance(result, dict) else {"symbol": symbol}
        except Exception as exc:
            logger.warning("UniverseGovernanceAdapter.symbol_status error: %s", exc)
            return {"symbol": symbol, "error": str(exc)}

    def limitations(self) -> list:
        return ["Universe data requires real CSV data files to be populated"]


# ---------------------------------------------------------------------------
# Onboarding Governance Adapter
# ---------------------------------------------------------------------------

class OnboardingGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads from data_onboarding module."""

    MODULE_NAME = "ONBOARDING"

    def available(self) -> bool:
        return _onboarding_available

    def health(self) -> GovernanceModuleStatus:
        if not _onboarding_available:
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=False,
                health_status="UNAVAILABLE",
                reason="data_onboarding module not importable",
            )
        try:
            from data_onboarding.onboarding_health import ImportOnboardingHealthCheck
            checker = ImportOnboardingHealthCheck()
            results = checker.run()
            pass_c = sum(1 for _, s, _ in results if s == "PASS")
            warn_c = sum(1 for _, s, _ in results if s == "WARN")
            fail_c = sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
            overall = "PASS" if fail_c == 0 and warn_c == 0 else ("WARN" if fail_c == 0 else "FAIL")
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status=overall,
                pass_count=pass_c,
                warn_count=warn_c,
                fail_count=fail_c,
            )
        except Exception as exc:
            logger.warning("OnboardingGovernanceAdapter.health error: %s", exc)
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status="WARN",
                reason=str(exc),
            )

    def list_issues(self) -> list:
        if not _onboarding_available:
            return []
        try:
            from data_onboarding.onboarding_query import OnboardingQuery
            q = OnboardingQuery()
            issues = q.list_issues() if hasattr(q, "list_issues") else []
            return issues if isinstance(issues, list) else []
        except Exception as exc:
            logger.warning("OnboardingGovernanceAdapter.list_issues error: %s", exc)
            return []

    def limitations(self) -> list:
        return ["Onboarding requires real import files (CSV/XQ/Excel) to be present"]


# ---------------------------------------------------------------------------
# Repair Governance Adapter
# ---------------------------------------------------------------------------

class RepairGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads from coverage_repair module."""

    MODULE_NAME = "COVERAGE_REPAIR"

    def available(self) -> bool:
        return _repair_available

    def health(self) -> GovernanceModuleStatus:
        if not _repair_available:
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=False,
                health_status="UNAVAILABLE",
                reason="coverage_repair module not importable",
            )
        try:
            from coverage_repair.repair_health import CoverageRepairHealthCheck
            checker = CoverageRepairHealthCheck()
            results = checker.run()
            pass_c = sum(1 for _, s, _ in results if s == "PASS")
            warn_c = sum(1 for _, s, _ in results if s == "WARN")
            fail_c = sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
            overall = "PASS" if fail_c == 0 and warn_c == 0 else ("WARN" if fail_c == 0 else "FAIL")
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status=overall,
                pass_count=pass_c,
                warn_count=warn_c,
                fail_count=fail_c,
            )
        except Exception as exc:
            logger.warning("RepairGovernanceAdapter.health error: %s", exc)
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status="WARN",
                reason=str(exc),
            )

    def list_issues(self) -> list:
        if not _repair_available:
            return []
        try:
            from coverage_repair.repair_query import RepairQuery
            q = RepairQuery()
            issues = q.list_open_tasks() if hasattr(q, "list_open_tasks") else []
            return issues if isinstance(issues, list) else []
        except Exception as exc:
            logger.warning("RepairGovernanceAdapter.list_issues error: %s", exc)
            return []

    def limitations(self) -> list:
        return ["Coverage repair is dry-run only by default; destructive repair disabled"]


# ---------------------------------------------------------------------------
# Freshness Governance Adapter
# ---------------------------------------------------------------------------

class FreshnessGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads from data_freshness module."""

    MODULE_NAME = "FRESHNESS"

    def available(self) -> bool:
        return _freshness_available

    def health(self) -> GovernanceModuleStatus:
        if not _freshness_available:
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=False,
                health_status="UNAVAILABLE",
                reason="data_freshness module not importable",
            )
        try:
            from data_freshness.freshness_health import DataFreshnessHealthCheck
            checker = DataFreshnessHealthCheck()
            results = checker.run()
            pass_c = sum(1 for _, s, _ in results if s == "PASS")
            warn_c = sum(1 for _, s, _ in results if s == "WARN")
            fail_c = sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
            overall = "PASS" if fail_c == 0 and warn_c == 0 else ("WARN" if fail_c == 0 else "FAIL")
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status=overall,
                pass_count=pass_c,
                warn_count=warn_c,
                fail_count=fail_c,
            )
        except Exception as exc:
            logger.warning("FreshnessGovernanceAdapter.health error: %s", exc)
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status="WARN",
                reason=str(exc),
            )

    def latest_summary(self) -> dict:
        if not _freshness_available:
            return {}
        try:
            from data_freshness.freshness_query import FreshnessQuery
            q = FreshnessQuery()
            summary = q.summary() if hasattr(q, "summary") else {}
            return summary if isinstance(summary, dict) else {}
        except Exception as exc:
            logger.warning("FreshnessGovernanceAdapter.latest_summary error: %s", exc)
            return {}

    def list_issues(self) -> list:
        if not _freshness_available:
            return []
        try:
            from data_freshness.freshness_query import FreshnessQuery
            q = FreshnessQuery()
            stale = q.stale_symbols() if hasattr(q, "stale_symbols") else []
            return [{"symbol": s, "issue": "STALE"} for s in (stale or [])]
        except Exception as exc:
            logger.warning("FreshnessGovernanceAdapter.list_issues error: %s", exc)
            return []

    def limitations(self) -> list:
        return [
            "Calendar uses approximation (Mon-Fri). Public holidays are not excluded.",
            "Auto external refresh is DISABLED. Fresh data requires manual import.",
        ]


# ---------------------------------------------------------------------------
# Quality Gate Governance Adapter
# ---------------------------------------------------------------------------

class QualityGateGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads from quality_gates module."""

    MODULE_NAME = "QUALITY_GATES"

    def available(self) -> bool:
        return _qg_available

    def health(self) -> GovernanceModuleStatus:
        if not _qg_available:
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=False,
                health_status="UNAVAILABLE",
                reason="quality_gates module not importable",
            )
        try:
            from quality_gates.gate_health import CoverageQualityGateHealthCheck
            checker = CoverageQualityGateHealthCheck()
            results = checker.run()
            pass_c = sum(1 for _, s, _ in results if s == "PASS")
            warn_c = sum(1 for _, s, _ in results if s == "WARN")
            fail_c = sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
            overall = "PASS" if fail_c == 0 and warn_c == 0 else ("WARN" if fail_c == 0 else "FAIL")
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status=overall,
                pass_count=pass_c,
                warn_count=warn_c,
                fail_count=fail_c,
                version=getattr(_qg_mod, "__version__", ""),
            )
        except Exception as exc:
            logger.warning("QualityGateGovernanceAdapter.health error: %s", exc)
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status="WARN",
                reason=str(exc),
            )

    def latest_summary(self) -> dict:
        if not _qg_available:
            return {}
        try:
            from quality_gates.gate_query import GateQuery
            q = GateQuery()
            return q.summary() if hasattr(q, "summary") else {}
        except Exception as exc:
            logger.warning("QualityGateGovernanceAdapter.latest_summary error: %s", exc)
            return {}

    def limitations(self) -> list:
        return ["Quality gate does NOT enable trading. Gate override disabled by default."]


# ---------------------------------------------------------------------------
# Gate Enforcement Governance Adapter
# ---------------------------------------------------------------------------

class EnforcementGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads from gate_enforcement module."""

    MODULE_NAME = "GATE_ENFORCEMENT"

    def available(self) -> bool:
        return _ge_available

    def health(self) -> GovernanceModuleStatus:
        if not _ge_available:
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=False,
                health_status="UNAVAILABLE",
                reason="gate_enforcement module not importable",
            )
        try:
            from gate_enforcement.enforcement_health import QualityGateEnforcementHealthCheck
            checker = QualityGateEnforcementHealthCheck()
            results = checker.run()
            pass_c = sum(1 for _, s, _ in results if s == "PASS")
            warn_c = sum(1 for _, s, _ in results if s == "WARN")
            fail_c = sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
            overall = "PASS" if fail_c == 0 and warn_c == 0 else ("WARN" if fail_c == 0 else "FAIL")
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status=overall,
                pass_count=pass_c,
                warn_count=warn_c,
                fail_count=fail_c,
                version=getattr(_ge_mod, "__version__", ""),
            )
        except Exception as exc:
            logger.warning("EnforcementGovernanceAdapter.health error: %s", exc)
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status="WARN",
                reason=str(exc),
            )

    def latest_summary(self) -> dict:
        if not _ge_available:
            return {}
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            q = EnforcementQuery()
            return q.audit_summary()
        except Exception as exc:
            logger.warning("EnforcementGovernanceAdapter.latest_summary error: %s", exc)
            return {}

    def list_issues(self) -> list:
        if not _ge_available:
            return []
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            q = EnforcementQuery()
            non_qual = q.list_non_qualified_runs()
            return non_qual if isinstance(non_qual, list) else []
        except Exception as exc:
            logger.warning("EnforcementGovernanceAdapter.list_issues error: %s", exc)
            return []

    def limitations(self) -> list:
        return [
            "Gate enforcement is research-only. VALIDATED does not enable trading.",
            "Gate bypass is DISABLED. Override requires explicit research override.",
        ]


# ---------------------------------------------------------------------------
# Report Pack Governance Adapter
# ---------------------------------------------------------------------------

class ReportPackGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads from report_pack module."""

    MODULE_NAME = "REPORT_PACK"

    def available(self) -> bool:
        return _rp_available

    def health(self) -> GovernanceModuleStatus:
        if not _rp_available:
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=False,
                health_status="UNAVAILABLE",
                reason="report_pack module not importable",
            )
        try:
            from report_pack.report_pack_health import ReportPackHealthCheck
            checker = ReportPackHealthCheck()
            results = checker.run()
            pass_c = sum(1 for _, s, _ in results if s == "PASS")
            warn_c = sum(1 for _, s, _ in results if s == "WARN")
            fail_c = sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
            overall = "PASS" if fail_c == 0 and warn_c == 0 else ("WARN" if fail_c == 0 else "FAIL")
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status=overall,
                pass_count=pass_c,
                warn_count=warn_c,
                fail_count=fail_c,
            )
        except Exception as exc:
            logger.warning("ReportPackGovernanceAdapter.health error: %s", exc)
            return GovernanceModuleStatus(
                module_name=self.MODULE_NAME,
                available=True,
                health_status="WARN",
                reason=str(exc),
            )

    def limitations(self) -> list:
        return ["Report pack depends on all upstream reports being generated first"]


# ---------------------------------------------------------------------------
# System Health Governance Adapter (KB + Local Assistant)
# ---------------------------------------------------------------------------

class SystemHealthGovernanceAdapter(_BaseGovernanceAdapter):
    """Reads system-level health (KB, local assistant, release gate)."""

    MODULE_NAME = "SYSTEM_HEALTH"

    def available(self) -> bool:
        return True

    def health(self) -> GovernanceModuleStatus:
        checks_pass = 0
        checks_warn = 0
        checks_fail = 0

        # Check knowledge base
        try:
            from knowledge_base.kb_health import KBHealthCheck
            checker = KBHealthCheck()
            results = checker.run()
            checks_pass += sum(1 for _, s, _ in results if s == "PASS")
            checks_warn += sum(1 for _, s, _ in results if s == "WARN")
            checks_fail += sum(1 for _, s, _ in results if s in ("FAIL", "BLOCKED"))
        except Exception:
            checks_warn += 1

        overall = "PASS" if checks_fail == 0 and checks_warn == 0 else ("WARN" if checks_fail == 0 else "FAIL")
        return GovernanceModuleStatus(
            module_name=self.MODULE_NAME,
            available=True,
            health_status=overall,
            pass_count=checks_pass,
            warn_count=checks_warn,
            fail_count=checks_fail,
        )

    def limitations(self) -> list:
        return ["Knowledge base search requires docs/reports to be indexed first"]

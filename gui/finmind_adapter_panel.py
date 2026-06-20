"""
gui/finmind_adapter_panel.py — FinMind Adapter Panel for v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SECONDARY_AGGREGATOR. Cannot override TWSE/TPEx/MOPS.
[!] No Token Display. No Fetch All Button. No Override Primary. No Trading Controls.
[!] Quota exhausted / invalid token — do not crash.
[!] No Auto-Discovery. No Auto-Download. No Silent Fallback. No Mock Fallback.
"""
TAB_ID = "finmind_adapter"
DISPLAY_NAME = "FinMind Adapter"
GROUP = "data"
PRIORITY = "P1"

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FINMIND_REALTIME_FORMAL_USE_ALLOWED = False
FINMIND_MOCK_FALLBACK_ENABLED = False
FINMIND_AUTO_DOWNLOAD_ENABLED = False
FINMIND_AUTO_DISCOVERY_ENABLED = False
FINMIND_DATASET_ALLOWLIST_REQUIRED = True
FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False
FINMIND_BROKER_EXECUTION_AVAILABLE = False
FINMIND_SILENT_FALLBACK_ENABLED = False
FINMIND_TOKEN_OPTIONAL = True

SAFETY_BANNER_LINES = [
    "[!] SECONDARY_AGGREGATOR — not a primary source.",
    "[!] Cannot override TWSE/TPEx/MOPS primary sources.",
    "[!] Formal conclusion requires primary source validation.",
    "[!] No token display. Token stored in env var only.",
    "[!] Quota exhausted → no retry, no token rotation, no mock fallback.",
    "[!] No Auto-Discovery. No Auto-Download. No Silent Fallback.",
    "[!] Research Only. No Real Orders. Not Investment Advice.",
]


def _try_import_qt():
    try:
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea
        from PyQt5.QtCore import QThread, pyqtSignal
        from PyQt5.QtGui import QFont
        return True, None
    except ImportError as e:
        return False, str(e)


_QT_AVAILABLE, _QT_ERROR = _try_import_qt()


def get_panel_data() -> dict:
    """Collect all data for the panel. Graceful on errors."""
    # Health
    try:
        from data.providers.finmind.health_v144 import FinMindAdapterHealthCheck
        health = FinMindAdapterHealthCheck().get_health_summary()
    except Exception as exc:
        health = {"error": str(exc), "provider_status": "ERROR"}

    # Allowlist
    try:
        from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
        al = FinMindDatasetAllowlist()
        allowlist_summary = al.summary()
        datasets = al.get_all()
    except Exception as exc:
        allowlist_summary = {"error": str(exc)}
        datasets = []

    # Auth (no token)
    try:
        from data.providers.finmind.auth_v144 import FinMindAuthManager
        auth_summary = FinMindAuthManager().get_auth_summary()
    except Exception as exc:
        auth_summary = {"error": str(exc)}

    # Quota
    try:
        from data.providers.finmind.quota_v144 import FinMindQuotaManager
        quota_state = FinMindQuotaManager().get_status()
        quota_summary = {
            "status": quota_state.status.value,
            "quota_limit": quota_state.quota_limit,
            "quota_used": quota_state.quota_used,
            "quota_remaining": quota_state.quota_remaining,
            "plan_unknown": quota_state.plan_unknown,
        }
    except Exception as exc:
        quota_summary = {"error": str(exc)}

    # Capabilities
    try:
        from data.providers.finmind.capabilities_v144 import get_capabilities
        capabilities = get_capabilities()
    except Exception as exc:
        capabilities = [{"error": str(exc)}]

    return {
        "provider": "finmind",
        "display_name": DISPLAY_NAME,
        "authoritative_level": "SECONDARY_AGGREGATOR",
        "official": False,
        "no_real_orders": NO_REAL_ORDERS,
        "broker_execution_enabled": BROKER_EXECUTION_ENABLED,
        "production_trading_blocked": PRODUCTION_TRADING_BLOCKED,
        "realtime_formal_use_allowed": FINMIND_REALTIME_FORMAL_USE_ALLOWED,
        "mock_fallback_enabled": FINMIND_MOCK_FALLBACK_ENABLED,
        "auto_download_enabled": FINMIND_AUTO_DOWNLOAD_ENABLED,
        "auto_discovery_enabled": FINMIND_AUTO_DISCOVERY_ENABLED,
        "allowlist_required": FINMIND_DATASET_ALLOWLIST_REQUIRED,
        "can_override_primary_provider": FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER,
        "silent_fallback_enabled": FINMIND_SILENT_FALLBACK_ENABLED,
        "token_optional": FINMIND_TOKEN_OPTIONAL,
        "safety_banner": SAFETY_BANNER_LINES,
        "health": health,
        "allowlist_summary": allowlist_summary,
        "datasets": datasets,
        "auth_summary": auth_summary,
        "quota_summary": quota_summary,
        "capabilities": capabilities,
    }


def get_section_adapter_status() -> dict:
    data = get_panel_data()
    return {
        "section": "Adapter Status",
        "provider": data["provider"],
        "authoritative_level": data["authoritative_level"],
        "health_status": data.get("health", {}).get("provider_status", "UNKNOWN"),
        "passed": data.get("health", {}).get("passed", 0),
        "failed": data.get("health", {}).get("failed", 0),
        "safety_banner": data["safety_banner"],
    }


def get_section_dataset_registry() -> dict:
    data = get_panel_data()
    return {
        "section": "Dataset Registry",
        "allowlist_summary": data["allowlist_summary"],
        "datasets": data["datasets"],
    }


def get_section_request_planner() -> dict:
    return {
        "section": "Request Planner",
        "note": "Dry-run only. No auto-download. Use finmind-plan CLI for details.",
        "auto_download_enabled": FINMIND_AUTO_DOWNLOAD_ENABLED,
        "auto_discovery_enabled": FINMIND_AUTO_DISCOVERY_ENABLED,
    }


def get_section_schema_drift() -> dict:
    return {
        "section": "Schema Drift",
        "note": "Schema drift detection available. Breaking changes block ingest.",
        "schema_drift_detection_available": True,
    }


def get_section_conflict_comparison() -> dict:
    return {
        "section": "Conflict Comparison",
        "note": "Primary source always wins. FinMind preserved as secondary evidence. No auto-repair.",
        "can_override_primary": FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER,
    }


def get_section_lineage() -> dict:
    try:
        from data.providers.finmind.provider_v144 import FinMindAdapterV144
        lineage = FinMindAdapterV144().get_provider_lineage()
    except Exception as exc:
        lineage = {"error": str(exc)}
    return {
        "section": "Lineage",
        "lineage": lineage,
    }

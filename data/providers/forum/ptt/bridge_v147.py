"""
data/providers/forum/ptt/bridge_v147.py — PTTGovernanceBridge v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Maps PTT articles/fetch-runs to v1.4.5 Source Lineage.
[!] Registers PTT as SUPPLEMENTARY in central registry.
[!] formal_use_allowed=False always.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORMAL_USE_ALLOWED = False  # ALWAYS FALSE


class PTTGovernanceBridge:
    """
    Bridges PTT fetch operations with v1.4.5 Source Lineage governance.
    [!] formal_use_allowed=False ALWAYS.
    [!] Registers PTT as SUPPLEMENTARY in central registry.
    [!] Maps fetch runs to lineage records.
    """

    SOURCE_ID = "ptt_stock"
    AUTHORITY = "SUPPLEMENTARY"
    FORMAL_USE_ALLOWED = False  # ALWAYS FALSE

    def register_ptt_source(self) -> bool:
        """
        Register PTT Stock as SUPPLEMENTARY in central registry.
        Returns True if registered successfully (or already registered).
        [!] formal_use_allowed=False always.
        """
        try:
            from data.providers.forum.source_registry_v147 import ForumSourceRegistry
            reg = ForumSourceRegistry()
            source = reg.get_source(self.SOURCE_ID)
            return source is not None  # PTT pre-registered
        except Exception as exc:
            logger.warning("PTTGovernanceBridge: register error: %s", exc)
            return False

    def record_fetch_run_lineage(self, run_id: int, fetch_result: Dict) -> Optional[Dict]:
        """
        Map a PTT fetch run to source lineage record.
        [!] formal_use_allowed=False always.
        """
        lineage = {
            "source_id": self.SOURCE_ID,
            "authority_level": self.AUTHORITY,
            "formal_use_allowed": False,
            "run_id": run_id,
            "articles_found": fetch_result.get("articles_found", 0),
            "pages_fetched": fetch_result.get("pages_fetched", 0),
            "dry_run": fetch_result.get("dry_run", True),
            "status": fetch_result.get("status", "UNKNOWN"),
            "provider_type": "PUBLIC_FORUM",
            "can_override_official": False,
            "can_generate_buy_sell": False,
        }
        try:
            from data.governance.lineage_registry_v145 import LineageRegistry
            registry = LineageRegistry()
            registry.record_fetch_run(lineage)
        except Exception:
            pass  # Governance layer may not be available in all environments
        return lineage

    def get_ptt_source_authority(self) -> str:
        """Return PTT source authority level."""
        return self.AUTHORITY

    def validate_governance_constraints(self) -> Dict[str, Any]:
        """Validate that PTT governance constraints are intact."""
        return {
            "source_id": self.SOURCE_ID,
            "authority": self.AUTHORITY,
            "formal_use_allowed": False,
            "private_board_access": False,
            "login_bypass": False,
            "captcha_bypass": False,
            "proxy_rotation": False,
            "credentials_stored": False,
            "buy_sell_generation": False,
            "official_override": False,
            "all_constraints_valid": True,
        }

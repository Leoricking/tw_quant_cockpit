"""
replay/registry_events.py — ReplayRegistryEvents v1.2.8

Records registry lifecycle events.
Events are append-only and include research_only and no_real_orders flags.

Events:
  DATASET_REGISTERED, DATASET_VERSION_CREATED, DATASET_FROZEN,
  DATASET_ARCHIVED, DATASET_RESTORED, DATASET_VALIDATED, DATASET_CORRUPTED,
  DATASET_PACKAGE_EXPORTED, DATASET_PACKAGE_IMPORTED,
  SESSION_REGISTERED, SESSION_DATASET_BOUND, SESSION_REBOUND,
  SESSION_ORPHANED, SESSION_REFERENCE_BROKEN,
  REGISTRY_REPAIR_PREVIEWED, REGISTRY_REPAIR_EXECUTED

Also maps to Research Registry events:
  REPLAY_DATASET_REGISTERED, REPLAY_SESSION_REGISTERED, etc.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from replay.registry_audit import ReplayRegistryAudit

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Event type constants
DATASET_REGISTERED           = "DATASET_REGISTERED"
DATASET_VERSION_CREATED      = "DATASET_VERSION_CREATED"
DATASET_FROZEN               = "DATASET_FROZEN"
DATASET_ARCHIVED             = "DATASET_ARCHIVED"
DATASET_RESTORED             = "DATASET_RESTORED"
DATASET_VALIDATED            = "DATASET_VALIDATED"
DATASET_CORRUPTED            = "DATASET_CORRUPTED"
DATASET_PACKAGE_EXPORTED     = "DATASET_PACKAGE_EXPORTED"
DATASET_PACKAGE_IMPORTED     = "DATASET_PACKAGE_IMPORTED"
SESSION_REGISTERED           = "SESSION_REGISTERED"
SESSION_DATASET_BOUND        = "SESSION_DATASET_BOUND"
SESSION_REBOUND              = "SESSION_REBOUND"
SESSION_ORPHANED             = "SESSION_ORPHANED"
SESSION_REFERENCE_BROKEN     = "SESSION_REFERENCE_BROKEN"
REGISTRY_REPAIR_PREVIEWED    = "REGISTRY_REPAIR_PREVIEWED"
REGISTRY_REPAIR_EXECUTED     = "REGISTRY_REPAIR_EXECUTED"

# Research Registry integration event types
REPLAY_DATASET_REGISTERED       = "REPLAY_DATASET_REGISTERED"
REPLAY_DATASET_VERSION_CREATED  = "REPLAY_DATASET_VERSION_CREATED"
REPLAY_DATASET_FROZEN           = "REPLAY_DATASET_FROZEN"
REPLAY_DATASET_VALIDATED        = "REPLAY_DATASET_VALIDATED"
REPLAY_DATASET_PACKAGE_EXPORTED = "REPLAY_DATASET_PACKAGE_EXPORTED"
REPLAY_DATASET_PACKAGE_IMPORTED = "REPLAY_DATASET_PACKAGE_IMPORTED"
REPLAY_SESSION_REGISTERED       = "REPLAY_SESSION_REGISTERED"
REPLAY_SESSION_DATASET_BOUND    = "REPLAY_SESSION_DATASET_BOUND"
REPLAY_SESSION_ORPHANED         = "REPLAY_SESSION_ORPHANED"
REPLAY_REGISTRY_REPAIR_PREVIEWED = "REPLAY_REGISTRY_REPAIR_PREVIEWED"
REPLAY_REGISTRY_REPAIR_EXECUTED  = "REPLAY_REGISTRY_REPAIR_EXECUTED"


class ReplayRegistryEvents:
    """
    Records registry lifecycle events.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: str = "."):
        self._audit = ReplayRegistryAudit(repo_root)

    def emit(
        self,
        event_type: str,
        dataset_id: Optional[str] = None,
        dataset_version: Optional[str] = None,
        session_id: Optional[str] = None,
        fingerprint: Optional[str] = None,
        package_id: Optional[str] = None,
        status: str = "OK",
        warnings: Optional[List[str]] = None,
        elapsed_seconds: float = 0.0,
    ) -> Dict[str, Any]:
        """Emit a registry event."""
        return self._audit.record(
            event_type=event_type,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            session_id=session_id,
            fingerprint=fingerprint,
            package_id=package_id,
            status=status,
            warnings=warnings,
            elapsed_seconds=elapsed_seconds,
        )

    def list_events(self, **kwargs) -> List[Dict[str, Any]]:
        return self._audit.list_events(**kwargs)

    def summary(self) -> str:
        return self._audit.summary()

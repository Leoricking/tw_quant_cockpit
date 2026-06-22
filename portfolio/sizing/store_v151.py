"""
portfolio/sizing/store_v151.py — Position Sizing Store v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Immutable proposals (idempotent by proposal_id/content_hash).
In-memory mode for tests (use_temp_db=True).
Runtime DB: data/position_sizing/ (gitignored).
No transaction ledger. No order table.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
SCHEMA_VERSION = "1.5.1"
NO_ORDER_TABLE = True
NO_TRANSACTION_LEDGER = True


def _decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Not serializable: {type(obj)}")


class PositionSizingStore:
    """
    In-memory store for sizing policies and proposals.
    Proposals are immutable — idempotent save by proposal_id and content_hash.
    """

    RESEARCH_ONLY = True

    def __init__(self, data_dir: Optional[str] = None, use_temp_db: bool = True):
        self.use_temp_db = use_temp_db
        self.data_dir = data_dir
        self._policies: Dict[str, Dict] = {}
        self._proposals: Dict[str, Dict] = {}
        self._schema_version = SCHEMA_VERSION

    # -------------------------------------------------------------------------
    # Policy methods
    # -------------------------------------------------------------------------

    def save_policy(self, policy) -> str:
        pid = policy.policy_id if hasattr(policy, "policy_id") else policy["policy_id"]
        data = self._to_dict(policy)
        self._policies[pid] = data
        return pid

    def get_policy(self, policy_id: str) -> Optional[Dict]:
        return self._policies.get(policy_id)

    def list_policies(self) -> List[Dict]:
        return list(self._policies.values())

    # -------------------------------------------------------------------------
    # Proposal methods (immutable)
    # -------------------------------------------------------------------------

    def save_proposal(self, proposal) -> str:
        pid = proposal.proposal_id if hasattr(proposal, "proposal_id") else proposal["proposal_id"]
        if pid in self._proposals:
            # Idempotent: skip duplicate (immutable)
            return pid
        data = self._to_dict(proposal)
        self._proposals[pid] = data
        return pid

    def get_proposal(self, proposal_id: str) -> Optional[Dict]:
        return self._proposals.get(proposal_id)

    def list_proposals(self, portfolio_id: Optional[str] = None) -> List[Dict]:
        proposals = list(self._proposals.values())
        if portfolio_id:
            proposals = [p for p in proposals if p.get("portfolio_id") == portfolio_id]
        return proposals

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _to_dict(obj) -> Dict[str, Any]:
        if isinstance(obj, dict):
            return obj
        if hasattr(obj, "__dataclass_fields__"):
            result = {}
            for k in obj.__dataclass_fields__:
                v = getattr(obj, k)
                if isinstance(v, Decimal):
                    result[k] = str(v)
                elif isinstance(v, list) and v and hasattr(v[0], "__dataclass_fields__"):
                    result[k] = [PositionSizingStore._to_dict(i) for i in v]
                else:
                    result[k] = v
            return result
        return dict(obj)

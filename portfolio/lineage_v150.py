"""
portfolio/lineage_v150.py — Lineage chain tracking for v1.5.0.

Chain: snapshot → valuation → price → provider → source
Each step records the originating ID and authority tier.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True


class PortfolioLineageTracker:
    RESEARCH_ONLY = True

    def build_chain(
        self,
        snapshot_id: str,
        valuation_id: Optional[str],
        price_source: Optional[str],
        provider_id: Optional[str],
        source_id: Optional[str],
        authority_tier: Optional[str] = None,
        extra: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Build a lineage chain dict linking snapshot → valuation → price → provider → source.
        """
        return {
            "snapshot_id": snapshot_id,
            "valuation_id": valuation_id,
            "price_source": price_source,
            "provider_id": provider_id,
            "source_id": source_id,
            "authority_tier": authority_tier,
            "chain_built_at": datetime.now(timezone.utc).isoformat(),
            "extra": extra or {},
            "research_only": True,
        }

    def verify_chain(self, chain: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify the lineage chain is structurally complete.
        Returns {valid, missing_links, research_only}.
        """
        required = ["snapshot_id", "valuation_id", "price_source", "provider_id", "source_id"]
        missing = [f for f in required if not chain.get(f)]
        return {
            "valid": len(missing) == 0,
            "missing_links": missing,
            "research_only": True,
        }

    def get_lineage_summary(self, chains: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Summarize a list of lineage chains.
        """
        total = len(chains)
        complete = sum(1 for c in chains if self.verify_chain(c)["valid"])
        providers = list({c.get("provider_id") for c in chains if c.get("provider_id")})
        authority_tiers = list({c.get("authority_tier") for c in chains if c.get("authority_tier")})
        return {
            "total_chains": total,
            "complete_chains": complete,
            "incomplete_chains": total - complete,
            "providers": providers,
            "authority_tiers": authority_tiers,
            "research_only": True,
        }

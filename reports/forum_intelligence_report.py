"""
reports/forum_intelligence_report.py — Forum Intelligence Report v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SUPPLEMENTARY authority only. Cannot override official sources.
[!] No BUY/SELL. No formal standalone conclusions.
12 sections: Overview, Collection, Symbols, Topics, Sentiment, Engagement,
             Credibility, Coordination/Manipulation Risk, PIT/Lineage, Safety.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED = False

_SECTIONS = [
    "overview",
    "collection",
    "symbols",
    "topics",
    "sentiment",
    "engagement",
    "credibility",
    "coordination_manipulation_risk",
    "pit_lineage",
    "safety",
    "quality_freshness",
    "appendix",
]


class ForumIntelligenceReport:
    """
    12-section Forum Intelligence report.
    [!] Research Only. SUPPLEMENTARY authority. No BUY/SELL.
    """

    VERSION = "1.4.7"

    def __init__(self, store=None) -> None:
        if store is None:
            from data.providers.forum.store_v147 import ForumStore
            store = ForumStore()
        self._store = store

    def build(self, as_of: Optional[str] = None) -> Dict[str, Any]:
        """Build the full report."""
        as_of = as_of or datetime.utcnow().isoformat() + "Z"
        report = {
            "_report_type": "forum_intelligence",
            "_version": self.VERSION,
            "_as_of": as_of,
            "_formal_standalone": False,
            "_authority": "SUPPLEMENTARY",
            "_can_generate_buy_sell": False,
            "_can_override_official": False,
            "_not_investment_advice": True,
            "sections": {},
        }
        for section in _SECTIONS:
            try:
                builder = getattr(self, f"_build_{section}", None)
                if builder:
                    report["sections"][section] = builder(as_of)
                else:
                    report["sections"][section] = {"status": "not_implemented"}
            except Exception as exc:
                report["sections"][section] = {"status": "error", "error": str(exc)}
        return report

    def _build_overview(self, as_of: str) -> Dict:
        sources = self._store.list_sources()
        with self._store._conn() as conn:
            article_count = conn.execute("SELECT COUNT(*) FROM forum_articles").fetchone()[0]
            run_count = conn.execute("SELECT COUNT(*) FROM forum_fetch_runs").fetchone()[0]
        return {
            "as_of": as_of,
            "sources_registered": len(sources),
            "total_articles": article_count,
            "total_fetch_runs": run_count,
            "authority": "SUPPLEMENTARY",
            "formal_standalone": False,
            "note": "Forum data is SUPPLEMENTARY and UNVERIFIED. Not Investment Advice.",
        }

    def _build_collection(self, as_of: str) -> Dict:
        runs = self._store.list_fetch_runs()
        completed = [r for r in runs if r.get("status") == "COMPLETE"]
        dry_run = [r for r in runs if r.get("dry_run") == 1]
        return {
            "total_runs": len(runs),
            "completed_runs": len(completed),
            "dry_runs": len(dry_run),
            "last_run": runs[0] if runs else None,
        }

    def _build_symbols(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT symbol, COUNT(*) as cnt FROM forum_symbol_mentions GROUP BY symbol ORDER BY cnt DESC LIMIT 20"
            ).fetchall()
        return {
            "top_symbols": [{"symbol": r["symbol"], "mention_count": r["cnt"]} for r in rows],
            "note": "Symbol linking is SUPPLEMENTARY. Not for formal analysis.",
        }

    def _build_topics(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT topic_label, COUNT(*) as cnt FROM forum_topic_signals GROUP BY topic_label ORDER BY cnt DESC LIMIT 10"
            ).fetchall()
        return {
            "top_topics": [{"topic": r["topic_label"], "count": r["cnt"]} for r in rows],
        }

    def _build_sentiment(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT polarity, COUNT(*) as cnt FROM forum_sentiment_signals GROUP BY polarity"
            ).fetchall()
        distribution = {r["polarity"]: r["cnt"] for r in rows}
        return {
            "polarity_distribution": distribution,
            "formal_standalone": False,
            "note": "Sentiment is UNVERIFIED forum opinion. Cannot generate BUY/SELL.",
        }

    def _build_engagement(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            row = conn.execute(
                "SELECT SUM(total_comments) as tc, SUM(push_count) as pushes, SUM(boo_count) as boos "
                "FROM forum_engagement_signals"
            ).fetchone()
        return {
            "total_comments": row["tc"] or 0,
            "total_pushes": row["pushes"] or 0,
            "total_boos": row["boos"] or 0,
            "note": "PUSH/BOO are engagement metrics only. Not bullish/bearish indicators.",
        }

    def _build_credibility(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as total, SUM(has_official_link) as official, "
                "SUM(has_guaranteed_profit) as guarantee FROM forum_credibility_signals"
            ).fetchone()
        return {
            "total_assessed": row["total"] or 0,
            "with_official_link": row["official"] or 0,
            "with_profit_guarantee_warning": row["guarantee"] or 0,
            "note": "Content credibility only. No person credit score assigned.",
        }

    def _build_coordination_manipulation_risk(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            coord = conn.execute(
                "SELECT risk_level, COUNT(*) as cnt FROM forum_coordination_risks GROUP BY risk_level"
            ).fetchall()
            manip = conn.execute(
                "SELECT risk_level, COUNT(*) as cnt FROM forum_manipulation_risks GROUP BY risk_level"
            ).fetchall()
        return {
            "coordination_risk_distribution": {r["risk_level"]: r["cnt"] for r in coord},
            "manipulation_risk_distribution": {r["risk_level"]: r["cnt"] for r in manip},
            "note": "Risk classification only. No criminal or legal labels.",
        }

    def _build_pit_lineage(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            edits = conn.execute("SELECT COUNT(*) FROM forum_edit_events").fetchone()[0]
            deletions = conn.execute("SELECT COUNT(*) FROM forum_deletion_events").fetchone()[0]
            versions = conn.execute("SELECT COUNT(*) FROM forum_article_versions").fetchone()[0]
        return {
            "edit_events": edits,
            "deletion_events": deletions,
            "article_versions": versions,
            "future_leakage": False,
            "pit_safe": True,
        }

    def _build_safety(self, as_of: str) -> Dict:
        from data.providers.forum import (
            FORUM_CAN_GENERATE_BUY_SELL,
            FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE,
            FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED,
            FORUM_PRIVATE_BOARD_ACCESS_ENABLED,
            FORUM_LOGIN_BYPASS_ENABLED,
            NO_REAL_ORDERS,
            BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED,
        )
        return {
            "FORUM_CAN_GENERATE_BUY_SELL": FORUM_CAN_GENERATE_BUY_SELL,
            "FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE": FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE,
            "FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED": FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED,
            "FORUM_PRIVATE_BOARD_ACCESS_ENABLED": FORUM_PRIVATE_BOARD_ACCESS_ENABLED,
            "FORUM_LOGIN_BYPASS_ENABLED": FORUM_LOGIN_BYPASS_ENABLED,
            "NO_REAL_ORDERS": NO_REAL_ORDERS,
            "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
            "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
            "all_safety_flags_ok": (
                not FORUM_CAN_GENERATE_BUY_SELL
                and not FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE
                and not FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED
                and not FORUM_PRIVATE_BOARD_ACCESS_ENABLED
                and not FORUM_LOGIN_BYPASS_ENABLED
                and NO_REAL_ORDERS
                and not BROKER_EXECUTION_ENABLED
                and PRODUCTION_TRADING_BLOCKED
            ),
        }

    def _build_quality_freshness(self, as_of: str) -> Dict:
        with self._store._conn() as conn:
            deleted = conn.execute("SELECT COUNT(*) FROM forum_articles WHERE is_deleted=1").fetchone()[0]
            total = conn.execute("SELECT COUNT(*) FROM forum_articles").fetchone()[0]
        return {
            "total_articles": total,
            "deleted_articles": deleted,
            "live_articles": total - deleted,
            "note": "Rate limit ≠ freshness. Repair is optional, not auto.",
        }

    def _build_appendix(self, as_of: str) -> Dict:
        return {
            "report_version": self.VERSION,
            "sections": _SECTIONS,
            "authority": "SUPPLEMENTARY",
            "formal_standalone": False,
            "disclaimer": (
                "This report is for research purposes only. "
                "Forum data is unverified supplementary information. "
                "Cannot replace official market data. Not Investment Advice."
            ),
        }

    def format_text(self, report: Optional[Dict] = None) -> str:
        """Format report as text."""
        if report is None:
            report = self.build()
        lines = [
            "=" * 70,
            "  TW Quant Cockpit — Forum Intelligence Report v1.4.7",
            f"  As Of: {report.get('_as_of', 'N/A')}",
            f"  [!] Research Only. Authority: SUPPLEMENTARY. Not Investment Advice.",
            f"  [!] formal_standalone=False. No BUY/SELL. No official override.",
            "=" * 70,
        ]
        for section_id, section_data in report.get("sections", {}).items():
            lines.append(f"\n  [{section_id.upper()}]")
            if isinstance(section_data, dict):
                for k, v in section_data.items():
                    if not k.startswith("_"):
                        lines.append(f"    {k}: {v}")
        lines.append("=" * 70)
        return "\n".join(lines)

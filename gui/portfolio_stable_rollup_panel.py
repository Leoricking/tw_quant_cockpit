"""Portfolio Stable Rollup Panel v1.5.9 — Research Only. Freeze/Stabilization."""
RESEARCH_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
NO_FORMAL_LEDGER_WRITE = True
NO_LIVE_REBALANCE = True
NO_AUTO_APPLY = True
PRODUCTION_TRADING_BLOCKED = True
FREEZE_ONLY = True

TAB_CONFIG = {
    "tab_id": "portfolio_stable_rollup",
    "display_name": "Portfolio Stable Rollup",
    "group": "portfolio",
    "priority": "P1",
}

SAFETY_BANNER_LINES = [
    "Research Only",
    "Freeze / Stabilization Release",
    "No Real Orders",
    "No Broker",
    "No Formal Ledger Write",
    "No Live Rebalance",
    "No Auto Apply",
    "Production Trading BLOCKED",
]

FORBIDDEN_ACTIONS = [
    "Execute", "Submit", "Buy", "Sell", "Connect Broker",
    "Apply to Live Portfolio", "Auto Rebalance", "Auto Stop",
    "Optimize Live Weights", "Broker Sync",
]


class PortfolioStableRollupPanel:
    """Portfolio Stable Rollup research panel. Headless safe — no QApplication import at module level."""

    def __init__(self):
        self.research_only = True
        self.freeze_only = True
        self._worker = None

    def get_metadata(self):
        return {
            "tab_id": TAB_CONFIG["tab_id"],
            "research_only": True,
            "freeze_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "no_formal_ledger_write": True,
            "no_live_rebalance": True,
            "no_auto_apply": True,
            "production_trading_blocked": True,
        }

    def get_stable_capabilities(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        return StableRollupQueryService().get_stable_capabilities()

    def get_planned_capabilities(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        return StableRollupQueryService().get_planned_capabilities()

    def get_manifest_summary(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        manifest = StableRollupQueryService().build_stable_manifest()
        return {
            "version": manifest.version,
            "release": manifest.release,
            "stable_count": len(manifest.stable_capabilities),
            "schema_count": len(manifest.schema_fingerprints),
            "content_hash": manifest.content_hash,
            "research_only": True,
        }

    def get_readiness_matrix(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        return StableRollupQueryService().build_readiness_matrix()

    def get_widget(self):
        """Headless safe — returns None when no QApplication."""
        return None

    def cancel_worker(self):
        if self._worker:
            self._worker = None

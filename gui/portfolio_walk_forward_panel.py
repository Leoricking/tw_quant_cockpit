"""Portfolio Walk-forward Research Panel v1.5.4 — Historical Simulation Only."""
RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
NO_FORMAL_LEDGER_WRITE = True
NO_LIVE_REBALANCE = True
PRODUCTION_TRADING_BLOCKED = True

TAB_CONFIG = {
    "tab_id": "portfolio_walk_forward",
    "display_name": "Portfolio Walk-forward",
    "group": "portfolio",
    "priority": "P1",
}

SAFETY_BANNER_LINES = [
    "Historical Simulation Only",
    "No Real Orders",
    "No Broker",
    "No Formal Ledger Write",
    "No Live Rebalance",
    "Past Performance Is Not Future Performance",
    "Production Trading BLOCKED",
]

FORBIDDEN_ACTIONS = [
    "Execute", "Submit", "Buy", "Sell", "Connect Broker",
    "Apply to Live Portfolio", "Auto Rebalance", "Optimize Live Weights",
]


class PortfolioWalkForwardPanel:
    """Portfolio Walk-forward research panel. Headless safe — no QApplication import at module level."""

    def __init__(self):
        self.research_only = True
        self.historical_simulation_only = True
        self._worker = None

    def get_metadata(self):
        return {
            "tab_id": TAB_CONFIG["tab_id"],
            "research_only": True,
            "historical_simulation_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "no_formal_ledger_write": True,
            "no_live_rebalance": True,
            "production_trading_blocked": True,
        }

    def get_widget(self):
        """Headless safe — returns None when no QApplication."""
        return None

    def cancel_worker(self):
        if self._worker:
            self._worker = None

    def get_safety_banner(self):
        return SAFETY_BANNER_LINES

    def get_forbidden_actions(self):
        return FORBIDDEN_ACTIONS

    def render_summary(self, result=None):
        lines = [
            "Portfolio Walk-forward Research Panel v1.5.4",
            "HISTORICAL SIMULATION ONLY — Not Investment Advice",
            f"Research Only: {self.research_only}",
            f"No Real Orders: {NO_REAL_ORDERS}",
            f"No Broker: {NO_BROKER}",
            f"Production Trading BLOCKED: {PRODUCTION_TRADING_BLOCKED}",
        ]
        return "\n".join(lines)

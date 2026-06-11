"""
GUI Health Check — v1.0.3 GUI Stability & Usability Polish.
Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. VALIDATED does not enable trading.
"""
from __future__ import annotations
import importlib
import re
from dataclasses import dataclass, field
from typing import List, Optional

_FORBIDDEN = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]
_WHITELIST = [
    "No Real Orders",
    "Broker Execution Disabled",
    "No broker execution",
    "Not an order",
    "No automatic deletion",
    "No automatic archive",
    "Archive Suggestions Only",
    "VALIDATED does not enable trading",
    "No auto trading",
    "No forbidden trading action",
]


def _scan_forbidden(text: str) -> List[str]:
    cleaned = text
    for phrase in _WHITELIST:
        cleaned = cleaned.replace(phrase, '')
    hits = []
    for f in _FORBIDDEN:
        if re.search(r'\b' + f + r'\b', cleaned):
            hits.append(f)
    return hits


@dataclass
class GuiHealthCheckResult:
    name: str
    status: str   # PASS / WARN / FAIL / BLOCKED
    detail: str = ""


@dataclass
class GuiHealthCheckReport:
    results: List[GuiHealthCheckResult] = field(default_factory=list)

    def add(self, name: str, status: str, detail: str = "") -> None:
        self.results.append(GuiHealthCheckResult(name=name, status=status, detail=detail))

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results if r.status == "PASS")

    @property
    def warn_count(self) -> int:
        return sum(1 for r in self.results if r.status == "WARN")

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if r.status == "FAIL")

    @property
    def blocked_count(self) -> int:
        return sum(1 for r in self.results if r.status == "BLOCKED")

    @property
    def overall(self) -> str:
        if self.blocked_count > 0:
            return "BLOCKED"
        if self.fail_count > 0:
            return "FAIL"
        if self.warn_count > 0:
            return "WARN"
        return "PASS"


class GuiHealthCheck:
    """
    Runs GUI health checks for v1.0.3.
    Checks panel imports, adapter imports, navigation, safety banners,
    forbidden GUI text, QThread helpers, table utils, and copy utils.
    Research Only. No Real Orders. Production Trading BLOCKED.
    Broker Execution Disabled. VALIDATED does not enable trading.
    """

    PANEL_MODULES = [
        ("gui.dashboard", "launch"),
        ("gui.navigation.tab_registry", "GUITabRegistry"),
        ("gui.strategy_lab_dashboard_panel", None),
        ("gui.strategy_validation_panel", None),
        ("gui.evidence_graph_panel", None),
        ("gui.crash_reversal_panel", None),
        ("gui.data_report_hygiene_panel", None),
        ("gui.strategy_memory_panel", None),
        ("gui.backtest_coach_panel", None),
        ("gui.training_metrics_panel", None),
        ("gui.research_intelligence_panel", None),
    ]

    ADAPTER_MODULES = [
        ("gui.strategy_lab_dashboard_adapter", None),
        ("gui.strategy_validation_adapter", None),
        ("gui.evidence_graph_adapter", None),
        ("gui.crash_reversal_adapter", None),
        ("gui.data_report_hygiene_adapter", None),
    ]

    COMMON_MODULES = [
        ("gui.common.gui_safety", "build_research_only_banner"),
        ("gui.common.gui_threading", "SafeWorker"),
        ("gui.common.table_utils", "set_table_defaults"),
        ("gui.common.empty_state", "build_empty_state"),
        ("gui.common.copy_utils", "copy_safe_text"),
    ]

    SAFETY_STRINGS = [
        "Research Only",
        "No Real Orders",
        "Production Trading BLOCKED",
        "Broker Execution Disabled",
    ]

    FORBIDDEN_GUI_STRINGS = [
        "BUY", "SELL", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
        "LIVE_TRADE", "BROKER_ORDER",
    ]

    def __init__(self):
        self.report = GuiHealthCheckReport()

    def _try_import(self, module_name: str, attr: Optional[str] = None) -> bool:
        try:
            mod = importlib.import_module(module_name)
            if attr:
                getattr(mod, attr)
            return True
        except (ImportError, AttributeError):
            return False

    def check_panels(self) -> None:
        pass_count = 0
        warn_count = 0
        for mod_name, attr in self.PANEL_MODULES:
            if self._try_import(mod_name, attr):
                pass_count += 1
            else:
                warn_count += 1
        if warn_count == 0:
            self.report.add("Panels", "PASS", f"{pass_count}/{len(self.PANEL_MODULES)} imported")
        else:
            self.report.add("Panels", "WARN", f"{pass_count} PASS, {warn_count} optional missing")

    def check_adapters(self) -> None:
        pass_count = 0
        warn_count = 0
        for mod_name, attr in self.ADAPTER_MODULES:
            if self._try_import(mod_name, attr):
                pass_count += 1
            else:
                warn_count += 1
        if warn_count == 0:
            self.report.add("Adapters", "PASS", f"{pass_count}/{len(self.ADAPTER_MODULES)} imported")
        else:
            self.report.add("Adapters", "WARN", f"{pass_count} PASS, {warn_count} optional missing")

    def check_navigation(self) -> None:
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            registry = GUITabRegistry()
            count = len(registry.list_tabs())
            self.report.add("Navigation", "PASS", f"{count} tabs registered")
        except Exception as exc:
            self.report.add("Navigation", "FAIL", f"tab_registry import failed: {exc}")

    def check_safety_banners(self) -> None:
        try:
            from gui.common.gui_safety import build_research_only_banner, SAFE_BANNER_TEXT
            banner = build_research_only_banner()
            missing = [s for s in self.SAFETY_STRINGS if s not in banner]
            if missing:
                self.report.add("Safety Banners", "WARN", f"Missing: {missing}")
            else:
                self.report.add("Safety Banners", "PASS", "All safety strings present")
        except Exception as exc:
            self.report.add("Safety Banners", "FAIL", f"gui_safety import failed: {exc}")

    def check_forbidden_gui_text(self) -> None:
        # Scan safety module strings for forbidden text
        try:
            from gui.common.gui_safety import SAFE_BANNER_TEXT, SAFE_NEXT_STEPS
            test_texts = [SAFE_BANNER_TEXT] + SAFE_NEXT_STEPS
            hits = []
            for text in test_texts:
                found = _scan_forbidden(text)
                if found:
                    hits.extend(found)
            if hits:
                self.report.add("Forbidden GUI Text", "BLOCKED", f"Detected: {hits}")
            else:
                self.report.add("Forbidden GUI Text", "PASS", "No forbidden text in safety strings")
        except Exception as exc:
            self.report.add("Forbidden GUI Text", "WARN", f"Could not scan: {exc}")

    def check_qthread_helpers(self) -> None:
        if self._try_import("gui.common.gui_threading", "SafeWorker"):
            self.report.add("QThread Helpers", "PASS", "SafeWorker available")
        else:
            self.report.add("QThread Helpers", "FAIL", "gui.common.gui_threading import failed")

    def check_table_utils(self) -> None:
        if self._try_import("gui.common.table_utils", "set_table_defaults"):
            self.report.add("Table Utils", "PASS", "set_table_defaults available")
        else:
            self.report.add("Table Utils", "FAIL", "gui.common.table_utils import failed")

    def check_copy_utils(self) -> None:
        if self._try_import("gui.common.copy_utils", "copy_safe_text"):
            self.report.add("Copy Utils", "PASS", "copy_safe_text available")
        else:
            self.report.add("Copy Utils", "FAIL", "gui.common.copy_utils import failed")

    def run_all(self) -> GuiHealthCheckReport:
        self.check_panels()
        self.check_adapters()
        self.check_navigation()
        self.check_safety_banners()
        self.check_forbidden_gui_text()
        self.check_qthread_helpers()
        self.check_table_utils()
        self.check_copy_utils()
        return self.report

    def print_report(self) -> None:
        print("=" * 60)
        print("TW Quant Cockpit — GUI Health Check")
        print("Research Only | No Real Orders | Production Trading BLOCKED")
        print("Broker Execution Disabled | VALIDATED does not enable trading")
        print("=" * 60)
        for r in self.report.results:
            print(f"  {r.name}: {r.status}" + (f" — {r.detail}" if r.detail else ""))
        print("-" * 60)
        print(f"  PASS:    {self.report.pass_count}")
        print(f"  WARN:    {self.report.warn_count}")
        print(f"  FAIL:    {self.report.fail_count}")
        print(f"  BLOCKED: {self.report.blocked_count}")
        print(f"  OVERALL: {self.report.overall}")
        print("=" * 60)

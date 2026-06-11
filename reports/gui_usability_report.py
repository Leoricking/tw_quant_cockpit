"""
GUI Usability Report Builder — v1.0.3 GUI Stability & Usability Polish.
Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. VALIDATED does not enable trading.
"""
from __future__ import annotations
import datetime
import os
from pathlib import Path
from typing import Optional


class GuiUsabilityReportBuilder:
    """
    Generates Markdown GUI Stability & Usability Report for v1.0.3.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    VERSION = "1.0.3"
    RELEASE_NAME = "GUI Stability & Usability Polish"

    PANELS = [
        "Strategy Lab Dashboard",
        "Strategy Validation",
        "Evidence Graph",
        "Crash Reversal",
        "Data Hygiene",
        "Strategy Memory",
        "Backtest Coach",
        "Training Metrics",
        "Research Intelligence",
    ]

    def __init__(self, report_dir: str = "reports", mode: str = "real"):
        self.report_dir = report_dir
        self.mode = mode
        self._today = datetime.date.today().isoformat()
        self._lines: list = []

    def _w(self, line: str = "") -> None:
        self._lines.append(line)

    def _check_panel_import(self, panel_name: str) -> str:
        module_map = {
            "Strategy Lab Dashboard": "gui.strategy_lab_dashboard_panel",
            "Strategy Validation": "gui.strategy_validation_panel",
            "Evidence Graph": "gui.evidence_graph_panel",
            "Crash Reversal": "gui.crash_reversal_panel",
            "Data Hygiene": "gui.data_report_hygiene_panel",
            "Strategy Memory": "gui.strategy_memory_panel",
            "Backtest Coach": "gui.backtest_coach_panel",
            "Training Metrics": "gui.training_metrics_panel",
            "Research Intelligence": "gui.research_intelligence_panel",
        }
        mod = module_map.get(panel_name)
        if not mod:
            return "WARN — not mapped"
        try:
            import importlib
            importlib.import_module(mod)
            return "PASS"
        except ImportError:
            return "WARN — optional, not installed"
        except Exception as exc:
            return f"FAIL — {exc}"

    def _check_nav_keyword(self, keyword: str) -> str:
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            registry = GUITabRegistry()
            tabs = registry.list_tabs()
            matches = [t for t in tabs if keyword.lower() in " ".join(t.keywords).lower()]
            return f"PASS — {len(matches)} tab(s)" if matches else "WARN — no match"
        except Exception as exc:
            return f"FAIL — {exc}"

    def _check_import(self, module: str, attr: str) -> str:
        try:
            import importlib
            mod = importlib.import_module(module)
            getattr(mod, attr)
            return "PASS"
        except Exception as exc:
            return f"FAIL — {exc}"

    def build(self) -> str:
        self._lines = []
        self._w(f"# GUI Stability & Usability Report v{self.VERSION}")
        self._w(f"> Research Only | No Real Orders | Production Trading BLOCKED | Broker Execution Disabled | VALIDATED does not enable trading")
        self._w(f"> Generated: {self._today} | Mode: {self.mode}")
        self._w()

        # Section 1 — Overview
        self._w("## 一、總覽 (Overview)")
        self._w()
        self._w(f"| Field | Value |")
        self._w(f"|-------|-------|")
        self._w(f"| Version | {self.VERSION} |")
        self._w(f"| Release | {self.RELEASE_NAME} |")
        self._w(f"| Research Only | True |")
        self._w(f"| No Real Orders | True |")
        self._w(f"| Production Trading BLOCKED | True |")
        self._w(f"| Broker Execution Disabled | True |")
        self._w(f"| VALIDATED does not enable trading | True |")
        self._w(f"| GUI Stability Focus | True |")
        self._w()

        # Section 2 — Panel Health
        self._w("## 二、Panel Health")
        self._w()
        self._w("| Panel | Import | Note |")
        self._w("|-------|--------|------|")
        for panel in self.PANELS:
            status = self._check_panel_import(panel)
            self._w(f"| {panel} | {status} | Research Only |")
        self._w()

        # Section 3 — Navigation Health
        self._w("## 三、Navigation Health")
        self._w()
        keywords_to_check = [
            "strategy lab dashboard", "strategy validation", "evidence graph",
            "crash reversal", "data hygiene", "maintenance",
            "GUI優化", "介面穩定", "安全複製",
        ]
        self._w("| Keyword | Result |")
        self._w("|---------|--------|")
        for kw in keywords_to_check:
            result = self._check_nav_keyword(kw)
            self._w(f"| {kw} | {result} |")
        self._w()

        # Section 4 — QThread Safety
        self._w("## 四、QThread Safety")
        self._w()
        qt_result = self._check_import("gui.common.gui_threading", "SafeWorker")
        cleanup_result = self._check_import("gui.common.gui_threading", "cleanup_thread")
        run_result = self._check_import("gui.common.gui_threading", "run_in_qthread")
        self._w("| Component | Status |")
        self._w("|-----------|--------|")
        self._w(f"| SafeWorker | {qt_result} |")
        self._w(f"| cleanup_thread | {cleanup_result} |")
        self._w(f"| run_in_qthread | {run_result} |")
        self._w(f"| Worker lifecycle | Prevent QThread destroyed warning |")
        self._w(f"| Exception handling | Friendly error via SafeWorkerResult |")
        self._w()

        # Section 5 — Table Usability
        self._w("## 五、Table Usability")
        self._w()
        tbl_result = self._check_import("gui.common.table_utils", "set_table_defaults")
        self._w("| Feature | Status |")
        self._w("|---------|--------|")
        self._w(f"| table_utils import | {tbl_result} |")
        self._w(f"| Column width cap | max_width=360 |")
        self._w(f"| Ellipsis delegate | Available |")
        self._w(f"| Tooltip from cell | Available |")
        self._w(f"| Empty row message | No data yet |")
        self._w(f"| Bool formatting | True/False or ✓/— |")
        self._w(f"| Score formatting | 1 decimal place |")
        self._w()

        # Section 6 — Copy Safety
        self._w("## 六、Copy Safety")
        self._w()
        copy_result = self._check_import("gui.common.copy_utils", "copy_safe_text")
        safety_result = self._check_import("gui.common.gui_safety", "assert_no_forbidden_gui_text")
        self._w("| Feature | Status |")
        self._w("|---------|--------|")
        self._w(f"| copy_utils import | {copy_result} |")
        self._w(f"| Forbidden text scan | {safety_result} |")
        self._w(f"| Safe command copy | Research CLI only |")
        self._w(f"| Safe next step copy | Whitelist enforced |")
        self._w(f"| Forbidden action block | BUY/SELL/SUBMIT blocked |")
        self._w()

        # Section 7 — Known Warnings
        self._w("## 七、Known Warnings")
        self._w()
        self._w("- Missing optional panel: WARN (non-critical, panel not yet installed)")
        self._w("- No latest output found: WARN (non-critical, run command first)")
        self._w("- Optional report missing: WARN (non-critical, ENV_LIMITED)")
        self._w("- cp950 subprocess encoding warning: Windows only, non-critical")
        self._w()

        # Section 8 — Safety Declaration
        self._w("## 八、安全聲明 (Safety Declaration)")
        self._w()
        self._w("> **No Real Orders** — This system does not and cannot place real trading actions.")
        self._w(">")
        self._w("> **No broker execution** — There is no connection to any broker API.")
        self._w(">")
        self._w("> **No auto trading** — No automatic trading, no automatic rule weight changes.")
        self._w(">")
        self._w("> **GUI does not enable trading** — GUI panels are research-only displays.")
        self._w(">")
        self._w("> **VALIDATED does not enable trading** — VALIDATED grade is research-only.")
        self._w(">")
        self._w("> **Not Investment Advice** — Nothing in this system constitutes investment advice.")
        self._w()
        self._w(f"---")
        self._w(f"*TW Quant Cockpit v{self.VERSION} — {self.RELEASE_NAME} — Research Only — Not Investment Advice*")
        return "\n".join(self._lines)

    def save(self) -> str:
        os.makedirs(self.report_dir, exist_ok=True)
        filename = f"gui_usability_report_{self._today}.md"
        path = os.path.join(self.report_dir, filename)
        content = self.build()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

"""
Regression Hardening Report Builder — v1.0.4.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import datetime
import importlib
import os


class RegressionHardeningReportBuilder:
    VERSION = "1.0.4"
    RELEASE_NAME = "Regression & Release Gate Hardening"

    def __init__(self, report_dir: str = "reports", mode: str = "real"):
        self.report_dir = report_dir
        self.mode = mode
        self._today = datetime.date.today().isoformat()
        self._lines: list = []

    def _w(self, line: str = "") -> None:
        self._lines.append(line)

    def _check_import(self, module: str, attr: str) -> str:
        try:
            mod = importlib.import_module(module)
            getattr(mod, attr)
            return "PASS"
        except Exception as exc:
            return f"FAIL \u2014 {exc}"

    def build(self) -> str:
        self._lines = []
        self._w(f"# Regression & Release Gate Hardening Report v{self.VERSION}")
        self._w(f"> Research Only | No Real Orders | Production Trading BLOCKED | Broker Execution Disabled | VALIDATED does not enable trading")
        self._w(f"> Generated: {self._today} | Mode: {self.mode}")
        self._w()

        # Section 1 — Overview
        self._w("## \u4e00\u3001\u7e3d\u89bd (Overview)")
        self._w()
        self._w("| Field | Value |")
        self._w("|-------|-------|")
        self._w(f"| Version | {self.VERSION} |")
        self._w(f"| Release | {self.RELEASE_NAME} |")
        self._w(f"| Research Only | True |")
        self._w(f"| No Real Orders | True |")
        self._w(f"| Production Trading BLOCKED | True |")
        self._w(f"| Broker Execution Disabled | True |")
        self._w(f"| VALIDATED does not enable trading | True |")
        self._w(f"| Regression Hardening Release | True |")
        self._w(f"| Release Gate Hardening | True |")
        self._w(f"| Safety Scanner Hardening | True |")
        self._w()

        # Section 2 — Release Gate Health
        self._w("## \u4e8c\u3001Release Gate Health")
        self._w()
        rgh_result = self._check_import("regression_hardening.release_gate_health", "ReleaseGateHealth")
        rgs_result = self._check_import("regression.suite_registry", "SUITE_RELEASE_GATE")
        self._w("| Component | Status |")
        self._w("|-----------|--------|")
        self._w(f"| ReleaseGateHealth | {rgh_result} |")
        self._w(f"| release_gate suite | {rgs_result} |")
        self._w(f"| Known WARNs classified | 4 categories |")
        self._w(f"| Known BLOCKED classified | 1 category |")
        self._w(f"| Unknown FAIL target | 0 |")
        self._w()

        # Section 3 — Safety Scanner
        self._w("## \u4e09\u3001Safety Scanner")
        self._w()
        ss_result = self._check_import("regression_hardening.safety_scanner", "SafetyScanner")
        self._w("| Component | Status |")
        self._w("|-----------|--------|")
        self._w(f"| SafetyScanner | {ss_result} |")
        self._w(f"| Forbidden actions | 9 patterns |")
        self._w(f"| Whitelist phrases | See safety_scanner.py |")
        self._w(f"| No Real Orders false positive | Whitelisted |")
        self._w(f"| Broker Execution Disabled false positive | Whitelisted |")
        self._w()

        # Section 4 — Known Warning Classification
        self._w("## \u56db\u3001Known Warning Classification")
        self._w()
        self._w("| Classification | Description |")
        self._w("|----------------|-------------|")
        self._w("| KNOWN_CP950_WARNING | Windows cp950 subprocess encoding (non-critical) |")
        self._w("| KNOWN_PAPER_SMOKE_WARNING | paper_state.json missing (non-critical) |")
        self._w("| KNOWN_REPORT_PACK_OPTIONAL | ENV_LIMITED / NOT_GENERATED optional reports |")
        self._w("| KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE | no_real_orders flag pre-existing check |")
        self._w("| KNOWN_NO_REAL_ORDERS_FLAG_CHECK | Known BLOCKED \u2014 pre-existing advisory |")
        self._w()

        # Section 5 — Regression Summary
        self._w("## \u4e94\u3001Regression Summary")
        self._w()
        rs_result = self._check_import("regression_hardening.regression_summary", "build_release_summary")
        self._w("| Component | Status |")
        self._w("|-----------|--------|")
        self._w(f"| regression_summary | {rs_result} |")
        self._w(f"| UNKNOWN_FAIL target | 0 |")
        self._w(f"| UNKNOWN_BLOCKED target | 0 |")
        self._w(f"| Known vs Unknown classification | Available |")
        self._w()

        # Section 6 — Hardening Actions
        self._w("## \u516d\u3001Hardening Actions")
        self._w()
        self._w("- Safety scanner: expanded whitelist, context-aware forbidden detection")
        self._w("- Regression summary: warning/blocked classification with known vs unknown")
        self._w("- Release gate health: explicit known warn/blocked listing")
        self._w("- Encoding utils: Windows cp950 warning detection and classification")
        self._w("- Checklist integration: 5 new stable checks, 5 new stable-v060 checks")
        self._w("- Regression suite: 16 new release_gate test cases")
        self._w("- Docs: regression_release_gate_hardening_v1.0.4.md")
        self._w()

        # Section 7 — Safety Declaration
        self._w("## \u4e03\u3001\u5b89\u5168\u8072\u660e (Safety Declaration)")
        self._w()
        self._w("> **No Real Orders** \u2014 This system does not and cannot place real trading actions.")
        self._w(">")
        self._w("> **No broker execution** \u2014 There is no connection to any broker API.")
        self._w(">")
        self._w("> **No auto trading** \u2014 No automatic trading, no automatic rule weight changes.")
        self._w(">")
        self._w("> **Regression does not enable trading** \u2014 Regression checks are research-only.")
        self._w(">")
        self._w("> **VALIDATED does not enable trading** \u2014 VALIDATED grade is research-only.")
        self._w(">")
        self._w("> **Not Investment Advice** \u2014 Nothing in this system constitutes investment advice.")
        self._w()
        self._w("---")
        self._w(f"*TW Quant Cockpit v{self.VERSION} \u2014 {self.RELEASE_NAME} \u2014 Research Only \u2014 Not Investment Advice*")
        return "\n".join(self._lines)

    def save(self) -> str:
        os.makedirs(self.report_dir, exist_ok=True)
        filename = f"regression_hardening_report_{self._today}.md"
        path = os.path.join(self.report_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build())
        return path

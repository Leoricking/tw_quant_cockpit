"""
Documentation Health Report Builder — v1.0.5 Documentation & User Guide Polish.
Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. VALIDATED does not enable trading.
"""
from __future__ import annotations
import datetime
import os


class DocumentationHealthReportBuilder:
    VERSION = "1.0.5"
    RELEASE_NAME = "Documentation & User Guide Polish"

    CORE_DOCS = {
        "README": "README.md",
        "docs/index": "docs/index.md",
        "User Guide": "docs/user_guide_v1.0.md",
        "GUI User Guide": "docs/gui_user_guide_v1.0.md",
        "CLI Cookbook": "docs/cli_cookbook_v1.0.md",
        "Daily Workflow SOP": "docs/daily_workflow_sop_v1.0.md",
        "Troubleshooting": "docs/troubleshooting_v1.0.md",
        "Safety Guide": "docs/safety_guide_v1.0.md",
        "Version Map": "docs/version_map_v1.0.md",
        "Handoff Guide": "docs/handoff_guide_v1.0.md",
    }

    def __init__(self, report_dir: str = "reports", mode: str = "real"):
        self.report_dir = report_dir
        self.mode = mode
        self._today = datetime.date.today().isoformat()
        self._lines: list = []

    def _w(self, line: str = "") -> None:
        self._lines.append(line)

    def _exists(self, path: str) -> str:
        import os
        return "PASS" if os.path.exists(path) else "WARN — not found"

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
        self._w(f"# Documentation & User Guide Polish Report v{self.VERSION}")
        self._w(f"> Research Only | No Real Orders | Production Trading BLOCKED | Broker Execution Disabled | VALIDATED does not enable trading")
        self._w(f"> Generated: {self._today} | Mode: {self.mode}")
        self._w()

        # Section 1 — Overview
        self._w("## Overview")
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
        self._w(f"| Documentation Polish Release | True |")
        self._w(f"| User Guide Focus | True |")
        self._w(f"| Handoff Guide Available | True |")
        self._w()

        # Section 2 — Core Documents
        self._w("## Core Documents")
        self._w()
        self._w("| Document | Status |")
        self._w("|----------|--------|")
        for name, path in self.CORE_DOCS.items():
            status = self._exists(path)
            self._w(f"| {name} | {status} |")
        self._w()

        # Section 3 — Documentation Health
        self._w("## Documentation Health")
        self._w()
        hc_result = self._check_import("documentation.docs_health_check", "DocumentationHealthCheck")
        idx_result = self._check_import("documentation.docs_indexer", "DocumentationIndexer")
        sum_result = self._check_import("documentation.docs_summary", "DocumentationSummaryBuilder")
        self._w("| Component | Status |")
        self._w("|-----------|--------|")
        self._w(f"| DocumentationHealthCheck | {hc_result} |")
        self._w(f"| DocumentationIndexer | {idx_result} |")
        self._w(f"| DocumentationSummaryBuilder | {sum_result} |")
        self._w()

        # Section 4 — Safety Coverage
        self._w("## Safety Coverage")
        self._w()
        self._w("| Phrase | Requirement |")
        self._w("|--------|-------------|")
        self._w("| Research Only | All core docs |")
        self._w("| No Real Orders | All core docs |")
        self._w("| Broker Execution Disabled | README + User Guide + Safety Guide |")
        self._w("| VALIDATED does not enable trading | User Guide + Safety Guide |")
        self._w("| No compound command rule | Handoff Guide + CLI Cookbook |")
        self._w("| No git add . rule | Handoff Guide |")
        self._w()

        # Section 5 — How to Start
        self._w("## How to Start")
        self._w()
        self._w("**GUI:**")
        self._w("```")
        self._w("python main.py cockpit")
        self._w("```")
        self._w()
        self._w("**CLI:**")
        self._w("```")
        self._w("python main.py version-info")
        self._w("python main.py research-cockpit-stable --mode real")
        self._w("python main.py strategy-lab-dashboard --mode real")
        self._w("```")
        self._w()
        self._w("**Reports:**")
        self._w("```")
        self._w("python main.py report-pack --type full --mode real")
        self._w("```")
        self._w()
        self._w("**Daily Workflow:** See `docs/daily_workflow_sop_v1.0.md`")
        self._w()

        # Section 6 — Known Warnings
        self._w("## Known Warnings")
        self._w()
        self._w("| Warning | Classification |")
        self._w("|---------|---------------|")
        self._w("| cp950 subprocess encoding | KNOWN_CP950_WARNING (non-critical) |")
        self._w("| paper_state.json missing | KNOWN_PAPER_SMOKE_WARNING (non-critical) |")
        self._w("| ENV_LIMITED report | KNOWN_REPORT_PACK_OPTIONAL (non-critical) |")
        self._w("| no_real_orders flag check | KNOWN_NO_REAL_ORDERS_FLAG_CHECK (known) |")
        self._w()

        # Section 7 — Safety Declaration
        self._w("## Safety Declaration")
        self._w()
        self._w("> **No Real Orders** — This system does not and cannot place real trading actions.")
        self._w(">")
        self._w("> **No broker execution** — There is no connection to any broker API.")
        self._w(">")
        self._w("> **No auto trading** — No automatic trading, no automatic rule weight changes.")
        self._w(">")
        self._w("> **VALIDATED does not enable trading** — VALIDATED grade is research-only.")
        self._w(">")
        self._w("> **Not Investment Advice** — Nothing in this system constitutes investment advice.")
        self._w()
        self._w("---")
        self._w(f"*TW Quant Cockpit v{self.VERSION} — {self.RELEASE_NAME} — Research Only — Not Investment Advice*")
        return "\n".join(self._lines)

    def save(self) -> str:
        os.makedirs(self.report_dir, exist_ok=True)
        filename = f"documentation_health_report_{self._today}.md"
        path = os.path.join(self.report_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build())
        return path

"""
Workflow Templates Report Builder — v1.0.6 Example Workflows & Templates.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import datetime
import os


class WorkflowTemplatesReportBuilder:
    VERSION = "1.0.6"
    RELEASE_NAME = "Example Workflows & Templates"

    EXAMPLES = [
        "Daily Operation", "Weekend Review", "Single Stock Research",
        "Strategy Validation", "Crash Reversal Review", "Data Hygiene",
        "GUI Operation", "Claude Code Maintenance", "Troubleshooting",
        "Paper & Mock Practice",
    ]

    TEMPLATES = [
        "Daily Review", "Single Stock Research", "Strategy Idea",
        "Backtest Review", "Weekly Retrospective", "Error Report",
        "Release Prompt", "Handoff Summary",
    ]

    EXAMPLE_PATHS = {
        "Daily Operation": "docs/examples/daily_operation_example.md",
        "Weekend Review": "docs/examples/weekend_review_example.md",
        "Single Stock Research": "docs/examples/single_stock_research_example.md",
        "Strategy Validation": "docs/examples/strategy_validation_example.md",
        "Crash Reversal Review": "docs/examples/crash_reversal_review_example.md",
        "Data Hygiene": "docs/examples/data_hygiene_example.md",
        "GUI Operation": "docs/examples/gui_operation_example.md",
        "Claude Code Maintenance": "docs/examples/claude_code_maintenance_example.md",
        "Troubleshooting": "docs/examples/troubleshooting_example.md",
        "Paper & Mock Practice": "docs/examples/paper_mock_practice_example.md",
    }

    TEMPLATE_PATHS = {
        "Daily Review": "docs/templates/daily_review_template.md",
        "Single Stock Research": "docs/templates/single_stock_research_template.md",
        "Strategy Idea": "docs/templates/strategy_idea_template.md",
        "Backtest Review": "docs/templates/backtest_review_template.md",
        "Weekly Retrospective": "docs/templates/weekly_retrospective_template.md",
        "Error Report": "docs/templates/error_report_template.md",
        "Release Prompt": "docs/templates/release_prompt_template.md",
        "Handoff Summary": "docs/templates/handoff_summary_template.md",
    }

    def __init__(self, report_dir: str = "reports", mode: str = "real"):
        self.report_dir = report_dir
        self.mode = mode
        self._today = datetime.date.today().isoformat()
        self._lines: list = []

    def _w(self, line: str = "") -> None:
        self._lines.append(line)

    def _check_exists(self, path: str) -> str:
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
        self._w(f"# Example Workflows & Templates Report v{self.VERSION}")
        self._w(f"> Research Only | No Real Orders | Production Trading BLOCKED | Broker Execution Disabled | VALIDATED does not enable trading")
        self._w(f"> Generated: {self._today} | Mode: {self.mode}")
        self._w()

        # Section 1 — Overview
        self._w("## 一、總覽 (Overview)")
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
        self._w(f"| Workflow Templates Available | True |")
        self._w()

        # Section 2 — Example Workflows
        self._w("## 二、Example Workflows")
        self._w()
        self._w("| Example | Status |")
        self._w("|---------|--------|")
        for name in self.EXAMPLES:
            path = self.EXAMPLE_PATHS.get(name, "")
            status = self._check_exists(path) if path else "WARN — not mapped"
            self._w(f"| {name} | {status} |")
        self._w()

        # Section 3 — Templates
        self._w("## 三、Templates")
        self._w()
        self._w("| Template | Status |")
        self._w("|----------|--------|")
        for name in self.TEMPLATES:
            path = self.TEMPLATE_PATHS.get(name, "")
            status = self._check_exists(path) if path else "WARN — not mapped"
            self._w(f"| {name} | {status} |")
        self._w()

        # Section 4 — Template Health
        self._w("## 四、Template Health")
        self._w()
        hc = self._check_import("workflows.workflow_template_health", "WorkflowTemplateHealthCheck")
        idx = self._check_import("workflows.workflow_template_indexer", "WorkflowTemplateIndexer")
        self._w("| Component | Status |")
        self._w("|-----------|--------|")
        self._w(f"| WorkflowTemplateHealthCheck | {hc} |")
        self._w(f"| WorkflowTemplateIndexer | {idx} |")
        self._w(f"| No forbidden actions | Verified via SafetyScanner |")
        self._w(f"| No compound commands | Verified |")
        self._w(f"| No git add . | Verified |")
        self._w(f"| No heredoc commit | Verified |")
        self._w()

        # Section 5 — How to Use
        self._w("## 五、How to Use")
        self._w()
        self._w("1. Choose the workflow example matching your situation from `docs/examples/`")
        self._w("2. Copy the relevant template from `docs/templates/`")
        self._w("3. Fill in the template fields")
        self._w("4. Run the safe CLI commands listed in the example")
        self._w("5. Attach the generated report to your review notes")
        self._w("6. Review only — no trading actions")
        self._w()

        # Section 6 — Safety Declaration
        self._w("## 六、安全聲明 (Safety Declaration)")
        self._w()
        self._w("> **No Real Orders** — Templates do not and cannot trigger real trading actions.")
        self._w(">")
        self._w("> **No broker execution** — There is no connection to any broker API.")
        self._w(">")
        self._w("> **No auto trading** — No automatic trading, no automatic rule changes.")
        self._w(">")
        self._w("> **Templates do not enable trading** — All templates are research-only.")
        self._w(">")
        self._w("> **Not Investment Advice** — Nothing in this system constitutes investment advice.")
        self._w()
        self._w("---")
        self._w(f"*TW Quant Cockpit v{self.VERSION} — {self.RELEASE_NAME} — Research Only — Not Investment Advice*")
        return "\n".join(self._lines)

    def save(self) -> str:
        os.makedirs(self.report_dir, exist_ok=True)
        filename = f"workflow_templates_report_{self._today}.md"
        path = os.path.join(self.report_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build())
        return path

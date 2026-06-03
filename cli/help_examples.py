"""
cli/help_examples.py — CLIHelpExamples for TW Quant Cockpit v0.5.1.

Curated usage examples grouped by workflow phase.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class CLIHelpExamples:
    """
    Curated CLI usage examples for TW Quant Cockpit v0.5.1.

    Examples are grouped into the following categories:
      quick_start      — Getting started in < 1 minute
      daily_research   — Standard daily research pipeline
      weekly_review    — Weekly review and journal
      safety_checks    — Safety, release, and regression
      alias_reference  — Short aliases quick reference

    Safety invariants
    -----------------
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    # ------------------------------------------------------------------
    # Class-level example data
    # ------------------------------------------------------------------

    QUICK_START: List[dict] = [
        {
            "example": "python main.py version-info",
            "notes":   "Show application version and build metadata",
        },
        {
            "example": "python main.py research-os-summary",
            "notes":   "High-level overview of all research OS modules",
        },
        {
            "example": "python main.py run-research --profile quick --mode real",
            "notes":   "Quick research pipeline run (real data, no orders)",
        },
        {
            "example": "python main.py auto-report --mode real --profile daily",
            "notes":   "Auto-generate all daily reports",
        },
        {
            "example": "python main.py cockpit --mode real",
            "notes":   "Launch the PySide6 Cockpit GUI",
        },
    ]

    DAILY_RESEARCH: List[dict] = [
        {
            "example": "python main.py data-quality-gate --mode real",
            "notes":   "Run all data quality checks (pass/fail gate)",
        },
        {
            "example": "python main.py provider-reliability --mode real",
            "notes":   "Check data provider reliability scores",
        },
        {
            "example": "python main.py research-coach --mode real --period daily",
            "notes":   "Get daily research coaching suggestions",
        },
        {
            "example": "python main.py research-workflow --mode real --type daily_research --dry-run",
            "notes":   "Preview daily workflow without executing tasks",
        },
        {
            "example": "python main.py research-workflow --mode real --type daily_research",
            "notes":   "Run full daily research workflow",
        },
    ]

    WEEKLY_REVIEW: List[dict] = [
        {
            "example": "python main.py research-review --mode real --period weekly",
            "notes":   "Run structured weekly research review",
        },
        {
            "example": "python main.py journal-summary",
            "notes":   "Print concise journal summary for the week",
        },
        {
            "example": "python main.py rule-governance --mode real",
            "notes":   "Audit rule conflicts and coverage",
        },
        {
            "example": "python main.py experiment-list",
            "notes":   "List all registered experiments",
        },
        {
            "example": "python main.py research-workflow --mode real --type weekly_review",
            "notes":   "Run full weekly review workflow",
        },
    ]

    SAFETY_CHECKS: List[dict] = [
        {
            "example": "python main.py stable-release-check --mode real",
            "notes":   "Verify all stability gates before release",
        },
        {
            "example": "python main.py regression-suite --mode real --quick",
            "notes":   "Run quick regression test subset",
        },
        {
            "example": "python main.py research-os-safety",
            "notes":   "Verify safety invariants across all OS modules",
        },
    ]

    ALIAS_REFERENCE: List[dict] = [
        {
            "example": "python main.py daily",
            "notes":   "→ run-research --profile daily --mode real",
        },
        {
            "example": "python main.py quick",
            "notes":   "→ run-research --profile quick --mode real",
        },
        {
            "example": "python main.py dq --mode real",
            "notes":   "→ data-quality-gate --mode real",
        },
        {
            "example": "python main.py providers",
            "notes":   "→ provider-reliability",
        },
        {
            "example": "python main.py rules",
            "notes":   "→ rule-governance",
        },
        {
            "example": "python main.py signals",
            "notes":   "→ signal-quality",
        },
        {
            "example": "python main.py journal",
            "notes":   "→ journal-summary",
        },
        {
            "example": "python main.py notify",
            "notes":   "→ notification-list",
        },
        {
            "example": "python main.py os",
            "notes":   "→ research-os-summary",
        },
        {
            "example": "python main.py version",
            "notes":   "→ version-info",
        },
        {
            "example": "python main.py gui",
            "notes":   "→ cockpit",
        },
    ]

    # Per-command example map (command name → list of example strings)
    _COMMAND_EXAMPLES: Dict[str, List[str]] = {
        "version-info":            ["python main.py version-info"],
        "research-os-summary":     ["python main.py research-os-summary"],
        "run-research":            [
            "python main.py run-research --profile quick --mode real",
            "python main.py run-research --profile daily --mode real",
        ],
        "auto-report":             ["python main.py auto-report --mode real --profile daily"],
        "cockpit":                 ["python main.py cockpit --mode real"],
        "data-quality-gate":       ["python main.py data-quality-gate --mode real"],
        "provider-reliability":    ["python main.py provider-reliability --mode real"],
        "research-coach":          ["python main.py research-coach --mode real --period daily"],
        "research-workflow":       [
            "python main.py research-workflow --mode real --type daily_research --dry-run",
            "python main.py research-workflow --mode real --type daily_research",
            "python main.py research-workflow --mode real --type weekly_review",
        ],
        "research-review":         [
            "python main.py research-review --mode real --period daily",
            "python main.py research-review --mode real --period weekly",
        ],
        "journal-summary":         ["python main.py journal-summary"],
        "rule-governance":         ["python main.py rule-governance --mode real"],
        "stable-release-check":    ["python main.py stable-release-check --mode real"],
        "regression-suite":        [
            "python main.py regression-suite --mode real",
            "python main.py regression-suite --mode real --quick",
        ],
        "research-os-safety":      ["python main.py research-os-safety"],
        "intraday-replay":         ["python main.py intraday-replay --mode real"],
        "signal-quality":          ["python main.py signal-quality --mode real"],
        "ml-feature-catalog":      ["python main.py ml-feature-catalog --mode real"],
        "notification-list":       ["python main.py notification-list"],
        "provider-health":         ["python main.py provider-health --mode real"],
    }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_examples(self, command: str) -> List[str]:
        """
        Return example strings for a specific command.

        Parameters
        ----------
        command : str
            Canonical command name.

        Returns
        -------
        list of example command strings, or empty list if not found.
        """
        return list(self._COMMAND_EXAMPLES.get(command, []))

    def get_category_examples(self, category: str) -> List[dict]:
        """
        Return example dicts for a named category group.

        Valid category names:
          quick_start, daily_research, weekly_review, safety_checks, alias_reference

        Returns
        -------
        list of {"example": str, "notes": str}
        """
        mapping = {
            "quick_start":     self.QUICK_START,
            "daily_research":  self.DAILY_RESEARCH,
            "weekly_review":   self.WEEKLY_REVIEW,
            "safety_checks":   self.SAFETY_CHECKS,
            "alias_reference": self.ALIAS_REFERENCE,
        }
        return list(mapping.get(category, []))

    def get_quick_start(self) -> List[dict]:
        """Return Quick Start examples."""
        return list(self.QUICK_START)

    def get_daily_workflow_examples(self) -> List[dict]:
        """Return Daily Research examples."""
        return list(self.DAILY_RESEARCH)

    def get_safety_examples(self) -> List[dict]:
        """Return Safety Check examples."""
        return list(self.SAFETY_CHECKS)

    def get_all_examples(self) -> Dict[str, List[dict]]:
        """
        Return all examples grouped by category name.

        Returns
        -------
        dict mapping category → list of {"example": str, "notes": str}
        """
        return {
            "quick_start":     list(self.QUICK_START),
            "daily_research":  list(self.DAILY_RESEARCH),
            "weekly_review":   list(self.WEEKLY_REVIEW),
            "safety_checks":   list(self.SAFETY_CHECKS),
            "alias_reference": list(self.ALIAS_REFERENCE),
        }

    def print_all(self) -> None:
        """Print all examples to stdout in a readable format."""
        sections = {
            "Quick Start":         self.QUICK_START,
            "Daily Research":      self.DAILY_RESEARCH,
            "Weekly Review":       self.WEEKLY_REVIEW,
            "Safety Checks":       self.SAFETY_CHECKS,
            "Alias Quick Reference": self.ALIAS_REFERENCE,
        }
        print()
        print("=" * 72)
        print("  TW Quant Cockpit — CLI Usage Examples  (v0.5.1)")
        print("  [!] Research Only  |  No Real Orders  |  Production: BLOCKED")
        print("=" * 72)
        for section_title, examples in sections.items():
            print()
            print(f"  {section_title}")
            print("  " + "-" * 66)
            for ex in examples:
                print(f"    {ex['example']}")
                if ex.get("notes"):
                    print(f"      # {ex['notes']}")
        print()
        print("=" * 72)
        print()

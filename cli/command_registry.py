"""
cli/command_registry.py — CLICommand dataclass and CLICommandRegistry (v0.5.1).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Valid category and safety-level literals
# ---------------------------------------------------------------------------

VALID_CATEGORIES = {
    "data", "provider", "quality", "strategy", "backtest", "portfolio",
    "ml", "replay", "journal", "notification", "review", "coach",
    "workflow", "os_planning", "release", "gui", "utility",
}

VALID_SAFETY_LEVELS = {
    "SAFE_READ_ONLY",
    "RESEARCH_ONLY",
    "REPORT_ONLY",
    "SIMULATION_ONLY",
    "GUI_ONLY",
    "BLOCKED_TRADING",
}


# ---------------------------------------------------------------------------
# CLICommand dataclass
# ---------------------------------------------------------------------------

@dataclass
class CLICommand:
    """
    Represents a single CLI command entry in the TW Quant Cockpit.

    Safety invariants
    -----------------
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False
    """

    name:              str
    category:          str
    purpose:           str
    description:       str
    aliases:           List[str] = field(default_factory=list)
    canonical_command: str       = ""
    example_commands:  List[str] = field(default_factory=list)
    mode_support:      List[str] = field(default_factory=lambda: ["real", "mock"])
    report_support:    bool      = False
    output_paths:      List[str] = field(default_factory=list)
    safety_level:      str       = "SAFE_READ_ONLY"
    read_only:         bool      = True
    no_real_orders:    bool      = True
    production_blocked: bool     = True
    legacy:            bool      = False
    deprecation_candidate: bool  = False
    hidden:            bool      = False
    notes:             str       = ""

    def __post_init__(self) -> None:
        if not self.canonical_command:
            self.canonical_command = self.name
        if self.category not in VALID_CATEGORIES:
            logger.warning("CLICommand '%s' has unknown category '%s'", self.name, self.category)
        if self.safety_level not in VALID_SAFETY_LEVELS:
            logger.warning("CLICommand '%s' has unknown safety_level '%s'", self.name, self.safety_level)

    def to_dict(self) -> dict:
        return {
            "name":               self.name,
            "category":           self.category,
            "purpose":            self.purpose,
            "description":        self.description,
            "aliases":            ", ".join(self.aliases),
            "canonical_command":  self.canonical_command,
            "example_commands":   "; ".join(self.example_commands),
            "mode_support":       ", ".join(self.mode_support),
            "report_support":     self.report_support,
            "safety_level":       self.safety_level,
            "read_only":          self.read_only,
            "no_real_orders":     self.no_real_orders,
            "production_blocked": self.production_blocked,
            "legacy":             self.legacy,
            "deprecation_candidate": self.deprecation_candidate,
            "hidden":             self.hidden,
            "notes":              self.notes,
        }


# ---------------------------------------------------------------------------
# CLICommandRegistry
# ---------------------------------------------------------------------------

class CLICommandRegistry:
    """
    Registry of all CLI commands for TW Quant Cockpit v0.5.1.

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

    def __init__(self) -> None:
        self._commands: dict[str, CLICommand] = {}
        self._build_registry()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, cmd: CLICommand) -> None:
        """Register a CLICommand. Skips silently if name already registered."""
        if cmd.name in self._commands:
            logger.debug("CLICommandRegistry: skipping duplicate '%s'", cmd.name)
            return
        self._commands[cmd.name] = cmd

    def list_commands(self, category: Optional[str] = None) -> List[CLICommand]:
        """Return all commands, optionally filtered by category."""
        cmds = list(self._commands.values())
        if category:
            cmds = [c for c in cmds if c.category == category]
        return sorted(cmds, key=lambda c: (c.category, c.name))

    def get_command(self, name: str) -> Optional[CLICommand]:
        """Return command by exact name, or None."""
        return self._commands.get(name)

    def get_alias_target(self, alias: str) -> Optional[str]:
        """Search aliases fields; return canonical command name or None."""
        for cmd in self._commands.values():
            if alias in cmd.aliases:
                return cmd.name
        return None

    def resolve_command(self, name: str) -> Optional[CLICommand]:
        """Check direct name first, then aliases."""
        if name in self._commands:
            return self._commands[name]
        target = self.get_alias_target(name)
        if target:
            return self._commands.get(target)
        return None

    def export_registry(self) -> List[dict]:
        """Return list of dicts suitable for CSV export or GUI tables."""
        return [cmd.to_dict() for cmd in self.list_commands()]

    # ------------------------------------------------------------------
    # Internal build
    # ------------------------------------------------------------------

    def _build_registry(self) -> None:  # noqa: C901
        """Populate the command registry with the full command set."""

        # ----------------------------------------------------------------
        # utility
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="version-info", category="utility", aliases=["version"],
                purpose="Show application version",
                description="Print TW Quant Cockpit version string and build metadata.",
                example_commands=["python main.py version-info"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-os-summary", category="utility", aliases=["os"],
                purpose="Print research OS module summary",
                description="High-level summary of all research OS modules, status, and coverage.",
                example_commands=["python main.py research-os-summary"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-os-audit", category="utility", aliases=["os-audit"],
                purpose="Audit research OS modules",
                description="Deep audit of all research OS modules for gaps and inconsistencies.",
                example_commands=["python main.py research-os-audit"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="cli-list", category="utility",
                purpose="List all CLI commands",
                description="Print all registered CLI commands grouped by category.",
                example_commands=["python main.py cli-list"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="cli-search", category="utility",
                purpose="Search CLI commands by keyword",
                description="Search commands by keyword in name, purpose, description, or category.",
                example_commands=["python main.py cli-search replay"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="cli-aliases", category="utility",
                purpose="List all CLI aliases",
                description="Print all registered short aliases and their target commands.",
                example_commands=["python main.py cli-aliases"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="cli-examples", category="utility",
                purpose="Show CLI usage examples",
                description="Print grouped usage examples: quick start, daily, weekly, safety.",
                example_commands=["python main.py cli-examples"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="cli-ux-report", category="utility",
                purpose="Generate CLI UX audit report",
                description="Build a CLI UX audit report covering aliases, coverage, and safety.",
                example_commands=["python main.py cli-ux-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="cli-resolve", category="utility",
                purpose="Resolve a command or alias",
                description="Given a name or alias, resolve to canonical command and show details.",
                example_commands=["python main.py cli-resolve daily"],
                safety_level="SAFE_READ_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # data
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="download", category="data",
                purpose="Download market data",
                description="Download daily OHLCV data for all universe tickers.",
                example_commands=["python main.py download --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="import-csv", category="data",
                purpose="Import CSV data files",
                description="Import one or more CSV files into the local data store.",
                example_commands=["python main.py import-csv --path data/raw/"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="data-check", category="data",
                purpose="Check data integrity",
                description="Validate data files for gaps, duplicates, and format issues.",
                example_commands=["python main.py data-check --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="batch-import", category="data",
                purpose="Batch import market data",
                description="Import multiple tickers from a manifest or directory.",
                example_commands=["python main.py batch-import --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="data-audit", category="data",
                purpose="Full data audit",
                description="Comprehensive data audit across all tickers and timeframes.",
                example_commands=["python main.py data-audit --mode real"],
                report_support=True,
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="import-plan", category="data",
                purpose="Generate import plan",
                description="Identify missing data and build an import plan.",
                example_commands=["python main.py import-plan --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="import-xq-export", category="data",
                purpose="Import XQ exported data",
                description="Import data exported from XQ (XueQiu) format.",
                example_commands=["python main.py import-xq-export --path data/xq/"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="batch-import-xq", category="data",
                purpose="Batch import XQ data",
                description="Batch import multiple XQ export files.",
                example_commands=["python main.py batch-import-xq --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="data-freshness", category="data", aliases=["freshness"],
                purpose="Check data freshness",
                description="Report how recently each ticker's data was updated.",
                example_commands=["python main.py data-freshness --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="data-source-status", category="data",
                purpose="Show data source status",
                description="Summary of each data source: last update, row count, coverage.",
                example_commands=["python main.py data-source-status --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # provider
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="provider-status", category="provider", aliases=["provider"],
                purpose="Show provider status",
                description="Quick status summary for all configured data providers.",
                example_commands=["python main.py provider-status --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="provider-health", category="provider",
                purpose="Run provider health check",
                description="Deep health check including connectivity and rate-limit status.",
                example_commands=["python main.py provider-health --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="provider-reliability", category="provider", aliases=["providers"],
                purpose="Provider reliability report",
                description="Compute and report reliability scores for each provider.",
                example_commands=["python main.py provider-reliability --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="provider-auto-fetch", category="provider",
                purpose="Auto-fetch from provider",
                description="Automatically fetch missing data from available providers.",
                example_commands=["python main.py provider-auto-fetch --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="provider-reliability-report", category="provider",
                purpose="Generate provider reliability report",
                description="Generate a Markdown report of provider reliability metrics.",
                example_commands=["python main.py provider-reliability-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
                notes="report subcommand",
            ),
            CLICommand(
                name="api-token-check", category="provider", aliases=["api-check"],
                purpose="Check API token validity",
                description="Validate configured API tokens (no display of full token).",
                example_commands=["python main.py api-token-check --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="api-cache-status", category="provider",
                purpose="Show API cache status",
                description="Report cache hit rates and sizes for each provider.",
                example_commands=["python main.py api-cache-status --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="api-fetch-diagnostics", category="provider", aliases=["api-diag"],
                purpose="API fetch diagnostics",
                description="Detailed fetch diagnostics: latency, errors, retry counts.",
                example_commands=["python main.py api-fetch-diagnostics --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="api-cache-cleanup", category="provider",
                purpose="Clean up API cache",
                description="Remove stale or expired API cache entries.",
                example_commands=["python main.py api-cache-cleanup --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="api-fetch-production-report", category="provider",
                purpose="Generate API fetch production report",
                description="Build a full API fetch productionization report.",
                example_commands=["python main.py api-fetch-production-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # quality
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="data-quality-gate", category="quality", aliases=["dq", "quality"],
                purpose="Run data quality gate",
                description="Run all data quality checks and return a pass/fail gate result.",
                example_commands=["python main.py data-quality-gate --mode real"],
                report_support=True,
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="clean-csv", category="quality",
                purpose="Clean CSV data files",
                description="Normalize and clean raw CSV files in-place.",
                example_commands=["python main.py clean-csv --path data/raw/"],
                safety_level="RESEARCH_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # strategy
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="strategy-preview", category="strategy",
                purpose="Preview strategy signals",
                description="Preview the latest strategy signals without running a backtest.",
                example_commands=["python main.py strategy-preview --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="strategy-knowledge-ingest", category="strategy",
                purpose="Ingest strategy knowledge",
                description="Ingest strategy knowledge documents into the knowledge base.",
                example_commands=["python main.py strategy-knowledge-ingest --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="strategy-knowledge-summary", category="strategy",
                aliases=["strategy-knowledge"],
                purpose="Summarize strategy knowledge base",
                description="Print a summary of the current strategy knowledge base.",
                example_commands=["python main.py strategy-knowledge-summary --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="rule-governance", category="strategy", aliases=["rules"],
                purpose="Run rule governance check",
                description="Audit trading rules for conflicts, redundancy, and coverage.",
                example_commands=["python main.py rule-governance --mode real"],
                report_support=True,
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="tune-rule-weights", category="strategy", aliases=["weights"],
                purpose="Tune rule weights",
                description="Optimize rule weights using recent backtest performance.",
                example_commands=["python main.py tune-rule-weights --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="signal-quality", category="strategy", aliases=["signals"],
                purpose="Assess signal quality",
                description="Evaluate signal quality: hit rate, precision, recall.",
                example_commands=["python main.py signal-quality --mode real"],
                report_support=True,
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="backtest-strategy-knowledge", category="strategy",
                purpose="Backtest with strategy knowledge",
                description="Run a knowledge-guided backtest using strategy knowledge base.",
                example_commands=["python main.py backtest-strategy-knowledge --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # backtest
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="backtest", category="backtest",
                purpose="Run backtest",
                description="Run a standard backtest simulation. No real orders.",
                example_commands=["python main.py backtest --mode real"],
                mode_support=["real", "mock"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="backtest-screener", category="backtest",
                purpose="Run screener backtest",
                description="Backtest the stock screener selection criteria.",
                example_commands=["python main.py backtest-screener --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="backtest-buy-points", category="backtest",
                purpose="Backtest entry buy points",
                description="Validate entry point detection against historical data.",
                example_commands=["python main.py backtest-buy-points --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="backtest-long-term-strategy", category="backtest",
                purpose="Long-term strategy backtest",
                description="Run a long-term multi-year strategy backtest.",
                example_commands=["python main.py backtest-long-term-strategy --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="hardened-backtest", category="backtest",
                purpose="Run hardened backtest",
                description="Run backtest with additional robustness checks and slippage models.",
                example_commands=["python main.py hardened-backtest --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="validate-score", category="backtest",
                purpose="Validate scoring model",
                description="Validate the composite scoring model against test data.",
                example_commands=["python main.py validate-score --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="run-validation-suite", category="backtest",
                purpose="Run full validation suite",
                description="Execute the full regression and validation test suite.",
                example_commands=["python main.py run-validation-suite --mode real"],
                report_support=True,
                safety_level="SIMULATION_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # portfolio
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="paper", category="portfolio",
                purpose="Run paper trading simulation",
                description="Simulate paper trading using latest signals. No real orders.",
                example_commands=["python main.py paper --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="simulate-portfolio", category="portfolio",
                purpose="Simulate portfolio",
                description="Run full portfolio simulation with position sizing and risk control.",
                example_commands=["python main.py simulate-portfolio --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="stock-report", category="portfolio",
                purpose="Generate stock report",
                description="Generate a detailed stock analysis report for a given ticker.",
                example_commands=["python main.py stock-report --ticker 2330 --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # ml
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="ml-feature-catalog", category="ml",
                purpose="Show ML feature catalog",
                description="Print the full catalog of ML features with metadata.",
                example_commands=["python main.py ml-feature-catalog --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="ml-feature-snapshot", category="ml",
                purpose="Snapshot ML features",
                description="Take a point-in-time snapshot of feature values for all tickers.",
                example_commands=["python main.py ml-feature-snapshot --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="ml-labels", category="ml",
                purpose="Generate ML labels",
                description="Generate forward-return labels for supervised learning.",
                example_commands=["python main.py ml-labels --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="ml-build-dataset", category="ml",
                purpose="Build ML training dataset",
                description="Assemble features and labels into a training dataset.",
                example_commands=["python main.py ml-build-dataset --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="ml-leakage-check", category="ml",
                purpose="Check for data leakage",
                description="Scan ML pipeline for temporal data leakage.",
                example_commands=["python main.py ml-leakage-check --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="ml-feature-quality", category="ml",
                purpose="Assess feature quality",
                description="Evaluate feature quality: missing rate, variance, correlation.",
                example_commands=["python main.py ml-feature-quality --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="ml-feature-importance", category="ml",
                purpose="Compute feature importance",
                description="Compute feature importance scores from trained models.",
                example_commands=["python main.py ml-feature-importance --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="ml-feature-store-report", category="ml",
                purpose="Generate feature store report",
                description="Generate a comprehensive ML feature store audit report.",
                example_commands=["python main.py ml-feature-store-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="ml-knowledge-integrate", category="ml",
                purpose="Integrate ML knowledge",
                description="Integrate new knowledge documents into the ML knowledge base.",
                example_commands=["python main.py ml-knowledge-integrate --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="ml-knowledge-leakage-check", category="ml", aliases=["ml-leakage"],
                purpose="Check ML knowledge leakage",
                description="Audit ML knowledge base for temporal leakage or look-ahead bias.",
                example_commands=["python main.py ml-knowledge-leakage-check --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="ml-knowledge-feature-summary", category="ml", aliases=["ml-summary"],
                purpose="Summarize ML knowledge features",
                description="Print a feature-level summary of the ML knowledge base.",
                example_commands=["python main.py ml-knowledge-feature-summary --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="model-monitoring", category="ml",
                purpose="Run model monitoring",
                description="Monitor deployed model performance and drift.",
                example_commands=["python main.py model-monitoring --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="model-monitoring-report", category="ml",
                purpose="Generate model monitoring report",
                description="Generate a Markdown report of model monitoring metrics.",
                example_commands=["python main.py model-monitoring-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="prediction-log", category="ml",
                purpose="View prediction log",
                description="Display recent model prediction logs.",
                example_commands=["python main.py prediction-log --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="prediction-review", category="ml",
                purpose="Review model predictions",
                description="Compare model predictions against actual outcomes.",
                example_commands=["python main.py prediction-review --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="drift-check", category="ml",
                purpose="Check for model/feature drift",
                description="Detect statistical drift in feature distributions.",
                example_commands=["python main.py drift-check --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="signal-degradation", category="ml",
                purpose="Detect signal degradation",
                description="Detect degradation in signal quality over time.",
                example_commands=["python main.py signal-degradation --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="rule-vs-ml", category="ml",
                purpose="Compare rule vs ML signals",
                description="Head-to-head comparison of rule-based vs ML signal performance.",
                example_commands=["python main.py rule-vs-ml --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="model-registry-list", category="ml",
                purpose="List model registry",
                description="List all registered models with metadata.",
                example_commands=["python main.py model-registry-list"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="model-register", category="ml",
                purpose="Register a model",
                description="Register a trained model artifact in the model registry.",
                example_commands=["python main.py model-register --model-id model_001"],
                safety_level="RESEARCH_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # replay
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="intraday-replay", category="replay", aliases=["replay"],
                purpose="Run intraday replay session",
                description="Replay historical intraday data for analysis and training.",
                example_commands=["python main.py intraday-replay --mode real"],
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="intraday-replay-report", category="replay", aliases=["replay-report"],
                purpose="Generate intraday replay report",
                description="Generate a Markdown report for the latest replay session.",
                example_commands=["python main.py intraday-replay-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="replay-session-list", category="replay", aliases=["replay-sessions"],
                purpose="List replay sessions",
                description="List all saved intraday replay sessions.",
                example_commands=["python main.py replay-session-list"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="replay-session-show", category="replay",
                purpose="Show replay session details",
                description="Show details of a specific replay session by ID.",
                example_commands=["python main.py replay-session-show --session-id 001"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="replay-training-summary", category="replay",
                purpose="Summarize replay training",
                description="Aggregate summary of replay training outcomes.",
                example_commands=["python main.py replay-training-summary"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="intraday-pipeline", category="replay",
                purpose="Run intraday pipeline",
                description="Execute the full intraday data processing pipeline.",
                example_commands=["python main.py intraday-pipeline --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="intraday-quality", category="replay",
                purpose="Check intraday data quality",
                description="Quality check for intraday OHLCV data.",
                example_commands=["python main.py intraday-quality --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="intraday-features", category="replay",
                purpose="Compute intraday features",
                description="Compute feature set from intraday OHLCV data.",
                example_commands=["python main.py intraday-features --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="import-intraday", category="replay",
                purpose="Import intraday data",
                description="Import intraday tick or minute-bar data files.",
                example_commands=["python main.py import-intraday --path data/intraday/"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="mock-realtime", category="replay",
                purpose="Mock real-time feed",
                description="Simulate a real-time data feed from historical intraday data.",
                example_commands=["python main.py mock-realtime --mode mock"],
                mode_support=["mock"],
                safety_level="SIMULATION_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # journal
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="journal-add", category="journal",
                purpose="Add journal entry",
                description="Add a research journal entry with notes and tags.",
                example_commands=["python main.py journal-add --text 'Today reviewed MACD signals'"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="journal-list", category="journal", aliases=["notes"],
                purpose="List journal entries",
                description="List recent research journal entries.",
                example_commands=["python main.py journal-list"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="journal-show", category="journal",
                purpose="Show journal entry",
                description="Show full detail of a specific journal entry.",
                example_commands=["python main.py journal-show --id 42"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="journal-review", category="journal",
                purpose="Review journal entries",
                description="Review journal entries by date range or tag.",
                example_commands=["python main.py journal-review --period weekly"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="journal-report", category="journal",
                purpose="Generate journal report",
                description="Generate a Markdown report of journal activity.",
                example_commands=["python main.py journal-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="journal-summary", category="journal", aliases=["journal"],
                purpose="Summarize journal",
                description="Print a concise summary of recent journal entries.",
                example_commands=["python main.py journal-summary"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="journal-link-replay", category="journal",
                purpose="Link journal to replay session",
                description="Associate a journal entry with an intraday replay session.",
                example_commands=["python main.py journal-link-replay --journal-id 42 --session-id 001"],
                safety_level="RESEARCH_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # notification
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="notification-scan", category="notification",
                purpose="Scan for new notifications",
                description="Scan all data and research sources for new alerts.",
                example_commands=["python main.py notification-scan --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="notification-list", category="notification",
                aliases=["notify", "alerts"],
                purpose="List notifications",
                description="List unread and recent notifications.",
                example_commands=["python main.py notification-list"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="notification-report", category="notification",
                purpose="Generate notification report",
                description="Generate a Markdown report of recent notifications.",
                example_commands=["python main.py notification-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="notification-clear-read", category="notification",
                purpose="Mark notifications as read",
                description="Mark all current notifications as read.",
                example_commands=["python main.py notification-clear-read"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="notification-test", category="notification",
                purpose="Test notification system",
                description="Send a test notification to verify the notification pipeline.",
                example_commands=["python main.py notification-test --mode mock"],
                safety_level="SIMULATION_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # review
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="research-review", category="review", aliases=["review-daily"],
                purpose="Run research review",
                description="Run a structured research review. --period daily adds --period daily.",
                example_commands=[
                    "python main.py research-review --mode real --period daily",
                    "python main.py research-review --mode real --period weekly",
                ],
                report_support=True,
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-review-report", category="review",
                purpose="Generate research review report",
                description="Generate a Markdown report for the latest review session.",
                example_commands=["python main.py research-review-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="research-review-summary", category="review",
                purpose="Summarize research review",
                description="Print a concise summary of the latest review session.",
                example_commands=["python main.py research-review-summary"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-review-actions", category="review",
                purpose="List review action items",
                description="List outstanding action items from recent research reviews.",
                example_commands=["python main.py research-review-actions"],
                safety_level="SAFE_READ_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # coach
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="research-coach", category="coach", aliases=["coach-daily"],
                purpose="Run research coach",
                description="Run the AI research coach. --period daily adds daily suggestions.",
                example_commands=["python main.py research-coach --mode real --period daily"],
                report_support=True,
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-coach-report", category="coach",
                purpose="Generate coach report",
                description="Generate a Markdown coach report.",
                example_commands=["python main.py research-coach-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="research-coach-summary", category="coach",
                purpose="Summarize coach session",
                description="Print a concise summary of the latest coach session.",
                example_commands=["python main.py research-coach-summary"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-coach-checklist", category="coach",
                purpose="Show coach checklist",
                description="Display today's research coach checklist.",
                example_commands=["python main.py research-coach-checklist"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-coach-replay-plan", category="coach",
                purpose="Generate replay training plan",
                description="Generate a coach-guided intraday replay training plan.",
                example_commands=["python main.py research-coach-replay-plan"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-coach-rule-queue", category="coach",
                purpose="Show coach rule queue",
                description="List rules queued for review by the research coach.",
                example_commands=["python main.py research-coach-rule-queue"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-coach-data-repair", category="coach",
                purpose="Data repair suggestions",
                description="Coach-generated suggestions for data repair and gap-filling.",
                example_commands=["python main.py research-coach-data-repair --mode real"],
                safety_level="SAFE_READ_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # workflow
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="research-workflow", category="workflow",
                aliases=["workflow-daily", "workflow-weekly"],
                purpose="Run research workflow",
                description=(
                    "Run the full research workflow. "
                    "workflow-daily → --type daily_research; workflow-weekly → --type weekly_review."
                ),
                example_commands=[
                    "python main.py research-workflow --mode real --type daily_research --dry-run",
                    "python main.py research-workflow --mode real --type daily_research",
                    "python main.py research-workflow --mode real --type weekly_review",
                ],
                report_support=True,
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="research-workflow-report", category="workflow",
                purpose="Generate workflow report",
                description="Generate a Markdown report of the latest workflow run.",
                example_commands=["python main.py research-workflow-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="research-workflow-summary", category="workflow",
                purpose="Summarize workflow run",
                description="Print a concise summary of the latest workflow run.",
                example_commands=["python main.py research-workflow-summary"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-workflow-tasks", category="workflow",
                purpose="List workflow tasks",
                description="List all tasks in the current workflow with status.",
                example_commands=["python main.py research-workflow-tasks"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-workflow-package", category="workflow",
                purpose="Package workflow outputs",
                description="Bundle workflow outputs into a versioned package.",
                example_commands=["python main.py research-workflow-package --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="run-research", category="workflow", aliases=["daily", "quick"],
                purpose="Run research pipeline",
                description=(
                    "Run the full research pipeline. "
                    "daily → --profile daily --mode real; quick → --profile quick --mode real."
                ),
                example_commands=[
                    "python main.py run-research --profile daily --mode real",
                    "python main.py run-research --profile quick --mode real",
                ],
                report_support=True,
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="daily-workflow", category="workflow",
                purpose="Run daily workflow",
                description="Run the standard daily research workflow shortcut.",
                example_commands=["python main.py daily-workflow --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="update-data", category="workflow",
                purpose="Update all data sources",
                description="Trigger a full data update across all configured sources.",
                example_commands=["python main.py update-data --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # os_planning
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="research-os-report", category="os_planning",
                purpose="Generate research OS report",
                description="Generate a comprehensive research OS planning report.",
                example_commands=["python main.py research-os-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="research-os-modules", category="os_planning",
                purpose="List research OS modules",
                description="List all registered research OS modules and their status.",
                example_commands=["python main.py research-os-modules"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-os-cli", category="os_planning",
                purpose="Show research OS CLI coverage",
                description="Audit CLI coverage for each research OS module.",
                example_commands=["python main.py research-os-cli"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-os-gui", category="os_planning",
                purpose="Show research OS GUI coverage",
                description="Audit GUI panel coverage for each research OS module.",
                example_commands=["python main.py research-os-gui"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="research-os-safety", category="os_planning",
                purpose="Run research OS safety audit",
                description="Verify safety invariants across all research OS modules.",
                example_commands=["python main.py research-os-safety"],
                safety_level="SAFE_READ_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # release
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="stable-release-check", category="release", aliases=["release-check"],
                purpose="Run stable release check",
                description="Verify all stability gates before a release.",
                example_commands=["python main.py stable-release-check --mode real"],
                report_support=True,
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="regression-suite", category="release", aliases=["regress"],
                purpose="Run regression test suite",
                description="Run full regression test suite; --quick for fast subset.",
                example_commands=[
                    "python main.py regression-suite --mode real",
                    "python main.py regression-suite --mode real --quick",
                ],
                report_support=True,
                safety_level="SIMULATION_ONLY",
            ),
            CLICommand(
                name="stable-release-report", category="release",
                purpose="Generate stable release report",
                description="Generate a Markdown stable release readiness report.",
                example_commands=["python main.py stable-release-report --mode real"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="auto-report", category="release",
                purpose="Auto-generate all reports",
                description="Automatically generate all scheduled reports.",
                example_commands=["python main.py auto-report --mode real --profile daily"],
                report_support=True,
                safety_level="REPORT_ONLY",
            ),
            CLICommand(
                name="scheduler-run", category="release",
                purpose="Run scheduler manually",
                description="Trigger a manual scheduler run for all pending tasks.",
                example_commands=["python main.py scheduler-run --mode real"],
                safety_level="RESEARCH_ONLY",
            ),
            CLICommand(
                name="scheduler-status", category="release",
                purpose="Show scheduler status",
                description="Display current scheduler status and next run times.",
                example_commands=["python main.py scheduler-status"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="scheduler-list", category="release",
                purpose="List scheduled tasks",
                description="List all scheduled tasks with cron expressions.",
                example_commands=["python main.py scheduler-list"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="scheduler-next-runs", category="release",
                purpose="Show next scheduled runs",
                description="Show next N scheduled run times for each task.",
                example_commands=["python main.py scheduler-next-runs --n 5"],
                safety_level="SAFE_READ_ONLY",
            ),
            CLICommand(
                name="scheduler-init-config", category="release",
                purpose="Initialize scheduler config",
                description="Initialize or reset the scheduler configuration file.",
                example_commands=["python main.py scheduler-init-config"],
                safety_level="RESEARCH_ONLY",
            ),
        ]:
            self.register(entry)

        # ----------------------------------------------------------------
        # gui
        # ----------------------------------------------------------------
        for entry in [
            CLICommand(
                name="cockpit", category="gui", aliases=["gui", "dashboard", "open"],
                purpose="Launch the Cockpit GUI",
                description="Open the TW Quant Cockpit PySide6 GUI dashboard.",
                example_commands=["python main.py cockpit --mode real"],
                mode_support=["real", "mock"],
                safety_level="GUI_ONLY",
            ),
            CLICommand(
                name="open-cockpit", category="gui",
                purpose="Open cockpit (alias entry)",
                description="Alternative command to open the Cockpit GUI.",
                example_commands=["python main.py open-cockpit --mode real"],
                safety_level="GUI_ONLY",
            ),
            CLICommand(
                name="ui", category="gui",
                purpose="Launch UI",
                description="Launch the TW Quant Cockpit UI (same as cockpit).",
                example_commands=["python main.py ui --mode real"],
                safety_level="GUI_ONLY",
            ),
        ]:
            self.register(entry)

        logger.debug(
            "CLICommandRegistry built: %d commands across %d categories.",
            len(self._commands),
            len({c.category for c in self._commands.values()}),
        )


# =============================================================================
# v1.4.3.1 Provider Command Registry
# Central registry for v1.3.9–v1.4.3 provider commands.
# Eliminates divergence between _build_parser() registration and command_map dispatch.
# [!] Research Only. No Real Orders. Not Investment Advice.
# =============================================================================

import argparse as _argparse
from dataclasses import dataclass as _dataclass, field as _field
from typing import Any as _Any, Callable as _Callable, Dict as _Dict, List as _List, Optional as _Optional, Set as _Set

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
REGISTRY_VERSION = "1.4.3.1"


@_dataclass
class CommandArg:
    flags: _List[str]
    kwargs: _Dict[str, _Any] = _field(default_factory=dict)


@_dataclass
class CommandSpec:
    name: str
    handler_name: str   # name of cmd_* function in main.py
    help: str
    group: str
    introduced_in: str
    research_only: bool = True
    hidden: bool = False
    aliases: _List[str] = _field(default_factory=list)
    args: _List[CommandArg] = _field(default_factory=list)
    capability: str = ""
    safety_classification: str = "RESEARCH_ONLY"


# ---------------------------------------------------------------------------
# v1.3.9 Research Foundation commands
# ---------------------------------------------------------------------------
_RESEARCH_FOUNDATION_COMMANDS: _List[CommandSpec] = [
    CommandSpec(
        name="research-foundation-health",
        handler_name="cmd_research_foundation_health",
        help="[v1.3.9] Research Foundation health check. Research Only.",
        group="research_foundation",
        introduced_in="1.3.9",
    ),
    CommandSpec(
        name="research-foundation-stable-check",
        handler_name="cmd_research_foundation_stable_check",
        help="[v1.3.9] Research Foundation stable checklist. Research Only.",
        group="research_foundation",
        introduced_in="1.3.9",
    ),
    CommandSpec(
        name="research-foundation-release-gate",
        handler_name="cmd_research_foundation_release_gate",
        help="[v1.3.9] Research Foundation release gate. Research Only.",
        group="research_foundation",
        introduced_in="1.3.9",
    ),
    CommandSpec(
        name="research-foundation-summary",
        handler_name="cmd_research_foundation_summary",
        help="[v1.3.9] Research Foundation summary. Research Only.",
        group="research_foundation",
        introduced_in="1.3.9",
    ),
    CommandSpec(
        name="cli-registration-health",
        handler_name="cmd_cli_registration_health",
        help="[v1.4.3.1] CLI registration consistency health. Research Only.",
        group="research_foundation",
        introduced_in="1.4.3.1",
    ),
]

# ---------------------------------------------------------------------------
# v1.4.0 TWSE commands
# ---------------------------------------------------------------------------
_TWSE_COMMANDS: _List[CommandSpec] = [
    CommandSpec(name="twse-health", handler_name="cmd_twse_health",
                help="[v1.4.0] TWSE provider health. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-endpoints", handler_name="cmd_twse_endpoints",
                help="[v1.4.0] TWSE endpoint registry. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-capabilities", handler_name="cmd_twse_capabilities",
                help="[v1.4.0] TWSE capability matrix. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-security", handler_name="cmd_twse_security",
                help="[v1.4.0] TWSE security info. Research Only.", group="twse", introduced_in="1.4.0",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="twse-security-list", handler_name="cmd_twse_security_list",
                help="[v1.4.0] TWSE security list. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-fetch-security-master", handler_name="cmd_twse_fetch_security_master",
                help="[v1.4.0] TWSE fetch security master. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-daily", handler_name="cmd_twse_daily",
                help="[v1.4.0] TWSE daily OHLCV. Research Only.", group="twse", introduced_in="1.4.0",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="twse-fetch-daily", handler_name="cmd_twse_fetch_daily",
                help="[v1.4.0] TWSE fetch daily OHLCV. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-market-summary", handler_name="cmd_twse_market_summary",
                help="[v1.4.0] TWSE market summary. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-institutional", handler_name="cmd_twse_institutional",
                help="[v1.4.0] TWSE institutional flows. Research Only.", group="twse", introduced_in="1.4.0",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="twse-margin", handler_name="cmd_twse_margin",
                help="[v1.4.0] TWSE margin trading. Research Only.", group="twse", introduced_in="1.4.0",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="twse-index", handler_name="cmd_twse_index",
                help="[v1.4.0] TWSE index data. Research Only.", group="twse", introduced_in="1.4.0",
                args=[CommandArg(flags=["--index-id"], kwargs={"dest": "index_id", "default": None})]),
    CommandSpec(name="twse-calendar", handler_name="cmd_twse_calendar",
                help="[v1.4.0] TWSE trading calendar. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-corporate-actions", handler_name="cmd_twse_corporate_actions",
                help="[v1.4.0] TWSE corporate actions. Research Only.", group="twse", introduced_in="1.4.0",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="twse-coverage", handler_name="cmd_twse_coverage",
                help="[v1.4.0] TWSE coverage summary. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-lineage", handler_name="cmd_twse_lineage",
                help="[v1.4.0] TWSE data lineage. Research Only.", group="twse", introduced_in="1.4.0",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="twse-cache-status", handler_name="cmd_twse_cache_status",
                help="[v1.4.0] TWSE cache status. Research Only.", group="twse", introduced_in="1.4.0"),
    CommandSpec(name="twse-provider-report", handler_name="cmd_twse_provider_report",
                help="[v1.4.0] TWSE provider report. Research Only.", group="twse", introduced_in="1.4.0"),
]

# ---------------------------------------------------------------------------
# v1.4.1 TPEx commands
# ---------------------------------------------------------------------------
_TPEX_COMMANDS: _List[CommandSpec] = [
    CommandSpec(name="tpex-health", handler_name="cmd_tpex_health",
                help="[v1.4.1] TPEx provider health. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-endpoints", handler_name="cmd_tpex_endpoints",
                help="[v1.4.1] TPEx endpoint registry. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-capabilities", handler_name="cmd_tpex_capabilities",
                help="[v1.4.1] TPEx capability matrix. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-security", handler_name="cmd_tpex_security",
                help="[v1.4.1] TPEx security info. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="tpex-security-list", handler_name="cmd_tpex_security_list",
                help="[v1.4.1] TPEx security list. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-fetch-security-master", handler_name="cmd_tpex_fetch_security_master",
                help="[v1.4.1] TPEx fetch security master. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-daily", handler_name="cmd_tpex_daily",
                help="[v1.4.1] TPEx daily OHLCV. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="tpex-fetch-daily", handler_name="cmd_tpex_fetch_daily",
                help="[v1.4.1] TPEx fetch daily OHLCV. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-market-summary", handler_name="cmd_tpex_market_summary",
                help="[v1.4.1] TPEx market summary. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-institutional", handler_name="cmd_tpex_institutional",
                help="[v1.4.1] TPEx institutional flows. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="tpex-margin", handler_name="cmd_tpex_margin",
                help="[v1.4.1] TPEx margin trading. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="tpex-index", handler_name="cmd_tpex_index",
                help="[v1.4.1] TPEx index data. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--index-id"], kwargs={"dest": "index_id", "default": None})]),
    CommandSpec(name="tpex-calendar", handler_name="cmd_tpex_calendar",
                help="[v1.4.1] TPEx trading calendar. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-suspensions", handler_name="cmd_tpex_suspensions",
                help="[v1.4.1] TPEx suspensions. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-corporate-actions", handler_name="cmd_tpex_corporate_actions",
                help="[v1.4.1] TPEx corporate actions. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="tpex-valuation", handler_name="cmd_tpex_valuation",
                help="[v1.4.1] TPEx valuation ratios. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="tpex-coverage", handler_name="cmd_tpex_coverage",
                help="[v1.4.1] TPEx coverage summary. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-lineage", handler_name="cmd_tpex_lineage",
                help="[v1.4.1] TPEx data lineage. Research Only.", group="tpex", introduced_in="1.4.1",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="tpex-cache-status", handler_name="cmd_tpex_cache_status",
                help="[v1.4.1] TPEx cache status. Research Only.", group="tpex", introduced_in="1.4.1"),
    CommandSpec(name="tpex-provider-report", handler_name="cmd_tpex_provider_report",
                help="[v1.4.1] TPEx provider report. Research Only.", group="tpex", introduced_in="1.4.1"),
]

# ---------------------------------------------------------------------------
# v1.4.2 MOPS commands
# ---------------------------------------------------------------------------
_MOPS_COMMANDS: _List[CommandSpec] = [
    CommandSpec(name="mops-health", handler_name="cmd_mops_health",
                help="[v1.4.2] MOPS provider health. Research Only.", group="mops", introduced_in="1.4.2"),
    CommandSpec(name="mops-endpoints", handler_name="cmd_mops_endpoints",
                help="[v1.4.2] MOPS endpoint registry. Research Only.", group="mops", introduced_in="1.4.2"),
    CommandSpec(name="mops-capabilities", handler_name="cmd_mops_capabilities",
                help="[v1.4.2] MOPS capability matrix. Research Only.", group="mops", introduced_in="1.4.2"),
    CommandSpec(name="mops-company-profile", handler_name="cmd_mops_company_profile",
                help="[v1.4.2] MOPS company profile. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="mops-revenue", handler_name="cmd_mops_revenue",
                help="[v1.4.2] MOPS monthly revenue. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--year-month"], kwargs={"dest": "year_month", "default": None})]),
    CommandSpec(name="mops-balance-sheet", handler_name="cmd_mops_balance_sheet",
                help="[v1.4.2] MOPS balance sheet. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--year"], kwargs={"default": None}),
                      CommandArg(flags=["--quarter"], kwargs={"default": None})]),
    CommandSpec(name="mops-income-statement", handler_name="cmd_mops_income_statement",
                help="[v1.4.2] MOPS income statement. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--year"], kwargs={"default": None}),
                      CommandArg(flags=["--quarter"], kwargs={"default": None})]),
    CommandSpec(name="mops-cash-flow", handler_name="cmd_mops_cash_flow",
                help="[v1.4.2] MOPS cash flow. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--year"], kwargs={"default": None}),
                      CommandArg(flags=["--quarter"], kwargs={"default": None})]),
    CommandSpec(name="mops-material-info", handler_name="cmd_mops_material_info",
                help="[v1.4.2] MOPS material information. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="mops-investor-conference", handler_name="cmd_mops_investor_conference",
                help="[v1.4.2] MOPS investor conference. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="mops-xbrl-index", handler_name="cmd_mops_xbrl_index",
                help="[v1.4.2] MOPS XBRL index. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--year"], kwargs={"default": None})]),
    CommandSpec(name="mops-revision-lineage", handler_name="cmd_mops_revision_lineage",
                help="[v1.4.2] MOPS revision lineage. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="mops-point-in-time", handler_name="cmd_mops_point_in_time",
                help="[v1.4.2] MOPS point-in-time query. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--as-of"], kwargs={"dest": "as_of", "default": None})]),
    CommandSpec(name="mops-derived-metrics", handler_name="cmd_mops_derived_metrics",
                help="[v1.4.2] MOPS derived metrics. Research Only.", group="mops", introduced_in="1.4.2",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="mops-coverage", handler_name="cmd_mops_coverage",
                help="[v1.4.2] MOPS coverage summary. Research Only.", group="mops", introduced_in="1.4.2"),
    CommandSpec(name="mops-cache-status", handler_name="cmd_mops_cache_status",
                help="[v1.4.2] MOPS cache status. Research Only.", group="mops", introduced_in="1.4.2"),
    CommandSpec(name="mops-provider-report", handler_name="cmd_mops_provider_report",
                help="[v1.4.2] MOPS provider report. Research Only.", group="mops", introduced_in="1.4.2"),
]

# ---------------------------------------------------------------------------
# v1.4.3 data.gov.tw commands
# ---------------------------------------------------------------------------
_DATA_GOV_TW_COMMANDS: _List[CommandSpec] = [
    CommandSpec(name="data-gov-tw-health", handler_name="cmd_data_gov_tw_health",
                help="[v1.4.3] data.gov.tw provider health. Research Only.", group="data_gov_tw", introduced_in="1.4.3"),
    CommandSpec(name="data-gov-tw-capabilities", handler_name="cmd_data_gov_tw_capabilities",
                help="[v1.4.3] data.gov.tw capability matrix. Research Only.", group="data_gov_tw", introduced_in="1.4.3"),
    CommandSpec(name="data-gov-tw-catalog", handler_name="cmd_data_gov_tw_catalog",
                help="[v1.4.3] data.gov.tw dataset catalog. Research Only.", group="data_gov_tw", introduced_in="1.4.3"),
    CommandSpec(name="data-gov-tw-search", handler_name="cmd_data_gov_tw_search",
                help="[v1.4.3] data.gov.tw search datasets. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--keyword"], kwargs={"default": None})]),
    CommandSpec(name="data-gov-tw-dataset", handler_name="cmd_data_gov_tw_dataset",
                help="[v1.4.3] data.gov.tw dataset info. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-resources", handler_name="cmd_data_gov_tw_resources",
                help="[v1.4.3] data.gov.tw dataset resources. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-allowlist", handler_name="cmd_data_gov_tw_allowlist",
                help="[v1.4.3] data.gov.tw allowlist. Research Only.", group="data_gov_tw", introduced_in="1.4.3"),
    CommandSpec(name="data-gov-tw-allowlist-check", handler_name="cmd_data_gov_tw_allowlist_check",
                help="[v1.4.3] data.gov.tw allowlist check. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-license", handler_name="cmd_data_gov_tw_license",
                help="[v1.4.3] data.gov.tw license validation. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-schema", handler_name="cmd_data_gov_tw_schema",
                help="[v1.4.3] data.gov.tw schema contract. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-revisions", handler_name="cmd_data_gov_tw_revisions",
                help="[v1.4.3] data.gov.tw revision tracking. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-fetch", handler_name="cmd_data_gov_tw_fetch",
                help="[v1.4.3] data.gov.tw fetch dataset. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None}),
                      CommandArg(flags=["--execute"], kwargs={"action": "store_true", "default": False})]),
    CommandSpec(name="data-gov-tw-records", handler_name="cmd_data_gov_tw_records",
                help="[v1.4.3] data.gov.tw stored records. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-as-of", handler_name="cmd_data_gov_tw_as_of",
                help="[v1.4.3] data.gov.tw point-in-time query. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None}),
                      CommandArg(flags=["--as-of"], kwargs={"dest": "as_of", "default": None})]),
    CommandSpec(name="data-gov-tw-observations", handler_name="cmd_data_gov_tw_observations",
                help="[v1.4.3] data.gov.tw government observations. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--domain"], kwargs={"default": None})]),
    CommandSpec(name="data-gov-tw-coverage", handler_name="cmd_data_gov_tw_coverage",
                help="[v1.4.3] data.gov.tw coverage summary. Research Only.", group="data_gov_tw", introduced_in="1.4.3"),
    CommandSpec(name="data-gov-tw-lineage", handler_name="cmd_data_gov_tw_lineage",
                help="[v1.4.3] data.gov.tw data lineage. Research Only.", group="data_gov_tw", introduced_in="1.4.3",
                args=[CommandArg(flags=["--dataset-id"], kwargs={"dest": "dataset_id", "default": None})]),
    CommandSpec(name="data-gov-tw-cache-status", handler_name="cmd_data_gov_tw_cache_status",
                help="[v1.4.3] data.gov.tw cache status. Research Only.", group="data_gov_tw", introduced_in="1.4.3"),
    CommandSpec(name="data-gov-tw-provider-report", handler_name="cmd_data_gov_tw_provider_report",
                help="[v1.4.3] data.gov.tw provider report. Research Only.", group="data_gov_tw", introduced_in="1.4.3"),
]

# ---------------------------------------------------------------------------
# v1.4.4 FinMind commands
# ---------------------------------------------------------------------------
_FINMIND_COMMANDS: _List[CommandSpec] = [
    CommandSpec(name="finmind-health", handler_name="cmd_finmind_health",
                help="[v1.4.4] FinMind adapter health. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-capabilities", handler_name="cmd_finmind_capabilities",
                help="[v1.4.4] FinMind capabilities. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-datasets", handler_name="cmd_finmind_datasets",
                help="[v1.4.4] FinMind dataset registry. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-dataset", handler_name="cmd_finmind_dataset",
                help="[v1.4.4] FinMind dataset info. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--dataset"], kwargs={"default": None})]),
    CommandSpec(name="finmind-schema", handler_name="cmd_finmind_schema",
                help="[v1.4.4] FinMind schema. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--dataset"], kwargs={"default": None})]),
    CommandSpec(name="finmind-schema-drift", handler_name="cmd_finmind_schema_drift",
                help="[v1.4.4] FinMind schema drift. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--dataset"], kwargs={"default": None})]),
    CommandSpec(name="finmind-quota", handler_name="cmd_finmind_quota",
                help="[v1.4.4] FinMind quota status. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-auth-status", handler_name="cmd_finmind_auth_status",
                help="[v1.4.4] FinMind auth status. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-plan", handler_name="cmd_finmind_plan",
                help="[v1.4.4] FinMind fetch plan (dry-run). Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--dataset"], kwargs={"default": None}),
                      CommandArg(flags=["--data-id"], kwargs={"dest": "data_id", "default": None}),
                      CommandArg(flags=["--start-date"], kwargs={"dest": "start_date", "default": None}),
                      CommandArg(flags=["--end-date"], kwargs={"dest": "end_date", "default": None})]),
    CommandSpec(name="finmind-fetch", handler_name="cmd_finmind_fetch",
                help="[v1.4.4] FinMind fetch dataset. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--dataset"], kwargs={"default": None}),
                      CommandArg(flags=["--data-id"], kwargs={"dest": "data_id", "default": None}),
                      CommandArg(flags=["--start-date"], kwargs={"dest": "start_date", "default": None}),
                      CommandArg(flags=["--end-date"], kwargs={"dest": "end_date", "default": None}),
                      CommandArg(flags=["--execute"], kwargs={"action": "store_true", "default": False})]),
    CommandSpec(name="finmind-price", handler_name="cmd_finmind_price",
                help="[v1.4.4] FinMind price data. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--start-date"], kwargs={"dest": "start_date", "default": None}),
                      CommandArg(flags=["--end-date"], kwargs={"dest": "end_date", "default": None})]),
    CommandSpec(name="finmind-institutional", handler_name="cmd_finmind_institutional",
                help="[v1.4.4] FinMind institutional flows. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--start-date"], kwargs={"dest": "start_date", "default": None}),
                      CommandArg(flags=["--end-date"], kwargs={"dest": "end_date", "default": None})]),
    CommandSpec(name="finmind-margin", handler_name="cmd_finmind_margin",
                help="[v1.4.4] FinMind margin data. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--symbol"], kwargs={"default": None}),
                      CommandArg(flags=["--start-date"], kwargs={"dest": "start_date", "default": None}),
                      CommandArg(flags=["--end-date"], kwargs={"dest": "end_date", "default": None})]),
    CommandSpec(name="finmind-compare-primary", handler_name="cmd_finmind_compare_primary",
                help="[v1.4.4] FinMind vs primary comparison. Research Only.", group="finmind", introduced_in="1.4.4",
                args=[CommandArg(flags=["--dataset"], kwargs={"default": None}),
                      CommandArg(flags=["--symbol"], kwargs={"default": None})]),
    CommandSpec(name="finmind-conflicts", handler_name="cmd_finmind_conflicts",
                help="[v1.4.4] FinMind conflict report. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-coverage", handler_name="cmd_finmind_coverage",
                help="[v1.4.4] FinMind coverage summary. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-lineage", handler_name="cmd_finmind_lineage",
                help="[v1.4.4] FinMind data lineage. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-cache-status", handler_name="cmd_finmind_cache_status",
                help="[v1.4.4] FinMind cache status. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-adapter-report", handler_name="cmd_finmind_adapter_report",
                help="[v1.4.4] FinMind adapter report. Research Only.", group="finmind", introduced_in="1.4.4"),
    CommandSpec(name="finmind-pit-status", handler_name="cmd_finmind_pit_status",
                help="[v1.4.4] FinMind point-in-time status for a dataset. Research Only.", group="finmind",
                introduced_in="1.4.4",
                args=[CommandArg(flags=["--dataset"], kwargs={"default": None})]),
]

# ---------------------------------------------------------------------------
# v1.4.5 Source Governance commands
# ---------------------------------------------------------------------------
_SOURCE_GOVERNANCE_COMMANDS: _List[CommandSpec] = [
    CommandSpec(name="source-governance-health", handler_name="cmd_source_governance_health",
                help="[v1.4.5] Source governance health. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="source-lineage-sources", handler_name="cmd_source_lineage_sources",
                help="[v1.4.5] List source identities. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="source-lineage-show", handler_name="cmd_source_lineage_show",
                help="[v1.4.5] Show lineage record. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--lineage-id"], kwargs={"dest": "lineage_id", "default": None})]),
    CommandSpec(name="source-lineage-trace", handler_name="cmd_source_lineage_trace",
                help="[v1.4.5] Trace lineage to root. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--lineage-id"], kwargs={"dest": "lineage_id", "default": None})]),
    CommandSpec(name="source-lineage-record", handler_name="cmd_source_lineage_record",
                help="[v1.4.5] Get record lineage. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None}),
                      CommandArg(flags=["--record-key"], kwargs={"dest": "record_key", "default": None})]),
    CommandSpec(name="source-lineage-incomplete", handler_name="cmd_source_lineage_incomplete",
                help="[v1.4.5] List incomplete lineage. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="request-ledger-list", handler_name="cmd_request_ledger_list",
                help="[v1.4.5] List request ledger. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="request-ledger-show", handler_name="cmd_request_ledger_show",
                help="[v1.4.5] Show request. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--request-id"], kwargs={"dest": "request_id", "default": None})]),
    CommandSpec(name="fetch-run-list", handler_name="cmd_fetch_run_list",
                help="[v1.4.5] List fetch runs. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="fetch-run-show", handler_name="cmd_fetch_run_show",
                help="[v1.4.5] Show fetch run. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--fetch-run-id"], kwargs={"dest": "fetch_run_id", "default": None})]),
    CommandSpec(name="rate-limit-status", handler_name="cmd_rate_limit_status",
                help="[v1.4.5] Rate limit status. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="rate-limit-host", handler_name="cmd_rate_limit_host",
                help="[v1.4.5] Host rate limit state. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--host"], kwargs={"default": None})]),
    CommandSpec(name="rate-limit-provider", handler_name="cmd_rate_limit_provider",
                help="[v1.4.5] Provider rate limit state. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None})]),
    CommandSpec(name="rate-limit-endpoint", handler_name="cmd_rate_limit_endpoint",
                help="[v1.4.5] Endpoint rate policy. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None}),
                      CommandArg(flags=["--endpoint-family"], kwargs={"dest": "endpoint_family", "default": None})]),
    CommandSpec(name="request-budget-status", handler_name="cmd_request_budget_status",
                help="[v1.4.5] Request budget status. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="quota-evidence-list", handler_name="cmd_quota_evidence_list",
                help="[v1.4.5] List quota evidence. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="retry-evidence-list", handler_name="cmd_retry_evidence_list",
                help="[v1.4.5] List retry evidence. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="cache-lineage-show", handler_name="cmd_cache_lineage_show",
                help="[v1.4.5] Show cache lineage. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--cache-entry-id"], kwargs={"dest": "cache_entry_id", "default": None})]),
    CommandSpec(name="conflict-lineage-list", handler_name="cmd_conflict_lineage_list",
                help="[v1.4.5] List conflict lineage. Research Only.", group="source_governance", introduced_in="1.4.5"),
    CommandSpec(name="conflict-lineage-show", handler_name="cmd_conflict_lineage_show",
                help="[v1.4.5] Show conflict. Research Only.", group="source_governance", introduced_in="1.4.5",
                args=[CommandArg(flags=["--conflict-id"], kwargs={"dest": "conflict_id", "default": None})]),
    CommandSpec(name="source-governance-report", handler_name="cmd_source_governance_report",
                help="[v1.4.5] Source governance report. Research Only.", group="source_governance", introduced_in="1.4.5"),
]

# ---------------------------------------------------------------------------
# v1.4.6 Provider Quality Gates commands
# ---------------------------------------------------------------------------
_PROVIDER_QUALITY_GATES_COMMANDS: _List[CommandSpec] = [
    CommandSpec(name="provider-quality-health", handler_name="cmd_provider_quality_health",
                help="[v1.4.6] Provider quality gates health check. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-gates", handler_name="cmd_provider_quality_gates",
                help="[v1.4.6] Show provider quality gate registry. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-evaluate-provider", handler_name="cmd_provider_quality_evaluate_provider",
                help="[v1.4.6] Evaluate quality gates for a provider. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-evaluate-dataset", handler_name="cmd_provider_quality_evaluate_dataset",
                help="[v1.4.6] Evaluate quality gates for a dataset. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None}),
                      CommandArg(flags=["--dataset"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-evaluate-endpoint", handler_name="cmd_provider_quality_evaluate_endpoint",
                help="[v1.4.6] Evaluate quality gates for an endpoint. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--endpoint"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-evaluate-fetch-run", handler_name="cmd_provider_quality_evaluate_fetch_run",
                help="[v1.4.6] Evaluate quality gates for a fetch run. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--fetch-run-id"], kwargs={"dest": "fetch_run_id", "default": None})]),
    CommandSpec(name="provider-quality-profiles", handler_name="cmd_provider_quality_profiles",
                help="[v1.4.6] List all provider quality profiles. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-datasets", handler_name="cmd_provider_quality_datasets",
                help="[v1.4.6] List dataset quality profiles. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-quarantine-list", handler_name="cmd_provider_quality_quarantine_list",
                help="[v1.4.6] List quarantined providers. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-blocked-list", handler_name="cmd_provider_quality_blocked_list",
                help="[v1.4.6] List blocked providers. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-decision", handler_name="cmd_provider_quality_decision",
                help="[v1.4.6] Show quality decision details. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--decision-id"], kwargs={"dest": "decision_id", "default": None})]),
    CommandSpec(name="provider-quality-explain", handler_name="cmd_provider_quality_explain",
                help="[v1.4.6] Explain a quality decision. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--decision-id"], kwargs={"dest": "decision_id", "default": None})]),
    CommandSpec(name="provider-quality-audit", handler_name="cmd_provider_quality_audit",
                help="[v1.4.6] View quality decision audit trail. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-score", handler_name="cmd_provider_quality_score",
                help="[v1.4.6] Show quality score for a provider. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-policy", handler_name="cmd_provider_quality_policy",
                help="[v1.4.6] Show quality policy for a provider. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-formal-research", handler_name="cmd_provider_quality_formal_research",
                help="[v1.4.6] Check formal research eligibility. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None}),
                      CommandArg(flags=["--dataset"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-backtest", handler_name="cmd_provider_quality_backtest",
                help="[v1.4.6] Check backtest input eligibility. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--provider"], kwargs={"default": None}),
                      CommandArg(flags=["--dataset"], kwargs={"default": None})]),
    CommandSpec(name="provider-quality-safety", handler_name="cmd_provider_quality_safety",
                help="[v1.4.6] Run safety gate check. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-report", handler_name="cmd_provider_quality_report",
                help="[v1.4.6] Generate provider quality gates report. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6"),
    CommandSpec(name="provider-quality-gate-detail", handler_name="cmd_provider_quality_gate_detail",
                help="[v1.4.6] Show quality gate definition detail. Research Only.",
                group="provider_quality_gates", introduced_in="1.4.6",
                args=[CommandArg(flags=["--gate-id"], kwargs={"dest": "gate_id", "default": None})]),
]

# Combined list of all provider commands
PROVIDER_COMMANDS: _List[CommandSpec] = (
    _RESEARCH_FOUNDATION_COMMANDS
    + _TWSE_COMMANDS
    + _TPEX_COMMANDS
    + _MOPS_COMMANDS
    + _DATA_GOV_TW_COMMANDS
    + _FINMIND_COMMANDS
    + _SOURCE_GOVERNANCE_COMMANDS
    + _PROVIDER_QUALITY_GATES_COMMANDS
)


def get_all_commands() -> _List[CommandSpec]:
    """Return all provider commands."""
    return list(PROVIDER_COMMANDS)


def get_command(name: str) -> _Optional[CommandSpec]:
    """Return a CommandSpec by exact name, or None."""
    for spec in PROVIDER_COMMANDS:
        if spec.name == name:
            return spec
    return None


def get_commands_by_group(group: str) -> _List[CommandSpec]:
    """Return all commands in the given group."""
    return [s for s in PROVIDER_COMMANDS if s.group == group]


def get_formal_command_names() -> _Set[str]:
    """Return the set of all formal command names."""
    return {s.name for s in PROVIDER_COMMANDS}


def register_all_commands(subparsers) -> None:
    """Register all provider commands in argparse subparsers. Call from _build_parser()."""
    for spec in PROVIDER_COMMANDS:
        p = subparsers.add_parser(spec.name, help=spec.help)
        for arg in spec.args:
            p.add_argument(*arg.flags, **arg.kwargs)


def build_command_map(handlers: _Dict[str, _Any]) -> _Dict[str, _Any]:
    """Build command_map from handler lookup. handlers: {handler_name: callable}"""
    result = {}
    for spec in PROVIDER_COMMANDS:
        handler = handlers.get(spec.handler_name)
        if handler is not None:
            result[spec.name] = handler
    return result


def validate_command_registry(parser_commands: _Set[str], handler_map: _Dict[str, _Any]) -> _Dict[str, _Any]:
    """Validate consistency between parser and handlers."""
    formal = get_formal_command_names()
    registered_and_dispatched = formal & parser_commands & set(handler_map.keys())
    registered_without_handler = (formal & parser_commands) - set(handler_map.keys())
    handler_without_registration = (formal & set(handler_map.keys())) - parser_commands

    seen: _Set[str] = set()
    duplicates: _Set[str] = set()
    for s in PROVIDER_COMMANDS:
        if s.name in seen:
            duplicates.add(s.name)
        seen.add(s.name)

    errors = []
    if registered_without_handler:
        errors.append(f"Registered but no handler: {sorted(registered_without_handler)}")
    if handler_without_registration:
        errors.append(f"Handler but not registered: {sorted(handler_without_registration)}")
    if duplicates:
        errors.append(f"Duplicate commands: {sorted(duplicates)}")

    return {
        "REGISTERED_AND_DISPATCHED": sorted(registered_and_dispatched),
        "REGISTERED_WITHOUT_HANDLER": sorted(registered_without_handler),
        "HANDLER_WITHOUT_REGISTRATION": sorted(handler_without_registration),
        "DUPLICATE_REGISTRATION": sorted(duplicates),
        "DUPLICATE_ALIAS": [],
        "formal_count": len(formal),
        "parser_count": len(parser_commands & formal),
        "handler_count": len(set(handler_map.keys()) & formal),
        "errors": errors,
        "is_consistent": len(errors) == 0,
    }


def list_cli_commands(group: _Optional[str] = None) -> _List[_Dict[str, str]]:
    cmds = PROVIDER_COMMANDS if group is None else get_commands_by_group(group)
    return [{"name": c.name, "group": c.group, "introduced_in": c.introduced_in, "help": c.help} for c in cmds]

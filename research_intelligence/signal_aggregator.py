"""research_intelligence/signal_aggregator.py — ResearchSignalAggregator v0.7.0.

Reads summary CSV outputs from all Research OS modules and produces ResearchSignal list.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
[!] No broker connection. No order submission. No auto-trading.
"""
from __future__ import annotations

import csv
import logging
import os
import uuid
from datetime import datetime
from typing import List, Optional

from research_intelligence.research_intelligence_schema import (
    ResearchSignal,
    SRC_DATA_COVERAGE, SRC_REPORT_PACK, SRC_REPLAY_TRAINING,
    SRC_PORTFOLIO_JOURNAL, SRC_RULE_GOVERNANCE, SRC_STRATEGY_KNOWLEDGE,
    SRC_REGRESSION, SRC_STABLE_RELEASE,
    CAT_DATA_GAP, CAT_REPORT_GAP, CAT_REPLAY_MISTAKE, CAT_JOURNAL_PATTERN,
    CAT_RULE_REVIEW, CAT_STRATEGY_RESEARCH, CAT_SYSTEM_RISK, CAT_REGRESSION_WARN,
    CAT_STABLE_NOTE, CAT_PROVIDER_LIMIT, CAT_TRAINING_TASK,
    PRI_P0, PRI_P1, PRI_P2, PRI_P3,
    SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW, SEV_INFO,
    ACT_FIX_DATA, ACT_GENERATE_REPORT, ACT_REVIEW_RULE, ACT_PRACTICE_REPLAY,
    ACT_REVIEW_JOURNAL, ACT_RUN_BACKTEST, ACT_RUN_REGRESSION, ACT_READ_REPORT,
    ACT_WAIT,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _sig_id() -> str:
    return f"SIG-{uuid.uuid4().hex[:8].upper()}"


def _read_latest_csv(path: str) -> List[dict]:
    """Read all rows from a CSV; return [] if missing or unreadable."""
    if not os.path.isfile(path):
        return []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as exc:
        logger.warning("[SignalAggregator] CSV read error %s: %s", path, exc)
        return []


class ResearchSignalAggregator:
    """Collects ResearchSignals from all Research OS modules.

    Reads CSV summary files — never modifies data, never submits orders,
    never connects to brokers.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/research_intelligence",
    ) -> None:
        self._root       = os.path.abspath(project_root) if project_root != "." else BASE_DIR
        self._output_dir = os.path.join(self._root, output_dir) if not os.path.isabs(output_dir) else output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    def _abs(self, *parts: str) -> str:
        return os.path.join(self._root, *parts)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def collect_all(self, mode: str = "real") -> List[ResearchSignal]:
        """Collect signals from all modules. Never raises; graceful fallback."""
        signals: List[ResearchSignal] = []
        collectors = [
            self.collect_data_coverage_signals,
            self.collect_report_pack_signals,
            self.collect_replay_training_signals,
            self.collect_journal_signals,
            self.collect_rule_governance_signals,
            self.collect_strategy_knowledge_signals,
            self.collect_regression_signals,
            self.collect_stable_release_signals,
            # v0.9.0.1 crash reversal integration
            lambda: self._collect_crash_reversal_signals(mode),
        ]
        for collector in collectors:
            try:
                results = collector()
                signals.extend(results)
            except Exception as exc:
                logger.warning("[SignalAggregator] collector %s error: %s", collector.__name__, exc)
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module="signal_aggregator",
                    category=CAT_SYSTEM_RISK,
                    title=f"Collector error: {collector.__name__}",
                    description=str(exc),
                    severity=SEV_LOW,
                    priority=PRI_P3,
                    suggested_action=ACT_READ_REPORT,
                    warning="Collector raised exception; check logs",
                ))
        # v0.7.1: enrich signals with UX fields
        _SAFE_HINT = {
            CAT_DATA_GAP:        "Run data-coverage to scan and fix gaps",
            CAT_REPORT_GAP:      "Run the report generator CLI command",
            CAT_REPLAY_MISTAKE:  "Open replay training and practice identified scenarios",
            CAT_JOURNAL_PATTERN: "Review journal entries for the pattern",
            CAT_RULE_REVIEW:     "Run rule-governance snapshot and review",
            CAT_STRATEGY_RESEARCH: "Run strategy-knowledge-ingest to update knowledge",
            CAT_SYSTEM_RISK:     "Run stable-v060-check to verify system health",
            CAT_TRAINING_TASK:   "Open replay training and complete the drill",
            CAT_PROVIDER_LIMIT:  "Configure provider token in .env (no code change needed)",
            CAT_REGRESSION_WARN: "Run regression-run suite to confirm status",
            CAT_STABLE_NOTE:     "Run stable-v060-check to confirm release health",
        }
        for sig in signals:
            if not sig.display_label:
                sig.display_label = sig.title[:60] if sig.title else ""
            if not sig.user_friendly_reason:
                sig.user_friendly_reason = sig.description[:120] if sig.description else sig.evidence[:120]
            if not sig.safe_action_hint:
                sig.safe_action_hint = _SAFE_HINT.get(sig.category, "Review and take appropriate research action")
        return signals

    # ------------------------------------------------------------------
    # A. Data Coverage
    # ------------------------------------------------------------------

    def collect_data_coverage_signals(self) -> List[ResearchSignal]:
        path = self._abs("data/backtest_results/data_coverage/data_coverage_summary.csv")
        rows = _read_latest_csv(path)
        if not rows:
            return [ResearchSignal(
                signal_id=_sig_id(),
                source_module=SRC_DATA_COVERAGE,
                category=CAT_DATA_GAP,
                title="Data Coverage summary not found",
                description="Run: python main.py data-coverage --mode real",
                severity=SEV_INFO,
                priority=PRI_P3,
                suggested_action=ACT_FIX_DATA,
                suggested_command="python main.py data-coverage --mode real",
            )]
        row = rows[-1]
        signals = []
        try:
            missing_req = int(float(row.get("missing_required_count", 0) or 0))
            env_limited = int(float(row.get("env_limited_count", 0) or 0))
            not_gen     = int(float(row.get("not_generated_count", 0) or 0))
            score       = float(row.get("coverage_score", 0) or 0)

            if missing_req > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_DATA_COVERAGE,
                    category=CAT_DATA_GAP,
                    title=f"Data Coverage: {missing_req} required dataset(s) missing",
                    description=f"Coverage score: {score:.1f}. Required data gaps block research quality.",
                    severity=SEV_HIGH,
                    confidence=0.9,
                    priority=PRI_P0,
                    suggested_action=ACT_FIX_DATA,
                    suggested_command="python main.py data-coverage-gaps",
                    evidence=f"missing_required={missing_req}, score={score:.1f}",
                ))
            if env_limited > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_DATA_COVERAGE,
                    category=CAT_PROVIDER_LIMIT,
                    title=f"Data Coverage: {env_limited} item(s) ENV_LIMITED (token required)",
                    description="Provider token not configured. Set FINMIND_TOKEN or similar.",
                    severity=SEV_MEDIUM,
                    confidence=0.8,
                    priority=PRI_P2,
                    suggested_action=ACT_WAIT,
                    suggested_command="python main.py data-coverage-gaps",
                    evidence=f"env_limited={env_limited}",
                ))
            if not_gen > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_DATA_COVERAGE,
                    category=CAT_REPORT_GAP,
                    title=f"Data Coverage: {not_gen} optional report(s) not generated",
                    description="Run the relevant CLI commands to generate missing optional reports.",
                    severity=SEV_LOW,
                    confidence=0.7,
                    priority=PRI_P2,
                    suggested_action=ACT_GENERATE_REPORT,
                    suggested_command="python main.py data-coverage-gaps",
                    evidence=f"not_generated={not_gen}",
                ))
            if not signals:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_DATA_COVERAGE,
                    category=CAT_DATA_GAP,
                    title=f"Data Coverage healthy — score {score:.1f}/100",
                    description="No required data gaps detected.",
                    severity=SEV_INFO,
                    priority=PRI_P3,
                    suggested_action=ACT_READ_REPORT,
                    evidence=f"coverage_score={score:.1f}",
                ))
        except Exception as exc:
            logger.warning("[SignalAggregator] data_coverage parse error: %s", exc)
        return signals

    # ------------------------------------------------------------------
    # B. Report Pack
    # ------------------------------------------------------------------

    def collect_report_pack_signals(self) -> List[ResearchSignal]:
        # Look for the most recent report pack index
        path = self._abs("data/backtest_results/report_pack")
        signals = []
        try:
            if not os.path.isdir(path):
                return [ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPORT_PACK,
                    category=CAT_REPORT_GAP,
                    title="Report Pack directory not found",
                    description="Run: python main.py report-pack --type full --mode real",
                    severity=SEV_INFO,
                    priority=PRI_P3,
                    suggested_action=ACT_GENERATE_REPORT,
                    suggested_command="python main.py report-pack --type full --mode real",
                )]
            # Find latest manifest
            manifests = []
            for d in os.listdir(path):
                mf = os.path.join(path, d, "manifest.json")
                if os.path.isfile(mf):
                    manifests.append(mf)
            if not manifests:
                return [ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPORT_PACK,
                    category=CAT_REPORT_GAP,
                    title="No report pack manifest found",
                    description="Run report-pack to generate reports.",
                    severity=SEV_MEDIUM,
                    priority=PRI_P2,
                    suggested_action=ACT_GENERATE_REPORT,
                    suggested_command="python main.py report-pack --type full --mode real",
                )]
            import json
            latest = sorted(manifests, reverse=True)[0]
            with open(latest, encoding="utf-8") as f:
                manifest = json.load(f)
            failed   = manifest.get("failed_count", 0)
            missing  = manifest.get("missing_required_count", manifest.get("missing_count", 0))
            status   = manifest.get("status", "")
            if failed > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPORT_PACK,
                    category=CAT_REPORT_GAP,
                    title=f"Report Pack: {failed} report(s) FAILED",
                    description="Reports failed to generate. Investigate errors.",
                    severity=SEV_HIGH,
                    confidence=0.9,
                    priority=PRI_P1,
                    suggested_action=ACT_GENERATE_REPORT,
                    suggested_command="python main.py report-pack --type full --mode real",
                    evidence=f"failed={failed}, status={status}",
                ))
            elif missing > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPORT_PACK,
                    category=CAT_REPORT_GAP,
                    title=f"Report Pack: {missing} required report(s) missing",
                    severity=SEV_HIGH,
                    priority=PRI_P1,
                    suggested_action=ACT_GENERATE_REPORT,
                    suggested_command="python main.py report-pack --type full --mode real",
                    evidence=f"missing_required={missing}",
                ))
            else:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPORT_PACK,
                    category=CAT_REPORT_GAP,
                    title=f"Report Pack status: {status}",
                    description="Optional reports may be missing; required reports OK.",
                    severity=SEV_INFO,
                    priority=PRI_P3,
                    suggested_action=ACT_READ_REPORT,
                    evidence=f"status={status}",
                ))
        except Exception as exc:
            logger.warning("[SignalAggregator] report_pack error: %s", exc)
        return signals

    # ------------------------------------------------------------------
    # C. Replay Training
    # ------------------------------------------------------------------

    def collect_replay_training_signals(self) -> List[ResearchSignal]:
        summary_path = self._abs("data/backtest_results/replay_training/replay_training_summary.csv")
        rows = _read_latest_csv(summary_path)
        if not rows:
            return [ResearchSignal(
                signal_id=_sig_id(),
                source_module=SRC_REPLAY_TRAINING,
                category=CAT_TRAINING_TASK,
                title="No replay training sessions found",
                description="Start a replay training session to build tape reading skills.",
                severity=SEV_MEDIUM,
                priority=PRI_P2,
                suggested_action=ACT_PRACTICE_REPLAY,
                suggested_command="python main.py replay-training-summary",
            )]
        row = rows[-1]
        signals = []
        try:
            score    = float(row.get("latest_score", 0) or 0)
            mistakes = int(float(row.get("mistakes_count", 0) or 0))

            if score < 50:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPLAY_TRAINING,
                    category=CAT_REPLAY_MISTAKE,
                    title=f"Replay score low: {score:.1f}/100 — focused practice needed",
                    description="Score below 50. Review entry quality, stop discipline, and fake breakout recognition.",
                    severity=SEV_HIGH,
                    confidence=0.85,
                    priority=PRI_P1,
                    suggested_action=ACT_PRACTICE_REPLAY,
                    suggested_command="python main.py replay-training-report --mode real",
                    evidence=f"latest_score={score:.1f}, mistakes={mistakes}",
                ))
            elif score < 70:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPLAY_TRAINING,
                    category=CAT_REPLAY_MISTAKE,
                    title=f"Replay score moderate: {score:.1f}/100 — room for improvement",
                    description="Focus on weakest scoring components.",
                    severity=SEV_MEDIUM,
                    priority=PRI_P2,
                    suggested_action=ACT_PRACTICE_REPLAY,
                    suggested_command="python main.py replay-ai-review --session-id latest",
                    evidence=f"latest_score={score:.1f}, mistakes={mistakes}",
                ))
            else:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPLAY_TRAINING,
                    category=CAT_TRAINING_TASK,
                    title=f"Replay score good: {score:.1f}/100",
                    description="Maintain practice frequency and review drills.",
                    severity=SEV_INFO,
                    priority=PRI_P3,
                    suggested_action=ACT_READ_REPORT,
                    evidence=f"latest_score={score:.1f}, mistakes={mistakes}",
                ))

            if mistakes >= 3:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REPLAY_TRAINING,
                    category=CAT_REPLAY_MISTAKE,
                    title=f"Replay: {mistakes} mistake(s) in latest session",
                    description="Review mistake patterns and practice targeted drills.",
                    severity=SEV_HIGH if mistakes >= 5 else SEV_MEDIUM,
                    confidence=0.8,
                    priority=PRI_P1 if mistakes >= 5 else PRI_P2,
                    suggested_action=ACT_PRACTICE_REPLAY,
                    suggested_command="python main.py replay-training-drills --session-id latest",
                    evidence=f"mistakes_count={mistakes}",
                ))
        except Exception as exc:
            logger.warning("[SignalAggregator] replay_training parse error: %s", exc)
        return signals

    # ------------------------------------------------------------------
    # D. Portfolio Journal
    # ------------------------------------------------------------------

    def collect_journal_signals(self) -> List[ResearchSignal]:
        path = self._abs("data/backtest_results/journal/journal_summary.csv")
        rows = _read_latest_csv(path)
        if not rows:
            return [ResearchSignal(
                signal_id=_sig_id(),
                source_module=SRC_PORTFOLIO_JOURNAL,
                category=CAT_JOURNAL_PATTERN,
                title="No portfolio journal entries found",
                description="Add research journal entries to track trading decisions.",
                severity=SEV_INFO,
                priority=PRI_P3,
                suggested_action=ACT_REVIEW_JOURNAL,
                suggested_command="python main.py journal-summary",
            )]
        row = rows[-1]
        signals = []
        try:
            process_quality = float(row.get("avg_process_quality", row.get("quality_score", 5)) or 5)
            if process_quality < 4:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_PORTFOLIO_JOURNAL,
                    category=CAT_JOURNAL_PATTERN,
                    title=f"Journal process quality low: {process_quality:.1f}/10",
                    description="Review recent journal entries for recurring process errors.",
                    severity=SEV_HIGH,
                    priority=PRI_P1,
                    suggested_action=ACT_REVIEW_JOURNAL,
                    suggested_command="python main.py journal-review",
                    evidence=f"avg_process_quality={process_quality:.1f}",
                ))
            else:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_PORTFOLIO_JOURNAL,
                    category=CAT_JOURNAL_PATTERN,
                    title=f"Journal quality: {process_quality:.1f}/10",
                    description="Journal review looks healthy.",
                    severity=SEV_INFO,
                    priority=PRI_P3,
                    suggested_action=ACT_READ_REPORT,
                    evidence=f"avg_process_quality={process_quality:.1f}",
                ))
        except Exception as exc:
            logger.warning("[SignalAggregator] journal parse error: %s", exc)
        return signals

    # ------------------------------------------------------------------
    # E. Rule Governance
    # ------------------------------------------------------------------

    def collect_rule_governance_signals(self) -> List[ResearchSignal]:
        path = self._abs("data/backtest_results/rule_governance/rule_governance_summary.csv")
        rows = _read_latest_csv(path)
        if not rows:
            return [ResearchSignal(
                signal_id=_sig_id(),
                source_module=SRC_RULE_GOVERNANCE,
                category=CAT_RULE_REVIEW,
                title="Rule governance summary not found",
                description="Run rule-governance to snapshot rule confidence.",
                severity=SEV_INFO,
                priority=PRI_P3,
                suggested_action=ACT_REVIEW_RULE,
                suggested_command="python main.py rule-governance --mode real --snapshot",
            )]
        row = rows[-1]
        signals = []
        try:
            low_conf = int(float(row.get("low_confidence_count", 0) or 0))
            deprecated = int(float(row.get("deprecated_count", 0) or 0))
            candidates = int(float(row.get("candidate_count", 0) or 0))

            if deprecated > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_RULE_GOVERNANCE,
                    category=CAT_RULE_REVIEW,
                    title=f"Rule Governance: {deprecated} deprecated rule(s) need review",
                    severity=SEV_HIGH,
                    priority=PRI_P1,
                    suggested_action=ACT_REVIEW_RULE,
                    suggested_command="python main.py rule-governance --mode real --snapshot",
                    evidence=f"deprecated={deprecated}",
                ))
            if low_conf > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_RULE_GOVERNANCE,
                    category=CAT_RULE_REVIEW,
                    title=f"Rule Governance: {low_conf} low-confidence rule(s)",
                    severity=SEV_MEDIUM,
                    priority=PRI_P1,
                    suggested_action=ACT_REVIEW_RULE,
                    suggested_command="python main.py rule-governance --mode real --snapshot",
                    evidence=f"low_confidence={low_conf}",
                ))
            if candidates > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_RULE_GOVERNANCE,
                    category=CAT_RULE_REVIEW,
                    title=f"Rule Governance: {candidates} transcript candidate rule(s) pending review",
                    severity=SEV_MEDIUM,
                    priority=PRI_P2,
                    suggested_action=ACT_REVIEW_RULE,
                    suggested_command="python main.py strategy-knowledge-summary",
                    evidence=f"candidates={candidates}",
                ))
        except Exception as exc:
            logger.warning("[SignalAggregator] rule_governance parse error: %s", exc)
        return signals

    # ------------------------------------------------------------------
    # F. Strategy Knowledge
    # ------------------------------------------------------------------

    def collect_strategy_knowledge_signals(self) -> List[ResearchSignal]:
        path = self._abs("data/backtest_results/strategy_knowledge/strategy_knowledge_summary.csv")
        rows = _read_latest_csv(path)
        if not rows:
            return []  # not critical if missing
        row = rows[-1]
        signals = []
        try:
            new_candidates = int(float(row.get("new_candidate_count", row.get("candidates", 0)) or 0))
            if new_candidates > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_STRATEGY_KNOWLEDGE,
                    category=CAT_STRATEGY_RESEARCH,
                    title=f"Strategy Knowledge: {new_candidates} new candidate rule(s) from transcripts",
                    description="Review and backtest new strategy candidates.",
                    severity=SEV_MEDIUM,
                    priority=PRI_P2,
                    suggested_action=ACT_REVIEW_RULE,
                    suggested_command="python main.py strategy-knowledge-summary",
                    evidence=f"new_candidates={new_candidates}",
                ))
        except Exception as exc:
            logger.warning("[SignalAggregator] strategy_knowledge parse error: %s", exc)
        return signals

    # ------------------------------------------------------------------
    # G. Regression
    # ------------------------------------------------------------------

    def collect_regression_signals(self) -> List[ResearchSignal]:
        path = self._abs("data/backtest_results/regression/regression_summary.csv")
        rows = _read_latest_csv(path)
        if not rows:
            return []
        row = rows[-1]
        signals = []
        try:
            failed   = int(float(row.get("failed_count", row.get("failed", 0)) or 0))
            warnings = int(float(row.get("warning_count", row.get("warnings", 0)) or 0))
            if failed > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REGRESSION,
                    category=CAT_SYSTEM_RISK,
                    title=f"Regression: {failed} test(s) FAILED",
                    description="System reliability is at risk. Investigate and fix failing tests.",
                    severity=SEV_CRITICAL,
                    confidence=0.95,
                    priority=PRI_P0,
                    suggested_action=ACT_RUN_REGRESSION,
                    suggested_command="python main.py regression-run --suite full --mode real",
                    evidence=f"failed={failed}, warnings={warnings}",
                ))
            elif warnings > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_REGRESSION,
                    category=CAT_REGRESSION_WARN,
                    title=f"Regression: {warnings} warning(s)",
                    description="Some regression tests have warnings. Review before release.",
                    severity=SEV_MEDIUM,
                    priority=PRI_P2,
                    suggested_action=ACT_RUN_REGRESSION,
                    suggested_command="python main.py regression-run --suite quick --mode real",
                    evidence=f"warnings={warnings}",
                ))
        except Exception as exc:
            logger.warning("[SignalAggregator] regression parse error: %s", exc)
        return signals

    # ------------------------------------------------------------------
    # v0.9.0.1 Crash Reversal
    # ------------------------------------------------------------------

    def _collect_crash_reversal_signals(self, mode: str = "real") -> List[ResearchSignal]:
        """Informational signals about crash reversal pack availability.

        [!] Research Only. No Real Orders. No BUY/SELL/ORDER output.
        """
        try:
            from strategy_filters.crash_reversal_strategy_pack import CrashReversalStrategyPack
            _crsp = CrashReversalStrategyPack()
            _cr = _crsp.evaluate_market({})  # empty context → UNKNOWN/default results
            signals = []
            signals.append(ResearchSignal(
                signal_id=_sig_id(),
                source_module="crash_reversal_strategy_pack",
                category=CAT_STRATEGY_RESEARCH,
                title="Crash Reversal Strategy Pack v0.9.0.1 registered",
                description=(
                    "CrashReversalStrategyPack is available. "
                    "6 candidate rules loaded (NEEDS_REVIEW). "
                    "Research Only. No Real Orders."
                ),
                severity=SEV_INFO,
                priority=PRI_P3,
                suggested_action=ACT_REVIEW_RULE,
                suggested_command="python main.py rule-governance --mode real --snapshot",
                evidence="crash_reversal_pack=available, rules=6, status=NEEDS_REVIEW",
            ))
            crash_cause = _cr.get("crash_cause", "UNKNOWN") if _cr else "UNKNOWN"
            signals.append(ResearchSignal(
                signal_id=_sig_id(),
                source_module="crash_reversal_strategy_pack",
                category=CAT_RULE_REVIEW,
                title=f"Crash Reversal: current crash_cause={crash_cause}",
                description=(
                    "Crash cause classification from empty-context evaluation. "
                    "Provide real market context for meaningful output."
                ),
                severity=SEV_INFO,
                priority=PRI_P3,
                suggested_action=ACT_GENERATE_REPORT,
                evidence=f"crash_cause={crash_cause}",
            ))
            return signals
        except Exception as exc:
            logger.debug("[SignalAggregator] _collect_crash_reversal_signals: %s", exc)
            return []

    # ------------------------------------------------------------------
    # H. Stable Release
    # ------------------------------------------------------------------

    def collect_stable_release_signals(self) -> List[ResearchSignal]:
        try:
            from stable_release.capability_matrix import StableCapabilityMatrix
            matrix = StableCapabilityMatrix()
            summary = matrix.summarize()
            total    = summary.get("total", 0)
            stable   = summary.get("stable_count", 0)
            blocked  = summary.get("blocked_count", 0)
            signals = []
            if blocked > 0:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_STABLE_RELEASE,
                    category=CAT_SYSTEM_RISK,
                    title=f"Stable Release: {blocked} capability/capabilities BLOCKED",
                    description="Review capability matrix for blocked items.",
                    severity=SEV_HIGH,
                    priority=PRI_P1,
                    suggested_action=ACT_RUN_REGRESSION,
                    suggested_command="python main.py stable-v060-check --mode real",
                    evidence=f"total={total}, stable={stable}, blocked={blocked}",
                ))
            else:
                signals.append(ResearchSignal(
                    signal_id=_sig_id(),
                    source_module=SRC_STABLE_RELEASE,
                    category=CAT_STABLE_NOTE,
                    title=f"Stable Release: {stable}/{total} capabilities STABLE",
                    description="Capability matrix healthy.",
                    severity=SEV_INFO,
                    priority=PRI_P3,
                    suggested_action=ACT_READ_REPORT,
                    suggested_command="python main.py stable-v060-capabilities",
                    evidence=f"total={total}, stable={stable}",
                ))
            return signals
        except Exception as exc:
            logger.warning("[SignalAggregator] stable_release error: %s", exc)
            return []

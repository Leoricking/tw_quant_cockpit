"""
ml/knowledge_leakage_checker.py — KnowledgeLeakageChecker (v0.4.2.1).

Checks transcript-derived knowledge features for data leakage patterns.

Leakage types:
  POST_EVENT_KNOWLEDGE     — transcript published after training sample dates
  TIMING_ESTIMATED         — announcement_date_is_estimated=True for fundamentals
  LONG_CYCLE_RISK          — long-cycle/crash-watch view used as short-term label
  PATTERN_INCOMPLETE       — M-top/head-shoulders before pattern_confirmed_date
  UNVALIDATED_CANDIDATE    — rule candidate, not yet back-tested

Output status: CLEAN / WARNING / LEAKAGE_RISK / BLOCKED
Output per-feature: feature_id, leakage_type, severity, reason, recommendation

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Leakage type constants
LEAKAGE_POST_EVENT          = "POST_EVENT_KNOWLEDGE"
LEAKAGE_TIMING_ESTIMATED    = "TIMING_ESTIMATED"
LEAKAGE_LONG_CYCLE_RISK     = "LONG_CYCLE_RISK"
LEAKAGE_PATTERN_INCOMPLETE  = "PATTERN_INCOMPLETE"
LEAKAGE_UNVALIDATED_CANDIDATE = "UNVALIDATED_CANDIDATE"
LEAKAGE_UNKNOWN             = "UNKNOWN_LEAKAGE"

SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_WARNING  = "WARNING"
SEVERITY_INFO     = "INFO"

STATUS_CLEAN        = "CLEAN"
STATUS_WARNING      = "WARNING"
STATUS_LEAKAGE_RISK = "LEAKAGE_RISK"
STATUS_BLOCKED      = "BLOCKED"


class KnowledgeLeakageChecker:
    """
    Checks transcript-derived knowledge features for data leakage.

    Covers:
      1. Fundamental timing (EPS/revenue/margin → announcement_date required)
      2. Transcript publication date (POST_EVENT_KNOWLEDGE)
      3. Long-cycle crash-watch (LONG_CYCLE_RISK — not for short-term labels)
      4. Pattern conditions (PATTERN_INCOMPLETE — needs pattern_confirmed_date)
      5. Unvalidated rule candidates (UNVALIDATED_CANDIDATE)

    [!] ML Research Only. No Real Orders.
    """

    read_only: bool = True
    no_real_orders: bool = True

    def __init__(self):
        self._findings: List[dict] = []

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def check_features(self, features: List[dict]) -> dict:
        """
        Check list of feature metadata dicts for leakage.

        Returns dict with:
            status, findings, findings_by_feature, summary
        """
        self._findings = []
        findings_by_feature: Dict[str, List[dict]] = {}

        for feat in features:
            fid = feat.get("feature_id", "unknown")
            feat_findings = self._check_one(feat)
            if feat_findings:
                findings_by_feature[fid] = feat_findings
                self._findings.extend(feat_findings)

        # Overall status
        critical = [f for f in self._findings if f.get("severity") == SEVERITY_CRITICAL]
        warnings = [f for f in self._findings if f.get("severity") == SEVERITY_WARNING]

        if critical:
            status = STATUS_BLOCKED
        elif warnings:
            status = STATUS_LEAKAGE_RISK
        elif self._findings:
            status = STATUS_WARNING
        else:
            status = STATUS_CLEAN

        return {
            "status":              status,
            "findings":            self._findings,
            "findings_by_feature": findings_by_feature,
            "summary":             self._build_summary(),
            "total_findings":      len(self._findings),
            "critical_count":      len(critical),
            "warning_count":       len(warnings),
            "blocked_features":    [f.get("feature_id") for f in critical],
            "auto_enabled_count":  0,  # always
        }

    # ------------------------------------------------------------------
    # Per-feature check
    # ------------------------------------------------------------------

    def _check_one(self, feat: dict) -> List[dict]:
        findings: List[dict] = []
        fid          = feat.get("feature_id", "unknown")
        leakage_note = feat.get("leakage_note", "")
        feature_type = feat.get("feature_type", "")
        timeframe    = feat.get("timeframe", "")
        source_cat   = feat.get("source_category", "")
        name         = feat.get("feature_name", fid)
        desc         = feat.get("description", "")

        # 1. Long-cycle risk → not for short-term labels
        if (timeframe == "cycle"
                or feature_type == "regime_flag"
                or "LONG_CYCLE" in leakage_note.upper()):
            findings.append({
                "feature_id":   fid,
                "leakage_type": LEAKAGE_LONG_CYCLE_RISK,
                "severity":     SEVERITY_WARNING,
                "reason":       (
                    f"'{name}' is a long-cycle / regime feature. "
                    "Must NOT be used as short-term return label. "
                    "Regime/cycle metadata only."
                ),
                "recommendation": (
                    "Store as metadata/cycle note only. "
                    "not_for_short_term_label=True. "
                    "Do not include in model training labels."
                ),
            })

        # 2. Fundamental timing leakage
        if "TIMING_ESTIMATED" in leakage_note.upper():
            findings.append({
                "feature_id":   fid,
                "leakage_type": LEAKAGE_TIMING_ESTIMATED,
                "severity":     SEVERITY_WARNING,
                "reason":       (
                    f"'{name}' uses fundamental data where "
                    "announcement_date_is_estimated=True. "
                    "Actual announcement date is unknown — timing leakage risk."
                ),
                "recommendation": (
                    "Use MOPSFinancialParser timing_quality=ACTUAL rows only. "
                    "Filter out rows with announcement_date_is_estimated=True."
                ),
            })

        # 3. Pattern incomplete (M-top, head-shoulders)
        if "PATTERN_INCOMPLETE" in leakage_note.upper():
            findings.append({
                "feature_id":   fid,
                "leakage_type": LEAKAGE_PATTERN_INCOMPLETE,
                "severity":     SEVERITY_CRITICAL,
                "reason":       (
                    f"'{name}' requires a completed top/reversal pattern. "
                    "Using a pattern before pattern_confirmed_date = future leakage."
                ),
                "recommendation": (
                    "Only use this feature AFTER pattern_confirmed_date. "
                    "Exclude from training rows before pattern completion date."
                ),
            })

        # 4. Post-event knowledge (rule/avoid candidates with unvalidated note)
        if "POST_EVENT_KNOWLEDGE" in leakage_note.upper():
            findings.append({
                "feature_id":   fid,
                "leakage_type": LEAKAGE_POST_EVENT,
                "severity":     SEVERITY_WARNING,
                "reason":       (
                    f"'{name}' is a rule/avoid candidate derived from a transcript. "
                    "Transcript publication date may be after training sample dates — "
                    "POST_EVENT_KNOWLEDGE risk."
                ),
                "recommendation": (
                    "Verify transcript saved_at date is before all training sample dates. "
                    "If not, exclude from training set for those dates."
                ),
            })

        # 5. Unvalidated rule candidates
        if source_cat == "rule_candidate":
            findings.append({
                "feature_id":   fid,
                "leakage_type": LEAKAGE_UNVALIDATED_CANDIDATE,
                "severity":     SEVERITY_INFO,
                "reason":       (
                    f"'{name}' is a rule candidate from transcript only. "
                    "Not yet empirically validated — cannot be used as a training feature."
                ),
                "recommendation": (
                    "Run backtest validation before enabling. "
                    "readiness must reach PARTIAL or READY before use."
                ),
            })

        return findings

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _build_summary(self) -> dict:
        by_type: Dict[str, int] = {}
        by_severity: Dict[str, int] = {}
        for f in self._findings:
            lt = f.get("leakage_type", "UNKNOWN")
            sv = f.get("severity", "INFO")
            by_type[lt]     = by_type.get(lt, 0) + 1
            by_severity[sv] = by_severity.get(sv, 0) + 1

        recs = []
        lt_set = set(by_type.keys())
        if LEAKAGE_LONG_CYCLE_RISK in lt_set:
            recs.append("Exclude long-cycle / regime features from short-term model labels")
        if LEAKAGE_TIMING_ESTIMATED in lt_set:
            recs.append("Filter fundamental features to timing_quality=ACTUAL rows only")
        if LEAKAGE_PATTERN_INCOMPLETE in lt_set:
            recs.append("Require pattern_confirmed_date before using pattern-based features")
        if LEAKAGE_POST_EVENT in lt_set:
            recs.append("Verify transcript saved_at dates vs training sample date range")
        if LEAKAGE_UNVALIDATED_CANDIDATE in lt_set:
            recs.append("Run backtest validation on rule candidates before enabling")

        return {
            "total_findings":   len(self._findings),
            "by_leakage_type":  by_type,
            "by_severity":      by_severity,
            "recommendations":  recs,
            "auto_enabled_count": 0,
        }

    def build_readiness_report(self, features: List[dict], check_result: dict) -> dict:
        """Build a combined leakage + readiness summary for reporting."""
        findings_by_feature = check_result.get("findings_by_feature", {})
        rows = []
        for feat in features:
            fid = feat.get("feature_id", "")
            feat_findings = findings_by_feature.get(fid, [])
            worst_severity = ""
            leakage_types = []
            for f in feat_findings:
                sv = f.get("severity", "")
                lt = f.get("leakage_type", "")
                if lt:
                    leakage_types.append(lt)
                if sv == SEVERITY_CRITICAL:
                    worst_severity = SEVERITY_CRITICAL
                elif sv == SEVERITY_WARNING and worst_severity != SEVERITY_CRITICAL:
                    worst_severity = SEVERITY_WARNING
                elif sv == SEVERITY_INFO and not worst_severity:
                    worst_severity = SEVERITY_INFO

            rows.append({
                "feature_id":    fid,
                "feature_name":  feat.get("feature_name", ""),
                "readiness":     feat.get("readiness", ""),
                "leakage_types": "; ".join(leakage_types),
                "worst_severity": worst_severity,
                "leakage_count": len(feat_findings),
                "auto_enabled":  False,
            })
        return {
            "features": rows,
            "total":    len(rows),
        }

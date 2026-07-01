"""
paper_trading/multi_session/fixture_registry_v1661.py
Formal fixture registry for Multi-session Coordination v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker. No Production Capability.
[!] Deterministic. No network. No file mutation. Side-effect free.

All 80 fixtures are registered here as the canonical source of truth for
fixture existence, identity, path, category, purpose, and usage reference.
"""
from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

VERSION = "1.6.6.1"
REGISTRY_VERSION = "1661"
FIXTURE_DIR = "tests/fixtures/multi_session"

VALID_PURPOSES = {
    "scenario_primary",
    "negative_case",
    "edge_case",
    "governance_validation",
    "recovery_case",
    "conflict_matrix",
    "integration",
    "metrics",
    "governance",
}

VALID_CATEGORIES = {
    "checkpoint_recovery",
    "coordination",
    "capital_risk",
    "event_ordering",
    "lifecycle",
    "lock_lease",
    "priority_fairness",
    "registration",
    "resource",
    "symbol_strategy",
    "metrics",
    "panel",
    "scorecard",
    "report",
    "integration",
}


@dataclass
class FixtureEntry:
    fixture_id: str
    filename: str
    category: str
    purpose: str
    description: str
    referenced_by: List[str] = field(default_factory=list)

    @property
    def path(self) -> str:
        return os.path.join(FIXTURE_DIR, self.filename)

    def is_referenced(self) -> bool:
        return len(self.referenced_by) > 0


# ─── Canonical registry of all 80 fixtures ────────────────────────────────────

_REGISTRY_ENTRIES: List[FixtureEntry] = [
    # Checkpoint & Recovery (6)
    FixtureEntry("chk_collision", "chk_collision.json", "checkpoint_recovery", "conflict_matrix",
                 "Checkpoint collision when two sessions write same slot",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("chk_create", "chk_create.json", "checkpoint_recovery", "scenario_primary",
                 "Per-session checkpoint created with hash",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("chk_hash", "chk_hash.json", "checkpoint_recovery", "scenario_primary",
                 "Checkpoint hash verification passes for unmodified checkpoint",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("chk_partial_failure", "chk_partial_failure.json", "checkpoint_recovery", "recovery_case",
                 "Partial recovery failure: s1 ok, s2 fails",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("chk_rec_collision", "chk_rec_collision.json", "checkpoint_recovery", "conflict_matrix",
                 "Recovery collision when two sessions recover to same slot",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("chk_recovery", "chk_recovery.json", "checkpoint_recovery", "scenario_primary",
                 "Recovery plan created and executed from checkpoint",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Coordination (3)
    FixtureEntry("coord_basic", "coord_basic.json", "coordination", "scenario_primary",
                 "Basic coordination: 2 sessions admitted with no conflicts",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("coord_block", "coord_block.json", "coordination", "negative_case",
                 "Coordination block: capital overallocation causes 3rd session block",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("coord_with_conflict", "coord_with_conflict.json", "coordination", "conflict_matrix",
                 "Coordination with symbol overlap conflict",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Capital & Risk (8)
    FixtureEntry("cr_aggregate", "cr_aggregate.json", "capital_risk", "scenario_primary",
                 "Aggregate risk computed across 4 sessions",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("cr_concentration", "cr_concentration.json", "capital_risk", "edge_case",
                 "Risk concentration warned when 3 sessions concentrated in same sector",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("cr_no_real_capital", "cr_no_real_capital.json", "capital_risk", "governance_validation",
                 "Confirms no real capital movement in paper trading mode",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("cr_over_alloc", "cr_over_alloc.json", "capital_risk", "negative_case",
                 "Capital over-allocation blocked when request exceeds available",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("cr_partial", "cr_partial.json", "capital_risk", "edge_case",
                 "Partial capital grant when both requests cannot be fully satisfied",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("cr_priority_alloc", "cr_priority_alloc.json", "capital_risk", "scenario_primary",
                 "Priority-based capital allocation gives more to higher priority",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("cr_risk_exceed", "cr_risk_exceed.json", "capital_risk", "negative_case",
                 "Risk budget exceeded when allocated risk surpasses limit",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("cr_within_budget", "cr_within_budget.json", "capital_risk", "scenario_primary",
                 "Capital allocation within total budget succeeds",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Event Ordering (9)
    FixtureEntry("eo_barrier_all", "eo_barrier_all.json", "event_ordering", "scenario_primary",
                 "Cross-session ALL_OF barrier requires all 3 sessions to arrive",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("eo_barrier_quorum", "eo_barrier_quorum.json", "event_ordering", "scenario_primary",
                 "QUORUM barrier releases when 2 of 3 sessions arrive",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("eo_dedup", "eo_dedup.json", "event_ordering", "edge_case",
                 "Duplicate event with same event_id is deduplicated",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("eo_late_event", "eo_late_event.json", "event_ordering", "edge_case",
                 "Late event detected when timestamp behind watermark",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("eo_monotonic", "eo_monotonic.json", "event_ordering", "scenario_primary",
                 "Global event sequences are monotonically increasing",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("eo_out_of_order", "eo_out_of_order.json", "event_ordering", "negative_case",
                 "Out-of-order event detected",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("eo_same_ts", "eo_same_ts.json", "event_ordering", "edge_case",
                 "Same-timestamp events use deterministic tie-break",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("eo_seq_gap", "eo_seq_gap.json", "event_ordering", "negative_case",
                 "Sequence gap detected",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("event_full_sequence", "event_full_sequence.json", "event_ordering", "integration",
                 "Full event sequence: 5 events with monotonic global sequence",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Lifecycle (10)
    FixtureEntry("lc_cancelled", "lc_cancelled.json", "lifecycle", "scenario_primary",
                 "CANCELLED is terminal with no further transitions",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lc_completed_run", "lc_completed_run.json", "lifecycle", "negative_case",
                 "COMPLETED to RUNNING is blocked (terminal state)",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lc_created_registered", "lc_created_registered.json", "lifecycle", "scenario_primary",
                 "Valid CREATED to REGISTERED transition",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lc_degraded", "lc_degraded.json", "lifecycle", "edge_case",
                 "DEGRADED state requires verification before RUNNING",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lc_failed_run", "lc_failed_run.json", "lifecycle", "negative_case",
                 "FAILED to RUNNING is blocked",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lc_invalid_direct_run", "lc_invalid_direct_run.json", "lifecycle", "negative_case",
                 "Invalid direct CREATED to RUNNING is blocked",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lc_pause_resume", "lc_pause_resume.json", "lifecycle", "scenario_primary",
                 "PAUSED to READY transition requires verification",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lc_recovering", "lc_recovering.json", "lifecycle", "recovery_case",
                 "RECOVERING to READY with successful verification",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("lifecycle_full_cycle", "lifecycle_full_cycle.json", "lifecycle", "integration",
                 "Full lifecycle: CREATED through COMPLETED",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Lock & Lease (8)
    FixtureEntry("ll_excl_acquire", "ll_excl_acquire.json", "lock_lease", "scenario_primary",
                 "Exclusive lock acquired by s1",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ll_excl_conflict", "ll_excl_conflict.json", "lock_lease", "conflict_matrix",
                 "Exclusive lock conflict: s1 holds, s2 blocked",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ll_lease_expiry", "ll_lease_expiry.json", "lock_lease", "edge_case",
                 "Lease expiry invalidates lock after TTL",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ll_ordering", "ll_ordering.json", "lock_lease", "scenario_primary",
                 "Consistent lock ordering prevents deadlock",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ll_owner_validate", "ll_owner_validate.json", "lock_lease", "negative_case",
                 "Owner validation prevents s2 from releasing s1's lock",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ll_renew", "ll_renew.json", "lock_lease", "scenario_primary",
                 "Lease renewal extends lock TTL before expiry",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ll_shared", "ll_shared.json", "lock_lease", "scenario_primary",
                 "Shared lock allows multiple sessions concurrently",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ll_stale_cleanup", "ll_stale_cleanup.json", "lock_lease", "edge_case",
                 "Stale lock cleanup removes locks held by sessions with stale heartbeat",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Metrics (1)
    FixtureEntry("metrics_summary", "metrics_summary.json", "metrics", "metrics",
                 "Metrics summary across 5 coordinations",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Panel (1)
    FixtureEntry("panel_state", "panel_state.json", "panel", "governance_validation",
                 "Panel state snapshot with all 26 tabs populated",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Priority & Fairness (8)
    FixtureEntry("pf_aging", "pf_aging.json", "priority_fairness", "scenario_primary",
                 "Priority aging prevents starvation of low priority",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("pf_high_first", "pf_high_first.json", "priority_fairness", "scenario_primary",
                 "High priority session admitted first",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("pf_inversion", "pf_inversion.json", "priority_fairness", "conflict_matrix",
                 "Priority inversion detected: LOW priority holding resource needed by HIGH",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("pf_max_grants", "pf_max_grants.json", "priority_fairness", "edge_case",
                 "Max consecutive grants enforced to prevent monopolization",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("pf_score", "pf_score.json", "priority_fairness", "scenario_primary",
                 "Fairness score computed correctly",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("pf_starvation", "pf_starvation.json", "priority_fairness", "negative_case",
                 "Starvation detected after session denied 10 consecutive rounds",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("pf_tie_break", "pf_tie_break.json", "priority_fairness", "edge_case",
                 "Same priority: deterministic tie-break via seed",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("pf_weighted", "pf_weighted.json", "priority_fairness", "scenario_primary",
                 "Weighted priority allocation across 4 sessions",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Registration (6)
    FixtureEntry("reg_duplicate", "reg_duplicate.json", "registration", "negative_case",
                 "Duplicate session ID rejection",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("reg_history", "reg_history.json", "registration", "governance_validation",
                 "Registration history is immutable once written",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("reg_no_owner", "reg_no_owner.json", "registration", "negative_case",
                 "Missing owner triggers registration conflict",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("reg_no_type", "reg_no_type.json", "registration", "negative_case",
                 "Missing session type triggers registration conflict",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("reg_single", "reg_single.json", "registration", "scenario_primary",
                 "Single paper session registration",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("reg_stale", "reg_stale.json", "registration", "edge_case",
                 "Stale session detection based on heartbeat age",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Report (1)
    FixtureEntry("report_full", "report_full.json", "report", "scenario_primary",
                 "Full coordination report with all sections populated",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Resource Management (10)
    FixtureEntry("res_double_book", "res_double_book.json", "resource", "conflict_matrix",
                 "Resource double booking detected",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_exhaustion", "res_exhaustion.json", "resource", "negative_case",
                 "Resource exhaustion: s1 granted, s2 blocked",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_expiry", "res_expiry.json", "resource", "edge_case",
                 "Reservation expiry invalidates lease after TTL",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_idempotent", "res_idempotent.json", "resource", "edge_case",
                 "Idempotent release: releasing same reservation twice is safe",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_partial", "res_partial.json", "resource", "edge_case",
                 "Partial resource grant when full request cannot be satisfied",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_release_unblock", "res_release_unblock.json", "resource", "scenario_primary",
                 "Resource release by s1 unblocks waiting session s2",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_renew", "res_renew.json", "resource", "scenario_primary",
                 "Reservation renewal extends lease before expiry",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_rollback", "res_rollback.json", "resource", "recovery_case",
                 "Rollback releases all granted resources on admission failure",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_single_grant", "res_single_grant.json", "resource", "scenario_primary",
                 "Single session resource grant succeeds",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("res_three_compete", "res_three_compete.json", "resource", "conflict_matrix",
                 "Three sessions compete for same resource; only one wins",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Scorecard (1)
    FixtureEntry("scorecard_full", "scorecard_full.json", "scorecard", "scenario_primary",
                 "Full scorecard with all 12 dimensions populated",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Symbol & Strategy Conflicts (8)
    FixtureEntry("ss_concentration", "ss_concentration.json", "symbol_strategy", "conflict_matrix",
                 "Concentration limit warned when 3 sessions all trade AAPL",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ss_correlated", "ss_correlated.json", "symbol_strategy", "conflict_matrix",
                 "Correlated strategy cluster warned",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ss_direction", "ss_direction.json", "symbol_strategy", "negative_case",
                 "Direction conflict detected: s1 LONG, s2 SHORT, blocked",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ss_dup_strategy", "ss_dup_strategy.json", "symbol_strategy", "conflict_matrix",
                 "Duplicate strategy warned",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ss_no_overlap", "ss_no_overlap.json", "symbol_strategy", "scenario_primary",
                 "No symbol overlap: s1 trades AAPL, s2 trades TSMC",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ss_opposite", "ss_opposite.json", "symbol_strategy", "negative_case",
                 "Opposite direction conflict: s1 LONG AAPL, s2 SHORT AAPL",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ss_overlap_warn", "ss_overlap_warn.json", "symbol_strategy", "edge_case",
                 "Symbol overlap warned when both s1 and s2 trade AAPL",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
    FixtureEntry("ss_stale", "ss_stale.json", "symbol_strategy", "edge_case",
                 "Stale strategy signal detected",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),

    # Integration (1)
    FixtureEntry("integration_multi_session", "integration_multi_session.json", "integration", "integration",
                 "Integration scenario: 3 sessions through full coordination lifecycle",
                 referenced_by=["fixture_registry_v1661", "health_v1661"]),
]


# ─── Public API ───────────────────────────────────────────────────────────────

def _build_index() -> Dict[str, FixtureEntry]:
    index: Dict[str, FixtureEntry] = {}
    for entry in _REGISTRY_ENTRIES:
        index[entry.fixture_id] = entry
    return index


_INDEX: Dict[str, FixtureEntry] = _build_index()


def register_fixture(fixture_id: str, filename: str, category: str, purpose: str,
                     description: str, referenced_by: Optional[List[str]] = None) -> FixtureEntry:
    """Register a new fixture entry (used for dynamic registration in tests)."""
    entry = FixtureEntry(
        fixture_id=fixture_id,
        filename=filename,
        category=category,
        purpose=purpose,
        description=description,
        referenced_by=referenced_by or [],
    )
    _INDEX[fixture_id] = entry
    return entry


def list_fixtures() -> List[FixtureEntry]:
    """Return all registered fixture entries. Deterministic (sorted by ID)."""
    return sorted(_INDEX.values(), key=lambda e: e.fixture_id)


def get_fixture(fixture_id: str) -> Optional[FixtureEntry]:
    """Return fixture entry by ID, or None if not found."""
    return _INDEX.get(fixture_id)


def validate_fixture_reference(fixture_id: str) -> Tuple[bool, str]:
    """Return (True, '') if fixture is registered and referenced, else (False, reason)."""
    entry = _INDEX.get(fixture_id)
    if entry is None:
        return (False, f"fixture_id {fixture_id!r} not registered")
    if not entry.is_referenced():
        return (False, f"fixture_id {fixture_id!r} has no referenced_by entries")
    return (True, "")


def list_referenced_fixtures() -> List[FixtureEntry]:
    """Return fixtures that have at least one referenced_by entry."""
    return [e for e in list_fixtures() if e.is_referenced()]


def list_unreferenced_fixtures() -> List[FixtureEntry]:
    """Return fixtures with no referenced_by entry."""
    return [e for e in list_fixtures() if not e.is_referenced()]


def fixture_usage_summary() -> Dict[str, Any]:
    """
    Return aggregated usage summary.
    Deterministic. No side effects.
    """
    all_fixtures = list_fixtures()
    referenced = list_referenced_fixtures()
    unreferenced = list_unreferenced_fixtures()
    ids = [e.fixture_id for e in all_fixtures]
    paths = [e.path for e in all_fixtures]
    duplicate_ids = [x for x in ids if ids.count(x) > 1]
    duplicate_paths = [x for x in paths if paths.count(x) > 1]
    missing_purpose = [e.fixture_id for e in all_fixtures if not e.purpose]
    invalid_purpose = [e.fixture_id for e in all_fixtures
                       if e.purpose and e.purpose not in VALID_PURPOSES]
    categories = sorted(set(e.category for e in all_fixtures))
    return {
        "total": len(all_fixtures),
        "registered": len(all_fixtures),
        "referenced": len(referenced),
        "unreferenced": len(unreferenced),
        "unused": len(unreferenced),
        "duplicate_ids": list(set(duplicate_ids)),
        "duplicate_paths": list(set(duplicate_paths)),
        "missing_purpose": missing_purpose,
        "invalid_purpose": invalid_purpose,
        "categories": categories,
        "registry_version": REGISTRY_VERSION,
        "all_referenced": len(unreferenced) == 0,
    }

"""
paper_trading/multi_session/scenario_registry_v166.py — Scenario Registry v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
At least 70 multi-session scenarios across all required categories.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


@dataclass
class MultiSessionScenario:
    scenario_id: str
    version: str
    category: str
    description: str
    session_count: int
    deterministic_seed: int
    expected_conflicts: List[str]
    expected_decisions: List[str]
    expected_final_states: Dict[str, str]
    fixture_reference: str
    forbidden_side_effects: List[str]
    policy_version: str
    paper_only: bool = True
    research_only: bool = True


def build_scenario_registry() -> List[MultiSessionScenario]:
    forbidden = ["real_order", "broker_execution", "capital_movement", "production_db_write"]

    def _s(sid, cat, desc, session_count, seed, conflicts, decisions, final_states, fixture, policy="1.6.6"):
        return MultiSessionScenario(
            scenario_id=sid, version="1.6.6", category=cat, description=desc,
            session_count=session_count, deterministic_seed=seed,
            expected_conflicts=conflicts, expected_decisions=decisions,
            expected_final_states=final_states, fixture_reference=fixture,
            forbidden_side_effects=forbidden, policy_version=policy,
        )

    # Registration (6)
    reg = [
        _s("REG_001","registration","Single paper session registration",1,1,[],["admit"],{"s1":"REGISTERED"},"reg_single.json"),
        _s("REG_002","registration","Duplicate session ID rejected",2,2,["duplicate_id"],["block"],{"s1":"REGISTERED"},"reg_duplicate.json"),
        _s("REG_003","registration","Missing owner rejected",1,3,["missing_owner"],["block"],{},"reg_no_owner.json"),
        _s("REG_004","registration","Missing session type rejected",1,4,["missing_type"],["block"],{},"reg_no_type.json"),
        _s("REG_005","registration","Registration history immutable",1,5,[],["admit"],{"s1":"REGISTERED"},"reg_history.json"),
        _s("REG_006","registration","Stale session detection",1,6,["stale_heartbeat"],["warn"],{"s1":"REGISTERED"},"reg_stale.json"),
    ]

    # Lifecycle (8)
    lc = [
        _s("LC_001","lifecycle","Valid CREATED→REGISTERED transition",1,10,[],["admit"],{"s1":"REGISTERED"},"lc_created_registered.json"),
        _s("LC_002","lifecycle","Invalid CREATED→RUNNING blocked",1,11,["invalid_transition"],["block"],{"s1":"CREATED"},"lc_invalid_direct_run.json"),
        _s("LC_003","lifecycle","PAUSED→READY requires verification",1,12,[],["resume_eligible"],{"s1":"READY"},"lc_pause_resume.json"),
        _s("LC_004","lifecycle","FAILED→RUNNING blocked",1,13,["invalid_transition"],["block"],{"s1":"FAILED"},"lc_failed_run.json"),
        _s("LC_005","lifecycle","COMPLETED→RUNNING blocked",1,14,["invalid_transition"],["block"],{"s1":"COMPLETED"},"lc_completed_run.json"),
        _s("LC_006","lifecycle","DEGRADED requires verification before RUNNING",1,15,[],["resume_blocked"],{"s1":"DEGRADED"},"lc_degraded.json"),
        _s("LC_007","lifecycle","RECOVERING→READY with verification",1,16,[],["resume_eligible"],{"s1":"READY"},"lc_recovering.json"),
        _s("LC_008","lifecycle","CANCELLED is terminal",1,17,[],["block"],{"s1":"CANCELLED"},"lc_cancelled.json"),
    ]

    # Resource (10)
    res = [
        _s("RES_001","resource","Single session resource grant",1,20,[],["admit"],{"s1":"RUNNING"},"res_single_grant.json"),
        _s("RES_002","resource","Resource exhaustion blocks new session",2,21,["resource_exhaustion"],["block"],{"s1":"RUNNING","s2":"BLOCKED"},"res_exhaustion.json"),
        _s("RES_003","resource","Partial resource grant",2,22,[],["admit"],{"s1":"RUNNING"},"res_partial.json"),
        _s("RES_004","resource","Resource double booking detected",2,23,["resource_double_booking"],["warn"],{},"res_double_book.json"),
        _s("RES_005","resource","Idempotent release",1,24,[],["admit"],{"s1":"RUNNING"},"res_idempotent.json"),
        _s("RES_006","resource","Reservation expiry",1,25,["lease_expired"],["warn"],{},"res_expiry.json"),
        _s("RES_007","resource","Reservation renewal",1,26,[],["admit"],{},"res_renew.json"),
        _s("RES_008","resource","Rollback on admission failure",2,27,[],["block"],{},"res_rollback.json"),
        _s("RES_009","resource","Three sessions compete for same resource",3,28,["resource_exhaustion"],["block"],{},"res_three_compete.json"),
        _s("RES_010","resource","Resource release unblocks waiting session",2,29,[],["admit"],{},"res_release_unblock.json"),
    ]

    # Lock/Lease (8)
    ll = [
        _s("LL_001","lock_lease","Exclusive lock acquired",1,30,[],["admit"],{},"ll_excl_acquire.json"),
        _s("LL_002","lock_lease","Exclusive lock conflict blocks",2,31,["resource_double_booking"],["block"],{},"ll_excl_conflict.json"),
        _s("LL_003","lock_lease","Shared lock multiple sessions",2,32,[],["admit"],{},"ll_shared.json"),
        _s("LL_004","lock_lease","Lease expiry invalidates lock",1,33,["lease_expired"],["warn"],{},"ll_lease_expiry.json"),
        _s("LL_005","lock_lease","Lease renewal",1,34,[],["admit"],{},"ll_renew.json"),
        _s("LL_006","lock_lease","Stale lock cleanup",1,35,["stale_heartbeat"],["warn"],{},"ll_stale_cleanup.json"),
        _s("LL_007","lock_lease","Lock ordering prevents deadlock",2,36,[],["admit"],{},"ll_ordering.json"),
        _s("LL_008","lock_lease","Owner validation on release",1,37,[],["admit"],{},"ll_owner_validate.json"),
    ]

    # Priority/Fairness (8)
    pf = [
        _s("PF_001","priority_fairness","High priority session admitted first",3,40,[],["admit"],{},"pf_high_first.json"),
        _s("PF_002","priority_fairness","Same priority deterministic tie-break",2,41,[],["admit"],{},"pf_tie_break.json"),
        _s("PF_003","priority_fairness","Priority aging prevents starvation",3,42,[],["admit"],{},"pf_aging.json"),
        _s("PF_004","priority_fairness","Starvation detected after threshold rounds",2,43,["starvation"],["warn"],{},"pf_starvation.json"),
        _s("PF_005","priority_fairness","Max consecutive grants enforced",2,44,[],["admit"],{},"pf_max_grants.json"),
        _s("PF_006","priority_fairness","Priority inversion detected",2,45,["priority_inversion"],["warn"],{},"pf_inversion.json"),
        _s("PF_007","priority_fairness","Fairness score computed correctly",3,46,[],["admit"],{},"pf_score.json"),
        _s("PF_008","priority_fairness","Weighted priority allocation",4,47,[],["admit"],{},"pf_weighted.json"),
    ]

    # Event Ordering (8)
    eo = [
        _s("EO_001","event_ordering","Monotonic global sequence assigned",2,50,[],["admit"],{},"eo_monotonic.json"),
        _s("EO_002","event_ordering","Same timestamp deterministic tie-break",2,51,[],["admit"],{},"eo_same_ts.json"),
        _s("EO_003","event_ordering","Late event detected and warned",2,52,[],["warn"],{},"eo_late_event.json"),
        _s("EO_004","event_ordering","Duplicate event deduplicated",2,53,[],["admit"],{},"eo_dedup.json"),
        _s("EO_005","event_ordering","Sequence gap detected",2,54,["event_order_violation"],["warn"],{},"eo_seq_gap.json"),
        _s("EO_006","event_ordering","Out-of-order event detected",2,55,["event_order_violation"],["warn"],{},"eo_out_of_order.json"),
        _s("EO_007","event_ordering","Cross-session barrier ALL_OF released",3,56,[],["admit"],{},"eo_barrier_all.json"),
        _s("EO_008","event_ordering","Cross-session barrier QUORUM released",3,57,[],["admit"],{},"eo_barrier_quorum.json"),
    ]

    # Symbol/Strategy (8)
    ss = [
        _s("SS_001","symbol_strategy","No overlap allowed",2,60,[],["admit"],{},"ss_no_overlap.json"),
        _s("SS_002","symbol_strategy","Symbol overlap warned",2,61,["symbol_overlap"],["warn"],{},"ss_overlap_warn.json"),
        _s("SS_003","symbol_strategy","Opposite direction strategy conflict",2,62,["strategy_conflict"],["warn"],{},"ss_opposite.json"),
        _s("SS_004","symbol_strategy","Duplicate strategy warned",2,63,["strategy_conflict"],["warn"],{},"ss_dup_strategy.json"),
        _s("SS_005","symbol_strategy","Concentration limit warned",2,64,["symbol_overlap"],["warn"],{},"ss_concentration.json"),
        _s("SS_006","symbol_strategy","Direction conflict detected",2,65,["strategy_conflict"],["block"],{},"ss_direction.json"),
        _s("SS_007","symbol_strategy","Correlated strategy cluster warned",3,66,["strategy_conflict"],["warn"],{},"ss_correlated.json"),
        _s("SS_008","symbol_strategy","Stale strategy signal detected",2,67,["strategy_conflict"],["warn"],{},"ss_stale.json"),
    ]

    # Capital/Risk (8)
    cr = [
        _s("CR_001","capital_risk","Capital within budget admitted",2,70,[],["admit"],{},"cr_within_budget.json"),
        _s("CR_002","capital_risk","Capital over-allocation blocked",3,71,["capital_overallocation"],["block"],{},"cr_over_alloc.json"),
        _s("CR_003","capital_risk","Partial capital grant",2,72,[],["warn"],{},"cr_partial.json"),
        _s("CR_004","capital_risk","Risk budget exceeded blocks",2,73,["risk_budget_exceeded"],["block"],{},"cr_risk_exceed.json"),
        _s("CR_005","capital_risk","Risk concentration warned",3,74,[],["warn"],{},"cr_concentration.json"),
        _s("CR_006","capital_risk","Priority-based capital allocation",3,75,[],["admit"],{},"cr_priority_alloc.json"),
        _s("CR_007","capital_risk","Aggregate risk aggregation",4,76,[],["warn"],{},"cr_aggregate.json"),
        _s("CR_008","capital_risk","No real capital movement confirmed",2,77,[],["admit"],{},"cr_no_real_capital.json"),
    ]

    # Checkpoint/Recovery (6)
    chk = [
        _s("CHK_001","checkpoint_recovery","Per-session checkpoint created",1,80,[],["admit"],{},"chk_create.json"),
        _s("CHK_002","checkpoint_recovery","Checkpoint collision detected",2,81,["checkpoint_conflict"],["block"],{},"chk_collision.json"),
        _s("CHK_003","checkpoint_recovery","Checkpoint hash verified",1,82,[],["admit"],{},"chk_hash.json"),
        _s("CHK_004","checkpoint_recovery","Recovery plan created and executed",1,83,[],["admit"],{},"chk_recovery.json"),
        _s("CHK_005","checkpoint_recovery","Recovery collision detected",2,84,["recovery_collision"],["block"],{},"chk_rec_collision.json"),
        _s("CHK_006","checkpoint_recovery","Partial failure: one session recovery fails",2,85,["recovery_collision"],["warn"],{},"chk_partial_failure.json"),
    ]

    all_scenarios = reg + lc + res + ll + pf + eo + ss + cr + chk
    assert len(all_scenarios) == 70, f"Expected 70 scenarios, got {len(all_scenarios)}"
    return all_scenarios


SCENARIO_REGISTRY = build_scenario_registry()

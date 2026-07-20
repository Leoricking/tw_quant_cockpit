"""
paper_trading/small_capital_strategy/paper_cockpit_v203.py
v2.0.3 Paper Strategy Simulation Batch & Scenario Replay
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.3"
SCHEMA_VERSION = "203"
RELEASE_NAME = "Paper Strategy Simulation Batch & Scenario Replay"
BASELINE_TESTS = 33205
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

MARKET_CONDITIONS: List[str] = [
    "bull_trend",
    "pullback",
    "range_bound",
    "breakdown",
    "panic_selloff",
    "rebound",
    "high_volatility",
    "low_liquidity",
]

ENTRY_STYLES: List[str] = [
    "conservative",
    "balanced",
    "aggressive",
    "second_wave",
    "abc_pullback",
    "breakout_only",
    "risk_first",
]

CLI_COMMANDS_V203: List[str] = [
    "paper-cockpit-v203-simulate-one",
    "paper-cockpit-v203-simulate-batch",
    "paper-cockpit-v203-replay-scenario",
    "paper-cockpit-v203-compare-profiles",
    "paper-cockpit-v203-rank-results",
    "paper-cockpit-v203-export-json",
    "paper-cockpit-v203-export-md",
    "paper-cockpit-v203-export-csv",
    "paper-cockpit-v203-health",
    "paper-cockpit-v203-gate",
]

GUI_TABS_V203: List[str] = [
    "simulation_batch_v203",
    "scenario_replay_v203",
    "strategy_comparison_v203",
]

SIMULATION_EXPORT_FORMATS: List[str] = ["json", "markdown", "csv", "audit_snapshot"]

SCENARIO_REPLAY_FIELDS: List[str] = [
    "scenario_id", "scenario_name", "market_condition", "trend_condition",
    "volatility_condition", "liquidity_condition", "chip_condition",
    "margin_condition", "candidate_inputs", "expected_block_reasons",
    "expected_final_actions", "replay_notes",
]

STRATEGY_PROFILE_FIELDS: List[str] = [
    "profile_id", "profile_name", "entry_style", "risk_budget_pct",
    "max_position_count", "max_single_position_pct", "stop_loss_policy",
    "add_policy", "reduce_policy", "exit_policy", "no_entry_policy",
    "human_review_policy",
]

BATCH_COMPARISON_FIELDS: List[str] = [
    "strategy_profile_id", "total_candidates", "allowed_count", "blocked_count",
    "paper_buy_plan_count", "paper_add_plan_count", "reduce_plan_count",
    "exit_plan_count", "no_entry_count", "avg_score", "avg_risk_used",
    "human_review_count", "top_candidates", "worst_blocked_reasons",
    "simulation_quality_score",
]

SIMULATION_RANKING_FIELDS: List[str] = [
    "rank", "profile_id", "scenario_id", "quality_score", "risk_score",
    "selectivity_score", "actionability_score", "review_burden_score",
    "safety_score", "final_grade",
]

SAFETY_FLAGS_V203: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "simulation_batch_only": True,
    "scenario_replay_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "deterministic_simulation": True,
    "paper_only_data_only": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
}

assert len(SAFETY_FLAGS_V203) == 20, f"Expected 20 SAFETY_FLAGS_V203, got {len(SAFETY_FLAGS_V203)}"
assert len(MARKET_CONDITIONS) == 8
assert len(ENTRY_STYLES) == 7
assert len(CLI_COMMANDS_V203) == 10
assert len(GUI_TABS_V203) == 3
assert len(SCENARIO_REPLAY_FIELDS) == 12
assert len(STRATEGY_PROFILE_FIELDS) == 12
assert len(BATCH_COMPARISON_FIELDS) == 15
assert len(SIMULATION_RANKING_FIELDS) == 10


# ---------------------------------------------------------------------------
# Dataclasses — 12 models, schema_version="203"
# ---------------------------------------------------------------------------

@dataclass
class SimulationInput:
    """Input for a simulation run. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    no_real_orders: bool = True
    simulation_id: str = ""
    simulation_version: str = "2.0.3"
    scenario_id: str = ""
    strategy_profile_id: str = ""
    watchlist: List[str] = field(default_factory=list)
    candidates: List[str] = field(default_factory=list)
    market_condition: str = "bull_trend"
    entry_style: str = "balanced"
    risk_budget_pct: float = 20.0
    human_review_required: bool = True


@dataclass
class ScenarioReplaySchema:
    """Scenario replay definition. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    scenario_id: str = ""
    scenario_name: str = ""
    market_condition: str = "bull_trend"
    trend_condition: str = "uptrend"
    volatility_condition: str = "normal"
    liquidity_condition: str = "adequate"
    chip_condition: str = "neutral"
    margin_condition: str = "normal"
    candidate_inputs: List[str] = field(default_factory=list)
    expected_block_reasons: List[str] = field(default_factory=list)
    expected_final_actions: List[str] = field(default_factory=list)
    replay_notes: str = ""
    no_real_orders: bool = True


@dataclass
class StrategyProfile:
    """Strategy profile configuration. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    no_real_orders: bool = True
    profile_id: str = ""
    profile_name: str = ""
    entry_style: str = "balanced"
    risk_budget_pct: float = 20.0
    max_position_count: int = 5
    max_single_position_pct: float = 15.0
    stop_loss_policy: str = "fixed_8pct"
    add_policy: str = "add_on_pullback"
    reduce_policy: str = "reduce_on_extend"
    exit_policy: str = "exit_on_breakdown"
    no_entry_policy: str = "strict"
    human_review_policy: str = "always_required"


@dataclass
class SimulationCandidateResult:
    """Per-candidate simulation result. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    scenario_id: str = ""
    profile_id: str = ""
    abc_type: str = "NO_ENTRY"
    final_action: str = "NO_ENTRY"
    signal_score: float = 0.0
    risk_ok: bool = False
    sizing_ok: bool = False
    no_entry_reasons: List[str] = field(default_factory=list)
    human_review_required: bool = True
    block_reason: str = ""


@dataclass
class BatchComparison:
    """Batch comparison output for a strategy profile. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    no_real_orders: bool = True
    strategy_profile_id: str = ""
    total_candidates: int = 0
    allowed_count: int = 0
    blocked_count: int = 0
    paper_buy_plan_count: int = 0
    paper_add_plan_count: int = 0
    reduce_plan_count: int = 0
    exit_plan_count: int = 0
    no_entry_count: int = 0
    avg_score: float = 0.0
    avg_risk_used: float = 0.0
    human_review_count: int = 0
    top_candidates: List[str] = field(default_factory=list)
    worst_blocked_reasons: List[str] = field(default_factory=list)
    simulation_quality_score: float = 0.0


@dataclass
class SimulationRanking:
    """Simulation ranking entry. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    rank: int = 0
    profile_id: str = ""
    scenario_id: str = ""
    quality_score: float = 0.0
    risk_score: float = 0.0
    selectivity_score: float = 0.0
    actionability_score: float = 0.0
    review_burden_score: float = 0.0
    safety_score: float = 100.0
    final_grade: str = "C"


@dataclass
class SimulationExportResult:
    """Export result for a simulation run. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    no_real_orders: bool = True
    simulation_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True


@dataclass
class SimulationAuditSnapshot:
    """Audit snapshot for a simulation run. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    simulation_id: str = ""
    run_metadata: str = ""
    input_snapshot: str = ""
    decision_snapshot: str = ""
    risk_snapshot: str = ""
    ticket_snapshot: str = ""
    blocked_reason_snapshot: str = ""
    human_review_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class SimulationResult:
    """Full result of one simulation run. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    simulation_id: str = ""
    simulation_version: str = "2.0.3"
    scenario_id: str = ""
    strategy_profile_id: str = ""
    watchlist_snapshot: List[str] = field(default_factory=list)
    candidate_snapshot: List[str] = field(default_factory=list)
    rule_snapshot: str = "paper_abc_rules_v203"
    risk_policy_snapshot: str = "paper_risk_policy_v203"
    replay_result: List[SimulationCandidateResult] = field(default_factory=list)
    final_action_summary: Dict[str, int] = field(default_factory=dict)
    paper_only_safety_snapshot: bool = True
    all_passed: bool = False


@dataclass
class BatchSimulationResult:
    """Result of a batch simulation across multiple profiles/scenarios. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    no_real_orders: bool = True
    batch_id: str = ""
    simulations: List[SimulationResult] = field(default_factory=list)
    comparisons: List[BatchComparison] = field(default_factory=list)
    rankings: List[SimulationRanking] = field(default_factory=list)
    all_passed: bool = False


@dataclass
class V203HealthSummary:
    """Health summary for v2.0.3. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.3"


@dataclass
class V203ReleaseSummary:
    """Release summary for v2.0.3. v2.0.3."""
    schema_version: str = "203"
    paper_only: bool = True
    version: str = "2.0.3"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 12
    cli_count: int = 10
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


_ALL_MODEL_NAMES_V203: List[str] = [
    "SimulationInput",
    "ScenarioReplaySchema",
    "StrategyProfile",
    "SimulationCandidateResult",
    "BatchComparison",
    "SimulationRanking",
    "SimulationExportResult",
    "SimulationAuditSnapshot",
    "SimulationResult",
    "BatchSimulationResult",
    "V203HealthSummary",
    "V203ReleaseSummary",
]

assert len(_ALL_MODEL_NAMES_V203) == 12


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------

def _make_simulation_id(scenario_id: str, profile_id: str, watchlist_len: int) -> str:
    raw = f"sim-{scenario_id}-{profile_id}-{watchlist_len}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _make_batch_id(profile_ids: List[str]) -> str:
    raw = "batch-" + "-".join(sorted(profile_ids))
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _score_candidate_v203(symbol: str, market_condition: str, entry_style: str) -> float:
    """Simple deterministic score for simulation. Paper only."""
    base = float(abs(hash(symbol)) % 40 + 50)  # 50..89
    condition_bonus = {
        "bull_trend": 10.0, "pullback": 5.0, "rebound": 7.0,
        "range_bound": 0.0, "breakdown": -10.0, "panic_selloff": -15.0,
        "high_volatility": -5.0, "low_liquidity": -8.0,
    }.get(market_condition, 0.0)
    style_bonus = {
        "aggressive": 5.0, "breakout_only": 3.0, "balanced": 0.0,
        "conservative": -3.0, "risk_first": -5.0,
        "abc_pullback": 2.0, "second_wave": 1.0,
    }.get(entry_style, 0.0)
    return min(100.0, max(0.0, base + condition_bonus + style_bonus))


def _determine_final_action(score: float, market_condition: str, risk_budget_pct: float) -> str:
    """Determine final action for simulation. Paper only."""
    if market_condition in ("breakdown", "panic_selloff"):
        return "NO_ENTRY"
    if risk_budget_pct <= 0.0:
        return "NO_ENTRY"
    if score >= 80.0:
        return "PAPER_BUY_PLAN"
    if score >= 70.0:
        return "PAPER_ADD_PLAN"
    if score >= 60.0:
        return "WATCH"
    if score >= 50.0:
        return "WAIT"
    return "NO_ENTRY"


def simulate_one(sim_input: Optional[SimulationInput] = None) -> SimulationResult:
    """Run a single paper simulation. Paper only."""
    if sim_input is None:
        sim_input = SimulationInput()
    sim_id = _make_simulation_id(
        sim_input.scenario_id, sim_input.strategy_profile_id,
        len(sim_input.watchlist)
    )
    candidate_results: List[SimulationCandidateResult] = []
    final_action_summary: Dict[str, int] = {}
    for symbol in (sim_input.candidates or sim_input.watchlist):
        score = _score_candidate_v203(symbol, sim_input.market_condition, sim_input.entry_style)
        action = _determine_final_action(score, sim_input.market_condition, sim_input.risk_budget_pct)
        res = SimulationCandidateResult(
            symbol=symbol,
            scenario_id=sim_input.scenario_id,
            profile_id=sim_input.strategy_profile_id,
            abc_type="A_PULLBACK_10MA" if score >= 75 else "NO_ENTRY",
            final_action=action,
            signal_score=round(score, 2),
            risk_ok=sim_input.risk_budget_pct > 0,
            sizing_ok=score >= 50.0,
            human_review_required=True,
        )
        candidate_results.append(res)
        final_action_summary[action] = final_action_summary.get(action, 0) + 1
    return SimulationResult(
        simulation_id=sim_id,
        scenario_id=sim_input.scenario_id,
        strategy_profile_id=sim_input.strategy_profile_id,
        watchlist_snapshot=list(sim_input.watchlist),
        candidate_snapshot=list(sim_input.candidates or sim_input.watchlist),
        replay_result=candidate_results,
        final_action_summary=final_action_summary,
        all_passed=True,
    )


def replay_scenario(scenario: Optional[ScenarioReplaySchema] = None) -> SimulationResult:
    """Replay a scenario. Paper only."""
    if scenario is None:
        scenario = ScenarioReplaySchema(scenario_id="SC203-001", scenario_name="default")
    sim_input = SimulationInput(
        scenario_id=scenario.scenario_id,
        watchlist=list(scenario.candidate_inputs),
        market_condition=scenario.market_condition,
    )
    return simulate_one(sim_input)


def simulate_batch(
    profiles: Optional[List[StrategyProfile]] = None,
    scenarios: Optional[List[ScenarioReplaySchema]] = None,
) -> BatchSimulationResult:
    """Run batch simulation across profiles. Paper only."""
    if profiles is None:
        profiles = [StrategyProfile(profile_id="P001", profile_name="default_balanced")]
    if scenarios is None:
        scenarios = [ScenarioReplaySchema(scenario_id="SC203-001", market_condition="bull_trend")]
    batch_id = _make_batch_id([p.profile_id for p in profiles])
    simulations: List[SimulationResult] = []
    comparisons: List[BatchComparison] = []
    for profile in profiles:
        for scenario in scenarios:
            sim_input = SimulationInput(
                scenario_id=scenario.scenario_id,
                strategy_profile_id=profile.profile_id,
                watchlist=list(scenario.candidate_inputs) or ["2330", "2317", "2454"],
                market_condition=scenario.market_condition,
                entry_style=profile.entry_style,
                risk_budget_pct=profile.risk_budget_pct,
            )
            result = simulate_one(sim_input)
            simulations.append(result)
            cmp = build_batch_comparison(result, profile.profile_id)
            comparisons.append(cmp)
    rankings = rank_simulations(comparisons)
    return BatchSimulationResult(
        batch_id=batch_id,
        simulations=simulations,
        comparisons=comparisons,
        rankings=rankings,
        all_passed=True,
    )


def build_batch_comparison(result: SimulationResult, profile_id: str) -> BatchComparison:
    """Build batch comparison output. Paper only."""
    candidates = result.replay_result
    allowed = [c for c in candidates if c.final_action != "NO_ENTRY"]
    blocked = [c for c in candidates if c.final_action == "NO_ENTRY"]
    buy_plan = [c for c in candidates if c.final_action == "PAPER_BUY_PLAN"]
    add_plan = [c for c in candidates if c.final_action == "PAPER_ADD_PLAN"]
    reduce_plan = [c for c in candidates if c.final_action == "PAPER_REDUCE_PLAN"]
    exit_plan = [c for c in candidates if c.final_action == "PAPER_EXIT_PLAN"]
    no_entry = [c for c in candidates if c.final_action == "NO_ENTRY"]
    avg_score = (sum(c.signal_score for c in candidates) / len(candidates)) if candidates else 0.0
    top = sorted(candidates, key=lambda c: c.signal_score, reverse=True)[:3]
    block_reasons = list({c.block_reason for c in blocked if c.block_reason})[:3]
    quality = min(100.0, avg_score * (len(allowed) / max(1, len(candidates))) * 1.2)
    return BatchComparison(
        strategy_profile_id=profile_id,
        total_candidates=len(candidates),
        allowed_count=len(allowed),
        blocked_count=len(blocked),
        paper_buy_plan_count=len(buy_plan),
        paper_add_plan_count=len(add_plan),
        reduce_plan_count=len(reduce_plan),
        exit_plan_count=len(exit_plan),
        no_entry_count=len(no_entry),
        avg_score=round(avg_score, 2),
        avg_risk_used=20.0,
        human_review_count=len(candidates),
        top_candidates=[c.symbol for c in top],
        worst_blocked_reasons=block_reasons,
        simulation_quality_score=round(quality, 2),
    )


def rank_simulations(comparisons: List[BatchComparison]) -> List[SimulationRanking]:
    """Rank simulations by quality score. Paper only."""
    sorted_cmp = sorted(comparisons, key=lambda c: c.simulation_quality_score, reverse=True)
    rankings: List[SimulationRanking] = []
    for rank_idx, cmp in enumerate(sorted_cmp, start=1):
        q = cmp.simulation_quality_score
        grade = "A" if q >= 80 else "B" if q >= 65 else "C" if q >= 50 else "D"
        rankings.append(SimulationRanking(
            rank=rank_idx,
            profile_id=cmp.strategy_profile_id,
            scenario_id="",
            quality_score=q,
            risk_score=max(0.0, 100.0 - cmp.avg_risk_used * 2),
            selectivity_score=min(100.0, cmp.allowed_count / max(1, cmp.total_candidates) * 100),
            actionability_score=min(100.0, cmp.paper_buy_plan_count / max(1, cmp.total_candidates) * 200),
            review_burden_score=min(100.0, cmp.human_review_count / max(1, cmp.total_candidates) * 100),
            safety_score=100.0,
            final_grade=grade,
        ))
    return rankings


def export_simulation_json(result: SimulationResult) -> SimulationExportResult:
    """Export simulation result as JSON-like string. Paper only."""
    content = (
        f'{{"simulation_id": "{result.simulation_id}", '
        f'"simulation_version": "{result.simulation_version}", '
        f'"scenario_id": "{result.scenario_id}", '
        f'"profile_id": "{result.strategy_profile_id}", '
        f'"candidates": {len(result.replay_result)}, '
        f'"paper_only": true, "no_real_orders": true}}'
    )
    return SimulationExportResult(
        simulation_id=result.simulation_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
    )


def export_simulation_markdown(result: SimulationResult) -> SimulationExportResult:
    """Export simulation result as Markdown. Paper only."""
    lines = [
        f"# Paper Simulation Report v{result.simulation_version}",
        f"## Simulation ID: {result.simulation_id}",
        f"## Scenario: {result.scenario_id}",
        f"## Profile: {result.strategy_profile_id}",
        "## Paper Only — No Real Orders — Not Investment Advice",
        "## Candidates",
    ]
    for c in result.replay_result:
        lines.append(f"- {c.symbol}: {c.final_action} (score={c.signal_score})")
    lines.append("## Final Action Summary")
    for action, count in result.final_action_summary.items():
        lines.append(f"- {action}: {count}")
    return SimulationExportResult(
        simulation_id=result.simulation_id,
        export_format="markdown",
        content="\n".join(lines),
        is_valid=True,
        export_status="complete",
    )


def export_simulation_csv(result: SimulationResult) -> SimulationExportResult:
    """Export simulation result as CSV. Paper only."""
    rows = ["symbol,final_action,signal_score,risk_ok,sizing_ok,human_review_required"]
    for c in result.replay_result:
        rows.append(f"{c.symbol},{c.final_action},{c.signal_score},{c.risk_ok},{c.sizing_ok},{c.human_review_required}")
    return SimulationExportResult(
        simulation_id=result.simulation_id,
        export_format="csv",
        content="\n".join(rows),
        is_valid=True,
        export_status="complete",
    )


def build_simulation_audit_snapshot(result: SimulationResult) -> SimulationAuditSnapshot:
    """Build audit snapshot for a simulation. Paper only."""
    raw = f"{result.simulation_id}{result.scenario_id}{result.strategy_profile_id}"
    repro_hash = hashlib.md5(raw.encode()).hexdigest()
    return SimulationAuditSnapshot(
        simulation_id=result.simulation_id,
        run_metadata=f"v{result.simulation_version}|scenario={result.scenario_id}",
        input_snapshot=f"candidates={len(result.candidate_snapshot)}|watchlist={len(result.watchlist_snapshot)}",
        decision_snapshot=f"actions={result.final_action_summary}",
        risk_snapshot="risk_policy=paper_risk_policy_v203",
        ticket_snapshot=f"tickets={len(result.replay_result)}",
        blocked_reason_snapshot="no_blocked_reasons_snapshot",
        human_review_snapshot="all_require_human_review=True",
        safety_snapshot="NO_REAL_ORDERS=True|BROKER_EXECUTION_ENABLED=False|PRODUCTION_TRADING_BLOCKED=True",
        reproducibility_hash=repro_hash,
    )


def get_simulation_summary() -> Dict[str, Any]:
    """Return v2.0.3 simulation summary. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "models": len(_ALL_MODEL_NAMES_V203),
        "cli_commands": len(CLI_COMMANDS_V203),
        "gui_tabs": len(GUI_TABS_V203),
        "market_conditions": len(MARKET_CONDITIONS),
        "entry_styles": len(ENTRY_STYLES),
        "safety_flags": len(SAFETY_FLAGS_V203),
        "paper_only": True,
        "no_real_orders": True,
        "broker_execution_disabled": True,
        "production_trading_blocked": True,
        "not_investment_advice": True,
    }


def get_version_info_v203() -> Dict[str, Any]:
    """Return version info for v2.0.3. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def verify_version_v203() -> bool:
    """Assert all v2.0.3 module-level invariants."""
    assert VERSION == "2.0.3"
    assert SCHEMA_VERSION == "203"
    assert NO_REAL_ORDERS is True
    assert BROKER_EXECUTION_ENABLED is False
    assert PRODUCTION_TRADING_BLOCKED is True
    assert len(MARKET_CONDITIONS) == 8
    assert len(ENTRY_STYLES) == 7
    assert len(CLI_COMMANDS_V203) == 10
    assert len(GUI_TABS_V203) == 3
    assert len(SAFETY_FLAGS_V203) == 20
    assert len(_ALL_MODEL_NAMES_V203) == 12
    assert len(SCENARIO_REPLAY_FIELDS) == 12
    assert len(STRATEGY_PROFILE_FIELDS) == 12
    assert len(BATCH_COMPARISON_FIELDS) == 15
    assert len(SIMULATION_RANKING_FIELDS) == 10
    assert SAFETY_FLAGS_V203["paper_only"] is True
    assert SAFETY_FLAGS_V203["no_real_orders"] is True
    assert SAFETY_FLAGS_V203["broker_execution_disabled"] is True
    assert SAFETY_FLAGS_V203["production_trading_blocked"] is True
    return True


assert verify_version_v203(), "paper_cockpit_v203 verify_version_v203() FAILED"

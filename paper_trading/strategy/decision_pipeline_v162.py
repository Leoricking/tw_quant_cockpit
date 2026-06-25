"""
paper_trading/strategy/decision_pipeline_v162.py — 19-step decision pipeline for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Optional

from paper_trading.strategy.enums_v162 import (
    ApprovalMode,
    DecisionOutcome,
    EligibilityResult,
    SignalType,
)
from paper_trading.strategy.models_v162 import (
    DecisionContext,
    DecisionResult,
    _new_id,
    _now_iso,
)

logger = logging.getLogger(__name__)


def _log_step(ctx: DecisionContext, step: int, msg: str) -> None:
    ctx.pipeline_step = step
    ctx.pipeline_log.append(f"[{step:02d}] {msg}")
    logger.debug("[v1.6.2][pipeline] step=%02d %s", step, msg)


def _reject(ctx: DecisionContext, step: int, outcome: DecisionOutcome, reason: str) -> DecisionResult:
    _log_step(ctx, step, f"REJECT outcome={outcome.value} reason={reason}")
    return DecisionResult(
        context_id=ctx.context_id,
        strategy_id=ctx.strategy_config.strategy_id if ctx.strategy_config else "",
        ticker=ctx.signal.ticker if ctx.signal else "",
        signal_id=ctx.signal.signal_id if ctx.signal else "",
        outcome=outcome.value,
        reason=reason,
        pipeline_steps_completed=step,
        decided_at=_now_iso(),
        paper_only=True,
        research_only=True,
        simulation_only=True,
        not_a_real_order=True,
        no_broker_call=True,
    )


def _approve(ctx: DecisionContext, step: int, proposal_id: Optional[str] = None) -> DecisionResult:
    _log_step(ctx, step, "APPROVE")
    return DecisionResult(
        context_id=ctx.context_id,
        strategy_id=ctx.strategy_config.strategy_id if ctx.strategy_config else "",
        ticker=ctx.signal.ticker if ctx.signal else "",
        signal_id=ctx.signal.signal_id if ctx.signal else "",
        outcome=DecisionOutcome.APPROVED.value,
        reason="All pipeline checks passed",
        pipeline_steps_completed=step,
        decided_at=_now_iso(),
        proposal_id=proposal_id,
        paper_only=True,
        research_only=True,
        simulation_only=True,
        not_a_real_order=True,
        no_broker_call=True,
    )


class DecisionPipeline:
    """
    19-step fixed-order decision pipeline for paper signal evaluation.

    Steps:
     01. Validate strategy (registered, running)
     02. Validate signal (type, safety flags)
     03. Check duplicate (dedup)
     04. Check cooldown (per-ticker)
     05. Check rate limits (signals/min)
     06. Build context (assemble PIT/market/quality info)
     07. Check market state (open/closed)
     08. Check data quality
     09. Check PIT validity
     10. Check eligibility
     11. Run sizing
     12. Run correlation
     13. Run risk controls
     14. Resolve conflicts
     15. Apply approval policy
     16. Build proposal
     17. Submit to paper order machine
     18. Journal
     19. Create lineage

    Steps 17-19 are performed by the orchestrator after this pipeline
    returns APPROVED. The pipeline itself performs steps 1-16 and
    returns a DecisionResult.
    """

    def run(
        self,
        ctx: DecisionContext,
        *,
        is_registered: bool = True,
        is_running: bool = True,
        is_duplicate: bool = False,
        is_on_cooldown: bool = False,
        is_rate_limited: bool = False,
        is_market_open: bool = False,
        data_quality_ok: bool = False,
        pit_valid: bool = False,
        eligibility: str = EligibilityResult.UNCERTAIN.value,
        suggested_size: Optional[float] = None,
        correlation_breach: bool = False,
        risk_blocked: bool = False,
        conflict_detected: bool = False,
        at_proposal_capacity: bool = False,
    ) -> DecisionResult:
        """
        Execute the pipeline. Returns a DecisionResult.
        All inputs are research-context values — no real broker data.
        """

        # Step 1 — Validate strategy
        if not is_registered:
            return _reject(ctx, 1, DecisionOutcome.PIPELINE_ERROR, "Strategy not registered")
        if not is_running:
            return _reject(ctx, 1, DecisionOutcome.BLOCKED,
                           "Strategy not in RUNNING state")
        _log_step(ctx, 1, "Strategy validated: registered+running")

        # Step 2 — Validate signal
        if ctx.signal is None:
            return _reject(ctx, 2, DecisionOutcome.PIPELINE_ERROR, "No signal in context")
        if not ctx.signal.paper_only:
            return _reject(ctx, 2, DecisionOutcome.PIPELINE_ERROR, "Signal missing paper_only=True")
        if not ctx.signal.not_a_real_order:
            return _reject(ctx, 2, DecisionOutcome.PIPELINE_ERROR, "Signal missing not_a_real_order=True")
        forbidden = {"ENTRY_SHORT", "SELL_SHORT", "MARGIN_LONG", "MARGIN_SHORT"}
        if ctx.signal.signal_type in forbidden:
            return _reject(ctx, 2, DecisionOutcome.BLOCKED,
                           f"Forbidden signal type: {ctx.signal.signal_type}")
        _log_step(ctx, 2, f"Signal validated: type={ctx.signal.signal_type} ticker={ctx.signal.ticker}")

        # Step 3 — Duplicate check
        if is_duplicate:
            return _reject(ctx, 3, DecisionOutcome.DUPLICATE,
                           f"Duplicate signal for {ctx.signal.ticker} (dedup_key={ctx.signal.dedup_key[:8]})")
        _log_step(ctx, 3, "Dedup: not a duplicate")

        # Step 4 — Cooldown
        if is_on_cooldown:
            return _reject(ctx, 4, DecisionOutcome.COOLDOWN,
                           f"Ticker {ctx.signal.ticker} on cooldown")
        _log_step(ctx, 4, f"Cooldown: {ctx.signal.ticker} clear")

        # Step 5 — Rate limit
        if is_rate_limited:
            return _reject(ctx, 5, DecisionOutcome.RATE_LIMITED, "Signal rate limit exceeded")
        _log_step(ctx, 5, "Rate limit: OK")

        # Step 6 — Build context (already built by caller; log it)
        _log_step(ctx, 6, "Context assembled")

        # Step 7 — Market state
        if not is_market_open:
            _log_step(ctx, 7, "Market closed — continuing (paper simulation)")
            # Research-mode: we allow signals through even if market closed
            # (paper simulation can evaluate on any data)
        else:
            _log_step(ctx, 7, "Market open")

        # Step 8 — Data quality
        if not data_quality_ok:
            return _reject(ctx, 8, DecisionOutcome.DATA_STALE,
                           "Data quality check failed — stale or unavailable")
        _log_step(ctx, 8, "Data quality: OK")

        # Step 9 — PIT validity
        if not pit_valid:
            return _reject(ctx, 9, DecisionOutcome.DATA_STALE, "Point-in-time data invalid")
        _log_step(ctx, 9, "PIT: valid")

        # Step 10 — Eligibility
        if eligibility == EligibilityResult.INELIGIBLE.value:
            return _reject(ctx, 10, DecisionOutcome.INELIGIBLE,
                           f"Ticker {ctx.signal.ticker} not eligible")
        _log_step(ctx, 10, f"Eligibility: {eligibility}")

        # Step 11 — Sizing
        if suggested_size is not None and suggested_size <= 0:
            return _reject(ctx, 11, DecisionOutcome.SIZING_ZERO,
                           f"Suggested size is zero/negative: {suggested_size}")
        _log_step(ctx, 11, f"Sizing: {suggested_size}")

        # Step 12 — Correlation
        if correlation_breach:
            return _reject(ctx, 12, DecisionOutcome.RISK_BLOCKED,
                           "Correlation exposure limit breached")
        _log_step(ctx, 12, "Correlation: OK")

        # Step 13 — Risk controls
        if risk_blocked:
            return _reject(ctx, 13, DecisionOutcome.RISK_BLOCKED,
                           "Risk controls blocked this signal")
        _log_step(ctx, 13, "Risk: OK")

        # Step 14 — Conflict resolution
        if conflict_detected:
            return _reject(ctx, 14, DecisionOutcome.CONFLICT,
                           "Conflicting signal detected; applying MOST_CONSERVATIVE policy")
        _log_step(ctx, 14, "Conflict: none")

        # Step 15 — Approval policy
        approval_mode = ctx.approval_mode
        if approval_mode == ApprovalMode.MANUAL_REQUIRED.value:
            return _reject(ctx, 15, DecisionOutcome.DEFERRED,
                           "MANUAL_REQUIRED approval mode: awaiting explicit approval")
        if approval_mode != ApprovalMode.AUTO_PAPER_ONLY.value:
            return _reject(ctx, 15, DecisionOutcome.BLOCKED,
                           f"Unknown approval mode: {approval_mode}")
        _log_step(ctx, 15, "Approval: AUTO_PAPER_ONLY granted")

        # Step 16 — Proposal capacity
        if at_proposal_capacity:
            return _reject(ctx, 16, DecisionOutcome.BLOCKED,
                           "Open proposal capacity reached")
        _log_step(ctx, 16, "Proposal capacity: OK — proposal ready")

        # Steps 17-19 are handled by the orchestrator
        return _approve(ctx, 16)

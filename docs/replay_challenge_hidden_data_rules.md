# Replay Challenge Hidden Data Rules v1.2.7

**[!] Future data hidden. Outcome hidden. Answer Key separate. Research Only.**

## Forbidden Fields in Active Payload → BLOCKED

- forward_return, realized_pnl, outcome_score, future_signal
- final_high, final_low, hindsight_score
- answer_key, best_action, expected_result
- future_bars, future_strategy_signals, future_timeframe_conflicts
- future_review_classification, prior_attempt_answer, best_attempt_answer
- future_journal_revisions, MFE, MAE, final_session_high, final_session_low

## Optional Hidden (by difficulty)

- symbol, date, company_name (ADVANCED/EXPERT)
- exact_price_scale, strategy_module_label, timeframe_label (EXPERT)

## Reveal Rules

- Outcome reveal requires both `--reveal` AND `--confirm-review`
- No auto-reveal. No Yes/No popup.
- Review never auto-Confirms Mistakes.

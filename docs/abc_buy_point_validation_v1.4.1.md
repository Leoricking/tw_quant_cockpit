# A/B/C Buy Point Validation v1.4.1

**[!] Research Only | No Real Orders | Broker Execution Disabled | Production Trading BLOCKED | Backtest Does Not Guarantee Future Performance | Not Investment Advice**

---

## Overview

The A/B/C Buy Point Validation system (v1.4.1) provides a structured empirical framework for validating A/B/C buy point strategy rules using historical data. It wraps the existing `BuyPointAnalyzer` domain logic with adapters and adds rigorous analysis layers: holding period, stop loss, take profit, regime, volume, institutional/margin, second wave, filter ablation, walk-forward validation, and comparison engine.

All results are research-only. Formal conclusions require real data, OOS/walk-forward validation, ≥30 trades, ≥5 symbols, and ≥2 regimes. Fixture and demo data are explicitly blocked from formal conclusions.

---

## Buy Point Types

| Type | Description | Support MA | Min History |
|------|-------------|-----------|-------------|
| A | MA10 pullback — price touches/approaches 10-day MA, support holds | MA10 | 30 bars |
| B | MA5+VWAP — short-term momentum with VWAP support | MA5 | 20 bars |
| C | MA20 reclaim — price reclaims 20-day MA after pullback | MA20 | 40 bars |

---

## Package: `abc_validation/`

### `__init__.py`
Safety flags exported at package level:
- `NO_REAL_ORDERS = True`
- `BROKER_EXECUTION_ENABLED = False`
- `PRODUCTION_TRADING_BLOCKED = True`
- `ABC_BUY_POINT_VALIDATION_AVAILABLE = True`

### `rule_adapters_v141.py`
Wraps existing `StrategyKnowledgeRuleRegistry` rules without redefining domain logic.
- `ABuyPointRuleAdapter` — delegates to rule `abc_buy_point_a`
- `BBuyPointRuleAdapter` — delegates to rule `abc_buy_point_b`
- `CBuyPointRuleAdapter` — delegates to rule `abc_buy_point_c`
- Each adapter: `get_rule()`, `analyze()`, `is_x_signal(result)`

### `snapshots_v141.py`
`ABCBuyPointRuleSnapshot` dataclass — captures rule configuration at a point in time.
- Deterministic `parameter_hash` (SHA256[:16] of rule_id + parameters)
- `to_dict()` / `from_dict()` (ignores unknown fields)
- `make_default(buy_point_type)` factory

### `signal_classification_v141.py`
`ABCSignalClassification` — string constants for all signal outcomes:
- A: `A_STRICT`, `A_RELAXED`, `A_FAILED_SUPPORT`, `A_INSUFFICIENT_DATA`
- B: `B_STRICT`, `B_RELAXED`, `B_OVEREXTENDED`, `B_FAILED_SUPPORT`, `B_INSUFFICIENT_DATA`
- C: `C_STRICT_RECLAIM`, `C_WEAK_RECLAIM`, `C_FALSE_RECLAIM`, `C_NO_CONFIRMATION`, `C_INSUFFICIENT_DATA`
- `BLOCKED`

`ABCSignalRecord` dataclass — full signal record with `formal_conclusion_allowed: bool`.
`validate_fixture_mode(mode)` — raises `ValueError` if `mode=='real'` and `fixture_data=True`.

### `integrity_guard_v141.py`
`ABCSignalIntegrityGuard.check(signal_dict, bars)` returns `{passed, classification, issues}`.

Checks performed:
- Minimum history (A: 30, B: 20, C: 40 bars)
- Volume baseline availability
- Timestamp ordering (no future timestamps)
- Lookahead bias (execution date must be after signal date)
- No duplicate bars
- Stale data detection
- Corporate action status
- Fixture data in real mode

Failure mappings:
- Missing data → `INSUFFICIENT_DATA`
- Lookahead detected → `BLOCKED`
- Same-bar execution → `BLOCKED`
- Duplicate bars → `BLOCKED`
- Fixture in real mode → `BLOCKED`

### `parameters_v141.py`
Default parameters for each buy point type:

`APointParameters`: ma10_touch_tolerance=0.01, max_breach_pct=0.02, recovery_window=3, vol_contraction_ratio=0.7, kd_low_threshold=30.0, institutional_sell_limit=-2000.0, trend_requirement="MA60_UP"

`BPointParameters`: ma5_touch_tolerance=0.005, max_breach_pct=0.01, recovery_window=2, vol_contraction_ratio=0.8, overextension_limit=0.05, short_term_trend_requirement="MA10_UP"

`CPointParameters`: ma20_reclaim_tolerance=0.005, min_close_above_ma20=1, confirmation_bars=2, vol_confirmation_ratio=1.2, kd_turn_requirement=True, rsi_recovery_threshold=40.0, macd_improvement_requirement=True

`ABCValidationParameters` — combines all three with `validate()`, `to_dict()`, `from_dict()`.

### `holding_period_analyzer_v141.py`
`ABCHoldingPeriodAnalyzer(periods=[1,2,3,5,10,20])` — analyzes returns across multiple holding periods. Per period: signals, filled_trades, avg_return, median_return, win_rate, expectancy, max_drawdown, MFE, MAE, positive/negative excursion probability, fees/taxes/slippage, benchmark excess return.

### `stop_loss_analyzer_v141.py`
9 stop models: `no_stop`, `fixed_pct`, `below_signal_low`, `below_ma5`, `below_ma10`, `below_ma20`, `atr_based`, `time_stop`, `structure_failure`.

Stop slippage included; `effective_stop = stop_price * (1 - slippage_rate)`. Invalid model raises `ValueError`.

### `take_profit_analyzer_v141.py`
10 take-profit models: `fixed_pct`, `risk_reward_multiple`, `ma5_exit`, `ma10_exit`, `ma20_exit`, `trailing_stop`, `momentum_failure`, `volume_price_failure`, `max_holding_period`, `strategy_defined_exit`.

Same-bar stop+target collision → conservative resolution (use stop, not target). Output includes `stop_target_collision_count` and `exit_reason_distribution`.

### `regime_analyzer_v141.py`
`ABCRegimeAnalyzer` — classifies market regime from bars before signal only (no future regime labeling). Uses `MarketRegimeClassifier` from `empirical_backtest`. Per regime: signal count, fill rate, win rate, expectancy, stop-out rate, average return.

Regimes: BULL, BEAR, SIDEWAYS, HIGH_VOLATILITY, LOW_VOLATILITY, UNKNOWN.

### `filter_ablation_v141.py`
12 filter stages: `base_only`, `+volume_contraction`, `+kd`, `+rsi`, `+macd`, `+foreign`, `+investment_trust`, `+dealer`, `+margin`, `+ma60_trend`, `+second_wave`, `full_composite`.

Over-filter threshold: 50% signal decrease. All stages preserved in output. "No single best declared" — researcher reviews stages.

### `second_wave_analyzer_v141.py`
`ABCSecondWaveAnalyzer.check_second_wave_conditions(signal, bars)` — 9 conditions:
1. prior_impulse — prior momentum move present
2. intact_trend — trend structure unbroken
3. pullback_vol_contraction — volume contracted during pullback
4. valid_support — support level holds
5. re_strengthening — momentum indicators recovering
6. no_institutional_retreat — institutional not selling
7. no_excessive_margin — margin not overextended
8. reasonable_distance_from_high — within 30% of prior high
9. not_overextended — not stretched from prior high (≤30%)

### `institutional_margin_analyzer_v141.py`
`MISSING_SENTINEL = "INSUFFICIENT"` — never substitutes 0 or False for missing data.

`ABCInstitutionalMarginAnalyzer.classify_signal(signal)` → states: foreign_state, trust_state, institutional_state, margin_state, data_timestamp_safe.

Missing institutional → INSUFFICIENT. Missing margin → INSUFFICIENT.

### `volume_analyzer_v141.py`
7 volume states: `pullback_volume_contraction`, `breakout_volume_expansion`, `no_volume_reclaim`, `abnormal_single_day`, `multi_day_confirmation`, `volume_unavailable`, `volume_baseline_insufficient`.

Per state: signal_count, fill_count, expectancy, false_signal_rate, stop_out_rate, drawdown, sample_confidence.

### `outcome_taxonomy_v141.py`
15 outcome types:
- Success: `SUCCESS_TREND_CONTINUATION`, `SUCCESS_QUICK_REBOUND`, `SUCCESS_SECOND_WAVE`
- Failure: `FAILED_SUPPORT_BREAK`, `FALSE_BREAKOUT`, `FALSE_RECLAIM`, `SIDEWAYS_CHOP`, `GAP_FAILURE`, `STOPPED_THEN_RECOVERED`, `TARGET_THEN_REVERSED`
- Neutral: `NO_FILL`, `NO_FOLLOW_THROUGH`, `END_OF_DATA`
- Data: `INSUFFICIENT_DATA`, `BLOCKED`

No post-hoc high-price labeling (avoids hindsight bias).

### `failure_rate_analyzer_v141.py`
`ABCFailureRateAnalyzer.analyze(signals, trades, buy_point_type)` — computes: signal_failure_rate, stop_out_rate, no_follow_through_rate, false_breakout_rate, false_reclaim_rate, support_break_rate, stopped_then_recovered_rate, target_then_reversed_rate, no_fill_rate.

### `validation_result_v141.py`
`ABCValidationResult` dataclass — captures complete validation run output.

`to_dict()` always enforces safety flags. `from_dict()` ignores unknown fields and always enforces safety flags regardless of stored values.

### `comparison_engine_v141.py`
10 comparison modes: `a_vs_b`, `a_vs_c`, `b_vs_c`, `a_vs_b_vs_c`, `strict_vs_relaxed`, `base_vs_full_filters`, `second_wave_vs_non`, `regime_specific`, `holding_period_specific`, `stop_model_specific`.

Required same fields for comparability: universe, date_range, cost_model, slippage_model, execution_model, benchmark, data_quality. Different configuration → not directly rankable. Invalid mode raises `ValueError`.

### `confidence_v141.py`
`ABCValidationConfidence.evaluate(validation_result)` → {level, formal_conclusion_allowed, blockers, reasons, requirements_met, requirements_failed}.

10 requirements for HIGH confidence:
1. real_data
2. no_fixture_data
3. lookahead_safe
4. corporate_action_clean
5. sufficient_trades (≥30)
6. multiple_symbols (≥5)
7. multiple_regimes (≥2)
8. oos_or_walk_forward
9. positive_expectancy
10. not_parameter_sensitive

Levels: `HIGH` / `MEDIUM` / `LOW` / `INSUFFICIENT` / `BLOCKED`.

### `walk_forward_v141.py`
`ABCWalkForwardValidator(n_folds=5, train_pct=0.6, val_pct=0.2, test_pct=0.2)`.

Splits must sum to 1.0 (AssertionError otherwise). All folds preserved including negative-performance folds. No test-set parameter tuning.

### `store_v141.py`
`SCHEMA_VERSION = "1.4.1"`, `STORE_DIR = "data/abc_validation"`.

Atomic writes: write to `.tmp` then `os.replace`. Safe load: returns empty list on corruption/missing.

Files: abc_rule_snapshots.json, abc_validation_runs.json, abc_validation_results.json, abc_comparison_results.json, abc_ablation_results.json, abc_walk_forward_results.json.

### `repair_integration_v141.py`
`ABCRepairIntegration(create_repair_tasks=False)` — default disabled. No auto repair/refresh/download/mock fallback. `create_candidates()` returns candidates without creating tasks unless explicitly enabled.

### `replay_integration_v141.py`
`ABCReplayIntegration` — READ_ONLY. MODIFIES_REPLAY_SESSIONS=False, MODIFIES_CHALLENGE_QUESTIONS=False, MODIFIES_RULE_PARAMETERS=False, MODIFIES_REGISTRY=False. Evidence summary only.

### `report_v141.py`
`ABCValidationReport.generate_text(result)` — multi-section text report with safety footer.
`generate_dict(result)` — structured dict with sections list.

### `health_v141.py`
`ABCBuyPointValidationHealthCheck` with 31 checks covering: package import, safety flags, all 3 rule adapters, all analyzer modules, store, confidence evaluator, walk-forward validator, comparison engine, report generator, integrity guard.

`get_health_summary()` includes:
- `abc_a_available`, `abc_b_available`, `abc_c_available`
- `auto_optimization_enabled = False`
- `auto_trading_enabled = False`
- `mock_fallback_enabled = False`
- `broker_execution_enabled = False`
- `production_trading_blocked = True`

---

## GUI Panel: `gui/abc_buy_point_validation_panel.py`

| Field | Value |
|-------|-------|
| TAB_ID | abc_buy_point_validation |
| DISPLAY_NAME | A/B/C Validation |
| GROUP | research |
| PRIORITY | P1 |

15-tab QTabWidget: Overview, Trades, Signals, Outcomes, Holding Period, Stop Loss, Take Profit, Regimes, Ablation, Second Wave, Institutional, Margin, Volume, Blocked Symbols, Provenance.

`ABCValidationWorker(QThread)` — runs health check in background thread. `finished` / `error` signals.

`ABCBuyPointValidationPanel(QWidget)` — safety banner, config group, 10 action buttons. `closeEvent()` calls `_stop_worker()`.

Stub class returned if PySide6 unavailable.

---

## CLI Commands (19 new in v1.4.1)

All commands default to dry-run mode unless `--execute` is specified.

| Command | Description |
|---------|-------------|
| `abc-validation-health` | Health check for the ABC validation package |
| `abc-validation-plan` | Plan a validation run (dry-run default) |
| `abc-validation-run` | Execute a validation run |
| `abc-validation-list` | List all validation runs |
| `abc-validation-show` | Show a specific validation result |
| `abc-validation-compare` | Compare two or more validation results |
| `abc-validation-holding-period` | Analyze holding period results |
| `abc-validation-stop-loss` | Analyze stop loss models |
| `abc-validation-take-profit` | Analyze take profit models |
| `abc-validation-regime` | Analyze regime-specific results |
| `abc-validation-ablation` | Run filter ablation analysis |
| `abc-validation-second-wave` | Analyze second wave conditions |
| `abc-validation-institutional` | Analyze institutional/margin factors |
| `abc-validation-volume` | Analyze volume states |
| `abc-validation-confidence` | Evaluate validation confidence |
| `abc-validation-walk-forward` | Run walk-forward validation |
| `abc-validation-report` | Generate validation report |
| `abc-validation-snapshot` | Create a rule snapshot |
| `abc-validation-summary` | Print validation store summary |

---

## Test Fixtures: `tests/fixtures/abc_validation/`

All fixtures have `_fixture_meta.TEST_FIXTURE=true`, `NOT_REAL_DATA=true`, `NOT_FOR_FORMAL_CONCLUSION=true`, `fixture_data=true`, `formal_conclusion_allowed=false`.

| File | Contents |
|------|----------|
| `signal_a_strict.json` | A buy point strict classification signal |
| `signal_b_relaxed.json` | B buy point relaxed classification signal |
| `signal_c_reclaim.json` | C buy point MA20 reclaim signal |
| `signal_blocked.json` | Signal that should be blocked (same-bar execution) |
| `multi_symbol_signals.json` | Multiple symbols for universe-level testing |
| `regime_cases.json` | 4 signals across BULL/BEAR/SIDEWAYS/HIGH_VOLATILITY regimes |
| `second_wave.json` | Second wave candidate with all 9 conditions |
| `stop_target_collision.json` | Stop/target nearly identical — collision scenario |
| `walk_forward_folds.json` | Walk-forward fold structure for testing |
| `validation_result_v1.json` | Complete validation result (INSUFFICIENT confidence) |

---

## Test File: `tests/test_abc_validation_v141.py`

182 tests covering:
- Package / safety flags (5 tests)
- Rule adapters (8 tests)
- Snapshots (6 tests)
- Signal classification (8 tests)
- Integrity guard (8 tests)
- Parameters (6 tests)
- Holding period analyzer (6 tests)
- Stop loss analyzer (8 tests)
- Take profit analyzer (8 tests)
- Regime analyzer (6 tests)
- Filter ablation (7 tests)
- Second wave analyzer (7 tests)
- Institutional/margin analyzer (7 tests)
- Volume analyzer (7 tests)
- Outcome taxonomy (7 tests)
- Failure rate analyzer (6 tests)
- Validation result (7 tests)
- Comparison engine (7 tests)
- Confidence evaluator (7 tests)
- Walk-forward validator (6 tests)
- Store (8 tests)
- Repair integration (5 tests)
- Replay integration (5 tests)
- Report (5 tests)
- Health check (8 tests)
- Version info (5 tests)
- Fixture loading (10 tests)
- CLI smoke tests (22 tests)
- GUI smoke tests (3 tests)
- Regression / cross-module (6 tests)
- End-to-end (1 test)

All 182 tests pass. No external network or credential access.

---

## Safety Summary

| Flag | Value |
|------|-------|
| NO_REAL_ORDERS | True |
| BROKER_EXECUTION_ENABLED | False |
| PRODUCTION_TRADING_BLOCKED | True |
| MOCK_FORMAL_CONCLUSION_ALLOWED | False |
| AUTO_OPTIMIZATION_ENABLED | False |
| AUTO_TRADING_ENABLED | False |
| MOCK_FALLBACK_ENABLED | False |
| Fixture data in real mode | BLOCKED |
| Formal conclusion minimum | real data + OOS + ≥30 trades + ≥5 symbols + ≥2 regimes |
| CLI default | dry-run |
| Lookahead | BLOCKED |
| Same-bar execution | BLOCKED |

---

## Limitations

- All demo/fixture results have `confidence=INSUFFICIENT` and `formal_conclusion_allowed=False`
- Formal conclusions require real historical data with verified adjustments
- Walk-forward results must include out-of-sample period to qualify for HIGH confidence
- Comparison across different configurations is not directly rankable
- Parameters not optimized — default values used for all analysis
- Not Investment Advice

---

*v1.4.1 — A/B/C Buy Point Validation — Research Only*

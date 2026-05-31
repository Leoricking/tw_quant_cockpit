# Strategy Rule Governance — v0.3.28

> **[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.**

---

## 1. What Is v0.3.28 Rule Governance?

Version 0.3.28 introduces the **Strategy Rule Governance** subsystem. Its goal is to give every strategy rule a persistent, queryable identity — including a unique ID, version, status, confidence level, and dependency graph — so that the research workflow has a clear audit trail and no rule can silently influence results without being explicitly registered and reviewed.

Key outcomes of v0.3.28:

- Every rule has a machine-readable `rule_id` in a canonical format.
- Rules have lifecycle statuses (ACTIVE, EXPERIMENTAL, NEEDS_REVIEW, DISABLED, …).
- Rule confidence is scored from backtest validation data.
- Dependencies between rules are tracked in a directed graph.
- A point-in-time snapshot can be exported at any time.
- A Markdown governance report can be generated from the GUI or CLI.

---

## 2. What Is Rule Governance?

Rule governance is the practice of treating each strategy rule as a first-class artifact with:

- A unique, versioned identifier.
- A clearly defined status and confidence level.
- Explicit links to the source module, data requirements, and peer rules it depends on.
- A change log recording every status or metadata update.
- Regular validation against backtest results.

Without governance, rules accumulate silently. A rule that worked in one market regime may be applied in another without anyone noticing it was never re-validated. Governance makes that visible.

---

## 3. Rule ID Format

Every rule must have a `rule_id` in the format:

```
CATEGORY.TIMEFRAME.NAME.VERSION
```

Examples:

| Rule ID | Meaning |
|---------|---------|
| `BUY.SHORT.PULLBACK_10MA.V1` | Buy-point rule, short timeframe, pullback to 10MA, version 1 |
| `SCREEN.UNIVERSAL.VOLUME_BREAKOUT.V1` | Screener rule, universal timeframe, volume breakout |
| `BACKTEST.COST.TAIWAN_REALISTIC.V1` | Governance rule, Taiwan cost model |
| `INTRADAY.VWAP.RECLAIM.V1` | Intraday rule, VWAP reclaim signal |

The version suffix (`V1`, `V2`, …) is incremented when the rule logic changes significantly, preserving the history of the old version.

---

## 4. Status Values

| Status | Meaning |
|--------|---------|
| `ACTIVE` | Rule is validated and in use. |
| `EXPERIMENTAL` | Rule is being tested — do not rely on it for primary decisions. |
| `NEEDS_REVIEW` | Rule requires re-validation or logic review before next use. |
| `INSUFFICIENT_SAMPLE` | Too few backtest observations to assess reliability. |
| `DISABLED` | Rule has been turned off but not deleted. |
| `DEPRECATED` | Rule is superseded by a newer version. |
| `BLOCKED` | Rule must not be used — hard block. |

---

## 5. Confidence Levels

| Level | Meaning |
|-------|---------|
| `HIGH` | Validated on large sample with strong performance. |
| `GOOD` | Validated on adequate sample with good performance. |
| `PARTIAL` | Validated but sample is limited or performance is moderate. |
| `WEAK` | Minimal validation — treat results with caution. |
| `LOW` | Poor validation results or rule is disabled/blocked. |
| `UNKNOWN` | No validation data available yet. |
| `PLANNED` | Rule logic planned but not yet implemented or tested. |

Confidence is scored by `RuleConfidenceScorer` using backtest CSV files in `data/backtest_results/`. If no data is present, rules default to `UNKNOWN`.

---

## 6. Rule Categories

| Category | Description |
|----------|-------------|
| `buy_point` | Entry trigger rules based on price/MA patterns |
| `screener` | Universe filtering rules (volume, MA alignment, holder data) |
| `strategy_knowledge` | Encoded trading knowledge (MACD, KD, sector rotation) |
| `long_term` | Fundamental quality rules for longer holding periods |
| `portfolio` | Position sizing, risk, and cash management rules |
| `signal_quality` | Rules that modify signal weight (boost, reduce, disable) |
| `rule_weight` | Direct rule weighting adjustments |
| `intraday` | Intraday price/volume microstructure rules |
| `risk` | Standalone risk flag rules |
| `data_quality` | Data freshness and completeness checks |
| `provider` | Data provider reliability rules |
| `governance` | Backtest execution, cost, and validation rules |

---

## 7. Rule Dependencies

Rules can declare `dependencies` — a list of other `rule_id` values they build upon. For example, `BUY.SHORT.SECOND_WAVE.V1` depends on both `SCREEN.UNIVERSAL.MAIN_THEME_STRENGTH.V1` and `SCREEN.UNIVERSAL.INSTITUTIONAL_BUYING.V1`.

The `RuleDependencyGraph` class builds a directed graph from these declarations. It provides:

- Forward lookup: what does this rule depend on?
- Reverse lookup: what rules depend on this rule?
- Cycle detection: are there circular dependencies?
- Topological ordering: in what order should rules be evaluated?
- High-impact rule identification: which rules have the most dependents?

If a rule is disabled or has low confidence, you should check its dependents in the graph before acting on any downstream signals.

---

## 8. Experimental vs. Disabled vs. Needs Review

These three states are frequently confused:

- **Experimental** (`experimental=True`, status=`EXPERIMENTAL`): The rule is live in the system but flagged as unproven. It may produce signals, but those signals should be treated as informational only. Confidence is capped at `PARTIAL`.

- **Disabled** (status=`DISABLED`): The rule has been explicitly turned off. It will not contribute to screens or signals. It remains in the registry for audit purposes.

- **Needs Review** (status=`NEEDS_REVIEW`): The rule was previously active but something triggered a review flag — a regime change, new contradictory data, or a logic question. It should not be trusted until reviewed and re-activated.

---

## 9. Rule Snapshot

A **rule snapshot** is a point-in-time export of all registered rules and their current metadata. Snapshots are written to:

```
data/backtest_results/rule_governance_snapshot_YYYY-MM-DD.json
data/backtest_results/rule_governance_summary_YYYY-MM-DD.csv
```

These files are **not committed to git** — they are runtime outputs.

You can generate a snapshot via:

- GUI: click **Export Snapshot** in the Rule Governance panel.
- CLI: `python -c "from gui.rule_governance_adapter import RuleGovernanceAdapter; print(RuleGovernanceAdapter().export_snapshot())"`

---

## 10. GUI Usage

The Rule Governance panel is accessible from the main cockpit dashboard.

Sections:

1. **Safety Banner** — always visible, confirms no real orders are possible.
2. **Summary Cards** — total rules, active count, experimental, needs review, high-confidence count, unknown-confidence count.
3. **Rule Table** — full rule list with columns: Rule ID, Name, Category, Version, Status, Enabled, Experimental, Confidence, Sample Count, Timeframe.
4. **Dependency Table** — per-rule dependency and dependent counts, plus cycle warnings.
5. **Review Queue** — rules that need attention, with reason and recommended action.
6. **Action Buttons**:
   - **Refresh Governance**: re-runs the full governance pipeline (background thread — GUI does not freeze).
   - **Generate Report**: writes a Markdown report to `reports/`.
   - **Export Snapshot**: writes JSON + CSV to `data/backtest_results/`.

---

## 11. CLI Usage

```bash
# Run full governance pipeline
python -c "
from gui.rule_governance_adapter import RuleGovernanceAdapter
adapter = RuleGovernanceAdapter()
result = adapter.run_governance()
print('Total rules:', result['registry_summary']['total_rules'])
print('Needs review:', result['registry_summary']['needs_review_count'])
"

# Generate report
python -c "
from gui.rule_governance_adapter import RuleGovernanceAdapter
path = RuleGovernanceAdapter().generate_report()
print('Report written to:', path)
"

# Export snapshot
python -c "
from gui.rule_governance_adapter import RuleGovernanceAdapter
print(RuleGovernanceAdapter().export_snapshot())
"

# Inspect a specific rule
python -c "
from governance.rule_registry import RuleRegistry
r = RuleRegistry()
r.load_builtin_rules()
rule = r.get_rule('BUY.SHORT.PULLBACK_10MA.V1')
print(rule)
"

# List all rules needing review
python -c "
from governance.rule_registry import RuleRegistry
r = RuleRegistry()
r.load_builtin_rules()
for rule in r.list_rules(status='NEEDS_REVIEW'):
    print(rule.rule_id, '—', rule.description)
"
```

---

## 12. Why Weights Are Not Auto-Applied

Rule weights — the coefficients that determine how much each signal contributes to a composite score — are **never automatically applied** by this system.

Reasons:

1. **Sample size**: Most rules have fewer than 50 validated trades. Auto-applying weights from small samples leads to overfitting.
2. **Regime sensitivity**: A rule that works in a trending market may fail in a choppy one. Applying weights without checking the current regime is dangerous.
3. **Audit requirement**: Any change to weights must be traceable. An automatic update with no human review creates audit gaps.
4. **Safety invariant**: The system is explicitly marked `no_real_orders = True` and `production_blocked = True`. Auto-weight application would be a step toward production trading without the required safety review.

To change a rule weight, a researcher must:
1. Review the rule's confidence level and sample count.
2. Inspect the dependency graph for downstream effects.
3. Update the weight manually in the relevant configuration file.
4. Log the change in the rule change log with a reason.

---

## 13. No Real Orders / No Live Trading

This entire subsystem — and the TW Quant Cockpit as a whole — operates in research mode only.

Safety guarantees:

| Flag | Value | Meaning |
|------|-------|---------|
| `read_only` | `True` | No writes to broker APIs or order systems |
| `no_real_orders` | `True` | No orders are generated or submitted |
| `production_blocked` | `True` | Production trading pathways are disabled |

These flags appear in every class, every module docstring, and in all generated reports and snapshots. They are not configurable at runtime. Any code path that would reach a real broker is explicitly absent from this codebase.

---

*TW Quant Cockpit v0.3.28 — Research Only*

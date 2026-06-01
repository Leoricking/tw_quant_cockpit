# ML Feature Store Knowledge Integration — v0.4.2.1

> **[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] No live prediction. No auto-trading. auto_enabled=False. Confidence ≤ PARTIAL.**
> **[!] Long-cycle / crash-watch risk = Metadata Only. Not a short-term sell signal.**

---

## Objectives

v0.4.2.1 connects transcript-derived strategy knowledge (from v0.4.1.1 `StrategyKnowledgeStore` CSVs)
into the v0.4.2 ML Feature Store. The bridge converts structured knowledge from four categories
(factor_candidates, rule_candidates, avoid_conditions, risk_conditions) into ML feature metadata
with readiness assessment and leakage checking.

**What this version does NOT do:**
- Does NOT train any model
- Does NOT auto-enable any feature
- Does NOT place any order
- Does NOT affect existing ML Feature Store (v0.4.2) built-in features
- Does NOT affect Strategy Knowledge Ingestion (v0.4.1.1)

---

## Feature Mapping Rules

| Knowledge Category | feature_source | feature_type | readiness | Notes |
|--------------------|---------------|--------------|-----------|-------|
| factor_candidates | transcript_knowledge | numeric/boolean | NEEDS_MAPPING | Needs column mapping to data source |
| rule_candidates | rule_candidate | boolean | NEEDS_BACKTEST | Empirical validation required |
| avoid_conditions | avoid_condition | avoid_flag | PARTIAL or NEEDS_BACKTEST | Pattern-based → BLOCKED |
| risk_conditions | risk_condition | risk_flag | PARTIAL | Non-cycle risk |
| risk_conditions (long_cycle) | risk_condition | regime_flag | METADATA_ONLY | not_for_short_term_label=True |

All features: `auto_enabled=False`, `experimental=True`, `confidence ≤ PARTIAL`

---

## Readiness Levels

| Readiness | Meaning |
|-----------|---------|
| READY | Validated, no leakage — may be included optionally in model schema |
| PARTIAL | Partially validated — needs backtest confirmation |
| METADATA_ONLY | Regime/cycle metadata only — NOT for short-term labels |
| NEEDS_MAPPING | Factor candidate — needs column mapping to actual data source |
| NEEDS_BACKTEST | Rule candidate — requires empirical backtest first |
| LEAKAGE_RISK | Leakage risk detected — requires manual review |
| BLOCKED | Critical leakage or pattern incomplete |
| INSUFFICIENT_DATA | Insufficient data to assess |

---

## Leakage Types

| Type | Description |
|------|-------------|
| POST_EVENT_KNOWLEDGE | Transcript published after training sample dates |
| TIMING_ESTIMATED | announcement_date_is_estimated=True for fundamentals |
| LONG_CYCLE_RISK | Long-cycle/crash-watch view — cannot be short-term label |
| PATTERN_INCOMPLETE | Pattern feature before pattern_confirmed_date |
| UNVALIDATED_CANDIDATE | Rule candidate not yet empirically validated |

---

## Output Files

All outputs are under `data/backtest_results/ml_feature_store/` (gitignored).

| File | Contents |
|------|----------|
| `knowledge_feature_catalog.csv` | All features with full metadata |
| `knowledge_feature_readiness.csv` | Readiness assessment per feature |
| `knowledge_feature_leakage.csv` | Leakage findings per feature |
| `model_ready_knowledge_schema.json` | READY/PARTIAL features with no critical leakage (optional) |
| `ml_knowledge_integration_summary.json` | Latest integration run summary |

**model_ready_knowledge_schema.json** excludes:
- Long-cycle / regime features (not_for_short_term_label=True)
- Features with critical leakage findings
- All features are still `auto_enabled=False` and require `--include-knowledge-features` flag

---

## CLI Commands

```bash
# Dry run (no files written)
python main.py ml-knowledge-integrate --mode real --dry-run

# Full integration
python main.py ml-knowledge-integrate --mode real

# With Markdown report
python main.py ml-knowledge-integrate --mode real --report

# Leakage check (reads existing catalog)
python main.py ml-knowledge-leakage-check --mode real

# Show latest summary
python main.py ml-knowledge-feature-summary
```

**Prerequisite:** Run `strategy-knowledge-ingest` first to populate knowledge CSVs.

---

## Safety Summary

| Invariant | Value |
|-----------|-------|
| Read Only | True |
| No Real Orders | True |
| Production Trading | BLOCKED |
| auto_enabled | False (always) |
| Confidence cap | PARTIAL (transcript-only) |
| Long-cycle as label | NEVER (METADATA_ONLY) |
| Model training | NEVER |
| Include by default | False (--include-knowledge-features required) |

---

*ML Feature Store Knowledge Integration v0.4.2.1 — Research Only. No Real Orders.*

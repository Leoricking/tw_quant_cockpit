# Data Quality Rules

This document defines minimum data requirements for each analysis timeframe
in TW Quant Cockpit.

---

## Timeframe Requirements

### Short-term Analysis (formal_allowed = short_allowed)

| Data Type | Minimum Rows |
|-----------|-------------|
| Daily K | >= 20 trading days |
| Institutional | >= 5 days |
| Margin | >= 5 days |

A symbol with all three conditions met is flagged `short_allowed = True`.

### Mid-term Analysis (formal_allowed = mid_allowed)

| Data Type | Minimum Rows |
|-----------|-------------|
| Daily K | >= 60 trading days |
| Institutional | >= 5 days |
| Margin | >= 5 days |
| Monthly Revenue | >= 6 months |
| Holder | >= 2 periods |

### Long-term Analysis (formal_allowed = long_allowed)

| Data Type | Minimum Rows |
|-----------|-------------|
| Daily K | >= 120 trading days |
| Monthly Revenue | >= 12 months |
| Holder | >= 2 periods |

---

## Per Data-Type Rules

### Daily K

- Must have: date, symbol, open, high, low, close, volume
- close must be > 0
- high must be >= low
- volume must be >= 0
- Duplicate symbol+date rows are removed (last kept)
- Minimum for short: 20 rows; mid: 60 rows; long: 120 rows

### Institutional

- Must have: date, symbol, foreign_net_buy, trust_net_buy, dealer_net_buy
- Values may be negative (net sell)
- Duplicate symbol+date rows are removed
- Minimum for analysis: 5 rows; recommended: 40 rows

### Margin

- Must have: date, symbol, margin_balance, margin_change, short_balance, short_change
- margin_balance and short_balance must be >= 0
- Duplicate symbol+date rows are removed
- Minimum for analysis: 5 rows; recommended: 40 rows

### Monthly Revenue

- Must have: month, symbol, revenue
- revenue must be >= 0
- Duplicate symbol+month rows are removed
- Minimum for mid-term: 6 months; long-term: 12 months
- YoY and MoM percentages stored as percentage values (e.g. 12.3 not 0.123)

### Holder

- Must have: date, symbol, major_holder_ratio, retail_holder_ratio
- Ratio values must be between 0 and 100
- Duplicate symbol+date rows are removed
- Minimum for analysis: 2 periods; recommended: 4 periods

### Trust Cost

- Must have: date, symbol, trust_avg_cost, close
- trust_avg_cost and close must be > 0
- Duplicate symbol+date rows are removed
- Minimum: 3 rows (basic), 20 rows (standard), 40 rows (full)

### Profile

- Must have: symbol, name
- One row per symbol
- Duplicate symbols are removed (last kept)
- No date column

---

## Statistical Confidence Levels

The system classifies backtest results into three tiers based on universe size:

| Universe Size | Stage | Confidence |
|---------------|-------|------------|
| < 10 symbols | FUNCTIONAL_TEST | INSUFFICIENT |
| 10-49 symbols | SMALL_SAMPLE | INSUFFICIENT |
| 50-99 symbols | BASIC_VALIDATION | OBSERVATIONAL |
| 100-199 symbols | BETTER_VALIDATION | RELIABLE |
| >= 200 symbols | PRODUCTION_LEVEL | RELIABLE |

### INSUFFICIENT

- Sample too small for any strategy conclusions.
- Results confirm only that the code runs correctly.
- Do not draw investment conclusions from INSUFFICIENT results.

### OBSERVATIONAL

- Initial patterns may be visible.
- Not yet sufficient for strategy adjustments.
- Treat as directional indication only.

### RELIABLE

- Sufficient for strategy-adjustment reference.
- Still not investment advice.
- Always verify with out-of-sample data.

---

## How Missing Data Affects formal_allowed

If a symbol is missing any required data type, the corresponding formal_allowed
flag is set to False:

- Missing daily -> short_allowed = False, mid_allowed = False, long_allowed = False
- Missing institutional -> short_allowed = False, mid_allowed = False
- Missing margin -> short_allowed = False, mid_allowed = False
- Missing monthly_revenue -> mid_allowed = False, long_allowed = False
- Missing holder -> mid_allowed = False, long_allowed = False

The data-check and data-audit commands show which conditions each symbol fails.

---

## Common Data Problems and Fixes

| Problem | Symptom | Fix |
|---------|---------|-----|
| Symbol as integer | 0050 becomes 50 | Format column as Text in Excel before export |
| ROC year date | 113/01/02 not parsed | Use clean-csv; the cleaner handles ROC dates |
| Big5 encoding | Garbled Chinese in columns | Re-save as UTF-8 CSV from Excel |
| Thousand separators | 1,234 not parsed as number | Use clean-csv; commas are removed automatically |
| Percentage with % sign | 12.3% not parsed | Use clean-csv; % is removed automatically |
| Blank rows | Empty rows in middle of file | Remove manually before import |
| Duplicate dates | Same symbol+date appears twice | clean-csv drops duplicates, last row kept |
| Negative margin balance | margin_balance < 0 | Check source data; may be a data error |

---

## Recommended Import Volume

| Target | Symbols | Expected Daily Rows |
|--------|---------|---------------------|
| Minimum functional | 50 | ~6,000 (50 x 120 days) |
| Recommended | 100 | ~12,000 (100 x 120 days) |
| Ideal | 200 | ~24,000 (200 x 120 days) |

For institutional, margin: 50 symbols x 40 days = 2,000 rows minimum.
For monthly revenue: 50 symbols x 12 months = 600 rows minimum.
For holder: 50 symbols x 4 periods = 200 rows minimum.

---

## Disclaimer

All data, analysis, and backtest results are for research and simulation only.
They do not constitute investment advice. Past performance does not guarantee
future results. Automated order execution is strictly prohibited in v1.

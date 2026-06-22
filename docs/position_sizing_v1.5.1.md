# Position Sizing v1.5.1

**[!] Research Only. No Real Orders. Production Trading: BLOCKED.**

## Version

- **Version**: 1.5.1
- **Release Name**: Position Sizing
- **Base Release**: 1.5.0.2 Portfolio Research CLI Completeness Hotfix
- **Replay Stable Baseline**: 1.2.9
- **Provider Stable Baseline**: 1.4.9
- **Portfolio Research Baseline**: 1.5.0
- **Position Sizing Baseline**: 1.5.1

## Version Positioning

v1.5.1 is the **research-only position sizing and risk budget engine**.

It answers:
- Given the current portfolio and cash, how much can be allocated?
- Given a maximum per-trade risk limit, how many shares can be purchased?
- Given a stop distance, what is the permissible position size?
- Given ATR/volatility, what is the recommended position size?
- Are single-name, industry, theme, and market caps exceeded?
- After minimum lot size and odd-lot normalization, what is the actual research quantity?
- If data is stale/missing/lineage-incomplete, should sizing be BLOCKED?
- What is the full rationale for every step of the sizing proposal?

## Safety Boundaries (Permanent)

This version **cannot** and **does not**:
- Create buy or sell orders
- Execute orders automatically
- Rebalance the portfolio
- Submit to a broker
- Sync with a live account
- Optimize the full portfolio weight
- Use full Kelly
- Apply leverage, margin, short selling
- Trade options or futures

Every sizing result carries these mandatory labels:
```
RESEARCH_ONLY
NOT_AN_ORDER
NOT_EXECUTABLE
NO_BROKER_CALL
NO_LEDGER_WRITE
NO_AUTO_REBALANCE
```

## Sizing Methods

### A. Fixed Fractional

```
risk_amount = portfolio_value × risk_per_trade_percent
quantity = risk_amount / (entry_price - stop_price)
```

- Long-only: stop_price must be < entry_price
- stop_distance = 0 or stop >= entry → BLOCKED

### B. Stop Distance

```
risk_per_share = entry_price - stop_price
raw_quantity = risk_budget / risk_per_share
```

Supports absolute and percentage distances. Includes fee, tax, and slippage buffers.

### C. ATR Based

```
stop_distance = ATR × atr_multiplier
quantity = risk_budget / stop_distance
```

ATR must have PIT, freshness, and lineage. ATR ≤ 0 → BLOCKED.

### D. Volatility Target (Research Baseline)

```
target_weight = portfolio_vol_budget / asset_volatility
```

**Important limitations**: No covariance matrix, no correlation adjustment, no portfolio optimization claim. Volatility missing → BLOCKED or INSUFFICIENT_DATA.

### E. Fixed Portfolio Weight

```
target_value = portfolio_value × target_weight
incremental_value = target_value - current_market_value
```

If incremental_value ≤ 0 → NO_ADDITIONAL_BUY_REQUIRED. No sell orders generated.

### F. Cash Limited

```
max_cash = available_cash - required_cash_reserve
raw_quantity = max_cash / entry_price
```

Available cash cannot go negative.

## Constraints

Applied in order:
1. Portfolio eligibility
2. Asset support
3. Canonical symbol
4. Price authority & quality
5. Freshness & PIT
6. Lineage
7. Conflict detection
8. Available cash
9. Cash reserve
10. Max order value
11. Single-name weight cap
12. Industry weight cap
13. Theme weight cap
14. Market weight cap
15. ETF limit
16. Liquidity participation limit
17. Lot size normalization
18. Minimum order value
19. Final safety gate

### Single-name Cap

`final_position_value / portfolio_value <= max_single_position_weight`

Incomplete portfolio value → BLOCKED_INCOMPLETE_PORTFOLIO_VALUE.

### Industry Cap

Requires classified industry with lineage, PIT, and effective date.
Unknown industry → shows UNKNOWN, policy decides BLOCK vs WARNING.

### Theme Cap

Overlapping themes are tracked. Most restrictive cap wins.

### Liquidity Cap

`estimated_order_value <= average_daily_traded_value × participation_limit`

ADV must have authority, PIT, freshness, and lineage. Stale ADV → not used formally.

## Lot Normalization

Taiwan stock baseline:
- Standard lot size: 1000 shares
- Odd lots configurable per instrument

Normalization order:
1. Calculate raw quantity
2. Apply caps
3. Round DOWN
4. If allow_odd_lot=False → round down to nearest lot
5. If result < minimum_order_value → return 0
6. Recalculate final risk and weight

**Never round up** — rounding up could exceed risk or cash limits.

## Fee / Tax / Slippage Buffer

Research estimation only. Configurable via policy version with effective date and source.
If rates unknown → assumptions are explicitly shown. Not assumed to be precise.

## Eligibility Gate

Checks before sizing:
- `research_only=True`
- `broker_linked=False`
- `real_order_enabled=False`
- Valid price with primary authority
- Freshness, PIT, lineage
- No blocking conflict
- Cash known, portfolio value complete
- Valid policy, risk budget, stop/ATR/volatility inputs
- Valid classification, liquidity data, lot metadata

Output includes `sizing_allowed`, `methods_allowed`, `methods_blocked`, `warnings`, `blockers`.

## Point-in-Time (PIT)

All inputs must satisfy:

```
available_from <= as_of
```

Not allowed: future price, future ATR, future volatility, future portfolio snapshot, future classification, future liquidity, future corporate action, future policy version.

`fetched_at` is not a substitute for `available_from`.

## Lineage

Every proposal traces back to:
- Sizing request → portfolio snapshot → positions → ledger
- Reference price → provider response → official source
- ATR / volatility / liquidity / classification → source lineage

Stored: portfolio snapshot hash, price lineage, indicator lineage, liquidity lineage, policy version, calculation version, constraint decisions, result hash.

## Explainability

Every proposal includes a step-by-step explanation:
- Requested method, portfolio value, available cash, risk budget
- Entry price, stop/ATR/volatility input
- Raw quantity
- Each constraint's before/after quantity
- Lot normalization
- Final quantity, value, weight
- Risk amount, risk percent
- Binding constraint, blockers, warnings, assumptions

## What-If Analysis

Supports hypothetical scenarios:
- Different stop, entry, risk percent, max weight, cash reserve
- ATR up/down, volatility up/down

All what-if results carry: `HYPOTHETICAL_ONLY`, `NO_LEDGER_WRITE`, `NO_ORDER_CREATED`, `NO_BROKER_CALL`.

## Store

Research-only store for policies and proposals:
- Proposals are immutable
- Idempotent save by proposal_id
- Revision creates new proposal
- No transaction ledger
- No order table
- No broker credentials

## Query Service

Available methods:
- `create_sizing_policy()`, `get_sizing_policy()`, `list_sizing_policies()`
- `evaluate_sizing_eligibility()`
- `size_fixed_fractional()`, `size_by_stop_distance()`, `size_by_atr()`
- `size_by_volatility_target()`, `size_by_target_weight()`, `size_by_cash_limit()`
- `apply_constraints()`, `normalize_lot_size()`, `build_sizing_proposal()`
- `explain_sizing_proposal()`, `run_sizing_what_if()`
- `save_sizing_proposal()`, `get_sizing_proposal()`, `list_sizing_proposals()`
- `get_sizing_lineage()`

**Not available** (permanently blocked): `submit_order`, `execute_order`, `sync_broker`, `apply_to_portfolio`, `auto_rebalance`.

## CLI Commands

All commands are research-only, fixture/demo safe, dry-run, no network required:

| Command | Description |
|---------|-------------|
| `position-sizing-health` | Health check |
| `position-sizing-policies` | List policies |
| `position-sizing-policy-show` | Show policy |
| `position-sizing-eligibility` | Evaluate eligibility |
| `position-sizing-fixed-fractional` | Fixed fractional sizing |
| `position-sizing-stop-distance` | Stop-distance sizing |
| `position-sizing-atr` | ATR-based sizing |
| `position-sizing-volatility` | Volatility target sizing |
| `position-sizing-target-weight` | Target weight sizing |
| `position-sizing-cash-limit` | Cash-limited sizing |
| `position-sizing-constraints` | Apply and show constraints |
| `position-sizing-explain` | Explain a proposal |
| `position-sizing-what-if` | Hypothetical what-if |
| `position-sizing-show` | Show a proposal |
| `position-sizing-list` | List proposals |
| `position-sizing-lineage` | Show proposal lineage |
| `position-sizing-report` | Generate sizing report |

**Not available**: `position-sizing-execute`, `position-sizing-order`, `position-sizing-submit`, `position-sizing-rebalance`.

## GUI

Tab: **Position Sizing** (group: portfolio, priority: P1)

Safety banner displays:
- Research Sizing Only
- Not an Order
- No Broker Connection
- No Auto Apply
- No Auto Rebalance
- Production Trading BLOCKED

Available actions: Refresh, Evaluate Eligibility, Calculate, Explain, Run What-if, View Lineage, Export Report.

**Not available**: Buy, Sell, Submit, Execute, Send to Broker, Apply Position, Auto Rebalance.

## No Broker, No Order, No Ledger Write

- No broker adapter
- No order model
- No execution router
- No live account sync
- No auto rebalance engine

## Known Limitations

1. Volatility target uses simplified formula (no covariance matrix)
2. Industry/theme classification requires pre-populated metadata (not auto-fetched)
3. Liquidity data uses static ADV snapshots (no intraday)
4. Fee/tax/slippage buffers are research estimates only
5. Single-portfolio scope (no cross-portfolio correlation)
6. No optimal portfolio weight allocation (Kelly, MVO, etc.)
7. No drawdown controls (planned for v1.5.3)
8. No walk-forward backtest of sizing (planned for v1.5.4)

## Roadmap

| Version | Name | Status |
|---------|------|--------|
| v1.5.0 | Portfolio Research Foundation | Done |
| v1.5.0.1 | Integrity Hotfix | Done |
| v1.5.0.2 | CLI Completeness Hotfix | Done |
| **v1.5.1** | **Position Sizing** | **Done** |
| v1.5.2 | Correlation & Exposure | Next |
| v1.5.3 | Drawdown & Risk Controls | Planned |
| v1.5.4 | Portfolio Walk-forward Backtest | Planned |
| v1.5.9 | Portfolio Stable Rollup | Planned |

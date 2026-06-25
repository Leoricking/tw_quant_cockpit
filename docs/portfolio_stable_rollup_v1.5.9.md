# Portfolio Stable Rollup v1.5.9

**Release Type:** Freeze / Stabilization  
**Version:** 1.5.9  
**Baseline:** 1.5.4 Portfolio Walk-forward Backtest  
**Status:** STABLE  

> [!] Research Only. No Real Orders. No Broker. Production Trading: BLOCKED.

---

## Purpose

v1.5.9 is a freeze-and-document release. No new research capabilities are added. The goal is to create registries, contracts, manifests, audit tools, and a comprehensive test suite that lock the stable platform state at the v1.5.4 baseline.

---

## Stable Capabilities (6)

| ID | Module | Introduced | Status |
|----|--------|-----------|--------|
| portfolio_foundation | portfolio/ | 1.5.0 | STABLE |
| position_sizing | portfolio/sizing/ | 1.5.1 | STABLE |
| correlation_exposure | portfolio/correlation/ | 1.5.2 | STABLE |
| drawdown_risk_controls | portfolio/risk_controls/ | 1.5.3 | STABLE |
| portfolio_walk_forward | portfolio/walk_forward/ | 1.5.4 | STABLE |
| portfolio_stable_rollup | portfolio/stable_rollup/ | 1.5.9 | STABLE |

---

## Module Structure

```
portfolio/stable_rollup/
    __init__.py
    enums_v159.py               — CapabilityStage, DebtSeverity, etc.
    models_v159.py              — Dataclass definitions (StableCapabilityRecord, ...)
    capability_registry_v159.py — STABLE and PLANNED capability registry
    schema_registry_v159.py     — 33 schema fingerprints (v1.5.0–v1.5.4)
    enum_registry_v159.py       — 13 enum fingerprints
    policy_registry_v159.py     — 9 research-only policies
    cli_registry_v159.py        — CLI command registry validation
    health_registry_v159.py     — 13 health-check records
    release_gate_registry_v159.py — 6 release-gate records
    pit_contract_v159.py        — Point-in-time contract (17 rules)
    lineage_contract_v159.py    — Lineage contract (11 rules)
    reproducibility_contract_v159.py — Reproducibility contract (19 rules)
    safety_contract_v159.py     — Safety contract (13 rules, 6 blocking violations)
    compatibility_registry_v159.py  — Semantic version compatibility
    migration_registry_v159.py  — 8 NO_DATA_MIGRATION_REQUIRED migrations
    stable_manifest_v159.py     — Signed stable-state manifest
    readiness_matrix_v159.py    — Readiness matrix (6 ready, 5 not ready)
    integrity_validator_v159.py — Cross-module integrity validation
    integration_audit_v159.py   — Integration-interface audit (8 checks)
    debt_scanner_v159.py        — Broker-reference / hardcoded-path / whitelist debt scan
    query_v159.py               — StableRollupQueryService (20+ query methods)
    health_v159.py              — PortfolioStableRollupHealthCheck (42 checks)
```

---

## CLI Commands (22 new in v1.5.9)

| Command | Description |
|---------|-------------|
| portfolio-stable-health | Run full health check |
| portfolio-stable-rollup | Run stable rollup summary |
| portfolio-stable-manifest | Build and display stable manifest |
| portfolio-stable-capabilities | List stable capabilities |
| portfolio-stable-schemas | List schema registry |
| portfolio-stable-enums | List enum registry |
| portfolio-stable-policies | List policy registry |
| portfolio-stable-cli-registry | List CLI registry |
| portfolio-stable-health-registry | List health check registry |
| portfolio-stable-release-gates | List release gate registry |
| portfolio-stable-pit-contract | Display PIT contract |
| portfolio-stable-lineage-contract | Display lineage contract |
| portfolio-stable-reproducibility-contract | Display reproducibility contract |
| portfolio-stable-safety-contract | Display safety contract |
| portfolio-stable-compatibility | Display compatibility registry |
| portfolio-stable-migrations | List migration registry |
| portfolio-stable-readiness | Display readiness matrix |
| portfolio-stable-integrity | Run integrity validation |
| portfolio-stable-integration-audit | Run integration audit |
| portfolio-stable-debt-scan | Run debt scan |
| portfolio-stable-explain | Explain stable rollup |
| portfolio-stable-report | Generate full stable rollup report |

Total CLI commands after v1.5.9: 332

---

## Safety Constraints

All outputs are research-only. The following are permanently blocked:

- Real order creation (`REAL_ORDER_CREATION_ENABLED = False`)
- Broker connectivity (`BROKER_CONNECTION_ENABLED = False`)
- Auto-apply / auto-rebalance (`AUTO_APPLY_ENABLED = False`, `AUTO_REBALANCE_ENABLED = False`)
- Live trading (`PRODUCTION_TRADING_BLOCKED = True`)
- Ledger writes from simulation

---

## Tests

- **Test file:** `tests/test_portfolio_stable_rollup_v159.py`
- **Test classes:** 30
- **Tests:** 222
- **Fixtures:** `tests/fixtures/portfolio_stable_rollup/` (34 JSON files)

---

## Known Limitations

- Research-only: all outputs are simulated / historical
- Freeze-only: no new research features added
- No broker connectivity, no real orders, no live trading
- Historical simulation only — past performance does not guarantee future results

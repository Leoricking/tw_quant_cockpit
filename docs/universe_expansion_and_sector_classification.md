# Universe Expansion & Sector Classification — v0.3.25

> **[!] Research Only | No Real Orders | Not Investment Advice | Production BLOCKED**
> All universe configurations are research tools only and must not be used for live trading.

---

## 1. Overview

Version 0.3.25 introduces the **Universe Expansion & Sector Classification** subsystem for the TW Quant Cockpit. This subsystem enables researchers to define, manage, validate, and expand Taiwan stock research universes while maintaining strict safety invariants throughout.

### Key capabilities

- Structured universe registry with named universe groups (core_14 through core_200)
- Sector and theme taxonomy for Taiwan stock classification
- Data-driven universe quality scoring across 6 dimensions
- Expansion proposal engine that suggests candidates without auto-writing
- PySide6 GUI panel integrated into the dashboard
- Universe manifest export (YAML) for reproducibility
- Comprehensive reporting pipeline

### Safety invariants (enforced in every class)

| Property | Value |
|---|---|
| `read_only` | `True` |
| `no_real_orders` | `True` |
| `production_blocked` | `True` |
| `REAL_ORDER_READY` | `False` |
| Strategy changes | None |
| Weight changes | None |

---

## 2. Architecture

```
trading_master/
├── universe/
│   ├── __init__.py                   # Package init
│   ├── universe_registry.py          # Registry engine (load/save/validate/manifest)
│   ├── sector_classifier.py          # Sector & theme classification
│   ├── universe_quality.py           # 6-dimension quality scoring
│   └── universe_expander.py          # Expansion proposal engine
├── reports/
│   └── universe_expansion_report.py  # Markdown report builder
├── gui/
│   ├── universe_manager_panel.py     # PySide6 GUI panel
│   └── universe_manager_adapter.py   # GUI-to-engine bridge
└── config/universe/
    ├── sector_taxonomy.yaml          # Sector/theme taxonomy
    ├── default_universe_seed.csv     # ~60 seed symbols
    ├── universe_manifest.yaml        # Generated manifest
    ├── core_14.csv                   # Built on demand
    ├── core_30.csv
    ├── core_50.csv
    ├── core_100.csv
    ├── core_200.csv
    └── themes/
        ├── ai_mainstream.csv
        ├── semiconductor.csv
        ├── high_speed_interconnect.csv
        ├── server_supply_chain.csv
        ├── power_thermal.csv
        ├── financial.csv
        ├── etf_candidates.csv
        └── institutional_focus.csv
```

### Data flow

```
default_universe_seed.csv
        |
        v
UniverseRegistry.build_default_universes()
        |
        +-----> core_14 / core_30 / core_50 / core_100 / core_200 (CSV)
        +-----> themes/*.csv
        +-----> universe_manifest.yaml
        |
        v
SectorClassifier.classify_universe()
        |
        v
UniverseQualityAnalyzer.run()
        |
        v
UniverseExpander.propose_expansion()
        |
        v
UniverseExpansionReportBuilder.build()
        |
        v
reports/universe_expansion_report_YYYY-MM-DD.md
```

---

## 3. Universe Registry (`universe/universe_registry.py`)

### Purpose

The `UniverseRegistry` class is the central engine for managing named universe configurations. It handles:

- Loading and saving universe CSVs
- Enumerating all known universe groups
- Validating symbol lists (duplicates, missing fields)
- Building default universes from the seed file
- Exporting the universe manifest

### Universe groups

| Group | Description | Min symbols |
|---|---|---|
| `core_14` | Original 14-symbol core | 14 |
| `core_30` | Expanded core | 30 |
| `core_50` | Standard research universe | 50 |
| `core_100` | Extended universe | 100 |
| `core_200` | Full universe | 200 |
| `ai_mainstream` | AI-exposed symbols | varies |
| `semiconductor` | Semiconductor sector | varies |
| `high_speed_interconnect` | PCB/CCL/ABF | varies |
| `server_supply_chain` | Server ODM/parts | varies |
| `power_thermal` | Power/cooling | varies |
| `financial` | Financial sector | varies |
| `etf_candidates` | ETF-eligible symbols | varies |
| `institutional_focus` | Institutional interest | varies |

### CSV schema

```
symbol, name, sector, theme_primary, theme_secondary,
supply_chain_role, ai_exposure, etf_relevance,
institutional_focus, liquidity_tier, market_cap_tier, notes
```

### Key methods

```python
reg = UniverseRegistry()

# List all universe groups with status
universes = reg.list_universes()

# Load rows for a specific universe
rows = reg.load_universe("core_50")

# Get just the symbol list
symbols = reg.get_symbols("core_50")

# Build all default universes from seed
created = reg.build_default_universes(force=False)

# Export manifest YAML
path = reg.export_universe_manifest()

# Validate a universe
result = reg.validate_universe("core_50")
```

### Readiness levels (quick)

| Symbol count | Level |
|---|---|
| >= 100 | BACKTEST_READY |
| >= 50 | RESEARCH_READY |
| >= 10 | OBSERVATIONAL |
| < 10 | INSUFFICIENT |

---

## 4. Sector Classifier (`universe/sector_classifier.py`)

### Purpose

`SectorClassifier` assigns each symbol a sector, theme, and supply chain role. It uses:

1. A built-in known-symbol mapping for 25 core symbols (always accurate)
2. A YAML taxonomy file for keyword-based fallback classification
3. Graceful degradation to built-in taxonomy if YAML is unavailable

### Taxonomy structure

```yaml
semiconductor:
  name: 半導體
  themes: [AI, IC_DESIGN, FOUNDRY, MEMORY, PACKAGING]
  keywords: [半導體, ic設計, 晶圓, 封測]
```

### AI exposure levels

| Level | Meaning |
|---|---|
| HIGH | Direct AI revenue: chips, servers, AI infrastructure |
| MEDIUM | Indirect AI: components used in AI products |
| LOW | Minimal AI exposure: traditional sector |

### Key methods

```python
clf = SectorClassifier()

# Classify a single symbol
result = clf.classify_symbol("2330", name="台積電 TSMC")

# Enrich a list of universe rows
enriched = clf.classify_universe(rows)

# Sector distribution summary
summary = clf.get_sector_summary(enriched)

# Theme/AI exposure summary
theme_summary = clf.get_theme_summary(enriched)

# Validate taxonomy YAML
validation = clf.validate_taxonomy()
```

### Classification output

```python
{
    "symbol":             "2330",
    "name":               "台積電 TSMC",
    "sector":             "semiconductor",
    "theme_primary":      "FOUNDRY",
    "theme_secondary":    "AI",
    "supply_chain_role":  "foundry",
    "ai_exposure":        "HIGH",
    "etf_relevance":      "1",
    "institutional_focus":"1",
    "liquidity_tier":     "LARGE",
    "market_cap_tier":    "LARGE",
}
```

---

## 5. Universe Quality Analyzer (`universe/universe_quality.py`)

### Purpose

`UniverseQualityAnalyzer` scores a universe across 6 dimensions and produces an overall readiness level. This helps researchers understand whether a universe is suitable for observation, research, or backtesting.

### Quality dimensions

| Dimension | Weight | Description |
|---|---|---|
| Coverage | 25% | How many symbols have import data across all 4 datasets |
| Freshness | 20% | Data freshness from `DataFreshnessChecker` |
| Provider Reliability | 20% | Provider health from `ProviderReliabilityMatrix` |
| Sector Balance | 15% | Diversity of sectors; penalizes high concentration |
| Liquidity Readiness | 10% | Ratio of LARGE/MID liquidity tier symbols |
| Backtest Sample Readiness | 10% | Symbol count adequacy for backtesting |

### Readiness levels

| Score | Level |
|---|---|
| >= 90 | STRONG_RESEARCH_UNIVERSE |
| >= 75 | BACKTEST_READY |
| >= 60 | RESEARCH_READY |
| >= 40 | OBSERVATIONAL |
| < 40 | INSUFFICIENT |

### Degradation caps

- < 30 symbols: capped at 59 (max OBSERVATIONAL)
- Coverage < 60: capped at 59
- Freshness < 60: capped at 74 (max RESEARCH_READY)
- Provider reliability < 60: capped at 74

### Usage

```python
from universe.universe_quality import UniverseQualityAnalyzer

analyzer = UniverseQualityAnalyzer(universe_name="core_50")
result = analyzer.run()

print(result["overall_universe_score"])   # e.g., 72.5
print(result["readiness_level"])          # e.g., "RESEARCH_READY"
print(result["recommendations"])          # list of actionable items
```

---

## 6. Universe Expander (`universe/universe_expander.py`)

### Purpose

`UniverseExpander` proposes candidates for expanding a universe. It:

- Reads the source universe and identifies symbols not yet included
- Ranks candidates by AI exposure and data availability
- Returns a proposal dict — does NOT auto-write to config files
- Users apply proposals explicitly via `universe-build-defaults` or `--write` flag

### Ranking criteria

1. AI exposure: HIGH (3 pts) > MEDIUM (2 pts) > LOW (1 pt)
2. Has import data: +3 pts bonus

### Usage

```python
from universe.universe_expander import UniverseExpander

exp = UniverseExpander(source_universe="core_30", target_size=50)
proposal = exp.propose_expansion()

for candidate in proposal["candidates"]:
    print(candidate["symbol"], candidate["data_coverage"], candidate["reason"])
```

### Output structure

```python
{
    "source_universe": "core_30",
    "source_size":     30,
    "target_size":     50,
    "proposed_count":  20,
    "candidates":      [...],
    "note":            "Proposal only — use universe-build-defaults to apply",
    "not_investment_advice": True,
    "read_only":       True,
}
```

---

## 7. Report Builder (`reports/universe_expansion_report.py`)

### Purpose

`UniverseExpansionReportBuilder` assembles data from all four subsystems and writes a structured Markdown report.

### Report sections

| Section | Content |
|---|---|
| 一、總覽 | Mode, universe count, overall readiness |
| 二、Universe List | All 13 universe groups with counts and readiness |
| 三、Sector Distribution | Top sectors, concentration, breakdown table |
| 四、Universe Quality | 6-dimension quality scorecard |
| 五、Expansion Candidates | Top 20 proposed expansion symbols |
| 六、Weakness / Blockers | Missing data, weak sectors, symbol count issues |
| 七、Recommendations | Actionable steps |
| 八、安全聲明 | Safety declaration |

### Output

Reports are written to `reports/universe_expansion_report_YYYY-MM-DD.md`.

### Usage

```python
from reports.universe_expansion_report import UniverseExpansionReportBuilder

builder = UniverseExpansionReportBuilder(
    report_date="2026-05-31",
    universe_data=quality_result,
    registry_data=registry_list,
    expansion_data=expansion_proposal,
    classifier_data=sector_summary,
)
path = builder.build()
```

---

## 8. GUI Panel (`gui/universe_manager_panel.py`)

### Purpose

`UniverseManagerPanel` is a PySide6 QWidget that provides a full GUI for managing research universes within the TW Quant Cockpit dashboard.

### Components

| Component | Description |
|---|---|
| Safety banner | Prominently displays research-only, no-real-orders warnings |
| Universe selector | QComboBox listing all 13 universe groups |
| Symbol count + readiness | Updated on each load |
| Universe table | 10-column table: Symbol, Name, Sector, Theme, Supply Chain Role, Data Coverage, AI Exposure, Liquidity Tier, Notes |
| Sector summary | Single-line sector distribution below the table |
| Quality cards | 6 QGroupBox cards with color-coded scores |
| Empty state | Clear message when no universe is configured |
| Action buttons | 5 buttons: Load, Build Defaults, Analyze Quality, Generate Report, Export Manifest |
| Status bar | Inline status messages |

### Background workers

All long-running operations run in QThread workers to keep the GUI responsive:

| Worker | Operation |
|---|---|
| `_LoadUniverseWorker` | Load and classify universe rows |
| `_BuildDefaultsWorker` | Build all default universe configs |
| `_AnalyzeQualityWorker` | Run quality analysis |
| `_GenerateReportWorker` | Generate full Markdown report |

### Stub mode

When PySide6 is not installed, the module defines a stub `UniverseManagerPanel` class that logs a warning and does nothing. This ensures the rest of the codebase can import without error.

### Integration

```python
from gui.universe_manager_panel import UniverseManagerPanel

panel = UniverseManagerPanel(mode="real")
# panel.status_message.connect(dashboard.set_status)
# panel.report_generated.connect(dashboard.open_report)
```

---

## 9. Configuration Files

### `config/universe/sector_taxonomy.yaml`

Defines sector classifications used by `SectorClassifier`. Structure:

```yaml
sector_key:
  name: Human-readable name (Chinese/English)
  themes: [list of theme constants]
  keywords: [list of match strings for fallback classification]
```

Sectors defined: `semiconductor`, `high_speed_interconnect`, `server_supply_chain`, `power_thermal`, `network`, `financial`, `odm_brand`, `transport`, `traditional`.

### `config/universe/default_universe_seed.csv`

The canonical seed file (~60 symbols) from which all universe groups are derived. Columns:

```
symbol, name, sector, theme_primary, theme_secondary,
supply_chain_role, ai_exposure, etf_relevance,
institutional_focus, liquidity_tier, market_cap_tier, notes
```

Core coverage:
- AI infrastructure: 2330, 2454, 6669, 2382, 2376, 2317, 3231, 2356, 4938, 2357
- Semiconductors: 3661, 5274, 3081, 3228, 3443, 4966, 3711, 2303, 5347, 3034
- High-speed interconnect: 2383, 3037, 8358, 2327, 3533, 6213, 6274, 8046, 3189
- Power/thermal: 2308, 3017, 2301
- Network: 2345, 2379
- Financial: 2881, 2882, 2884, 2885, 2886, 2887, 2888, 2890, 2891, 2892

### `config/universe/universe_manifest.yaml`

Auto-generated by `UniverseRegistry.export_universe_manifest()`. Contains:

```yaml
version: v0.3.25
generated_at: "2026-05-31T..."
read_only: true
no_real_orders: true
research_only: true
not_investment_advice: true
universes:
  core_50:
    symbol_count: 50
    path: config/universe/core_50.csv
  ...
```

---

## 10. CLI Integration

### Building default universes

```bash
python main.py universe-build-defaults
```

Reads `config/universe/default_universe_seed.csv` and writes:
- `config/universe/core_14.csv` through `core_200.csv`
- `config/universe/themes/*.csv` (theme sub-universes)
- `config/universe/universe_manifest.yaml`

### Analyzing universe quality

```bash
python main.py analyze-universe-quality --universe core_50
```

### Generating universe expansion report

```bash
python main.py generate-universe-report --universe core_50
```

Output: `reports/universe_expansion_report_YYYY-MM-DD.md`

### Proposing expansion

```bash
python main.py propose-expansion --source core_30 --target-size 50
```

Proposal only — does not write to config files.

---

## Appendix A: Safety Declaration

| Property | Value |
|---|---|
| `read_only` | `True` in all classes |
| `no_real_orders` | `True` in all classes |
| `production_blocked` | `True` in all classes |
| No token in code | Confirmed — no API tokens hardcoded |
| Research Universe Only | All universes tagged `research_only: True` |
| Not investment advice | All outputs tagged `not_investment_advice: True` |
| No auto trading | System does not place, cancel, or modify orders |
| No auto weight changes | Strategy weights are not modified automatically |

---

## Appendix B: Extending the Seed List

To add symbols to the research universe:

1. Edit `config/universe/default_universe_seed.csv`
2. Add rows following the CSV schema
3. Run `python main.py universe-build-defaults --force`
4. Verify with `python main.py analyze-universe-quality --universe core_50`

Guidelines for new entries:
- Set `ai_exposure` honestly (HIGH only for direct AI revenue)
- Set `etf_relevance=1` for liquid, widely-held AI names
- Set `institutional_focus=1` for symbols with documented institutional ownership
- Use `liquidity_tier=LARGE` only for daily turnover > NT$500M average

---

## Appendix C: Version History

| Version | Changes |
|---|---|
| v0.3.25 | Initial Universe Expansion & Sector Classification subsystem |
| v0.3.22 | Usability QA and smoke tests |
| v0.3.21 | Data quality gate and production readiness score |
| v0.3.20 | Provider auto-fetch and data freshness integration |

---

*Generated: 2026-05-31 | TW Quant Cockpit v0.3.25*
*[!] Research Only | No Real Orders | Not Investment Advice*

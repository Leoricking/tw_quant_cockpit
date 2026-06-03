"""
main.py - CLI entry point for the Taiwan Quantitative Trading Platform.

Commands
--------
download      : Download all stock price data from FinMind
features      : Compute technical features for all stocks
train         : Train the ML ensemble model
backtest      : Run a backtest for a given strategy
pipeline      : Run the full daily pipeline (update → features → predict → report)
report        : Generate / display the latest daily report
ui            : Launch the Streamlit dashboard

TW Quant Cockpit v1 commands
------------------------------
screener      : Run 4-layer Taiwan stock screener, output top 3-8 candidates
cockpit       : Launch TW Quant Cockpit GUI (PySide6)
paper         : Show paper trading positions and P&L
stock-report  : Generate multi-timeframe analysis report for a single stock
mock-realtime : Run mock real-time market data simulation (no Shioaji required)

TW Quant Cockpit v0.2 Phase 4 commands
----------------------------------------
import-csv    : Import XQ/Excel/manual CSV into standard data/import/ structure
data-check    : Check data completeness for a stock or the full universe

TW Quant Cockpit v0.3.3 commands
----------------------------------
clean-csv          : Clean and normalize a CSV file (XQ/Excel) without importing
data-audit         : Audit all imported data for quality and coverage
import-plan        : Show prioritized import plan based on current data gaps

TW Quant Cockpit v0.3.3-hotfix commands
-----------------------------------------
import-xq-export   : One-command import of XQ technical-analysis export files

TW Quant Cockpit v0.3.4 commands
----------------------------------
provider-status      : Show data provider availability (CSV, XQ, TWSE planned, Mega planned)
time-machine-preview : Volume Profile + Microstructure summary for a stock
feature-preview      : Display latest computed features (indicators + volume profile + microstructure)

TW Quant Cockpit v0.3.6 commands
----------------------------------
strategy-preview     : Full Strategy Knowledge Engine (position plan, MACD, volume, valuation, exit)

Usage examples
--------------
    python main.py download
    python main.py features
    python main.py train
    python main.py backtest --strategy momentum
    python main.py backtest --strategy mean_reversion --start 2022-01-01
    python main.py pipeline
    python main.py report
    python main.py ui
    python main.py screener
    python main.py cockpit
    python main.py paper
    python main.py stock-report --stock 2330
    python main.py mock-realtime
"""

import argparse
import logging
import os
import sys
from datetime import date, datetime

# Force UTF-8 output on Windows so Chinese characters display correctly
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---- Setup path so all sub-packages resolve correctly -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DASH = '\u2014'   # em dash safe outside f-string expressions
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config

# ---- Logging setup -------------------------------------------------------

def _setup_logging(level: str = "INFO") -> None:
    """Configure root logger with a consistent format."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_download(args: argparse.Namespace) -> None:
    """Download stock price data from FinMind."""
    from data.downloader import download_all_stocks
    from data.database import initialize_db

    initialize_db()
    logger = logging.getLogger("main.download")
    logger.info("Starting full data download.")

    stocks = args.stocks if hasattr(args, "stocks") and args.stocks else config.STOCK_UNIVERSE
    start = args.start if hasattr(args, "start") and args.start else config.DEFAULT_START_DATE
    end = args.end if hasattr(args, "end") and args.end else date.today().strftime("%Y-%m-%d")

    logger.info("Stocks: %d | Start: %s | End: %s", len(stocks), start, end)

    rows = download_all_stocks(
        stock_ids=stocks,
        start_date=start,
        end_date=end,
    )
    logger.info("Download complete. %d rows saved.", rows)


def cmd_features(args: argparse.Namespace) -> None:
    """Compute and persist all technical features."""
    from pipeline.daily import compute_all_features

    logger = logging.getLogger("main.features")
    logger.info("Computing features.")

    start = args.start if hasattr(args, "start") and args.start else config.DEFAULT_START_DATE
    end = args.end if hasattr(args, "end") and args.end else date.today().strftime("%Y-%m-%d")

    df = compute_all_features(start_date=start, end_date=end, save_to_db=True)

    if df.empty:
        logger.error("Feature computation returned empty DataFrame. Check that price data exists.")
        sys.exit(1)

    logger.info("Features computed for %d stock-days.", len(df))


def cmd_train(args: argparse.Namespace) -> None:
    """Train the ML ensemble model."""
    from models.trainer import run_training

    logger = logging.getLogger("main.train")
    logger.info("Starting model training.")

    start = args.start if hasattr(args, "start") and args.start else config.DEFAULT_START_DATE
    end = args.end if hasattr(args, "end") and args.end else date.today().strftime("%Y-%m-%d")

    summary = run_training(
        start_date=start,
        end_date=end,
        validate=True,
        save_model=True,
    )

    if summary.get("status") == "failed":
        logger.error("Training failed: %s", summary.get("reason"))
        sys.exit(1)

    logger.info("Training complete. Summary:")
    for k, v in summary.items():
        if k != "metrics":
            logger.info("  %s: %s", k, v)
    if "metrics" in summary:
        logger.info("  Metrics: %s", summary["metrics"])


def cmd_backtest(args: argparse.Namespace) -> None:
    """Run a backtest for the specified strategy."""
    from backtest.engine import BacktestEngine
    from data.database import initialize_db
    from features.indicators import compute_indicators
    from features.volatility import compute_volatility
    from features.momentum import compute_momentum
    from features.regime import detect_regime
    from data.database import load_features, load_prices

    logger = logging.getLogger("main.backtest")
    initialize_db()

    strategy_name = getattr(args, "strategy", "momentum")
    start = getattr(args, "start", None) or config.DEFAULT_START_DATE
    end = getattr(args, "end", None) or date.today().strftime("%Y-%m-%d")
    walk_fwd = getattr(args, "walk_forward", False)

    logger.info("Backtesting strategy: %s | %s → %s", strategy_name, start, end)

    # Load feature data
    feature_df = load_features(start_date=start, end_date=end)

    if feature_df.empty:
        logger.warning("No features in DB. Trying to compute from prices.")
        from pipeline.daily import compute_all_features
        feature_df = compute_all_features(start_date=start, end_date=end, save_to_db=False)

    if feature_df.empty:
        logger.error(
            "No data available. Run 'python main.py download' and "
            "'python main.py features' first."
        )
        sys.exit(1)

    # Build strategy instance
    if strategy_name == "momentum":
        from strategies.momentum import MomentumStrategy
        strategy = MomentumStrategy()
    elif strategy_name == "mean_reversion":
        from strategies.mean_reversion import MeanReversionStrategy
        strategy = MeanReversionStrategy()
    elif strategy_name == "breakout":
        from strategies.breakout import BreakoutStrategy
        strategy = BreakoutStrategy()
    else:
        logger.error("Unknown strategy: %s. Choose: momentum, mean_reversion, breakout", strategy_name)
        sys.exit(1)

    if walk_fwd:
        # Walk-forward validation
        from backtest.walk_forward import run_walk_forward, summarise_walk_forward

        logger.info("Running walk-forward validation.")
        wf_results = run_walk_forward(
            feature_df=feature_df,
            strategy_factory=lambda: type(strategy)(),
        )
        summary_text = summarise_walk_forward(wf_results)
        print(summary_text)
    else:
        # Single backtest
        engine = BacktestEngine(strategy=strategy, initial_capital=config.INITIAL_CAPITAL)
        results = engine.run(feature_df)

        print("\n" + "=" * 55)
        print(f"  Backtest Results: {strategy_name.replace('_', ' ').title()}")
        print("=" * 55)
        for k, v in results.items():
            if k in ("trades", "portfolio_history"):
                continue
            if isinstance(v, float):
                if k in ("total_return", "annualised_return", "max_drawdown", "win_rate"):
                    print(f"  {k:<25}: {v:+.2%}")
                elif k in ("sharpe_ratio", "profit_factor"):
                    print(f"  {k:<25}: {v:.4f}")
                else:
                    print(f"  {k:<25}: {v:.4f}")
            else:
                print(f"  {k:<25}: {v}")

        # KPI check
        kpi_check = engine.meets_kpi_targets(results)
        print("\n  KPI Target Assessment:")
        for kpi, info in kpi_check.items():
            status = "PASS" if info["passed"] else "FAIL"
            print(f"  [{status}] {kpi}: {info['value']:.4f} (target {info['target']})")


def cmd_pipeline(args: argparse.Namespace) -> None:
    """Run the full daily pipeline."""
    from pipeline.daily import run_daily_pipeline

    logger = logging.getLogger("main.pipeline")
    logger.info("Running daily pipeline.")

    target_date = getattr(args, "date", None) or date.today().strftime("%Y-%m-%d")
    update = not getattr(args, "no_update", False)

    result = run_daily_pipeline(target_date=target_date, update_data=update)

    print("\n" + "=" * 55)
    print("  Daily Pipeline Result")
    print("=" * 55)
    print(f"  Date     : {result.get('date')}")
    print(f"  Status   : {result.get('status')}")
    print(f"  Regime   : {result.get('regime')} / {result.get('vol_regime')}")
    print(f"  Strategy : {result.get('selected_strategy')}")

    picks = result.get("picks", None)
    if picks is not None and not picks.empty:
        print(f"\n  Top {min(10, len(picks))} Picks:")
        print(f"  {'StockID':>10} {'Score':>8} {'PredRet':>10} {'UpProb':>7}")
        for _, row in picks.head(10).iterrows():
            sid = row.get("stock_id", "N/A")
            score = row.get("composite_score", float("nan"))
            pred_ret = row.get("predicted_return", float("nan"))
            up_prob = row.get("up_probability", float("nan"))
            score_s = f"{score:.4f}" if not pd.isna(score) else "   N/A"
            ret_s = f"{pred_ret:+.2%}" if not pd.isna(pred_ret) else "    N/A"
            prob_s = f"{up_prob:.1%}" if not pd.isna(up_prob) else "  N/A"
            print(f"  {sid:>10} {score_s:>8} {ret_s:>10} {prob_s:>7}")

    if result.get("errors"):
        print(f"\n  Errors: {result['errors']}")

    # Print report to console
    report = result.get("report")
    if report:
        print("\n" + report)


def cmd_report(args: argparse.Namespace) -> None:
    """Display the latest saved report."""
    from data.database import load_report, list_report_dates, initialize_db

    initialize_db()
    logger = logging.getLogger("main.report")

    target_date = getattr(args, "date", None)
    if not target_date:
        dates = list_report_dates()
        if not dates:
            logger.error("No reports found. Run 'python main.py pipeline' first.")
            sys.exit(1)
        target_date = dates[0]
        logger.info("Loading latest report for %s.", target_date)

    text = load_report(target_date)
    if text:
        print(text)
    else:
        logger.error("No report found for date %s.", target_date)

        # Try to generate one on the fly
        from reports.generator import generate_daily_report
        from data.database import load_predictions, save_report

        preds = load_predictions(date=target_date)
        report = generate_daily_report(
            date=target_date,
            regime="unknown",
            vol_regime="low",
            strategy_name="momentum",
            picks=preds,
        )
        print(report)
        save_report(target_date, report)


def cmd_ui(_args: argparse.Namespace) -> None:
    """Launch the Streamlit dashboard."""
    import subprocess

    dashboard_path = os.path.join(BASE_DIR, "ui", "dashboard.py")
    logger = logging.getLogger("main.ui")
    logger.info("Launching Streamlit dashboard at %s.", dashboard_path)

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", dashboard_path],
        check=True,
    )


# ---------------------------------------------------------------------------
# TW Quant Cockpit v1 command handlers
# ---------------------------------------------------------------------------

def cmd_screener(args: argparse.Namespace) -> None:
    """Run the 4-layer Taiwan stock screener and print top candidates."""
    from screener.screener_pipeline import ScreenerPipeline

    logger = logging.getLogger("main.screener")
    mode = getattr(args, 'mode', 'mock')
    logger.info("Running Taiwan stock screener... [mode=%s]", mode)

    top_n = getattr(args, "top", 8)
    pipeline = ScreenerPipeline()
    pipeline.run(mode=mode)
    result = pipeline.get_top_candidates(n=top_n)

    # get_top_candidates may return a DataFrame or a list of dicts
    import pandas as pd
    if isinstance(result, pd.DataFrame):
        if result.empty:
            candidates = []
        else:
            candidates = result.to_dict(orient='records')
    else:
        candidates = list(result) if result is not None else []

    if not candidates:
        print("No candidates found. Check theme pool CSV files in config/theme_pools/")
        return

    _mlabel = 'MOCK DATA' if mode == 'mock' else 'REAL CSV'
    print("\n" + "=" * 70)
    print(f"  TW Quant Cockpit v1 — 飆股候選篩選結果 (Top {len(candidates)}) [{_mlabel}]")
    print("=" * 70)
    print(f"  {'代號':>6}  {'名稱':<8}  {'分數':>6}  {'主題':<20}  建議")
    print("-" * 70)

    for c in candidates:
        sym    = str(c.get('symbol', ''))
        name   = str(c.get('name', ''))
        score  = float(c.get('bull_stock_score', 0))
        themes_raw = c.get('theme_tags', [])
        if isinstance(themes_raw, str):
            themes = themes_raw
        elif themes_raw:
            themes = ','.join(themes_raw)
        else:
            themes = '-'
        decision = str(c.get('decision', '-'))
        print(f"  {sym:>6}  {name:<8}  {score:>6.1f}  {themes:<20}  {decision}")

    print("=" * 70)
    print("\n[Score] 80+ Bull candidate | 65-79 Strong watch | 50-64 Wait | <50 Avoid")
    print("[!] For research and simulation only. Not investment advice.")


def cmd_cockpit(args: argparse.Namespace) -> None:
    """Launch the TW Quant Cockpit PySide6 GUI."""
    logger = logging.getLogger("main.cockpit")
    mode = getattr(args, 'mode', 'mock')
    logger.info("Launching TW Quant Cockpit GUI [mode=%s]...", mode)

    try:
        from gui.dashboard import launch
        launch(mode=mode)
    except ImportError as exc:
        logger.error("Failed to import gui.dashboard: %s", exc)
        print("ERROR: PySide6 may not be installed. Run: pip install PySide6")
        sys.exit(1)


def cmd_paper(args: argparse.Namespace) -> None:
    """Show paper trading positions and performance summary."""
    logger = logging.getLogger("main.paper")
    logger.info("Paper trading summary.")

    try:
        from sim.simulator import PaperTrader
        trader = PaperTrader(initial_capital=1_000_000)

        # Try to load persisted state if available
        state_path = os.path.join(BASE_DIR, "data", "paper_state.json")
        if os.path.isfile(state_path):
            try:
                import json
                with open(state_path) as f:
                    state = json.load(f)
                logger.info("Loaded paper state from %s", state_path)
            except Exception as exc:
                logger.warning("Could not load paper state: %s", exc)
                state = {}
        else:
            logger.info("No saved paper state found at %s — showing empty portfolio.", state_path)
            state = {}

        print("\n" + "=" * 60)
        print("  TW Quant Cockpit v1 — 模擬持倉 & 績效")
        print("=" * 60)
        print("  初始資金: NTD 1,000,000")

        positions = []
        if hasattr(trader, 'get_positions'):
            positions = trader.get_positions()

        if not positions:
            print("  目前無持倉。使用 `python main.py cockpit` 開啟 GUI 操作模擬單。")
        else:
            print(f"\n  {'代號':>6}  {'均成本':>8}  {'持倉':>6}  {'浮動損益':>10}")
            print("-" * 45)
            for p in positions:
                sym   = str(p.get('symbol', ''))
                cost  = float(p.get('avg_cost', 0))
                qty   = int(p.get('quantity', 0))
                upnl  = float(p.get('unrealized_pnl', 0))
                print(f"  {sym:>6}  {cost:>8.1f}  {qty:>6}  {upnl:>+10,.0f}")

        pnl = {}
        if hasattr(trader, 'get_pnl_summary'):
            pnl = trader.get_pnl_summary()

        total_pnl = pnl.get('realized_pnl', 0) + pnl.get('unrealized_pnl', 0)
        print(f"\n  已實現損益: NTD {pnl.get('realized_pnl', 0):+,.0f}")
        print(f"  未實現損益: NTD {pnl.get('unrealized_pnl', 0):+,.0f}")
        print(f"  合計損益:   NTD {total_pnl:+,.0f}")
        print("=" * 60)
        print("[!] v1: No real order execution. For research and simulation only.")

    except Exception as exc:
        logger.error("Paper trading command failed: %s", exc)
        print(f"ERROR: {exc}")
        sys.exit(1)


def cmd_stock_report(args: argparse.Namespace) -> None:
    """Generate a multi-timeframe analysis report for a single stock."""
    from analysis.stock_report_builder import StockReportBuilder

    logger = logging.getLogger("main.stock_report")

    stock = getattr(args, 'stock', None)
    if not stock:
        logger.error("--stock is required. Example: python main.py stock-report --stock 2330")
        sys.exit(1)

    mode = getattr(args, 'mode', 'mock')
    logger.info("Building stock report for: %s [mode=%s]", stock, mode)

    try:
        sym = str(stock)

        # Load all real data via RealDataLoader (real mode) or DataSourceRouter (mock mode)
        from data.data_source_router import DataSourceRouter
        router = DataSourceRouter(mode=mode)

        stock_name = None
        price_data = None
        chip_data = None
        fundamental_data = None
        data_sources = None

        if mode == 'real':
            from data.real_data_loader import RealDataLoader
            loader = RealDataLoader()
            all_data = loader.load_all(sym)
            data_sources = all_data.get('_sources')
            profile = all_data.get('profile')
            if profile:
                stock_name = profile.get('name')
            _dk = all_data.get('daily_k')               # dict with 'bars' key, or None
            price_data = _dk.get('bars') if _dk else None
            chip_data = all_data.get('institutional')   # dict or None
            fundamental_data = all_data.get('fundamental')  # dict or None
            logger.info("Real data loaded for %s: price=%s bars, chip=%s, fundamental=%s",
                        sym,
                        len(price_data) if price_data else 0,
                        'yes' if chip_data else 'no',
                        'yes' if fundamental_data else 'no')
        else:
            price_data = router.get_price_data(sym, n_bars=60)
            chip_data = router.get_chip_data(sym)

        # Resolve stock name: profile CSV → _STOCK_NAMES fallback
        if not stock_name:
            from screener.screener_pipeline import _STOCK_NAMES
            stock_name = _STOCK_NAMES.get(sym, sym)

        from analysis.daytrade_analyzer import DaytradeAnalyzer
        from analysis.short_term_analyzer import ShortTermAnalyzer
        from analysis.mid_term_analyzer import MidTermAnalyzer
        from analysis.long_term_analyzer import LongTermAnalyzer

        daytrade_result = None
        short_result = None
        mid_result = None
        long_result = None

        try:
            daytrade_result = DaytradeAnalyzer().analyze(
                symbol=sym, price_data=price_data, mode=mode)
        except Exception as exc:
            logger.warning("DaytradeAnalyzer failed: %s", exc)

        try:
            short_result = ShortTermAnalyzer().analyze(
                symbol=sym, price_data=price_data, chip_data=chip_data,
                fundamental_data=fundamental_data, mode=mode)
        except Exception as exc:
            logger.warning("ShortTermAnalyzer failed: %s", exc)

        # Extract fundamental scalar fields for analyzer params
        _fd = fundamental_data or {}
        _eps_ttm = _fd.get('eps_ttm')
        _gross_margin = _fd.get('gross_margin')
        _operating_margin = _fd.get('operating_margin')
        _fundamental_ready = bool(fundamental_data and (_eps_ttm is not None or _gross_margin is not None))
        _announcement_date = _fd.get('announcement_date')
        _ann_is_estimated = bool(_fd.get('announcement_date_is_estimated', False))

        try:
            mid_result = MidTermAnalyzer().analyze(
                symbol=sym, price_data=price_data, chip_data=chip_data,
                fundamental_data=fundamental_data,
                eps_ttm=_eps_ttm, gross_margin=_gross_margin,
                operating_margin=_operating_margin, mode=mode)
        except Exception as exc:
            logger.warning("MidTermAnalyzer failed: %s", exc)

        try:
            long_result = LongTermAnalyzer().analyze(
                symbol=sym, price_data=price_data,
                fundamental_data=fundamental_data,
                eps_ttm=_eps_ttm, gross_margin=_gross_margin,
                operating_margin=_operating_margin,
                fundamental_ready=_fundamental_ready,
                announcement_date=_announcement_date,
                announcement_date_is_estimated=_ann_is_estimated,
                mode=mode)
        except Exception as exc:
            logger.warning("LongTermAnalyzer failed: %s", exc)

        # Align formal gating with DataQualityChecker rules (real mode only)
        if mode == 'real':
            _dk_data = all_data.get('daily_k')
            _daily_rows = len(_dk_data.get('bars', [])) if _dk_data else 0
            _inst_rows = len((all_data.get('institutional') or {}).get('rows', []))
            _margin_rows = len((all_data.get('margin') or {}).get('rows', []))
            _rev_rows = len((all_data.get('monthly_revenue') or {}).get('rows', []))
            _holder_rows = len((all_data.get('holder') or {}).get('rows', []))
            _mid_formal = (
                _daily_rows >= 60 and _rev_rows >= 6
                and _inst_rows >= 5 and _margin_rows >= 5 and _holder_rows >= 2
            )
            _long_formal = _daily_rows >= 120 and _rev_rows >= 12 and _holder_rows >= 2
            _no_formal_msg = '資料不足，禁止正式判斷'
            if mid_result is not None:
                mid_result['formal_allowed'] = _mid_formal
                if not _mid_formal:
                    mid_result['add_position_price'] = None
                    mid_result['exit_price'] = None
                    mid_result['stop_loss_price'] = None
                    if _no_formal_msg not in mid_result.get('no_entry_conditions', []):
                        mid_result.setdefault('no_entry_conditions', []).append(_no_formal_msg)
            if long_result is not None:
                long_result['formal_allowed'] = _long_formal
                if not _long_formal:
                    long_result['add_position_price'] = None
                    long_result['exit_price'] = None
                    long_result['stop_loss_price'] = None
                    if _no_formal_msg not in long_result.get('no_entry_conditions', []):
                        long_result.setdefault('no_entry_conditions', []).append(_no_formal_msg)

        # Build Strategy Knowledge Engine signals for Section 9
        strategy_signals = None
        try:
            import pandas as _pd
            if price_data:
                _df = _pd.DataFrame(price_data)
                if "date" in _df.columns:
                    _df["date"] = _pd.to_datetime(_df["date"])
                    _df = _df.sort_values("date").reset_index(drop=True)
                if len(_df) >= 10:
                    from analysis.strategy_knowledge_engine import build_strategy_signals
                    strategy_signals = build_strategy_signals(
                        df=_df, symbol=sym,
                        eps_ttm=_eps_ttm,
                        trailing_eps=_eps_ttm,
                        gross_margin=_gross_margin,
                        operating_margin=_operating_margin,
                    )
        except Exception as _exc:
            logger.warning("strategy_knowledge_engine skipped: %s", _exc)

        builder = StockReportBuilder()
        report = builder.build(
            symbol=sym,
            name=stock_name,
            mode=mode,
            daytrade_result=daytrade_result,
            short_result=short_result,
            mid_result=mid_result,
            long_result=long_result,
            data_sources=data_sources,
            strategy_signals=strategy_signals,
        )

        # Print to console
        print(report)

        # Optionally save to file
        out_dir = os.path.join(BASE_DIR, "data", "reports")
        os.makedirs(out_dir, exist_ok=True)
        from datetime import date as _date
        filename = f"report_{stock}_{_date.today()}.md"
        out_path = os.path.join(out_dir, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info("Report saved to: %s", out_path)
        print(f"\n[報告已儲存至 {out_path}]")

    except Exception as exc:
        logger.error("stock-report failed: %s", exc)
        print(f"ERROR: {exc}")
        sys.exit(1)


def cmd_import_csv(args: argparse.Namespace) -> None:
    """Import a CSV file into the standard data/import/ structure."""
    from data.csv_importer import CSVImporter

    logger = logging.getLogger("main.import_csv")

    data_type = getattr(args, 'type', None)
    file_path = getattr(args, 'file', None)
    replace = getattr(args, 'replace', False)

    if not data_type:
        logger.error("--type is required.")
        sys.exit(1)
    if not file_path:
        logger.error("--file is required.")
        sys.exit(1)

    append = not replace
    importer = CSVImporter()
    result = importer.import_csv(data_type=data_type, file_path=file_path, append=append)

    print("\n" + "=" * 55)
    print("  TW Quant Cockpit — CSV 匯入")
    print("=" * 55)
    print(f"  匯入類型：{result['data_type']}")
    print(f"  輸入檔案：{result['input_file']}")
    print(f"  輸出檔案：{result['output_file']}")
    print(f"  匯入筆數：{result['rows_imported']}")
    print(f"  總筆數：  {result['rows_total']}")
    missing = result.get('missing_columns', [])
    print(f"  缺少欄位：{missing if missing else '無'}")
    warnings = result.get('warnings', [])
    if warnings:
        for w in warnings:
            print(f"  警告：{w}")
    else:
        print("  警告：無")
    status = "[OK] 成功" if result['success'] else "[FAIL] 失敗"
    print(f"  狀態：{status}")
    print("=" * 55)

    if not result['success']:
        sys.exit(1)


def cmd_data_check(args: argparse.Namespace) -> None:
    """Check data completeness for a stock or the entire universe."""
    from data.data_quality_checker import DataQualityChecker

    logger = logging.getLogger("main.data_check")

    stock = getattr(args, 'stock', None)
    check_all = getattr(args, 'all', False)

    checker = DataQualityChecker()

    if stock:
        result = checker.check_stock(str(stock))

        print("\n" + "=" * 55)
        print("  TW Quant Cockpit Data Check")
        print("=" * 55)
        print(f"\n  股票：{result['symbol']} {result['name']}\n")

        def _ok(val, threshold):
            return "OK" if val >= threshold else f"不足（需 {threshold} 筆）"

        profile_status = "OK" if result['profile_ok'] else "缺少"
        print(f"  Profile:          {profile_status}")
        print(f"  Daily K:          {result['daily_rows']} rows  {_ok(result['daily_rows'], 20)}")
        print(f"  Institutional:    {result['institutional_rows']} rows  {_ok(result['institutional_rows'], 5)}")
        print(f"  Margin:           {result['margin_rows']} rows  {_ok(result['margin_rows'], 5)}")
        print(f"  Monthly Revenue:  {result['monthly_revenue_rows']} rows  {_ok(result['monthly_revenue_rows'], 6)}")
        print(f"  Holder:           {result['holder_rows']} rows  {_ok(result['holder_rows'], 2)}")
        print(f"  Trust Cost:       {result['trust_cost_rows']} rows  {_ok(result['trust_cost_rows'], 3)}")

        print("\n  正式判斷允許：")
        dt_note = "否，缺 intraday / bidask" if not result['daytrade_allowed'] else "是"
        print(f"  當沖：{dt_note}")
        print(f"  短線：{'是' if result['short_allowed'] else '否'}")
        print(f"  中線：{'是' if result['mid_allowed'] else '否'}")
        print(f"  長線：{'是' if result['long_allowed'] else '否'}")

        missing = [m for m in result['missing'] if m not in ('intraday', 'bidask')]
        if missing:
            print("\n  缺失資料：")
            for m in missing:
                print(f"  - {m}")

        recs = result.get('recommendations', [])
        if recs:
            print("\n  建議：")
            for r in recs:
                print(f"  - {r}")

        print("=" * 55)

    elif check_all:
        logger.info("Checking full universe...")
        df = checker.check_universe()

        if df is None or (hasattr(df, 'empty') and df.empty):
            print("No stocks found in profile CSV. Run import-csv --type profile first.")
            return

        print("\n" + "=" * 95)
        print("  TW Quant Cockpit Data Check — Universe")
        print("=" * 95)
        print(f"  {'代號':>6}  {'名稱':<8}  {'日K':>5}  {'法人':>5}  {'融資':>5}  "
              f"{'月收':>5}  {'大戶':>5}  {'投信成':>6}  短 中 長  缺失數")
        print("  " + "-" * 85)

        for _, row in df.iterrows():
            sym    = str(row.get('symbol', ''))
            name   = str(row.get('name', ''))[:8]
            daily  = int(row.get('daily_rows', 0))
            inst   = int(row.get('institutional_rows', 0))
            margin = int(row.get('margin_rows', 0))
            rev    = int(row.get('monthly_revenue_rows', 0))
            holder = int(row.get('holder_rows', 0))
            tc     = int(row.get('trust_cost_rows', 0))
            s      = 'Y' if row.get('short_ready', row.get('short_allowed')) else 'N'
            m      = 'Y' if row.get('mid_ready',   row.get('mid_allowed'))   else 'N'
            l      = 'Y' if row.get('long_ready',  row.get('long_allowed'))  else 'N'
            mc     = int(row.get('missing_count', 0))
            print(f"  {sym:>6}  {name:<8}  {daily:>5}  {inst:>5}  {margin:>5}  "
                  f"{rev:>5}  {holder:>5}  {tc:>6}  {s} {m} {l}  {mc:>4}")

        short_ready = int(df.get('short_ready', df.get('short_allowed', [])).sum()) if len(df) else 0
        mid_ready   = int(df.get('mid_ready',   df.get('mid_allowed',   [])).sum()) if len(df) else 0
        long_ready  = int(df.get('long_ready',  df.get('long_allowed',  [])).sum()) if len(df) else 0

        print("=" * 95)
        print(f"  Total symbols : {len(df)}")
        print(f"  Short-ready   : {short_ready}")
        print(f"  Mid-ready     : {mid_ready}")
        print(f"  Long-ready    : {long_ready}")
        print(f"  Y=formal analysis allowed  N=data insufficient")
        print("=" * 95)

        # --- Universe Expansion Status ---
        try:
            from data.universe_expansion_guide import UniverseExpansionGuide
            guide  = UniverseExpansionGuide()
            result = guide.analyze()
            sym    = result['symbol_count']
            stage  = result['confidence_stage']
            ms     = result['missing_summary']
            dc     = result.get('data_coverage', {})
            print("")
            print("  Universe Expansion Status")
            print("  " + "-" * 60)
            print(f"  Current symbols      : {sym}")
            print(f"  Validation stage     : {stage}")
            print(f"  Min validation target: {result['target_min_symbols']}")
            print(f"  Recommended target   : {result['target_recommended_symbols']}-200")
            print(f"  Short-term OK        : {result['complete_short_count']} symbols")
            print(f"  Mid-term OK          : {result['complete_mid_count']} symbols")
            print(f"  Long-term OK         : {result['complete_long_count']} symbols")
            print("")
            print("  Data coverage (threshold met):")
            print(f"  daily >= 120         : {dc.get('daily_120', 0)} symbols")
            print(f"  institutional >= 40  : {dc.get('institutional_40', 0)} symbols")
            print(f"  margin >= 40         : {dc.get('margin_40', 0)} symbols")
            print(f"  revenue >= 12        : {dc.get('revenue_12', 0)} symbols")
            print(f"  holder >= 4          : {dc.get('holder_4', 0)} symbols")
            print(f"  trust_cost >= 20     : {dc.get('trust_cost_20', 0)} symbols")
            print("")
            print("  Missing data gaps:")
            for key, count in ms.items():
                status = f"missing in {count} symbols" if count else "all present"
                print(f"  {key:<22}: {status}")
            print("")
            if sym < 50:
                print("  Recommended next import:")
                print("  - python main.py build-universe --template top50 --replace")
                print("  - Import daily K (>= 120 days per symbol)")
            elif sym < 100:
                print("  Recommended next import:")
                print("  - python main.py build-universe --template top100")
                print("  - Supplement holder / trust_cost data")
            else:
                print("  Universe adequate for validate-score. Check industry bias.")
            print("=" * 95)
        except Exception as _ue:
            logger.debug("universe expansion guide error: %s", _ue)

    else:
        print("請指定 --stock <代號> 或 --all")
        sys.exit(1)


def cmd_mock_realtime(args: argparse.Namespace) -> None:
    """Run mock real-time market data simulation (no Shioaji account required)."""
    import time

    logger = logging.getLogger("main.mock_realtime")

    try:
        from broker.mock_broker import MockBroker

        wl = os.path.join(BASE_DIR, "config", "watchlist.csv")
        broker = MockBroker(watchlist_path=wl)

        symbols = broker._symbols[:10]   # cap at 10 for console demo
        duration = getattr(args, 'duration', 60)
        interval = getattr(args, 'interval', 2)

        print("\n" + "=" * 70)
        print("  TW Quant Cockpit v1 — Mock Realtime 模擬行情 (無需 Shioaji)")
        print(f"  監控 {len(symbols)} 檔 | 更新間隔 {interval}s | 執行 {duration}s | Ctrl+C 停止")
        print("=" * 70)

        start_time = time.time()
        tick_num = 0

        while time.time() - start_time < duration:
            tick_num += 1
            elapsed = time.time() - start_time
            remaining = duration - elapsed

            print(f"\n  --- 更新 #{tick_num}  {datetime.now().strftime('%H:%M:%S')}  "
                  f"(剩餘 {remaining:.0f}s) ---")
            print(f"  {'代號':>6}  {'名稱':<8}  {'價格':>8}  {'漲跌%':>8}  "
                  f"{'委買1':>8}  {'委賣1':>8}  {'成交量':>10}")
            print("  " + "-" * 65)

            for sym in symbols:
                try:
                    snap = broker.get_snapshot(sym)
                    name  = snap.get('name', sym)
                    price = snap.get('price', 0)
                    chg   = snap.get('change_pct', 0)
                    bid1  = snap.get('bid_1', snap.get('bid_price_1', 0))
                    ask1  = snap.get('ask_1', snap.get('ask_price_1', 0))
                    vol   = snap.get('volume', 0)
                    arrow = '▲' if chg > 0 else ('▼' if chg < 0 else ' ')
                    print(f"  {sym:>6}  {name:<8}  {price:>8.1f}  "
                          f"{arrow}{abs(chg):>6.2f}%  {bid1:>8.1f}  {ask1:>8.1f}  {vol:>10,}")
                except Exception as exc:
                    logger.debug("Snapshot error for %s: %s", sym, exc)

            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                break

        print("\n[Mock Realtime 結束]")
        print("[!] For research and simulation only. Not investment advice.")

    except Exception as exc:
        logger.error("mock-realtime failed: %s", exc)
        print(f"ERROR: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# v0.3 — Score / Buy-Point / Screener Validation Commands
# ---------------------------------------------------------------------------

def cmd_validate_score(args: argparse.Namespace) -> None:
    """Validate bull_stock_score effectiveness against historical forward returns."""
    logger = logging.getLogger("main.validate_score")
    mode   = getattr(args, 'mode',   'real')
    start  = getattr(args, 'start',  None)
    end    = getattr(args, 'end',    None)
    top_n  = getattr(args, 'top',    8)
    output = getattr(args, 'output', None)
    logger.info("validate-score [mode=%s start=%s end=%s]", mode, start, end)

    try:
        from backtest.score_validation import ScoreValidator
        from reports.score_validation_report import ScoreValidationReport

        sv      = ScoreValidator(mode=mode, start=start, end=end, top_n=top_n)
        results = sv.run()

        status = results.get('status')
        if status == 'insufficient_data':
            print(results.get('message', '資料不足，無法完成可靠統計。'))
            return

        paths = sv.save_results(results, output_dir=output)
        rpt   = ScoreValidationReport(results)
        rpt_path = rpt.save()

        print("\n" + "=" * 60)
        print("  TW Quant Cockpit — Score Validation Results")
        print("=" * 60)
        src_tag = 'REAL CSV SAMPLE' if results.get('is_sample') else 'REAL CSV'
        conf    = results.get('confidence', {})
        _s = results.get('start', _DASH)
        _e = results.get('end',   _DASH)
        print(f"  Period    : {_s} to {_e}")
        print(f"  Symbols   : {results.get('n_symbols', 0)}")
        print(f"  Records   : {results.get('n_records', 0)}")
        print(f"  Data source         : {src_tag}")
        print(f"  Statistical confidence: {conf.get('overall', 'INSUFFICIENT')}")
        for reason in conf.get('reasons', []):
            print(f"    - {reason}")

        bucket_df = results.get('score_bucket_df')
        if bucket_df is not None and not bucket_df.empty:
            print("\n  Score Bucket Performance (20d return%)")
            print(f"  {'Range':<10} {'N':>5} {'Avg%':>8} {'Win%':>8} {'Confidence':<15} {'Note'}")
            print("  " + "-" * 65)
            for _, row in bucket_df.iterrows():
                note  = row.get('sample_note', '')
                bconf = row.get('bucket_confidence', 'INSUFFICIENT')
                avg   = row.get('avg_return_20d')
                wr    = row.get('win_rate_20d')
                avg_s = f"{avg:+.2f}%" if avg is not None and str(avg) != 'nan' else '\u2014'
                wr_s  = f"{wr:.1f}%"   if wr  is not None and str(wr)  != 'nan' else '\u2014'
                print(f"  {str(row.get('score_bucket','')):<10} {row.get('sample_count',0):>5} {avg_s:>8} {wr_s:>8}  {bconf:<15} {note}")

        _csv_out = paths.get('score_bucket_df', paths.get('raw', _DASH))
        print(f"\n  Output CSV : {_csv_out}")
        print(f"  Report     : {rpt_path}")
        print("\n[!] For research and simulation only. Not investment advice.")

    except Exception as exc:
        logger.error("validate-score failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_backtest_buy_points(args: argparse.Namespace) -> None:
    """Backtest historical A/B/C buy-point signals."""
    logger = logging.getLogger("main.backtest_buy_points")
    mode   = getattr(args, 'mode',   'real')
    start  = getattr(args, 'start',  None)
    end    = getattr(args, 'end',    None)
    stock  = getattr(args, 'stock',  None)
    output = getattr(args, 'output', None)
    logger.info("backtest-buy-points [mode=%s start=%s end=%s stock=%s]", mode, start, end, stock)

    try:
        from backtest.buy_point_backtester import BuyPointBacktester
        from reports.buy_point_validation_report import BuyPointValidationReport

        bt      = BuyPointBacktester(mode=mode, start=start, end=end, stock=stock)
        results = bt.run()

        status = results.get('status')
        if status == 'insufficient_data':
            print(results.get('message', '資料不足，無法完成可靠統計。'))
            return

        paths = bt.save_results(results, output_dir=output)
        rpt   = BuyPointValidationReport(results)
        rpt_path = rpt.save()

        print("\n" + "=" * 60)
        print("  TW Quant Cockpit — Buy Point Validation Results")
        print("=" * 60)
        src_tag = 'REAL CSV SAMPLE' if results.get('is_sample') else 'REAL CSV'
        conf    = results.get('confidence', {})
        print(f"  Signals   : {results.get('n_signals', 0)}")
        print(f"  Data source         : {src_tag}")
        print(f"  Statistical confidence: {conf.get('overall', 'INSUFFICIENT')}")
        for reason in conf.get('reasons', []):
            print(f"    - {reason}")

        grade_df = results.get('grade_df')
        if grade_df is not None and not grade_df.empty:
            print(f"\n  {'Grade':<5} {'N':>5} {'Win 20d%':>10} {'Avg 20d%':>10} {'PF':>6} {'Confidence':<15} {'Note'}")
            print("  " + "-" * 68)
            for _, row in grade_df.iterrows():
                note  = row.get('sample_note', '')
                gconf = row.get('grade_confidence', 'INSUFFICIENT')
                wr    = row.get('win_rate_20d')
                ret   = row.get('avg_return_20d')
                pf    = row.get('profit_factor')
                wr_s  = f"{wr:.1f}%"   if wr  is not None and str(wr)  != 'nan' else '\u2014'
                ret_s = f"{ret:+.2f}%" if ret is not None and str(ret) != 'nan' else '\u2014'
                pf_s  = f"{pf:.2f}"    if pf  is not None and str(pf)  != 'nan' else '\u2014'
                print(f"  {row.get('buy_point_grade',''):<5} {row.get('signal_count',0):>5} {wr_s:>10} {ret_s:>10} {pf_s:>6}  {gconf:<15} {note}")

        _csv_out = paths.get('grade', _DASH)
        print(f"\n  Output CSV : {_csv_out}")
        print(f"  Report     : {rpt_path}")
        print("\n[!] For research and simulation only. Not investment advice.")

    except Exception as exc:
        logger.error("backtest-buy-points failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_backtest_screener(args: argparse.Namespace) -> None:
    """Replay historical screener scores and measure forward return by score bucket."""
    logger = logging.getLogger("main.backtest_screener")
    mode   = getattr(args, 'mode',   'real')
    start  = getattr(args, 'start',  None)
    end    = getattr(args, 'end',    None)
    top_n  = getattr(args, 'top',    8)
    output = getattr(args, 'output', None)
    logger.info("backtest-screener [mode=%s start=%s end=%s top_n=%d]", mode, start, end, top_n)

    try:
        from backtest.screener_backtester import ScreenerBacktester
        from reports.score_validation_report import ScoreValidationReport

        bt      = ScreenerBacktester(mode=mode, start=start, end=end, top_n=top_n)
        results = bt.run()

        status = results.get('status')
        if status == 'insufficient_data':
            print(results.get('message', '資料不足，無法完成可靠統計。'))
            return

        paths = bt.export_results(results.get('raw_df'), output_dir=output)
        rpt   = ScoreValidationReport(results)
        rpt_path = rpt.save()

        print("\n" + "=" * 60)
        print("  TW Quant Cockpit — Screener Backtest Results")
        print("=" * 60)
        src_tag   = 'REAL CSV SAMPLE' if results.get('is_sample') else 'REAL CSV'
        conf      = results.get('confidence', {})
        uni_conf  = results.get('universe_confidence', {})
        tdays     = results.get('trading_days')
        _s2 = results.get('start', _DASH)
        _e2 = results.get('end',   _DASH)
        print(f"  Period    : {_s2} to {_e2}")
        print(f"  Symbols   : {results.get('n_symbols', 0)}")
        print(f"  Records   : {results.get('n_records', 0)}")
        if tdays:
            print(f"  Trade days: {tdays}")
        print(f"  Data source         : {src_tag}")
        print(f"  Statistical confidence: {conf.get('overall', 'INSUFFICIENT')}")
        print(f"  Universe stage      : {uni_conf.get('stage', 'FUNCTIONAL_TEST')}")
        for reason in conf.get('reasons', []):
            print(f"    - {reason}")
        if uni_conf.get('note'):
            print(f"    - {uni_conf['note']}")

        bucket_df = results.get('bucket_df')
        if bucket_df is not None and not bucket_df.empty:
            print(f"\n  {'Range':<10} {'N':>5} {'Avg 20d%':>10} {'Win 20d%':>10} {'Confidence'}")
            print("  " + "-" * 50)
            for _, row in bucket_df.iterrows():
                bconf = row.get('bucket_confidence', 'INSUFFICIENT')
                avg   = row.get('avg_return_20d')
                wr    = row.get('win_rate_20d')
                avg_s = f"{avg:+.2f}%" if avg is not None and str(avg) != 'nan' else '\u2014'
                wr_s  = f"{wr:.1f}%"   if wr  is not None and str(wr)  != 'nan' else '\u2014'
                print(f"  {str(row.get('score_bucket','')):<10} {row.get('sample_count',0):>5} {avg_s:>10} {wr_s:>10}  {bconf}")

        _csv_out2 = paths.get('raw', _DASH)
        print(f"\n  Output CSV : {_csv_out2}")
        print(f"  Report     : {rpt_path}")
        print("\n[!] For research and simulation only. Not investment advice.")

    except Exception as exc:
        logger.error("backtest-screener failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_backtest_strategy_knowledge(args: argparse.Namespace) -> None:
    """Validate Strategy Knowledge Engine Phase 2 modules against historical forward returns."""
    logger = logging.getLogger("main.backtest_strategy_knowledge")
    mode         = getattr(args, 'mode',         'real')
    start        = getattr(args, 'start',        None)
    end          = getattr(args, 'end',          None)
    stock        = getattr(args, 'stock',        None)
    holding_days = getattr(args, 'holding_days', 20)
    min_samples  = getattr(args, 'min_samples',  30)
    output_dir   = getattr(args, 'output_dir',   None)
    report_dir   = getattr(args, 'report_dir',   None)
    logger.info(
        "backtest-strategy-knowledge [mode=%s stock=%s start=%s end=%s hd=%d]",
        mode, stock, start, end, holding_days,
    )

    try:
        from backtest.strategy_knowledge_backtester import StrategyKnowledgeBacktester
        from reports.strategy_knowledge_validation_report import StrategyKnowledgeValidationReport

        bt      = StrategyKnowledgeBacktester(
            mode=mode, start=start, end=end, stock=stock,
            holding_days=holding_days, min_samples=min_samples,
            output_dir=output_dir,
        )
        results = bt.run()

        status = results.get('status')
        if status == 'insufficient_data':
            print(results.get('message', '[WARN] 資料不足，無法完成統計。'))
            return

        paths    = bt.save_results(results, output_dir=output_dir)
        rpt      = StrategyKnowledgeValidationReport(results)
        rpt_path = rpt.save(output_dir=report_dir)

        conf     = results.get('confidence', {})
        uni_conf = results.get('universe_confidence', {})
        ms       = results.get('module_summary', {})

        print('\n' + '=' * 60)
        print('  TW Quant Cockpit \u2014 Strategy Knowledge Backtest')
        print('=' * 60)
        src_tag = ('MOCK DEMO' if results.get('is_mock_demo')
                   else 'REAL CSV SAMPLE' if results.get('is_sample')
                   else 'REAL CSV')
        print(f"  Data source           : {src_tag}")
        print(f"  Symbols               : {results.get('n_symbols', 0)}")
        print(f"  Records               : {results.get('n_records', 0)}")
        print(f"  Signals               : {results.get('n_signals', 0)}")
        print(f"  Period                : {results.get('start', _DASH)} \u2192 {results.get('end', _DASH)}")
        print(f"  Statistical confidence: {conf.get('overall', 'INSUFFICIENT')}")
        for reason in conf.get('reasons', []):
            print(f"    - {reason}")
        if uni_conf.get('note'):
            print(f"    - {uni_conf['note']}")
        print('')
        print('  Module summary:')
        for mod, summary in ms.items():
            print(f"    {mod}: {summary}")
        print('')
        csv_out = paths.get('signals_df', _DASH)
        print(f"  Output CSV  : {csv_out}")
        print(f"  Report      : {rpt_path}")
        if results.get('is_mock_demo'):
            print('\n  [!] MOCK DEMO ONLY \u2014 synthetic data, not a strategy conclusion.')
        else:
            print('\n  [!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger.error("backtest-strategy-knowledge failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


# ---------------------------------------------------------------------------
# v0.3.8 — Universe Expansion Commands
# ---------------------------------------------------------------------------

def cmd_build_universe_manifest(args: argparse.Namespace) -> None:
    """Build or extend the universe manifest CSV for 10 / 30 / 50 stocks."""
    logger = logging.getLogger("main.build_universe_manifest")
    size       = getattr(args, 'size',    10)
    output     = getattr(args, 'output',  None)
    replace    = getattr(args, 'replace', False)
    try:
        from data.universe_manifest import UniverseManifest
        um = UniverseManifest(manifest_path=output) if output else UniverseManifest()
        df = um.build(size=size, replace=replace)
        # Also write sample manifest
        um.build_sample()
        print(f"\nUniverse manifest built: {um.manifest_path}")
        print(f"  Symbols : {len(df)}")
        print(f"  Size    : {size}")
        for _, row in df.head(5).iterrows():
            print(f"    {row['symbol']}  {row['name']}")
        if len(df) > 5:
            print(f"    ... ({len(df) - 5} more)")
        print("\n  Next: python main.py batch-import-xq --folder <XQ_folder> "
              f"--universe {size} --dry-run")
    except Exception as exc:
        logger.error("build-universe-manifest failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_batch_import_xq(args: argparse.Namespace) -> None:
    """Batch-import XQ export files for all universe symbols."""
    logger   = logging.getLogger("main.batch_import_xq")
    folder   = getattr(args, 'folder',   None)
    universe = getattr(args, 'universe', 10)
    manifest = getattr(args, 'manifest', None)
    dry_run  = getattr(args, 'dry_run',  False)
    replace  = getattr(args, 'replace',  False)

    if not folder:
        print("ERROR: --folder is required.")
        return

    print('\n' + '=' * 60)
    print('  TW Quant Cockpit \u2014 Batch XQ Import')
    print('=' * 60)
    print(f"  Folder   : {folder}")
    print(f"  Universe : {universe}")
    print(f"  Mode     : {'dry-run' if dry_run else 'import'}")
    print()

    try:
        from data.batch_xq_importer import BatchXQImporter
        bxi    = BatchXQImporter()
        result = bxi.import_all(
            folder=folder, universe=universe,
            manifest_path=manifest, dry_run=dry_run, replace=replace,
        )

        found   = result.get('found', [])
        missing = result.get('missing', [])

        print(f"  Found    : {len(found)} file(s)")
        for sym, fpath in found:
            print(f"    {sym}  {os.path.basename(fpath)}")

        if missing:
            print(f"\n  Missing  : {len(missing)} symbol(s)")
            for sym in missing:
                print(f"    {sym}  [no matching file in folder]")

        if not dry_run:
            results = result.get('results', {})
            print(f"\n  Import results:")
            for sym, outcome in results.items():
                if outcome.get('success'):
                    print(f"    {sym}  OK")
                else:
                    err = outcome.get('error', outcome.get('warnings', ['?'])[-1] if outcome.get('warnings') else '?')
                    print(f"    {sym}  FAILED: {err}")
            print("\n  Next: python main.py universe-quality --report")
        else:
            print("\n  [dry-run] No data written.")

        print('\n' + '=' * 60)
        print('[!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger.error("batch-import-xq failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_universe_quality(args: argparse.Namespace) -> None:
    """Check universe data quality and optionally generate a Markdown report."""
    logger   = logging.getLogger("main.universe_quality")
    manifest = getattr(args, 'manifest', None)
    report   = getattr(args, 'report',   False)

    try:
        from data.universe_quality_checker import UniverseQualityChecker
        uqc = UniverseQualityChecker()
        df  = uqc.check_universe(manifest_path=manifest)

        if df.empty:
            print("[WARN] No symbols found. Run: python main.py build-universe-manifest --size 10")
            return

        summary = uqc.summarize_universe_quality(df)
        csv_path = uqc.save_quality_report_csv(df)
        conf     = summary.get('confidence', {})

        print('\n' + '=' * 60)
        print('  TW Quant Cockpit \u2014 Universe Quality')
        print('=' * 60)
        print(f"  Universe size             : {summary.get('universe_size', 0)}")
        print(f"  Imported (daily > 0)      : {summary.get('imported_count', 0)}")
        print(f"  Short-term ready          : {summary.get('short_ready_count', 0)}")
        print(f"  Mid-term ready            : {summary.get('mid_ready_count', 0)}")
        print(f"  Long-term ready           : {summary.get('long_ready_count', 0)}")
        print(f"  Strategy backtest eligible: {summary.get('strategy_bt_ready_count', 0)}")
        print(f"  Statistical confidence    : {conf.get('overall', 'INSUFFICIENT')}")
        for reason in conf.get('reasons', []):
            print(f"    - {reason}")
        next_steps = summary.get('next_steps', [])
        if next_steps:
            print('\n  Next steps:')
            for step in next_steps:
                print(f"    - {step}")
        print(f"\n  Quality CSV : {csv_path}")

        if report:
            from reports.universe_quality_report import UniverseQualityReport
            rpt      = UniverseQualityReport(df, summary)
            rpt_path = rpt.save()
            print(f"  Report      : {rpt_path}")

        print('\n[!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger.error("universe-quality failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_run_validation_suite(args: argparse.Namespace) -> None:
    """Run all four validation backtests in sequence."""
    logger      = logging.getLogger("main.run_validation_suite")
    mode        = getattr(args, 'mode',        'real')
    min_symbols = getattr(args, 'min_symbols', 10)
    output      = getattr(args, 'output',      None)

    print('\n' + '=' * 60)
    print('  TW Quant Cockpit \u2014 Validation Suite')
    print('=' * 60)
    print(f"  Mode        : {mode}")
    print(f"  Min symbols : {min_symbols}")

    suite_results = {}

    # 1. validate-score
    print('\n--- Step 1/4: validate-score ---')
    try:
        from backtest.score_validation import ScoreValidator
        sv = ScoreValidator(mode=mode)
        r  = sv.run()
        conf = r.get('confidence', {})
        print(f"  Status     : {r.get('status', 'ok')}")
        print(f"  Confidence : {conf.get('overall', 'INSUFFICIENT')}")
        suite_results['validate_score'] = {'ok': True, 'confidence': conf.get('overall')}
    except Exception as exc:
        logger.warning("validate-score failed: %s", exc)
        print(f"  FAILED: {exc}")
        suite_results['validate_score'] = {'ok': False, 'error': str(exc)}

    # 2. backtest-buy-points
    print('\n--- Step 2/4: backtest-buy-points ---')
    try:
        from backtest.buy_point_backtester import BuyPointBacktester
        bt = BuyPointBacktester(mode=mode)
        r  = bt.run()
        conf = r.get('confidence', {})
        print(f"  Status     : {r.get('status', 'ok')}")
        print(f"  Signals    : {r.get('n_signals', 0)}")
        print(f"  Confidence : {conf.get('overall', 'INSUFFICIENT')}")
        suite_results['buy_points'] = {'ok': True, 'confidence': conf.get('overall')}
    except Exception as exc:
        logger.warning("backtest-buy-points failed: %s", exc)
        print(f"  FAILED: {exc}")
        suite_results['buy_points'] = {'ok': False, 'error': str(exc)}

    # 3. backtest-screener
    print('\n--- Step 3/4: backtest-screener ---')
    try:
        from backtest.screener_backtester import ScreenerBacktester
        bt = ScreenerBacktester(mode=mode)
        r  = bt.run()
        conf = r.get('confidence', {})
        print(f"  Status     : {r.get('status', 'ok')}")
        print(f"  Symbols    : {r.get('n_symbols', 0)}")
        print(f"  Confidence : {conf.get('overall', 'INSUFFICIENT')}")
        suite_results['screener'] = {'ok': True, 'confidence': conf.get('overall')}
    except Exception as exc:
        logger.warning("backtest-screener failed: %s", exc)
        print(f"  FAILED: {exc}")
        suite_results['screener'] = {'ok': False, 'error': str(exc)}

    # 4. backtest-strategy-knowledge
    print('\n--- Step 4/4: backtest-strategy-knowledge ---')
    try:
        from backtest.strategy_knowledge_backtester import StrategyKnowledgeBacktester
        bt = StrategyKnowledgeBacktester(mode=mode)
        r  = bt.run()
        conf = r.get('confidence', {})
        print(f"  Status     : {r.get('status', 'ok')}")
        print(f"  Symbols    : {r.get('n_symbols', 0)}")
        print(f"  Confidence : {conf.get('overall', 'INSUFFICIENT')}")
        suite_results['strategy_knowledge'] = {'ok': True, 'confidence': conf.get('overall')}
    except Exception as exc:
        logger.warning("backtest-strategy-knowledge failed: %s", exc)
        print(f"  FAILED: {exc}")
        suite_results['strategy_knowledge'] = {'ok': False, 'error': str(exc)}

    # Summary
    print('\n' + '=' * 60)
    print('  Validation Suite Summary')
    print('=' * 60)
    all_ok = all(v.get('ok') for v in suite_results.values())
    for step, res in suite_results.items():
        status = 'OK' if res.get('ok') else 'FAILED'
        conf   = res.get('confidence', 'INSUFFICIENT')
        print(f"  {step:<30} {status}  {conf}")
    print(f"\n  All steps passed : {'YES' if all_ok else 'NO (see above)'}")
    print('\n[!] For research and simulation only. Not investment advice.')


# ---------------------------------------------------------------------------
# v0.3.2 — Build Universe Command
# ---------------------------------------------------------------------------

def cmd_build_universe(args: argparse.Namespace) -> None:
    """Build or update the stock universe / profile CSV."""
    from data.universe_builder import UniverseBuilder

    logger = logging.getLogger("main.build_universe")
    builder = UniverseBuilder()

    template = getattr(args, 'template', None)
    file_path = getattr(args, 'file', None)
    replace   = getattr(args, 'replace', False)

    print('')
    print('=' * 60)
    print('  TW Quant Cockpit Build Universe')
    print('=' * 60)

    try:
        if template:
            result = builder.build_from_template(template)
            source_label = f'template: {template}'
        elif file_path:
            df = builder.load_universe_file(file_path)
            result = builder.merge_universe(df, replace=replace)
            result['source'] = file_path
            result['output'] = builder._output
            source_label = f'file: {file_path}'
        else:
            print('  ERROR: specify --template or --file')
            sys.exit(1)

        if not result.get('success'):
            print(f"  ERROR: {result.get('error', 'unknown error')}")
            sys.exit(1)

        # Reload profile to get final count
        final_df = builder.load_profile()
        final_count = len(final_df)

        print(f"  來源     : {source_label}")
        print(f"  輸出     : {result.get('output', builder._output)}")
        print(f"  匯入筆數 : {result.get('rows_added', 0)}")
        print(f"  總 universe 筆數 : {final_count}")

        # Validation details
        if template:
            from data.universe_builder import UniverseBuilder as _UB
            val = _UB().validate_universe(final_df)
        else:
            val = builder.validate_universe(final_df)

        dupes = val.get('duplicate_symbols', [])
        missing_names = val.get('missing_names', [])
        warnings = result.get('warnings', []) + val.get('warnings', [])

        print(f"  重複 symbol  : {dupes if dupes else '無'}")
        print(f"  缺少名稱     : {len(missing_names)} 檔  {missing_names[:5] if missing_names else ''}")
        if warnings:
            print('')
            print('  警告：')
            for w in warnings[:10]:
                print(f'  - {w}')

        print('=' * 60)
        print('[!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger.error("build-universe failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# v0.3.2 — Batch Import Command
# ---------------------------------------------------------------------------

def cmd_batch_import(args: argparse.Namespace) -> None:
    """Batch import CSV files from a folder or bundle directory."""
    from data.batch_importer import BatchImporter

    logger         = logging.getLogger("main.batch_import")
    bi             = BatchImporter()
    replace        = getattr(args, 'replace', False)
    dry_run        = getattr(args, 'dry_run', False)
    export_report  = getattr(args, 'export_report', False)

    data_type  = getattr(args, 'type', None)
    folder_arg = getattr(args, 'folder', None)
    bundle_arg = getattr(args, 'bundle', None)

    print('')
    print('=' * 60)
    print('  TW Quant Cockpit Batch Import')
    print('=' * 60)
    if dry_run:
        print('  Mode     : dry-run (no data written)')

    try:
        if bundle_arg:
            result = bi.import_bundle(
                bundle_arg, replace=replace,
                dry_run=dry_run, export_report=export_report,
            )
            print(f"  Bundle   : {bundle_arg}")
            print(f"  Success  : {result.get('success')}")
            print('')
            for dtype, sub in result.get('results', {}).items():
                ok    = len(sub.get('success_files', []))
                fail  = len(sub.get('failed_files', []))
                rows  = sub.get('total_rows_imported', 0)
                total = sub.get('total_files', 0)
                print(f"  [{dtype:<20}] files={total}  ok={ok}  fail={fail}  rows={rows}")
                for f in sub.get('failed_files', []):
                    print(f"    FAIL {f['file']}: {f['error']}")
            warnings = result.get('warnings', [])

        elif data_type and folder_arg:
            result = bi.import_folder(
                data_type, folder_arg, replace=replace, dry_run=dry_run
            )
            ok    = len(result.get('success_files', []))
            fail  = len(result.get('failed_files', []))
            rows  = result.get('total_rows_imported', 0)
            total = result.get('total_files', 0)
            print(f"  Type     : {data_type}")
            print(f"  Folder   : {folder_arg}")
            print(f"  Files    : {total}")
            print(f"  Success  : {ok}")
            print(f"  Failed   : {fail}")
            print(f"  Total rows imported : {rows}")
            for f in result.get('failed_files', []):
                print(f"  FAIL {f['file']}: {f['error']}")
            warnings = result.get('warnings', [])

            if export_report:
                try:
                    from data.import_reporter import ImportReporter
                    from datetime import datetime
                    import os as _os
                    _base = _os.path.dirname(_os.path.abspath(__file__))
                    _dir  = _os.path.join(_base, 'data', 'import_reports')
                    _os.makedirs(_dir, exist_ok=True)
                    _ts   = datetime.now().strftime('%Y%m%d_%H%M%S')
                    _out  = _os.path.join(_dir, f'batch_import_report_{_ts}.md')
                    ImportReporter().write_batch_import_report(result, _out)
                    print(f"  Report   : {_out}")
                except Exception as rep_exc:
                    logger.warning("export_report failed: %s", rep_exc)

        else:
            print('  ERROR: specify --type + --folder or --bundle')
            sys.exit(1)

        if warnings:
            unique_warnings = list(dict.fromkeys(warnings))[:10]
            print('')
            print('  Warnings:')
            for w in unique_warnings:
                print(f'  - {w}')

        print('=' * 60)
        print('[!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger.error("batch-import failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# v0.3.1 — Universe Check Command
# ---------------------------------------------------------------------------

def cmd_universe_check(args: argparse.Namespace) -> None:  # noqa: ARG001
    """Show universe expansion status and import recommendations."""
    try:
        from data.universe_expansion_guide import UniverseExpansionGuide
        guide = UniverseExpansionGuide()
        guide.print_summary()
        print("[!] For research and simulation only. Not investment advice.")
    except Exception as exc:
        logging.getLogger("main.universe_check").error("universe-check failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


# ---------------------------------------------------------------------------
# v0.3.3-hotfix — Import XQ Export Command
# ---------------------------------------------------------------------------

def cmd_import_xq_export(args: argparse.Namespace) -> None:
    """One-command import of XQ technical-analysis export files."""
    from data.xq_export_importer import XQExportImporter

    logger_cmd  = logging.getLogger("main.import_xq_export")
    file_path   = getattr(args, 'file', None)
    symbol      = getattr(args, 'symbol', None)
    name        = getattr(args, 'name', '') or ''
    sheet       = getattr(args, 'sheet', 0)
    dry_run     = getattr(args, 'dry_run', False)
    replace     = getattr(args, 'replace', False)
    export_split= getattr(args, 'export_split', False)
    output_dir  = getattr(args, 'output_dir', 'data/xq_exports') or 'data/xq_exports'

    print('')
    print('=' * 60)
    print('  TW Quant Cockpit XQ Export Import')
    print('=' * 60)
    print(f'  Input   : {file_path}')
    print(f'  Symbol  : {symbol}')
    print(f'  Name    : {name if name else "(not provided)"}')
    print(f'  Mode    : {"dry-run" if dry_run else "import"}')

    try:
        importer = XQExportImporter()

        # Split first so we can show detected columns
        split_result = importer.split(file_path, symbol=symbol, name=name, sheet=sheet)

        if split_result.get('errors'):
            for e in split_result['errors']:
                print(f'  ERROR   : {e}')
            sys.exit(1)

        print('')
        print(f'  Detected columns ({len(split_result["columns_detected"])}):')
        for col in split_result['columns_detected']:
            print(f'    - {col}')

        print('')
        print('  Split result:')
        all_warnings = []
        for dt in ['daily', 'margin', 'institutional', 'trust_cost', 'holder']:
            df, warnings = split_result.get(dt, (None, []))
            if df is not None and not df.empty:
                partial = ' (partial)' if warnings else ''
                print(f'  {dt:<16}: {len(df)} rows{partial}')
            else:
                print(f'  {dt:<16}: no data detected')
            all_warnings.extend(warnings)

        if all_warnings:
            print('')
            print('  Warnings:')
            for w in all_warnings:
                print(f'    - {w}')

        if dry_run:
            print('')
            print('  No data written.')
        else:
            # Perform import
            outcome = importer.import_file(
                file_path, symbol=symbol, name=name,
                replace=replace, dry_run=False, sheet=sheet,
            )

            print('')
            print('  Imported:')
            for dt, res in outcome.get('results', {}).items():
                if res.get('skipped'):
                    print(f'  {dt:<16}: skipped (no data)')
                elif res.get('success'):
                    out = res.get('output', '')
                    print(f'  {dt:<16}: {res["rows"]} rows -> {out}')
                else:
                    ws = res.get('warnings', [])
                    print(f'  {dt:<16}: FAILED  {ws[-1] if ws else ""}')

            if export_split:
                abs_out = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    output_dir.replace('/', os.sep),
                )
                exported = importer.export_split_csvs(split_result, abs_out)
                print('')
                print(f'  Split CSVs exported to: {abs_out}')
                for dt, fp in exported.items():
                    print(f'    {dt}: {fp}')

            print('')
            print('  Next steps:')
            print(f'    python main.py data-check --stock {symbol}')
            print(f'    python main.py stock-report --stock {symbol} --mode real')

        print('')
        print('=' * 60)
        print('[!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger_cmd.error("import-xq-export failed: %s", exc, exc_info=True)
        print(f'  ERROR: {exc}')
        sys.exit(1)


# ---------------------------------------------------------------------------
# v0.3.3 — Clean CSV Command
# ---------------------------------------------------------------------------

def cmd_clean_csv(args: argparse.Namespace) -> None:
    """Clean and normalize a CSV file without importing to standard path."""
    from data.csv_cleaner import CSVCleaner
    from data.csv_importer import CSVImporter

    logger_cmd = logging.getLogger("main.clean_csv")
    data_type = getattr(args, 'type', None)
    file_path = getattr(args, 'file', None)
    output    = getattr(args, 'output', None)
    dry_run   = getattr(args, 'dry_run', False)

    print('')
    print('=' * 60)
    print('  TW Quant Cockpit CSV Clean')
    print('=' * 60)
    print(f'  Type    : {data_type}')
    print(f'  Input   : {file_path}')
    if output:
        print(f'  Output  : {output}')
    if dry_run:
        print('  Mode    : dry-run (no output written)')

    try:
        importer = CSVImporter()
        cleaner  = CSVCleaner()

        # Read file
        warnings = []
        df = importer._read_with_encoding(file_path, warnings)
        if df is None:
            print(f'  ERROR   : Cannot read file: {file_path}')
            if warnings:
                for w in warnings:
                    print(f'  - {w}')
            sys.exit(1)

        print(f'  Input rows : {len(df)}')

        # Normalize columns
        df = importer.normalize_columns(data_type, df)

        # Validate columns
        validation = importer.validate_columns(data_type, df)
        if not validation['ok']:
            print(f'  ERROR   : Missing required columns: {validation["missing"]}')
            sys.exit(1)
        if validation.get('extra'):
            print(f'  Ignored columns : {validation["extra"]}')

        # Clean
        cleaned_df, summary = cleaner.clean_dataframe(data_type, df)

        print(f'  Output rows        : {summary["output_rows"]}')
        print(f'  Duplicates removed : {summary["duplicates_removed"]}')

        w_list = summary.get('warnings', [])
        e_list = summary.get('errors', [])
        print(f'  Warnings           : {len(w_list)}')
        print(f'  Errors             : {len(e_list)}')

        if w_list:
            print('')
            print('  Warnings:')
            for w in w_list[:10]:
                print(f'    - {w}')

        if e_list:
            print('')
            print('  Errors:')
            for e in e_list[:10]:
                print(f'    - {e}')

        if not dry_run and output:
            cleaned_df.to_csv(output, index=False, encoding='utf-8-sig')
            print(f'')
            print(f'  Saved to: {output}')

        print('=' * 60)
        print('[!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger_cmd.error("clean-csv failed: %s", exc, exc_info=True)
        print(f'  ERROR: {exc}')
        sys.exit(1)


# ---------------------------------------------------------------------------
# v0.3.3 — Data Audit Command
# ---------------------------------------------------------------------------

def cmd_data_audit(args: argparse.Namespace) -> None:
    """Audit all imported data for quality and coverage."""
    from data.data_auditor import DataAuditor

    logger_cmd = logging.getLogger("main.data_audit")
    stock      = getattr(args, 'stock', None)
    export     = getattr(args, 'export', False)

    print('')
    print('=' * 60)
    print('  TW Quant Cockpit Data Audit')
    print('=' * 60)

    try:
        auditor = DataAuditor()

        if stock:
            result = auditor.audit_symbol(stock)
            print(f'  Symbol: {stock}')
            print('')
            for dt, info in result.items():
                if dt == 'symbol':
                    continue
                rows = info.get('rows', 0) if isinstance(info, dict) else 0
                print(f'  {dt:<22}: {rows} rows')
        else:
            result   = auditor.audit_all()
            readiness = result.get('readiness', {})

            print(f'  Universe:')
            print(f'    symbols          : {readiness.get("profile_count", 0)}')
            print(f'    validation stage : {readiness.get("validation_stage", "N/A")}')
            print(f'    confidence       : {readiness.get("statistical_confidence", "N/A")}')
            print('')
            print(f'  Coverage:')
            print(f'    daily >= 120     : {readiness.get("daily_120", 0)} symbols')
            print(f'    institutional >= 40 : {readiness.get("institutional_40", 0)} symbols')
            print(f'    margin >= 40     : {readiness.get("margin_40", 0)} symbols')
            print(f'    revenue >= 12    : {readiness.get("revenue_12", 0)} symbols')
            print(f'    holder >= 4      : {readiness.get("holder_4", 0)} symbols')
            print(f'    trust_cost >= 20 : {readiness.get("trust_cost_20", 0)} symbols')
            print('')
            daily_info = result.get('daily', {})
            dup_daily  = daily_info.get('duplicate_rows', 0)
            inv_close  = daily_info.get('invalid_close', 0)
            high_lt_low = daily_info.get('high_lt_low', 0)
            neg_vol    = daily_info.get('negative_volume', 0)
            missing_types = [
                dt for dt in ['daily', 'institutional', 'margin',
                               'monthly_revenue', 'holder', 'trust_cost']
                if not result.get(dt, {}).get('found', False)
            ]
            print(f'  Problems:')
            print(f'    missing data types : {", ".join(missing_types) if missing_types else "none"}')
            print(f'    invalid OHLC       : {inv_close + high_lt_low}')
            print(f'    duplicate rows     : {dup_daily}')
            print(f'    negative volume    : {neg_vol}')
            print('')
            print(f'  Readiness:')
            print(f'    short-ready      : {readiness.get("short_ready_count", 0)} symbols')
            print(f'    mid-ready        : {readiness.get("mid_ready_count", 0)} symbols')
            print(f'    long-ready       : {readiness.get("long_ready_count", 0)} symbols')

        if export and not stock:
            paths = auditor.export_audit_report()
            print('')
            print(f'  Exported:')
            print(f'    Markdown : {paths["markdown"]}')
            print(f'    CSV      : {paths["csv"]}')

        print('=' * 60)
        print('[!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger_cmd.error("data-audit failed: %s", exc, exc_info=True)
        print(f'  ERROR: {exc}')
        sys.exit(1)


# ---------------------------------------------------------------------------
# v0.3.3 — Import Plan Command
# ---------------------------------------------------------------------------

def cmd_import_plan(args: argparse.Namespace) -> None:
    """Show prioritized import plan based on current data gaps."""
    from data.import_plan import ImportPlan

    logger_cmd = logging.getLogger("main.import_plan")
    export     = getattr(args, 'export', False)

    try:
        plan_builder = ImportPlan()
        if export:
            paths = plan_builder.export_plan()
            plan_builder._print(paths['plan'])
            print(f'')
            print(f'  Exported: {paths["file"]}')
        else:
            plan_builder.print_plan()

    except Exception as exc:
        logger_cmd.error("import-plan failed: %s", exc, exc_info=True)
        print(f'  ERROR: {exc}')
        sys.exit(1)


# ---------------------------------------------------------------------------
# v0.3.4 — Provider Status Command
# ---------------------------------------------------------------------------

def cmd_provider_status(args: argparse.Namespace) -> None:
    """Show the status of all configured data providers."""
    logger_cmd = logging.getLogger("main.provider_status")

    print()
    print("=" * 60)
    print("  TW Quant Cockpit — Data Provider Status")
    print("=" * 60)

    providers_info = [
        ("csv",        "CSV provider (data/import/)"),
        ("xq_export",  "XQ export provider (transition)"),
        ("twse",       "TWSE OpenAPI provider (planned)"),
        ("mega",       "Mega (兆豐) provider (planned, disabled)"),
    ]

    for key, label in providers_info:
        try:
            from data.providers import get_provider
            p = get_provider(key)
            status = p.health_check()
            if status.get("available"):
                marker = "[OK]      "
            elif status.get("planned"):
                marker = "[PLANNED] "
            else:
                marker = "[OFF]     "
            note = status.get("note", "")
            print(f"  {marker} {label}")
            if note:
                note_short = note[:70] + "..." if len(note) > 70 else note
                print(f"           {note_short}")
        except Exception as exc:
            logger_cmd.debug("Provider check error for %s: %s", key, exc)
            print(f"  [ERROR]   {label} — {exc}")

    print()
    print("  Real order execution : DISABLED")
    print("  Broker API (Mega)    : planned / not configured")
    print("  Broker API (Shioaji) : not used")
    print()
    print("  Run 'python main.py import-xq-export' to import XQ data.")
    print("  Run 'python main.py data-check' to verify CSV completeness.")
    print()


# ---------------------------------------------------------------------------
# v0.3.4 — Time Machine Preview Command
# ---------------------------------------------------------------------------

def cmd_time_machine_preview(args: argparse.Namespace) -> None:
    """Show Volume Profile and Microstructure summary for a stock."""
    import pandas as pd

    logger_cmd = logging.getLogger("main.time_machine_preview")
    symbol = getattr(args, 'stock', None)
    mode   = getattr(args, 'mode', 'mock')

    if not symbol:
        print("  ERROR: --stock is required. Example: python main.py time-machine-preview --stock 2454")
        sys.exit(1)

    print()
    print("=" * 60)
    print(f"  Time Machine Preview — {symbol}  (mode={mode})")
    print("=" * 60)

    # Load daily data via provider
    try:
        from data.providers import get_provider
        provider = get_provider("csv")
        daily_df = provider.get_daily(symbol)
    except Exception as exc:
        logger_cmd.warning("Provider load failed: %s", exc)
        daily_df = None

    # Fallback: mock minimal data for demo
    if daily_df is None or (hasattr(daily_df, 'empty') and daily_df.empty):
        if mode == 'real':
            print(f"  [WARN] real data insufficient for {symbol}. Import data first.")
            print(f"  Run: python main.py data-check --stock {symbol}")
            print(f"  Or use mock mode: python main.py time-machine-preview --stock {symbol} --mode mock")
            print()
            return
        logger_cmd.info("Using mock data for time-machine-preview (mock mode).")
        import numpy as np
        rng = pd.date_range("2024-01-02", periods=120, freq="B")
        base = 200.0
        closes = base + np.cumsum(np.random.randn(120) * 2)
        closes = np.maximum(closes, 10.0)
        daily_df = pd.DataFrame({
            "date":   rng,
            "stock_id": symbol,
            "open":   closes * 0.99,
            "high":   closes * 1.01,
            "low":    closes * 0.98,
            "close":  closes,
            "volume": (np.abs(np.random.randn(120)) * 5000 + 10000).astype(int),
        })

    if "stock_id" not in daily_df.columns:
        daily_df["stock_id"] = symbol

    # Compute Volume Profile
    print()
    print("  [Volume Profile]")
    try:
        from features.volume_profile import compute_volume_profile_single
        vp_df = compute_volume_profile_single(daily_df)
        last = vp_df.iloc[-1]
        close_val = last.get("close", float("nan"))
        poc = last.get("vp_peak_price", float("nan"))
        dist = last.get("vp_distance_to_peak", float("nan"))
        strength = last.get("vp_cluster_strength", float("nan"))
        sps = last.get("support_pressure_score", float("nan"))
        va_hi = last.get("vp_value_area_high", float("nan"))
        va_lo = last.get("vp_value_area_low", float("nan"))
        in_va = last.get("vp_price_in_value_area", float("nan"))

        print(f"    Close              : {close_val:.2f}")
        print(f"    POC (peak price)   : {poc:.2f}")
        print(f"    Distance to POC    : {dist:+.2%}")
        print(f"    Cluster strength   : {strength:.2%}")
        print(f"    Value Area         : {va_lo:.2f} — {va_hi:.2f}")
        print(f"    Price in VA        : {'Yes' if in_va == 1 else 'No'}")
        print(f"    Support/Pressure   : {sps:+.3f}  (+ = support, - = pressure)")
    except Exception as exc:
        logger_cmd.warning("Volume profile computation failed: %s", exc)
        print(f"    WARNING: Volume Profile unavailable — {exc}")

    # Compute Microstructure
    try:
        from features.microstructure import compute_microstructure_single
        from data.intraday_data_importer import IntradayDataImporter
        _importer = IntradayDataImporter()
        _idf = _importer.load_intraday(symbol, freq="1min")
        ms_df = compute_microstructure_single(daily_df, intraday_df=_idf)
        last = ms_df.iloc[-1]
        _ms_src = last.get("microstructure_source", "UNAVAILABLE")
        ms_score = last.get("microstructure_score", float("nan"))
        fake_risk = last.get("ms_fake_breakout_risk", float("nan"))
        no_chase = last.get("ms_no_chase_flag", float("nan"))
        bsp = last.get("buy_sell_pressure", float("nan"))
        ovr = last.get("opening_volume_ratio", float("nan"))

        print()
        print(f"  [Opening Microstructure]  ({_ms_src})")

        def _fmt(v):
            return f"{v:.3f}" if v == v else "NaN"

        print(f"    Microstructure score : {_fmt(ms_score)}")
        print(f"    Buy/sell pressure    : {_fmt(bsp)}")
        print(f"    Opening volume ratio : {_fmt(ovr)}")
        print(f"    Fake breakout risk   : {'YES' if fake_risk == 1 else ('No' if fake_risk == 0 else 'unknown')}")
        print(f"    No-chase flag        : {'YES' if no_chase == 1 else ('No' if no_chase == 0 else 'unknown')}")
        if _ms_src == "DAILY_PROXY":
            print()
            print("    NOTE: intraday / tick data not available.")
            print("    Scores are daily OHLCV proxies.  Import intraday data for exact values.")
    except Exception as exc:
        logger_cmd.warning("Microstructure computation failed: %s", exc)
        print(f"    WARNING: Microstructure unavailable — {exc}")

    print()


# ---------------------------------------------------------------------------
# v0.3.4 — Feature Preview Command
# ---------------------------------------------------------------------------

def cmd_feature_preview(args: argparse.Namespace) -> None:
    """Display the latest computed features for a stock."""
    import pandas as pd

    logger_cmd = logging.getLogger("main.feature_preview")
    symbol = getattr(args, 'stock', None)
    mode   = getattr(args, 'mode', 'mock')

    if not symbol:
        print("  ERROR: --stock is required. Example: python main.py feature-preview --stock 2454")
        sys.exit(1)

    print()
    print("=" * 60)
    print(f"  Feature Preview — {symbol}  (mode={mode})")
    print("=" * 60)

    # Load daily data
    try:
        from data.providers import get_provider
        provider = get_provider("csv")
        daily_df = provider.get_daily(symbol)
    except Exception as exc:
        logger_cmd.warning("Provider load failed: %s", exc)
        daily_df = None

    if daily_df is None or (hasattr(daily_df, 'empty') and daily_df.empty):
        if mode == 'real':
            print(f"  [WARN] real data insufficient for {symbol}. Import data first.")
            print(f"  Run: python main.py data-check --stock {symbol}")
            print(f"  Or use mock mode: python main.py feature-preview --stock {symbol} --mode mock")
            print()
            return
        import numpy as np
        rng = pd.date_range("2024-01-02", periods=120, freq="B")
        base = 200.0
        closes = base + np.cumsum(np.random.randn(120) * 2)
        closes = np.maximum(closes, 10.0)
        daily_df = pd.DataFrame({
            "date":   rng,
            "stock_id": symbol,
            "open":   closes * 0.99,
            "high":   closes * 1.01,
            "low":    closes * 0.98,
            "close":  closes,
            "volume": (np.abs(np.random.randn(120)) * 5000 + 10000).astype(int),
        })

    if "stock_id" not in daily_df.columns:
        daily_df["stock_id"] = symbol

    # Compute full feature set
    try:
        from features.indicators import compute_indicators
        feat_df = compute_indicators(daily_df, intraday_df=None)
        last = feat_df.iloc[-1]

        def _show(label: str, cols: list) -> None:
            print()
            print(f"  [{label}]")
            for col in cols:
                val = last.get(col)
                if val is None:
                    print(f"    {col:<35} : n/a")
                elif isinstance(val, float) and val != val:
                    print(f"    {col:<35} : NaN")
                elif isinstance(val, float):
                    print(f"    {col:<35} : {val:.4f}")
                else:
                    print(f"    {col:<35} : {val}")

        _show("Core Indicators", [
            "rsi_14", "macd", "macd_signal", "macd_hist",
            "sma_20", "sma_60", "ema_12", "ema_26",
            "volume_spike", "bb_width", "bb_position",
            "price_above_sma20", "price_above_sma60",
        ])

        _show("Volume Profile (分價量)", [
            "vp_peak_price", "vp_distance_to_peak", "vp_cluster_strength",
            "vp_support_score", "vp_pressure_score", "support_pressure_score",
            "vp_value_area_high", "vp_value_area_low", "vp_price_in_value_area",
        ])

        _ms_source = last.get("microstructure_source", "UNAVAILABLE")
        _show(f"Opening Microstructure (盤口微觀) — {_ms_source}", [
            "opening_return_15m", "opening_volume_ratio",
            "opening_high_break", "opening_low_break",
            "large_trade_ratio", "buy_sell_pressure",
            "microstructure_score", "ms_fake_breakout_risk", "ms_no_chase_flag",
        ])
        print(f"    {'microstructure_source':<35} : {_ms_source}")

        print()
        print(f"  Total features computed: {len(feat_df.columns)}")
        print(f"  Date of last row: {last.get('date', 'unknown')}")
        print()
    except Exception as exc:
        logger_cmd.error("Feature computation failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
        sys.exit(1)



# ---------------------------------------------------------------------------
# v0.3.6 – strategy-preview command
# ---------------------------------------------------------------------------

def cmd_strategy_preview(args: argparse.Namespace) -> None:
    """
    strategy-preview: Full Strategy Knowledge Engine output for a stock.

    Example
    -------
    python main.py strategy-preview --stock 2454 --mode real
    """
    logger_cmd = logging.getLogger("cmd.strategy_preview")
    symbol = args.stock
    mode   = getattr(args, "mode", "real")

    print()
    print(f"Strategy Knowledge Preview — {symbol} (mode={mode})")
    print("=" * 60)

    # ── Load daily data ───────────────────────────────────────────────────
    import pandas as pd
    df = None
    try:
        if mode == "real":
            from data.providers.csv_provider import CSVProvider
            prov = CSVProvider()
            raw  = prov.get_daily(symbol)
            if raw is not None and len(raw) > 0:
                df = raw.copy()
                if "date" in df.columns:
                    df = df.sort_values("date").reset_index(drop=True)
        else:
            from data.data_source_router import DataSourceRouter
            router = DataSourceRouter()
            raw    = router.get_daily(symbol)
            if raw is not None and len(raw) > 0:
                df = raw.copy()
                if "date" in df.columns:
                    df = df.sort_values("date").reset_index(drop=True)
    except Exception as exc:
        logger_cmd.warning("Data load failed (%s): %s", symbol, exc)

    # Real mode must NOT fall back to mock
    if df is None or len(df) < 10:
        if mode == "real":
            print("  [WARN] real data insufficient for strategy analysis.")
            print("  Strategy Knowledge unavailable in real mode.")
            print("  Hint: use --mode mock for demo.")
            return
        # Mock mode: generate seeded random OHLCV
        import numpy as np
        rng = np.random.default_rng(int(symbol) if symbol.isdigit() else 42)
        n   = 80
        price = 100.0 + rng.normal(0, 2, n).cumsum()
        price = np.clip(price, 10, None)
        df = pd.DataFrame({
            "date":   pd.date_range("2024-01-01", periods=n, freq="B"),
            "open":   price * (1 + rng.normal(0, 0.005, n)),
            "high":   price * (1 + np.abs(rng.normal(0, 0.01, n))),
            "low":    price * (1 - np.abs(rng.normal(0, 0.01, n))),
            "close":  price,
            "volume": (rng.integers(5_000, 50_000, n)).astype(float),
        })
        print("  [MOCK] 無真實資料，使用隨機模擬價格")

    # ── Run Strategy Knowledge Engine ─────────────────────────────────────
    try:
        from analysis.strategy_knowledge_engine import build_strategy_signals
        signals = build_strategy_signals(
            df=df,
            symbol=symbol,
        )
    except Exception as exc:
        logger_cmd.error("StrategyKnowledgeEngine failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
        import sys; sys.exit(1)

    pos_plan  = signals.get("position_plan", {})
    hold_plan = signals.get("holding_period_plan", {})
    vol_sigs  = signals.get("volume_signals", {})
    macd_sigs = signals.get("macd_signals", {})
    val_sigs  = signals.get("valuation_signals", {})
    exit_sigs = signals.get("exit_signals", {})
    final     = signals.get("final_strategy_decision", {})
    no_chase  = signals.get("no_chase_reasons", [])
    no_panic  = signals.get("no_sell_low_reasons", [])
    no_rebuy  = signals.get("do_not_rebuy_yet_reasons", [])
    # Phase 2 signals
    kd_sigs   = signals.get("kd_advanced_signals", {})
    si_sigs   = signals.get("short_interest_signals", {})
    br_sigs   = signals.get("bottom_reversal_signals", {})
    sr_sigs   = signals.get("sector_rotation_signals", {})
    fq_sigs   = signals.get("fundamental_quality_signals", {})

    def _fmt(label: str, value) -> str:
        if value is None or value == "":
            return f"  {label}: —"
        return f"  {label}: {value}"

    def _bool(v) -> str:
        return "[YES]" if v else "[NO]"

    # ── 1. Position Plan ──────────────────────────────────────────────────
    print()
    print("Position Plan:")
    print(_fmt("first_entry_size",       pos_plan.get("first_entry_size")))
    print(_fmt("second_entry_size",      pos_plan.get("second_entry_size")))
    print(_fmt("take_profit_half_price", pos_plan.get("take_profit_half_price")))
    print(_fmt("remaining_trailing_stop",pos_plan.get("remaining_trailing_stop")))
    print(_fmt("breakeven_exit_price",   pos_plan.get("breakeven_exit_price")))
    print(_fmt("portfolio_weight_warning",pos_plan.get("portfolio_weight_warning")))

    # ── 2. Holding Period ─────────────────────────────────────────────────
    print()
    print("Holding Period:")
    print(_fmt("mode",           hold_plan.get("holding_mode")))
    print(_fmt("trailing_ma_rule", hold_plan.get("trailing_ma_rule")))
    print(_fmt("trend_stage",    hold_plan.get("trend_stage")))
    print(_fmt("can_hold_swing", hold_plan.get("can_hold_for_swing")))
    sw_r = hold_plan.get("swing_risk_reason", "")
    if sw_r:
        print(_fmt("swing_risk",   sw_r))

    # ── 3. Volume Behavior ────────────────────────────────────────────────
    print()
    print("Volume Behavior:")
    print(_fmt("breakout_volume_confirmed", _bool(vol_sigs.get("breakout_volume_confirmed"))))
    print(_fmt("volume_roll_up_score",      vol_sigs.get("volume_roll_up_score")))
    print(_fmt("one_day_volume_spike_risk", _bool(vol_sigs.get("one_day_volume_spike_risk"))))
    print(_fmt("volume_shrink_above_ma",    _bool(vol_sigs.get("volume_shrink_above_ma"))))
    print(_fmt("volume_failure_warning",    _bool(vol_sigs.get("volume_failure_warning"))))
    print(_fmt("demand_persistence_score",  vol_sigs.get("demand_persistence_score")))

    # ── 4. MACD ───────────────────────────────────────────────────────────
    print()
    print("MACD:")
    print(_fmt("trend_context",        macd_sigs.get("macd_trend_context")))
    print(_fmt("bull_pullback_buy",    _bool(macd_sigs.get("macd_bull_pullback_buy"))))
    print(_fmt("wait_confirm",         _bool(macd_sigs.get("macd_wait_confirm"))))
    print(_fmt("fake_reclaim_warning", _bool(macd_sigs.get("macd_fake_reclaim_warning"))))
    print(_fmt("buy_reason",           macd_sigs.get("macd_buy_reason")))
    print(_fmt("rebound_end_warning",  _bool(macd_sigs.get("macd_rebound_end_warning"))))
    print(_fmt("rebound_status",       macd_sigs.get("macd_rebound_status")))
    sar = macd_sigs.get("macd_sell_or_avoid_reason", "")
    if sar:
        print(_fmt("sell_or_avoid_reason", sar))

    # ── 5. Valuation ──────────────────────────────────────────────────────
    print()
    print("Valuation:")
    print(_fmt("valuation_zone",   val_sigs.get("valuation_zone")))
    print(_fmt("fair_value_price", val_sigs.get("fair_value_price")))
    print(_fmt("current_pe",       val_sigs.get("current_pe")))
    vw = val_sigs.get("valuation_warning", "")
    if vw:
        print(_fmt("[WARN]", vw))

    # ── 6. Exit / Re-entry ────────────────────────────────────────────────
    print()
    print("Exit / Re-entry:")
    print(_fmt("relative_high_exit_signal",   _bool(exit_sigs.get("relative_high_exit_signal"))))
    print(_fmt("failed_breakout_exit_signal", _bool(exit_sigs.get("failed_breakout_exit_signal"))))
    print(_fmt("chip_linked_exit_reason",     exit_sigs.get("chip_linked_exit_reason")))
    print(_fmt("pullback_rebuy_condition",    exit_sigs.get("pullback_rebuy_condition")))
    dnr = exit_sigs.get("do_not_rebuy_yet_reason", "")
    if dnr:
        print(_fmt("do_not_rebuy_yet_reason", dnr))

    # ── Phase 2: KD Advanced ─────────────────────────────────────────────
    print()
    print("Phase 2 — KD Advanced:")
    kd_sig_str = kd_sigs.get("kd_signal", "unavailable")
    print(_fmt("signal",           kd_sig_str))
    print(_fmt("kd_k",             kd_sigs.get("kd_k")))
    print(_fmt("kd_d",             kd_sigs.get("kd_d")))
    print(_fmt("low_golden_cross", _bool(kd_sigs.get("kd_low_golden_cross"))))
    print(_fmt("high_death_cross", _bool(kd_sigs.get("kd_high_death_cross"))))
    print(_fmt("sticky_days",      kd_sigs.get("kd_high_sticky_days")))
    kd_r = kd_sigs.get("kd_strategy_reason", "")
    if kd_r:
        print(_fmt("reason", kd_r))

    # ── Phase 2: Short Interest ───────────────────────────────────────────
    print()
    print("Phase 2 — Short Interest:")
    print(_fmt("signal",              si_sigs.get("short_interest_signal", "unavailable")))
    print(_fmt("squeeze_fuel_score",  si_sigs.get("short_squeeze_fuel_score")))
    print(_fmt("short_covering_warn", _bool(si_sigs.get("short_covering_warning"))))
    print(_fmt("weak_short_increase", _bool(si_sigs.get("weak_stock_short_increase"))))
    si_r = si_sigs.get("short_interest_reason", "")
    if si_r:
        print(_fmt("reason", si_r))

    # ── Phase 2: Bottom Reversal ──────────────────────────────────────────
    print()
    print("Phase 2 — Bottom Reversal:")
    print(_fmt("signal",     br_sigs.get("bottom_signal", "unavailable")))
    print(_fmt("detected",   _bool(br_sigs.get("bottom_reversal_detected"))))
    if br_sigs.get("bottom_reversal_detected"):
        print(_fmt("entry_price", br_sigs.get("rebound_entry_price")))
        print(_fmt("stop_loss",   br_sigs.get("rebound_stop_loss_price")))
        print(_fmt("target",      br_sigs.get("rebound_target_price")))
        print(_fmt("risk_level",  br_sigs.get("rebound_risk_level")))
    br_r = br_sigs.get("rebound_reason", "")
    if br_r:
        print(_fmt("reason", br_r))

    # ── Phase 2: Sector Rotation ──────────────────────────────────────────
    print()
    print("Phase 2 — Sector Rotation:")
    print(_fmt("signal",         sr_sigs.get("sector_signal", "unavailable")))
    print(_fmt("leader",         sr_sigs.get("leader_symbol")))
    print(_fmt("linkage_score",  sr_sigs.get("linkage_score")))
    print(_fmt("laggard_follow", _bool(sr_sigs.get("laggard_follow_signal"))))
    sr_r = sr_sigs.get("sector_rotation_reason", "")
    if sr_r:
        print(_fmt("reason", sr_r))

    # ── Phase 2: Fundamental Quality ─────────────────────────────────────
    print()
    print("Phase 2 — Fundamental Quality:")
    print(_fmt("score",             fq_sigs.get("fundamental_quality_score")))
    print(_fmt("revenue_signal",    fq_sigs.get("revenue_growth_signal", "unavailable")))
    print(_fmt("margin_signal",     fq_sigs.get("margin_quality_signal", "unavailable")))
    print(_fmt("eps_signal",        fq_sigs.get("eps_quality_signal", "unavailable")))
    fq_w = fq_sigs.get("earnings_risk_warning", "")
    if fq_w:
        print(_fmt("[WARN]", fq_w))
    fq_pw = fq_sigs.get("pre_earnings_price_warning", "")
    if fq_pw:
        print(_fmt("[WARN]", fq_pw))

    # ── 7. No Chase Reasons ───────────────────────────────────────────────
    print()
    print("No Chase Reasons:")
    if no_chase:
        for r in no_chase:
            print(f"  - {r}")
    else:
        print("  (none)")

    # ── 8. No Panic Sell Reasons ──────────────────────────────────────────
    print()
    print("No Panic Sell Reasons:")
    if no_panic:
        for r in no_panic:
            print(f"  - {r}")
    else:
        print("  (none)")

    # ── 9. Do Not Rebuy Yet Reasons ───────────────────────────────────────
    print()
    print("Do Not Rebuy Yet Reasons:")
    if no_rebuy:
        for r in no_rebuy:
            print(f"  - {r}")
    else:
        print("  (none)")

    # ── 10. Final Strategy Decision ───────────────────────────────────────
    print()
    print("Final:")
    print(_fmt("decision", final.get("decision")))
    fw = final.get("warning", "")
    if fw:
        print(_fmt("[WARN]", fw))
    print()


# ---------------------------------------------------------------------------
# v0.3.10 — Fetch Historical Daily Price
# ---------------------------------------------------------------------------

def cmd_fetch_daily_history(args: argparse.Namespace) -> None:
    """Fetch historical daily OHLCV from FinMind and merge into daily_k.csv."""
    logger_cmd = logging.getLogger("main.fetch_daily_history")

    symbols_arg = getattr(args, "stocks", None) or []
    universe_size = getattr(args, "universe", None)
    years = getattr(args, "years", 3)
    dry_run = getattr(args, "dry_run", False)

    # Build symbol list
    symbols = []
    if symbols_arg:
        symbols = [s.strip() for s in symbols_arg if s.strip()]
    elif universe_size:
        try:
            from data.universe_manager import UniverseManager
            symbols = UniverseManager().get_universe(universe_size)
        except Exception as exc:
            logger_cmd.warning("Cannot load universe: %s", exc)

    if not symbols:
        print("[ERROR] No symbols specified. Use --stocks 2454 2330 ... or --universe 30")
        return

    from datetime import datetime as _dt, timedelta as _td
    start_date = (_dt.today() - _td(days=int(years * 365))).strftime("%Y-%m-%d")

    from data.providers.public_data_provider import PublicDataProvider
    from data.fundamental_data_builder import FundamentalDataBuilder
    provider = PublicDataProvider(source="finmind")
    builder = FundamentalDataBuilder(dry_run=dry_run)

    print("=" * 60)
    print("  TW Quant Cockpit v0.3.10 — Fetch Historical Daily Price")
    print("=" * 60)
    print(f"  Symbols : {len(symbols)} — {', '.join(symbols[:8])}{'...' if len(symbols) > 8 else ''}")
    print(f"  Start   : {start_date}  (years={years})")
    print(f"  Dry-run : {dry_run}")
    print()

    ok_count = 0
    fail_list = []
    for sym in symbols:
        try:
            df = provider.get_daily_price(sym, start=start_date)
            if df is None or df.empty:
                logger_cmd.warning("[%s] daily price unavailable from FinMind", sym)
                fail_list.append(sym)
                continue
            result = builder.build_daily_k(df)
            rows = result.get("total_rows", 0)
            new_rows = result.get("rows_added", 0)
            print(f"  [{sym}] OK — fetched {new_rows} rows → total {rows} rows in daily_k.csv")
            ok_count += 1
        except Exception as exc:
            logger_cmd.warning("[%s] fetch-daily-history error: %s", sym, exc)
            fail_list.append(sym)

    print()
    print(f"  Done. {ok_count}/{len(symbols)} symbols OK.")
    if fail_list:
        print(f"  Failed: {', '.join(fail_list)}")
    if dry_run:
        print("  [DRY-RUN] No files written.")
    print()
    print("[!] For research and simulation only. Not investment advice.")


# ---------------------------------------------------------------------------
# v0.3.11 — Long-Term Strategy Validation
# ---------------------------------------------------------------------------

def cmd_backtest_long_term_strategy(args: argparse.Namespace) -> None:
    """Validate long-term strategy rules against historical forward returns (v0.3.11)."""
    logger_cmd   = logging.getLogger("main.backtest_long_term_strategy")
    mode         = getattr(args, 'mode',         'real')
    stock        = getattr(args, 'stock',        None)
    holding_days = getattr(args, 'holding_days', 60)
    output_dir   = getattr(args, 'output_dir',   None)
    report_dir   = getattr(args, 'report_dir',   None)
    logger_cmd.info(
        "backtest-long-term-strategy [mode=%s stock=%s holding_days=%d]",
        mode, stock, holding_days,
    )

    try:
        from backtest.long_term_strategy_backtester import LongTermStrategyBacktester
        from reports.long_term_validation_report import LongTermValidationReport

        bt      = LongTermStrategyBacktester(
            mode=mode, stock=stock, holding_days=holding_days, output_dir=output_dir,
        )
        results = bt.run()

        status = results.get('status')
        if status == 'insufficient_data':
            print(results.get('message', '[WARN] 資料不足，無法完成長線回測。'))
            return

        paths    = bt.save_results(results, output_dir=output_dir)
        rpt      = LongTermValidationReport(results)
        rpt_path = rpt.save(output_dir=report_dir)

        conf     = results.get('confidence', {})
        factors  = results.get('factors', {})

        print('\n' + '=' * 60)
        print('  TW Quant Cockpit \u2014 Long-Term Strategy Backtest (v0.3.11)')
        print('=' * 60)
        src_tag = 'REAL CSV SAMPLE' if results.get('is_sample') else 'REAL CSV'
        print(f"  Data source           : {src_tag}")
        print(f"  Mode                  : {mode}")
        print(f"  Holding days          : {holding_days}")
        print(f"  Symbols               : {results.get('n_symbols', 0)}")
        print(f"  Signal rows           : {results.get('n_signals', 0)}")
        print(f"  Valid forward rows    : {results.get('n_valid_fwd', 0)}")
        print(f"  Period                : {results.get('start', _DASH)} \u2192 {results.get('end', _DASH)}")
        print(f"  Statistical confidence: {conf.get('overall', 'INSUFFICIENT')}")
        for reason in conf.get('reasons', []):
            print(f"    - {reason}")
        if conf.get('timing_warning'):
            print(f"    ! {conf['timing_warning']}")

        # EPS factor summary
        eps_data = factors.get('eps_positive', [])
        if eps_data:
            print(f"\n  EPS factor ({holding_days}d forward return):")
            fwd_col_label = f'fwd_{holding_days}d'
            for row in eps_data:
                avg = row.get('avg_return')
                wr  = row.get('win_rate')
                avg_s = f"{float(avg)*100:+.2f}%" if avg is not None else _DASH
                wr_s  = f"{float(wr)*100:.1f}%"   if wr  is not None else _DASH
                print(f"    eps_positive={row.get('bucket'):<6}  N={row.get('n'):>4}  "
                      f"Avg={avg_s}  WinRate={wr_s}  [{row.get('confidence')}]")

        # Signal filter summary
        sf = factors.get('signal_filter', {})
        if sf:
            print(f"\n  Signal filter (BUY_BREAKOUT vs others):")
            for grp in ('filtered', 'excluded'):
                d    = sf.get(grp, {})
                avg  = d.get('avg_return')
                wr   = d.get('win_rate')
                avg_s = f"{float(avg)*100:+.2f}%" if avg is not None else _DASH
                wr_s  = f"{float(wr)*100:.1f}%"   if wr  is not None else _DASH
                print(f"    {grp:<10}  N={d.get('n',0):>4}  Avg={avg_s}  WinRate={wr_s}")

        csv_out = paths.get('signals_df', _DASH)
        print(f"\n  Output CSV  : {csv_out}")
        print(f"  Report      : {rpt_path}")
        print('\n  [!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger_cmd.error("backtest-long-term-strategy failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


# ---------------------------------------------------------------------------
# v0.3.12 — Portfolio & Risk Simulation
# ---------------------------------------------------------------------------

def cmd_simulate_portfolio(args: argparse.Namespace) -> None:
    """Simulate a multi-position portfolio with capital allocation and risk controls (v0.3.12)."""
    logger_cmd        = logging.getLogger("main.simulate_portfolio")
    mode              = getattr(args, 'mode',              'real')
    scenario          = getattr(args, 'scenario',          'balanced')
    initial_capital   = getattr(args, 'initial_capital',   1_000_000)
    max_positions     = getattr(args, 'max_positions',     5)
    position_size_pct = getattr(args, 'position_size_pct', 0.2)
    max_sector_exp    = getattr(args, 'max_sector_exposure_pct', 0.5)
    stop_loss_pct     = getattr(args, 'stop_loss_pct',     0.08)
    take_profit_pct   = getattr(args, 'take_profit_pct',   0.20)
    trailing_stop_pct = getattr(args, 'trailing_stop_pct', 0.10)
    start             = getattr(args, 'start',             None)
    end               = getattr(args, 'end',               None)
    output_dir        = getattr(args, 'output_dir',        None)
    report_dir        = getattr(args, 'report_dir',        None)
    logger_cmd.info(
        "simulate-portfolio [mode=%s scenario=%s capital=%.0f]",
        mode, scenario, initial_capital,
    )

    try:
        import pandas as pd
        from backtest.portfolio_simulator import PortfolioSimulator
        from backtest.portfolio_scenarios import PortfolioScenarios, SCENARIOS
        from reports.portfolio_simulation_report import PortfolioSimulationReport

        run_all = (scenario == 'all')

        print('\n' + '=' * 60)
        print('  TW Quant Cockpit \u2014 Portfolio & Risk Simulation (v0.3.12)')
        print('=' * 60)
        print(f"  Mode             : {mode}")
        print(f"  Scenario         : {scenario}")
        print(f"  Initial capital  : NTD {initial_capital:,.0f}")
        print()

        if run_all:
            # Run all 4 scenarios
            runner = PortfolioScenarios(
                mode=mode, start=start, end=end, initial_capital=initial_capital,
            )
            all_results = runner.run_all()
            # Use 'balanced' as the primary result for display
            primary = all_results.get('balanced') or next(
                (r for r in all_results.values() if r.get('status') == 'ok'), {}
            )
            comp_path = runner.save_comparison(all_results, output_dir=output_dir)
            rpt = PortfolioSimulationReport(primary, all_scenario_results=all_results)
        else:
            # Single scenario (use preset or custom params)
            if scenario in SCENARIOS:
                runner = PortfolioScenarios(
                    mode=mode, start=start, end=end, initial_capital=initial_capital,
                )
                primary = runner.run_selected(scenario)
                all_results = {scenario: primary}
            else:
                # Custom params from CLI
                sim = PortfolioSimulator(
                    mode=mode, start=start, end=end,
                    initial_capital=initial_capital,
                    max_positions=max_positions,
                    position_size_pct=position_size_pct,
                    max_sector_exposure_pct=max_sector_exp,
                    stop_loss_pct=stop_loss_pct,
                    take_profit_pct=take_profit_pct,
                    trailing_stop_pct=trailing_stop_pct,
                )
                primary = sim.run()
                all_results = {scenario: primary}

            comp_path = None
            rpt = PortfolioSimulationReport(primary, all_scenario_results=all_results)

        status = primary.get('status')
        if status == 'insufficient_data':
            print(primary.get('message', '[WARN] 資料不足，無法完成 portfolio simulation。'))
            return

        # Save primary results
        sim_primary = PortfolioSimulator(mode=mode, initial_capital=initial_capital)
        sim_primary._trades      = primary.get('trades_df', pd.DataFrame()).to_dict('records') \
            if hasattr(primary.get('trades_df', None), 'to_dict') else []
        sim_primary._equity_curve = primary.get('equity_df', pd.DataFrame()).to_dict('records') \
            if hasattr(primary.get('equity_df', None), 'to_dict') else []
        sim_primary._daily_pos   = []
        paths    = {}
        out_dir  = output_dir or os.path.join(BASE_DIR, 'data', 'backtest_results')
        os.makedirs(out_dir, exist_ok=True)
        for key, df_key in [('equity_curve', 'equity_df'), ('trades', 'trades_df'),
                             ('daily_positions', 'daily_positions_df')]:
            df = primary.get(df_key)
            if df is not None and not df.empty:
                p = os.path.join(out_dir, f'portfolio_{key}.csv')
                df.to_csv(p, index=False, encoding='utf-8-sig')
                paths[key] = p
        m_df = pd.DataFrame([primary.get('metrics', {})])
        if not m_df.empty:
            p = os.path.join(out_dir, 'portfolio_metrics.csv')
            m_df.to_csv(p, index=False, encoding='utf-8-sig')
            paths['metrics'] = p
        if comp_path:
            paths['comparison'] = comp_path

        rpt_path = rpt.save(output_dir=report_dir)

        # Console output
        conf = primary.get('confidence', {})
        m    = primary.get('metrics', {})
        cfg  = primary.get('config',  {})
        src_tag = 'REAL CSV SAMPLE' if primary.get('is_sample') else 'REAL CSV'
        print(f"  Data source      : {src_tag}")
        print(f"  Universe         : {primary.get('n_symbols', 0)} symbols")
        print(f"  Period           : {primary.get('start', _DASH)} \u2192 {primary.get('end', _DASH)}")
        print(f"  Trading days     : {primary.get('trading_days', _DASH)}")
        print()
        print(f"  Final equity     : NTD {m.get('final_equity', 0):,.0f}")
        print(f"  Total return     : {_fmt_pct(m.get('total_return'))}")
        print(f"  Sharpe           : {m.get('sharpe', _DASH)}")
        print(f"  Max drawdown     : {_fmt_pct(m.get('max_drawdown'))}")
        print(f"  Profit factor    : {m.get('profit_factor', _DASH)}")
        print(f"  Win rate         : {_fmt_pct(m.get('win_rate'), sign=False)}")
        print(f"  Trade count      : {m.get('trade_count', 0)}")
        print(f"  Avg exposure     : {_fmt_pct(m.get('average_exposure'), sign=False)}")
        print(f"  Statistical conf : {conf.get('overall', 'INSUFFICIENT')}")
        for reason in conf.get('reasons', []):
            print(f"    - {reason}")

        # Scenario comparison summary
        if run_all and len(all_results) > 1:
            from backtest.portfolio_scenarios import PortfolioScenarios
            comp_df = PortfolioScenarios.build_comparison_df(all_results)
            print('\n  Scenario comparison:')
            print(f"  {'Scenario':<28} {'Return':>8} {'Sharpe':>7} {'MaxDD':>8} {'PF':>6}")
            print('  ' + '-' * 62)
            for _, row in comp_df.iterrows():
                if row.get('status') != 'ok':
                    print(f"  {row.get('scenario_name',''):<28} ERROR")
                    continue
                print(
                    f"  {row.get('scenario_name',''):<28} "
                    f"{_fmt_pct(row.get('total_return')):>8} "
                    f"{str(row.get('sharpe','—')):>7} "
                    f"{_fmt_pct(row.get('max_drawdown')):>8} "
                    f"{str(row.get('profit_factor','—')):>6}"
                )

        print(f"\n  Output CSV   : {paths.get('equity_curve', _DASH)}")
        if comp_path:
            print(f"  Comparison   : {comp_path}")
        print(f"  Report       : {rpt_path}")
        print('\n  [!] For research and simulation only. Not investment advice.')

    except Exception as exc:
        logger_cmd.error("simulate-portfolio failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_signal_quality(args: argparse.Namespace) -> None:
    """Generate Signal Quality Dashboard — aggregates all backtest results (v0.3.14)."""
    logger_cmd  = logging.getLogger("main.signal_quality")
    mode        = getattr(args, "mode",        "real")
    do_report   = getattr(args, "report",      False)
    do_refresh  = getattr(args, "refresh",     False)
    results_dir = getattr(args, "results_dir", None) or os.path.join(BASE_DIR, "data", "backtest_results")
    report_dir  = getattr(args, "report_dir",  None) or os.path.join(BASE_DIR, "reports")
    logger_cmd.info("signal-quality [mode=%s report=%s refresh=%s]", mode, do_report, do_refresh)

    print()
    print("=" * 60)
    print("  TW Quant Cockpit \u2014 Signal Quality Dashboard (v0.3.14)")
    print("=" * 60)
    print(f"  Mode: {mode}")
    print()

    try:
        from analysis.signal_quality_engine import SignalQualityEngine
        from reports.signal_quality_report import SignalQualityReport

        engine  = SignalQualityEngine(results_dir=results_dir, reports_dir=report_dir, mode=mode)
        results = engine.run()

        if results.get("status") == "no_data":
            print(f"  [WARN] {results.get('message')}")
            print("  Run backtests first:")
            print("    python main.py backtest-buy-points --mode real")
            print("    python main.py validate-score --mode real")
            print("    python main.py backtest-strategy-knowledge --mode real")
            print("    python main.py backtest-long-term-strategy --mode real")
            print("    python main.py simulate-portfolio --mode real --scenario all")
            return

        df   = results.get("summary_df")
        warn = results.get("warnings", [])
        found   = results.get("sources_found", [])
        missing = results.get("sources_missing", [])

        import pandas as pd
        if df is None or (hasattr(df, "empty") and df.empty):
            print("  No signal quality data generated.")
            return

        rec_col = "recommendation" if "recommendation" in df.columns else None
        counts  = df[rec_col].value_counts().to_dict() if rec_col else {}

        overall_conf = "OBSERVATIONAL"

        print(f"  Available backtests  : {', '.join(found) or '—'}")
        if missing:
            print(f"  Missing sources      : {', '.join(missing)}")
        print(f"  Total signals        : {len(df)}")
        print(f"  Confidence           : {overall_conf}")
        print()
        print(f"  BOOST            : {counts.get('BOOST', 0)}")
        print(f"  KEEP             : {counts.get('KEEP', 0)}")
        print(f"  REDUCE           : {counts.get('REDUCE', 0)}")
        print(f"  DISABLE          : {counts.get('DISABLE', 0)}")
        print(f"  INSUFFICIENT     : {counts.get('INSUFFICIENT_SAMPLE', 0)}")

        # Top BOOST signals
        if rec_col:
            boost_df = df[df[rec_col] == "BOOST"]
            if not boost_df.empty:
                print()
                print("  Top BOOST signals:")
                for _, row in boost_df.head(5).iterrows():
                    print(f"    [{row.get('source','?')}] {row.get('signal_group','')}/{row.get('signal_name','?')} — {row.get('reason','')}")

            # Top REDUCE signals
            red_df = df[df[rec_col] == "REDUCE"]
            if not red_df.empty:
                print()
                print("  Top REDUCE signals:")
                for _, row in red_df.head(5).iterrows():
                    print(f"    [{row.get('source','?')}] {row.get('signal_group','')}/{row.get('signal_name','?')} — {row.get('reason','')}")

            # DISABLE candidates
            dis_df = df[df[rec_col] == "DISABLE"]
            if not dis_df.empty:
                print()
                print("  Disable candidates:")
                for _, row in dis_df.iterrows():
                    print(f"    [{row.get('source','?')}] {row.get('signal_group','')}/{row.get('signal_name','?')} — {row.get('reason','')}")

        print()
        print(f"  Output CSV   : {results.get('summary_path', _DASH)}")

        if warn:
            print()
            for w in warn:
                print(f"  [WARN] {w}")

        # Save Markdown report
        if do_report or do_refresh:
            rpt      = SignalQualityReport(results)
            rpt_path = rpt.save(output_dir=report_dir)
            print(f"  Report       : {rpt_path}")
        else:
            rpt_path = None

        if not (do_report or do_refresh):
            print("  (Use --report to generate Markdown report)")

        print()
        print("  [!] Simulation only. Recommendations do not automatically change strategy weights.")
        print("  [!] For research and simulation only. Not investment advice.")

    except Exception as exc:
        logger_cmd.error("signal-quality failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def cmd_tune_rule_weights(args: argparse.Namespace) -> None:
    """Run Rule Weight Tuning Lab — compare 7 scoring weight configurations (v0.3.15)."""
    logger_cmd  = logging.getLogger("main.tune_rule_weights")
    mode        = getattr(args, "mode",           "real")
    config_name = getattr(args, "config",         "all")
    initial_cap = getattr(args, "initial_capital", 1_000_000)
    start       = getattr(args, "start",          None)
    end         = getattr(args, "end",            None)
    do_report   = getattr(args, "report",         False)
    results_dir = getattr(args, "results_dir",    None) or os.path.join(BASE_DIR, "data", "backtest_results")
    report_dir  = getattr(args, "report_dir",     None) or os.path.join(BASE_DIR, "reports")

    logger_cmd.info(
        "tune-rule-weights [mode=%s config=%s capital=%.0f]",
        mode, config_name, initial_cap,
    )

    print()
    print("=" * 65)
    print("  TW Quant Cockpit \u2014 Rule Weight Tuning Lab (v0.3.15)")
    print("=" * 65)
    print(f"  Mode             : {mode}")
    print(f"  Config(s)        : {config_name}")
    print(f"  Initial capital  : NTD {initial_cap:,.0f}")
    print()
    print("  [!] Advisory Only. Does NOT auto-apply weights to production strategy.")
    print("  [!] Simulation Only. No Real Orders.")
    print()

    try:
        from tuning.rule_weight_tuner import RuleWeightTuner
        from tuning.rule_weight_scenarios import get_all_scenarios

        if config_name != "all":
            # Single config evaluation
            scenarios = get_all_scenarios(results_dir)
            if config_name not in scenarios:
                valid = list(scenarios.keys())
                print(f"  ERROR: unknown config '{config_name}'. Choose from: {valid}")
                sys.exit(1)

            tuner = RuleWeightTuner(
                mode=mode, start=start, end=end,
                initial_capital=initial_cap,
                results_dir=results_dir, reports_dir=report_dir,
            )
            cfg = scenarios[config_name]
            result = tuner.evaluate_config(cfg)
            m = result.get("metrics", {})
            status = result.get("status", "error")

            print(f"  Config           : {config_name}")
            print(f"  Status           : {status}")
            if status == "ok":
                print(f"  Total return     : {_fmt_pct(m.get('total_return'))}")
                print(f"  Sharpe           : {m.get('sharpe', _DASH)}")
                print(f"  Max drawdown     : {_fmt_pct(m.get('max_drawdown'))}")
                print(f"  Profit factor    : {m.get('profit_factor', _DASH)}")
                print(f"  Win rate         : {_fmt_pct(m.get('win_rate'), sign=False)}")
                print(f"  Trade count      : {m.get('trade_count', 0)}")
            else:
                print(f"  Message          : {result.get('message', _DASH)}")
            return

        # Run all 7 configs
        tuner = RuleWeightTuner(
            mode=mode, start=start, end=end,
            initial_capital=initial_cap,
            results_dir=results_dir, reports_dir=report_dir,
        )
        results = tuner.run()

        status = results.get("status")
        if status == "insufficient_data":
            print(f"  [WARN] {results.get('message', 'insufficient data')}")
            print("  Run simulations first to build backtest data:")
            print("    python main.py simulate-portfolio --mode real --scenario all")
            return
        if status != "ok":
            print(f"  ERROR: {results.get('message', 'unknown error')}")
            return

        comp_df   = results.get("comparison_df")
        best      = results.get("best_config")
        bs_best   = results.get("best_by_sharpe")
        dd_best   = results.get("best_by_drawdown")
        pf_best   = results.get("best_by_pf")
        warnings  = results.get("warnings", [])

        print(f"  Configs evaluated : {results.get('n_configs', 0)}")
        print()

        if comp_df is not None and not comp_df.empty:
            print(f"  {'Rank':<5} {'Config':<28} {'Return':>8} {'Sharpe':>7} "
                  f"{'MaxDD':>8} {'PF':>6} {'B.Score':>8} {'DQ?':>4}")
            print("  " + "-" * 75)
            for _, row in comp_df.iterrows():
                dq_s = "YES" if row.get("disqualified") else "no"
                bs_s = f"{float(row['balanced_score']):.4f}" \
                    if row.get("balanced_score") is not None else "—"
                print(
                    f"  {str(row.get('rank','')):<5} "
                    f"{str(row.get('config_name','')):<28} "
                    f"{_fmt_pct(row.get('total_return')):>8} "
                    f"{str(row.get('sharpe','—')):>7} "
                    f"{_fmt_pct(row.get('max_drawdown')):>8} "
                    f"{str(row.get('profit_factor','—')):>6} "
                    f"{bs_s:>8} "
                    f"{dq_s:>4}"
                )

        print()
        if best:
            print(f"  Best config (balanced score) : {best.name}")
        if bs_best:
            print(f"  Best by Sharpe               : {bs_best.name}")
        if dd_best:
            print(f"  Best by drawdown             : {dd_best.name}")
        if pf_best:
            print(f"  Best by PF                   : {pf_best.name}")

        paths = results.get("save_paths", {})
        if paths.get("comparison"):
            print(f"\n  Comparison CSV : {paths['comparison']}")

        if warnings:
            print()
            for w in warnings:
                print(f"  [WARN] {w}")

        # Generate report
        if do_report:
            from tuning.rule_weight_report import RuleWeightReport
            rpt = RuleWeightReport(results)
            rpt_path = rpt.save(output_dir=report_dir)
            print(f"  Report         : {rpt_path}")
        else:
            print("  (Use --report to generate Markdown report)")

        print()
        print("  [!] Advisory only. Recommendations do NOT auto-apply weights.")
        print("  [!] For research and simulation only. Not investment advice.")

    except Exception as exc:
        logger_cmd.error("tune-rule-weights failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


def _fmt_pct(v, sign=True):
    """Format a fraction (0.15 → '+15.00%'). Returns '—' if None."""
    if v is None:
        return _DASH
    try:
        f = float(v)
        if sign:
            return f'{f*100:+.2f}%'
        return f'{f*100:.2f}%'
    except Exception:
        return str(v)


# ---------------------------------------------------------------------------
# v0.3.16 — Auto Report Center
# ---------------------------------------------------------------------------

def cmd_auto_report(args: argparse.Namespace) -> None:
    """Run Auto Report Center — one-click daily research report pack (v0.3.16)."""
    logger_cmd  = logging.getLogger("main.auto_report")
    mode        = getattr(args, "mode",        "real")
    profile     = getattr(args, "profile",     "full")
    stocks      = getattr(args, "stocks",      None) or []
    top_n       = getattr(args, "top",         8)
    output_dir  = getattr(args, "output_dir",  None)
    results_dir = getattr(args, "results_dir", None)
    report_date = getattr(args, "report_date", None)

    logger_cmd.info(
        "auto-report [mode=%s profile=%s date=%s]",
        mode, profile, report_date or "today",
    )

    print()
    print("=" * 65)
    print("  TW Quant Cockpit \u2014 Auto Report Center (v0.3.16)")
    print("=" * 65)
    print(f"  Mode    : {mode}")
    print(f"  Profile : {profile}")
    print(f"  Date    : {report_date or 'today'}")
    print(f"  Stocks  : {stocks or 'from universe'}")
    print()
    print("  [!] Research Only. Simulation Only. No Real Orders.")
    print()

    try:
        from reports.auto_report_center import AutoReportCenter

        center = AutoReportCenter(
            mode=mode,
            profile=profile,
            stocks=stocks,
            top_n=top_n,
            output_dir=output_dir,
            results_dir=results_dir,
            report_date=report_date,
        )
        results = center.run()

        status    = results.get("status", "unknown")
        gen       = results.get("generated", [])
        failed    = results.get("failed", [])
        out_dir   = results.get("output_dir", "")
        index_p   = results.get("index_path")
        manifest  = results.get("manifest_path")

        print(f"  Status            : {status}")
        print(f"  Output folder     : {out_dir}")
        print(f"  Generated reports : {len(gen)}")
        print(f"  Failed reports    : {len(failed)}")
        print()

        if gen:
            print("  Generated:")
            for g in gen:
                print(f"    ✓  {g.get('name', '')}")

        if failed:
            print()
            print("  Failed:")
            for f in failed:
                print(f"    ✗  {f.get('name', '')}  — {f.get('error', '')}")

        print()
        if index_p:
            print(f"  Index     : {index_p}")
        if manifest:
            print(f"  Manifest  : {manifest}")

        print()
        print("  [!] All outputs are research-only simulation artifacts.")
        print("  [!] Does NOT auto-apply weights. Does NOT place real orders.")

    except Exception as exc:
        logger_cmd.error("auto-report failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")


# ---------------------------------------------------------------------------
# v0.3.17 — API Automation Scheduler Commands
# ---------------------------------------------------------------------------

def _print_scheduler_header() -> None:
    print()
    print("=" * 65)
    print("  TW Quant Cockpit \u2014 API Automation Scheduler (v0.3.17)")
    print("=" * 65)
    print("  [!] Read Only Automation")
    print("  [!] No real orders will be placed")
    print("  [!] Scheduler does NOT trade. Does NOT modify weights.")
    print()


def cmd_scheduler_init_config(args: argparse.Namespace) -> None:
    """Create a safe, all-disabled scheduler config file (v0.3.17)."""
    _print_scheduler_header()
    config_path = getattr(args, "config", None) or os.path.join(BASE_DIR, "config", "scheduler_config.yaml")
    try:
        from automation.scheduler import AutomationScheduler
        sched = AutomationScheduler(config_path=config_path)
        path  = sched.save_default_config()
        print(f"  Config written : {path}")
        print("  All tasks are disabled by default.")
        print("  Edit the YAML to enable tasks.")
    except Exception as exc:
        print(f"ERROR: {exc}")


def cmd_scheduler_status(args: argparse.Namespace) -> None:
    """Show automation scheduler status (v0.3.17)."""
    _print_scheduler_header()
    config_path = getattr(args, "config", None) or os.path.join(BASE_DIR, "config", "scheduler_config.yaml")
    log_dir     = getattr(args, "log_dir", None) or os.path.join(BASE_DIR, "logs", "automation")
    try:
        from automation.scheduler import AutomationScheduler
        sched  = AutomationScheduler(config_path=config_path, log_dir=log_dir)
        status = sched.status()

        print(f"  Scheduler Enabled : {status.get('scheduler_enabled', False)}")
        print(f"  Mode              : {status.get('mode', '—')}")
        print(f"  Read Only         : {status.get('read_only', True)}")
        print(f"  No Real Orders    : {status.get('no_real_orders', True)}")
        print(f"  Total Tasks       : {status.get('total_tasks', 0)}")
        print(f"  Enabled Tasks     : {len(status.get('enabled_tasks', []))}")
        print(f"  Next Task         : {status.get('next_task', '—')}")
        print(f"  Next Run          : {status.get('next_run', '—')}")
        print()
        summary = status.get("run_summary", {})
        print(f"  Recent Runs (last 50):")
        print(f"    Total   : {summary.get('total', 0)}")
        print(f"    OK      : {summary.get('ok', 0)}")
        print(f"    Failed  : {summary.get('failed', 0)}")
        print(f"    Warning : {summary.get('warning', 0)}")
        print(f"    Last Run: {summary.get('last_run_at', '—')}")
        print(f"    Last Status: {summary.get('last_status', '—')}")
    except Exception as exc:
        print(f"ERROR: {exc}")


def cmd_scheduler_list(args: argparse.Namespace) -> None:
    """List all automation tasks and their schedule (v0.3.17)."""
    _print_scheduler_header()
    config_path = getattr(args, "config", None) or os.path.join(BASE_DIR, "config", "scheduler_config.yaml")
    log_dir     = getattr(args, "log_dir", None) or os.path.join(BASE_DIR, "logs", "automation")
    try:
        from automation.scheduler import AutomationScheduler
        sched = AutomationScheduler(config_path=config_path, log_dir=log_dir)
        tasks = sched.list_tasks()

        if not tasks:
            print("  No tasks configured. Run scheduler-init-config first.")
            return

        print(f"  {'Task':<32} {'Enabled':<8} {'Schedule':<12} {'Time':<7} {'Last Status':<12} {'Read Only'}")
        print("  " + "-" * 85)
        for t in tasks:
            sched_type = t.get("schedule_type", "—")
            if sched_type == "weekly":
                sched_str = f"weekly/wd{t.get('weekday','?')}"
            elif sched_type == "monthly":
                sched_str = f"monthly/d{t.get('month_day','?')}"
            else:
                sched_str = sched_type
            print(
                f"  {t.get('task_name',''):<32} "
                f"{'YES' if t.get('enabled') else 'no':<8} "
                f"{sched_str:<12} "
                f"{t.get('run_time','—'):<7} "
                f"{str(t.get('last_status','—')):<12} "
                f"{str(t.get('read_only', True))}"
            )
    except Exception as exc:
        print(f"ERROR: {exc}")


def cmd_scheduler_next_runs(args: argparse.Namespace) -> None:
    """Show next scheduled run times for all tasks (v0.3.17)."""
    _print_scheduler_header()
    config_path = getattr(args, "config", None) or os.path.join(BASE_DIR, "config", "scheduler_config.yaml")
    log_dir     = getattr(args, "log_dir", None) or os.path.join(BASE_DIR, "logs", "automation")
    try:
        from automation.scheduler import AutomationScheduler
        sched = AutomationScheduler(config_path=config_path, log_dir=log_dir)
        next_runs = sched.next_run_times()

        print(f"  {'Task':<32} {'Next Run (ISO)'}")
        print("  " + "-" * 60)
        for name, nrt in next_runs.items():
            print(f"  {name:<32} {nrt or 'DISABLED'}")
        print()
        print("  (Tasks with enabled=false show DISABLED)")
    except Exception as exc:
        print(f"ERROR: {exc}")


def cmd_scheduler_run(args: argparse.Namespace) -> None:
    """Run a single automation task once (v0.3.17)."""
    _print_scheduler_header()
    task_name   = getattr(args, "task",    None)
    mode        = getattr(args, "mode",    "real")
    config_path = getattr(args, "config",  None) or os.path.join(BASE_DIR, "config", "scheduler_config.yaml")
    log_dir     = getattr(args, "log_dir", None) or os.path.join(BASE_DIR, "logs", "automation")

    if not task_name:
        print("  ERROR: --task is required. Example: --task daily_auto_report")
        return

    print(f"  Task   : {task_name}")
    print(f"  Mode   : {mode}")
    print()

    try:
        from automation.scheduler import AutomationScheduler
        sched  = AutomationScheduler(config_path=config_path, mode=mode, log_dir=log_dir)
        result = sched.run_once(task_name)

        status   = result.get("status",           "unknown")
        duration = result.get("duration_seconds", 0)
        outputs  = result.get("generated_outputs", [])
        warnings = result.get("warnings",          [])
        errors   = result.get("errors",            [])

        print(f"  Status    : {status.upper()}")
        print(f"  Started   : {result.get('started_at', '—')}")
        print(f"  Finished  : {result.get('finished_at', '—')}")
        print(f"  Duration  : {duration:.1f}s")
        print(f"  Read Only : {result.get('read_only', True)}")
        print(f"  No Orders : {result.get('no_real_orders', True)}")

        if outputs:
            print()
            print("  Outputs:")
            for o in outputs:
                print(f"    \u2713  {o}")

        if warnings:
            print()
            print("  Warnings:")
            for w in warnings:
                print(f"    [WARN] {w}")

        if errors:
            print()
            print("  Errors:")
            for e in errors:
                print(f"    [ERR ] {e}")

        log_path = os.path.join(log_dir, "task_runs.jsonl")
        status_path = os.path.join(log_dir, "latest_status.json")
        print()
        print(f"  Log            : {log_path}")
        print(f"  Latest status  : {status_path}")

    except Exception as exc:
        logging.getLogger("main.scheduler_run").error("scheduler-run failed: %s", exc, exc_info=True)
        print(f"ERROR: {exc}")

    print()
    print("  [!] Read Only Automation. No real orders placed.")
    print("  [!] For research and simulation only. Not investment advice.")


# ---------------------------------------------------------------------------
# v0.3.18 — Provider Health CLI
# ---------------------------------------------------------------------------

def _print_provider_health_header() -> None:
    print()
    print("=" * 60)
    print("  TW Quant Cockpit — Provider Health  (v0.3.18)")
    print("=" * 60)
    print()
    print("  [!] Read Only")
    print("  [!] No Real Orders")
    print("  [!] Tokens masked — no full token displayed")
    print()


def cmd_provider_health(args: argparse.Namespace) -> None:
    """Check provider health status (v0.3.18)."""
    import os
    _print_provider_health_header()

    report_flag      = getattr(args, "report", False)
    create_example   = getattr(args, "create_env_example", False)
    provider_filter  = getattr(args, "provider", "all")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, ".env")

    # --- create config/env.example (safe path only) ---
    if create_example:
        try:
            from data.providers.token_safe_config import TokenSafeConfig
            cfg = TokenSafeConfig(env_path=env_path)
            # Only write to config/env.example — never overwrite root .env.example
            # (root .env.example may already contain Shioaji + other fields)
            out = cfg.create_env_example(
                path=os.path.join(base_dir, "config", "env.example")
            )
            print(f"  config/env.example created: {out}")
            print("  Note: Root .env.example was NOT overwritten.")
            print("        Add FINMIND_TOKEN= etc. to your .env.example manually if needed.")
        except Exception as exc:
            print(f"  ERROR creating env.example: {exc}")
        print()
        return

    # --- run health check ---
    try:
        from data.providers.provider_health import ProviderHealthChecker
        providers_arg = None
        if provider_filter and provider_filter.lower() != "all":
            providers_arg = [provider_filter]
        checker = ProviderHealthChecker(
            env_path=env_path,
            providers=providers_arg,
        )
        result = checker.run_all()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    # --- print provider summary ---
    print("  Provider Summary:")
    print()
    for p in result.get("providers", []):
        name   = p.get("provider_name", "")
        status = p.get("status", "")
        tc     = "✓" if p.get("token_configured", False) else "✗"
        msg    = p.get("message", "")[:60]
        print(f"    {name:<28} {status:<16} token:{tc}  {msg}")
    print()

    # --- token status ---
    print("  Token Status:")
    print()
    for name, info in result.get("token_status", {}).items():
        configured = info.get("configured", False)
        masked     = info.get("masked", "(not configured)")
        mark       = "✓" if configured else "✗"
        print(f"    {name:<20} configured:{mark}  {masked}")
    print()

    # --- capability matrix summary ---
    print("  Capability Matrix:")
    print()
    for p in result.get("providers", []):
        pname = p.get("provider_name", "")
        caps  = p.get("capabilities", {})
        ro_exec = caps.get("real_order_execution", False)
        mark = "[DISABLED]" if not ro_exec else "[**UNSAFE**]"
        daily = "✓" if caps.get("daily_price") else "✗"
        rev   = "✓" if caps.get("monthly_revenue") else "✗"
        inst  = "✓" if caps.get("institutional") else "✗"
        print(f"    {pname:<28} daily:{daily} revenue:{rev} institutional:{inst}  real_order_execution:{mark}")
    print()

    # --- safety summary ---
    print("  Safety:")
    print("    real_order_execution: DISABLED for all providers  [✓]")
    print("    read_only_guarantee : True  [✓]")
    print("    no_real_orders      : True  [✓]")
    print()

    # --- report ---
    if report_flag:
        try:
            from reports.provider_health_report import ProviderHealthReportBuilder
            from datetime import datetime
            builder = ProviderHealthReportBuilder(
                report_date=datetime.now().strftime("%Y-%m-%d"),
                health_data=result,
            )
            reports_dir = os.path.join(base_dir, "reports")
            out_path = builder.build(output_dir=reports_dir)
            print(f"  Report: {out_path}")
        except Exception as exc:
            print(f"  Report ERROR: {exc}")
        print()

    print("  [!] Read Only. No Real Orders. Research and simulation only.")


# ---------------------------------------------------------------------------
# v0.3.19 — Provider Auto Fetch & Data Freshness CLI
# ---------------------------------------------------------------------------

def _print_auto_fetch_header() -> None:
    print()
    print("=" * 60)
    print("  TW Quant Cockpit — Data Provider Auto Fetch  (v0.3.19)")
    print("=" * 60)
    print()
    print("  [!] Read Only")
    print("  [!] No Real Orders")
    print("  [!] Tokens masked — no full token displayed")
    print()


def cmd_provider_auto_fetch(args: argparse.Namespace) -> None:
    """Run provider auto fetch for one or all datasets (v0.3.19)."""
    import os
    _print_auto_fetch_header()

    mode        = getattr(args, "mode", "real")
    dry_run     = getattr(args, "dry_run", False)
    dataset     = getattr(args, "dataset", "all")
    months      = getattr(args, "months", 24)
    max_sym     = getattr(args, "max_symbols", None)
    output_root = getattr(args, "output_root", None)
    report_dir  = getattr(args, "report_dir", None)
    report_flag = getattr(args, "report", False)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    datasets = None
    if dataset and dataset.lower() != "all":
        datasets = [dataset]

    print(f"  Mode     : {mode.upper()}")
    print(f"  Dry Run  : {'Yes' if dry_run else 'No'}")
    print(f"  Dataset  : {dataset}")
    print(f"  Months   : {months}")
    print()

    try:
        from data.providers.auto_fetcher import DataProviderAutoFetcher
        fetcher = DataProviderAutoFetcher(
            mode=mode,
            output_root=output_root or base_dir,
            report_dir=report_dir or os.path.join(base_dir, "reports"),
            months=months,
            max_symbols=max_sym,
            dry_run=dry_run,
        )
        result = fetcher.run(datasets=datasets)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    print("  Dataset Results:")
    print()
    for ds, info in result.get("datasets", {}).items():
        status = info.get("status", "")
        prov   = info.get("provider_used", "—")
        rf     = info.get("rows_fetched", 0)
        rw     = info.get("rows_written", 0)
        warn   = "; ".join(info.get("warnings", []))[:60]
        print(f"    {ds:<20} {status:<10} provider:{prov}  fetched:{rf}  written:{rw}")
        if warn:
            print(f"               [warn] {warn}")
    print()

    fs = result.get("freshness_summary", {})
    if fs:
        print("  Freshness:")
        print()
        for ds, info in fs.items():
            st = info.get("status", "")
            ld = info.get("latest_date", "—")
            print(f"    {ds:<20} {st:<16} latest:{ld}")
        print()

    for w in result.get("warnings", [])[:10]:
        print(f"  [WARN] {w}")
    for e in result.get("errors", [])[:5]:
        print(f"  [ERR]  {e}")

    print()
    print(f"  Rows fetched : {result.get('rows_fetched', 0)}")
    print(f"  Rows written : {result.get('rows_written', 0)}")
    print(f"  Providers    : {', '.join(result.get('providers_used', [])) or '—'}")
    print(f"  Status       : {result.get('status', '')}")

    if report_flag:
        try:
            from reports.data_provider_fetch_report import DataProviderFetchReportBuilder
            from data.providers.data_freshness import DataFreshnessChecker
            from datetime import datetime as _dt
            fc      = DataFreshnessChecker()
            fresh   = fc.run_all()
            builder = DataProviderFetchReportBuilder(
                report_date=_dt.now().strftime("%Y-%m-%d"),
                mode=mode,
                fetch_result=result,
                freshness=fresh,
            )
            rdir = report_dir or os.path.join(base_dir, "reports")
            path = builder.build(output_dir=rdir)
            print()
            print(f"  Report: {path}")
        except Exception as exc:
            print(f"  Report ERROR: {exc}")

    print()
    print("  [!] Read Only. No Real Orders. Research and simulation only.")


def cmd_data_freshness(args: argparse.Namespace) -> None:
    """Check data freshness across standard import datasets (v0.3.19)."""
    import os
    print()
    print("=" * 60)
    print("  TW Quant Cockpit — Data Freshness Check  (v0.3.19)")
    print("=" * 60)
    print()

    dataset     = getattr(args, "dataset", None)
    report_flag = getattr(args, "report", False)
    base_dir    = os.path.dirname(os.path.abspath(__file__))

    try:
        from data.providers.data_freshness import DataFreshnessChecker
        checker = DataFreshnessChecker()
        if dataset:
            result = {"datasets": {dataset: checker.check_dataset(dataset)}, "summary": {}}
        else:
            result = checker.run_all()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    print("  Dataset Freshness:")
    print()
    for ds, info in result.get("datasets", {}).items():
        status = info.get("status", "")
        ld     = info.get("latest_date", "—")
        rows   = info.get("rows", 0)
        warn   = info.get("warning", "")[:60]
        action = info.get("recommended_action", "")
        print(f"    {ds:<25} {status:<20} latest:{ld}  rows:{rows}")
        if warn:
            print(f"               [warn] {warn}")
        if action:
            print(f"               [action] {action}")
    print()

    summary = result.get("summary", {})
    if summary:
        print(f"  Summary: fresh={summary.get('fresh',0)}  stale={summary.get('stale',0)}  "
              f"missing={summary.get('missing',0)}  partial={summary.get('partial',0)}")
        print()

    if report_flag:
        try:
            from reports.data_provider_fetch_report import DataProviderFetchReportBuilder
            from datetime import datetime as _dt
            builder = DataProviderFetchReportBuilder(
                report_date=_dt.now().strftime("%Y-%m-%d"),
                freshness=result,
            )
            rdir = os.path.join(base_dir, "reports")
            path = builder.build(output_dir=rdir)
            print(f"  Report: {path}")
        except Exception as exc:
            print(f"  Report ERROR: {exc}")
        print()

    print("  [!] Read Only. No Real Orders. Research and simulation only.")


# ---------------------------------------------------------------------------
# v0.3.20 — Data Quality Gate & Production Readiness Score
# ---------------------------------------------------------------------------

def cmd_data_quality_gate(args: argparse.Namespace) -> None:
    """Run data quality gate and production readiness score (v0.3.20)."""
    import os
    print()
    print("=" * 64)
    print("  TW Quant Cockpit — Data Quality Gate  (v0.3.20)")
    print("=" * 64)
    print()

    mode        = getattr(args, "mode", "real")
    report_flag = getattr(args, "report", False)
    check_mock  = getattr(args, "check_mock", False)
    import_root = getattr(args, "import_root", None)
    results_dir = getattr(args, "results_dir", None)
    report_dir  = getattr(args, "report_dir", None)
    base_dir    = os.path.dirname(os.path.abspath(__file__))

    print(f"  Mode: {mode}")
    print()

    try:
        from quality.data_quality_gate import DataQualityGate
        kwargs = {"mode": mode}
        if import_root:
            kwargs["import_root"] = import_root
        if results_dir:
            kwargs["results_dir"] = results_dir
        gate = DataQualityGate(**kwargs)

        if check_mock:
            # Only run mock contamination check
            from quality.mock_contamination_checker import MockContaminationChecker
            checker = MockContaminationChecker(
                import_root=import_root or os.path.join(base_dir, "data", "import"),
                results_dir=results_dir or os.path.join(base_dir, "data", "backtest_results"),
                mode=mode,
            )
            result = checker.run()
            print(f"  Mock Contamination: {result.status}  Score: {result.score:.1f}")
            print()
            if result.details:
                print("  Issues:")
                for d in result.details[:10]:
                    print(f"    {d}")
                print()
            if result.recommended_action:
                print(f"  Action: {result.recommended_action}")
            print()
            print("  [!] Read Only. No Real Orders.")
            return

        gate_result = gate.run()

    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    # Production readiness
    prod  = gate_result.get("production_readiness_score", 0.0)
    btest = gate_result.get("backtest_readiness_score", 0.0)
    p_cls = gate_result.get("production_classification", "")
    b_cls = gate_result.get("backtest_classification", "")

    print(f"  Production Readiness: {prod:.1f}  ({p_cls})")
    print(f"  Backtest Readiness:   {btest:.1f}  ({b_cls})")
    print()

    # Sub-scores
    print("  Sub-Scores:")
    scores = gate_result.get("scores", {})
    _labels = [
        ("freshness_score",          "Freshness"),
        ("coverage_score",           "Coverage"),
        ("source_confidence_score",  "Source Confidence"),
        ("timing_quality_score",     "Timing Quality"),
        ("sample_size_score",        "Sample Size"),
        ("intraday_coverage_score",  "Intraday Coverage"),
        ("provider_health_score",    "Provider Health"),
        ("mock_contamination_score", "Mock Contamination"),
    ]
    for key, label in _labels:
        val = scores.get(key, 0.0)
        print(f"    {label:<25} {val:.1f}")
    print()

    # Gate decisions
    print("  Gate Decisions:")
    gates = gate_result.get("gates", {})
    _gate_labels = [
        ("RESEARCH_ONLY",       "Research Only"),
        ("BACKTEST_READY",      "Backtest Ready"),
        ("PAPER_TRADING_READY", "Paper Trading Ready"),
        ("PRODUCTION_BLOCKED",  "Production Blocked"),
        ("API_READY_READONLY",  "API Ready (Read-Only)"),
        ("INTRADAY_READY",      "Intraday Ready"),
        ("LONG_TERM_READY",     "Long-Term Ready"),
        ("PORTFOLIO_READY",     "Portfolio Ready"),
        ("REAL_ORDER_READY",    "Real Order Ready"),
    ]
    for key, label in _gate_labels:
        val = gates.get(key)
        status = "YES" if val is True else "NO" if val is False else str(val)
        print(f"    {label:<25} {status}")
    print()

    # Warnings
    warnings = gate_result.get("warnings", [])
    if warnings:
        print("  Warnings:")
        for w in warnings[:5]:
            print(f"    {w}")
        print()

    # Generate report
    if report_flag:
        try:
            from reports.data_quality_gate_report import DataQualityGateReportBuilder
            rdir = report_dir or os.path.join(base_dir, "reports")
            builder = DataQualityGateReportBuilder(gate_result)
            path = builder.build(output_dir=rdir)
            print(f"  Report: {path}")
        except Exception as exc:
            print(f"  Report ERROR: {exc}")
        print()

    print("  [!] Read Only. No Real Orders. PRODUCTION_BLOCKED=True always.")


# ---------------------------------------------------------------------------
# v0.3.21 — Daily Research Workflow Commands
# ---------------------------------------------------------------------------

def _print_workflow_result(result: dict) -> None:
    """Print a workflow result dict to console."""
    mode    = result.get("mode", "").upper()
    profile = result.get("profile", "")
    status  = result.get("overall_status", result.get("status", "UNKNOWN"))
    dur     = result.get("duration_seconds", 0.0)
    ok_n    = len(result.get("ok_steps", []))
    fail_n  = len(result.get("failed_steps", []))
    warn_n  = result.get("warning_count", 0)

    print(f"  Mode:            {mode}")
    print(f"  Profile:         {profile}")
    print(f"  Status:          {status}")
    print(f"  Duration:        {dur:.1f}s")
    print(f"  OK steps:        {ok_n}")
    print(f"  Failed steps:    {fail_n}")
    print(f"  Warnings:        {warn_n}")
    print(f"  Read Only:       True")
    print(f"  No Real Orders:  True")
    print(f"  Production:      BLOCKED")
    print()

    qg = result.get("quality_gate_summary", {})
    if qg:
        prod  = qg.get("production_readiness_score", "N/A")
        btest = qg.get("backtest_readiness_score", "N/A")
        p_cls = qg.get("production_classification", "")
        prod_str  = f"{prod:.1f}"  if isinstance(prod,  float) else str(prod)
        btest_str = f"{btest:.1f}" if isinstance(btest, float) else str(btest)
        print(f"  Production Readiness: {prod_str} ({p_cls})")
        print(f"  Backtest Readiness:   {btest_str}")
        print()

    steps = result.get("steps", [])
    if steps:
        print("  Steps:")
        for s in steps:
            name   = s.get("step_name", "")
            sts    = s.get("status", "")
            dur_s  = s.get("duration_seconds", 0.0)
            err_n  = len(s.get("errors", []))
            warn_s = len(s.get("warnings", []))
            print(f"    {name:<30} {sts:<8} {dur_s:.1f}s  warn={warn_s}  err={err_n}")
        print()

    failed = result.get("failed_steps", [])
    if failed:
        print(f"  Failed: {', '.join(failed)}")
        print()

    ar_dir = result.get("auto_report_dir", "")
    if ar_dir:
        ar_n = result.get("auto_report_count", 0)
        print(f"  Auto Report: {ar_n} reports → {ar_dir}")
        print()


def cmd_update_data(args: argparse.Namespace) -> None:
    """Daily data update workflow (v0.3.21)."""
    import os
    print()
    print("=" * 64)
    print("  TW Quant Cockpit — Update Data  (v0.3.21)")
    print("  Research Only | Read Only | No Real Orders")
    print("  Production Trading: BLOCKED")
    print("=" * 64)
    print()

    mode    = getattr(args, "mode", "real")
    profile = getattr(args, "profile", "standard")
    dry_run = getattr(args, "dry_run", False)
    if dry_run:
        print("  [DRY-RUN] Data fetch steps will not write files.")
        print()

    try:
        from workflow.daily_workflow import DailyResearchWorkflow
        wf = DailyResearchWorkflow(mode=mode, profile=profile, dry_run=dry_run)
        result = wf.run_update_data()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    _print_workflow_result(result)
    print("  [!] Read Only. No Real Orders. Production Trading: BLOCKED.")


def cmd_run_research(args: argparse.Namespace) -> None:
    """Daily research workflow (v0.3.21)."""
    import os
    print()
    print("=" * 64)
    print("  TW Quant Cockpit — Run Research  (v0.3.21)")
    print("  Research Only | Read Only | No Real Orders")
    print("  Production Trading: BLOCKED")
    print("=" * 64)
    print()

    mode    = getattr(args, "mode", "real")
    profile = getattr(args, "profile", "standard")

    print(f"  Mode: {mode}  Profile: {profile}")
    print()

    try:
        from workflow.daily_workflow import DailyResearchWorkflow
        wf = DailyResearchWorkflow(mode=mode, profile=profile)
        result = wf.run_research()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    _print_workflow_result(result)
    print("  [!] Read Only. No Real Orders. Do NOT auto-apply weights. Production Trading: BLOCKED.")


def cmd_daily_workflow(args: argparse.Namespace) -> None:
    """Full daily research workflow: update-data + run-research (v0.3.21)."""
    import os
    print()
    print("=" * 64)
    print("  TW Quant Cockpit — Daily Workflow  (v0.3.21)")
    print("  Research Only | Read Only | No Real Orders")
    print("  Production Trading: BLOCKED")
    print("=" * 64)
    print()

    mode     = getattr(args, "mode", "real")
    profile  = getattr(args, "profile", "standard")
    dry_run  = getattr(args, "dry_run", False)
    open_gui = getattr(args, "open_gui", False)

    print(f"  Mode: {mode}  Profile: {profile}")
    if dry_run:
        print("  [DRY-RUN] Fetch steps will not write files.")
    print()

    try:
        from workflow.daily_workflow import DailyResearchWorkflow
        wf = DailyResearchWorkflow(mode=mode, profile=profile, dry_run=dry_run)
        result = wf.run_full_workflow()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    _print_workflow_result(result)

    if open_gui:
        print("  Opening cockpit GUI...")
        print()
        try:
            from gui.dashboard import launch
            launch(mode=mode)
        except Exception as exc:
            print(f"  GUI ERROR: {exc}")

    print("  [!] Read Only. No Real Orders. Do NOT auto-apply weights. Production Trading: BLOCKED.")


def cmd_open_cockpit(args: argparse.Namespace) -> None:
    """Open the TW Quant Cockpit GUI (alias for cockpit) (v0.3.21)."""
    # Delegate to the existing cockpit command handler
    cmd_cockpit(args)


# ---------------------------------------------------------------------------
# v0.3.22 — Usability QA & Error Message Polish
# ---------------------------------------------------------------------------

def cmd_usability_smoke_test(args: argparse.Namespace) -> None:
    """Run usability smoke tests (v0.3.22)."""
    from utils.cli_output import CLIOutput
    out = CLIOutput()
    out.header("Usability Smoke Test", version="v0.3.22")
    out.safety_banner()
    out.flush()

    try:
        from qa.usability_smoke_test import UsabilitySmokeTest
        test = UsabilitySmokeTest()
        result = test.run()
    except Exception as exc:
        from utils.cli_output import CLIOutput as _CO
        _o = _CO()
        _o.error(f"Smoke test failed: {exc}")
        _o.flush()
        return

    out2 = CLIOutput()
    out2.section("Summary")
    out2.key_value("Overall Status",         result.get("overall_status", "UNKNOWN"))
    out2.key_value("Tests Passed",           result.get("passed",   0))
    out2.key_value("Tests Failed",           result.get("failed",   0))
    out2.key_value("Warnings",               result.get("warnings", 0))
    out2.key_value("Skipped",                result.get("skipped",  0))
    out2.key_value("Safety Banner Coverage", result.get("safety_banner_coverage", 0))
    out2.blank()

    cases = result.get("cases", [])
    if cases:
        out2.section("Test Results")
        for c in cases:
            status = c.get("status", "")
            dur    = f"{c.get('duration_seconds', 0):.1f}s"
            note   = c.get("message", "")[:60]
            out2.status_line(c.get("name", ""), status, detail=f"{dur}  {note}")

    out2.footer()
    out2.flush()

    # Generate report if requested
    if getattr(args, "report", False):
        try:
            from reports.usability_qa_report import UsabilityQAReportBuilder
            path = UsabilityQAReportBuilder(smoke_result=result).build()
            print(f"  Report: {path}")
        except Exception as exc:
            print(f"  Report generation failed: {exc}")


def cmd_usability_qa_report(args: argparse.Namespace) -> None:
    """Generate usability QA Markdown report from latest smoke test results (v0.3.22)."""
    from utils.cli_output import CLIOutput
    out = CLIOutput()
    out.header("Usability QA Report", version="v0.3.22")
    out.flush()

    try:
        from gui.usability_qa_adapter import UsabilityQAAdapter
        adapter = UsabilityQAAdapter()

        # Try to load latest summary first
        summary = adapter.load_latest_summary()
        if summary:
            smoke_result = {
                "cases":    summary.get("rows", []),
                "passed":   summary.get("passed",   0),
                "failed":   summary.get("failed",   0),
                "warnings": summary.get("warnings", 0),
                "skipped":  0,
                "overall_status": "PASS" if summary.get("failed", 0) == 0 else "FAIL",
                "safety_banner_coverage": 0,
            }
        else:
            smoke_result = {}

        path = adapter.generate_report(smoke_result)
        print(f"  Report: {path}")

    except Exception as exc:
        print(f"  ERROR: {exc}")

    out2 = CLIOutput()
    out2.footer()
    out2.flush()


# ---------------------------------------------------------------------------
# v0.3.24 — Provider Reliability & Fallback Matrix CLI
# ---------------------------------------------------------------------------

def _print_provider_reliability_header() -> None:
    print()
    print("=" * 62)
    print("  TW Quant Cockpit — Provider Reliability  (v0.3.24)")
    print("=" * 62)
    print()
    print("  [!] Read Only")
    print("  [!] No Real Orders")
    print("  [!] Production Trading: BLOCKED")
    print("  [!] Mock Fallback: DISABLED")
    print()


def cmd_provider_reliability(args: argparse.Namespace) -> None:
    """Provider Reliability & Fallback Matrix (v0.3.24)."""
    import os
    _print_provider_reliability_header()

    mode        = getattr(args, "mode", "real")
    report_flag = getattr(args, "report", False)
    refresh     = getattr(args, "refresh", False)
    dataset_f   = getattr(args, "dataset", None)
    provider_f  = getattr(args, "provider", None)
    results_dir = getattr(args, "results_dir", "data/backtest_results")
    report_dir  = getattr(args, "report_dir", "reports")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_results = os.path.join(base_dir, results_dir)
    abs_reports = os.path.join(base_dir, report_dir)

    print(f"  Mode             : {mode.upper()}")
    print(f"  Read Only        : Yes")
    print(f"  No Real Orders   : Yes")
    print(f"  Production Trading: BLOCKED")
    print()

    try:
        from data.providers.reliability_matrix import ProviderReliabilityMatrix
        matrix = ProviderReliabilityMatrix(
            results_dir=abs_results,
            report_dir=abs_reports,
            mode=mode,
        )
        result = matrix.run()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    summary = result.get("reliability_summary", {})

    print(f"  Providers       : {summary.get('providers_checked', '?')}")
    print(f"  Datasets        : {summary.get('datasets_covered', '?')}")
    print(f"  Overall reliability: {summary.get('overall_reliability_score', 'N/A')}")
    print(f"  Weak datasets   : {summary.get('weak_datasets', [])}")
    print(f"  Fallback used   : {summary.get('local_fallback_count', 0)} local")
    print(f"  Mock fallback   : {summary.get('mock_fallback_count', 0)}  [DISABLED]")
    print()

    # Dataset filter
    if dataset_f:
        print(f"  Dataset filter: {dataset_f}")
        rows = [r for r in result.get("dataset_matrix", []) if r["dataset"] == dataset_f]
        for row in rows:
            print(f"    primary: {row['primary_provider']}")
            print(f"    fallback_1: {row['fallback_1']}")
            print(f"    fallback_2: {row['fallback_2']}")
            print(f"    local_fallback: {row['local_fallback']}")
            print(f"    confidence: {row['confidence_score']:.1f} ({row['confidence_level']})")
            print(f"    mock_fallback: disabled")
        print()

    # Provider filter
    if provider_f:
        print(f"  Provider filter: {provider_f}")
        providers = [p for p in result.get("provider_summary", []) if p["provider_name"] == provider_f]
        for p in providers:
            sr  = f"{p['success_rate']:.0%}" if isinstance(p.get("success_rate"), float) else "N/A"
            rel = f"{p['reliability_score']:.1f}" if isinstance(p.get("reliability_score"), float) else "N/A"
            print(f"    status: {p['status']}")
            print(f"    success_rate: {sr}")
            print(f"    reliability_score: {rel}")
            print(f"    recommended_usage: {p.get('recommended_usage', '')}")
        print()

    # Dataset confidence scores summary
    print("  Dataset Confidence Scores:")
    for ds, v in result.get("dataset_confidence_scores", {}).items():
        print(f"    {ds:<20} {v.get('score', 0):>5.1f}  {v.get('level', 'UNKNOWN')}")
    print()

    # Report
    if report_flag:
        try:
            from reports.provider_reliability_report import ProviderReliabilityReportBuilder
            from datetime import datetime as _dt
            builder = ProviderReliabilityReportBuilder(
                report_date=_dt.now().strftime("%Y-%m-%d"),
                matrix_data=result,
            )
            rpt_path = builder.build(output_dir=abs_reports)
            print(f"  Report: {rpt_path}")
        except Exception as exc:
            print(f"  Report ERROR: {exc}")
        print()

    warnings = result.get("warnings", [])
    if warnings:
        print("  Warnings:")
        for w in warnings:
            print(f"    - {w}")
        print()

    print("  [!] Read Only. No Real Orders. Production BLOCKED. Mock Fallback: DISABLED.")


# ---------------------------------------------------------------------------
# v0.3.26 — Hardened Backtest CLI
# ---------------------------------------------------------------------------

def _print_hardened_backtest_header() -> None:
    print()
    print("=" * 62)
    print("  TW Quant Cockpit — Hardened Backtest  (v0.3.26)")
    print("  [!] Research / Backtest Only. No Real Orders.")
    print("  [!] Production Trading: BLOCKED.")
    print("  [!] Not Investment Advice.")
    print("=" * 62)
    print()


def cmd_hardened_backtest(args: argparse.Namespace) -> None:
    """Hardened Backtest Engine (v0.3.26)."""
    import os
    _print_hardened_backtest_header()

    mode            = getattr(args, "mode", "real")
    entry_model     = getattr(args, "entry_model", "next_open")
    exit_model      = getattr(args, "exit_model", "combined")
    cost_model_name = getattr(args, "cost_model", "taiwan_realistic")
    split_method    = getattr(args, "split_method", "walk_forward")
    max_holding     = getattr(args, "max_holding_days", 20)
    no_liquidity    = getattr(args, "no_liquidity_filter", False)
    no_gap          = getattr(args, "no_gap_risk", False)
    zero_cost       = getattr(args, "zero_cost", False)
    report_flag     = getattr(args, "report", False)
    results_dir     = getattr(args, "results_dir", "data/backtest_results")
    report_dir      = getattr(args, "report_dir", "reports")

    base_dir    = os.path.dirname(os.path.abspath(__file__))
    abs_results = os.path.join(base_dir, results_dir)
    abs_reports = os.path.join(base_dir, report_dir)

    if zero_cost:
        cost_model_name = "zero"

    print(f"  Mode             : {mode.upper()}")
    print(f"  Entry model      : {entry_model}")
    print(f"  Exit model       : {exit_model}")
    print(f"  Cost model       : {'zero' if zero_cost else cost_model_name}")
    print(f"  Split method     : {split_method}")
    print(f"  Max holding days : {max_holding}")
    print(f"  Liquidity filter : {'disabled' if no_liquidity else 'enabled'}")
    print(f"  Gap risk         : {'disabled' if no_gap else 'enabled'}")
    print(f"  Read Only        : Yes")
    print(f"  No Real Orders   : Yes")
    print(f"  Production       : BLOCKED")
    print()

    try:
        from backtest.hardened_backtester import HardenedBacktester
        bt = HardenedBacktester(
            mode=mode,
            entry_model=entry_model,
            exit_model=exit_model,
            cost_model=cost_model_name,
            split_method=split_method,
            max_holding_days=max_holding,
            use_liquidity_filter=not no_liquidity,
            use_gap_risk=not no_gap,
            results_dir=abs_results,
            report_dir=abs_reports,
            zero_cost=zero_cost,
        )
        result = bt.run()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return

    status = result.get("status", "UNKNOWN")
    print(f"  Status           : {status}")
    if status == "INSUFFICIENT_DATA":
        print("  Insufficient data — import CSV data or run: python main.py provider-auto-fetch")
        print()
    else:
        print(f"  Trade count      : {result.get('trade_count', 0)}")
        print(f"  Net return       : {result.get('net_return', 'N/A')}")
        print(f"  Sharpe           : {result.get('sharpe', 'N/A')}")
        print(f"  Max Drawdown     : {result.get('max_drawdown', 'N/A')}")
        print(f"  Profit Factor    : {result.get('profit_factor', 'N/A')}")
        print(f"  Win Rate         : {result.get('win_rate', 'N/A')}")
        print(f"  Confidence Grade : {result.get('confidence_grade', 'D')}")
        print()
        trades_path = result.get("trades_path")
        if trades_path:
            print(f"  Trades CSV       : {trades_path}")
        metrics_path = result.get("metrics_path")
        if metrics_path:
            print(f"  Metrics CSV      : {metrics_path}")
        warnings = result.get("warnings", [])
        if warnings:
            print()
            print("  Warnings:")
            for w in warnings:
                print(f"    - {w}")

    # Report
    if report_flag:
        try:
            from reports.hardened_backtest_report import HardenedBacktestReportBuilder
            from datetime import datetime as _dt
            builder = HardenedBacktestReportBuilder(
                report_date=_dt.now().strftime("%Y-%m-%d"),
                backtest_result=result,
                mode=mode,
            )
            rpt_path = builder.build(output_dir=abs_reports)
            print()
            print(f"  Report           : {rpt_path}")
        except Exception as exc:
            print(f"  Report ERROR     : {exc}")

    print()
    print("  [!] Research / Backtest Only. No Real Orders. Production BLOCKED.")
    print("  [!] Confidence grade A does not authorize live trading.")


# ---------------------------------------------------------------------------
# v0.3.25 — Universe Expansion & Sector Classification CLI
# ---------------------------------------------------------------------------

def _print_universe_header(title: str = "Universe Manager") -> None:
    print()
    print("=" * 62)
    print(f"  TW Quant Cockpit — {title}  (v0.3.25)")
    print("  [!] Research Only. Read Only. No Real Orders.")
    print("  [!] Not Investment Advice.")
    print("=" * 62)
    print()


def cmd_universe_list(args: argparse.Namespace) -> None:
    """List all available universe groups (v0.3.25)."""
    _print_universe_header("Universe List")
    try:
        from universe.universe_registry import UniverseRegistry
        reg = UniverseRegistry()
        universes = reg.list_universes()   # returns list of dicts
        print(f"  Available universe groups ({len(universes)}):")
        for u in universes:
            name   = u.get("name", "?")
            size   = u.get("symbol_count", 0)
            exists = "OK" if u.get("exists") else "not built"
            print(f"    {name:<35} size={size:<5} [{exists}]")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  Run 'python main.py universe-build-defaults' to create universe CSV files.")
    print("  [!] Read Only. Research Universe Only.")


def cmd_universe_build_defaults(args: argparse.Namespace) -> None:
    """Build default universe CSV files from seed data (v0.3.25)."""
    _print_universe_header("Build Default Universes")
    force = getattr(args, "force", False)
    try:
        from universe.universe_registry import UniverseRegistry
        reg = UniverseRegistry()
        # Returns {name: path, ...} for created files, plus "manifest" key
        result = reg.build_default_universes(force=force)
        if "error" in result:
            print(f"  ERROR: {result['error']}")
        else:
            manifest_path = result.pop("manifest", "")
            built = list(result.keys())
            print(f"  Built   : {len(built)} universe(s)")
            for name in built:
                print(f"    + {name}")
            if not built:
                print("  All files already exist. Use --force to rebuild.")
            if manifest_path:
                print(f"  Manifest: {manifest_path}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Read Only. Research Universe Only.")


def cmd_universe_show(args: argparse.Namespace) -> None:
    """Show symbols and sector summary for a universe group (v0.3.25)."""
    universe_name = getattr(args, "universe", "core_30")
    _print_universe_header(f"Universe Show: {universe_name}")
    try:
        from universe.universe_registry import UniverseRegistry
        from universe.sector_classifier import SectorClassifier
        reg = UniverseRegistry()
        rows = reg.load_universe(universe_name)   # list of dicts
        if not rows:
            print(f"  Universe '{universe_name}' not found or empty.")
            print("  Run: python main.py universe-build-defaults")
            return
        symbols = [str(r.get("symbol", "")) for r in rows if r.get("symbol")]
        print(f"  Universe : {universe_name}")
        print(f"  Symbols  : {len(symbols)}")
        print()
        clf = SectorClassifier()
        enriched = clf.classify_universe(rows)
        sector_result = clf.get_sector_summary(enriched)
        by_sector = sector_result.get("by_sector", {})
        print("  Sector breakdown:")
        for sector, count in sorted(by_sector.items(), key=lambda x: -x[1]):
            print(f"    {sector:<35} {count}")
        print()
        print(f"  Symbols: {', '.join(symbols[:20])}{'...' if len(symbols) > 20 else ''}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Read Only. Research Universe Only.")


def cmd_universe_quality_score(args: argparse.Namespace) -> None:
    """Compute Universe Quality Score for a universe group (v0.3.25)."""
    universe_name = getattr(args, "universe", "core_30")
    _print_universe_header(f"Universe Quality Score: {universe_name}")
    try:
        from universe.universe_registry import UniverseRegistry
        from universe.universe_quality import UniverseQualityAnalyzer
        reg = UniverseRegistry()
        symbols = reg.get_symbols(universe_name)
        if not symbols:
            print(f"  Universe '{universe_name}' not found or empty.")
            print("  Run: python main.py universe-build-defaults")
            return
        analyzer = UniverseQualityAnalyzer(universe_name=universe_name)
        result = analyzer.run()
        score = result.get("overall_universe_score") or result.get("overall_score") or 0
        level = result.get("readiness_level", "UNKNOWN")
        print(f"  Universe       : {universe_name}")
        print(f"  Symbol count   : {len(symbols)}")
        try:
            print(f"  Quality score  : {float(score):.1f} / 100")
        except (TypeError, ValueError):
            print(f"  Quality score  : {score} / 100")
        print(f"  Readiness      : {level}")
        print()
        _COMPONENT_KEYS = [
            "coverage_score", "freshness_score", "provider_reliability_score",
            "sector_balance_score", "liquidity_readiness_score",
            "backtest_sample_readiness_score",
        ]
        comp_found = False
        for key in _COMPONENT_KEYS:
            val = result.get(key)
            if val is not None:
                comp_found = True
                try:
                    print(f"    {key:<40} {float(val):.1f}")
                except (TypeError, ValueError):
                    print(f"    {key:<40} {val}")
        if comp_found:
            print()
        caveats = result.get("caveats", result.get("warnings", []))
        if caveats:
            print("  Caveats:")
            for c in caveats:
                print(f"    - {c}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Read Only. Research Universe Only.")


def cmd_universe_expand(args: argparse.Namespace) -> None:
    """Propose expansion candidates (read-only, no auto-write) (v0.3.25)."""
    from_universe = getattr(args, "from_universe", "core_30")
    target_size   = getattr(args, "target_size", 50)
    _print_universe_header(f"Universe Expand: {from_universe} → {target_size}")
    try:
        from universe.universe_expander import UniverseExpander
        expander = UniverseExpander(source_universe=from_universe, target_size=target_size)
        result = expander.propose_expansion()
        current = result.get("source_symbols", [])
        candidates = result.get("candidates", [])
        print(f"  From universe  : {from_universe} ({len(current)} symbols)")
        print(f"  Target size    : {target_size}")
        print(f"  New candidates : {len(candidates)}")
        print()
        if candidates:
            print("  Proposed additions (ranked by score):")
            for i, c in enumerate(candidates[:20], 1):
                sym  = c.get("symbol", "?")
                name = c.get("name", "")
                score = c.get("expansion_score", 0)
                sector = c.get("sector", "")
                print(f"    {i:>2}. {sym:<8} {name:<20} score={score:.2f}  {sector}")
        warnings = result.get("warnings", [])
        if warnings:
            print()
            print("  Warnings:")
            for w in warnings:
                print(f"    - {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Proposals only. No files written. Manual review required.")
    print("  [!] Read Only. Research Universe Only.")


def cmd_universe_report(args: argparse.Namespace) -> None:
    """Generate Universe Expansion Markdown report (v0.3.25)."""
    universe_name = getattr(args, "universe", "core_30")
    mode          = getattr(args, "mode", "real")
    report_dir    = getattr(args, "report_dir", "reports")
    _print_universe_header(f"Universe Report: {universe_name}")
    import os
    base_dir    = os.path.dirname(os.path.abspath(__file__))
    abs_reports = os.path.join(base_dir, report_dir)
    try:
        from universe.universe_registry import UniverseRegistry
        from universe.universe_quality import UniverseQualityAnalyzer
        from universe.sector_classifier import SectorClassifier
        from universe.universe_expander import UniverseExpander
        from reports.universe_expansion_report import UniverseExpansionReportBuilder
        from datetime import datetime as _dt
        reg = UniverseRegistry()
        rows = reg.load_universe(universe_name)
        if not rows:
            print(f"  Universe '{universe_name}' not found or empty.")
            print("  Run: python main.py universe-build-defaults")
            return
        # Quality analysis
        analyzer = UniverseQualityAnalyzer(universe_name=universe_name)
        quality_result = analyzer.run()
        # Registry listing
        registry_data = reg.list_universes()
        # Sector classification
        clf = SectorClassifier()
        enriched = clf.classify_universe(rows)
        classifier_data = clf.get_sector_summary(enriched)
        # Expansion proposals
        expander = UniverseExpander(source_universe=universe_name, target_size=len(rows) + 20)
        expansion_data = expander.propose_expansion()
        builder = UniverseExpansionReportBuilder(
            report_date=_dt.now().strftime("%Y-%m-%d"),
            universe_data=quality_result,
            registry_data=registry_data,
            expansion_data=expansion_data,
            classifier_data=classifier_data,
            mode=mode,
        )
        rpt_path = builder.build(output_dir=abs_reports)
        print(f"  Report: {rpt_path}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Read Only. Research Universe Only.")


# ---------------------------------------------------------------------------
# v0.3.28 — Strategy Rule Governance Command
# ---------------------------------------------------------------------------

def cmd_rule_governance(args: argparse.Namespace) -> None:
    """Run strategy rule governance analysis."""
    mode       = getattr(args, "mode",        "real")
    category   = getattr(args, "category",    None)
    status_flt = getattr(args, "status",      None)
    report     = getattr(args, "report",      False)
    snapshot   = getattr(args, "snapshot",    False)
    results_dir = getattr(args, "results_dir", "data/backtest_results")
    report_dir  = getattr(args, "report_dir",  "reports")

    print()
    print("=" * 60)
    print("  TW Quant Cockpit v0.3.28 — Strategy Rule Governance")
    print("=" * 60)
    print(f"  Mode         : {mode}")
    print("  Research Only: True")
    print("  No Real Orders: True")
    print()

    try:
        from gui.rule_governance_adapter import RuleGovernanceAdapter
        adapter = RuleGovernanceAdapter(results_dir=results_dir, report_dir=report_dir)
        result  = adapter.run_governance(mode=mode)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    reg_summary = result.get("registry_summary", {})
    conf_result = result.get("confidence_result", {})
    cycles      = result.get("dependency_cycles", [])

    print(f"  Total rules  : {reg_summary.get('total_rules', 0)}")
    print(f"  Active       : {reg_summary.get('active_count', 0)}")
    print(f"  Experimental : {reg_summary.get('experimental_count', 0)}")
    print(f"  Needs review : {reg_summary.get('needs_review_count', 0)}")
    print(f"  High conf.   : {len(conf_result.get('high_confidence', []))}")
    print(f"  Unknown conf.: {len(conf_result.get('unknown_confidence', []))}")
    print(f"  Dep. warnings: {len(cycles)}")

    if category or status_flt:
        # Load registry for filtered rule listing (status filter is case-insensitive)
        try:
            from governance.rule_registry import RuleRegistry
            _reg = RuleRegistry()
            _reg.load_builtin_rules()
            rules = _reg.list_rules(
                category=category,
                status=status_flt.upper() if status_flt else None,
            )
        except Exception:
            rules = []
        print()
        lbl = f"category={category}" if category else f"status={status_flt}"
        print(f"  Filtered ({lbl}): {len(rules)} rules")
        for r in rules[:20]:
            rid  = r.rule_id  if hasattr(r, "rule_id")  else r.get("rule_id", "?")
            st   = r.status   if hasattr(r, "status")   else r.get("status", "?")
            conf = r.confidence_level if hasattr(r, "confidence_level") else r.get("confidence_level", "?")
            exp  = " [EXPERIMENTAL]" if (r.experimental if hasattr(r, "experimental") else r.get("experimental")) else ""
            print(f"    {rid}  status={st}  conf={conf}{exp}")
        if len(rules) > 20:
            print(f"    ... and {len(rules) - 20} more")

    print()

    if report:
        try:
            path = adapter.generate_report(mode=mode)
            print(f"  Report: {path}")
        except Exception as exc:
            print(f"  [WARN] Report failed: {exc}")

    if snapshot:
        try:
            snap = adapter.export_snapshot()
            snap_path = snap.get("snapshot_path") or snap.get("error", "unknown")
            print(f"  Snapshot: {snap_path}")
        except Exception as exc:
            print(f"  [WARN] Snapshot failed: {exc}")

    print()
    print("  [!] No auto weight apply. No real orders. Research Only.")
    print()


# ---------------------------------------------------------------------------
# v0.4.0 — Release Stabilization Commands
# ---------------------------------------------------------------------------

def _print_release_header() -> None:
    print()
    print("=" * 60)
    print("  TW Quant Cockpit — v0.4.0 Research Platform Stable Release")
    print("=" * 60)
    print("  [!] Research Only. No Real Orders. Production BLOCKED.")
    print()


def cmd_version_info(args: argparse.Namespace) -> None:
    """Print version info."""
    _print_release_header()
    try:
        from release.version_info import get_version_info, get_safety_banner
        info = get_version_info()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    print(f"  Version      : {info.get('version', '?')}")
    print(f"  Release      : {info.get('release_name', '?')}")
    print(f"  Stage        : {info.get('release_stage', '?')}")
    print(f"  Read Only    : {info.get('read_only', '?')}")
    print(f"  No Real Orders: {info.get('no_real_orders', '?')}")
    print(f"  Prod BLOCKED : {info.get('production_blocked', '?')}")
    print(f"  Real Order Ready: {info.get('real_order_ready', '?')}")
    print(f"  Modes        : {info.get('supported_modes', [])}")
    print()
    print(f"  Safety Banner: {get_safety_banner()}")
    print()
    features = info.get("major_features", [])
    print(f"  Features ({len(features)}):")
    for f in features:
        print(f"    • {f}")
    print()


def cmd_stable_release_check(args: argparse.Namespace) -> None:
    """Run stable release checklist."""
    _print_release_header()
    mode = getattr(args, "mode", "real")

    try:
        from release.stable_release_checklist import StableReleaseChecklist
        checker = StableReleaseChecklist(mode=mode)
        result  = checker.run()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    status = result.get("status", "?")
    passed = result.get("passed", 0)
    failed = result.get("failed", 0)
    warned = result.get("warnings", 0)

    print(f"  Overall Status : {status}")
    print(f"  Passed         : {passed}")
    print(f"  Failed         : {failed}")
    print(f"  Warnings       : {warned}")
    print()

    items = result.get("items", [])
    for item in items:
        st  = item.get("status", "?")
        nm  = item.get("name", "?")
        det = item.get("detail", "")[:60]
        marker = "✓" if st == "PASS" else ("⚠" if st == "WARN" else ("✗" if st == "FAIL" else "—"))
        print(f"  [{marker}] {nm:<35}  {st:<6}  {det}")

    print()
    if result.get("report_path"):
        print(f"  Report   : {result['report_path']}")
    if result.get("summary_csv_path"):
        print(f"  CSV      : {result['summary_csv_path']}")
    print()
    print("  [!] No real orders. Research Only.")
    print()


def cmd_regression_suite(args: argparse.Namespace) -> None:
    """Run regression suite."""
    _print_release_header()
    mode  = getattr(args, "mode",  "real")
    quick = not getattr(args, "full", False)

    suite_name = "quick" if quick else "full"
    print(f"  Suite: {suite_name}")
    print()

    try:
        from release.regression_suite import RegressionSuite
        suite  = RegressionSuite(mode=mode, quick=quick)
        result = suite.run_quick() if quick else suite.run_full()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    status = result.get("status", "?")
    passed = result.get("passed", 0)
    failed = result.get("failed", 0)
    warned = result.get("warned", 0)

    print(f"  Overall Status : {status}")
    print(f"  Passed         : {passed}")
    print(f"  Failed         : {failed}")
    print(f"  Warnings       : {warned}")
    print()

    tests = result.get("tests", [])
    for t in tests:
        st  = t.get("status", "?")
        nm  = t.get("name", "?")
        ms  = t.get("duration_ms", 0)
        marker = "✓" if st == "PASS" else ("⚠" if st == "WARN" else ("✗" if st == "FAIL" else "—"))
        print(f"  [{marker}] {nm:<38}  {st:<6}  {ms:.0f}ms")

    print()
    print("  [!] No real orders. Research Only.")
    print()


def cmd_stable_release_report(args: argparse.Namespace) -> None:
    """Generate stable release report."""
    _print_release_header()
    mode = getattr(args, "mode", "real")

    try:
        from reports.stable_release_report import StableReleaseReportBuilder
        builder = StableReleaseReportBuilder(mode=mode)
        path    = builder.build()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    print(f"  Report: {path}")
    print()
    print("  [!] No real orders. Research Only.")
    print()


# ---------------------------------------------------------------------------
# v0.3.29 — Research Notebook / Experiment Registry Commands
# ---------------------------------------------------------------------------

def _print_experiment_header() -> None:
    print()
    print("=" * 60)
    print("  TW Quant Cockpit v0.3.29 — Experiment Registry")
    print("=" * 60)
    print("  [!] Research Only. Backtest Only. No Real Orders.")
    print()


def cmd_experiment_create(args: argparse.Namespace) -> None:
    """Create a new experiment entry."""
    _print_experiment_header()
    name     = getattr(args, "name",    None)
    exp_type = getattr(args, "type",    "daily_research")
    mode     = getattr(args, "mode",    "real")
    profile  = getattr(args, "profile", "standard")
    tags_str = getattr(args, "tags",    None)
    notes    = getattr(args, "notes",   None)
    tags     = [t.strip() for t in tags_str.split(",")] if tags_str else []

    try:
        from experiments.experiment_registry import ExperimentRegistry
        registry = ExperimentRegistry()
        source_cmd = f"experiment-create --name \"{name}\" --type {exp_type} --mode {mode} --profile {profile}"
        meta = registry.create_experiment(
            name=name, experiment_type=exp_type, mode=mode,
            profile=profile, tags=tags, notes=notes,
            source_command=source_cmd,
        )
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    print(f"  Experiment ID  : {meta.experiment_id}")
    print(f"  Name           : {meta.experiment_name}")
    print(f"  Type           : {meta.experiment_type}")
    print(f"  Mode           : {meta.mode}")
    print(f"  Profile        : {meta.profile}")
    print(f"  Status         : {meta.status}")
    print(f"  Created At     : {meta.created_at}")
    print(f"  Git Commit     : {meta.git_commit or '—'}")
    print()
    print("  [!] No real orders. Research Only.")
    print()


def cmd_experiment_register_latest(args: argparse.Namespace) -> None:
    """Register the latest research run as an experiment."""
    _print_experiment_header()
    mode = getattr(args, "mode", "real")

    try:
        from experiments.experiment_registry import ExperimentRegistry
        registry = ExperimentRegistry()
        meta = registry.register_existing_run(source_command=f"experiment-register-latest --mode {mode}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    if meta is None:
        print("  No experiments found to register.")
    else:
        print(f"  Registered     : {meta.experiment_id}")
        print(f"  Status         : {meta.status}")
    print()
    print("  [!] No real orders. Research Only.")
    print()


def cmd_experiment_list(args: argparse.Namespace) -> None:
    """List experiments."""
    _print_experiment_header()
    status_flt = getattr(args, "status", None)
    type_flt   = getattr(args, "type",   None)
    limit      = getattr(args, "limit",  20)

    try:
        from experiments.experiment_registry import ExperimentRegistry
        registry = ExperimentRegistry()
        experiments = registry.list_experiments(limit=limit, status=status_flt, experiment_type=type_flt)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    if not experiments:
        print("  No experiments found.")
    else:
        print(f"  {'ID':<36}  {'Name':<24}  {'Type':<20}  {'Status':<12}  {'Created At':<20}")
        print(f"  {'-'*36}  {'-'*24}  {'-'*20}  {'-'*12}  {'-'*20}")
        for e in experiments:
            eid   = e.get("experiment_id", "")[:36]
            ename = e.get("experiment_name", "")[:24]
            etype = e.get("experiment_type", "")[:20]
            estat = e.get("status", "")[:12]
            edate = e.get("created_at", "")[:20]
            print(f"  {eid:<36}  {ename:<24}  {etype:<20}  {estat:<12}  {edate:<20}")
    print()


def cmd_experiment_show(args: argparse.Namespace) -> None:
    """Show experiment detail."""
    _print_experiment_header()
    exp_id = getattr(args, "id", None)

    if not exp_id:
        print("  ERROR: --id is required")
        sys.exit(1)

    try:
        from experiments.experiment_registry import ExperimentRegistry
        registry = ExperimentRegistry()
        meta = registry.get_experiment(registry._resolve_id(exp_id))
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    if meta is None:
        print(f"  Experiment not found: {exp_id}")
    else:
        print(f"  Experiment ID  : {meta.experiment_id}")
        print(f"  Name           : {meta.experiment_name}")
        print(f"  Type           : {meta.experiment_type}")
        print(f"  Mode           : {meta.mode}")
        print(f"  Profile        : {meta.profile}")
        print(f"  Status         : {meta.status}")
        print(f"  Created At     : {meta.created_at}")
        print(f"  Git Commit     : {meta.git_commit or '—'}")
        print(f"  Git Tag        : {meta.git_tag or '—'}")
        print(f"  Universe       : {meta.universe_name or '—'}")
        print(f"  Notes          : {meta.notes or '—'}")
        print(f"  Snapshots      : {list(meta.snapshots.keys()) or '(none)'}")
        print(f"  Reports        : {len(meta.reports)}")
        print(f"  Source Command : {meta.source_command or '—'}")
    print()


def cmd_experiment_notebook(args: argparse.Namespace) -> None:
    """Build experiment notebook.md."""
    _print_experiment_header()
    exp_id = getattr(args, "id", None)

    if not exp_id:
        print("  ERROR: --id is required")
        sys.exit(1)

    try:
        from experiments.experiment_registry import ExperimentRegistry
        from experiments.experiment_notebook import ExperimentNotebookBuilder
        registry = ExperimentRegistry()
        resolved = registry._resolve_id(exp_id)
        builder  = ExperimentNotebookBuilder()
        path     = builder.build_notebook(resolved)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    print(f"  Notebook: {path}")
    print()
    print("  [!] No real orders. Research Only.")
    print()


def cmd_experiment_compare(args: argparse.Namespace) -> None:
    """Compare two or more experiments."""
    _print_experiment_header()
    ids_str = getattr(args, "ids", None)

    if not ids_str:
        print("  ERROR: --ids is required (comma-separated list, e.g. EXP-aaa,EXP-bbb)")
        sys.exit(1)

    exp_ids = [i.strip() for i in ids_str.split(",") if i.strip()]
    if len(exp_ids) < 2:
        # Allow single id for self-compare (smoke test)
        if len(exp_ids) == 1:
            exp_ids = [exp_ids[0], exp_ids[0]]
        else:
            print("  ERROR: Need at least 2 experiment IDs")
            sys.exit(1)

    try:
        from experiments.experiment_comparator import ExperimentComparator
        comparator = ExperimentComparator()
        result = comparator.compare(exp_ids)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    pairs = result.get("pairs", [])
    for pair in pairs:
        print(f"  Left  : {pair.get('left_id', '?')}")
        print(f"  Right : {pair.get('right_id', '?')}")
        print(f"  Overall Direction: {pair.get('overall_direction', '?')}")
        print(f"  Recommendation: {pair.get('recommendation', '?')}")
        scores = pair.get("scores", {})
        for metric, info in scores.items():
            if isinstance(info, dict):
                direction = info.get("direction", "?")
                left_v  = info.get("left_value")
                right_v = info.get("right_value")
                print(f"    {metric}: {left_v} → {right_v}  [{direction}]")
        print()
    print("  [!] IMPROVED does not imply readiness for real trading. No real orders.")
    print()


def cmd_experiment_report(args: argparse.Namespace) -> None:
    """Generate Experiment Registry report."""
    _print_experiment_header()

    try:
        from reports.experiment_registry_report import ExperimentRegistryReportBuilder
        builder = ExperimentRegistryReportBuilder()
        path    = builder.build()
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    print(f"  Report: {path}")
    print()
    print("  [!] No real orders. Research Only.")
    print()


def cmd_experiment_snapshot(args: argparse.Namespace) -> None:
    """Build all snapshots for an experiment."""
    _print_experiment_header()
    exp_id = getattr(args, "id", None)

    if not exp_id:
        print("  ERROR: --id is required (use 'latest' for most recent)")
        sys.exit(1)

    try:
        from experiments.experiment_registry import ExperimentRegistry
        from gui.experiment_registry_adapter import ExperimentRegistryAdapter
        _reg     = ExperimentRegistry()
        exp_id_r = _reg._resolve_id(exp_id)
        adapter  = ExperimentRegistryAdapter()
        result   = adapter.build_snapshots(exp_id_r)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    print(f"  Experiment ID  : {result.get('experiment_id', exp_id)}")
    print(f"  Status         : {result.get('status', '?')}")
    print(f"  Snapshots saved: {result.get('saved_count', 0)}")
    snaps = result.get("snapshots", {})
    for stype, snap in snaps.items():
        gen_at = snap.get("generated_at", "?")[:19] if isinstance(snap, dict) else "?"
        print(f"    {stype}: {gen_at}")
    if result.get("error"):
        print(f"  [WARN] {result['error']}")
    print()
    print("  [!] No real orders. Research Only.")
    print()


# ---------------------------------------------------------------------------
# v0.3.27 — Intraday / Tick Data Pipeline Commands
# ---------------------------------------------------------------------------

def _print_intraday_header() -> None:
    print()
    print("=" * 60)
    print("  TW Quant Cockpit v0.3.27 — Intraday / Tick Pipeline")
    print("=" * 60)
    print("  [!] Read Only. Intraday Research Only. No Real Orders.")
    print()


def cmd_intraday_pipeline(args: argparse.Namespace) -> None:
    """Run intraday data standardization pipeline."""
    _print_intraday_header()

    mode     = getattr(args, "mode",    "real")
    freq     = getattr(args, "freq",    "1min")
    dry_run  = getattr(args, "dry_run", False)
    report   = getattr(args, "report",  False)
    rep_dir  = getattr(args, "report_dir", "reports")

    if dry_run:
        print("  [DRY-RUN] No files will be written.")

    try:
        from intraday.intraday_pipeline import IntradayDataPipeline
        pipeline = IntradayDataPipeline(mode=mode, freq=freq, dry_run=dry_run)
        result = pipeline.run()
    except Exception as exc:
        print(f"  ERROR: cannot run IntradayDataPipeline: {exc}")
        sys.exit(1)

    n_ok   = result.get("files_ok",     0)
    n_skip = result.get("files_skipped", 0)
    n_err  = result.get("files_error",  0)
    symbols = result.get("symbols", [])
    warns  = result.get("warnings", [])

    print(f"  Freq        : {freq}")
    print(f"  Files OK    : {n_ok}")
    print(f"  Skipped     : {n_skip}")
    print(f"  Errors      : {n_err}")
    print(f"  Symbols     : {', '.join(symbols[:10])}{'...' if len(symbols) > 10 else ''}")
    for w in warns[:5]:
        print(f"  [WARN] {w}")
    print()

    if report and not dry_run:
        try:
            from intraday.intraday_quality import IntradayQualityChecker
            from reports.intraday_pipeline_report import IntradayPipelineReportBuilder
            import datetime as _dt
            quality_result = IntradayQualityChecker().run()
            builder = IntradayPipelineReportBuilder(
                report_date=_dt.datetime.now().strftime("%Y-%m-%d"),
                quality_result=quality_result,
                mode=mode,
            )
            rpt_path = builder.build(output_dir=rep_dir)
            print(f"  Report: {rpt_path}")
        except Exception as exc:
            print(f"  [WARN] Could not generate report: {exc}")

    print("  Done. Run 'python main.py intraday-quality' to check quality.")
    print()


def cmd_intraday_quality(args: argparse.Namespace) -> None:
    """Check intraday data quality for standardized files."""
    _print_intraday_header()

    freq    = getattr(args, "freq", None)  # None = all freqs

    try:
        from intraday.intraday_quality import IntradayQualityChecker
        checker = IntradayQualityChecker()
        result  = checker.run()
    except Exception as exc:
        print(f"  ERROR: cannot run IntradayQualityChecker: {exc}")
        sys.exit(1)

    status  = result.get("status", "NO_DATA")
    symbols = result.get("symbols", [])
    overall = result.get("overall_quality_score", 0.0)
    warns   = result.get("warnings", [])
    results_list = result.get("results", [])

    print(f"  Status              : {status}")
    print(f"  Symbols found       : {len(symbols)}")
    print(f"  Overall quality     : {overall:.1f}/100")
    print()

    # Filter by freq if specified
    if freq:
        results_list = [r for r in results_list if r.get("freq") == freq]

    for r in results_list[:15]:
        sym    = r.get("symbol", "?")
        f      = r.get("freq",   "?")
        q      = r.get("quality_score", 0.0)
        st     = r.get("status", "?")
        n_rows = r.get("rows", 0)
        print(f"  {sym} [{f}]: score={q:.0f}  status={st}  rows={n_rows}")

    if len(results_list) > 15:
        print(f"  ... and {len(results_list) - 15} more")

    for w in warns[:5]:
        print(f"  [WARN] {w}")

    print()
    print("  Tick/bidask API: planned for v0.4+ — not a failure.")
    print()


def cmd_intraday_features(args: argparse.Namespace) -> None:
    """Preview intraday features (opening range, VWAP, fake breakout) for a stock."""
    _print_intraday_header()

    symbol = getattr(args, "stock", None)
    freq   = getattr(args, "freq", "1min")

    if not symbol:
        print("  ERROR: --stock SYMBOL required")
        sys.exit(1)

    print(f"  Symbol : {symbol}   Freq: {freq}")
    print()

    try:
        from data.intraday_data_importer import IntradayDataImporter
        importer = IntradayDataImporter()
        df = importer.load_intraday_standard(symbol, freq=freq)
        if df is None or df.empty:
            df = importer.load_intraday(symbol, freq=freq)
    except Exception as exc:
        print(f"  ERROR: cannot load intraday data: {exc}")
        sys.exit(1)

    if df is None or df.empty:
        print(f"  No intraday data found for {symbol} at freq={freq}.")
        print("  Run: python main.py intraday-pipeline  (or import-intraday)")
        print()
        return

    last_date = df["date"].max() if "date" in df.columns else "?"
    print(f"  Last date    : {last_date}")
    print(f"  Total bars   : {len(df)}")
    print()

    # Get most recent day
    if "date" in df.columns:
        last_df = df[df["date"] == last_date]
    else:
        last_df = df.tail(270)  # ~1 trading session of 1min bars

    # Opening Range
    try:
        from intraday.opening_range_features import OpeningRangeFeatureBuilder
        or_res = OpeningRangeFeatureBuilder().build(last_df)
        print("  Opening Range Features:")
        print(f"    return_5m   : {or_res.get('opening_return_5m')}")
        print(f"    return_15m  : {or_res.get('opening_return_15m')}")
        print(f"    high_break  : {or_res.get('opening_high_break')}")
        print(f"    low_break   : {or_res.get('opening_low_break')}")
        print(f"    strength    : {or_res.get('opening_strength_score')}")
        print()
    except Exception as exc:
        print(f"  Opening range: unavailable ({exc})")

    # VWAP
    try:
        from intraday.vwap_features import VWAPFeatureBuilder
        vwap_res = VWAPFeatureBuilder().build(last_df)
        print("  VWAP Features:")
        print(f"    intraday_vwap    : {vwap_res.get('intraday_vwap')}")
        print(f"    price_vs_vwap_%  : {vwap_res.get('price_vs_vwap_pct')}")
        print(f"    vwap_support_score: {vwap_res.get('vwap_support_score')}")
        print()
    except Exception as exc:
        print(f"  VWAP: unavailable ({exc})")

    # Fake Breakout
    try:
        from intraday.fake_breakout_detector import FakeBreakoutDetector
        fb_res = FakeBreakoutDetector().detect(last_df)
        print("  Fake Breakout Detection:")
        print(f"    fake_breakout_risk   : {fb_res.get('fake_breakout_risk')}")
        print(f"    fake_breakout_score  : {fb_res.get('fake_breakout_score')}")
        print(f"    chase_risk_score     : {fb_res.get('chase_risk_score')}")
        print(f"    breakout_quality     : {fb_res.get('breakout_quality')}")
        print()
    except Exception as exc:
        print(f"  Fake breakout: unavailable ({exc})")

    print("  Tick/bidask: planned for v0.4+")
    print()


# ---------------------------------------------------------------------------
# v0.3.9 — Public Data API & Crawler Commands
# ---------------------------------------------------------------------------

def cmd_fetch_public_data(args: argparse.Namespace) -> None:
    """Fetch public data (monthly revenue, fundamentals, institutional, margin)."""
    logger_cmd = logging.getLogger("main.fetch_public_data")

    symbol = getattr(args, "stock", None)
    universe_size = getattr(args, "universe", None)
    manifest_path = getattr(args, "manifest", None)
    months = getattr(args, "months", 24)
    source = getattr(args, "source", "auto")
    dry_run = getattr(args, "dry_run", False)
    replace = getattr(args, "replace", False)

    print()
    print("=" * 60)
    print("  TW Quant Cockpit v0.3.9 — Fetch Public Data")
    print("=" * 60)
    if dry_run:
        print("  [DRY-RUN] No files will be written.")
    print()

    # Resolve symbol list
    symbols = []
    if symbol:
        symbols = [symbol]
    elif universe_size:
        try:
            from data.universe_manifest import UniverseManifest
            um = UniverseManifest()
            df_mf = um.load()
            if df_mf is not None and not df_mf.empty:
                symbols = df_mf["symbol"].tolist()[:universe_size]
            else:
                from data.universe_manifest import _UNIVERSE_10
                symbols = [s["symbol"] for s in _UNIVERSE_10[:universe_size]]
        except Exception as exc:
            logger_cmd.warning("Cannot load universe manifest: %s", exc)
            symbols = []
    elif manifest_path:
        try:
            import pandas as _pd
            df_mf = _pd.read_csv(manifest_path)
            symbols = df_mf["symbol"].tolist() if "symbol" in df_mf.columns else []
        except Exception as exc:
            logger_cmd.warning("Cannot read manifest %s: %s", manifest_path, exc)

    if not symbols:
        print("  ERROR: specify --stock SYMBOL, --universe N, or --manifest PATH")
        sys.exit(1)

    print(f"  Symbols  : {', '.join(symbols)}")
    print(f"  Source   : {source}")
    print(f"  Months   : {months}")
    print()

    try:
        from data.fundamental_data_builder import FundamentalDataBuilder
        builder = FundamentalDataBuilder(replace=replace, dry_run=dry_run)
    except Exception as exc:
        print(f"  ERROR: cannot init FundamentalDataBuilder: {exc}")
        sys.exit(1)

    all_results = []
    failed_sources = []
    for sym in symbols:
        print(f"  [{sym}] Fetching...")
        try:
            result = builder.fetch_and_build(sym, months=months, source=source)
            all_results.append(result)
            warns = result.get("warnings", [])
            rev = result.get("monthly_revenue")
            fin = result.get("fundamental")
            inst = result.get("institutional")
            margin = result.get("margin")
            print(f"         monthly_revenue: {'OK (' + str(rev.get('rows_added', 0)) + ' rows)' if rev else 'unavailable'}")
            print(f"         fundamental    : {'OK (' + str(fin.get('rows_added', 0)) + ' rows)' if fin else 'unavailable'}")
            print(f"         institutional  : {'OK (' + str(inst.get('rows_added', 0)) + ' rows)' if inst else 'unavailable'}")
            print(f"         margin_short   : {'OK (' + str(margin.get('rows_added', 0)) + ' rows)' if margin else 'unavailable'}")
            for w in warns:
                print(f"         [WARN] {w}")
                if "error" in w.lower() or "failed" in w.lower():
                    failed_sources.append(w)
        except Exception as exc:
            logger_cmd.error("fetch_and_build(%s): %s", sym, exc)
            all_results.append({"symbol": sym, "warnings": [str(exc)]})
            failed_sources.append(f"{sym}: {exc}")

    # Generate report
    if not dry_run and all_results:
        try:
            from reports.data_fetch_report import DataFetchReport
            rpt = DataFetchReport()
            rpt_path = rpt.generate(
                fetch_results=all_results,
                failed_sources=failed_sources,
            )
            print()
            print(f"  Report: {rpt_path}")
        except Exception as exc:
            logger_cmd.warning("Cannot generate fetch report: %s", exc)

    print()
    print("  Done. Run 'python main.py data-check --stock SYMBOL' to verify.")
    print()


def cmd_import_intraday(args: argparse.Namespace) -> None:
    """Import intraday 1min / 5min data from XQ exports."""
    logger_cmd = logging.getLogger("main.import_intraday")

    folder = getattr(args, "folder", None)
    file_path = getattr(args, "file", None)
    symbol = getattr(args, "symbol", None)
    freq = getattr(args, "freq", "1min")
    dry_run = getattr(args, "dry_run", False)
    replace = getattr(args, "replace", False)

    print()
    print("=" * 60)
    print("  TW Quant Cockpit v0.3.9 — Import Intraday Data")
    print("=" * 60)
    if dry_run:
        print("  [DRY-RUN] No files will be written.")
    print()

    try:
        from data.intraday_data_importer import IntradayDataImporter
        importer = IntradayDataImporter(dry_run=dry_run, replace=replace)
    except Exception as exc:
        print(f"  ERROR: cannot init IntradayDataImporter: {exc}")
        sys.exit(1)

    if file_path:
        if not symbol:
            from data.intraday_data_importer import _infer_symbol_from_path
            symbol = _infer_symbol_from_path(file_path)
        print(f"  File : {file_path}")
        print(f"  Sym  : {symbol}   Freq: {freq}")
        print()
        result = importer.import_file(file_path, symbol=symbol, freq=freq)
        rows = result.get("rows_imported", 0)
        warns = result.get("warnings", [])
        print(f"  Rows imported : {rows}")
        for w in warns:
            print(f"  [WARN] {w}")
    elif folder:
        print(f"  Folder : {folder}   Freq: {freq}")
        print()
        results = importer.import_folder(folder, freq=freq)
        total = 0
        for r in results:
            sym = r.get("symbol", "?")
            rows = r.get("rows_imported", 0)
            warns = r.get("warnings", [])
            total += rows
            status = "OK" if not warns else f"WARN: {warns[0]}"
            print(f"  {sym}: {rows} bars — {status}")
        print()
        print(f"  Total bars imported: {total}")
    else:
        print("  ERROR: specify --folder FOLDER or --file FILE")
        sys.exit(1)

    # Show current status
    status = importer.status()
    print()
    print(f"  Intraday 1min files: {status.get('intraday_1min_files', 0)}")
    print(f"  Intraday 5min files: {status.get('intraday_5min_files', 0)}")
    print()


def cmd_data_source_status(args: argparse.Namespace) -> None:  # noqa: ARG001
    """Show comprehensive data source status including public API and intraday."""
    print()
    print("=" * 60)
    print("  TW Quant Cockpit v0.3.9 — Data Source Status")
    print("=" * 60)
    print()

    # 1. XQ daily CSV
    try:
        from data.providers.csv_provider import CSVProvider
        csv_p = CSVProvider()
        csv_ok = csv_p.health_check().get("ok", False)
        print(f"  XQ daily CSV          : {'[OK]' if csv_ok else '[PARTIAL]'}")
    except Exception as exc:
        print(f"  XQ daily CSV          : [ERROR] {exc}")

    # 2. Public monthly revenue
    try:
        import os
        rev_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "data", "import", "monthly_revenue", "monthly_revenue.csv")
        rev_ok = os.path.isfile(rev_path)
        print(f"  Public monthly revenue: {'[OK]' if rev_ok else '[NOT IMPORTED]'}")
    except Exception:
        print("  Public monthly revenue: [UNKNOWN]")

    # 3. Public fundamental
    try:
        import os
        fin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "data", "import", "fundamental", "fundamental.csv")
        fin_ok = os.path.isfile(fin_path)
        print(f"  Public fundamental    : {'[OK]' if fin_ok else '[NOT IMPORTED]'}")
    except Exception:
        print("  Public fundamental    : [UNKNOWN]")

    # 4. Institutional detail
    try:
        import os
        inst_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "data", "import", "institutional", "institutional.csv")
        inst_ok = os.path.isfile(inst_path)
        print(f"  Institutional detail  : {'[OK]' if inst_ok else '[NOT IMPORTED]'}")
    except Exception:
        print("  Institutional detail  : [UNKNOWN]")

    # 5. Margin short
    try:
        import os
        margin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "data", "import", "margin", "margin.csv")
        margin_ok = os.path.isfile(margin_path)
        print(f"  Margin short          : {'[OK]' if margin_ok else '[NOT IMPORTED]'}")
    except Exception:
        print("  Margin short          : [UNKNOWN]")

    # 6. Intraday 1min
    try:
        from data.intraday_data_importer import IntradayDataImporter
        importer = IntradayDataImporter()
        status = importer.status()
        n1 = status.get("intraday_1min_files", 0)
        print(f"  Intraday 1min         : {'[OK] ' + str(n1) + ' files' if n1 > 0 else '[NOT IMPORTED]'}")
    except Exception as exc:
        print(f"  Intraday 1min         : [ERROR] {exc}")

    # 7. Intraday 5min
    try:
        n5 = status.get("intraday_5min_files", 0)
        print(f"  Intraday 5min         : {'[OK] ' + str(n5) + ' files' if n5 > 0 else '[NOT IMPORTED]'}")
    except Exception:
        print("  Intraday 5min         : [UNKNOWN]")

    # 8. Tick provider
    print("  Tick provider         : [PLANNED] NOT CONFIGURED")

    # 9. BidAsk provider
    print("  BidAsk provider       : [PLANNED] NOT CONFIGURED")

    # 10. Public data provider health
    print()
    print("  Public Data API Providers:")
    try:
        from data.providers.public_data_provider import PublicDataProvider
        pdp = PublicDataProvider()
        health = pdp.health_check()
        for src_name, src_status in health.get("sources", {}).items():
            src_ok = src_status.get("ok", False)
            note = src_status.get("note", "")[:50]
            marker = "[OK]  " if src_ok else "[WARN]"
            print(f"    {marker} {src_name:<12} — {note}")
    except Exception as exc:
        print(f"    [ERROR] Cannot check public providers: {exc}")

    print()
    print("  Mega provider         : [PLANNED] not configured")
    print("  Real order execution  : DISABLED")
    print()
    print("  Hints:")
    print("    python main.py fetch-public-data --stock 2454 --months 24")
    print("    python main.py import-intraday --folder D:\\XQ\\twqc_bundle\\intraday --freq 1min")
    print()


def cmd_enrich_universe_data(args: argparse.Namespace) -> None:
    """Batch-fetch public data for all universe symbols and update quality."""
    logger_cmd = logging.getLogger("main.enrich_universe_data")

    universe_size = getattr(args, "universe", None)
    manifest_path = getattr(args, "manifest", None)
    months = getattr(args, "months", 24)
    dry_run = getattr(args, "dry_run", False)

    print()
    print("=" * 60)
    print("  TW Quant Cockpit v0.3.9 — Enrich Universe Data")
    print("=" * 60)
    if dry_run:
        print("  [DRY-RUN] No files will be written.")
    print()

    # Resolve symbols from universe manifest
    symbols = []
    if manifest_path:
        try:
            import pandas as _pd
            df_mf = _pd.read_csv(manifest_path)
            symbols = df_mf["symbol"].tolist() if "symbol" in df_mf.columns else []
        except Exception as exc:
            logger_cmd.warning("Cannot read manifest %s: %s", manifest_path, exc)
    elif universe_size:
        try:
            from data.universe_manifest import UniverseManifest
            um = UniverseManifest()
            df_mf = um.load()
            if df_mf is not None and not df_mf.empty:
                symbols = df_mf["symbol"].tolist()[:universe_size]
        except Exception as exc:
            logger_cmd.warning("Cannot load universe manifest: %s", exc)

    if not symbols:
        # Fall back to universe_10 default
        try:
            from data.universe_manifest import _UNIVERSE_10
            symbols = [s["symbol"] for s in _UNIVERSE_10]
            logger_cmd.info("Using default 10-stock universe")
        except Exception:
            print("  ERROR: no symbols found — build manifest first:")
            print("    python main.py build-universe-manifest --size 10")
            sys.exit(1)

    print(f"  Symbols ({len(symbols)}): {', '.join(symbols[:5])}{'...' if len(symbols) > 5 else ''}")
    print(f"  Months  : {months}")
    print()

    try:
        from data.fundamental_data_builder import FundamentalDataBuilder
        builder = FundamentalDataBuilder(dry_run=dry_run)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    all_results = []
    before_ready = {}
    after_ready = {}

    for sym in symbols:
        print(f"  [{sym}] Fetching public data...")
        try:
            result = builder.fetch_and_build(sym, months=months)
            all_results.append(result)
            warns = result.get("warnings", [])
            for w in warns:
                print(f"         [WARN] {w}")
        except Exception as exc:
            logger_cmd.error("enrich %s: %s", sym, exc)
            all_results.append({"symbol": sym, "warnings": [str(exc)]})

    # Re-run universe quality
    if not dry_run:
        print()
        print("  Updating universe quality...")
        try:
            from data.universe_quality_checker import UniverseQualityChecker
            uqc = UniverseQualityChecker()
            df_q = uqc.check_universe()
            if df_q is not None and not df_q.empty:
                summary = uqc.summarize_universe_quality(df_q)
                conf = summary.get("statistical_confidence", "UNKNOWN")
                short_ready = summary.get("short_term_ready_count", 0)
                mid_ready = summary.get("mid_term_ready_count", 0)
                print(f"  Statistical confidence : {conf}")
                print(f"  Short-term ready       : {short_ready}/{len(df_q)}")
                print(f"  Mid-term ready         : {mid_ready}/{len(df_q)}")
        except Exception as exc:
            logger_cmd.warning("Universe quality update failed: %s", exc)

    # Generate report
    if not dry_run and all_results:
        try:
            from reports.data_fetch_report import DataFetchReport
            rpt = DataFetchReport()
            rpt_path = rpt.generate(fetch_results=all_results)
            print()
            print(f"  Report: {rpt_path}")
        except Exception as exc:
            logger_cmd.warning("Cannot generate fetch report: %s", exc)

    print()
    print("  Done. Run 'python main.py universe-quality --report' to see updated quality.")
    print()


# ---------------------------------------------------------------------------
# TW Quant Cockpit v0.4.0 command handlers
# ---------------------------------------------------------------------------

def cmd_version_info(args: argparse.Namespace) -> None:
    """Print version info for TW Quant Cockpit v0.4.0."""
    try:
        from release.version_info import print_version_info, get_safety_banner
        print_version_info()
        print()
        print(get_safety_banner())
    except Exception as exc:
        print(f"  TW Quant Cockpit v0.4.0 — Research Only | No Real Orders | Production BLOCKED")
        print(f"  (version_info import error: {exc})")


def cmd_stable_release_check(args: argparse.Namespace) -> None:
    """Run stable release checklist (v0.4.0)."""
    import os
    mode        = getattr(args, "mode", "real")
    results_dir = getattr(args, "results_dir", "data/backtest_results")
    report_dir  = getattr(args, "report_dir",  "reports")

    _base = os.path.dirname(os.path.abspath(__file__))
    abs_results = os.path.join(_base, results_dir)
    abs_reports = os.path.join(_base, report_dir)

    print("=" * 60)
    print("  TW Quant Cockpit v0.4.0 — Stable Release Checklist")
    print("  [!] Research Only | No Real Orders | Production BLOCKED")
    print("=" * 60)

    try:
        from release.stable_release_checklist import StableReleaseChecklist
        checklist = StableReleaseChecklist(
            mode=mode,
            results_dir=os.path.relpath(abs_results, _base),
            report_dir=os.path.relpath(abs_reports, _base),
        )
        result = checklist.run()
    except Exception as exc:
        print(f"  ERROR running checklist: {exc}")
        return

    print(f"\n  Status  : {result['status']}")
    print(f"  Version : {result['version']}")
    print(f"  Mode    : {result['mode']}")
    print(f"  Passed  : {result['passed']}")
    print(f"  Failed  : {result['failed']}")
    print(f"  Warnings: {result['warnings']}")
    print()
    print(f"  {'#':<3} {'Name':<35} {'Status':<8} {'ms':>7}  Detail")
    print(f"  {'-'*3} {'-'*35} {'-'*8} {'-'*7}  {'-'*40}")
    for i, item in enumerate(result.get("items", []), 1):
        detail = str(item.get("detail", ""))[:60]
        print(
            f"  {i:<3} {item['name']:<35} {item['status']:<8} "
            f"{item['duration_ms']:>7.1f}  {detail}"
        )
    print()
    if result.get("summary_csv_path"):
        print(f"  CSV  : {result['summary_csv_path']}")
    if result.get("report_path"):
        print(f"  Report: {result['report_path']}")
    print(f"\n  Overall: {result['status']}")


def cmd_regression_suite(args: argparse.Namespace) -> None:
    """Run regression suite for v0.4.0."""
    import os
    mode        = getattr(args, "mode", "real")
    quick       = not getattr(args, "full", False)
    results_dir = getattr(args, "results_dir", "data/backtest_results")

    _base = os.path.dirname(os.path.abspath(__file__))
    abs_results = os.path.join(_base, results_dir)

    suite_label = "Quick" if quick else "Full"
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.0 — Regression Suite ({suite_label})")
    print("  [!] Research Only | No Real Orders | Production BLOCKED")
    print("=" * 60)

    try:
        from release.regression_suite import RegressionSuite
        suite = RegressionSuite(
            mode=mode,
            quick=quick,
            results_dir=os.path.relpath(abs_results, _base),
        )
        result = suite.run()
    except Exception as exc:
        print(f"  ERROR running regression suite: {exc}")
        return

    print(f"\n  Status  : {result['status']}")
    print(f"  Suite   : {result['suite']}")
    print(f"  Mode    : {result['mode']}")
    print(f"  Passed  : {result['passed']}")
    print(f"  Failed  : {result['failed']}")
    print(f"  Warned  : {result['warned']}")
    print()
    print(f"  {'#':<3} {'Name':<40} {'Status':<8} {'ms':>7}  Detail")
    print(f"  {'-'*3} {'-'*40} {'-'*8} {'-'*7}  {'-'*40}")
    for i, test in enumerate(result.get("tests", []), 1):
        detail = str(test.get("detail", ""))[:60]
        print(
            f"  {i:<3} {test['name']:<40} {test['status']:<8} "
            f"{test['duration_ms']:>7.1f}  {detail}"
        )
    print(f"\n  Overall: {result['status']}")


def cmd_stable_release_report(args: argparse.Namespace) -> None:
    """Generate stable release report for v0.4.0."""
    import os
    mode        = getattr(args, "mode", "real")
    report_dir  = getattr(args, "report_dir",  "reports")
    results_dir = getattr(args, "results_dir", "data/backtest_results")

    _base = os.path.dirname(os.path.abspath(__file__))
    abs_reports = os.path.join(_base, report_dir)
    abs_results = os.path.join(_base, results_dir)

    print("=" * 60)
    print("  TW Quant Cockpit v0.4.0 — Stable Release Report")
    print("  [!] Research Only | No Real Orders | Production BLOCKED")
    print("=" * 60)

    try:
        from reports.stable_release_report import StableReleaseReportBuilder
        builder = StableReleaseReportBuilder(
            report_dir=os.path.relpath(abs_reports, _base),
            results_dir=os.path.relpath(abs_results, _base),
            mode=mode,
        )
        path = builder.build()
        print(f"\n  Report saved: {path}")
        print(f"  Status: OK")
    except Exception as exc:
        print(f"  ERROR generating report: {exc}")


# ---------------------------------------------------------------------------
# v0.4.1 API Fetch Productionization CLI
# ---------------------------------------------------------------------------

def cmd_api_token_check(args: argparse.Namespace) -> None:
    """Check FinMind / API token configuration (read-only, never modifies .env)."""
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.1 — API Token Check")
    print("  [!] Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from data.providers.token_setup_assistant import TokenSetupAssistant
        assistant = TokenSetupAssistant()
        result = assistant.inspect()
        req = result.get("required_tokens", {})
        for name, info in req.items():
            configured = info.get("configured", False)
            masked = info.get("masked_value", "(not set)")
            status = "OK" if configured else "MISSING"
            print(f"  {name}: {status}  {masked}")
        safety = result.get("env_safety", {})
        print(f"  .env safe: {safety.get('safe', '—')}")
        issues = safety.get("issues", [])
        for issue in issues:
            print(f"  [!] {issue}")
        if result.get("all_required_configured"):
            print("\n  All required tokens configured.")
        else:
            print("\n  [!] Some required tokens are missing. See docs/api_fetch_productionization.md")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. Read Only.")


def cmd_api_cache_status(args: argparse.Namespace) -> None:
    """Show API cache statistics."""
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.1 — API Cache Status")
    print("  [!] Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from data.providers.api_cache import APICache
        stats = APICache().stats()
        print(f"  Enabled:        {stats.get('enabled', '—')}")
        print(f"  Cache root:     {stats.get('cache_root', '—')}")
        print(f"  Total entries:  {stats.get('total_entries', 0)}")
        print(f"  Active:         {stats.get('active', 0)}")
        print(f"  Expired:        {stats.get('expired', 0)}")
        print(f"  Hits / Misses:  {stats.get('hits', 0)} / {stats.get('misses', 0)}")
        print(f"  Hit rate:       {stats.get('hit_rate', 0):.1%}")
        print(f"  Size:           {stats.get('size_bytes', 0):,} bytes")
        print(f"  No token in keys: True")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. Read Only.")


def cmd_api_fetch_diagnostics(args: argparse.Namespace) -> None:
    """Run API fetch diagnostics — provider health and cache status."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.1 — API Fetch Diagnostics")
    print(f"  Mode: {mode}")
    print("  [!] Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from gui.api_fetch_status_adapter import APIFetchStatusAdapter
        result = APIFetchStatusAdapter().run_diagnostics(mode=mode)
        health = result.get("provider_health", {})
        providers = health.get("providers", [])
        if providers:
            print(f"\n  Providers ({len(providers)}):")
            for p in providers:
                status = p.get("status", "?")
                name = p.get("provider_name", "?")
                msg = p.get("message", "")[:60]
                print(f"    [{status:8s}] {name}  {msg}")
        cache_stats = result.get("cache_stats", {})
        if cache_stats:
            print(f"\n  Cache: enabled={cache_stats.get('enabled','—')} "
                  f"hits={cache_stats.get('hits',0)} misses={cache_stats.get('misses',0)} "
                  f"entries={cache_stats.get('total_entries',0)}")
        warnings = result.get("warnings", [])
        for w in warnings:
            print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. Read Only.")


def cmd_api_cache_cleanup(args: argparse.Namespace) -> None:
    """Remove expired API cache entries."""
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.1 — API Cache Cleanup")
    print("  [!] Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from data.providers.api_cache import APICache
        cache = APICache()
        removed = cache.cleanup_expired()
        print(f"  Removed {removed} expired cache entries.")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. Read Only.")


def cmd_api_fetch_production_report(args: argparse.Namespace) -> None:
    """Generate API fetch production report."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.1 — API Fetch Production Report")
    print(f"  Mode: {mode}")
    print("  [!] Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from gui.api_fetch_status_adapter import APIFetchStatusAdapter
        result = APIFetchStatusAdapter().generate_report(mode=mode)
        if result.get("ok"):
            print(f"  Report saved: {result.get('report_path')}")
        else:
            print(f"  ERROR: {result.get('error')}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. Read Only.")


# ---------------------------------------------------------------------------
# v0.4.3 Model Monitoring command handlers
# ---------------------------------------------------------------------------

def cmd_model_monitoring(args: argparse.Namespace) -> None:
    """Run Model Monitoring summary."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Model Monitoring (mode={mode})")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("  [!] No Live Prediction.")
    print("=" * 60)
    try:
        from monitoring.monitoring_summary import ModelMonitoringSummary
        result = ModelMonitoringSummary().run()
        print(f"  Mode:              {mode}")
        print(f"  Research Only:     {result.get('research_only', True)}")
        print(f"  Monitoring Only:   {result.get('monitoring_only', True)}")
        print(f"  No Live Predict:   True")
        print(f"  No Real Orders:    {result.get('no_real_orders', True)}")
        print(f"  Model count:       {result.get('model_count', 0)}")
        print(f"  Prediction count:  {result.get('prediction_count', 0)}")
        print(f"  Reviewed:          {result.get('reviewed_count', 0)}")
        hr = result.get('hit_rate')
        print(f"  Hit rate:          {f'{hr:.2%}' if isinstance(hr, float) else '—'}")
        print(f"  Drift:             {result.get('drift_status', '—')}")
        print(f"  Degradation:       {result.get('degradation_status', '—')}")
        print(f"  Rule vs ML:        {result.get('rule_vs_ml_status', '—')}")
        for w in result.get("warnings", [])[:5]:
            print(f"  [!] {w}")
        actions = result.get("next_actions", [])
        if actions:
            print()
            print("  Next actions:")
            for a in actions[:5]:
                print(f"    - {a}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Monitoring Only. No real orders. Not investment advice.")


def cmd_model_monitoring_report(args: argparse.Namespace) -> None:
    """Generate Model Monitoring report."""
    mode       = getattr(args, "mode", "real")
    report_dir = getattr(args, "report_dir", None)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Model Monitoring Report (mode={mode})")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        kwargs = {}
        if report_dir:
            kwargs["report_dir"] = report_dir
        from gui.model_monitoring_adapter import ModelMonitoringAdapter
        result = ModelMonitoringAdapter(**kwargs).generate_report(mode=mode)
        if result.get("ok"):
            print(f"  Report saved: {result.get('report_path')}")
        else:
            print(f"  ERROR: {result.get('error')}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Report NOT committed. Monitoring Only. No real orders.")


def cmd_model_registry_list(args: argparse.Namespace) -> None:
    """List registered ML model metadata."""
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.3 — Model Registry")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from monitoring.model_registry import ModelRegistry
        registry = ModelRegistry()
        models = registry.list_models()
        summary = registry.summary()
        print(f"  Total models:  {summary.get('total', 0)}")
        if models:
            print()
            print(f"  {'Model ID':<30} {'Name':<25} {'Type':<12} {'Status'}")
            print(f"  {'-'*80}")
            for m in models[:20]:
                print(f"  {m.get('model_id','')[:29]:<30} {m.get('model_name','')[:24]:<25} "
                      f"{m.get('model_type',''):<12} {m.get('monitoring_status','')}")
        else:
            print("  No models registered. Use: python main.py model-register --name ... --type ...")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Monitoring Only. No real orders.")


def cmd_model_register(args: argparse.Namespace) -> None:
    """Register a new ML model metadata entry."""
    name   = getattr(args, "name", "unnamed_model")
    mtype  = getattr(args, "type", "baseline")
    target = getattr(args, "target", "label_direction_5d")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Register Model Metadata")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from monitoring.model_registry import ModelRegistry, ModelMetadata
        from datetime import datetime
        import uuid
        model_id = f"MDL-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:6].upper()}"
        metadata = ModelMetadata(
            model_id=model_id,
            model_name=name,
            model_type=mtype,
            version="v1",
            created_at=datetime.now().isoformat(),
            target_label=target,
            training_status="RESEARCH_ONLY",
            monitoring_status="ACTIVE",
        )
        registry = ModelRegistry()
        result = registry.register_model(metadata)
        if result.get("ok"):
            print(f"  Registered: {model_id}")
            print(f"  Name:       {name}")
            print(f"  Type:       {mtype}")
            print(f"  Target:     {target}")
        else:
            print(f"  ERROR: {result.get('error')}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Metadata only. No model trained. No real orders.")


def cmd_prediction_log(args: argparse.Namespace) -> None:
    """Show prediction log summary."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Prediction Log (mode={mode})")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from monitoring.prediction_log import PredictionLog
        log = PredictionLog()
        summary = log.summarize()
        total = summary.get("total_predictions", 0)
        print(f"  Total predictions: {total}")
        if total == 0:
            print("  No prediction logs found.")
            print("  Prediction logs are appended by research workflows.")
        else:
            print(f"  Reviewed:          {summary.get('reviewed_count', 0)}")
            print(f"  Date range:        {summary.get('date_range', ('—', '—'))}")
            sources = summary.get("sources", {})
            if sources:
                print()
                print("  By source:")
                for src, cnt in sources.items():
                    print(f"    {src:<30} {cnt}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Prediction logs are research records only. Not investment advice.")


def cmd_prediction_review(args: argparse.Namespace) -> None:
    """Review prediction hit / miss results."""
    mode    = getattr(args, "mode", "real")
    horizon = getattr(args, "horizon", 5)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Prediction Review (horizon={horizon}d, mode={mode})")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from monitoring.hit_miss_review import HitMissReviewer
        result = HitMissReviewer().run(horizon=horizon)
        status = result.get("status", "—")
        print(f"  Status:            {status}")
        print(f"  Total predictions: {result.get('total_predictions', 0)}")
        print(f"  Reviewed:          {result.get('reviewed_predictions', 0)}")
        hr = result.get("hit_rate")
        print(f"  Hit rate:          {f'{hr:.2%}' if isinstance(hr, float) else '—'}")
        avg_ret = result.get("avg_actual_return")
        print(f"  Avg actual return: {f'{avg_ret:.4f}' if isinstance(avg_ret, float) else '—'}")
        print(f"  Precision:         {result.get('precision', '—')}")
        print(f"  Recall:            {result.get('recall', '—')}")
        for w in result.get("warnings", [])[:5]:
            print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Hit rate is not guaranteed win rate. Monitoring Only. No real orders.")


def cmd_drift_check(args: argparse.Namespace) -> None:
    """Run feature / prediction drift check."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Drift Check (mode={mode})")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from gui.model_monitoring_adapter import ModelMonitoringAdapter
        result = ModelMonitoringAdapter().run_drift_check()
        if not result.get("ok"):
            print(f"  ERROR: {result.get('error')}")
        else:
            r = result.get("drift_result", {})
            print(f"  Drift status:   {r.get('status', '—')}")
            feat = r.get("feature_drift", {})
            if feat:
                print(f"  Feature drift findings: {len(feat)}")
            miss = r.get("missing_drift", {})
            if miss:
                drifted = [k for k, v in miss.items() if isinstance(v, dict) and v.get("change", 0) > 0.05]
                if drifted:
                    print(f"  Missing ratio drifted:  {', '.join(drifted[:5])}")
            for w in r.get("warnings", [])[:5]:
                print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Drift warning is not a trading signal. Monitoring Only. No real orders.")


def cmd_signal_degradation(args: argparse.Namespace) -> None:
    """Run signal degradation check."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Signal Degradation (mode={mode})")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from monitoring.signal_degradation import SignalDegradationMonitor
        result = SignalDegradationMonitor().run()
        print(f"  Status:           {result.get('status', '—')}")
        rule = result.get("rule_degradation", {})
        if rule:
            print(f"  Rule degradation: {rule.get('status', '—')}")
        sq = result.get("signal_quality_degradation", {})
        if sq:
            print(f"  Signal quality:   {sq.get('status', '—')}")
        port = result.get("portfolio_degradation", {})
        if port:
            print(f"  Portfolio:        {port.get('status', '—')}")
        for w in result.get("warnings", [])[:5]:
            print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Degradation warning is not a trading signal. Monitoring Only. No real orders.")


def cmd_rule_vs_ml(args: argparse.Namespace) -> None:
    """Run rule vs ML comparison."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.3 — Rule vs ML Comparison (mode={mode})")
    print("  [!] Monitoring Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from monitoring.rule_vs_ml_comparator import RuleVsMLComparator
        result = RuleVsMLComparator().compare()
        print(f"  ML available:      {result.get('ml_available', False)}")
        if not result.get("ml_available", False):
            print("  ML predictions: ML_NOT_AVAILABLE (no predictions logged yet)")
        else:
            ar = result.get("agreement_rate")
            print(f"  Agreement rate:    {f'{ar:.2%}' if isinstance(ar, float) else '—'}")
            print(f"  Rule-only hits:    {result.get('rule_only_hits', 0)}")
            print(f"  ML-only hits:      {result.get('ml_only_hits', 0)}")
            print(f"  Both hits:         {result.get('both_hits', 0)}")
            print(f"  Both misses:       {result.get('both_misses', 0)}")
            print(f"  Recommendation:    {result.get('recommendation', '—')}")
        for w in result.get("warnings", [])[:3]:
            print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Disagreement does not auto-change strategy. Monitoring Only. No real orders.")


# ---------------------------------------------------------------------------
# v0.4.2 ML Feature Store command handlers
# ---------------------------------------------------------------------------

def cmd_ml_feature_catalog(args: argparse.Namespace) -> None:
    """List all ML feature definitions from the feature catalog."""
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.2 — ML Feature Catalog")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from ml.feature_catalog import FeatureCatalog
        catalog = FeatureCatalog()
        features = catalog.list_features()
        summary  = catalog.summary()
        print(f"  Total features: {summary.get('total_features', 0)}")
        print(f"  Enabled:        {summary.get('enabled_features', 0)}")
        print(f"  Experimental:   {summary.get('experimental_features', 0)}")
        print(f"  High leakage:   {summary.get('high_leakage_risk', 0)}")
        print()
        cats = summary.get("categories", {})
        if cats:
            print("  Categories:")
            for cat, count in sorted(cats.items()):
                print(f"    {cat:<20} {count}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. ML Research Only.")


def cmd_ml_feature_snapshot(args: argparse.Namespace) -> None:
    """Build ML feature snapshot from research data."""
    mode       = getattr(args, "mode", "real")
    symbols    = getattr(args, "symbols", None)
    start_date = getattr(args, "start_date", None)
    end_date   = getattr(args, "end_date", None)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.2 — ML Feature Snapshot (mode={mode})")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from ml.feature_snapshot import FeatureSnapshotBuilder
        builder = FeatureSnapshotBuilder(mode=mode)
        df, summary = builder.build(symbols=symbols, start_date=start_date, end_date=end_date)
        print(f"  Status:        {summary.get('status', '—')}")
        print(f"  Features:      {summary.get('feature_count', 0)}")
        print(f"  Rows:          {summary.get('row_count', 0)}")
        print(f"  Symbols:       {summary.get('symbol_count', 0)}")
        print(f"  Date range:    {summary.get('date_range', ('—', '—'))}")
        if summary.get("output_path"):
            print(f"  Output:        {summary['output_path']}")
        for w in summary.get("warnings", []):
            print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. ML Research Only.")


def cmd_ml_labels(args: argparse.Namespace) -> None:
    """Generate ML labels from feature snapshot data."""
    mode     = getattr(args, "mode", "real")
    horizons = getattr(args, "horizons", None)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.2 — ML Label Generation (mode={mode})")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from ml.feature_snapshot import FeatureSnapshotBuilder
        from ml.label_generator import LabelGenerator
        snap_builder = FeatureSnapshotBuilder(mode=mode)
        df, snap_summary = snap_builder.build()
        if df is None or (hasattr(df, "empty") and df.empty):
            print("  No feature snapshot data found. Run ml-feature-snapshot first.")
        else:
            h = list(map(int, horizons.split(","))) if horizons else [1, 5, 10, 20]
            gen = LabelGenerator(horizons=h)
            labeled_df, label_summary = gen.generate(df)
            print(f"  Horizons:      {label_summary.get('horizons', h)}")
            print(f"  Label columns: {label_summary.get('label_count', 0)}")
            print(f"  Rows:          {label_summary.get('row_count', 0)}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Label columns prefix: label_ or fwd_. No real orders. ML Research Only.")


def cmd_ml_build_dataset(args: argparse.Namespace) -> None:
    """Build model-ready ML dataset (features + labels + split)."""
    mode        = getattr(args, "mode", "real")
    symbols     = getattr(args, "symbols", None)
    start_date  = getattr(args, "start_date", None)
    end_date    = getattr(args, "end_date", None)
    horizons    = getattr(args, "horizons", None)
    output_root = getattr(args, "output_root", None)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.2 — ML Build Dataset (mode={mode})")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from ml.dataset_builder import MLFeatureDatasetBuilder
        kwargs = {}
        if output_root:
            kwargs["output_root"] = output_root
        builder = MLFeatureDatasetBuilder(mode=mode, **kwargs)
        h = list(map(int, horizons.split(","))) if horizons else (5, 10, 20)
        df, summary = builder.build_dataset(symbols=symbols, start_date=start_date, end_date=end_date, label_horizons=h)
        print(f"  Status:        {summary.get('status', '—')}")
        print(f"  Features:      {summary.get('feature_count', 0)}")
        print(f"  Rows:          {summary.get('row_count', 0)}")
        print(f"  Symbols:       {summary.get('symbol_count', 0)}")
        if summary.get("output_path"):
            print(f"  Output:        {summary['output_path']}")
        val = summary.get("validation", {})
        for w in val.get("warnings", []):
            print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Dataset NOT committed. No real orders. ML Research Only.")


def cmd_ml_leakage_check(args: argparse.Namespace) -> None:
    """Run data leakage check on the latest ML dataset."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.2 — ML Leakage Check (mode={mode})")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
        result = MLFeatureStoreAdapter().run_leakage_check()
        if not result.get("ok"):
            print(f"  ERROR: {result.get('error')}")
        else:
            r = result.get("result", {})
            print(f"  Status:  {r.get('status', '—')}")
            print(f"  Score:   {r.get('score', '—')}")
            findings = r.get("findings", [])
            if findings:
                print(f"  Findings ({len(findings)}):")
                for f in findings[:10]:
                    print(f"    [{f.get('severity','')}] {f.get('finding','')} — {f.get('column','')} — {f.get('reason','')[:60]}")
            else:
                print("  No leakage findings.")
            if r.get("status") == "BLOCKED_FOR_TRAINING":
                print()
                print("  [!] DATASET BLOCKED FOR TRAINING — Leakage detected.")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. ML Research Only.")


def cmd_ml_feature_quality(args: argparse.Namespace) -> None:
    """Run feature quality check on the latest ML dataset."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.2 — ML Feature Quality (mode={mode})")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
        result = MLFeatureStoreAdapter().run_feature_quality()
        if not result.get("ok"):
            print(f"  ERROR: {result.get('error')}")
        else:
            r = result.get("result", {})
            print(f"  Quality score:     {r.get('feature_quality_score', '—')}")
            print(f"  Feature count:     {r.get('feature_count', '—')}")
            print(f"  Constant features: {r.get('constant_feature_count', 0)}")
            hm = r.get("high_missing_features", [])
            print(f"  High missing (>50%): {len(hm)}")
            if hm:
                print(f"    {', '.join(hm[:8])}")
            for w in r.get("warnings", []):
                print(f"  [!] {w}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] No real orders. ML Research Only.")


def cmd_ml_feature_importance(args: argparse.Namespace) -> None:
    """Run feature importance shell on the latest ML dataset."""
    mode   = getattr(args, "mode", "real")
    target = getattr(args, "target", "label_direction_5d")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.2 — ML Feature Importance (mode={mode})")
    print(f"  Target: {target}")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
        result = MLFeatureStoreAdapter().run_feature_importance(target_label=target)
        if not result.get("ok"):
            print(f"  ERROR: {result.get('error')}")
        else:
            r = result.get("result", {})
            print(f"  Method:          {r.get('method', '—')}")
            print(f"  Target label:    {r.get('target_label', '—')}")
            print(f"  sklearn:         {r.get('sklearn_available', '—')}")
            top = r.get("top_features", [])
            if top:
                print()
                print(f"  {'#':<4} {'Feature':<35} {'Score':>8} {'Direction'}")
                print(f"  {'-'*60}")
                for i, f in enumerate(top[:15], 1):
                    print(f"  {i:<4} {f.get('feature',''):<35} {f.get('score',0):>8.4f} {f.get('direction','')}")
            else:
                print("  No importance data available.")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Importance scores are exploratory only — not investment advice.")
    print("  [!] No real orders. ML Research Only.")


def cmd_ml_feature_store_report(args: argparse.Namespace) -> None:
    """Generate ML Feature Store report."""
    mode       = getattr(args, "mode", "real")
    report_dir = getattr(args, "report_dir", None)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.2 — ML Feature Store Report (mode={mode})")
    print("  [!] ML Research Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        kwargs = {}
        if report_dir:
            kwargs["report_dir"] = report_dir
        from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
        result = MLFeatureStoreAdapter(**kwargs).generate_report(mode=mode)
        if result.get("ok"):
            print(f"  Report saved: {result.get('report_path')}")
        else:
            print(f"  ERROR: {result.get('error')}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Report NOT committed. No real orders. ML Research Only.")


# ---------------------------------------------------------------------------
# v0.4.4 Intraday Replay Cockpit command handlers
# ---------------------------------------------------------------------------

def cmd_intraday_replay(args: argparse.Namespace) -> None:
    """Step through intraday replay session."""
    mode  = getattr(args, "mode", "real")
    stock = getattr(args, "stock", None)
    freq  = getattr(args, "freq", "1min")
    steps = getattr(args, "steps", 30)
    date_ = getattr(args, "date", None)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.4 — Intraday Replay (mode={mode})")
    print(f"  [!] Replay Training Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from replay.replay_session import ReplaySessionManager
        from replay.replay_engine import IntradayReplayEngine
        if not stock:
            print("  No --stock specified. Use --stock <symbol> to replay a symbol.")
            return
        mgr    = ReplaySessionManager()
        sess   = mgr.create_session(symbol=stock, freq=freq, date=date_)
        engine = IntradayReplayEngine(freq=freq)
        result = engine.load_intraday_data(symbol=stock, date=date_)
        if result.get("status") == "INSUFFICIENT_INTRADAY_DATA":
            print(f"  Status: INSUFFICIENT_INTRADAY_DATA")
            print(f"  No intraday CSV found for {stock} ({freq}).")
            print(f"  Import data to data/import/intraday_standard/{freq}/ first.")
            return
        total_bars = result.get("total_bars", 0)
        print(f"  Symbol:     {stock}")
        print(f"  Frequency:  {freq}")
        print(f"  Total bars: {total_bars}")
        print(f"  Replaying {min(steps, total_bars)} bars...")
        print()
        for i in range(min(steps, total_bars)):
            bar = engine.step_forward()
            if bar is None or bar.get("status") in ("NOT_LOADED", "INSUFFICIENT_INTRADAY_DATA"):
                break
            t = bar.get("datetime", bar.get("time", "—"))
            o = bar.get("open", 0) or 0
            h = bar.get("high", 0) or 0
            lo = bar.get("low", 0) or 0
            c = bar.get("close", 0) or 0
            v = bar.get("volume", 0) or 0
            try:
                print(f"  [{i+1:>3}] {str(t)[:19]}  O={float(o):.2f}  H={float(h):.2f}  L={float(lo):.2f}  C={float(c):.2f}  V={int(v)}")
            except Exception:
                print(f"  [{i+1:>3}] {t}")
        mgr.complete_session(sess.session_id)
        print()
        print(f"  Session ID: {sess.session_id}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Replay bars are historical read-only data. Not investment advice.")
    print("  [!] No real orders. Replay Training Only.")


def cmd_intraday_replay_report(args: argparse.Namespace) -> None:
    """Generate Intraday Replay Cockpit report."""
    mode       = getattr(args, "mode", "real")
    report_dir = getattr(args, "report_dir", None)
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.4 — Intraday Replay Report (mode={mode})")
    print("  [!] Replay Training Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from gui.intraday_replay_adapter import IntradayReplayAdapter
        kwargs = {}
        if report_dir:
            kwargs["report_dir"] = report_dir
        result = IntradayReplayAdapter(**kwargs).generate_report(mode=mode)
        if result.get("ok"):
            print(f"  Report saved: {result.get('report_path')}")
        else:
            print(f"  ERROR: {result.get('error')}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Report NOT committed. No real orders. Replay Training Only.")


def cmd_replay_session_list(args: argparse.Namespace) -> None:
    """List all replay sessions."""
    limit = getattr(args, "limit", 20)
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.4 — Replay Session List")
    print("  [!] Replay Training Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from replay.replay_session import ReplaySessionManager
        sessions = ReplaySessionManager().list_sessions(limit=limit)
        if not sessions:
            print("  No sessions found.")
        else:
            print(f"  {'ID':<30} {'Symbol':<8} {'Freq':<6} {'Status':<12} {'Created'}")
            print(f"  {'-'*80}")
            for s in sessions[:limit]:
                print(f"  {s.get('session_id',''):<30} {s.get('symbol',''):<8} "
                      f"{s.get('freq',''):<6} {s.get('status',''):<12} {s.get('created_at','')[:19]}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Sessions are training records only. No real orders.")


def cmd_replay_session_show(args: argparse.Namespace) -> None:
    """Show detail for a single replay session."""
    session_id = getattr(args, "id", None)
    print("=" * 60)
    print("  TW Quant Cockpit v0.4.4 — Replay Session Detail")
    print("  [!] Replay Training Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    if not session_id:
        print("  ERROR: --id is required. Use 'python main.py replay-session-list' to find IDs.")
        return
    try:
        from replay.replay_session import ReplaySessionManager
        sess = ReplaySessionManager().load_session(session_id)
        if sess is None:
            print(f"  Session not found: {session_id}")
        else:
            for k, v in sess.to_dict().items():
                print(f"  {k:<25} {v}")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Session data is training record only. Not investment advice.")


def cmd_replay_training_summary(args: argparse.Namespace) -> None:
    """Show replay training mode summary (quiz accuracy, grade)."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print(f"  TW Quant Cockpit v0.4.4 — Replay Training Summary (mode={mode})")
    print("  [!] Replay Training Only | Read Only | No Real Orders | Production BLOCKED")
    print("=" * 60)
    try:
        from replay.replay_session import ReplaySessionManager
        mgr     = ReplaySessionManager()
        summary = mgr.summary()
        sessions_all = mgr.list_sessions(limit=1000)
        completed = [s for s in sessions_all if s.get("status") == "COMPLETED"]
        print(f"  Total sessions:      {summary.get('total', 0)}")
        print(f"  Completed sessions:  {len(completed)}")
        by_status = summary.get("by_status", {})
        for status, count in sorted(by_status.items()):
            print(f"    {status:<12} {count}")
        print()
        print(f"  (Run with --mode real to see per-session metrics after completing sessions)")
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()
    print("  [!] Training answers are NOT trading instructions. No real orders.")


# ---------------------------------------------------------------------------
# v0.4.2.1 ML Knowledge Integration command handlers
# ---------------------------------------------------------------------------

def cmd_ml_knowledge_integrate(args: argparse.Namespace) -> None:
    """Integrate transcript-derived knowledge into ML Feature Store."""
    mode         = getattr(args, "mode", "real")
    dry_run      = getattr(args, "dry_run", False)
    do_report    = getattr(args, "report", False)
    knowledge_dir = getattr(args, "knowledge_dir", "data/backtest_results/strategy_knowledge")
    output_dir   = getattr(args, "output_dir", "data/backtest_results/ml_feature_store")

    print("=" * 60)
    print("  TW Quant Cockpit — ML Knowledge Integration v0.4.2.1")
    print("=" * 60)
    print(f"  Mode     : {mode}")
    print(f"  Dry Run  : {dry_run}")
    print(f"  Knowledge: {knowledge_dir}")
    print(f"  Output   : {output_dir}")
    print()
    print("  [!] ML Research Only. No Real Orders. Production Trading: BLOCKED.")
    print("  [!] auto_enabled = False. Confidence capped at PARTIAL.")
    print()

    try:
        from ml.knowledge_feature_bridge import KnowledgeFeatureBridge
        from ml.knowledge_feature_catalog import KnowledgeFeatureCatalog
        from ml.knowledge_feature_readiness import KnowledgeFeatureReadinessChecker
        from ml.knowledge_leakage_checker import KnowledgeLeakageChecker
        from ml.knowledge_dataset_exporter import KnowledgeDatasetExporter

        # 1. Bridge
        bridge = KnowledgeFeatureBridge(knowledge_dir=knowledge_dir)
        files_present = bridge.knowledge_files_present()
        print("  Knowledge files:")
        for fname, present in files_present.items():
            status = "OK" if present else "NOT FOUND"
            print(f"    {fname}: {status}")
        print()

        if not bridge.knowledge_dir_exists():
            print(f"  [WARN] Knowledge directory not found: {knowledge_dir}")
            print("  Run 'strategy-knowledge-ingest' first to populate knowledge CSVs.")
            print()
            return

        result = bridge.convert_all()
        all_features  = result.get("all_features", [])
        bridge_summary = result.get("summary", {})

        src = bridge_summary.get("source_rows", {})
        print(f"  Source rows loaded:")
        print(f"    factor_candidates : {src.get('factor_candidates', 0)}")
        print(f"    rule_candidates   : {src.get('rule_candidates', 0)}")
        print(f"    avoid_conditions  : {src.get('avoid_conditions', 0)}")
        print(f"    risk_conditions   : {src.get('risk_conditions', 0)}")
        print(f"  Feature candidates : {len(all_features)}")
        print(f"  Auto Enabled       : 0")
        print()

        if not all_features:
            print("  [WARN] No knowledge features found.")
            print("  Strategy knowledge CSVs are empty or not present.")
            print()
            return

        # 2. Readiness
        readiness_checker = KnowledgeFeatureReadinessChecker()
        readiness_results = readiness_checker.check_features(all_features)
        readiness_summary = readiness_checker.build_summary(readiness_results)
        print("  Readiness estimate:")
        for rd, cnt in sorted(readiness_summary.get("by_readiness", {}).items(),
                              key=lambda x: -x[1]):
            print(f"    {rd:25s}: {cnt}")
        print()

        # 3. Leakage
        leakage_checker = KnowledgeLeakageChecker()
        leakage_result  = leakage_checker.check_features(all_features)
        print(f"  Leakage status     : {leakage_result.get('status', 'UNKNOWN')}")
        print(f"  Leakage findings   : {leakage_result.get('total_findings', 0)}")
        print(f"  Critical leakage   : {leakage_result.get('critical_count', 0)}")
        print()

        if dry_run:
            print("  [DRY RUN] No files written.")
            print()
        else:
            # 4. Export
            exporter = KnowledgeDatasetExporter(output_dir=output_dir)
            export_summary = exporter.export_all(
                catalog_features=all_features,
                readiness_results=readiness_results,
                leakage_result=leakage_result,
                dry_run=False,
            )
            print("  Output files:")
            for key, path in export_summary.get("output_files", {}).items():
                print(f"    {key:12s}: {path}")
            print(f"  Model-ready (optional): {export_summary.get('model_ready_features', 0)}")
            print()

        if do_report:
            try:
                from gui.ml_knowledge_integration_adapter import MLKnowledgeIntegrationAdapter
                adapter = MLKnowledgeIntegrationAdapter(
                    mode=mode, knowledge_dir=knowledge_dir, output_dir=output_dir
                )
                report_result = adapter.generate_report(dry_run=False)
                if report_result.get("status") == "OK":
                    print(f"  Report: {report_result.get('report_path', '')}")
                else:
                    print(f"  [WARN] Report: {report_result.get('error', '')}")
            except Exception as rexc:
                print(f"  [WARN] Report generation failed: {rexc}")
            print()

        print("  ML Knowledge Integration complete.")
        print("  Knowledge Only. Research Only. No Real Orders. Production Trading BLOCKED.")

    except Exception as exc:
        logger.error("ml-knowledge-integrate failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_ml_knowledge_leakage_check(args: argparse.Namespace) -> None:
    """Check transcript-derived knowledge features for data leakage."""
    output_dir = getattr(args, "output_dir", "data/backtest_results/ml_feature_store")

    print("=" * 60)
    print("  TW Quant Cockpit — ML Knowledge Leakage Check v0.4.2.1")
    print("=" * 60)
    print(f"  Output dir: {output_dir}")
    print()
    print("  [!] ML Research Only. No Real Orders.")
    print()

    try:
        from gui.ml_knowledge_integration_adapter import MLKnowledgeIntegrationAdapter
        adapter = MLKnowledgeIntegrationAdapter(output_dir=output_dir)
        result  = adapter.check_leakage()

        status = result.get("status", "UNKNOWN")
        print(f"  Leakage status   : {status}")
        print(f"  Total findings   : {result.get('total_findings', 0)}")
        print(f"  Critical         : {result.get('critical_count', 0)}")
        print(f"  Warning          : {result.get('warning_count', 0)}")
        print(f"  Auto Enabled     : 0")
        print()

        summary = result.get("summary", {})
        by_type = summary.get("by_leakage_type", {})
        if by_type:
            print("  By leakage type:")
            for lt, cnt in sorted(by_type.items(), key=lambda x: -x[1]):
                print(f"    {lt:35s}: {cnt}")
            print()

        recs = summary.get("recommendations", [])
        if recs:
            print("  Recommendations:")
            for rec in recs:
                print(f"    - {rec}")
            print()

        if result.get("warning"):
            print(f"  [WARN] {result['warning']}")
            print()

    except Exception as exc:
        logger.error("ml-knowledge-leakage-check failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_ml_knowledge_feature_summary(args: argparse.Namespace) -> None:
    """Show latest ML Knowledge Integration summary."""
    output_dir = getattr(args, "output_dir", "data/backtest_results/ml_feature_store")

    print("=" * 60)
    print("  TW Quant Cockpit — ML Knowledge Feature Summary v0.4.2.1")
    print("=" * 60)
    print()

    try:
        from ml.knowledge_dataset_exporter import KnowledgeDatasetExporter
        exporter = KnowledgeDatasetExporter(output_dir=output_dir)
        summary  = exporter.load_latest_summary()

        if not summary:
            print(f"  [WARN] No ML knowledge integration summary found in: {output_dir}")
            print("  Run 'ml-knowledge-integrate' first.")
            print()
            return

        print(f"  Generated at     : {summary.get('generated_at', 'N/A')}")
        print(f"  Total features   : {summary.get('total_features', 0)}")
        print(f"  Model-ready      : {summary.get('model_ready_features', 0)}")
        print(f"  Auto Enabled     : 0")
        print(f"  Leakage findings : {summary.get('leakage_findings', 0)}")
        print(f"  Critical leakage : {summary.get('critical_leakage', 0)}")
        print(f"  ML Research Only : True")
        print(f"  No Real Orders   : True")
        print()

        out_files = summary.get("output_files", {})
        if out_files:
            print("  Output files:")
            for key, path in out_files.items():
                print(f"    {key:12s}: {path}")
            print()

    except Exception as exc:
        logger.error("ml-knowledge-feature-summary failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


# ---------------------------------------------------------------------------
# v0.4.6 Portfolio Journal command handlers
# ---------------------------------------------------------------------------

def _journal_header(mode: str) -> None:
    print("=" * 60)
    print("  TW Quant Cockpit — Portfolio Journal v0.4.6")
    print("=" * 60)
    print(f"  Mode          : {mode}")
    print(f"  Journal Only  : True")
    print(f"  Research Only : True")
    print(f"  No Real Orders: True")
    print()


def cmd_journal_add(args: argparse.Namespace) -> None:
    """Add a research-only journal entry."""
    mode = getattr(args, "mode", "real")
    _journal_header(mode)
    try:
        from gui.portfolio_journal_adapter import PortfolioJournalAdapter
        adapter = PortfolioJournalAdapter(mode=mode)

        payload = {
            "symbol":               getattr(args, "symbol", ""),
            "entry_type":           getattr(args, "entry_type", "simulated_trade"),
            "timeframe":            getattr(args, "timeframe", ""),
            "signal_source":        getattr(args, "signal_source", ""),
            "planned_entry_price":  getattr(args, "planned_entry", None),
            "planned_stop_loss":    getattr(args, "planned_stop", None),
            "planned_take_profit":  getattr(args, "planned_target", None),
            "reason":               getattr(args, "reason", ""),
            "thesis":               getattr(args, "thesis", ""),
            "invalidation_condition": getattr(args, "invalidation", ""),
        }
        result = adapter.add_entry(payload)
        print(f"  Status     : {result.get('status', 'ERROR')}")
        if result.get("status") == "OK":
            print(f"  Journal ID : {result.get('journal_id', '')}")
        else:
            print(f"  ERROR: {result.get('error', '')}")
        print()
        print("  [!] Journal Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("journal-add failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_journal_list(args: argparse.Namespace) -> None:
    """List recent journal entries."""
    mode   = getattr(args, "mode", "real")
    limit  = getattr(args, "limit", 20)
    symbol = getattr(args, "symbol", None)
    status = getattr(args, "status", None)
    _journal_header(mode)
    try:
        from gui.portfolio_journal_adapter import PortfolioJournalAdapter
        adapter = PortfolioJournalAdapter(mode=mode)
        entries = adapter.list_entries(limit=limit, symbol=symbol, status=status)
        summary = adapter.build_summary()
        print(f"  Total: {summary.get('entries_count', 0)}  "
              f"Review Required: {summary.get('review_required_count', 0)}")
        print()
        if not entries:
            print("  No journal entries recorded.")
        else:
            for e in entries:
                created = str(e.get("created_at", ""))[:10]
                sym     = e.get("symbol", "—")
                etype   = e.get("entry_type", "")
                st      = e.get("status", "")
                outcome = e.get("outcome_label", "")
                jid     = e.get("journal_id", "")
                print(f"  {created}  {jid}  [{sym:6s}] [{etype:20s}] {st:20s}  {outcome}")
        print()
        print("  [!] Journal Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("journal-list failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_journal_show(args: argparse.Namespace) -> None:
    """Show detail for a single journal entry."""
    mode = getattr(args, "mode", "real")
    jid  = getattr(args, "id", "")
    _journal_header(mode)
    if not jid:
        print("  ERROR: --id is required.")
        print()
        return
    try:
        from gui.portfolio_journal_adapter import PortfolioJournalAdapter
        adapter = PortfolioJournalAdapter(mode=mode)
        entry = adapter.get_entry(jid)
        if not entry:
            print(f"  Not found: {jid}")
        else:
            for k, v in entry.items():
                if v not in (None, "", [], {}):
                    print(f"  {k:30s}: {v}")
        print()
        print("  [!] Journal Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("journal-show failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_journal_review(args: argparse.Namespace) -> None:
    """Update outcome / notes / mistake tags for a journal entry."""
    mode    = getattr(args, "mode", "real")
    jid     = getattr(args, "id", "")
    outcome = getattr(args, "outcome", "")
    notes   = getattr(args, "notes", "")
    tags    = getattr(args, "mistake_tags", "")
    _journal_header(mode)
    if not jid:
        print("  ERROR: --id is required.")
        print()
        return
    try:
        from gui.portfolio_journal_adapter import PortfolioJournalAdapter
        adapter = PortfolioJournalAdapter(mode=mode)
        payload = {}
        if outcome:
            payload["outcome_label"] = outcome
        if notes:
            payload["review_notes"] = notes
        if tags:
            payload["mistake_tags"] = tags
        result = adapter.update_review(jid, payload)
        print(f"  Status     : {result.get('status', 'ERROR')}")
        if result.get("status") == "OK":
            updated = result.get("entry", {})
            print(f"  Outcome    : {updated.get('outcome_label', '')}")
            print(f"  Status     : {updated.get('status', '')}")
        else:
            print(f"  ERROR: {result.get('error', '')}")
        print()
        print("  [!] Journal Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("journal-review failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_journal_report(args: argparse.Namespace) -> None:
    """Generate Portfolio Journal Markdown report."""
    mode    = getattr(args, "mode", "real")
    dry_run = getattr(args, "dry_run", False)
    _journal_header(mode)
    try:
        from gui.portfolio_journal_adapter import PortfolioJournalAdapter
        adapter = PortfolioJournalAdapter(mode=mode)
        result  = adapter.generate_report(mode=mode, dry_run=dry_run)
        print(f"  Status  : {result.get('status', 'ERROR')}")
        path = result.get("report_path", "")
        if result.get("status") == "OK":
            if dry_run:
                print(f"  [dry-run] Would write: {path}")
            else:
                print(f"  Report  → {path}")
        else:
            print(f"  ERROR: {result.get('error', '')}")
        print()
        print("  [!] Journal Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("journal-report failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_journal_summary(args: argparse.Namespace) -> None:
    """Show journal statistics summary."""
    mode = getattr(args, "mode", "real")
    _journal_header(mode)
    try:
        from gui.portfolio_journal_adapter import PortfolioJournalAdapter
        adapter  = PortfolioJournalAdapter(mode=mode)
        summary  = adapter.build_summary()
        analytics = adapter.run_analytics()
        print(f"  Total Entries    : {summary.get('entries_count', 0)}")
        print(f"  Reviewed         : {summary.get('reviewed_count', 0)}")
        print(f"  Review Required  : {summary.get('review_required_count', 0)}")
        print(f"  Open Simulated   : {summary.get('open_simulated_count', 0)}")
        print(f"  Closed Simulated : {summary.get('closed_simulated_count', 0)}")
        print(f"  Most Common Mistake: {summary.get('most_common_mistake', '—')}")
        print(f"  Latest Entry     : {summary.get('latest_entry_at', '—')}")
        if analytics.get("win_rate") is not None:
            print(f"  Win Rate         : {analytics['win_rate']:.1%}")
        if analytics.get("avg_return") is not None:
            print(f"  Avg Return %     : {analytics['avg_return']:.2f}%")
        mistakes = analytics.get("most_common_mistakes", [])
        if mistakes:
            print(f"  Top Mistakes     : {', '.join(mistakes[:3])}")
        print()
        print("  [!] Journal Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("journal-summary failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_journal_link_replay(args: argparse.Namespace) -> None:
    """Link a journal entry to a replay session."""
    mode       = getattr(args, "mode", "real")
    jid        = getattr(args, "id", "")
    session_id = getattr(args, "replay_session", "")
    _journal_header(mode)
    if not jid or not session_id:
        print("  ERROR: --id and --replay-session are required.")
        print()
        return
    try:
        from gui.portfolio_journal_adapter import PortfolioJournalAdapter
        adapter = PortfolioJournalAdapter(mode=mode)
        result  = adapter.link_replay_session(jid, session_id)
        print(f"  Status         : {result.get('status', 'ERROR')}")
        if result.get("status") == "OK":
            print(f"  Journal ID     : {jid}")
            print(f"  Replay Session : {session_id}")
        else:
            print(f"  ERROR: {result.get('error', '')}")
        print()
        print("  [!] Journal Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("journal-link-replay failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


# ---------------------------------------------------------------------------
# v0.4.5 Notification Center command handlers
# ---------------------------------------------------------------------------

def cmd_notification_scan(args: argparse.Namespace) -> None:
    """Evaluate notification rules and persist generated events."""
    mode = getattr(args, "mode", "real")
    print("=" * 60)
    print("  TW Quant Cockpit — Notification Scan v0.4.5")
    print("=" * 60)
    print(f"  Mode: {mode}")
    print(f"  [!] Notification Only. Research Only. No Real Orders.")
    print()
    try:
        from gui.notification_center_adapter import NotificationCenterAdapter
        adapter = NotificationCenterAdapter(mode=mode)
        result = adapter.run_scan()
        status    = result.get("status", "ERROR")
        new_events = result.get("new_events", 0)
        print(f"  Status     : {status}")
        print(f"  New Events : {new_events}")
        for evt in result.get("events", []):
            sev  = evt.get("severity", "INFO")
            cat  = evt.get("category", "")
            title = evt.get("title", "")
            print(f"    [{sev}] [{cat}] {title}")
        if status == "ERROR":
            print(f"  ERROR: {result.get('error', '')}")
        print()
        print("  [!] Notification Only. No Real Orders.")
    except Exception as exc:
        logger.error("notification-scan failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_notification_list(args: argparse.Namespace) -> None:
    """List recent notification events."""
    limit      = getattr(args, "limit", 50)
    severity   = getattr(args, "severity", None)
    category   = getattr(args, "category", None)
    unread_only = getattr(args, "unread_only", False)
    print("=" * 60)
    print("  TW Quant Cockpit — Notification List v0.4.5")
    print("=" * 60)
    try:
        from gui.notification_center_adapter import NotificationCenterAdapter
        adapter = NotificationCenterAdapter()
        events  = adapter.list_notifications(
            limit=limit,
            severity=severity,
            category=category,
            unread_only=unread_only,
        )
        summary = adapter.get_summary()
        print(f"  Total: {summary.get('total_events', 0)}  "
              f"Unread: {summary.get('unread_count', 0)}  "
              f"Critical: {summary.get('critical_count', 0)}")
        print()
        if not events:
            print("  No notifications recorded.")
        else:
            for evt in events:
                created = evt.get("created_at", "")[:19]
                sev     = evt.get("severity", "INFO")
                cat     = evt.get("category", "")
                title   = evt.get("title", "")
                status  = evt.get("status", "")
                print(f"  {created}  [{sev:8s}] [{cat:10s}] {title}  ({status})")
        print()
        print(f"  [!] Notification Only. No Real Orders. external_enabled=False.")
    except Exception as exc:
        logger.error("notification-list failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_notification_report(args: argparse.Namespace) -> None:
    """Generate Notification Center Markdown report."""
    mode    = getattr(args, "mode", "real")
    dry_run = getattr(args, "dry_run", False)
    print("=" * 60)
    print("  TW Quant Cockpit — Notification Report v0.4.5")
    print("=" * 60)
    print(f"  Mode   : {mode}")
    print(f"  Dry Run: {dry_run}")
    print()
    try:
        from gui.notification_center_adapter import NotificationCenterAdapter
        adapter = NotificationCenterAdapter(mode=mode)
        result  = adapter.generate_report(dry_run=dry_run)
        status  = result.get("status", "ERROR")
        path    = result.get("report_path", "")
        print(f"  Status: {status}")
        if status == "OK":
            if dry_run:
                print(f"  [dry-run] Report would be written to: {path}")
            else:
                print(f"  Report written → {path}")
        else:
            print(f"  ERROR: {result.get('error', '')}")
        print()
        print("  [!] Notification Only. Research Only. No Real Orders.")
    except Exception as exc:
        logger.error("notification-report failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_notification_clear_read(args: argparse.Namespace) -> None:
    """Clear all read notifications from the log."""
    print("=" * 60)
    print("  TW Quant Cockpit — Notification Clear Read v0.4.5")
    print("=" * 60)
    try:
        from gui.notification_center_adapter import NotificationCenterAdapter
        adapter = NotificationCenterAdapter()
        result  = adapter.clear_read()
        removed = result.get("removed", 0)
        print(f"  Removed {removed} read notification(s).")
        print()
        print("  [!] Notification Only. No Real Orders.")
    except Exception as exc:
        logger.error("notification-clear-read failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_notification_test(args: argparse.Namespace) -> None:
    """Add a test notification event."""
    severity = getattr(args, "severity", "INFO")
    print("=" * 60)
    print("  TW Quant Cockpit — Notification Test v0.4.5")
    print("=" * 60)
    print(f"  Severity: {severity}")
    print()
    try:
        from gui.notification_center_adapter import NotificationCenterAdapter
        adapter = NotificationCenterAdapter()
        result  = adapter.send_test_notification(severity=severity)
        status  = result.get("status", "ERROR")
        print(f"  Status: {status}")
        if status == "OK":
            evt = result.get("event", {})
            print(f"  ID     : {evt.get('notification_id', '')}")
            print(f"  Title  : {evt.get('title', '')}")
            print(f"  Message: {evt.get('message', '')}")
        else:
            print(f"  ERROR: {result.get('error', '')}")
        print()
        print("  [!] Notification Only. No Real Orders. external_enabled=False.")
    except Exception as exc:
        logger.error("notification-test failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


# ---------------------------------------------------------------------------
# v0.4.1.1 Strategy Knowledge Ingestion command handlers
# ---------------------------------------------------------------------------

def cmd_strategy_knowledge_ingest(args: argparse.Namespace) -> None:
    """Run Strategy Knowledge Ingestion from transcripts."""
    mode       = getattr(args, "mode", "real")
    dry_run    = getattr(args, "dry_run", False)
    input_dirs = getattr(args, "input_dir", None)
    output_dir = getattr(args, "output_dir", "data/backtest_results/strategy_knowledge")
    report_dir = getattr(args, "report_dir", "reports")
    do_report  = getattr(args, "report", False)

    # Parse comma-separated or repeated --input-dir values
    parsed_input_dirs = None
    if input_dirs:
        if isinstance(input_dirs, list):
            parsed_input_dirs = input_dirs
        else:
            parsed_input_dirs = [d.strip() for d in input_dirs.split(",") if d.strip()]

    print("=" * 60)
    print("  TW Quant Cockpit — Strategy Knowledge Ingestion v0.4.1.1")
    print("  [!] Knowledge Only. Research Only. No Real Orders.")
    print("  [!] auto_activated=False. Confidence capped at PARTIAL.")
    print("  [!] Not investment advice.")
    print("=" * 60)
    print(f"  Mode         : {mode}")
    print(f"  Dry Run      : {dry_run}")
    if parsed_input_dirs:
        for d in parsed_input_dirs:
            print(f"  Input Dir    : {d}")
    print(f"  Output Dir   : {output_dir}")
    print(f"  Report Dir   : {report_dir}")
    print()

    try:
        from knowledge.ingestion_pipeline import StrategyKnowledgeIngestionPipeline
        pipeline = StrategyKnowledgeIngestionPipeline(
            input_dirs=parsed_input_dirs,
            output_dir=output_dir,
            report_dir=report_dir,
            mode=mode,
            dry_run=dry_run,
        )
        summary = pipeline.run()

        print(f"  Files discovered     : {summary.get('files_discovered', 0)}")
        print(f"  Files loaded         : {summary.get('files_loaded', 0)}")
        print(f"  Sources              : {summary.get('sources_count', 0)}")
        print(f"  Knowledge items      : {summary.get('knowledge_items_count', 0)}")
        print(f"  Rule candidates      : {summary.get('rule_candidates_count', 0)}")
        print(f"  Factor candidates    : {summary.get('factor_candidates_count', 0)}")
        print(f"  Entry conditions     : {summary.get('entry_conditions_count', 0)}")
        print(f"  Exit conditions      : {summary.get('exit_conditions_count', 0)}")
        print(f"  Avoid conditions     : {summary.get('avoid_conditions_count', 0)}")
        print(f"  Risk conditions      : {summary.get('risk_conditions_count', 0)}")
        print(f"  Long-cycle risk      : {summary.get('long_cycle_risk_count', 0)}")

        warnings = summary.get("warnings", [])
        if warnings:
            print()
            for w in warnings:
                print(f"  [WARN] {w}")

        if not dry_run:
            out_paths = summary.get("output_paths", {})
            if out_paths:
                print()
                print("  Outputs:")
                for k, v in out_paths.items():
                    print(f"    {k}: {v}")

        if do_report and not dry_run:
            print()
            print("  Generating report…")
            try:
                from reports.strategy_knowledge_ingestion_report import (
                    StrategyKnowledgeIngestionReportBuilder,
                )
                report_path = StrategyKnowledgeIngestionReportBuilder(
                    report_dir=report_dir, mode=mode
                ).build()
                print(f"  Report: {report_path}")
            except Exception as rexc:
                print(f"  [WARN] Report generation failed: {rexc}")

        print()
        print("  Knowledge Only. Research Only. No Real Orders. Production Trading BLOCKED.")

    except Exception as exc:
        logger.error("strategy-knowledge-ingest failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_strategy_knowledge_summary(args: argparse.Namespace) -> None:
    """Show latest Strategy Knowledge Ingestion summary."""
    output_dir = getattr(args, "output_dir", "data/backtest_results/strategy_knowledge")

    print("=" * 60)
    print("  TW Quant Cockpit — Strategy Knowledge Summary v0.4.1.1")
    print("  [!] Knowledge Only. Research Only. No Real Orders.")
    print("=" * 60)

    try:
        from knowledge.knowledge_store import StrategyKnowledgeStore
        store = StrategyKnowledgeStore(output_dir=output_dir)
        summary = store.build_summary()

        print(f"  Sources              : {summary.get('sources_count', 0)}")
        print(f"  Total knowledge items: {summary.get('total_items', 0)}")
        print(f"  Rule candidates      : {summary.get('rule_candidates_count', 0)}")
        print(f"  Avoid conditions     : {summary.get('avoid_conditions_count', 0)}")
        print(f"  Risk conditions      : {summary.get('risk_conditions_count', 0)}")
        print(f"  Factor candidates    : {summary.get('factor_candidates_count', 0)}")
        print(f"  Latest ingestion at  : {summary.get('latest_ingestion_at') or '—'}")
        print()

        by_cat = summary.get("by_category", {})
        if by_cat:
            print("  Items by category:")
            for cat, cnt in sorted(by_cat.items()):
                print(f"    {cat:<30}: {cnt}")
            print()

        print("  Knowledge Only. Research Only. No Real Orders.")

    except Exception as exc:
        logger.error("strategy-knowledge-summary failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


# ---------------------------------------------------------------------------
# v0.4.7 Research Review Dashboard commands
# ---------------------------------------------------------------------------

def cmd_research_review(args: argparse.Namespace) -> None:
    """Run Research Review Dashboard aggregation (v0.4.7)."""
    logger = logging.getLogger("main.research_review")
    mode   = getattr(args, "mode",   "real")
    period = getattr(args, "period", "daily")
    logger.info("research-review mode=%s period=%s", mode, period)

    print()
    print("TW Quant Cockpit — Research Review Dashboard")
    print("=" * 60)
    print(f"  Mode:         {mode}")
    print(f"  Period:       {period}")
    print(f"  Review Only:  Yes")
    print(f"  Research Only: Yes")
    print(f"  No Real Orders: Yes")
    print(f"  Production Trading: BLOCKED")
    print()

    try:
        from review.review_aggregator import ResearchReviewAggregator
        from review.review_scorecard import ResearchReviewScorecard
        from review.review_action_planner import ReviewActionPlanner
        from review.review_store import ResearchReviewStore

        agg     = ResearchReviewAggregator()
        summary = agg.run(mode=mode, period=period)
        items   = agg.get_review_items()

        scorecard   = ResearchReviewScorecard().calculate(summary)
        action_plan = ReviewActionPlanner().build_action_plan(items, scorecard)

        store = ResearchReviewStore(
            output_dir=getattr(args, "output_dir", "data/backtest_results/research_review")
        )
        store.save_summary(summary)
        store.save_review_items(items)
        store.save_scorecard(scorecard)
        store.save_action_plan(action_plan)

        print(f"  Overall Score:    {scorecard.get('overall_review_score', '-')} ({scorecard.get('overall_grade', '-')})")
        print(f"  Open Items:       {summary.get('open_items', 0)}")
        print(f"  Critical:         {summary.get('critical_items', 0)}")
        print(f"  Warnings:         {summary.get('warning_items', 0)}")
        print(f"  Top Mistake:      {summary.get('most_common_mistake', '-') or '-'}")
        print(f"  Action Items:     {summary.get('action_items_count', 0)}")
        print()
        print(f"  [!] Review Only | No Real Orders | Production Trading BLOCKED")
        print()

    except Exception as exc:
        logger.error("research-review failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_review_report(args: argparse.Namespace) -> None:
    """Generate Research Review Dashboard Markdown report (v0.4.7)."""
    logger = logging.getLogger("main.research_review_report")
    mode   = getattr(args, "mode",   "real")
    period = getattr(args, "period", "daily")
    logger.info("research-review-report mode=%s period=%s", mode, period)

    print()
    print("TW Quant Cockpit — Research Review Dashboard Report")
    print("=" * 60)
    print(f"  Mode:   {mode}")
    print(f"  Period: {period}")
    print(f"  [!] Review Only | No Real Orders | Production Trading BLOCKED")
    print()

    try:
        from gui.research_review_dashboard_adapter import ResearchReviewDashboardAdapter
        adapter = ResearchReviewDashboardAdapter(
            report_dir=getattr(args, "report_dir", "reports")
        )
        path = adapter.generate_report(mode=mode, period=period)
        print(f"  Report: {path}")
    except Exception as exc:
        logger.error("research-review-report failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_review_summary(args: argparse.Namespace) -> None:
    """Show latest Research Review Dashboard summary (v0.4.7)."""
    logger = logging.getLogger("main.research_review_summary")

    print()
    print("TW Quant Cockpit — Research Review Summary")
    print("=" * 60)
    print(f"  [!] Review Only | No Real Orders | Production Trading BLOCKED")
    print()

    try:
        from review.review_store import ResearchReviewStore
        store   = ResearchReviewStore(
            output_dir=getattr(args, "output_dir", "data/backtest_results/research_review")
        )
        summary = store.load_latest_summary()
        if not summary:
            print("  No summary found. Run: python main.py research-review --mode real --period daily")
        else:
            for k, v in summary.items():
                print(f"  {k}: {v}")
    except Exception as exc:
        logger.error("research-review-summary failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_review_actions(args: argparse.Namespace) -> None:
    """Show latest Research Review action plan (v0.4.7)."""
    logger = logging.getLogger("main.research_review_actions")

    print()
    print("TW Quant Cockpit — Research Review Action Plan")
    print("=" * 60)
    print(f"  [!] Review Only | No Real Orders | No Trading Actions")
    print()

    try:
        from review.review_store import ResearchReviewStore
        store   = ResearchReviewStore(
            output_dir=getattr(args, "output_dir", "data/backtest_results/research_review")
        )
        actions = store.load_latest_action_plan()
        if not actions:
            print("  No action plan found. Run: python main.py research-review --mode real --period daily")
        else:
            for a in actions:
                p    = a.get("priority", "-")
                atype = a.get("action_type", "-")
                title = a.get("title", "-")
                cmd  = a.get("suggested_command", "")
                print(f"  [P{p}] {atype} | {title}")
                if cmd:
                    print(f"       → {cmd}")
    except Exception as exc:
        logger.error("research-review-actions failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


# ---------------------------------------------------------------------------
# v0.4.9 Research Workflow Automation CLI handlers
# ---------------------------------------------------------------------------

def cmd_research_workflow(args: argparse.Namespace) -> None:
    """Run Research Workflow Automation (v0.4.9)."""
    logger = logging.getLogger("main.research_workflow")
    mode       = getattr(args, "mode", "real")
    wf_type    = getattr(args, "type", "daily_research")
    dry_run    = getattr(args, "dry_run", False)
    output_dir = getattr(args, "output_dir", "data/backtest_results/research_workflow")
    report_dir = getattr(args, "report_dir", "reports")

    print()
    print("TW Quant Cockpit — Research Workflow Automation")
    print("=" * 60)
    print("  [!] Workflow Only | Research Only | No Real Orders | Production Trading BLOCKED")
    print()

    try:
        from workflow_automation.workflow_builder import ResearchWorkflowBuilder
        from workflow_automation.workflow_runner import ResearchWorkflowRunner
        from workflow_automation.workflow_store import ResearchWorkflowStore

        builder = ResearchWorkflowBuilder()
        build_fn = {
            "daily_research":  builder.build_daily_research_workflow,
            "weekly_review":   builder.build_weekly_review_workflow,
            "data_repair":     builder.build_data_repair_workflow,
            "rule_review":     builder.build_rule_review_workflow,
            "replay_training": builder.build_replay_training_workflow,
            "safety_check":    builder.build_safety_check_workflow,
        }.get(wf_type, builder.build_daily_research_workflow)
        tasks = build_fn()

        runner = ResearchWorkflowRunner(output_dir=output_dir, dry_run=dry_run)
        result = runner.run_workflow(tasks, mode=mode, workflow_type=wf_type)
        summary = runner.build_run_summary()

        store = ResearchWorkflowStore(output_dir=output_dir)
        store.save_run(result)
        store.save_tasks(result.workflow_id, tasks)
        store.save_summary(summary)

        print(f"  Mode:              {mode}")
        print(f"  Workflow Type:     {wf_type}")
        print(f"  Workflow Only:     True")
        print(f"  Research Only:     True")
        print(f"  No Real Orders:    True")
        print(f"  Dry Run:           {dry_run}")
        print(f"  Tasks:             {result.tasks_total}")
        print(f"  Passed:            {result.tasks_passed}")
        print(f"  Failed:            {result.tasks_failed}")
        print(f"  Blocked:           {result.tasks_skipped}")
        if result.output_package_path:
            print(f"  Package:           {result.output_package_path}")
    except Exception as exc:
        logger.error("research-workflow failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_workflow_report(args: argparse.Namespace) -> None:
    """Generate Research Workflow Automation Report (v0.4.9)."""
    logger = logging.getLogger("main.research_workflow_report")
    mode       = getattr(args, "mode", "real")
    report_dir = getattr(args, "report_dir", "reports")
    output_dir = getattr(args, "output_dir", "data/backtest_results/research_workflow")

    print()
    print("TW Quant Cockpit — Research Workflow Report")
    print("=" * 60)
    print("  [!] Workflow Only | Research Only | No Real Orders")
    print()

    try:
        from workflow_automation.workflow_store import ResearchWorkflowStore
        from reports.research_workflow_report import ResearchWorkflowReport
        store    = ResearchWorkflowStore(output_dir=output_dir)
        tasks    = store.load_latest_tasks()
        pkg_path = store.load_latest_summary().get("output_package_path", "") if store.load_latest_summary() else ""
        reporter = ResearchWorkflowReport(report_dir=report_dir)
        path = reporter.generate(workflow_run=None, tasks=tasks, package_path=pkg_path, mode=mode)
        print(f"  Report saved: {path}")
    except Exception as exc:
        logger.error("research-workflow-report failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_workflow_summary(args: argparse.Namespace) -> None:
    """Show latest Research Workflow Automation summary (v0.4.9)."""
    logger = logging.getLogger("main.research_workflow_summary")
    output_dir = getattr(args, "output_dir", "data/backtest_results/research_workflow")

    print()
    print("TW Quant Cockpit — Research Workflow Summary")
    print("=" * 60)
    print("  [!] Workflow Only | Research Only | No Real Orders")
    print()

    try:
        from workflow_automation.workflow_store import ResearchWorkflowStore
        store   = ResearchWorkflowStore(output_dir=output_dir)
        summary = store.load_latest_summary()
        if not summary:
            print("  No summary found. Run: python main.py research-workflow --mode real --type daily_research")
        else:
            for k, v in summary.items():
                print(f"  {k}: {v}")
    except Exception as exc:
        logger.error("research-workflow-summary failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_workflow_tasks(args: argparse.Namespace) -> None:
    """List latest Research Workflow tasks (v0.4.9)."""
    logger = logging.getLogger("main.research_workflow_tasks")
    output_dir = getattr(args, "output_dir", "data/backtest_results/research_workflow")

    print()
    print("TW Quant Cockpit — Research Workflow Tasks")
    print("=" * 60)
    print("  [!] Workflow Only | Research Only | No Real Orders")
    print()

    try:
        from workflow_automation.workflow_store import ResearchWorkflowStore
        store = ResearchWorkflowStore(output_dir=output_dir)
        tasks = store.load_latest_tasks()
        if not tasks:
            print("  No tasks found. Run: python main.py research-workflow --mode real --type daily_research")
        else:
            for t in tasks:
                p   = t.get("priority", "-")
                nm  = t.get("task_name", "")
                st  = t.get("status", "-")
                cmd = t.get("suggested_command", "")
                print(f"  [{p}] {nm} — {st}")
                if cmd:
                    print(f"       → {cmd}")
    except Exception as exc:
        logger.error("research-workflow-tasks failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_workflow_package(args: argparse.Namespace) -> None:
    """Generate / show Research Workflow package (v0.4.9)."""
    logger = logging.getLogger("main.research_workflow_package")
    wf_type    = getattr(args, "type", "daily_research")
    output_dir = getattr(args, "output_dir", "data/backtest_results/research_workflow")
    report_dir = getattr(args, "report_dir", "reports")

    print()
    print("TW Quant Cockpit — Research Workflow Package")
    print("=" * 60)
    print("  [!] Workflow Only | Research Only | No Real Orders")
    print()

    try:
        from workflow_automation.workflow_store import ResearchWorkflowStore
        from workflow_automation.package_builder import ResearchPackageBuilder
        store   = ResearchWorkflowStore(output_dir=output_dir)
        summary = store.load_latest_summary()
        run_obj = None
        try:
            from workflow_automation.workflow_schema import ResearchWorkflowRun
            if summary:
                run_obj = ResearchWorkflowRun(**{k: summary.get(k, "") for k in ResearchWorkflowRun.__dataclass_fields__})
        except Exception:
            pass

        builder = ResearchPackageBuilder(output_dir=output_dir, report_dir=report_dir)
        if wf_type == "weekly_review":
            pkg_path = builder.build_weekly_package(run_obj)
        else:
            pkg_path = builder.build_daily_package(run_obj)

        if pkg_path:
            print(f"  Package: {pkg_path}")
        else:
            print("  No package generated (no workflow data found)")
    except Exception as exc:
        logger.error("research-workflow-package failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


# ---------------------------------------------------------------------------
# v0.4.8 Research Assistant / Coach CLI handlers
# ---------------------------------------------------------------------------

def cmd_research_coach(args: argparse.Namespace) -> None:
    """Run Research Assistant / Coach (v0.4.8)."""
    logger = logging.getLogger("main.research_coach")
    mode   = getattr(args, "mode", "real")
    period = getattr(args, "period", "daily")
    output_dir = getattr(args, "output_dir", "data/backtest_results/research_coach")

    print()
    print("TW Quant Cockpit — Research Assistant / Coach")
    print("=" * 60)
    print(f"  [!] Coaching Only | Research Only | No Real Orders | Production Trading BLOCKED")
    print()

    try:
        from coach.research_assistant_engine import ResearchAssistantEngine
        from coach.coach_store import ResearchCoachStore
        engine  = ResearchAssistantEngine()
        summary = engine.run(mode=mode, period=period)
        store   = ResearchCoachStore(output_dir=output_dir)
        paths   = store.save_all(summary)

        print(f"  Mode:                {mode}")
        print(f"  Period:              {period}")
        print(f"  Coaching Only:       True")
        print(f"  Research Only:       True")
        print(f"  No Real Orders:      True")
        print(f"  Total Recommendations: {summary.get('total_recommendations', 0)}")
        print(f"  P0:                  {summary.get('p0_count', 0)}")
        print(f"  P1:                  {summary.get('p1_count', 0)}")
        print(f"  Daily Checklist:     {summary.get('daily_checklist_count', 0)}")
        print(f"  Replay Tasks:        {summary.get('replay_tasks_count', 0)}")
        print(f"  Rule Review:         {summary.get('rule_review_count', 0)}")
        print(f"  Data Repair:         {summary.get('data_repair_count', 0)}")
        if paths:
            print(f"  Saved to:            {output_dir}")
    except Exception as exc:
        logger.error("research-coach failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_coach_report(args: argparse.Namespace) -> None:
    """Generate Research Assistant / Coach Report (v0.4.8)."""
    logger = logging.getLogger("main.research_coach_report")
    mode   = getattr(args, "mode", "real")
    period = getattr(args, "period", "daily")
    report_dir = getattr(args, "report_dir", "reports")

    print()
    print("TW Quant Cockpit — Research Coach Report")
    print("=" * 60)
    print(f"  [!] Coaching Only | Research Only | No Real Orders")
    print()

    try:
        from coach.research_assistant_engine import ResearchAssistantEngine
        from reports.research_assistant_report import ResearchAssistantReport
        engine   = ResearchAssistantEngine()
        summary  = engine.run(mode=mode, period=period)
        reporter = ResearchAssistantReport(report_dir=report_dir)
        path     = reporter.generate(session_summary=summary, mode=mode, period=period)
        print(f"  Report saved: {path}")
    except Exception as exc:
        logger.error("research-coach-report failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_coach_summary(args: argparse.Namespace) -> None:
    """Show latest Research Coach summary (v0.4.8)."""
    logger = logging.getLogger("main.research_coach_summary")

    print()
    print("TW Quant Cockpit — Research Coach Summary")
    print("=" * 60)
    print(f"  [!] Coaching Only | Research Only | No Real Orders")
    print()

    try:
        from coach.coach_store import ResearchCoachStore
        store   = ResearchCoachStore()
        summary = store.load_latest_summary()
        if not summary:
            print("  No summary found. Run: python main.py research-coach --mode real --period daily")
        else:
            for k, v in summary.items():
                print(f"  {k}: {v}")
    except Exception as exc:
        logger.error("research-coach-summary failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_coach_checklist(args: argparse.Namespace) -> None:
    """Show latest Research Coach daily checklist (v0.4.8)."""
    logger = logging.getLogger("main.research_coach_checklist")

    print()
    print("TW Quant Cockpit — Research Coach Checklist")
    print("=" * 60)
    print(f"  [!] Coaching Only | Research Only | No Real Orders")
    print()

    try:
        from coach.coach_store import ResearchCoachStore
        store     = ResearchCoachStore()
        checklist = store.load_daily_checklist()
        if not checklist:
            print("  No checklist found. Run: python main.py research-coach --mode real --period daily")
        else:
            for item in checklist:
                p   = item.get("priority", "-")
                t   = item.get("title", "")
                cmd = item.get("suggested_command", "")
                print(f"  [{p}] {t}")
                if cmd:
                    print(f"       → {cmd}")
    except Exception as exc:
        logger.error("research-coach-checklist failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_coach_replay_plan(args: argparse.Namespace) -> None:
    """Show latest Replay Training Plan (v0.4.8)."""
    logger = logging.getLogger("main.research_coach_replay_plan")

    print()
    print("TW Quant Cockpit — Research Coach Replay Training Plan")
    print("=" * 60)
    print(f"  [!] Coaching Only | Research Only | No Real Orders")
    print()

    try:
        from coach.coach_store import ResearchCoachStore
        store = ResearchCoachStore()
        plan  = store.load_replay_training_plan()
        if not plan:
            print("  No replay plan found. Run: python main.py research-coach --mode real --period daily")
        else:
            for item in plan:
                p      = item.get("priority", "-")
                t      = item.get("title", "")
                reason = item.get("rationale", item.get("summary", ""))
                cmd    = item.get("suggested_command", "")
                print(f"  [{p}] {t} — {reason}")
                if cmd:
                    print(f"       → {cmd}")
    except Exception as exc:
        logger.error("research-coach-replay-plan failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_coach_rule_queue(args: argparse.Namespace) -> None:
    """Show latest Rule Review Queue (v0.4.8)."""
    logger = logging.getLogger("main.research_coach_rule_queue")

    print()
    print("TW Quant Cockpit — Research Coach Rule Review Queue")
    print("=" * 60)
    print(f"  [!] Coaching Only | Research Only | No Real Orders | No Auto Weight Changes")
    print()

    try:
        from coach.coach_store import ResearchCoachStore
        store = ResearchCoachStore()
        queue = store.load_rule_review_queue()
        if not queue:
            print("  No rule queue found. Run: python main.py research-coach --mode real --period daily")
        else:
            for item in queue:
                p      = item.get("priority", "-")
                t      = item.get("title", "")
                reason = item.get("summary", "")
                cmd    = item.get("suggested_command", "")
                print(f"  [{p}] {t}")
                print(f"       {reason}")
                if cmd:
                    print(f"       → {cmd}")
    except Exception as exc:
        logger.error("research-coach-rule-queue failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


def cmd_research_coach_data_repair(args: argparse.Namespace) -> None:
    """Show latest Data Repair Plan (v0.4.8)."""
    logger = logging.getLogger("main.research_coach_data_repair")

    print()
    print("TW Quant Cockpit — Research Coach Data Repair Plan")
    print("=" * 60)
    print(f"  [!] Coaching Only | Research Only | No Real Orders | No Token Display")
    print()

    try:
        from coach.coach_store import ResearchCoachStore
        store  = ResearchCoachStore()
        repair = store.load_data_repair_plan()
        if not repair:
            print("  No data repair plan found. Run: python main.py research-coach --mode real --period daily")
        else:
            for item in repair:
                p   = item.get("priority", "-")
                t   = item.get("title", "")
                s   = item.get("summary", "")
                cmd = item.get("suggested_command", "")
                print(f"  [{p}] {t}")
                print(f"       {s}")
                if cmd:
                    print(f"       → {cmd}")
    except Exception as exc:
        logger.error("research-coach-data-repair failed: %s", exc, exc_info=True)
        print(f"  ERROR: {exc}")
    print()


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Taiwan Quantitative Trading Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- download ---
    p_dl = subparsers.add_parser("download", help="Download stock price data from FinMind")
    p_dl.add_argument("--start", default=None, help="Start date YYYY-MM-DD")
    p_dl.add_argument("--end", default=None, help="End date YYYY-MM-DD")

    # --- features ---
    p_feat = subparsers.add_parser("features", help="Compute and store technical features")
    p_feat.add_argument("--start", default=None, help="Start date YYYY-MM-DD")
    p_feat.add_argument("--end", default=None, help="End date YYYY-MM-DD")

    # --- train ---
    p_train = subparsers.add_parser("train", help="Train the ML ensemble model")
    p_train.add_argument("--start", default=None, help="Start date for training data")
    p_train.add_argument("--end", default=None, help="End date for training data")

    # --- backtest ---
    p_bt = subparsers.add_parser("backtest", help="Run a backtest")
    p_bt.add_argument(
        "--strategy",
        default="momentum",
        choices=["momentum", "mean_reversion", "breakout"],
        help="Strategy to backtest (default: momentum)",
    )
    p_bt.add_argument("--start", default=None, help="Start date YYYY-MM-DD")
    p_bt.add_argument("--end", default=None, help="End date YYYY-MM-DD")
    p_bt.add_argument(
        "--walk-forward",
        action="store_true",
        help="Run walk-forward validation instead of a single backtest",
    )

    # --- pipeline ---
    p_pipe = subparsers.add_parser("pipeline", help="Run the full daily pipeline")
    p_pipe.add_argument("--date", default=None, help="Target date YYYY-MM-DD (default: today)")
    p_pipe.add_argument(
        "--no-update",
        action="store_true",
        help="Skip the data update step",
    )

    # --- report ---
    p_rep = subparsers.add_parser("report", help="Display the daily report")
    p_rep.add_argument("--date", default=None, help="Report date YYYY-MM-DD (default: latest)")

    # --- ui ---
    subparsers.add_parser("ui", help="Launch the Streamlit dashboard")

    # ---- TW Quant Cockpit v1 commands ----

    # --- screener ---
    p_scr = subparsers.add_parser("screener", help="Run Taiwan stock screener (4-layer)")
    p_scr.add_argument("--top", type=int, default=8, help="Max candidates to output (default: 8)")
    p_scr.add_argument("--mode", default="mock", choices=["mock", "real"],
                       help="Data mode: mock (demo) or real (DB/FinMind). Default: mock")

    # --- cockpit ---
    p_cockpit = subparsers.add_parser("cockpit", help="Launch TW Quant Cockpit GUI (PySide6)")
    p_cockpit.add_argument("--mode", default="mock", choices=["mock", "real"],
                           help="Data mode: mock (demo) or real (CSV). Default: mock")

    # --- paper ---
    subparsers.add_parser("paper", help="Show paper trading positions and P&L")

    # --- stock-report ---
    p_sr = subparsers.add_parser("stock-report", help="Generate multi-timeframe analysis report")
    p_sr.add_argument("--stock", required=True, help="Stock symbol, e.g. 2330")
    p_sr.add_argument("--mode", default="mock", choices=["mock", "real"],
                      help="Data mode: mock (demo) or real (DB/FinMind). Default: mock")

    # --- mock-realtime ---
    p_mr = subparsers.add_parser("mock-realtime", help="Run mock real-time market data simulation")
    p_mr.add_argument("--duration", type=int, default=60, help="Simulation duration in seconds (default: 60)")
    p_mr.add_argument("--interval", type=int, default=2, help="Tick interval in seconds (default: 2)")

    # --- import-csv ---
    p_ic = subparsers.add_parser(
        "import-csv",
        help="Import XQ/Excel/manual CSV into standard data/import/ structure",
    )
    p_ic.add_argument(
        "--type", required=True,
        choices=["profile", "daily", "institutional", "margin",
                 "monthly_revenue", "holder", "trust_cost"],
        help="Data type to import",
    )
    p_ic.add_argument("--file", required=True, help="Path to input CSV file")
    p_ic.add_argument(
        "--replace", action="store_true",
        help="Replace existing standard CSV (default: append and deduplicate)",
    )

    # --- data-check ---
    p_dc = subparsers.add_parser(
        "data-check",
        help="Check data completeness for a stock or the full universe",
    )
    grp = p_dc.add_mutually_exclusive_group(required=True)
    grp.add_argument("--stock", default=None, help="Stock symbol, e.g. 2383")
    grp.add_argument("--all", action="store_true", help="Check all stocks in profile universe")

    # --- validate-score ---
    p_vs = subparsers.add_parser(
        "validate-score",
        help="Validate bull_stock_score effectiveness against historical forward returns",
    )
    p_vs.add_argument("--mode",   default="real", choices=["mock", "real"],
                      help="Data mode (default: real)")
    p_vs.add_argument("--start",  default=None,   help="Start date YYYY-MM-DD (optional)")
    p_vs.add_argument("--end",    default=None,   help="End date YYYY-MM-DD (optional)")
    p_vs.add_argument("--top",    type=int, default=8, help="Top-N filter (default: 8)")
    p_vs.add_argument("--output", default=None,   help="Output directory (default: data/backtest_results/)")

    # --- backtest-buy-points ---
    p_bbp = subparsers.add_parser(
        "backtest-buy-points",
        help="Backtest A/B/C buy-point signals against historical outcomes",
    )
    p_bbp.add_argument("--mode",   default="real", choices=["mock", "real"],
                       help="Data mode (default: real)")
    p_bbp.add_argument("--start",  default=None,   help="Start date YYYY-MM-DD (optional)")
    p_bbp.add_argument("--end",    default=None,   help="End date YYYY-MM-DD (optional)")
    p_bbp.add_argument("--stock",  default=None,   help="Single symbol (optional; default: all)")
    p_bbp.add_argument("--output", default=None,   help="Output directory (default: data/backtest_results/)")

    # --- backtest-screener ---
    p_bs = subparsers.add_parser(
        "backtest-screener",
        help="Replay historical screener scores and measure forward return by score bucket",
    )
    p_bs.add_argument("--mode",   default="real", choices=["mock", "real"],
                      help="Data mode (default: real)")
    p_bs.add_argument("--start",  default=None,   help="Start date YYYY-MM-DD (optional)")
    p_bs.add_argument("--end",    default=None,   help="End date YYYY-MM-DD (optional)")
    p_bs.add_argument("--top",    type=int, default=8, help="Top-N filter (default: 8)")
    p_bs.add_argument("--output", default=None,   help="Output directory (default: data/backtest_results/)")

    # --- backtest-strategy-knowledge ---
    p_bsk = subparsers.add_parser(
        "backtest-strategy-knowledge",
        help="Validate Strategy Knowledge Engine Phase 2 signals against historical forward returns",
    )
    p_bsk.add_argument("--mode",         default="real", choices=["mock", "real"],
                       help="Data mode (default: real)")
    p_bsk.add_argument("--stock",        default=None,   help="Single symbol (optional; default: all)")
    p_bsk.add_argument("--start",        default=None,   help="Start date YYYY-MM-DD (optional)")
    p_bsk.add_argument("--end",          default=None,   help="End date YYYY-MM-DD (optional)")
    p_bsk.add_argument("--holding-days", dest="holding_days", type=int, default=20,
                       help="Forward return holding period in days (default: 20)")
    p_bsk.add_argument("--min-samples",  dest="min_samples",  type=int, default=30,
                       help="Minimum signals for OBSERVATIONAL/RELIABLE rating (default: 30)")
    p_bsk.add_argument("--output-dir",   dest="output_dir",   default=None,
                       help="CSV output directory (default: data/backtest_results/)")
    p_bsk.add_argument("--report-dir",   dest="report_dir",   default=None,
                       help="Markdown report directory (default: reports/)")

    # --- build-universe-manifest ---
    p_bum = subparsers.add_parser(
        "build-universe-manifest",
        help="Build universe manifest CSV for 10 / 30 / 50 stock expansion (v0.3.8)",
    )
    p_bum.add_argument("--size",    type=int, default=10, choices=[10, 30, 50],
                       help="Universe size (default: 10)")
    p_bum.add_argument("--output",  default=None,
                       help="Output path for manifest CSV (default: data/universe/universe_manifest.csv)")
    p_bum.add_argument("--replace", action="store_true",
                       help="Replace existing manifest entries (default: preserve existing data)")

    # --- batch-import-xq ---
    p_bixq = subparsers.add_parser(
        "batch-import-xq",
        help="Batch-import XQ export files for all universe symbols (v0.3.8)",
    )
    p_bixq.add_argument("--folder",   required=True,
                        help="Folder containing XQ Excel / CSV files")
    p_bixq.add_argument("--universe", type=int, default=10, choices=[10, 30, 50],
                        help="Universe size to import (default: 10)")
    p_bixq.add_argument("--manifest", default=None,
                        help="Path to universe_manifest.csv (optional)")
    p_bixq.add_argument("--dry-run",  action="store_true", dest="dry_run",
                        help="Scan files only, do not import")
    p_bixq.add_argument("--replace",  action="store_true",
                        help="Replace existing imported rows")

    # --- universe-quality ---
    p_uq = subparsers.add_parser(
        "universe-quality",
        help="Check universe data quality and show readiness summary (v0.3.8)",
    )
    p_uq.add_argument("--manifest", default=None,
                      help="Path to universe_manifest.csv (optional)")
    p_uq.add_argument("--report",   action="store_true",
                      help="Also generate Markdown report in reports/")

    # --- run-validation-suite ---
    p_rvs = subparsers.add_parser(
        "run-validation-suite",
        help="Run all four validation backtests in sequence (v0.3.8)",
    )
    p_rvs.add_argument("--mode",         default="real", choices=["mock", "real"],
                       help="Data mode (default: real)")
    p_rvs.add_argument("--min-symbols",  dest="min_symbols", type=int, default=10,
                       help="Minimum eligible symbols required (default: 10)")
    p_rvs.add_argument("--output",       default=None,
                       help="Output directory for CSV results (optional)")

    # --- universe-check ---
    subparsers.add_parser(
        "universe-check",
        help="Show universe expansion status and import recommendations",
    )

    # --- build-universe ---
    p_bu = subparsers.add_parser(
        "build-universe",
        help="Build or update the stock universe profile CSV",
    )
    grp_bu = p_bu.add_mutually_exclusive_group(required=True)
    grp_bu.add_argument(
        "--template",
        choices=["top50", "top100", "top200"],
        help="Use a built-in sample template (top50 / top100 / top200)",
    )
    grp_bu.add_argument(
        "--file",
        default=None,
        help="Path to a user-supplied profile CSV",
    )
    p_bu.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing profile CSV (default: append and deduplicate)",
    )

    # --- batch-import ---
    p_bi = subparsers.add_parser(
        "batch-import",
        help="Batch import CSV files from a folder or bundle directory",
    )
    grp_bi = p_bi.add_mutually_exclusive_group(required=True)
    grp_bi.add_argument(
        "--bundle",
        default=None,
        help="Path to a bundle folder with sub-dirs: profile/daily/institutional/...",
    )
    grp_bi.add_argument(
        "--folder",
        default=None,
        help="Path to folder containing CSV files for --type",
    )
    p_bi.add_argument(
        "--type",
        dest="type",
        choices=["profile", "daily", "institutional", "margin",
                 "monthly_revenue", "holder", "trust_cost"],
        default=None,
        help="Data type to import (required with --folder)",
    )
    p_bi.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing data (default: append and deduplicate)",
    )
    p_bi.add_argument(
        "--dry-run",
        action="store_true",
        help="Read and clean files but do not write to standard CSV",
    )
    p_bi.add_argument(
        "--export-report",
        action="store_true",
        help="Write a Markdown batch import report to data/import_reports/",
    )

    # --- import-xq-export ---
    p_xq = subparsers.add_parser(
        "import-xq-export",
        help="One-command import of XQ technical-analysis export (.xlsx/.xls/.csv)",
    )
    p_xq.add_argument("--file", required=True,
                      help="Path to XQ-exported file (.xlsx, .xls, or .csv)")
    p_xq.add_argument("--symbol", required=True,
                      help="Stock symbol, e.g. 2454")
    p_xq.add_argument("--name", default="",
                      help="Stock name (optional), e.g. 聯發科")
    p_xq.add_argument("--sheet", default=0,
                      help="Excel sheet name or index (default: 0 = first sheet)")
    p_xq.add_argument("--dry-run", action="store_true",
                      help="Split and check only, do not write to data/import/")
    p_xq.add_argument("--replace", action="store_true",
                      help="Replace existing standard CSVs (default: append)")
    p_xq.add_argument("--export-split", action="store_true",
                      help="Export each split DataFrame to --output-dir as separate CSVs")
    p_xq.add_argument("--output-dir", default="data/xq_exports",
                      help="Output folder for --export-split (default: data/xq_exports/)")

    # --- clean-csv ---
    p_cc = subparsers.add_parser(
        "clean-csv",
        help="Clean and normalize a CSV file without importing to standard path",
    )
    p_cc.add_argument(
        "--type", required=True,
        choices=["profile", "daily", "institutional", "margin",
                 "monthly_revenue", "holder", "trust_cost"],
        help="Data type of the CSV",
    )
    p_cc.add_argument("--file", required=True, help="Path to input CSV file")
    p_cc.add_argument("--output", default=None, help="Path to output cleaned CSV (optional)")
    p_cc.add_argument(
        "--dry-run", action="store_true",
        help="Check only, do not write output file",
    )

    # --- data-audit ---
    p_da = subparsers.add_parser(
        "data-audit",
        help="Audit all imported data for quality and coverage",
    )
    p_da.add_argument("--stock", default=None, help="Audit a single stock symbol, e.g. 2383")
    p_da.add_argument(
        "--export", action="store_true",
        help="Export audit report to data/import_reports/ (Markdown + CSV)",
    )

    # --- import-plan ---
    p_ip = subparsers.add_parser(
        "import-plan",
        help="Show prioritized import plan based on current data gaps",
    )
    p_ip.add_argument(
        "--export", action="store_true",
        help="Export import plan to data/import_reports/ (Markdown)",
    )

    # --- provider-status ---
    subparsers.add_parser(
        "provider-status",
        help="Show current data provider availability and configuration",
    )

    # --- time-machine-preview ---
    p_tm = subparsers.add_parser(
        "time-machine-preview",
        help="Show Volume Profile and Opening Microstructure summary for a stock",
    )
    p_tm.add_argument("--stock", required=True, help="Stock symbol, e.g. 2454")
    p_tm.add_argument(
        "--mode", choices=["mock", "real"], default="real",
        help="Data mode: real (default) or mock (demo only)",
    )

    # --- feature-preview ---
    p_fp = subparsers.add_parser(
        "feature-preview",
        help="Display latest computed features for a stock (indicators + volume profile + microstructure)",
    )
    p_fp.add_argument("--stock", required=True, help="Stock symbol, e.g. 2454")
    p_fp.add_argument(
        "--mode", choices=["mock", "real"], default="real",
        help="Data mode: real (default) or mock (demo only)",
    )

    # --- strategy-preview (v0.3.6) ---
    p_sp = subparsers.add_parser(
        "strategy-preview",
        help="Full Strategy Knowledge Engine preview (position plan, MACD, volume, valuation, exit)",
    )
    p_sp.add_argument("--stock", required=True, help="Stock symbol, e.g. 2454")
    p_sp.add_argument(
        "--mode", choices=["mock", "real"], default="real",
        help="Data mode: real (default) or mock (demo only)",
    )

    # --- simulate-portfolio (v0.3.12) ---
    p_sp12 = subparsers.add_parser(
        "simulate-portfolio",
        help="Simulate a multi-position portfolio with capital allocation and risk controls (v0.3.12)",
    )
    p_sp12.add_argument("--mode",     default="real", choices=["mock", "real"],
                        help="Data mode (default: real)")
    p_sp12.add_argument("--scenario", default="balanced",
                        choices=["conservative", "balanced", "aggressive",
                                 "no_risk_control_baseline", "all"],
                        help="Preset scenario or 'all' to compare all 4 (default: balanced)")
    p_sp12.add_argument("--initial-capital",      dest="initial_capital",      type=float, default=1_000_000,
                        help="Starting capital in NTD (default: 1000000)")
    p_sp12.add_argument("--max-positions",        dest="max_positions",        type=int,   default=5,
                        help="Max simultaneous positions (default: 5)")
    p_sp12.add_argument("--position-size-pct",    dest="position_size_pct",    type=float, default=0.2,
                        help="Position size as fraction of equity (default: 0.2)")
    p_sp12.add_argument("--max-sector-exposure-pct", dest="max_sector_exposure_pct", type=float, default=0.5,
                        help="Max sector exposure fraction (default: 0.5)")
    p_sp12.add_argument("--stop-loss-pct",        dest="stop_loss_pct",        type=float, default=0.08,
                        help="Fixed stop loss fraction (default: 0.08)")
    p_sp12.add_argument("--take-profit-pct",      dest="take_profit_pct",      type=float, default=0.20,
                        help="Take-profit trigger for half-exit (default: 0.20)")
    p_sp12.add_argument("--trailing-stop-pct",    dest="trailing_stop_pct",    type=float, default=0.10,
                        help="Trailing stop fraction from peak (default: 0.10)")
    p_sp12.add_argument("--start",      default=None, help="Start date YYYY-MM-DD (optional)")
    p_sp12.add_argument("--end",        default=None, help="End date YYYY-MM-DD (optional)")
    p_sp12.add_argument("--output-dir", dest="output_dir",  default=None,
                        help="Output directory for CSVs (default: data/backtest_results/)")
    p_sp12.add_argument("--report-dir", dest="report_dir",  default=None,
                        help="Output directory for report (default: reports/)")

    # --- signal-quality (v0.3.14) ---
    p_sq14 = subparsers.add_parser(
        "signal-quality",
        help="Generate Signal Quality Dashboard from all backtest results (v0.3.14)",
    )
    p_sq14.add_argument("--mode",       default="real", choices=["mock", "real"],
                        help="Data mode (default: real)")
    p_sq14.add_argument("--report",     action="store_true", default=False,
                        help="Generate Markdown report")
    p_sq14.add_argument("--refresh",    action="store_true", default=False,
                        help="Re-run signal quality engine and generate report")
    p_sq14.add_argument("--results-dir", dest="results_dir", default=None,
                        help="Backtest results directory (default: data/backtest_results/)")
    p_sq14.add_argument("--report-dir", dest="report_dir",  default=None,
                        help="Report output directory (default: reports/)")

    # --- scheduler-init-config (v0.3.17) ---
    p_si = subparsers.add_parser(
        "scheduler-init-config",
        help="Create safe disabled scheduler config (v0.3.17)",
    )
    p_si.add_argument("--config",  default=None,
                      help="Path to scheduler config YAML (default: config/scheduler_config.yaml)")

    # --- scheduler-status (v0.3.17) ---
    p_ss = subparsers.add_parser(
        "scheduler-status",
        help="Show automation scheduler status and recent run summary (v0.3.17)",
    )
    p_ss.add_argument("--config",  default=None)
    p_ss.add_argument("--log-dir", dest="log_dir", default=None)

    # --- scheduler-list (v0.3.17) ---
    p_sl = subparsers.add_parser(
        "scheduler-list",
        help="List all configured automation tasks (v0.3.17)",
    )
    p_sl.add_argument("--config",  default=None)
    p_sl.add_argument("--log-dir", dest="log_dir", default=None)

    # --- scheduler-next-runs (v0.3.17) ---
    p_sn = subparsers.add_parser(
        "scheduler-next-runs",
        help="Show next scheduled run times for all tasks (v0.3.17)",
    )
    p_sn.add_argument("--config",  default=None)
    p_sn.add_argument("--log-dir", dest="log_dir", default=None)

    # --- provider-auto-fetch (v0.3.19) ---
    p_paf = subparsers.add_parser(
        "provider-auto-fetch",
        help="Auto-fetch data from best available provider (v0.3.19)",
    )
    p_paf.add_argument("--mode", default="real", choices=["mock", "real"])
    p_paf.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                       help="Preview fetch without writing files")
    p_paf.add_argument("--dataset", default="all",
                       choices=["all","daily_price","monthly_revenue","institutional","margin","fundamental"],
                       help="Dataset to fetch (default: all)")
    p_paf.add_argument("--months", type=int, default=24,
                       help="Lookback months (default: 24)")
    p_paf.add_argument("--max-symbols", dest="max_symbols", type=int, default=None,
                       help="Limit number of symbols")
    p_paf.add_argument("--output-root", dest="output_root", default=None,
                       help="Root for data/import/ (default: project root)")
    p_paf.add_argument("--report-dir", dest="report_dir", default=None,
                       help="Report output directory")
    p_paf.add_argument("--report", action="store_true", default=False,
                       help="Generate fetch report after run")

    # --- data-freshness (v0.3.19) ---
    p_df = subparsers.add_parser(
        "data-freshness",
        help="Check data freshness of standard import datasets (v0.3.19)",
    )
    p_df.add_argument("--dataset", default=None,
                      choices=["daily_k","monthly_revenue","institutional","margin","fundamental","intraday"],
                      help="Check a specific dataset (default: all)")
    p_df.add_argument("--report", action="store_true", default=False,
                      help="Generate freshness report")

    # --- update-data (v0.3.21) ---
    p_ud = subparsers.add_parser(
        "update-data",
        help="Daily data update: provider health + auto fetch + freshness + quality gate (v0.3.21)",
    )
    p_ud.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_ud.add_argument("--profile", choices=["quick", "standard", "full", "gui_only"],
                      default="standard",
                      help="Workflow profile (default: standard)")
    p_ud.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                      help="Skip file writes in data fetch step")

    # --- run-research (v0.3.21) ---
    p_rr = subparsers.add_parser(
        "run-research",
        help="Daily research workflow: quality gate + signal quality + portfolio + auto report (v0.3.21)",
    )
    p_rr.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_rr.add_argument("--profile", choices=["quick", "standard", "full", "gui_only"],
                      default="standard",
                      help="Workflow profile (default: standard)")
    p_rr.add_argument("--stocks", default=None,
                      help="Comma-separated stock symbols for stock reports")
    p_rr.add_argument("--top", dest="top_n", type=int, default=8,
                      help="Number of top candidates (default: 8)")

    # --- daily-workflow (v0.3.21) ---
    p_dw = subparsers.add_parser(
        "daily-workflow",
        help="Full daily workflow: update-data + run-research + optional GUI (v0.3.21)",
    )
    p_dw.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_dw.add_argument("--profile", choices=["quick", "standard", "full", "gui_only"],
                      default="standard",
                      help="Workflow profile (default: standard)")
    p_dw.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                      help="Skip file writes in data fetch step")
    p_dw.add_argument("--open-gui", dest="open_gui", action="store_true", default=False,
                      help="Open cockpit GUI after workflow completes")
    p_dw.add_argument("--stocks", default=None,
                      help="Comma-separated stock symbols for stock reports")
    p_dw.add_argument("--top", dest="top_n", type=int, default=8,
                      help="Number of top candidates (default: 8)")

    # --- open-cockpit (v0.3.21) ---
    p_oc = subparsers.add_parser(
        "open-cockpit",
        help="Open TW Quant Cockpit GUI (alias for cockpit) (v0.3.21)",
    )
    p_oc.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")

    # --- usability-smoke-test (v0.3.22) ---
    p_ust = subparsers.add_parser(
        "usability-smoke-test",
        help="Run CLI + GUI panel smoke tests and check usability (v0.3.22)",
    )
    p_ust.add_argument(
        "--report", action="store_true", default=False,
        help="Also generate a Markdown QA report",
    )

    # --- usability-qa-report (v0.3.22) ---
    subparsers.add_parser(
        "usability-qa-report",
        help="Generate Markdown usability QA report from latest smoke test results (v0.3.22)",
    )

    # --- data-quality-gate (v0.3.20) ---
    p_dqg = subparsers.add_parser(
        "data-quality-gate",
        help="Run data quality gate and production readiness score (v0.3.20)",
    )
    p_dqg.add_argument(
        "--mode", choices=["real", "mock"], default="real",
        help="Data mode (default: real)",
    )
    p_dqg.add_argument(
        "--report", action="store_true", default=False,
        help="Generate Markdown report",
    )
    p_dqg.add_argument(
        "--check-mock", dest="check_mock", action="store_true", default=False,
        help="Only run mock contamination scan",
    )
    p_dqg.add_argument(
        "--import-root", dest="import_root", default=None,
        help="Custom data/import/ root path",
    )
    p_dqg.add_argument(
        "--results-dir", dest="results_dir", default=None,
        help="Custom data/backtest_results/ path",
    )
    p_dqg.add_argument(
        "--report-dir", dest="report_dir", default=None,
        help="Custom output folder for reports",
    )

    # --- version-info (v0.4.0) ---
    subparsers.add_parser(
        "version-info",
        help="Show TW Quant Cockpit version info and safety flags (v0.4.0)",
    )

    # --- stable-release-check (v0.4.0) ---
    p_src = subparsers.add_parser(
        "stable-release-check",
        help="Run v0.4.0 stable release checklist (v0.4.0)",
    )
    p_src.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- regression-suite (v0.4.0) ---
    p_rs = subparsers.add_parser(
        "regression-suite",
        help="Run regression suite — quick or full (v0.4.0)",
    )
    p_rs.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_rs_grp = p_rs.add_mutually_exclusive_group()
    p_rs_grp.add_argument("--quick", action="store_true", default=False,
                           help="Run quick regression suite (default)")
    p_rs_grp.add_argument("--full",  action="store_true", default=False,
                           help="Run full regression suite")

    # --- stable-release-report (v0.4.0) ---
    p_srr = subparsers.add_parser(
        "stable-release-report",
        help="Generate v0.4.0 stable release Markdown report (v0.4.0)",
    )
    p_srr.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- api-token-check (v0.4.1) ---
    subparsers.add_parser(
        "api-token-check",
        help="Check FinMind/API token configuration — read-only (v0.4.1)",
    )

    # --- api-cache-status (v0.4.1) ---
    subparsers.add_parser(
        "api-cache-status",
        help="Show API cache statistics (v0.4.1)",
    )

    # --- api-fetch-diagnostics (v0.4.1) ---
    p_afd = subparsers.add_parser(
        "api-fetch-diagnostics",
        help="Run API fetch diagnostics — provider health and cache status (v0.4.1)",
    )
    p_afd.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- api-cache-cleanup (v0.4.1) ---
    subparsers.add_parser(
        "api-cache-cleanup",
        help="Remove expired API cache entries (v0.4.1)",
    )

    # --- api-fetch-production-report (v0.4.1) ---
    p_afpr = subparsers.add_parser(
        "api-fetch-production-report",
        help="Generate API fetch production report (v0.4.1)",
    )
    p_afpr.add_argument("--mode", choices=["real", "mock"], default="real",
                        help="Data mode (default: real)")

    # --- model-monitoring (v0.4.3) ---
    p_mm = subparsers.add_parser(
        "model-monitoring",
        help="Run Model Monitoring summary (v0.4.3)",
    )
    p_mm.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")

    # --- model-monitoring-report (v0.4.3) ---
    p_mmr = subparsers.add_parser(
        "model-monitoring-report",
        help="Generate Model Monitoring Markdown report (v0.4.3)",
    )
    p_mmr.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_mmr.add_argument("--report-dir", dest="report_dir", default=None,
                       help="Custom output directory for reports")

    # --- model-registry-list (v0.4.3) ---
    subparsers.add_parser(
        "model-registry-list",
        help="List registered ML model metadata (v0.4.3)",
    )

    # --- model-register (v0.4.3) ---
    p_mreg = subparsers.add_parser(
        "model-register",
        help="Register a new ML model metadata entry (v0.4.3)",
    )
    p_mreg.add_argument("--name", default="unnamed_model",
                        help="Model name")
    p_mreg.add_argument("--type", dest="type", default="baseline",
                        help="Model type (e.g. baseline, experimental, rule_based)")
    p_mreg.add_argument("--target", default="label_direction_5d",
                        help="Target label (default: label_direction_5d)")

    # --- prediction-log (v0.4.3) ---
    p_pl = subparsers.add_parser(
        "prediction-log",
        help="Show prediction log summary (v0.4.3)",
    )
    p_pl.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")

    # --- prediction-review (v0.4.3) ---
    p_pr = subparsers.add_parser(
        "prediction-review",
        help="Review prediction hit / miss results (v0.4.3)",
    )
    p_pr.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_pr.add_argument("--horizon", type=int, default=5,
                      help="Label horizon in days (default: 5)")

    # --- drift-check (v0.4.3) ---
    p_dc = subparsers.add_parser(
        "drift-check",
        help="Run feature / prediction drift check (v0.4.3)",
    )
    p_dc.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")

    # --- signal-degradation (v0.4.3) ---
    p_sd = subparsers.add_parser(
        "signal-degradation",
        help="Run signal degradation check (v0.4.3)",
    )
    p_sd.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")

    # --- rule-vs-ml (v0.4.3) ---
    p_rvm = subparsers.add_parser(
        "rule-vs-ml",
        help="Run rule vs ML signal comparison (v0.4.3)",
    )
    p_rvm.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- ml-feature-catalog (v0.4.2) ---
    subparsers.add_parser(
        "ml-feature-catalog",
        help="List all ML feature definitions from the feature catalog (v0.4.2)",
    )

    # --- ml-feature-snapshot (v0.4.2) ---
    p_mfs = subparsers.add_parser(
        "ml-feature-snapshot",
        help="Build ML feature snapshot from research data (v0.4.2)",
    )
    p_mfs.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_mfs.add_argument("--symbols", nargs="*", default=None,
                       help="Stock symbols (default: full universe)")
    p_mfs.add_argument("--start-date", dest="start_date", default=None,
                       help="Start date YYYY-MM-DD")
    p_mfs.add_argument("--end-date", dest="end_date", default=None,
                       help="End date YYYY-MM-DD")

    # --- ml-labels (v0.4.2) ---
    p_mll = subparsers.add_parser(
        "ml-labels",
        help="Generate ML forward return and classification labels (v0.4.2)",
    )
    p_mll.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_mll.add_argument("--horizons", default=None,
                       help="Comma-separated label horizons in days, e.g. 1,5,10,20")

    # --- ml-build-dataset (v0.4.2) ---
    p_mbd = subparsers.add_parser(
        "ml-build-dataset",
        help="Build model-ready ML dataset: features + labels + split (v0.4.2)",
    )
    p_mbd.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_mbd.add_argument("--symbols", nargs="*", default=None,
                       help="Stock symbols (default: full universe)")
    p_mbd.add_argument("--start-date", dest="start_date", default=None,
                       help="Start date YYYY-MM-DD")
    p_mbd.add_argument("--end-date", dest="end_date", default=None,
                       help="End date YYYY-MM-DD")
    p_mbd.add_argument("--horizons", default=None,
                       help="Comma-separated label horizons in days, e.g. 5,10,20")
    p_mbd.add_argument("--output-root", dest="output_root", default=None,
                       help="Custom output directory for ML datasets")

    # --- ml-leakage-check (v0.4.2) ---
    p_mlc = subparsers.add_parser(
        "ml-leakage-check",
        help="Run data leakage check on the latest ML dataset (v0.4.2)",
    )
    p_mlc.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- ml-feature-quality (v0.4.2) ---
    p_mfq = subparsers.add_parser(
        "ml-feature-quality",
        help="Run feature quality check on the latest ML dataset (v0.4.2)",
    )
    p_mfq.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- ml-feature-importance (v0.4.2) ---
    p_mfi = subparsers.add_parser(
        "ml-feature-importance",
        help="Run feature importance shell on the latest ML dataset (v0.4.2)",
    )
    p_mfi.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_mfi.add_argument("--target", default="label_direction_5d",
                       help="Target label column (default: label_direction_5d)")

    # --- ml-feature-store-report (v0.4.2) ---
    p_mfsr = subparsers.add_parser(
        "ml-feature-store-report",
        help="Generate ML Feature Store Markdown report (v0.4.2)",
    )
    p_mfsr.add_argument("--mode", choices=["real", "mock"], default="real",
                        help="Data mode (default: real)")
    p_mfsr.add_argument("--report-dir", dest="report_dir", default=None,
                        help="Custom output directory for reports")

    # --- intraday-replay (v0.4.4) ---
    p_ir = subparsers.add_parser(
        "intraday-replay",
        help="Step through intraday 1min/5min bars in replay mode (v0.4.4)",
    )
    p_ir.add_argument("--mode",  choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_ir.add_argument("--stock", default=None, help="Stock symbol to replay")
    p_ir.add_argument("--freq",  choices=["1min", "5min"], default="1min",
                      help="Bar frequency (default: 1min)")
    p_ir.add_argument("--steps", type=int, default=30,
                      help="Number of bars to replay (default: 30)")
    p_ir.add_argument("--date",  default=None, help="Replay date YYYY-MM-DD (default: latest)")

    # --- intraday-replay-report (v0.4.4) ---
    p_irr = subparsers.add_parser(
        "intraday-replay-report",
        help="Generate Intraday Replay Cockpit Markdown report (v0.4.4)",
    )
    p_irr.add_argument("--mode",       choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_irr.add_argument("--report-dir", dest="report_dir", default=None,
                       help="Custom output directory for reports")

    # --- replay-session-list (v0.4.4) ---
    p_rsl = subparsers.add_parser(
        "replay-session-list",
        help="List replay training sessions (v0.4.4)",
    )
    p_rsl.add_argument("--limit", type=int, default=20,
                       help="Max sessions to show (default: 20)")

    # --- replay-session-show (v0.4.4) ---
    p_rss = subparsers.add_parser(
        "replay-session-show",
        help="Show detail for a single replay session (v0.4.4)",
    )
    p_rss.add_argument("--id", default=None, help="Session ID (REPLAY-YYYYMMDD-HHMMSS-XXXXXX)")

    # --- replay-training-summary (v0.4.4) ---
    p_rts = subparsers.add_parser(
        "replay-training-summary",
        help="Show replay training summary: quiz accuracy, grade (v0.4.4)",
    )
    p_rts.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- strategy-knowledge-ingest (v0.4.1.1) ---
    p_ski = subparsers.add_parser(
        "strategy-knowledge-ingest",
        help="Ingest transcripts and extract strategy knowledge items (v0.4.1.1)",
    )
    p_ski.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_ski.add_argument("--input-dir", dest="input_dir", default=None,
                       help="Input directory for transcripts (comma-separated or repeated; default: knowledge/transcripts)")
    p_ski.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                       help="Discover and extract but do not write output files")
    p_ski.add_argument("--report", action="store_true", default=False,
                       help="Generate Markdown report after ingestion")
    p_ski.add_argument("--output-dir", dest="output_dir",
                       default="data/backtest_results/strategy_knowledge",
                       help="Output directory for CSVs (default: data/backtest_results/strategy_knowledge)")
    p_ski.add_argument("--report-dir", dest="report_dir", default="reports",
                       help="Output directory for report (default: reports)")

    # --- strategy-knowledge-summary (v0.4.1.1) ---
    p_sks = subparsers.add_parser(
        "strategy-knowledge-summary",
        help="Show latest Strategy Knowledge Ingestion summary (v0.4.1.1)",
    )
    p_sks.add_argument("--output-dir", dest="output_dir",
                       default="data/backtest_results/strategy_knowledge",
                       help="Knowledge store output directory (default: data/backtest_results/strategy_knowledge)")

    # --- ml-knowledge-integrate (v0.4.2.1) ---
    p_mki = subparsers.add_parser(
        "ml-knowledge-integrate",
        help="Integrate transcript-derived knowledge into ML Feature Store (v0.4.2.1)",
    )
    p_mki.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_mki.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                       help="Show candidates without writing output files")
    p_mki.add_argument("--report", action="store_true", default=False,
                       help="Generate Markdown report after integration")
    p_mki.add_argument("--knowledge-dir", dest="knowledge_dir",
                       default="data/backtest_results/strategy_knowledge",
                       help="Strategy knowledge output directory (v0.4.1.1 CSVs)")
    p_mki.add_argument("--output-dir", dest="output_dir",
                       default="data/backtest_results/ml_feature_store",
                       help="ML feature store output directory")

    # --- ml-knowledge-leakage-check (v0.4.2.1) ---
    p_mkl = subparsers.add_parser(
        "ml-knowledge-leakage-check",
        help="Check transcript-derived knowledge features for data leakage (v0.4.2.1)",
    )
    p_mkl.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")
    p_mkl.add_argument("--output-dir", dest="output_dir",
                       default="data/backtest_results/ml_feature_store",
                       help="ML feature store output directory")

    # --- ml-knowledge-feature-summary (v0.4.2.1) ---
    p_mkfs = subparsers.add_parser(
        "ml-knowledge-feature-summary",
        help="Show latest ML knowledge integration summary (v0.4.2.1)",
    )
    p_mkfs.add_argument("--output-dir", dest="output_dir",
                        default="data/backtest_results/ml_feature_store",
                        help="ML feature store output directory")

    # --- journal-add (v0.4.6) ---
    p_ja = subparsers.add_parser("journal-add",
        help="Add a research-only portfolio journal entry (v0.4.6)")
    p_ja.add_argument("--symbol", default="", help="Stock symbol (e.g. 2330)")
    p_ja.add_argument("--entry-type", dest="entry_type", default="simulated_trade",
                      choices=["simulated_trade","paper_trade","replay_note",
                               "signal_review","portfolio_review","manual_note"])
    p_ja.add_argument("--timeframe", default="", help="Timeframe (e.g. daily, 60min)")
    p_ja.add_argument("--signal-source", dest="signal_source", default="")
    p_ja.add_argument("--planned-entry", dest="planned_entry", type=float, default=None)
    p_ja.add_argument("--planned-stop",  dest="planned_stop",  type=float, default=None)
    p_ja.add_argument("--planned-target",dest="planned_target",type=float, default=None)
    p_ja.add_argument("--reason", default="", help="Short reason for entry")
    p_ja.add_argument("--thesis", default="", help="Research thesis / hypothesis")
    p_ja.add_argument("--invalidation", default="", help="Invalidation condition")
    p_ja.add_argument("--mode", choices=["real","mock"], default="real")

    # --- journal-list (v0.4.6) ---
    p_jl = subparsers.add_parser("journal-list",
        help="List recent portfolio journal entries (v0.4.6)")
    p_jl.add_argument("--limit",  type=int, default=20)
    p_jl.add_argument("--symbol", default=None)
    p_jl.add_argument("--status", default=None)
    p_jl.add_argument("--mode",   choices=["real","mock"], default="real")

    # --- journal-show (v0.4.6) ---
    p_js = subparsers.add_parser("journal-show",
        help="Show detail for a single journal entry (v0.4.6)")
    p_js.add_argument("--id",   required=False, default="", help="Journal ID (JOURNAL-xxxx)")
    p_js.add_argument("--mode", choices=["real","mock"], default="real")

    # --- journal-review (v0.4.6) ---
    p_jr = subparsers.add_parser("journal-review",
        help="Update outcome / notes / mistake tags for a journal entry (v0.4.6)")
    p_jr.add_argument("--id",      required=False, default="", help="Journal ID")
    p_jr.add_argument("--outcome", default="", help="Outcome label (WIN/LOSS/…)")
    p_jr.add_argument("--notes",   default="", help="Review notes")
    p_jr.add_argument("--mistake-tags", dest="mistake_tags", default="",
                      help="Comma-separated mistake tags")
    p_jr.add_argument("--mode", choices=["real","mock"], default="real")

    # --- journal-report (v0.4.6) ---
    p_jrp = subparsers.add_parser("journal-report",
        help="Generate Portfolio Journal Markdown report (v0.4.6)")
    p_jrp.add_argument("--mode",    choices=["real","mock"], default="real")
    p_jrp.add_argument("--dry-run", dest="dry_run", action="store_true", default=False)

    # --- journal-summary (v0.4.6) ---
    p_jsum = subparsers.add_parser("journal-summary",
        help="Show portfolio journal statistics summary (v0.4.6)")
    p_jsum.add_argument("--mode", choices=["real","mock"], default="real")

    # --- journal-link-replay (v0.4.6) ---
    p_jlr = subparsers.add_parser("journal-link-replay",
        help="Link a journal entry to a replay session (v0.4.6)")
    p_jlr.add_argument("--id",             required=False, default="", help="Journal ID")
    p_jlr.add_argument("--replay-session", dest="replay_session", default="")
    p_jlr.add_argument("--mode", choices=["real","mock"], default="real")

    # --- notification-scan (v0.4.5) ---
    p_ns = subparsers.add_parser(
        "notification-scan",
        help="Evaluate notification rules and persist generated events (v0.4.5)",
    )
    p_ns.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")

    # --- notification-list (v0.4.5) ---
    p_nl = subparsers.add_parser(
        "notification-list",
        help="List recent notification events (v0.4.5)",
    )
    p_nl.add_argument("--limit", type=int, default=50,
                      help="Maximum events to show (default: 50)")
    p_nl.add_argument("--severity", default=None,
                      help="Filter by minimum severity (INFO/NOTICE/WARNING/ERROR/CRITICAL)")
    p_nl.add_argument("--category", default=None,
                      help="Filter by category (report/data/provider/signal/ml/…)")
    p_nl.add_argument("--unread-only", dest="unread_only", action="store_true", default=False,
                      help="Show unread notifications only")

    # --- notification-report (v0.4.5) ---
    p_nr = subparsers.add_parser(
        "notification-report",
        help="Generate Notification Center Markdown report (v0.4.5)",
    )
    p_nr.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_nr.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                      help="Show report path without writing file")

    # --- notification-clear-read (v0.4.5) ---
    subparsers.add_parser(
        "notification-clear-read",
        help="Clear all read notifications from the log (v0.4.5)",
    )

    # --- notification-test (v0.4.5) ---
    p_nt = subparsers.add_parser(
        "notification-test",
        help="Add a test notification event (v0.4.5)",
    )
    p_nt.add_argument("--severity", default="INFO",
                      help="Severity level for test notification (default: INFO)")

    # --- experiment-create (v0.3.29) ---
    p_ec = subparsers.add_parser(
        "experiment-create",
        help="Create a new experiment entry in the Experiment Registry (v0.3.29)",
    )
    p_ec.add_argument("--name",    default=None,           help="Experiment name")
    p_ec.add_argument("--type",    default="daily_research",
                      choices=["daily_research", "hardened_backtest", "signal_quality",
                               "rule_weight_tuning", "intraday_research", "universe_research",
                               "portfolio_simulation", "manual_note"],
                      help="Experiment type (default: daily_research)")
    p_ec.add_argument("--mode",    choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_ec.add_argument("--profile", default="standard",     help="Research profile (default: standard)")
    p_ec.add_argument("--tags",    default=None,           help="Comma-separated tags")
    p_ec.add_argument("--notes",   default=None,           help="Experiment notes")

    # --- experiment-register-latest (v0.3.29) ---
    p_erl = subparsers.add_parser(
        "experiment-register-latest",
        help="Register the latest research run outputs to the most recent experiment (v0.3.29)",
    )
    p_erl.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- experiment-list (v0.3.29) ---
    p_el = subparsers.add_parser(
        "experiment-list",
        help="List experiments in the Experiment Registry (v0.3.29)",
    )
    p_el.add_argument("--status", default=None,
                      help="Filter by status (CREATED, RUNNING, COMPLETED, PARTIAL, FAILED, ARCHIVED)")
    p_el.add_argument("--type",   default=None, help="Filter by experiment type")
    p_el.add_argument("--limit",  type=int, default=20, help="Max experiments to show (default: 20)")

    # --- experiment-show (v0.3.29) ---
    p_es = subparsers.add_parser(
        "experiment-show",
        help="Show experiment detail (v0.3.29)",
    )
    p_es.add_argument("--id", default=None, help="Experiment ID (use 'latest' for most recent)")

    # --- experiment-notebook (v0.3.29) ---
    p_en = subparsers.add_parser(
        "experiment-notebook",
        help="Build experiment notebook.md (v0.3.29)",
    )
    p_en.add_argument("--id", default=None, help="Experiment ID (use 'latest' for most recent)")

    # --- experiment-compare (v0.3.29) ---
    p_ecmp = subparsers.add_parser(
        "experiment-compare",
        help="Compare two or more experiments (v0.3.29)",
    )
    p_ecmp.add_argument("--ids", default=None,
                        help="Comma-separated experiment IDs, e.g. EXP-aaa,EXP-bbb")

    # --- experiment-report (v0.3.29) ---
    subparsers.add_parser(
        "experiment-report",
        help="Generate Experiment Registry Markdown report (v0.3.29)",
    )

    # --- experiment-snapshot (v0.3.29) ---
    p_esnap = subparsers.add_parser(
        "experiment-snapshot",
        help="Build all snapshots for an experiment (v0.3.29)",
    )
    p_esnap.add_argument("--id", default=None, help="Experiment ID (use 'latest' for most recent)")

    # --- rule-governance (v0.3.28) ---
    p_rg = subparsers.add_parser(
        "rule-governance",
        help="Strategy Rule Governance — registry, confidence, dependency, report, snapshot (v0.3.28)",
    )
    p_rg.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_rg.add_argument("--category", default=None,
                      help="Filter by category (buy_point, screener, intraday, portfolio, ...)")
    p_rg.add_argument("--status", default=None,
                      help="Filter by status (ACTIVE, EXPERIMENTAL, NEEDS_REVIEW, ...)")
    p_rg.add_argument("--report", action="store_true", default=False,
                      help="Generate Markdown governance report")
    p_rg.add_argument("--snapshot", action="store_true", default=False,
                      help="Export rule snapshot JSON + CSV")
    p_rg.add_argument("--results-dir", dest="results_dir", default="data/backtest_results",
                      help="Backtest results directory (default: data/backtest_results/)")
    p_rg.add_argument("--report-dir", dest="report_dir", default="reports",
                      help="Output directory for report (default: reports/)")

    # --- intraday-pipeline (v0.3.27) ---
    p_ip = subparsers.add_parser(
        "intraday-pipeline",
        help="Run intraday data standardization pipeline (v0.3.27)",
    )
    p_ip.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_ip.add_argument("--freq", choices=["1min", "5min"], default="1min",
                      help="Bar frequency to process (default: 1min)")
    p_ip.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                      help="Check only, do not write standardized files")
    p_ip.add_argument("--report", action="store_true", default=False,
                      help="Generate intraday pipeline Markdown report after run")
    p_ip.add_argument("--report-dir", dest="report_dir", default="reports",
                      help="Output directory for report (default: reports/)")

    # --- intraday-quality (v0.3.27) ---
    p_iq = subparsers.add_parser(
        "intraday-quality",
        help="Check intraday data quality for standardized files (v0.3.27)",
    )
    p_iq.add_argument("--freq", choices=["1min", "5min"], default=None,
                      help="Filter by frequency (default: all)")

    # --- intraday-features (v0.3.27) ---
    p_if = subparsers.add_parser(
        "intraday-features",
        help="Preview intraday features (opening range, VWAP, fake breakout) for a stock (v0.3.27)",
    )
    p_if.add_argument("--stock", required=True,
                      help="Stock symbol, e.g. 2454")
    p_if.add_argument("--freq", choices=["1min", "5min"], default="1min",
                      help="Bar frequency (default: 1min)")

    # --- universe-list (v0.3.25) ---
    subparsers.add_parser(
        "universe-list",
        help="List all available universe groups (v0.3.25)",
    )

    # --- universe-build-defaults (v0.3.25) ---
    p_ubd = subparsers.add_parser(
        "universe-build-defaults",
        help="Build default universe CSV files from seed data (v0.3.25)",
    )
    p_ubd.add_argument("--force", action="store_true", default=False,
                       help="Rebuild universes even if CSV files already exist")

    # --- universe-show (v0.3.25) ---
    p_us = subparsers.add_parser(
        "universe-show",
        help="Show symbols and sector summary for a universe group (v0.3.25)",
    )
    p_us.add_argument("--universe", default="core_30",
                      help="Universe group name (default: core_30)")

    # --- universe-quality-score (v0.3.25) ---
    p_uqs = subparsers.add_parser(
        "universe-quality-score",
        help="Compute Universe Quality Score for a universe group (v0.3.25)",
    )
    p_uqs.add_argument("--universe", default="core_30",
                       help="Universe group name (default: core_30)")
    p_uqs.add_argument("--mode", choices=["real", "mock"], default="real",
                       help="Data mode (default: real)")

    # --- universe-expand (v0.3.25) ---
    p_ue = subparsers.add_parser(
        "universe-expand",
        help="Propose expansion candidates for a universe (read-only) (v0.3.25)",
    )
    p_ue.add_argument("--from", dest="from_universe", default="core_30",
                      help="Source universe group (default: core_30)")
    p_ue.add_argument("--target-size", dest="target_size", type=int, default=50,
                      help="Target symbol count (default: 50)")

    # --- universe-report (v0.3.25) ---
    p_ur = subparsers.add_parser(
        "universe-report",
        help="Generate Universe Expansion Markdown report (v0.3.25)",
    )
    p_ur.add_argument("--universe", default="core_30",
                      help="Universe group name (default: core_30)")
    p_ur.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_ur.add_argument("--report-dir", dest="report_dir", default="reports",
                      help="Custom output folder for reports")

    # --- provider-reliability (v0.3.24) ---
    p_prel = subparsers.add_parser(
        "provider-reliability",
        help="Provider Reliability & Fallback Matrix (v0.3.24)",
    )
    p_prel.add_argument("--mode", choices=["real", "mock"], default="real",
                        help="Data mode (default: real)")
    p_prel.add_argument("--report", action="store_true", default=False,
                        help="Generate provider reliability Markdown report")
    p_prel.add_argument("--refresh", action="store_true", default=False,
                        help="Force refresh reliability matrix")
    p_prel.add_argument("--dataset", default=None,
                        help="Filter output to a specific dataset")
    p_prel.add_argument("--provider", default=None,
                        help="Filter output to a specific provider")
    p_prel.add_argument("--results-dir", dest="results_dir", default="data/backtest_results",
                        help="Custom data/backtest_results/ path")
    p_prel.add_argument("--report-dir", dest="report_dir", default="reports",
                        help="Custom output folder for reports")

    # --- provider-health (v0.3.18) ---
    p_ph = subparsers.add_parser(
        "provider-health",
        help="Check API provider health, token status, and capability matrix (v0.3.18)",
    )
    p_ph.add_argument(
        "--report", action="store_true", default=False,
        help="Generate provider health Markdown report",
    )
    p_ph.add_argument(
        "--create-env-example", dest="create_env_example",
        action="store_true", default=False,
        help="Create safe .env.example template (no real tokens)",
    )
    p_ph.add_argument(
        "--provider", default="all",
        help="Provider to check (csv/xq_export/finmind/twse/tpex/mops/mega_readonly_planned/all)",
    )

    # --- scheduler-run (v0.3.17) ---
    p_sr = subparsers.add_parser(
        "scheduler-run",
        help="Run a single automation task once (v0.3.17)",
    )
    p_sr.add_argument("--task",    required=True,
                      choices=[
                          "daily_data_update", "daily_validation", "daily_auto_report",
                          "weekly_signal_quality", "weekly_rule_weight_tuning",
                          "monthly_universe_quality",
                      ],
                      help="Task name to run")
    p_sr.add_argument("--mode",    default="real", choices=["mock", "real"],
                      help="Data mode (default: real)")
    p_sr.add_argument("--config",  default=None,
                      help="Path to scheduler config YAML")
    p_sr.add_argument("--log-dir", dest="log_dir", default=None,
                      help="Automation log directory (default: logs/automation/)")

    # --- auto-report (v0.3.16) ---
    p_ar16 = subparsers.add_parser(
        "auto-report",
        help="One-click daily research report pack (v0.3.16)",
    )
    p_ar16.add_argument("--mode",        default="real", choices=["mock", "real"],
                        help="Data mode (default: real)")
    p_ar16.add_argument("--profile",     default="full",
                        choices=["full", "daily", "portfolio", "signal", "stock", "universe"],
                        help="Report profile (default: full)")
    p_ar16.add_argument("--stocks",      nargs="+", default=None,
                        help="Specific stock symbols for stock reports")
    p_ar16.add_argument("--top",         dest="top", type=int, default=8,
                        help="Number of top candidates in summaries (default: 8)")
    p_ar16.add_argument("--output-dir",  dest="output_dir",  default=None,
                        help="Output root folder (default: reports/auto_report_center/)")
    p_ar16.add_argument("--results-dir", dest="results_dir", default=None,
                        help="Backtest results directory (default: data/backtest_results/)")
    p_ar16.add_argument("--report-date", dest="report_date", default=None,
                        help="Report date YYYY-MM-DD (default: today)")

    # --- tune-rule-weights (v0.3.15) ---
    p_rw15 = subparsers.add_parser(
        "tune-rule-weights",
        help="Compare 7 scoring weight configurations via portfolio simulation (v0.3.15)",
    )
    p_rw15.add_argument("--mode",     default="real", choices=["mock", "real"],
                        help="Data mode (default: real)")
    p_rw15.add_argument("--config",   default="all",
                        help="Config name to evaluate, or 'all' for all 7 (default: all)")
    p_rw15.add_argument("--initial-capital", dest="initial_capital", type=float,
                        default=1_000_000,
                        help="Starting capital in NTD (default: 1000000)")
    p_rw15.add_argument("--start",    default=None, help="Start date YYYY-MM-DD (optional)")
    p_rw15.add_argument("--end",      default=None, help="End date YYYY-MM-DD (optional)")
    p_rw15.add_argument("--report",   action="store_true", default=False,
                        help="Generate Markdown report after tuning")
    p_rw15.add_argument("--results-dir", dest="results_dir", default=None,
                        help="Output directory for CSVs (default: data/backtest_results/)")
    p_rw15.add_argument("--report-dir", dest="report_dir", default=None,
                        help="Output directory for report (default: reports/")

    # --- hardened-backtest (v0.3.26) ---
    p_hb = subparsers.add_parser(
        "hardened-backtest",
        help="Hardened backtest with realistic entry, cost, liquidity, gap, split, regime (v0.3.26)",
    )
    p_hb.add_argument("--mode", choices=["real", "mock"], default="real",
                      help="Data mode (default: real)")
    p_hb.add_argument("--entry-model", dest="entry_model",
                      choices=["signal_close", "next_open", "next_close", "vwap_proxy"],
                      default="next_open",
                      help="Entry price model (default: next_open)")
    p_hb.add_argument("--exit-model", dest="exit_model",
                      choices=["fixed_holding_days", "combined", "stop_loss", "take_profit", "trailing_stop", "time_stop"],
                      default="combined",
                      help="Exit model (default: combined)")
    p_hb.add_argument("--cost-model", dest="cost_model",
                      choices=["taiwan_realistic", "zero"],
                      default="taiwan_realistic",
                      help="Cost model (default: taiwan_realistic)")
    p_hb.add_argument("--split-method", dest="split_method",
                      choices=["in_sample_only", "out_of_sample", "walk_forward", "expanding_window"],
                      default="walk_forward",
                      help="Validation split method (default: walk_forward)")
    p_hb.add_argument("--max-holding-days", dest="max_holding_days", type=int, default=20,
                      help="Maximum holding days per trade (default: 20)")
    p_hb.add_argument("--no-liquidity-filter", dest="no_liquidity_filter",
                      action="store_true", default=False,
                      help="Disable liquidity filter")
    p_hb.add_argument("--no-gap-risk", dest="no_gap_risk",
                      action="store_true", default=False,
                      help="Disable gap risk model")
    p_hb.add_argument("--zero-cost", dest="zero_cost",
                      action="store_true", default=False,
                      help="Use zero-cost model (for comparison with old backtests)")
    p_hb.add_argument("--report", action="store_true", default=False,
                      help="Generate Markdown report after backtest")
    p_hb.add_argument("--results-dir", dest="results_dir", default="data/backtest_results",
                      help="Output directory for result CSVs")
    p_hb.add_argument("--report-dir", dest="report_dir", default="reports",
                      help="Output directory for report")

    # --- backtest-long-term-strategy (v0.3.11) ---
    p_blts = subparsers.add_parser(
        "backtest-long-term-strategy",
        help="Validate long-term strategy rules against historical forward returns (v0.3.11)",
    )
    p_blts.add_argument("--mode",         default="real", choices=["mock", "real"],
                        help="Data mode (default: real)")
    p_blts.add_argument("--stock",        default=None,
                        help="Single symbol (optional; default: all universe)")
    p_blts.add_argument("--holding-days", dest="holding_days", type=int, default=60,
                        help="Forward return window in trading bars (default: 60)")
    p_blts.add_argument("--output-dir",   dest="output_dir",  default=None,
                        help="Output directory for CSV results (default: data/backtest_results/)")
    p_blts.add_argument("--report-dir",   dest="report_dir",  default=None,
                        help="Output directory for Markdown report (default: reports/)")

    # --- fetch-daily-history (v0.3.10) ---
    p_fdh = subparsers.add_parser(
        "fetch-daily-history",
        help="Fetch historical daily OHLCV from FinMind and merge into daily_k.csv (v0.3.10)",
    )
    grp_fdh = p_fdh.add_mutually_exclusive_group(required=True)
    grp_fdh.add_argument("--stocks", nargs="+", default=None,
                         help="One or more stock symbols, e.g. --stocks 2454 2330 2383")
    grp_fdh.add_argument("--universe", type=int, choices=[10, 30, 50], default=None,
                         help="Fetch for universe of N stocks")
    p_fdh.add_argument("--years",    type=float, default=3.0,
                       help="Years of history to fetch (default: 3)")
    p_fdh.add_argument("--dry-run",  action="store_true", dest="dry_run",
                       help="Fetch only, do not write CSV files")

    # --- fetch-public-data (v0.3.9) ---
    p_fpd = subparsers.add_parser(
        "fetch-public-data",
        help="Fetch public data (monthly revenue, fundamentals, institutional, margin) via API/crawler",
    )
    grp_fpd = p_fpd.add_mutually_exclusive_group(required=True)
    grp_fpd.add_argument("--stock",    default=None, help="Single stock symbol, e.g. 2454")
    grp_fpd.add_argument("--universe", type=int, choices=[10, 30, 50], default=None,
                         help="Fetch for universe of N stocks")
    grp_fpd.add_argument("--manifest", default=None, help="Path to universe_manifest.csv")
    p_fpd.add_argument("--months",   type=int, default=24, help="Months of revenue history (default: 24)")
    p_fpd.add_argument("--source",   default="auto",
                       choices=["auto", "finmind", "twse", "tpex", "mops"],
                       help="Data source (default: auto — tries all in fallback order)")
    p_fpd.add_argument("--all-sources", dest="all_sources", action="store_true",
                       help="Try all sources (same as --source auto)")
    p_fpd.add_argument("--dry-run",  action="store_true", dest="dry_run",
                       help="Fetch only, do not write CSV files")
    p_fpd.add_argument("--replace",  action="store_true",
                       help="Replace existing data (default: append and deduplicate)")

    # --- import-intraday (v0.3.9) ---
    p_ii = subparsers.add_parser(
        "import-intraday",
        help="Import XQ 1min / 5min intraday data to data/import/intraday/",
    )
    grp_ii = p_ii.add_mutually_exclusive_group(required=True)
    grp_ii.add_argument("--folder", default=None, help="Folder containing intraday CSV/Excel files")
    grp_ii.add_argument("--file",   default=None, help="Single intraday CSV/Excel file")
    p_ii.add_argument("--symbol",  default=None, help="Symbol (required with --file if not in filename)")
    p_ii.add_argument("--freq",    default="1min", choices=["1min", "5min"],
                      help="Bar frequency (default: 1min)")
    p_ii.add_argument("--dry-run", action="store_true", dest="dry_run",
                      help="Check only, do not write files")
    p_ii.add_argument("--replace", action="store_true",
                      help="Replace existing intraday CSV")

    # --- data-source-status (v0.3.9) ---
    subparsers.add_parser(
        "data-source-status",
        help="Show comprehensive data source status including public API, intraday, and tick/bidask",
    )

    # --- enrich-universe-data (v0.3.9) ---
    p_eud = subparsers.add_parser(
        "enrich-universe-data",
        help="Batch-fetch public data for all universe symbols and update quality (v0.3.9)",
    )
    grp_eud = p_eud.add_mutually_exclusive_group(required=False)
    grp_eud.add_argument("--universe", type=int, choices=[10, 30, 50], default=None,
                         help="Universe size to enrich")
    grp_eud.add_argument("--manifest", default=None, help="Path to universe_manifest.csv")
    p_eud.add_argument("--months",   type=int, default=24, help="Months of revenue history (default: 24)")
    p_eud.add_argument("--dry-run",  action="store_true", dest="dry_run",
                       help="Fetch only, do not write CSV files")

    # ---- v0.4.7 Research Review Dashboard ----

    p_rr = subparsers.add_parser(
        "research-review",
        help="Run Research Review Dashboard (daily/weekly aggregation) (v0.4.7)",
    )
    p_rr.add_argument("--mode",   default="real", choices=["real", "mock"],
                      help="Data mode: real or mock (default: real)")
    p_rr.add_argument("--period", default="daily", choices=["daily", "weekly"],
                      help="Review period: daily or weekly (default: daily)")
    p_rr.add_argument("--output-dir", default="data/backtest_results/research_review",
                      dest="output_dir", help="Output directory for review data")
    p_rr.add_argument("--report-dir", default="reports",
                      dest="report_dir", help="Report directory")

    p_rrr = subparsers.add_parser(
        "research-review-report",
        help="Generate Research Review Dashboard Markdown report (v0.4.7)",
    )
    p_rrr.add_argument("--mode",   default="real", choices=["real", "mock"])
    p_rrr.add_argument("--period", default="daily", choices=["daily", "weekly"])
    p_rrr.add_argument("--report-dir", default="reports", dest="report_dir")

    p_rrs = subparsers.add_parser(
        "research-review-summary",
        help="Show latest Research Review Dashboard summary (v0.4.7)",
    )
    p_rrs.add_argument("--output-dir", default="data/backtest_results/research_review",
                       dest="output_dir")

    p_rra = subparsers.add_parser(
        "research-review-actions",
        help="Show latest Research Review action plan (v0.4.7)",
    )
    p_rra.add_argument("--output-dir", default="data/backtest_results/research_review",
                       dest="output_dir")

    # --- v0.4.8 Research Assistant / Coach ---
    p_rc = subparsers.add_parser(
        "research-coach",
        help="Run Research Assistant / Coach (v0.4.8)",
    )
    p_rc.add_argument("--mode",   default="real",  choices=["real", "mock"])
    p_rc.add_argument("--period", default="daily", choices=["daily", "weekly"])
    p_rc.add_argument("--output-dir", default="data/backtest_results/research_coach",
                      dest="output_dir")
    p_rc.add_argument("--report-dir", default="reports", dest="report_dir")

    p_rcr = subparsers.add_parser(
        "research-coach-report",
        help="Generate Research Coach Markdown report (v0.4.8)",
    )
    p_rcr.add_argument("--mode",   default="real",  choices=["real", "mock"])
    p_rcr.add_argument("--period", default="daily", choices=["daily", "weekly"])
    p_rcr.add_argument("--report-dir", default="reports", dest="report_dir")

    p_rcs = subparsers.add_parser(
        "research-coach-summary",
        help="Show latest Research Coach summary (v0.4.8)",
    )
    p_rcs.add_argument("--output-dir", default="data/backtest_results/research_coach",
                       dest="output_dir")

    p_rcc = subparsers.add_parser(
        "research-coach-checklist",
        help="Show latest Research Coach daily checklist (v0.4.8)",
    )
    p_rcc.add_argument("--output-dir", default="data/backtest_results/research_coach",
                       dest="output_dir")

    p_rcrp = subparsers.add_parser(
        "research-coach-replay-plan",
        help="Show latest Replay Training Plan (v0.4.8)",
    )
    p_rcrp.add_argument("--output-dir", default="data/backtest_results/research_coach",
                        dest="output_dir")

    p_rcrq = subparsers.add_parser(
        "research-coach-rule-queue",
        help="Show latest Rule Review Queue (v0.4.8)",
    )
    p_rcrq.add_argument("--output-dir", default="data/backtest_results/research_coach",
                        dest="output_dir")

    p_rcdr = subparsers.add_parser(
        "research-coach-data-repair",
        help="Show latest Data Repair Plan (v0.4.8)",
    )
    p_rcdr.add_argument("--output-dir", default="data/backtest_results/research_coach",
                        dest="output_dir")

    # ---- v0.4.9 Research Workflow Automation ----

    p_rw = subparsers.add_parser(
        "research-workflow",
        help="Run Research Workflow Automation (v0.4.9)",
    )
    p_rw.add_argument("--mode",   default="real", choices=["real", "mock"])
    p_rw.add_argument("--type",   default="daily_research",
                      choices=["daily_research", "weekly_review", "data_repair",
                               "rule_review", "replay_training", "safety_check"],
                      dest="type", help="Workflow type (default: daily_research)")
    p_rw.add_argument("--dry-run", action="store_true", default=False,
                      dest="dry_run", help="List tasks only, do not execute")
    p_rw.add_argument("--output-dir", default="data/backtest_results/research_workflow",
                      dest="output_dir")
    p_rw.add_argument("--report-dir", default="reports", dest="report_dir")

    p_rwrpt = subparsers.add_parser(
        "research-workflow-report",
        help="Generate Research Workflow Automation Markdown report (v0.4.9)",
    )
    p_rwrpt.add_argument("--mode",       default="real", choices=["real", "mock"])
    p_rwrpt.add_argument("--report-dir", default="reports", dest="report_dir")
    p_rwrpt.add_argument("--output-dir", default="data/backtest_results/research_workflow",
                         dest="output_dir")

    p_rwsum = subparsers.add_parser(
        "research-workflow-summary",
        help="Show latest Research Workflow Automation summary (v0.4.9)",
    )
    p_rwsum.add_argument("--output-dir", default="data/backtest_results/research_workflow",
                         dest="output_dir")

    p_rwtasks = subparsers.add_parser(
        "research-workflow-tasks",
        help="List latest Research Workflow tasks (v0.4.9)",
    )
    p_rwtasks.add_argument("--output-dir", default="data/backtest_results/research_workflow",
                           dest="output_dir")

    p_rwpkg = subparsers.add_parser(
        "research-workflow-package",
        help="Generate / show Research Workflow package (v0.4.9)",
    )
    p_rwpkg.add_argument("--type",       default="daily_research",
                         choices=["daily_research", "weekly_review"],
                         dest="type", help="Package type (default: daily_research)")
    p_rwpkg.add_argument("--output-dir", default="data/backtest_results/research_workflow",
                         dest="output_dir")
    p_rwpkg.add_argument("--report-dir", default="reports", dest="report_dir")

    return parser


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    """Main entrypoint."""
    import pandas as pd  # imported here to avoid shadowing at module level

    # Make pd available in cmd_pipeline (used in the print loop)
    globals()["pd"] = pd

    parser = _build_parser()
    args = parser.parse_args()

    _setup_logging(getattr(args, "log_level", "INFO"))

    command_map = {
        "download": cmd_download,
        "features": cmd_features,
        "train": cmd_train,
        "backtest": cmd_backtest,
        "pipeline": cmd_pipeline,
        "report": cmd_report,
        "ui": cmd_ui,
        # TW Quant Cockpit v1
        "screener":     cmd_screener,
        "cockpit":      cmd_cockpit,
        "paper":        cmd_paper,
        "stock-report": cmd_stock_report,
        "mock-realtime": cmd_mock_realtime,
        # TW Quant Cockpit v0.2 Phase 4
        "import-csv":   cmd_import_csv,
        "data-check":   cmd_data_check,
        # TW Quant Cockpit v0.3
        "validate-score":       cmd_validate_score,
        "backtest-buy-points":  cmd_backtest_buy_points,
        "backtest-screener":    cmd_backtest_screener,
        # TW Quant Cockpit v0.3.1
        "universe-check":       cmd_universe_check,
        # TW Quant Cockpit v0.3.2
        "build-universe":       cmd_build_universe,
        "batch-import":         cmd_batch_import,
        # TW Quant Cockpit v0.3.3
        "clean-csv":            cmd_clean_csv,
        "data-audit":           cmd_data_audit,
        "import-plan":          cmd_import_plan,
        # TW Quant Cockpit v0.3.3-hotfix
        "import-xq-export":    cmd_import_xq_export,
        # TW Quant Cockpit v0.3.4
        "provider-status":        cmd_provider_status,
        "time-machine-preview":   cmd_time_machine_preview,
        "feature-preview":        cmd_feature_preview,
        # TW Quant Cockpit v0.3.6
        "strategy-preview":       cmd_strategy_preview,
        # TW Quant Cockpit v0.3.7
        "backtest-strategy-knowledge": cmd_backtest_strategy_knowledge,
        # TW Quant Cockpit v0.3.8
        "build-universe-manifest": cmd_build_universe_manifest,
        "batch-import-xq":         cmd_batch_import_xq,
        "universe-quality":        cmd_universe_quality,
        "run-validation-suite":    cmd_run_validation_suite,
        # TW Quant Cockpit v0.3.9
        "fetch-public-data":       cmd_fetch_public_data,
        "import-intraday":         cmd_import_intraday,
        "data-source-status":      cmd_data_source_status,
        "enrich-universe-data":    cmd_enrich_universe_data,
        # TW Quant Cockpit v0.3.10
        "fetch-daily-history":     cmd_fetch_daily_history,
        # TW Quant Cockpit v0.3.11
        "backtest-long-term-strategy": cmd_backtest_long_term_strategy,
        # TW Quant Cockpit v0.3.12
        "simulate-portfolio":          cmd_simulate_portfolio,
        # TW Quant Cockpit v0.3.14
        "signal-quality":              cmd_signal_quality,
        # TW Quant Cockpit v0.3.15
        "tune-rule-weights":           cmd_tune_rule_weights,
        # TW Quant Cockpit v0.3.16
        "auto-report":                 cmd_auto_report,
        # TW Quant Cockpit v0.3.17
        "scheduler-init-config":       cmd_scheduler_init_config,
        "scheduler-status":            cmd_scheduler_status,
        "scheduler-list":              cmd_scheduler_list,
        "scheduler-next-runs":         cmd_scheduler_next_runs,
        "scheduler-run":               cmd_scheduler_run,
        # TW Quant Cockpit v0.3.18
        "provider-health":             cmd_provider_health,
        # TW Quant Cockpit v0.3.19
        "provider-auto-fetch":         cmd_provider_auto_fetch,
        "data-freshness":              cmd_data_freshness,
        # TW Quant Cockpit v0.3.20
        "data-quality-gate":           cmd_data_quality_gate,
        # TW Quant Cockpit v0.3.21
        "update-data":                 cmd_update_data,
        "run-research":                cmd_run_research,
        "daily-workflow":              cmd_daily_workflow,
        "open-cockpit":                cmd_open_cockpit,
        # TW Quant Cockpit v0.3.22
        "usability-smoke-test":        cmd_usability_smoke_test,
        "usability-qa-report":         cmd_usability_qa_report,
        # TW Quant Cockpit v0.3.24
        "provider-reliability":        cmd_provider_reliability,
        # TW Quant Cockpit v0.3.26
        "hardened-backtest":           cmd_hardened_backtest,
        # TW Quant Cockpit v0.3.29
        "experiment-create":           cmd_experiment_create,
        "experiment-register-latest":  cmd_experiment_register_latest,
        "experiment-list":             cmd_experiment_list,
        "experiment-show":             cmd_experiment_show,
        "experiment-notebook":         cmd_experiment_notebook,
        "experiment-compare":          cmd_experiment_compare,
        "experiment-report":           cmd_experiment_report,
        "experiment-snapshot":         cmd_experiment_snapshot,
        # TW Quant Cockpit v0.3.28
        "rule-governance":             cmd_rule_governance,
        # TW Quant Cockpit v0.3.27
        "intraday-pipeline":           cmd_intraday_pipeline,
        "intraday-quality":            cmd_intraday_quality,
        "intraday-features":           cmd_intraday_features,
        # TW Quant Cockpit v0.3.25
        "universe-list":               cmd_universe_list,
        "universe-build-defaults":     cmd_universe_build_defaults,
        "universe-show":               cmd_universe_show,
        "universe-quality-score":      cmd_universe_quality_score,
        "universe-expand":             cmd_universe_expand,
        "universe-report":             cmd_universe_report,
        # TW Quant Cockpit v0.4.0
        "version-info":                cmd_version_info,
        "stable-release-check":        cmd_stable_release_check,
        "regression-suite":            cmd_regression_suite,
        "stable-release-report":       cmd_stable_release_report,
        # TW Quant Cockpit v0.4.1
        "api-token-check":             cmd_api_token_check,
        "api-cache-status":            cmd_api_cache_status,
        "api-fetch-diagnostics":       cmd_api_fetch_diagnostics,
        "api-cache-cleanup":           cmd_api_cache_cleanup,
        "api-fetch-production-report": cmd_api_fetch_production_report,
        # v0.4.3 Model Monitoring
        "model-monitoring":            cmd_model_monitoring,
        "model-monitoring-report":     cmd_model_monitoring_report,
        "model-registry-list":         cmd_model_registry_list,
        "model-register":              cmd_model_register,
        "prediction-log":              cmd_prediction_log,
        "prediction-review":           cmd_prediction_review,
        "drift-check":                 cmd_drift_check,
        "signal-degradation":          cmd_signal_degradation,
        "rule-vs-ml":                  cmd_rule_vs_ml,
        # v0.4.2 ML Feature Store
        "ml-feature-catalog":          cmd_ml_feature_catalog,
        "ml-feature-snapshot":         cmd_ml_feature_snapshot,
        "ml-labels":                   cmd_ml_labels,
        "ml-build-dataset":            cmd_ml_build_dataset,
        "ml-leakage-check":            cmd_ml_leakage_check,
        "ml-feature-quality":          cmd_ml_feature_quality,
        "ml-feature-importance":       cmd_ml_feature_importance,
        "ml-feature-store-report":     cmd_ml_feature_store_report,
        # v0.4.4 Intraday Replay Cockpit
        "intraday-replay":             cmd_intraday_replay,
        "intraday-replay-report":      cmd_intraday_replay_report,
        "replay-session-list":         cmd_replay_session_list,
        "replay-session-show":         cmd_replay_session_show,
        "replay-training-summary":     cmd_replay_training_summary,
        # v0.4.1.1 Strategy Knowledge Ingestion
        "strategy-knowledge-ingest":   cmd_strategy_knowledge_ingest,
        "strategy-knowledge-summary":  cmd_strategy_knowledge_summary,
        # v0.4.2.1 ML Knowledge Integration
        "ml-knowledge-integrate":      cmd_ml_knowledge_integrate,
        "ml-knowledge-leakage-check":  cmd_ml_knowledge_leakage_check,
        "ml-knowledge-feature-summary": cmd_ml_knowledge_feature_summary,
        # v0.4.5 Notification Center
        "notification-scan":           cmd_notification_scan,
        "notification-list":           cmd_notification_list,
        "notification-report":         cmd_notification_report,
        "notification-clear-read":     cmd_notification_clear_read,
        "notification-test":           cmd_notification_test,
        # v0.4.6 Portfolio Journal
        "journal-add":                 cmd_journal_add,
        "journal-list":                cmd_journal_list,
        "journal-show":                cmd_journal_show,
        "journal-review":              cmd_journal_review,
        "journal-report":              cmd_journal_report,
        "journal-summary":             cmd_journal_summary,
        "journal-link-replay":         cmd_journal_link_replay,
        # v0.4.7 Research Review Dashboard
        "research-review":             cmd_research_review,
        "research-review-report":      cmd_research_review_report,
        "research-review-summary":     cmd_research_review_summary,
        "research-review-actions":     cmd_research_review_actions,
        # v0.4.8 Research Assistant / Coach
        "research-coach":              cmd_research_coach,
        "research-coach-report":       cmd_research_coach_report,
        "research-coach-summary":      cmd_research_coach_summary,
        "research-coach-checklist":    cmd_research_coach_checklist,
        "research-coach-replay-plan":  cmd_research_coach_replay_plan,
        "research-coach-rule-queue":   cmd_research_coach_rule_queue,
        "research-coach-data-repair":  cmd_research_coach_data_repair,
        # v0.4.9 Research Workflow Automation
        "research-workflow":           cmd_research_workflow,
        "research-workflow-report":    cmd_research_workflow_report,
        "research-workflow-summary":   cmd_research_workflow_summary,
        "research-workflow-tasks":     cmd_research_workflow_tasks,
        "research-workflow-package":   cmd_research_workflow_package,
    }

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    handler = command_map.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)

    handler(args)


if __name__ == "__main__":
    main()

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

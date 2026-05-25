"""
config.py - Central configuration for the Taiwan Stock Trading Platform.

All tunable parameters live here so that other modules import from this
single source of truth.
"""

import os
from datetime import date

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "trading_data.db")
DATA_DIR = os.path.join(BASE_DIR, "data_cache")
MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports_output")

# Ensure directories exist when config is imported
for _d in [DATA_DIR, MODELS_DIR, REPORTS_DIR]:
    os.makedirs(_d, exist_ok=True)

# ---------------------------------------------------------------------------
# FinMind API
# ---------------------------------------------------------------------------
# Set your FinMind token here or via environment variable FINMIND_TOKEN
FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")

# ---------------------------------------------------------------------------
# Stock Universe  (top ~200 TWSE large/mid cap stocks)
# ---------------------------------------------------------------------------
TOP_N_STOCKS = 200

STOCK_UNIVERSE = [
    # Semiconductors & Technology
    "2330", "2454", "2303", "2308", "2317", "2382", "2395", "3711", "4938",
    "2379", "2344", "2351", "3008", "2376", "2337", "2449", "3034", "2385",
    "3045", "2392", "2408", "2409", "3481", "2415", "2356", "3035", "3036",
    "2369", "2388", "3711", "4958", "6415", "6488", "6505", "8046",
    # Financial / Banking / Insurance
    "2882", "2881", "2886", "2891", "2892", "2884", "2885", "2887", "2888",
    "2889", "2890", "5880", "2801", "2823", "2833", "2834", "2836",
    # Petrochemicals / Plastics
    "1301", "1303", "1326", "1402", "6505",
    # Steel / Materials
    "2002", "2006", "2007", "2008", "9910",
    # Electronics / Hardware
    "2357", "2207", "2474", "2498", "2059", "2360", "2371", "3231",
    "2365", "2366", "2367", "2368", "2377", "2387", "2397", "2401",
    "2404", "2405", "2406", "2407", "2412", "2413", "2420", "2423",
    "2426", "2429", "2431", "2436", "2439", "2441", "2442", "2443",
    "2444", "2448", "2450", "2451", "2453", "2455", "2456", "2457",
    "2458", "2459", "2460", "2461", "2462", "2463", "2464", "2465",
    "2466", "2467", "2468", "2469", "2470", "2471", "2472", "2473",
    "2475", "2476", "2477", "2478", "2480", "2481", "2482", "2483",
    "2484", "2485", "2486", "2487", "2488", "2489", "2490", "2491",
    "2492", "2493", "2495", "2496", "2497", "2499",
    # Consumer / Retail
    "2912", "2903", "2915", "2916", "9917", "9921", "9926",
    # Automotive / Transportation
    "2201", "2204", "2206", "2211", "2227", "2228",
    # Construction / Real Estate
    "2501", "2503", "2504", "2506", "2511", "2515", "2520", "2524",
    # Telecom
    "2412", "4904", "3045",
    # Food & Beverage
    "1201", "1210", "1213", "1215", "1216", "1217", "1218", "1219",
    "1220", "1225", "1227", "1229", "1231",
    # Miscellaneous
    "9904", "9907", "9908", "9912", "9914", "9918", "9919", "9920",
    "9922", "9923", "9924", "9925", "9927", "9928", "9929", "9930",
    "9931", "9933", "9934", "9935", "9937", "9938", "9939", "9940",
    "9941", "9942", "9943", "9944", "9945", "9946", "9947", "9948",
    "9949", "9950", "9951", "9953", "9955", "9956", "9957", "9958",
]

# Deduplicate while preserving order
_seen: set = set()
_deduped = []
for _s in STOCK_UNIVERSE:
    if _s not in _seen:
        _seen.add(_s)
        _deduped.append(_s)
STOCK_UNIVERSE = _deduped

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
DEFAULT_START_DATE = "2019-01-01"
DEFAULT_END_DATE = None  # None => today

# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ATR_PERIOD = 14
BB_PERIOD = 20
BB_STD = 2.0

SMA_PERIODS = [5, 10, 20, 60]
EMA_PERIODS = [12, 26]
MOMENTUM_PERIODS = [1, 5, 20]
VOL_SHORT_PERIOD = 20
VOL_LONG_PERIOD = 60

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
FORWARD_RETURN_DAYS = 5

LGBM_PARAMS = {
    "objective": "regression",
    "metric": "rmse",
    "num_leaves": 63,
    "learning_rate": 0.05,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "min_child_samples": 20,
    "n_estimators": 300,
    "random_state": 42,
    "verbose": -1,
}

LGBM_CLF_PARAMS = {
    "objective": "binary",
    "metric": "binary_logloss",
    "num_leaves": 63,
    "learning_rate": 0.05,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "min_child_samples": 20,
    "n_estimators": 300,
    "random_state": 42,
    "verbose": -1,
}

XGB_PARAMS = {
    "objective": "reg:squarederror",
    "eval_metric": "rmse",
    "max_depth": 6,
    "learning_rate": 0.05,
    "n_estimators": 300,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 5,
    "random_state": 42,
    "verbosity": 0,
}

XGB_CLF_PARAMS = {
    "objective": "binary:logistic",
    "eval_metric": "logloss",
    "max_depth": 6,
    "learning_rate": 0.05,
    "n_estimators": 300,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 5,
    "random_state": 42,
    "verbosity": 0,
}

# ---------------------------------------------------------------------------
# Risk Management
# ---------------------------------------------------------------------------
RISK_PER_TRADE = 0.015        # 1.5% of portfolio
MAX_POSITION_SIZE = 0.10      # cap 10% per position
MAX_DRAWDOWN_HALT = 0.20      # halt if drawdown > 20%

# ---------------------------------------------------------------------------
# Backtest
# ---------------------------------------------------------------------------
COMMISSION_RATE = 0.001425    # 0.1425% one-way
SELL_TAX_RATE = 0.003         # 0.3% sell tax (Taiwan)
SLIPPAGE_RATE = 0.001         # 0.1% per trade
INITIAL_CAPITAL = 1_000_000   # NTD 1 million

# ---------------------------------------------------------------------------
# Walk-forward validation
# ---------------------------------------------------------------------------
TRAIN_WINDOW_DAYS = 504   # ~2 trading years
TEST_WINDOW_DAYS = 63     # ~3 trading months

# ---------------------------------------------------------------------------
# Strategy
# ---------------------------------------------------------------------------
MOMENTUM_TOP_N = 10            # top N stocks for momentum strategy
MEAN_REVERSION_MAX_POS = 15    # max positions for mean reversion
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
BREAKOUT_VOLUME_MULTIPLIER = 1.5
BREAKOUT_LOOKBACK = 20         # 20-day high
ATR_STOP_MULTIPLIER = 2.0
ATR_TARGET_MULTIPLIER = 3.0
REBALANCE_FREQ = 5             # rebalance every N days (weekly ≈ 5)

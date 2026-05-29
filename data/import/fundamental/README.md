# data/import/fundamental/

This directory contains fundamental financial data fetched from public APIs.

## Files

- `fundamental.csv` — EPS, gross margin, operating margin, announcement dates (fetched, not committed)

## Schema

```
year,quarter,symbol,eps,gross_margin,operating_margin,operating_income,net_income,announcement_date,source,fetched_at
```

## Usage

```bash
python main.py fetch-public-data --stock 2454 --months 24
```

Note: `fundamental.csv` is gitignored (user data). Only this README is committed.

# Momentum Strategy Backtest vs. S&P 500

A vectorized backtest of a cross-sectional momentum strategy — rank stocks by trailing returns, hold the winners, rebalance monthly — benchmarked against buy-and-hold SPY on risk-adjusted metrics (Sharpe, Sortino, max drawdown, Calmar).

Built to demonstrate quantitative finance and Python skills for data/finance analyst internship applications: signal construction, look-ahead-bias-free backtesting, transaction cost modeling, and honest performance reporting.

## Results at a Glance

| Metric | Momentum Strategy | SPY Benchmark |
|---|---|---|
| Cumulative Return | 284.34% | 216.44% |
| CAGR | 34.95% | 29.23% |
| Annualized Volatility | 14.69% | 17.48% |
| Sharpe Ratio | 1.85 | 1.33 |
| Sortino Ratio | 3.17 | 2.37 |
| Max Drawdown | -13.80% | -31.84% |
| Calmar Ratio | 2.53 | 0.92 |

*Full numbers, rebalance log, and written interpretation in [`output/REPORT.md`](output/REPORT.md). See [Data Disclosure](#-data-disclosure-read-this) below — these results are a methodology demonstration, not investment advice.*

![Equity Curve](output/equity_curve.png)

## What This Project Demonstrates

- **Signal construction**: cross-sectional momentum ranking with a skip-month convention (standard in academic momentum research, Jegadeesh & Titman 1993) to avoid short-term reversal noise.
- **No look-ahead bias**: today's signal determines *tomorrow's* position — never today's own return. This is the single most common bug in amateur backtests, and it's explicitly commented in `src/backtest.py`.
- **Transaction cost modeling**: turnover-based cost charged at every rebalance, so returns aren't inflated by assuming free trading.
- **Proper risk-adjusted evaluation**: Sharpe, Sortino, Calmar, and max drawdown — not just raw returns, which hide risk.
- **Parameter sensitivity testing**: a grid search across lookback windows and portfolio sizes (in the notebook) to check whether results are robust or a curve-fit fluke.
- **Clean, vectorized Python**: no day-by-day loops over the entire history; pandas/numpy vectorized operations throughout.

## Project Structure

```
momentum-backtest/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── LICENSE
├── .gitignore
├── momentum_backtest_analysis.ipynb   # Full walkthrough notebook (start here)
├── data/
│   └── prices.csv                     # Daily close prices, 8 stocks + SPY, 2020–2024
├── src/
│   ├── generate_data.py               # Generates placeholder data (see disclosure below)
│   ├── fetch_data.py                  # Pulls REAL data via yfinance (run this yourself)
│   ├── backtest.py                    # Core backtest engine
│   ├── metrics.py                     # Sharpe, Sortino, max drawdown, etc.
│   └── run_analysis.py                # Main script: runs backtest, saves charts + report
└── output/
    ├── equity_curve.png
    ├── drawdown.png
    ├── rolling_sharpe.png
    ├── rebalance_weights.csv
    └── REPORT.md                      # Auto-generated results writeup
```

## How to Run

```bash
git clone <your-repo-url>
cd momentum-backtest
pip install -r requirements.txt

# Option A: use the included placeholder data (works immediately, no internet needed)
python src/run_analysis.py

# Option B: pull real market data first (requires internet access), then run
python src/fetch_data.py
python src/run_analysis.py
```

Or open `momentum_backtest_analysis.ipynb` in Jupyter for the full annotated walkthrough with inline charts and a parameter sensitivity grid.

## Strategy Logic

1. **Each month-end**, rank all 8 stocks by their total return over the trailing 6 months (excluding the most recent month, to avoid short-term reversal effects).
2. **Go long the top 3** ranked stocks, equal-weighted, for the next month.
3. **Rebalance monthly**, paying a 10 bps transaction cost on portfolio turnover each time.
4. **Compare** the resulting daily return stream against buy-and-hold SPY over the same period.

All parameters (lookback window, number of holdings, transaction cost, universe) are configurable at the top of `src/run_analysis.py`.

## ⚠️ Data Disclosure (Read This)

**The data shipped in `data/prices.csv` is realistic placeholder data, not real historical prices.**

This project was built in a sandboxed environment without access to Yahoo Finance's API. To make the project runnable immediately with zero setup friction, `src/generate_data.py` produces synthetic daily prices using Geometric Brownian Motion calibrated to each stock's approximate real-world historical annualized return and volatility (with a simple one-factor market correlation so relative behavior is realistic).

**Before treating any result here as a real finding:**
```bash
python src/fetch_data.py
```
This pulls real adjusted close prices via `yfinance` and overwrites `data/prices.csv`. Every other script works unchanged on real data — the pipeline doesn't know or care where the prices came from.

I'm disclosing this explicitly because presenting synthetic data as real would be misleading, and because **knowing the difference and being upfront about it is itself part of the analytical skill this project is meant to demonstrate.**

## Honest Limitations

- **Small, fixed universe**: 8 large-cap stocks, not selected via any systematic screen — a real research process would test on hundreds of names to avoid cherry-picking survivors.
- **Survivorship bias**: all 8 tickers exist today; a rigorous backtest would include delisted/failed companies from the same starting universe.
- **Simplified transaction costs**: flat bps on turnover, not a real market-impact or bid-ask model.
- **No regime testing**: 2020–2024 includes a sharp bear market (2022) and recovery, but five years is a short sample for drawing strong conclusions about a strategy's durability.

## Possible Extensions

- Test on a larger universe (S&P 500 constituents) with proper point-in-time index membership.
- Add a long/short version (long top decile, short bottom decile) to isolate the momentum factor from market beta.
- Walk-forward out-of-sample validation instead of a single backtest window.
- Compare against other factors (value, low-volatility) to see if momentum adds anything incremental.

## Tech Stack

Python · pandas · numpy · matplotlib · yfinance · Jupyter

---

*Built as a portfolio project for data/finance analyst internship applications. Not investment advice.*
# Portfolio-backtesting

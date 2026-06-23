# Momentum Strategy Backtest — Results Report

**Strategy:** Top 3 stocks by 6-month momentum, monthly rebalance, 10 bps transaction cost per rebalance.

**Benchmark:** Buy-and-hold SPY


## Performance Summary

| Metric | Momentum Strategy | SPY Benchmark |
|---|---|---|
| Cumulative Return | 284.34% | 216.44% |
| CAGR | 34.95% | 29.23% |
| Annualized Volatility | 14.69% | 17.48% |
| Sharpe Ratio | 1.85 | 1.33 |
| Sortino Ratio | 3.17 | 2.37 |
| Max Drawdown | -13.80% | -31.84% |
| Calmar Ratio | 2.53 | 0.92 |
| Win Rate | 52.92% | 54.24% |

## Rebalance Log (most recent 10)

| Date | Holdings | Momentum Scores | Turnover | Cost |
|---|---|---|---|---|
| 2024-02-29 | NVDA, AAPL, GOOGL | NVDA: 15.7%, AAPL: 2.0%, GOOGL: -1.0% | 0.00 | 0.000% |
| 2024-03-29 | AAPL, GOOGL, MSFT | AAPL: 8.4%, GOOGL: 2.0%, MSFT: -2.1% | 0.67 | 0.067% |
| 2024-04-30 | AAPL, NVDA, GOOGL | AAPL: 20.3%, NVDA: 17.7%, GOOGL: 9.5% | 0.67 | 0.067% |
| 2024-05-31 | AAPL, NVDA, GOOGL | AAPL: 26.5%, NVDA: 21.8%, GOOGL: 19.7% | 0.00 | 0.000% |
| 2024-06-28 | GOOGL, AAPL, XOM | GOOGL: 30.2%, AAPL: 28.4%, XOM: 19.0% | 0.67 | 0.067% |
| 2024-07-31 | GOOGL, AAPL, AMZN | GOOGL: 35.1%, AAPL: 23.2%, AMZN: 21.1% | 0.67 | 0.067% |
| 2024-08-30 | GOOGL, AMZN, XOM | GOOGL: 49.2%, AMZN: 38.4%, XOM: 37.1% | 0.67 | 0.067% |
| 2024-09-30 | AMZN, GOOGL, XOM | AMZN: 51.4%, GOOGL: 41.9%, XOM: 39.3% | 0.00 | 0.000% |
| 2024-10-31 | AMZN, MSFT, GOOGL | AMZN: 39.9%, MSFT: 34.3%, GOOGL: 31.1% | 0.67 | 0.067% |
| 2024-11-29 | MSFT, AMZN, GOOGL | MSFT: 49.4%, AMZN: 37.8%, GOOGL: 36.1% | 0.00 | 0.000% |

## Interpretation Notes

- The strategy outperformed SPY on a raw CAGR basis (34.95% vs 29.23%).
- Risk-adjusted (Sharpe), the strategy's ratio was higher than the benchmark's by 0.52.
- Max drawdown was -13.80% for the strategy vs -31.84% for SPY — a milder worst-case decline.
- This backtest uses a small, fixed universe of 8 large-cap stocks and synthetic/placeholder price data (see README) — results should be read as a demonstration of methodology, not as evidence the strategy works in live markets.
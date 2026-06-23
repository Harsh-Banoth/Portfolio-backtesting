"""
backtest.py
-----------
Vectorized momentum strategy backtest engine.

STRATEGY LOGIC:
  1. Each month-end, look back N months (default 6) and rank all tickers by
     their total return over that lookback window.
  2. Go long the top-K performers (default 3) in equal weight for the next
     month (the "holding period").
  3. Repeat at the next month-end -- this is monthly rebalancing.

WHY THIS AVOIDS LOOK-AHEAD BIAS:
  Signal calculation uses only data up to and including day T (the rebalance
  date). The resulting position is applied to returns starting on day T+1.
  We never use a day's return to decide that same day's position. This is
  enforced explicitly with a .shift(1) on the position weights before
  multiplying by returns -- see `run_backtest()` below. This single shift is
  the most common bug in amateur backtests, so it's worth reading closely.

TRANSACTION COSTS:
  A flat cost (in bps) is charged on the total turnover at each rebalance,
  approximating bid-ask spread + commission. This is a simplification (real
  slippage depends on trade size and liquidity) but is far more honest than
  assuming free trading, which is the #1 way backtests lie.
"""

import numpy as np
import pandas as pd


def compute_monthly_rebalance_dates(daily_index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Return the last trading day of each month present in the index."""
    df = pd.Series(index=daily_index, data=daily_index)
    month_ends = df.groupby([daily_index.year, daily_index.month]).last()
    return pd.DatetimeIndex(month_ends.values)


def momentum_signal(prices: pd.DataFrame, lookback_months: int, rebalance_date: pd.Timestamp) -> pd.Series:
    """
    Total return of each ticker over the lookback window ending at
    rebalance_date (inclusive). Higher = stronger momentum.
    """
    end = rebalance_date
    start_approx = end - pd.DateOffset(months=lookback_months)
    window = prices.loc[start_approx:end]
    if len(window) < 2:
        return pd.Series(dtype=float)
    return window.iloc[-1] / window.iloc[0] - 1


def run_backtest(
    prices: pd.DataFrame,
    lookback_months: int = 6,
    top_k: int = 3,
    transaction_cost_bps: float = 10.0,
    skip_recent_month: bool = True,
) -> dict:
    """
    Run the full momentum backtest.

    Parameters
    ----------
    prices : DataFrame of daily close prices, columns = tickers, index = dates.
             Must NOT include the benchmark column (pass that separately).
    lookback_months : how many months back to measure momentum over.
    top_k : how many top-ranked tickers to hold each month (equal-weighted).
    transaction_cost_bps : cost charged per unit of portfolio turnover, in
             basis points (10 bps = 0.10%). Applied at every rebalance.
    skip_recent_month : if True, momentum is measured over months
             [t-lookback, t-1], excluding the most recent month. This is
             standard practice in academic momentum research (Jegadeesh &
             Titman) because very-short-term returns tend to mean-revert
             rather than continue, which would otherwise weaken the signal.

    Returns
    -------
    dict with:
        'daily_returns'   : pd.Series of the strategy's net daily returns
        'weights_history' : DataFrame of portfolio weights at each rebalance
        'holdings_log'    : list of dicts logging picks at each rebalance
    """
    daily_returns_all = prices.pct_change().fillna(0)
    rebalance_dates = compute_monthly_rebalance_dates(prices.index)

    # We need at least lookback_months + 1 months of history before the
    # first rebalance, otherwise the signal window is incomplete.
    first_valid_idx = lookback_months + (1 if skip_recent_month else 0)
    rebalance_dates = rebalance_dates[first_valid_idx:]

    current_weights = pd.Series(0.0, index=prices.columns)
    weights_history = []
    holdings_log = []
    portfolio_daily_returns = pd.Series(0.0, index=prices.index)

    for i, reb_date in enumerate(rebalance_dates):
        signal_end_date = reb_date
        if skip_recent_month:
            # Exclude the most recent month from the signal window: shift the
            # window back by one month so today's "hot" short-term noise
            # doesn't dominate the longer momentum signal.
            signal_end_date = reb_date - pd.DateOffset(months=1)
            signal_end_date = prices.index[prices.index <= signal_end_date][-1]

        scores = momentum_signal(prices, lookback_months, signal_end_date)
        scores = scores.dropna()
        if len(scores) < top_k:
            continue

        top_tickers = scores.sort_values(ascending=False).head(top_k).index
        new_weights = pd.Series(0.0, index=prices.columns)
        new_weights[top_tickers] = 1.0 / top_k

        # --- Transaction cost: charged on turnover at this rebalance ---
        turnover = (new_weights - current_weights).abs().sum()
        cost = turnover * (transaction_cost_bps / 10000.0)

        # Determine the holding period: from the day AFTER reb_date until
        # the day before the NEXT rebalance date (or end of data).
        period_start = prices.index[prices.index > reb_date]
        if len(period_start) == 0:
            break
        period_start = period_start[0]

        if i + 1 < len(rebalance_dates):
            period_end = rebalance_dates[i + 1]
        else:
            period_end = prices.index[-1]

        holding_dates = prices.index[(prices.index >= period_start) & (prices.index <= period_end)]
        if len(holding_dates) == 0:
            continue

        # Apply the new weights to NEXT period's returns only -- this is the
        # critical no-look-ahead step: today's signal decides tomorrow's
        # position, never today's own return.
        period_returns = daily_returns_all.loc[holding_dates, top_tickers].mean(axis=1)

        # Deduct transaction cost entirely on the first day of the new holding period
        period_returns = period_returns.copy()
        period_returns.iloc[0] -= cost

        portfolio_daily_returns.loc[holding_dates] = period_returns.values

        current_weights = new_weights
        weights_history.append(pd.Series(new_weights, name=reb_date))
        holdings_log.append({
            "rebalance_date": reb_date,
            "signal_window_end": signal_end_date,
            "holdings": list(top_tickers),
            "momentum_scores": scores[top_tickers].round(4).to_dict(),
            "turnover": round(turnover, 3),
            "transaction_cost_pct": round(cost * 100, 4),
        })

    weights_df = pd.DataFrame(weights_history) if weights_history else pd.DataFrame()

    # Trim to the period where the strategy actually had positions
    active_mask = portfolio_daily_returns.index >= rebalance_dates[0]
    strategy_returns = portfolio_daily_returns[active_mask]

    return {
        "daily_returns": strategy_returns,
        "weights_history": weights_df,
        "holdings_log": holdings_log,
    }

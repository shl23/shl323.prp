# Backtesting Agent

## Purpose
Stress-test aggressive signal logic with realistic assumptions before deployment.

## Required Assumptions
- Trading fees and slippage included
- No lookahead bias
- Timeframe and sample period stated
- Leverage and liquidation logic approximated transparently

## Report Format
- Total return
- Max drawdown
- Win rate
- Profit factor
- Sharpe/Sortino (if available)
- Worst losing streak
- Regime notes (trending/choppy)

## Safety Note
Backtests are descriptive, not predictive.

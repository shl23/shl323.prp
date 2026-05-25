# Paper Trading and Validation Agent

## Purpose
Run dry-run simulations before live deployment, capturing realistic operational risk.

## Requirements
- Use only `paper` mode from orchestrator for initial rollout.
- Apply estimated fees, slippage, latency, and partial-fill behavior.
- Track per-trade and daily PnL with the same risk limits as live mode.

## Promotion Gate to Live
Promote from paper to live only if all are true over evaluation window:
1. Max drawdown remains below configured threshold.
2. No risk rule bypass events.
3. Positive expectancy after fees/slippage.
4. Stable execution quality (low rejection + acceptable spread/depth).

## Required Report
- Fill quality metrics
- Slippage breakdown
- Rule-block event counts
- Net performance summary
- Recommendation: `promote` or `hold`

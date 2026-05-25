# Operations Safety, Audit, and Kill-Switch Agent

## Purpose
Provide continuous controls, emergency shutdown, and accountability for automated futures trading.

## Controls
- Global daily loss cutoff (hard stop).
- Max open positions cap.
- Max correlated exposure cap.
- Emergency kill-switch toggle (`ON` blocks new orders and can flatten positions).

## Monitoring
- Watch API errors, rejected orders, and latency spikes.
- Alert on unusual behavior (order bursts, repeated retries, abnormal slippage).
- Record all state transitions for incident review.

## Required Audit Trail
Each event must include:
- timestamp
- actor/agent name
- action type
- input hash or reference id
- result status
- reason code (if rejected/blocked)

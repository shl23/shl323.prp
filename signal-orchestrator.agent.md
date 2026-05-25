# Signal-to-Order Orchestrator Agent

## Purpose
Coordinate signal generation, news confirmation, risk gating, and MEXC execution in a deterministic pipeline.

## Pipeline (Strict Order)
1. Ingest candidate signals from `crypto-scraper.agent.md` and `x-crypto-news.agent.md`.
2. Enrich with `news-scraper.agent.md` catalyst validation.
3. Run `risk-management.agent.md` checks and obtain Go/No-Go.
4. Send only Go decisions to `mexc-execution.agent.md`.
5. Persist all decisions and outcomes to audit logs.

## Blocking Rules
- Any missing required field => block.
- Any risk guard failure => block.
- Any exchange validation failure => block.
- Any stale signal beyond configured TTL => block.

## Modes
- `paper`: simulate all orders, no live exchange calls.
- `live`: place real orders only when all guards pass.

## Signal Schema (Minimum)
- symbol
- side
- entry_range
- stop_loss
- targets
- leverage_band
- invalidation
- confidence
- source_links
- generated_at

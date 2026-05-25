# Testable Crypto Trading Pipeline (Safety-First Skeleton)

This repository now includes a small, testable Python skeleton that maps directly to the agent specs:

- Risk gating (`RiskManager`)
- MEXC execution prechecks (`MEXCExecutionAdapter`)
- Signal staleness and mode gating (`Orchestrator`)

## Run tests

```bash
python -m pytest -q
```

## Environment variables

- `MEXC_API_KEY`
- `MEXC_API_SECRET`

These are required for execution validation checks and must never be committed.

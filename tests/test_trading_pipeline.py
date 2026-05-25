from datetime import datetime, timedelta, timezone

from src.trading_pipeline import Signal, RiskConfig, RiskManager, MEXCExecutionAdapter, Orchestrator


def mk_signal(**kwargs):
    base = dict(
        symbol="BTCUSDT",
        side="LONG",
        entry=100.0,
        stop_loss=98.0,
        leverage=10.0,
        confidence="High",
        invalidation="close below support",
        generated_at=datetime.now(timezone.utc),
    )
    base.update(kwargs)
    return Signal(**base)


def test_risk_blocks_killswitch():
    result = RiskManager.evaluate(mk_signal(), RiskConfig(equity=1000), 0, 0.0, True)
    assert result.decision == "NO_GO"


def test_risk_allows_valid_signal():
    result = RiskManager.evaluate(mk_signal(), RiskConfig(equity=1000), 0, 0.0, False)
    assert result.decision == "GO"
    assert result.notional > 0


def test_orchestrator_blocks_stale():
    stale = mk_signal(generated_at=datetime.now(timezone.utc) - timedelta(minutes=30))
    ok, reason = Orchestrator.gate(stale, "paper", ttl_minutes=15)
    assert not ok
    assert "stale" in reason.lower()


def test_execution_requires_credentials(monkeypatch):
    monkeypatch.delenv("MEXC_API_KEY", raising=False)
    monkeypatch.delenv("MEXC_API_SECRET", raising=False)
    risk = RiskManager.evaluate(mk_signal(), RiskConfig(equity=1000), 0, 0.0, False)
    ok, reason = MEXCExecutionAdapter.validate_for_execution(mk_signal(), risk, {"BTCUSDT"})
    assert not ok
    assert "missing" in reason.lower()

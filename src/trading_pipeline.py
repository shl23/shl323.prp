from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal
import os


Decision = Literal["GO", "NO_GO"]
Mode = Literal["paper", "live"]


@dataclass
class Signal:
    symbol: str
    side: Literal["LONG", "SHORT"]
    entry: float
    stop_loss: float
    leverage: float
    confidence: Literal["Low", "Medium", "High"]
    invalidation: str
    generated_at: datetime


@dataclass
class RiskConfig:
    equity: float
    risk_per_trade: float = 0.01
    max_open_positions: int = 3
    daily_loss_limit: float = 0.03


@dataclass
class RiskResult:
    decision: Decision
    reason: str
    notional: float = 0.0


class RiskManager:
    @staticmethod
    def evaluate(signal: Signal, config: RiskConfig, open_positions: int, daily_loss_pct: float, kill_switch_on: bool) -> RiskResult:
        if kill_switch_on:
            return RiskResult("NO_GO", "Kill-switch is ON")
        if open_positions >= config.max_open_positions:
            return RiskResult("NO_GO", "Max open positions reached")
        if daily_loss_pct >= config.daily_loss_limit:
            return RiskResult("NO_GO", "Daily loss limit breached")
        if not signal.invalidation:
            return RiskResult("NO_GO", "Missing invalidation")
        if signal.stop_loss <= 0:
            return RiskResult("NO_GO", "Invalid stop loss")

        stop_distance_pct = abs(signal.entry - signal.stop_loss) / signal.entry
        if stop_distance_pct <= 0:
            return RiskResult("NO_GO", "Zero stop distance")
        if stop_distance_pct < 0.001:
            return RiskResult("NO_GO", "Stop too tight for aggressive leverage")

        risk_amount = config.equity * config.risk_per_trade
        notional = risk_amount / stop_distance_pct
        return RiskResult("GO", "Risk checks passed", notional=round(notional, 2))


class MEXCExecutionAdapter:
    @staticmethod
    def credentials_present() -> bool:
        return bool(os.getenv("MEXC_API_KEY") and os.getenv("MEXC_API_SECRET"))

    @staticmethod
    def validate_for_execution(signal: Signal, risk: RiskResult, allowed_symbols: set[str], max_leverage: float = 50.0) -> tuple[bool, str]:
        if not MEXCExecutionAdapter.credentials_present():
            return False, "Missing MEXC credentials"
        if signal.symbol not in allowed_symbols:
            return False, "Symbol not tradable on MEXC futures"
        if risk.decision != "GO":
            return False, f"Risk blocked: {risk.reason}"
        if signal.leverage > max_leverage:
            return False, "Leverage exceeds max cap"
        return True, "Execution validation passed"


class Orchestrator:
    @staticmethod
    def is_stale(signal: Signal, ttl_minutes: int) -> bool:
        now = datetime.now(timezone.utc)
        return signal.generated_at < now - timedelta(minutes=ttl_minutes)

    @staticmethod
    def gate(signal: Signal, mode: Mode, ttl_minutes: int = 15) -> tuple[bool, str]:
        if Orchestrator.is_stale(signal, ttl_minutes):
            return False, "Signal is stale"
        if mode not in ("paper", "live"):
            return False, "Invalid mode"
        return True, "Signal accepted"

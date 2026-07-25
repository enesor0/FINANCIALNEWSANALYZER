"""Provider-neutral market-data domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True, slots=True)
class MarketInstrument:
    """A requested instrument and the display context selected by a user."""

    symbol: str
    name: str
    category: str

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("An instrument symbol is required.")
        if not self.name.strip():
            raise ValueError("An instrument name is required.")


@dataclass(frozen=True, slots=True)
class MarketQuote:
    """The most recent available quote for an instrument."""

    instrument: MarketInstrument
    price: float
    previous_close: float | None
    volume: int | None
    day_high: float | None
    day_low: float | None
    observed_at: datetime
    provider: str

    @property
    def change(self) -> float:
        return self.price - self.previous_close if self.previous_close is not None else 0.0

    @property
    def change_percent(self) -> float:
        if not self.previous_close:
            return 0.0
        return self.change / self.previous_close * 100


@dataclass(frozen=True, slots=True)
class MarketSnapshot:
    """A coherent collection of quotes received from one provider request."""

    quotes: tuple[MarketQuote, ...]

    @classmethod
    def from_quotes(cls, quotes: Iterable[MarketQuote]) -> "MarketSnapshot":
        return cls(tuple(quotes))


@dataclass(frozen=True, slots=True)
class PriceBar:
    """One daily OHLCV observation."""

    observed_at: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int | None


@dataclass(frozen=True, slots=True)
class PriceHistory:
    """Chronological price history for a single symbol."""

    symbol: str
    bars: tuple[PriceBar, ...]

    @classmethod
    def from_bars(cls, symbol: str, bars: Iterable[PriceBar]) -> "PriceHistory":
        return cls(symbol=symbol, bars=tuple(bars))

"""Focused outbound ports for market prices and historical bars."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from ...domain.entities.market_data import (
    InstrumentProfile,
    InstrumentSearchResult,
    MarketInstrument,
    MarketQuote,
    PriceBar,
)


class MarketQuoteProvider(Protocol):
    """Capability required to retrieve latest market quotes."""

    def get_market_snapshot(self, instruments: Sequence[MarketInstrument]) -> Sequence[MarketQuote]:
        """Return the latest available quote for each usable instrument."""


class PriceHistoryProvider(Protocol):
    """Capability required to retrieve price history for one symbol."""

    def get_history(self, symbol: str, days: int) -> Sequence[PriceBar]:
        """Return chronological daily price bars."""


class InstrumentSearchProvider(Protocol):
    """Capability required to discover instruments by name, ticker, or asset."""

    def search_instruments(self, query: str, limit: int = 12) -> Sequence[InstrumentSearchResult]:
        """Return matching provider instruments."""


class InstrumentProfileProvider(Protocol):
    """Capability required to retrieve detailed metadata for one instrument."""

    def get_instrument_profile(self, symbol: str) -> InstrumentProfile:
        """Return the latest available detailed instrument profile."""

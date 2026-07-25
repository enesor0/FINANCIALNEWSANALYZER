"""Use case for requesting a selected market overview."""

from __future__ import annotations

from collections.abc import Iterable

from ...domain.entities.market_data import MarketInstrument, MarketSnapshot
from ..ports.market_data_provider import MarketQuoteProvider


class GetMarketSnapshotUseCase:
    """Convert a UI selection into a provider-neutral market snapshot."""

    def __init__(self, quote_provider: MarketQuoteProvider) -> None:
        self._quote_provider = quote_provider

    def execute(self, instruments: Iterable[MarketInstrument]) -> MarketSnapshot:
        requested_instruments = tuple(instruments)
        if not requested_instruments:
            return MarketSnapshot.from_quotes(())
        return MarketSnapshot.from_quotes(self._quote_provider.get_market_snapshot(requested_instruments))

"""Use case for a selected instrument's daily price history."""

from __future__ import annotations

from ...domain.entities.market_data import PriceHistory
from ..ports.market_data_provider import PriceHistoryProvider


class GetPriceHistoryUseCase:
    """Retrieve provider-neutral historical bars for one symbol."""

    def __init__(self, history_provider: PriceHistoryProvider) -> None:
        self._history_provider = history_provider

    def execute(self, symbol: str, days: int) -> PriceHistory:
        normalized_symbol = symbol.strip().upper()
        if not normalized_symbol:
            raise ValueError("A symbol is required.")
        if days < 1:
            raise ValueError("History days must be at least one.")
        return PriceHistory.from_bars(
            normalized_symbol,
            self._history_provider.get_history(normalized_symbol, days),
        )

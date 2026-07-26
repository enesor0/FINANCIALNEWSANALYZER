"""Use case for discovering market instruments."""

from __future__ import annotations

from ...domain.entities.market_data import InstrumentSearchResult
from ..ports.market_data_provider import InstrumentSearchProvider


class SearchInstrumentsUseCase:
    """Validate and execute provider-neutral instrument discovery."""

    def __init__(self, provider: InstrumentSearchProvider) -> None:
        self._provider = provider

    def execute(self, query: str, limit: int = 12) -> tuple[InstrumentSearchResult, ...]:
        normalized_query = query.strip()
        if len(normalized_query) < 1:
            raise ValueError("A search query is required.")
        if len(normalized_query) > 80:
            raise ValueError("Search queries must be 80 characters or fewer.")
        return tuple(self._provider.search_instruments(normalized_query, min(max(limit, 1), 20)))

"""Use case for the global market-clock display."""

from __future__ import annotations

from ...domain.entities.market import Market
from ..ports.market_schedule_repository import MarketScheduleRepository


class GetMarketSchedulesUseCase:
    """Expose configured markets without coupling the UI to storage details."""

    def __init__(self, market_repository: MarketScheduleRepository) -> None:
        self._market_repository = market_repository

    def execute(self) -> tuple[Market, ...]:
        return tuple(self._market_repository.list_markets())

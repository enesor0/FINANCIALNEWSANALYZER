"""Port for obtaining the application's exchange schedules."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from ...domain.entities.market import Market


class MarketScheduleRepository(Protocol):
    """Read the configured exchange schedules."""

    def list_markets(self) -> Sequence[Market]:
        """Return all configured markets in display order."""

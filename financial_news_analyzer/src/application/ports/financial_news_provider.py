"""Port for sourcing provider-linked financial news."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from ...domain.entities.financial_news import FinancialNews


class FinancialNewsProvider(Protocol):
    """Read-only capability required by the news-analysis use case."""

    def search_news(self, company: str, limit: int = 12) -> Sequence[FinancialNews]:
        """Return provider articles relevant to ``company``."""

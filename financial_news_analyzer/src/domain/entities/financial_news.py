"""Domain model for a provider-linked financial news article."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class FinancialNews:
    """An immutable news article independent from its delivery provider."""

    id: str
    title: str
    summary: str
    source: str
    published_at: datetime
    company: str
    url: str | None = None

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("A news article must have an id.")
        if not self.title.strip():
            raise ValueError("A news article must have a title.")
        if not self.company.strip():
            raise ValueError("A news article must identify its company.")

    @property
    def text_for_analysis(self) -> str:
        """Return the provider text that the sentiment policy may analyse."""
        return f"{self.title} {self.summary}".strip()

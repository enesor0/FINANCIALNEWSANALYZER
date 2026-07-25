"""Domain rules for determining an exchange's weekday trading status."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import Enum
from typing import FrozenSet
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class MarketStatus(Enum):
    """Operational states that are meaningful to the market domain."""

    OPEN = "open"
    CLOSED = "closed"


class MarketRegion(Enum):
    """Global regions used to group exchange schedules."""

    AMERICAS = "americas"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia_pacific"
    MENA_AFRICA = "mena_africa"


@dataclass(frozen=True, slots=True)
class Market:
    """An exchange schedule with no dependency on UI or provider libraries.

    Holiday and early-close data deliberately live outside this entity.  The
    entity can therefore make only the rule it owns: normal weekday hours.
    """

    code: str
    name: str
    country_code: str
    country_flag: str
    timezone: str
    region: MarketRegion
    open_time: time
    close_time: time
    trading_weekdays: FrozenSet[int] = field(default_factory=lambda: frozenset({0, 1, 2, 3, 4}))
    currency: str | None = None

    def __post_init__(self) -> None:
        if not self.code.strip() or not self.name.strip():
            raise ValueError("A market code and name are required.")
        if not self.trading_weekdays.issubset({0, 1, 2, 3, 4, 5, 6}):
            raise ValueError("Trading weekdays must contain values from 0 to 6.")
        try:
            ZoneInfo(self.timezone)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Unknown timezone: {self.timezone}") from exc

    def status_at(self, now: datetime | None = None) -> MarketStatus:
        """Return the status at ``now`` in the market's local timezone."""
        local_now = self.local_time_at(now)
        if local_now.weekday() not in self.trading_weekdays:
            return MarketStatus.CLOSED
        if self._is_time_between(local_now.time(), self.open_time, self.close_time):
            return MarketStatus.OPEN
        return MarketStatus.CLOSED

    def local_time_at(self, now: datetime | None = None) -> datetime:
        """Normalize an instant to the market timezone.

        A naive input is interpreted as already being in the market's local
        timezone.  This makes the policy deterministic for callers and tests.
        """
        timezone = ZoneInfo(self.timezone)
        if now is None:
            return datetime.now(timezone)
        if now.tzinfo is None:
            return now.replace(tzinfo=timezone)
        return now.astimezone(timezone)

    def get_current_status(self, now: datetime | None = None) -> MarketStatus:
        """Compatibility name for callers that ask for the current status."""
        return self.status_at(now)

    def next_open_after(self, now: datetime | None = None) -> datetime:
        """Return the next scheduled opening, respecting the weekday policy."""
        local_now = self.local_time_at(now)
        candidate = local_now.replace(
            hour=self.open_time.hour,
            minute=self.open_time.minute,
            second=0,
            microsecond=0,
        )
        while candidate <= local_now or candidate.weekday() not in self.trading_weekdays:
            candidate += timedelta(days=1)
        return candidate

    def _next_open_after(self, now: datetime) -> datetime:
        """Backward-compatible alias for the former internal helper."""
        return self.next_open_after(now)

    def time_until_open_at(self, now: datetime | None = None) -> timedelta | None:
        """Return the duration until opening when the market is closed."""
        local_now = self.local_time_at(now)
        if self.status_at(local_now) is MarketStatus.OPEN:
            return None
        return self.next_open_after(local_now) - local_now

    def time_until_close_at(self, now: datetime | None = None) -> timedelta | None:
        """Return the duration until closing when the market is open."""
        local_now = self.local_time_at(now)
        if self.status_at(local_now) is not MarketStatus.OPEN:
            return None
        close_today = local_now.replace(
            hour=self.close_time.hour,
            minute=self.close_time.minute,
            second=0,
            microsecond=0,
        )
        if self.close_time < self.open_time and close_today <= local_now:
            close_today += timedelta(days=1)
        return max(close_today - local_now, timedelta())

    @staticmethod
    def _is_time_between(current: time, start: time, end: time) -> bool:
        if start <= end:
            return start <= current <= end
        return current >= start or current <= end

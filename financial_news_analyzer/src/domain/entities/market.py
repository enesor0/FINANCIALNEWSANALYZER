"""
Market Entity
Represents financial markets with status and schedule information
"""
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Optional, Dict, Any
from enum import Enum
import pytz

class MarketStatus(Enum):
    """Market operational status"""
    OPEN = "open"
    CLOSED = "closed"
    PRE_MARKET = "pre_market"
    AFTER_HOURS = "after_hours"
    HOLIDAY = "holiday"
    MAINTENANCE = "maintenance"

class MarketRegion(Enum):
    """Global market regions"""
    AMERICAS = "americas"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia_pacific"
    MENA_AFRICA = "mena_africa"

@dataclass
class Market:
    """
    Represents a financial market with comprehensive information
    
    Design Principles:
    - Single Responsibility: Manages market information only
    - Encapsulation: Internal time calculations hidden
    - Open/Closed: Extensible for new market types
    """
    
    # Core identifiers
    code: str  # e.g., "NYSE", "LSE", "TSE"
    name: str  # Full market name
    country_code: str  # ISO country code
    country_flag: str  # Unicode flag emoji
    
    # Geographic and timezone info
    timezone: str  # Timezone identifier
    region: MarketRegion
    
    # Trading schedule
    open_time: time  # Market opening time (local)
    close_time: time  # Market closing time (local)
    
    # Current status
    current_status: Optional[MarketStatus] = None
    
    # Additional information
    currency: Optional[str] = None
    indices: Optional[list] = None  # Main market indices
    website: Optional[str] = None
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize computed fields"""
        if self.metadata is None:
            self.metadata = {}
        
        if self.indices is None:
            self.indices = []
        
        # Update current status if not provided
        if self.current_status is None:
            self.current_status = self.get_current_status()
    
    def get_current_status(self, now: Optional[datetime] = None) -> MarketStatus:
        """Calculate status for a weekday schedule in the market's timezone.

        Exchange holiday and early-close calendars are not embedded in this
        entity. Those require a dedicated market-calendar data source.
        """
        try:
            tz = pytz.timezone(self.timezone)
            local_now = now.astimezone(tz) if now is not None else datetime.now(tz)
            if local_now.weekday() >= 5:
                return MarketStatus.CLOSED

            current_time = local_now.time()
            if self._is_time_between(current_time, self.open_time, self.close_time):
                return MarketStatus.OPEN
            return MarketStatus.CLOSED
        except Exception:
            return MarketStatus.CLOSED
    
    def _is_time_between(self, current: time, start: time, end: time) -> bool:
        """Check if current time is between start and end times"""
        if start <= end:
            return start <= current <= end
        else:  # Overnight trading (crosses midnight)
            return current >= start or current <= end
    
    def get_local_time(self) -> datetime:
        """Get current local time for this market"""
        try:
            tz = pytz.timezone(self.timezone)
            return datetime.now(tz)
        except Exception:
            return datetime.now()
    
    def get_formatted_time(self) -> str:
        """Get formatted local time string"""
        local_time = self.get_local_time()
        return local_time.strftime("%H:%M")
    
    def get_formatted_date(self) -> str:
        """Get formatted local date string"""
        local_time = self.get_local_time()
        return local_time.strftime("%m/%d")
    
    @property
    def status_emoji(self) -> str:
        """Get emoji representation of market status"""
        emoji_map = {
            MarketStatus.OPEN: "🟢",
            MarketStatus.CLOSED: "🔴",
            MarketStatus.PRE_MARKET: "🟡",
            MarketStatus.AFTER_HOURS: "🟠",
            MarketStatus.HOLIDAY: "🔵",
            MarketStatus.MAINTENANCE: "⚪"
        }
        return emoji_map.get(self.current_status, "❓")
    
    @property
    def status_color(self) -> str:
        """Get color code for market status"""
        color_map = {
            MarketStatus.OPEN: "#28a745",
            MarketStatus.CLOSED: "#dc3545",
            MarketStatus.PRE_MARKET: "#ffc107",
            MarketStatus.AFTER_HOURS: "#fd7e14",
            MarketStatus.HOLIDAY: "#007bff",
            MarketStatus.MAINTENANCE: "#6c757d"
        }
        return color_map.get(self.current_status, "#6c757d")
    
    @property
    def display_name(self) -> str:
        """Get display name with flag"""
        return f"{self.country_flag} {self.name}"
    
    @property
    def is_trading(self) -> bool:
        """Check if market is currently trading"""
        return self.current_status == MarketStatus.OPEN
    
    def get_trading_hours(self) -> str:
        """Get formatted trading hours"""
        return f"{self.open_time.strftime('%H:%M')} - {self.close_time.strftime('%H:%M')}"

    def _next_open_after(self, now: datetime) -> datetime:
        """Return the next weekday opening instant in ``now``'s timezone."""
        candidate = now.replace(
            hour=self.open_time.hour,
            minute=self.open_time.minute,
            second=0,
            microsecond=0,
        )
        while candidate <= now or candidate.weekday() >= 5:
            candidate += timedelta(days=1)
        return candidate
    
    def time_until_open(self) -> Optional[str]:
        """Get time until market opens (if closed)"""
        if self.current_status == MarketStatus.OPEN:
            return None
        
        try:
            tz = pytz.timezone(self.timezone)
            now = datetime.now(tz)
            
            next_open = self._next_open_after(now)
            time_diff = next_open - now
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            
            if hours > 24:
                days = hours // 24
                hours = hours % 24
                return f"{days}d {hours}h {minutes}m"
            else:
                return f"{hours}h {minutes}m"
                
        except Exception:
            return "Unknown"
    
    def time_until_close(self) -> Optional[str]:
        """Get time until market closes (if open)"""
        if self.current_status != MarketStatus.OPEN:
            return None
        
        try:
            tz = pytz.timezone(self.timezone)
            now = datetime.now(tz)
            
            close_today = now.replace(
                hour=self.close_time.hour,
                minute=self.close_time.minute,
                second=0,
                microsecond=0
            )
            
            if close_today <= now:
                return "Closing soon"
            
            time_diff = close_today - now
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            
            return f"{hours}h {minutes}m"
            
        except Exception:
            return "Unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "code": self.code,
            "name": self.name,
            "country_code": self.country_code,
            "country_flag": self.country_flag,
            "timezone": self.timezone,
            "region": self.region.value,
            "open_time": self.open_time.strftime("%H:%M"),
            "close_time": self.close_time.strftime("%H:%M"),
            "current_status": self.current_status.value,
            "currency": self.currency,
            "indices": self.indices,
            "website": self.website,
            "local_time": self.get_formatted_time(),
            "local_date": self.get_formatted_date(),
            "trading_hours": self.get_trading_hours(),
            "time_until_open": self.time_until_open(),
            "time_until_close": self.time_until_close(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Market':
        """Create Market instance from dictionary"""
        return cls(
            code=data["code"],
            name=data["name"],
            country_code=data["country_code"],
            country_flag=data["country_flag"],
            timezone=data["timezone"],
            region=MarketRegion(data["region"]),
            open_time=time.fromisoformat(data["open_time"]),
            close_time=time.fromisoformat(data["close_time"]),
            current_status=MarketStatus(data.get("current_status", "closed")),
            currency=data.get("currency"),
            indices=data.get("indices", []),
            website=data.get("website"),
            metadata=data.get("metadata", {})
        )
    
    def __str__(self) -> str:
        """String representation"""
        return f"Market({self.code}, {self.display_name}, {self.current_status.value})"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return self.__str__()

"""
In-Memory Market Data Repository Implementation
For development and testing purposes
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal
import random

from ...domain.repositories.market_data_repository import IMarketDataRepository
from ...domain.entities.market_data import MarketData, Stock, MarketMetrics, MarketType, Currency

class InMemoryMarketRepository(IMarketDataRepository):
    """
    In-memory implementation of market data repository
    Useful for development, testing, and demos
    """
    
    def __init__(self):
        """Initialize with sample market data"""
        self._stocks_storage: Dict[str, Stock] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample stock data for demo purposes"""
        sample_stocks = [
            Stock(
                symbol="AAPL",
                name="Apple Inc.",
                exchange="NASDAQ",
                current_price=Decimal("175.50"),
                currency=Currency.USD,
                open_price=Decimal("174.20"),
                high_price=Decimal("176.80"),
                low_price=Decimal("173.90"),
                previous_close=Decimal("173.50"),
                volume=45000000,
                average_volume=52000000,
                market_cap=Decimal("2750000000000")
            ),
            Stock(
                symbol="MSFT",
                name="Microsoft Corporation",
                exchange="NASDAQ",
                current_price=Decimal("415.30"),
                currency=Currency.USD,
                open_price=Decimal("412.80"),
                high_price=Decimal("417.20"),
                low_price=Decimal("411.50"),
                previous_close=Decimal("413.00"),
                volume=22000000,
                average_volume=28000000,
                market_cap=Decimal("3100000000000")
            ),
            # Add more sample stocks...
        ]
        
        for stock in sample_stocks:
            self._stocks_storage[stock.symbol] = stock
    
    def get_market_data(self, market_type: MarketType, limit: int = 100) -> Optional[MarketData]:
        """Get current market data"""
        try:
            stocks = list(self._stocks_storage.values())[:limit]
            
            if not stocks:
                return None
            
            # Calculate metrics
            total_stocks = len(stocks)
            gaining_stocks = sum(1 for s in stocks if s.is_gaining)
            losing_stocks = sum(1 for s in stocks if s.is_losing)
            unchanged_stocks = total_stocks - gaining_stocks - losing_stocks
            
            # Calculate averages
            changes = [s.change_percent for s in stocks if s.change_percent is not None]
            avg_change = sum(changes) / len(changes) if changes else 0.0
            
            volumes = [s.volume for s in stocks if s.volume is not None]
            total_volume = sum(volumes) if volumes else 0
            
            metrics = MarketMetrics(
                total_stocks=total_stocks,
                gaining_stocks=gaining_stocks,
                losing_stocks=losing_stocks,
                unchanged_stocks=unchanged_stocks,
                total_volume=total_volume,
                average_change_percent=avg_change,
                market_sentiment_score=avg_change / 100 if abs(avg_change) <= 100 else 0.0
            )
            
            return MarketData(
                stocks=stocks,
                metrics=metrics,
                market_type=market_type,
                data_source="In-Memory Mock Data",
                last_updated=datetime.now(),
                market_status="Open"
            )
            
        except Exception:
            return None
    
    def get_stock_by_symbol(self, symbol: str) -> Optional[Stock]:
        """Get stock data by symbol"""
        return self._stocks_storage.get(symbol.upper())
    
    def get_stocks_by_exchange(self, exchange: str, limit: int = 100) -> List[Stock]:
        """Get stocks by exchange"""
        results = [stock for stock in self._stocks_storage.values() 
                  if stock.exchange.upper() == exchange.upper()]
        return results[:limit]
    
    def get_top_gainers(self, limit: int = 10) -> List[Stock]:
        """Get top gaining stocks"""
        stocks_with_change = [s for s in self._stocks_storage.values() 
                             if s.change_percent is not None]
        
        stocks_with_change.sort(key=lambda x: x.change_percent, reverse=True)
        return stocks_with_change[:limit]
    
    def get_top_losers(self, limit: int = 10) -> List[Stock]:
        """Get top losing stocks"""
        stocks_with_change = [s for s in self._stocks_storage.values() 
                             if s.change_percent is not None]
        
        stocks_with_change.sort(key=lambda x: x.change_percent)
        return stocks_with_change[:limit]
    
    def get_most_active(self, limit: int = 10) -> List[Stock]:
        """Get most active stocks by volume"""
        stocks_with_volume = [s for s in self._stocks_storage.values() 
                             if s.volume is not None]
        
        stocks_with_volume.sort(key=lambda x: x.volume, reverse=True)
        return stocks_with_volume[:limit]
    
    def search_stocks(self, query: str, limit: int = 20) -> List[Stock]:
        """Search stocks by name or symbol"""
        query_lower = query.lower()
        results = []
        
        for stock in self._stocks_storage.values():
            if (query_lower in stock.symbol.lower() or 
                query_lower in stock.name.lower()):
                results.append(stock)
        
        return results[:limit]
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get overall market overview"""
        stocks = list(self._stocks_storage.values())
        
        if not stocks:
            return {"message": "No market data available"}
        
        gaining = sum(1 for s in stocks if s.is_gaining)
        losing = sum(1 for s in stocks if s.is_losing)
        total = len(stocks)
        
        changes = [s.change_percent for s in stocks if s.change_percent is not None]
        avg_change = sum(changes) / len(changes) if changes else 0.0
        
        volumes = [s.volume for s in stocks if s.volume is not None]
        total_volume = sum(volumes) if volumes else 0
        
        return {
            "total_stocks": total,
            "gaining_stocks": gaining,
            "losing_stocks": losing,
            "gaining_percentage": (gaining / total * 100) if total > 0 else 0,
            "average_change": avg_change,
            "total_volume": total_volume,
            "market_sentiment": "bullish" if avg_change > 1 else "bearish" if avg_change < -1 else "neutral",
            "last_updated": datetime.now().isoformat()
        }
    
    def get_sector_performance(self) -> Dict[str, float]:
        """Get performance by sector"""
        # Mock sector data
        return {
            "Technology": 2.3,
            "Healthcare": 1.1,
            "Financial": -0.5,
            "Energy": -1.2,
            "Consumer": 0.8,
            "Industrial": 0.3,
            "Materials": -0.2,
            "Utilities": 0.1,
            "Real Estate": -0.8,
            "Telecommunications": 0.5
        }
    
    def get_market_indices(self) -> List[Stock]:
        """Get major market indices"""
        indices = [
            Stock(
                symbol="SPY",
                name="SPDR S&P 500 ETF",
                exchange="NYSE",
                current_price=Decimal("445.20"),
                currency=Currency.USD,
                previous_close=Decimal("443.80"),
                volume=75000000
            ),
            Stock(
                symbol="QQQ",
                name="Invesco QQQ ETF",
                exchange="NASDAQ",
                current_price=Decimal("378.50"),
                currency=Currency.USD,
                previous_close=Decimal("376.20"),
                volume=45000000
            )
        ]
        return indices
    
    def save_market_data(self, market_data: MarketData) -> bool:
        """Save market data snapshot"""
        try:
            for stock in market_data.stocks:
                self._stocks_storage[stock.symbol] = stock
            return True
        except Exception:
            return False
    
    def get_historical_data(self, symbol: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get historical data for a symbol"""
        stock = self.get_stock_by_symbol(symbol)
        
        if not stock:
            return []
        
        # Generate mock historical data
        historical_data = []
        base_price = float(stock.current_price)
        
        for i in range(days_back, 0, -1):
            date = datetime.now() - timedelta(days=i)
            
            # Simulate price movements
            change_pct = random.uniform(-0.05, 0.05)  # ±5% daily change
            price = base_price * (1 + change_pct)
            
            historical_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(price * 0.998, 2),
                "high": round(price * 1.015, 2),
                "low": round(price * 0.985, 2),
                "close": round(price, 2),
                "volume": random.randint(1000000, 50000000)
            })
            
            base_price = price  # Use as base for next day
        
        return historical_data
    
    def get_market_status(self) -> Dict[str, Any]:
        """Get current market status information"""
        return {
            "market_open": True,
            "next_open": "2025-08-03 09:30:00",
            "next_close": "2025-08-02 16:00:00",
            "timezone": "America/New_York",
            "trading_day": True,
            "session": "regular",
            "last_updated": datetime.now().isoformat()
        }
